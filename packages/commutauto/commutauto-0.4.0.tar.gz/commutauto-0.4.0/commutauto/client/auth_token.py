import time
import json

import logging

logger = logging.getLogger(__name__)

class AuthToken():
    def __init__(
            self, 
            id_token: str, 
            access_token: str, 
            expires_in: int, 
            token_type: str, 
            refresh_token: str, 
            scope: str,
            expiration_time=None):
        
        logger.info(f"Create AuthToken.")

        self.id_token = id_token
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.refresh_token = refresh_token
        self.scope = scope

        self.expiration_time = expiration_time
        if not expiration_time:
            self.expiration_time = time.time() + expires_in
        logger.info(f"AuthToken expires at {self.expiration_time} seconds.")
    
    def is_expired(self):
        expired = time.time() > self.expiration_time
        logger.info(f"Check if auth token is expired. Expired status is {expired}.")
        return expired

    def save_json(self, token_file_path):
        logger.info(f"Save auth token to file {token_file_path}.")
        json.dump(self.__dict__, open(token_file_path, "w"), indent=4)
        
