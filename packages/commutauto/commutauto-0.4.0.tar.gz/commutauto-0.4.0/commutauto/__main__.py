import argparse
from datetime import datetime
import logging
from typing import Set

import commutauto.booking_service.station as bs_station
import commutauto.booking_service.flex as bs_flex
from commutauto.client import CommutautoClient
from commutauto.constants import (CITIES_MAPPING_STR_ENUM, Cities, 
                                             MAX_STATION_EXPIRATION_TIME_SECOND,
                                             MAX_FLEX_EXPIRATION_TIME_SECOND,
                                             CitiesToBranchesMapping,
                                             SIZES_MAPPING_STR_ENUM)

logger = logging.getLogger(__name__)

def parse_date(date: str) -> datetime:
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    return date

def search_station(city: str, latitude: float, longitude: float, radius: float, start_date: datetime, 
                   end_date: datetime, search_duration: int=None, book: bool=False, sizes: Set[str]=None, swap: bool = False):
    city = CITIES_MAPPING_STR_ENUM[city]

    if sizes:
        sizes = {SIZES_MAPPING_STR_ENUM[x] for x in sizes}

    client = CommutautoClient(authenticated=False)
    if book:
        client = CommutautoClient(authenticated=True)

    available_station = None
    if not search_duration:
        available_station = bs_station.get_available_stations_whithin_radius(client, 
                                start_date=start_date,
                                end_date=end_date,
                                latitude=latitude,
                                longitude=longitude,
                                city_id=city,
                                radius=radius,
                                allowed_sizes=sizes,
                                swap_bookings=swap,
                                k=1)[0]
    else:
        available_station = bs_station.available_station_search_with_retries(
            client, 
            start_date=start_date, 
            end_date=end_date, 
            latitude=latitude, 
            longitude=longitude, 
            radius=radius,
            city_id=city,
            allowed_sizes=sizes,
            swap_bookings=swap,
            expiration_time_second=search_duration*24*60*60
        )
    
    if not available_station:
        logger.info(f"No station found stopping search.")
        return
    logger.info(f"Station found: {available_station}. Ending search.")

    if not book:
        return
    
    reservation_id = bs_station.book_car_from_id(client, 
                                    start_date=start_date, 
                                    end_date=end_date, 
                                    car_id=available_station.CarID, 
                                    latitude=latitude, 
                                    longitude=longitude,
                                    city_id=city,
                                    swap_bookings=swap)
    if reservation_id:
        logger.info(f"Successfull station booking. Reservation id: {reservation_id}.")
            
def book_station(city: str, latitude: float, longitude: float, start_date: datetime, 
                   end_date: datetime, car_id: str, swap: bool = False):
    city = CITIES_MAPPING_STR_ENUM[city]
    client = CommutautoClient(authenticated=True)

    reservation_id = bs_station.book_car_from_id(client, 
                                    start_date=start_date, 
                                    end_date=end_date, 
                                    car_id=car_id, 
                                    latitude=latitude, 
                                    longitude=longitude,
                                    city_id=city,
                                    swap_bookings=swap)
    if reservation_id:
        logger.info(f"Successfull station booking. Reservation id: {reservation_id}.")

def list_station_bookings():
    client = CommutautoClient(authenticated=True)
    reservations = bs_station.get_car_booking_list(client)

    if not reservations:
        logger.info("No reservation found.")
        return
    
    logger.info(f"Found the following reservations:")
    
    for res in reservations:
        logger.info(res)

def cancel_station_booking(reservation_id: str):
    client = CommutautoClient(authenticated=True)

    reservation = bs_station.get_car_booking(client, reservation_id)

    if not reservation:
        logger.info(f"No reservation found with id {reservation_id}.")
        return
    
    cancel_success = bs_station.cancel_car_booking(client, reservation, latitude=reservation.Latitude, longitude=reservation.Longitude)
    if cancel_success:
        logger.info("Successfull flex booking cancellation.")
    else:
        logger.info("Station booking cancellation failed.")

def search_flex(city: str, latitude: float, longitude: float, radius: float, search_duration: int=None, book: bool=False):
    city = CITIES_MAPPING_STR_ENUM[city]
    branch = CitiesToBranchesMapping[city]

    client = CommutautoClient(authenticated=False)
    if book:
        client = CommutautoClient(authenticated=True)

    available_flex = None
    if not search_duration:
        available_flex = bs_flex.get_available_flexess_whithin_radius(client,
                                                                    branch_id=branch,
                                                                    city_id=city,
                                                                    latitude=latitude, 
                                                                    longitude=longitude, 
                                                                    radius=radius,
                                                                    k=1)[0]
    else:
        available_flex = bs_flex.available_flexes_search_with_retries(client, 
                                latitude=latitude,
                                longitude=longitude,
                                branch_id=branch,
                                city_id=city,
                                radius=radius,
                                expiration_time_second=search_duration*60*60)

    if not available_flex:
        logger.info(f"No flex found stopping search.")
        return
    logger.info(f"Flex found: {available_flex}. Ending search.")

    if not book:
        return
    
    booking_success = bs_flex.book_flex_from_vin(client, 
                                car_vin=available_flex.CarVin,
                                branch_id=branch)
    if booking_success:
        logger.info("Successfull flex booking.")
    else:
        logger.info("Flex booking failed.")

def book_flex(city: str, car_vin: str):
    city = CITIES_MAPPING_STR_ENUM[city]
    branch = CitiesToBranchesMapping[city]
    client = CommutautoClient(authenticated=True)

    booking_success = bs_flex.book_flex_from_vin(client, 
                                car_vin=car_vin,
                                branch_id=branch)
    if booking_success:
        logger.info("Successfull flex booking.")
    else:
        logger.info("Flex booking failed.")

def cancel_flex_booking(city: str):
    city = CITIES_MAPPING_STR_ENUM[city]
    branch = CitiesToBranchesMapping[city]
    client = CommutautoClient(authenticated=True)

    cancel_success = bs_flex.cancel_flex_booking(client, branch_id=branch)
    if cancel_success:
        logger.info("Successfull flex booking cancellation.")
    else:
        logger.info("Flex booking cancellation failed.")
    
# TODO: always assume credentials as env variables? Works whithout .env?
def main():
    parser = argparse.ArgumentParser('Communauto booking manager.')
    subparsers = parser.add_subparsers()

    ###############
    ### STATION ###
    ###############
    station = subparsers.add_parser('station', help='Handle search and booking of station cars.')
    station_parsers = station.add_subparsers()

    ### SEARCH ###
    station_search_parser = station_parsers.add_parser('search', help="Start a station search.")
    station_search_parser.set_defaults(func=search_station)
    station_search_parser.add_argument('--city',
                                       choices=CITIES_MAPPING_STR_ENUM.keys(), 
                                       help='In which city to search for a station car.')
    
    station_search_parser.add_argument('--latitude',
                                       type=float, 
                                       help='Latitude for the center of the search circle. Should be in the selected city.')
    
    station_search_parser.add_argument('--longitude',
                                       type=float, 
                                       help='Longitude for the center of the search circle. Should be in the selected city.')
    
    station_search_parser.add_argument('--radius',
                                       type=float, 
                                       help='Radius of the search circle in kilometers. Only stations whithin the circle will be considered.')
    
    station_search_parser.add_argument('--start_date',
                                       type=parse_date, 
                                       help="""Date at which the car booking will start. Time must be expressed in the timezone of the specified city.
                                               Time will be rounded to closest 15 minutes. Date format must be 'YYYY-MM-DDTHH:mm:ss'.""")

    station_search_parser.add_argument('--end_date',
                                       type=parse_date, 
                                       help="""Date at which the car booking will end. Time must be expressed in the timezone of the specified city.
                                               Time will be rounded to closest 15 minutes. end_date must be at least 30 minutes more than start_date.
                                                Date format must be 'YYYY-MM-DDTHH:mm:ss'.""")
    
    station_search_parser.add_argument('--search_duration', type=float, required=False,
                                       help=f"""Duration of the search in days. If specified, the search will continue until a car is found or 
                                                the search duration is greater than the specified value. If not specified, only one search will be conducted. 
                                                If after this time no car is found, the search will stop. Maximum value is {int(MAX_STATION_EXPIRATION_TIME_SECOND/(24*60*60))} days.""")

    station_search_parser.add_argument('--sizes',
                                       choices=SIZES_MAPPING_STR_ENUM.keys(),
                                       default=None,
                                       nargs='+',
                                       help='What car sizes to allow. Possible values are: compact, midsize and family. If not specified, all sizes are allowed.')
    
    station_search_parser.add_argument('--book', action='store_true', 
                                       help='If the flag is set then if a station is found during the search it will be booked automatically.')
    
    station_search_parser.add_argument('--swap', action='store_true', 
                                       help='If the flag is set and an overlapping booking already exists the search will be enabled. And in the event where a new booking is found, the old one will be deleted.')
    
    ### BOOK ###
    station_book_parser = station_parsers.add_parser('book', help="Book a station.")
    station_book_parser.set_defaults(func=book_station)
    station_book_parser.add_argument('--city',
                                       choices=CITIES_MAPPING_STR_ENUM.keys(), 
                                       help='In which city to search for a station car.')
    
    station_book_parser.add_argument('--latitude',
                                       type=float, 
                                       help='Latitude for the center of the search circle. Should be in the selected city.')
    
    station_book_parser.add_argument('--longitude',
                                       type=float, 
                                       help='Longitude for the center of the search circle. Should be in the selected city.')
    
    station_book_parser.add_argument('--start_date',
                                       type=parse_date, 
                                       help="""Date at which the car booking will start. Time must be expressed in the timezone of the specified city.
                                               Time will be rounded to closest 15 minutes. Date format must be 'YYYY-MM-DDTHH:mm:ss'.""")

    station_book_parser.add_argument('--end_date',
                                       type=parse_date, 
                                       help="""Date at which the car booking will end. Time must be expressed in the timezone of the specified city.
                                               Time will be rounded to closest 15 minutes. end_date must be at least 30 minutes more than start_date.
                                                Date format must be 'YYYY-MM-DDTHH:mm:ss'.""")
    station_book_parser.add_argument('--car_id',
                                       help='Station car id (like 1234).')

    station_book_parser.add_argument('--swap', action='store_true', 
                                       help='If the flag is set and an overlapping booking already exists it will be canceled before creating the new one.')
    
    
    ### CANCEL BOOKING ###
    station_cancel_parser = station_parsers.add_parser('cancel_booking', help="Cancel a station booking.")
    station_cancel_parser.set_defaults(func=cancel_station_booking)
    station_cancel_parser.add_argument('--reservation_id',
                                       help='Station reservation id (like 39762132).')
    
    ### LIST BOOKINGS ###
    station_list_parser = station_parsers.add_parser('list_booking', help="List all bookings.")
    station_list_parser.set_defaults(func=list_station_bookings)
    

    ############
    ### FLEX ###
    ############
    flex = subparsers.add_parser('flex', help='Handle search and booking of flex cars.')
    flex_parsers = flex.add_subparsers()

    ### SEARCH ###
    flex_search_parser = flex_parsers.add_parser('search', help="Start a station search.")
    flex_search_parser.set_defaults(func=search_flex)

    flex_search_parser.add_argument('--city',
                                       choices=CITIES_MAPPING_STR_ENUM.keys(), 
                                       help='In which city to search for a flex car.')
    
    flex_search_parser.add_argument('--latitude',
                                       type=float, 
                                       help='Latitude for the center of the search circle. Should be in the selected city.')
    
    flex_search_parser.add_argument('--longitude',
                                       type=float, 
                                       help='Longitude for the center of the search circle. Should be in the selected city.')
    
    flex_search_parser.add_argument('--radius',
                                       type=float, 
                                       help='Radius of the search circle in kilometers. Only flex cars whithin the circle will be considered.')
    
    flex_search_parser.add_argument('--search_duration', type=int, required=False,
                                       help=f"""Duration of the search in days. If specified, the search will continue until a car is found or 
                                                the search duration is greater than the specified value. If not specified, only one search will be conducted. 
                                                If after this time no car is found, the search will stop. Maximum value is {int(MAX_FLEX_EXPIRATION_TIME_SECOND/(60*60))} days.""")

    flex_search_parser.add_argument('--book', action='store_true', 
                                       help='If the flag is set then if a flex is found during the search it will be booked automatically.')
    
    ### BOOK ###
    flex_book_parser = flex_parsers.add_parser('book', help="Book a station.")
    flex_book_parser.set_defaults(func=book_flex)
    flex_book_parser.add_argument('--city',
                                       choices=CITIES_MAPPING_STR_ENUM.keys(), 
                                       help='In which city to search for a flex car.')
    
    flex_book_parser.add_argument('--car_vin',
                                       help='Vehicle identification number (like JTDLDTB37Z6239023).')

    ### CANCEL BOOKING ###
    flex_cancel_parser = flex_parsers.add_parser('cancel_booking', help="Cancel a station booking.")
    flex_cancel_parser.set_defaults(func=cancel_flex_booking)
    flex_cancel_parser.add_argument('--city',
                                       choices=CITIES_MAPPING_STR_ENUM.keys(), 
                                       help='In which city to search for a flex car.')

    args = vars(parser.parse_args())
    func = args.pop("func")
    func(**args)

if __name__ == "__main__":
    main()