import json
import secrets
import hashlib
import base64
import requests
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from typing import Tuple, Callable
import os
from dotenv import load_dotenv
import logging

from commutauto.client.auth_token import AuthToken
from commutauto.booking_service.payload import Payload
from commutauto.constants import CommutautoEndpoint, EnumRouteType
from commutauto.exceptions import GetAuthTokenFailure, RefreshAuthTokenFailure

logger = logging.getLogger(__name__)

class CommutautoClient():
    def __init__(self, 
            commutauto_security_api_endpoint = "https://securityservice.reservauto.net",
            authentication_header_value = "Basic Q29tbXVuYXV0b01vYmlsZUFwcDI6dUVWbEM0dzdiUkMyWlZtQWRjWG9xeXUxdQ==", 
            token_file_path=os.environ.get('COMMUTAUTO_TOKEN_FILE', "token.json"),
            authenticated=False):
        
        logger.info(f"Create CommutautoClient. Authentication is {'enabled' if authenticated else 'disabled'}.")

        load_dotenv()
        self.token_file_path = token_file_path
        self.commutauto_security_api_endpoint = commutauto_security_api_endpoint
        self.authentication_header_value = authentication_header_value
        self.authenticated = authenticated
        if self.authenticated:
            self.load_token_from_json()
    
    def load_token_from_json(self):
        try:
            logger.info(f"Load token from {self.token_file_path}.")
            with open(self.token_file_path) as f:
                self.token = AuthToken(**json.load(f))
        except FileNotFoundError:
            self.token = None
            logger.exception("Token file not found. Defaulting to None.")

    def get_token(self):
        logger.info(f"Get authentication token from API.")

        code_verifier = generate_random_code_verifier()
        code_challenge = encode_code_verifier_to_code_challenge(code_verifier)
        
        antiforgery_token, antiforgery_cookies, \
            return_url = get_and_parse_authentication_form(self.commutauto_security_api_endpoint, code_challenge)

        redirect_url, authentication_cookies = \
            post_authentication_form_and_parse_response(self.commutauto_security_api_endpoint, antiforgery_token,  antiforgery_cookies, return_url)
        
        redirect_oidc_uri, oidc_code = get_oidc_information(redirect_url, authentication_cookies)

        token = get_authentication_token(self.commutauto_security_api_endpoint, self.authentication_header_value, redirect_oidc_uri, oidc_code, code_verifier)
        
        if not token:
            raise GetAuthTokenFailure

        token.save_json(self.token_file_path)
        self.load_token_from_json()

    def refresh_token(self):
        logging.info(f"Refresh token.")

        if self.token:
            logging.info(f"Token found. Refreshing...")
            self.load_token_from_refresh_token(self.token.refresh_token)

    def load_token_from_refresh_token(self, refresh_token):
        token = get_token_from_refresh_token(self.commutauto_security_api_endpoint, self.authentication_header_value, refresh_token)
        if not token:
            raise RefreshAuthTokenFailure
        token.save_json(self.token_file_path)
        self.load_token_from_json()

    def authenticate(self):
        logging.info(f"Authenticate client.")

        if not self.token:
            self.get_token()
        elif self.token.is_expired():
            self.refresh_token()

    def get_token_header(self) -> dict:
        if not self.authenticated:
            return {}
        
        self.authenticate()
        token_header = {
            "authorization": f"{self.token.token_type} {self.token.access_token}"
        }
        return token_header

    def get(self, commutauto_endpoint: CommutautoEndpoint, script_name: EnumRouteType, url_parameters = Payload, headers: dict = None) -> dict:
        url = os.path.join(commutauto_endpoint.value, script_name.value)
        if headers is None:
            headers = {}
        headers.update(self.get_token_header())
        args = {
            "url": url,
            "headers": headers,
            "params": url_parameters.to_dict()
        }
        response = handle_requests_exceptions(requests.get, args)
        log_response(response)
        return parse_response_content(response) if response else None

    def post(self, commutauto_endpoint: CommutautoEndpoint, script_name: EnumRouteType, payload: Payload, headers: dict = None) -> dict:
        url = os.path.join(commutauto_endpoint.value, script_name.value)
        if headers is None:
            headers = {}
        headers.update(self.get_token_header())
        args = {
            "url": url,
            "headers": headers
        }
        
        payload_arg_name = "json"
        if payload.is_url_encoded():
            payload_arg_name = "data"
        args[payload_arg_name] = payload.to_dict()

        response = handle_requests_exceptions(requests.post, args)
        log_response(response)
        return parse_response_content(response) if response else None

def parse_response_content(response: requests.Response) -> dict:
    return json.loads(response.content.decode('utf-8'))

def handle_requests_exceptions(requests_method: Callable, args: dict) -> requests.Response:
    try:
        response = requests_method(**args)
        response.raise_for_status()
    except Exception:
        logger.exception("Exception occurred when sending request with Commutauto client.")
        return None
    return response

def get_authentication_token(commutauto_security_api_endpoint: str, authentication_header_value: str, redirect_oidc_uri: str, oidc_code: str, code_verifier: str) -> AuthToken:
    body = {
        "code": oidc_code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_oidc_uri,
        "code_verifier": code_verifier
    }
    headers = {"authorization": authentication_header_value }

    logging.info(f"Send get token http request.")
    logging.info(f"Headers: {headers}.")
    logging.info(f"Body: {body}.")

    response = requests.post(
        get_ask_token_url(commutauto_security_api_endpoint),
        data=body,
        headers=headers,
        stream=True,
        allow_redirects=False
        )
    log_response(response)

    if response.status_code != 200:
        return None

    token = extract_token_from_response(response)
    return token

def get_token_from_refresh_token(commutauto_security_api_endpoint: str, authentication_header_value: str, refresh_token_token: str) -> AuthToken:
    body = {
        "refresh_token": refresh_token_token,
        "grant_type": "refresh_token"
    }
    headers = {"authorization": authentication_header_value }
    response = requests.post(
        get_ask_token_url(commutauto_security_api_endpoint),
        data=body,
        headers=headers,
        stream=True,
        allow_redirects=False
        )
    if response.status_code != 200:
        return None

    token = extract_token_from_response(response)
    return token

def extract_token_from_response(response: requests.Response) -> AuthToken:
    token = AuthToken(**json.loads(response.content.decode('utf-8')))
    return token

def get_oidc_information(redirect_url: str, authentication_cookies: str) -> Tuple[str, str]:
    logger.info(f"Get oidc information.")

    response = requests.get(
            redirect_url,
            cookies=authentication_cookies,
            stream=True,
            allow_redirects=False
        )
    log_response(response)
    redirect_oidc_uri, oidc_code = parse_oidc_header_location(response.headers['location'])
    logger.info(f"Redirect oidc uri: {redirect_oidc_uri}.")
    logger.info(f"Redirect oidc code: {oidc_code}.")

    return redirect_oidc_uri, oidc_code

def parse_oidc_header_location(redirect_oidc_location: str) -> Tuple[str, str]:
    redirect_oidc_uri = redirect_oidc_location.split("#")[0]
    oidc_code = redirect_oidc_location.split("#")[1] \
                                .split("&")[0] \
                                .split("code=")[1]
    return redirect_oidc_uri, oidc_code

def post_authentication_form_and_parse_response(
        commutauto_security_api_endpoint: str, antiforgery_token: str, 
        antiforgery_cookies: RequestsCookieJar, return_url: str) -> Tuple[str, RequestsCookieJar]:
    logger.info(f"Post authentication form.")
    
    post_form_body = {
            "ReturnUrl": return_url,
            "ClientId": "CommunautoMobileApp2",
            "BranchId": "Communauto_Quebec",
            "Username": os.environ.get('USER_NAME'),
            "Password": os.environ.get('PASSWORD'),
            "__RequestVerificationToken": antiforgery_token,
            "RecaptchaResponse": '""'
        }

    response = requests.post(
        get_post_form_url(commutauto_security_api_endpoint),
        data=post_form_body,
        cookies=antiforgery_cookies,
        stream=True,
        allow_redirects=False
    )
    log_response(response)

    redirect_url = f"{commutauto_security_api_endpoint}{response.headers['location']}"
    authentication_cookies = response.cookies
    return redirect_url, authentication_cookies

def log_response(response: requests.Response):
    logger.debug(f"Response status code: {response.status_code}.")
    logger.debug(f"Response headers: {response.headers}.")
    logger.debug(f"Response content: {response.content}.")
    logger.debug(f"Response cookies: {response.cookies}.")

def get_and_parse_authentication_form(commutauto_security_api_endpoint: str, code_challenge: str) -> Tuple[str, RequestsCookieJar, str]:
    logger.info(f"Get authentication form.")
    ask_form_url = get_ask_form_url(commutauto_security_api_endpoint, code_challenge)
    response = requests.get(ask_form_url, allow_redirects=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    antiforgery_token = get_antiforgery_token_from_form(soup)
    return_url = get_return_url_from_form(soup)
    antiforgery_cookies = response.cookies
    logger.info(f"Antiforgery token: {antiforgery_token}.")
    logger.info(f"Antiforgery cookies: {antiforgery_cookies}.")
    logger.info(f"Return Url: {return_url}")
    return antiforgery_token, antiforgery_cookies, return_url

def get_antiforgery_token_from_form(soup: BeautifulSoup) -> str:
    form = soup.find('form')
    request_verification_token = form.find('input', {'name': '__RequestVerificationToken'})["value"]
    return request_verification_token

def get_return_url_from_form(soup: BeautifulSoup) -> str:
    form = soup.find('form')
    return_url = form.find('input', {"name": "ReturnUrl"})["value"]
    return return_url

def get_ask_form_url(commutauto_security_api_endpoint: str, code_challenge: str) -> str:
    return f"{commutauto_security_api_endpoint}/connect/authorize?client_id=CommunautoMobileApp2&redirect_uri=com.communauto.reservauto%3A%2Foidcredirect&scope=openid%20offline_access%20communautorestapi%20reservautofrontofficerestapi&response_type=code%20id_token&state=851ed6f4-c660-1fd6-19e9-143465bdec5c-72194b-ffdd480cabac-47dd&nonce=49ec9137-761a-9832-1536-9dcb27df0c30-6c4238-3fd9f84fce5f-d8cf&code_challenge={code_challenge}&code_challenge_method=S256&branch_id=1&prompt=login&hideTopHeader=true&ui_locales=en-CA"

def get_post_form_url(commutauto_security_api_endpoint: str) -> str:
    return f"{commutauto_security_api_endpoint}/Account/Login"

def get_ask_token_url(commutauto_security_api_endpoint: str) -> str:
    return f"{commutauto_security_api_endpoint}/connect/token"

def generate_random_code_verifier(segment_lengths=[8, 4, 4, 4, 12, 6, 12, 4]):
    # Generate a random string of the desired length (in bytes)
    num_bytes = int(sum(segment_lengths) / 2) + 1
    rand_bytes = secrets.token_bytes(num_bytes)

    # Convert the bytes to a hex string
    hex_str = rand_bytes.hex()

    # Insert hyphens between segments
    segments = []
    start_index = 0
    for length in segment_lengths:
        segments.append(hex_str[start_index:start_index+length])
        start_index += length
    random_code = '-'.join(segments)
    logger.info(f"Generated random code verifier: {random_code}.")
    return random_code

def encode_code_verifier_to_code_challenge(code_verifier):
    # Calculate the SHA256 hash of the code verifier
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    # Base64 URL encode the hash
    code_challenge = base64.urlsafe_b64encode(code_challenge).rstrip(b'=')
    # Convert the bytes to a string
    code_challenge = code_challenge.decode()
    logger.info(f"Encoded code verifier {code_verifier} to code challenge {code_challenge}.")
    return code_challenge

if __name__ == "__main__":
    load_dotenv()
    client = CommutautoClient()
    print(client.get_token_header())