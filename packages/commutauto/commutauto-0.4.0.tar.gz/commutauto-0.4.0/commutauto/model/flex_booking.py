from typing import Optional
import datetime
import json
import re
import logging

logger = logging.getLogger(__name__)

class FlexBooking:
    def __init__(self, BookingId: int, BookingStatus: int, CarId: int, CarModel: str,
                 CarNo: int, CarPlate: str, CarVin: str, CityID: int, CreditCardAvailable: bool,
                 EndDateUTC: datetime.datetime, EnergyLevel: Optional[float], InUse: bool, IsElectric: bool,
                 LastUse: int, LastUseDateUTC: datetime.datetime, Latitude: float, Longitude: float,
                 RentalId: int, ReservationStartDateUTC: Optional[datetime.datetime], StartDateUTC: datetime.datetime,
                 VehiclePromotions: Optional[str], CurrentDateUTC: datetime.datetime) -> None:
        self.BookingId = BookingId
        self.BookingStatus = BookingStatus
        self.CarId = CarId
        self.CarModel = CarModel
        self.CarNo = CarNo
        self.CarPlate = CarPlate
        self.CarVin = CarVin
        self.CityID = CityID
        self.CreditCardAvailable = CreditCardAvailable
        self.EndDateUTC = EndDateUTC
        self.EnergyLevel = EnergyLevel
        self.InUse = InUse
        self.IsElectric = IsElectric
        self.LastUse = LastUse
        self.LastUseDateUTC = LastUseDateUTC
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.RentalId = RentalId
        self.ReservationStartDateUTC = ReservationStartDateUTC
        self.StartDateUTC = StartDateUTC
        self.VehiclePromotions = VehiclePromotions
        self.CurrentDateUTC = CurrentDateUTC

    @classmethod
    def from_get_flex_booking_json(cls, json_data):
        if "Booking" not in json_data or "UtcDates" not in json_data:
            return None
        
        booking_dict, utc_dates = json_data["Booking"], json_data["UtcDates"]
        del booking_dict["EndDate"]
        del booking_dict["StartDate"]
        del booking_dict["LastUseDate"]
        del booking_dict["ReservationStartDate"]
        del booking_dict["__type"]

        booking_dict["CurrentDateUTC"] = parse_iso_with_milliseconds_to_utc_datetime(utc_dates["CurrentDate"])
        booking_dict["EndDateUTC"] = parse_iso_with_milliseconds_to_utc_datetime(utc_dates["EndDate"])
        booking_dict["StartDateUTC"] = parse_iso_with_milliseconds_to_utc_datetime(utc_dates["StartDate"])
        booking_dict["LastUseDateUTC"] = parse_iso_with_milliseconds_to_utc_datetime(utc_dates["LastUseDate"])
        booking_dict["ReservationStartDateUTC"] = parse_iso_with_milliseconds_to_utc_datetime(utc_dates["ReservationStartDate"])

        flex_booking = cls(**booking_dict)
        return flex_booking
    def __str__(self):
        d = {key: value.isoformat() if isinstance(value, datetime.datetime) else value for key, value in self.__dict__.items()}
        return json.dumps(d, indent=4)
    
def parse_iso_with_milliseconds_to_utc_datetime(date: str)-> datetime.datetime:
    # remove  millisecond "\"2023-03-03T01:57:02.495417+00:00\"" (before the +)
    if date == "null":
        return None
    date = date.strip("\"")
    date = re.sub(r'\.\d+', '', date)
    isodate= datetime.datetime.fromisoformat(date)
    return isodate