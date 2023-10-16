from typing import List, Dict
import logging
import traceback
from tenacity import RetryError
import math
import logging

from commutauto.client import CommutautoClient
from commutauto.model import Station, Flex, FlexBooking
from commutauto.booking_service.payload import get_payload
from commutauto.booking_service.station import filter_vehicles_whithin_radius

from commutauto.constants import LSIRoute, MAP_ROUTE_ENDPOINT, Cities, Branches
from commutauto.constants import ( FLEX_BASE_WAIT_TIME_SECOND,
                                              FLEX_WAIT_TIME_JITTER_SECOND,
                                              FLEX_EXPIRATION_TIME_SECOND,
                                              MAX_FLEX_EXPIRATION_TIME_SECOND
                                            )
from commutauto.booking_service.retriers import get_available_station_search_retryer
from commutauto.exceptions import AlreadyBookedFlexError, NoCurrentlyBookedFlex, AuthenticatedClientRequiredException

logger = logging.getLogger(__name__)

def get_available_flexes(client: CommutautoClient, branch_id: Branches, city_id: Cities, latitude: float=None, longitude: float=None):
    logger.info(f"Get available flexes. Branch id: {branch_id}, City id: {city_id}, Latitude: {latitude}, Longitude: {longitude}.")
    url_params = get_payload(
        script_name=LSIRoute.GET_FLEX_DISPONIBILITY,
        payload_args={
            "BranchID": branch_id.value,
            "CityID": city_id.value
        }
    )
    response = client.get(
        commutauto_endpoint=MAP_ROUTE_ENDPOINT[type(LSIRoute.GET_FLEX_DISPONIBILITY)],
        script_name=LSIRoute.GET_FLEX_DISPONIBILITY, 
        url_parameters=url_params
    )
    if not response or \
       not "d" in response or \
       not "Vehicles" in response["d"]:
        logger.info("No flexes found.")
        return []
    flexes = parse_flexes(response["d"]["Vehicles"], latitude, longitude)
    logger.debug(f"Flexes found: {flexes}.")
    return flexes

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # radius of the Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def parse_flexes(flexes_dicts: List[Dict], latitude: float=None, longitude: float=None)-> List[Flex]:
    flexes = []
    for flexes_dict in flexes_dicts:
        flex = None
        if latitude and longitude:
            dist = haversine(
                latitude, longitude, 
                flexes_dict["Latitude"], flexes_dict["Longitude"]
            )
            flex = Flex(**flexes_dict, Distance=dist)
        else:
            flex = Flex(**flexes_dict)
        flexes.append(flex)
    return flexes

def get_available_flexess_whithin_radius(client: CommutautoClient, latitude: float, longitude: float, 
                                radius: float, branch_id: Branches, city_id: Cities, k: int = -1)-> List[Station]:
    """
    Args:
        start_date (dt.datetime): UTC time
        end_date (dt.datetime): UTC time
        radius (float): kilometers
    """
    logger.info(f"Get available flexes whithin radius. Branch id: {branch_id}, City id: {city_id}, Latitude: {latitude}, Longitude: {longitude}, radius: {radius}, k: {k}.")

    if client.authenticated and get_current_flex(client, branch_id=branch_id):
        raise AlreadyBookedFlexError
    
    flexes = get_available_flexes(client, branch_id=branch_id, city_id=city_id, latitude=latitude, longitude=longitude)
    flexes_whithin_radius = filter_vehicles_whithin_radius(flexes, radius, k)
    if flexes_whithin_radius:
        logger.info("Found flexes:")
        for flex in flexes_whithin_radius:
            logger.info(flex)
    return flexes_whithin_radius

def book_flex_from_vin(client: CommutautoClient, car_vin: str, branch_id: Branches) -> int:
    logger.info(f"Book flex from vin. Car vin: {car_vin}, Branch_id: {branch_id}.")

    if not client.authenticated:
        raise AuthenticatedClientRequiredException()
    
    if get_current_flex(client, branch_id=branch_id):
        raise AlreadyBookedFlexError
    
    payload = get_payload(
        script_name=LSIRoute.BOOK_FLEX,
        payload_args={ "CarVIN": car_vin, "BranchID": branch_id.value }
    )

    response = client.post(
        commutauto_endpoint=MAP_ROUTE_ENDPOINT[type(LSIRoute.BOOK_FLEX)],
        script_name=LSIRoute.BOOK_FLEX, 
        payload=payload
    )

    if not response or \
        "d" not in response or \
        "Success" not in response["d"]:
        logger.warn(f"Flex booking failed.")
        return False
    logger.info(f"Successfull flex booking.")
    return response["d"]["Success"]

def cancel_flex_booking(client: CommutautoClient, branch_id: Branches) -> int:
    logger.info(f"Cancel flex booking. Branch_id: {branch_id}.")

    if not client.authenticated:
        raise AuthenticatedClientRequiredException()
    
    if not get_current_flex(client, branch_id=branch_id):
        raise NoCurrentlyBookedFlex
    
    payload = get_payload(
        script_name=LSIRoute.CANCEL_BOOKING_FLEX,
        payload_args={"BranchID": branch_id.value}
    )

    response = client.post(
        commutauto_endpoint=MAP_ROUTE_ENDPOINT[type(LSIRoute.CANCEL_BOOKING_FLEX)],
        script_name=LSIRoute.CANCEL_BOOKING_FLEX, 
        payload=payload
    )

    if not response or \
        not "d" in response or \
        not "Success" in response["d"]:
        logger.warn(f"Flex booking cancellation failed.")
        return False
    logger.info(f"Flex booking cancellation successfull.")
    return response["d"]["Success"]

def get_current_flex(client: CommutautoClient, branch_id: Branches):
    logger.info(f"Check if flex is currently booked.")
    if not client.authenticated:
        raise AuthenticatedClientRequiredException()
    
    payload = get_payload(
        script_name=LSIRoute.GET_CURRENT_FLEX,
        payload_args={"BranchID": branch_id.value}
    )
    response = client.get(
        commutauto_endpoint=MAP_ROUTE_ENDPOINT[type(LSIRoute.GET_CURRENT_FLEX)],
        script_name=LSIRoute.GET_CURRENT_FLEX,
        url_parameters=payload
    )

    if not response or not "d" in response:
        logger.info(f"No flex currently booked.")
        return None
    flex_booking = FlexBooking.from_get_flex_booking_json(response["d"])
    logger.info(f"Flex currently booked {flex_booking}.")
    return flex_booking

def available_flexes_search_with_retries(client: CommutautoClient, 
                                latitude: float, longitude: float,
                                branch_id: Branches, city_id: Cities,
                                radius: float, base_wait_time_second: int=FLEX_BASE_WAIT_TIME_SECOND, 
                                wait_time_jitter_second: int=FLEX_WAIT_TIME_JITTER_SECOND, 
                                expiration_time_second: int=FLEX_EXPIRATION_TIME_SECOND, 
                                longer_pause_after_second: int=None, 
                                longer_pause_max_duration_second: int=None):
    
    logger.info(f"Search flex with retries. Wait time: {base_wait_time_second}s, Jitter: {wait_time_jitter_second}s, Expiration time: {expiration_time_second}.")

    if expiration_time_second > MAX_FLEX_EXPIRATION_TIME_SECOND:
        raise ValueError(f"Retrying for more than {MAX_FLEX_EXPIRATION_TIME_SECOND} is forbidden.")
    
    if client.authenticated and get_current_flex(client, branch_id=branch_id):
        raise AlreadyBookedFlexError
    
    retryer = get_available_station_search_retryer(base_wait_time_second,
                                                   wait_time_jitter_second,
                                                   expiration_time_second,
                                                   longer_pause_after_second,
                                                   longer_pause_max_duration_second)
        
    flex = None
    try:
        flexes = retryer(get_available_flexess_whithin_radius, client, latitude=latitude, longitude=longitude, radius=radius, branch_id=branch_id, city_id=city_id)
        if flexes:
            flex = flexes[0]
    except RetryError:
        logging.exception("Ending retry loop.")
    return flex