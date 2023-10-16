import datetime as dt
from typing import List, Dict, Union, Set
import heapq
import logging
from tenacity import RetryError
import logging

from commutauto.client import CommutautoClient
from commutauto.model import Station, Reservation, ReservationShort, Flex
from commutauto.booking_service.payload import get_payload
from commutauto.constants import (AspScript, 
                                             MAP_ROUTE_ENDPOINT, 
                                             Cities, 
                                             MINIMUM_SEARCH_RADIUS_KM,
                                             STATION_BASE_WAIT_TIME_SECOND,
                                             STATION_WAIT_TIME_JITTER_SECOND,
                                             STATION_EXPIRATION_TIME_SECOND,
                                             MAX_STATION_EXPIRATION_TIME_SECOND,
                                             CarSizes,
                                             CAR_MODELS_MAPPING_STR_ENUM,
                                             CAR_MODELS_TO_SIZE_MAPPING
                                            )
from commutauto.booking_service.retriers import get_available_station_search_retryer
import commutauto.booking_service.date_manager as dm
from commutauto.exceptions import AuthenticatedClientRequiredException, NoStationsWhithinRadiusException, OverlappingWithBookingsWindow

logger = logging.getLogger(__name__)

def parse_stations(station_dicts: List[Dict])-> List[Station]:
    stations = []
    for station_dict in station_dicts:
        stations.append(Station(**station_dict))
    return stations

def filter_available_stations(stations: List[Station]) -> List[Station]:
    available_stations = []
    for station in stations:
        if station.NbrRes == 0 or station.NbrRes == "0":
            available_stations.append(station)
    return available_stations

def filter_closest_station(stations: List[Station]) -> Station:
    min_distance = float("inf")
    closest_station = None
    for s in stations:
        if s.Distance < min_distance:
            min_distance = s.Distance
            closest_station = s
    return closest_station

def filter_car_size_station(stations: List[Station], allowed_sizes: Set[CarSizes]) -> Station:
    logger.info(f"Filter vehicles based on vehice size. Allowed sizes are: {allowed_sizes}.")
    allowed_stations = []
    for station in stations:
        model = CAR_MODELS_MAPPING_STR_ENUM[(station.Brand, station.Model)]
        car_size = CAR_MODELS_TO_SIZE_MAPPING[model]
        if car_size in allowed_sizes:
            allowed_stations.append(station)
    return allowed_stations

def check_stations_whithin_radius(stations: List[Station], radius: float):
    closest_station = filter_closest_station(stations)
    if closest_station and closest_station.Distance > radius:
        err_msg = f"Closest station is located at {closest_station.Distance} kilometers from the provided "
        err_msg += f"GPS coordinates. The specified search radius '{radius} kilometers' is lower than this distance."
        raise NoStationsWhithinRadiusException(err_msg)

def filter_vehicles_whithin_radius(vehicles: List[Union[Station, Flex]], radius: int, k: int = -1) -> List[Union[Station, Flex]]:
    logger.info(f"Filter vehicles based on radius {radius}km with k {k}.")

    if radius < MINIMUM_SEARCH_RADIUS_KM:
        raise ValueError(f"Search radius '{radius}' is lower than minimum allowed radius value '{MINIMUM_SEARCH_RADIUS_KM}'.")
    
    vehicles_whithin_radius = []
    minheap = []
    for vehicle in vehicles:
        heapq.heappush(minheap, vehicle)

    while minheap:
        if k != -1 and len(vehicles_whithin_radius) >= k:
            break
        vehicle = heapq.heappop(minheap)
        if vehicle.Distance > radius:
            break
        vehicles_whithin_radius.append(vehicle)
    return vehicles_whithin_radius

def prepare_and_validate_time_window(start_date: dt.datetime, 
                                end_date: dt.datetime, latitude: float, longitude: float):
    start_date = dm.convert_datetime_to_utc(start_date, latitude, longitude)
    end_date = dm.convert_datetime_to_utc(end_date, latitude, longitude)
    start_date, end_date = dm.round_booking_time_window(start_date, end_date)
    dm.validate_booking_request_time_window(start_date, end_date)
    dm.check_start_date_greater_than_quarter_hour_from_now(start_date)
    dm.check_start_date_sooner_than_one_month(start_date)
    return start_date, end_date

def check_existing_booking_overlap(client: CommutautoClient, start_date: dt.datetime, end_date: dt.datetime) -> List[ReservationShort]:
    reservations = get_car_booking_list(client)
    overlapping_reservations = dm.check_no_booking_intersection_with_search_window(start_date, end_date, reservations)
    return overlapping_reservations

def raise_reservation_overlap_error(overlapping_reservations: List[ReservationShort], start_date: dt.datetime, end_date: dt.datetime):
    err_msg = f"Provided search time window '[{start_date};{end_date}]' overlaps with the following reservations: \n"
    for res in overlapping_reservations:
        err_msg += f"{res} \n"
    raise OverlappingWithBookingsWindow(err_msg)

def get_stations(client: CommutautoClient, start_date: dt.datetime, 
                                end_date: dt.datetime, latitude: float, longitude: float, city_id: Cities, swap_bookings: bool = False):
    logger.info(f"Get available stations. City id: {city_id}, Latitude: {latitude}, Longitude: {longitude}, Start: {start_date}, End: {end_date}.")
    start_date, end_date = prepare_and_validate_time_window(start_date, end_date, latitude, longitude)

    if client.authenticated:
        overlaping_res = check_existing_booking_overlap(client, start_date, end_date)
        if overlaping_res and not swap_bookings:
            raise_reservation_overlap_error(overlaping_res, start_date, end_date)

    payload = get_payload(
        script_name=AspScript.GET_CAR_DISPONIBILITY,
        payload_args={
            "StartDateUTC": start_date, 
            "EndDateUTC": end_date, 
            "Latitude": latitude,
            "Longitude": longitude,
            "CityID": city_id.value
        }
    )
    response = client.post(
        commutauto_endpoint=MAP_ROUTE_ENDPOINT[type(AspScript.GET_CAR_DISPONIBILITY)],
        script_name=AspScript.GET_CAR_DISPONIBILITY, 
        payload=payload
    )
    if not response or "Stations" not in response:
        logger.info("No stations found.")
        return []
    
    stations = parse_stations(response["Stations"])
    logger.debug(f"Stations found: {stations}.")
    return stations

def get_available_stations_whithin_radius(client: CommutautoClient, start_date: dt.datetime, 
                                end_date: dt.datetime, latitude: float, longitude: float, city_id: Cities,
                                radius: float, k: int = -1, allowed_sizes: Set[CarSizes] = None, swap_bookings: bool = False)-> List[Station]:
    """
    Args:
        start_date (dt.datetime): UTC time
        end_date (dt.datetime): UTC time
        radius (float): kilometers
    """
    logger.info(f"Get available stations whithin radius {radius}.")

    stations = get_stations(client, start_date, end_date, latitude, longitude, city_id=city_id, swap_bookings=swap_bookings)
    check_stations_whithin_radius(stations, radius)
    available_stations = filter_available_stations(stations)
    stations_whithin_radius = filter_vehicles_whithin_radius(available_stations, radius, k)

    if allowed_sizes:
        stations_whithin_radius = filter_car_size_station(stations_whithin_radius, allowed_sizes)

    if stations_whithin_radius:
        logger.info("Found stations:")
        for station in stations_whithin_radius:
            logger.info(station)
    return stations_whithin_radius

def book_car_from_id(client: CommutautoClient, start_date: dt.datetime, 
                                end_date: dt.datetime, car_id: int, latitude: float, longitude: float, city_id: Cities, swap_bookings: bool = False) -> int:
    logger.info(f"Book station from id. Car id: {car_id}, City id: {city_id}, Latitude: {latitude}, Longitude: {longitude}, Start: {start_date}, End: {end_date}.")
    
    if not client.authenticated:
        raise AuthenticatedClientRequiredException()
    
    start_date, end_date = prepare_and_validate_time_window(start_date, end_date, latitude, longitude)

    if client.authenticated:
        overlaping_res = check_existing_booking_overlap(client, start_date, end_date)
        if overlaping_res:
            if not swap_bookings:
                raise_reservation_overlap_error(overlaping_res, start_date, end_date)
            else:
                for res in overlaping_res:
                    complete_res = get_car_booking(client, res.ReservationID)
                    cancel_car_booking(client, complete_res, latitude, longitude)
        
    payload = get_payload(
        script_name=AspScript.BOOK_CAR,
        payload_args={
            "StartDateUTC": start_date, 
            "EndDateUTC": end_date, 
            "CarId": car_id,
            "Latitude": latitude,
            "Longitude": longitude,
            "CityID": city_id.value
        }
    )

    response = client.post(
        commutauto_endpoint=MAP_ROUTE_ENDPOINT[type(AspScript.BOOK_CAR)],
        script_name=AspScript.BOOK_CAR, 
        payload=payload
    )
    if not response or \
        not "data" in response or \
        not "ReservationID" in response["data"] or \
        not(response["data"]["ReservationID"] > 0 and \
            response["data"]["Error"] == 0):
        logger.warn(f"Station booking failed.")
        return None
    logger.info(f"Successfull station booking.")
    return response["data"]["ReservationID"]

def get_car_booking(client: CommutautoClient, reservation_id: int) -> Reservation:
    logger.info(f"Get station booking. Reservation id: {reservation_id}.")

    if not client.authenticated:
        raise AuthenticatedClientRequiredException()
    
    payload = get_payload(
        script_name=AspScript.GET_BOOKING,
        payload_args={
            "ReservationID": reservation_id
        }
    )
    response = client.post(
        commutauto_endpoint=MAP_ROUTE_ENDPOINT[type(AspScript.GET_BOOKING)],
        script_name=AspScript.GET_BOOKING, 
        payload=payload
    )

    if not response or "Reservation" not in response:
        logger.info("No reservation found.")
        return None

    reservation = Reservation(**response["Reservation"])
    logger.info(f"Found reservation {reservation}.")
    return reservation

def cancel_car_booking(client: CommutautoClient, reservation: Reservation, latitude: float, longitude: float) -> bool:
    logger.info(f"Cancel station booking. Reservation: {reservation}, Latitude {latitude}, longitude {longitude}.")
    
    if not client.authenticated:
        raise AuthenticatedClientRequiredException()
    
    payload = get_payload(
        script_name=AspScript.CANCEL_BOOKING,
        payload_args={
            "StartDateUTC": reservation.StartDateUTC,
            "EndDateUTC": reservation.EndDateUTC,
            "ReservationID": reservation.ReservationID,
            "NewFeeType": reservation.FeeType,
            "ExpectedNbrKm": reservation.ExpectedNbrKm,
            "Latitude": latitude,
            "Longitude": longitude
        }
    )
    response = client.post(
        commutauto_endpoint=MAP_ROUTE_ENDPOINT[type(AspScript.CANCEL_BOOKING)],
        script_name=AspScript.CANCEL_BOOKING, 
        payload=payload)

    if not response or \
        not "data" in response or \
        not "ReservationID" in response["data"] or \
        not(response["data"]["ReservationID"] > 0 and response["data"]["Error"] == 0):
        logger.warn(f"Station booking cancellation failed.")
        return False
    logger.info(f"Station booking cancellation successfull.")
    return True

def parse_reservations(reservation_dicts: List[Dict])-> List[ReservationShort]:
    reservations = []
    for reservation_dict in reservation_dicts:
        reservations.append(ReservationShort(**reservation_dict))
    return reservations

def get_car_booking_list(client: CommutautoClient)-> List[ReservationShort]:
    logger.info(f"Get station booking list.")

    if not client.authenticated:
        raise AuthenticatedClientRequiredException()
    
    payload = get_payload(
        script_name=AspScript.GET_BOOKING_LIST,
        payload_args={}
    )
    response = client.post(
        commutauto_endpoint=MAP_ROUTE_ENDPOINT[type(AspScript.GET_BOOKING_LIST)],
        script_name=AspScript.GET_BOOKING_LIST, 
        payload=payload)
    
    if not response or "data" not in response:
        logger.info(f"No station bookings..")   
        return []
    reservations = parse_reservations(response["data"])
    if reservations:
        logger.info("Found station bookings:")
        for res in reservations:
            logger.info(res)
    return reservations

def available_station_search_with_retries(client: CommutautoClient, start_date: dt.datetime, 
                                end_date: dt.datetime, latitude: float, longitude: float, city_id: Cities, 
                                radius: float, allowed_sizes: Set[CarSizes] = None, swap_bookings: bool = False,
                                base_wait_time_second: int=STATION_BASE_WAIT_TIME_SECOND, 
                                wait_time_jitter_second: int=STATION_WAIT_TIME_JITTER_SECOND, 
                                expiration_time_second: int=STATION_EXPIRATION_TIME_SECOND, 
                                longer_pause_after_second: int=None, 
                                longer_pause_max_duration_second: int=None):
    logger.info(f"Search stations with retries. Wait time: {base_wait_time_second}s, Jitter: {wait_time_jitter_second}s, Expiration time: {expiration_time_second}.")
    
    if expiration_time_second > MAX_STATION_EXPIRATION_TIME_SECOND:
        raise ValueError(f"Retrying for more than {MAX_STATION_EXPIRATION_TIME_SECOND} is forbidden.")
    
    retryer = get_available_station_search_retryer(base_wait_time_second,
                                                   wait_time_jitter_second,
                                                   expiration_time_second,
                                                   longer_pause_after_second,
                                                   longer_pause_max_duration_second)
        
    station = None
    try:
        stations = retryer(get_available_stations_whithin_radius, client, start_date=start_date, 
                           end_date=end_date, latitude=latitude, longitude=longitude, radius=radius, city_id=city_id, 
                           allowed_sizes=allowed_sizes, swap_bookings=swap_bookings)
        if stations:
            station = stations[0]
    except RetryError:
        logging.exception("Ending retry loop.")
    return station