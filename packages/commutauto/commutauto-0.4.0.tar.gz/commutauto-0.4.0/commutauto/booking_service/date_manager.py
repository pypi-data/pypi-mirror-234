import datetime
import pytz
from timezonefinder import TimezoneFinder
from typing import List
import logging

from commutauto.exceptions import ExpiredSearchException

logger = logging.getLogger(__name__)

def check_datetime_utc(date: datetime.datetime):
    if date.tzinfo != pytz.utc:
        raise ValueError(f"Date '{date}' must be expressed in UTC time.")


def infer_local_timezone(latitude: float, longitude: float) -> datetime.tzinfo:
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
    tz = pytz.timezone(timezone_str)
    logger.info(f"Inferred timezone: {tz}.")
    return tz

def convert_datetime_to_utc(date: datetime.datetime, latitude: float, longitude: float) -> datetime.datetime:
    tz = infer_local_timezone(latitude, longitude)
    utc_date = tz.localize(date).astimezone(pytz.utc)
    logger.info(f"Date {date} converted to UTC {utc_date}.")
    return utc_date

def round_to_quarter_hour(date):
    """Round datetime to nearest quarter-hour"""
    logger.info(f"Rounding date {date} to closest quarter hour.")

    quarter_ratio = date.minute / 15 - date.minute // 15
    round_up = int(quarter_ratio > 0.5)
    quarter_hour = ((date.minute // 15) + round_up) * 15
    if quarter_hour > 45:
        date += datetime.timedelta(hours=1)
    date = date.replace(minute=quarter_hour % 60)
    logger.info(f"Rounded date: {date}.")
    date = date.replace(second=0, microsecond=0)
    return date

def round_booking_time_window(start_date: datetime.datetime, end_date: datetime.datetime):
    start_date = round_to_quarter_hour(start_date)
    end_date = round_to_quarter_hour(end_date)
    return start_date, end_date

def validate_booking_request_time_window(start_date: datetime.datetime, end_date: datetime.datetime):
    if end_date <= start_date:
        raise ValueError(f"End date '{end_date}' must be later than start date '{start_date}'.")
    
    if end_date < start_date+ datetime.timedelta(minutes=30):
        raise ValueError(f"Booking duration must be at least 30 minutes. Got {end_date-start_date}")

def check_start_date_greater_than_quarter_hour_from_now(start_date):
    if datetime.datetime.now(pytz.utc) + datetime.timedelta(minutes=15) > start_date:
        raise ExpiredSearchException(f"Booking search start date '{start_date}' is in less than 15 minutes from now.")

def check_start_date_sooner_than_one_month(start_date):
    cur_date = datetime.datetime.now(pytz.utc)
    cur_date = cur_date.replace(hour = 0, minute = 0, second =0, microsecond=0)

    # round hour to 0am then add 31 days
    if cur_date + datetime.timedelta(days=32) < start_date:
        raise ExpiredSearchException(f"Booking search start date '{start_date}' is in more than 31 days from now.")
    
def check_no_booking_intersection_with_search_window(start_date: datetime.datetime, end_date: datetime.datetime, reservations: List) -> List:
    overlapping_reservations = []
    for res in reservations:
        interval1 = [start_date, end_date]
        interval2 = [res.StartDateUTC, res.EndDateUTC]

        if interval2[0] < interval1[0]:
            temp = interval2
            interval2 = interval1
            interval1 = temp

        if interval2[0] < interval1[1]:
            overlapping_reservations.append(res)
    return overlapping_reservations