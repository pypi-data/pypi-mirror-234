from abc import ABC, abstractmethod
import datetime
import logging

from commutauto.constants import AspScript, LSIRoute
from commutauto.booking_service.date_manager import check_datetime_utc, infer_local_timezone

logger = logging.getLogger(__name__)

class Payload(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError
    
    def is_url_encoded(self) -> bool:
        raise NotImplementedError

class GetCarDisponibilityPayload(Payload):
    def __init__(
            self, 
            StartDateUTC: datetime.datetime, # UTC timezone
            EndDateUTC: datetime.datetime, 
            Latitude: float, 
            Longitude: float, 
            CityID: int,
            CurrentLanguageID: int = 2, 
            Accessories: str = 0, 
            FeeType: str = None):
        
        check_datetime_utc(StartDateUTC)
        check_datetime_utc(EndDateUTC)

        self._StartDateUTC = StartDateUTC
        self._EndDateUTC = EndDateUTC
        self.Latitude = Latitude
        self.Longitude = Longitude
        self.CurrentLanguageID = CurrentLanguageID
        self.CityID = CityID
        self.Accessories = Accessories
        self.FeeType = FeeType

        self._LocalTimeZone = infer_local_timezone(self.Latitude, self.Longitude)

    def to_dict(self):
        d = {key: value for key, value in self.__dict__.items() if key[0] != "_"} # TODO: infer out timezone from coordinates
        d["StartDate"] = self._StartDateUTC.astimezone(self._LocalTimeZone).strftime('%d/%m/%Y %H:%M')
        d["EndDate"] = self._EndDateUTC.astimezone(self._LocalTimeZone).strftime('%d/%m/%Y %H:%M')
        d["StartDateISO"] = self._StartDateUTC.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        d["EndDateISO"] = self._EndDateUTC.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return d
    
    def is_url_encoded(self) -> bool:
        return True

class BookCarPayload(Payload):
    def __init__(
        self, 
        StartDateUTC: datetime.datetime, # UTC timezone
        EndDateUTC: datetime.datetime,
        CarId: int, 
        Latitude: float, 
        Longitude: float,
        CityID: int,
        CurrentLanguageID: int = 2, 
        ReservationCityID: str = "undefined",
        Accessories: int = 0,
        FeeType: str = None,
        DestinationId: int = None,
        Note: str = "",
        ExpectedNbrKm: str = None,
        AcceptAdditionalCharges: str = "undefined"
    ):
        
        check_datetime_utc(StartDateUTC)
        check_datetime_utc(EndDateUTC)

        self._StartDateUTC = StartDateUTC
        self._EndDateUTC = EndDateUTC
        self.CarId = CarId
        self.CurrentLanguageID = CurrentLanguageID
        self.CityID = CityID
        self.ReservationCityID = ReservationCityID
        self.Accessories = Accessories
        self.FeeType = FeeType
        self.DestinationId = DestinationId
        self.Note = Note
        self.ExpectedNbrKm = ExpectedNbrKm
        self.AcceptAdditionalCharges = AcceptAdditionalCharges

        self._LocalTimeZone = infer_local_timezone(Latitude, Longitude)


    def to_dict(self):
        d = {key: value for key, value in self.__dict__.items() if key[0] != "_"}
        d["StartDate"] = self._StartDateUTC.astimezone(self._LocalTimeZone).strftime('%d/%m/%Y')
        d["EndDate"] = self._EndDateUTC.astimezone(self._LocalTimeZone).strftime('%d/%m/%Y')
        d["StartTime"] = self._StartDateUTC.astimezone(self._LocalTimeZone).strftime('%H:%M')
        d["EndTime"] = self._EndDateUTC.astimezone(self._LocalTimeZone).strftime('%H:%M')
        return d
    
    def is_url_encoded(self) -> bool:
        return True

class GetBookingPayload(Payload):
    def __init__(
        self,
        ReservationID: int,
        CurrentLanguageID: int = 2, 
    ):
        self.ReservationID = ReservationID
        self.CurrentLanguageID = CurrentLanguageID

    def to_dict(self):
        return self.__dict__
    
    def is_url_encoded(self) -> bool:
        return True

class CancelBookingPayload(Payload):
    def __init__(self,
                    StartDateUTC: datetime.datetime,
                    EndDateUTC: datetime.datetime,
                    ReservationID: int,
                    NewFeeType: int,
                    ExpectedNbrKm: int, 
                    Latitude: float, 
                    Longitude: float,
                    CurrentLanguageID: int = 2,
                    Action: str = "Supprimer",
                    NewDestinationID: str = "",
                    NewNote: str = ""):
        
        check_datetime_utc(StartDateUTC)
        check_datetime_utc(EndDateUTC)
        
        self._StartDateUTC = StartDateUTC
        self._EndDateUTC = EndDateUTC
        self.ReservationID = ReservationID
        self.NewFeeType = NewFeeType
        self.ExpectedNbrKm = ExpectedNbrKm
        self.NewDestinationID = NewDestinationID
        self.NewNote = NewNote
        self.Action = Action
        self.CurrentLanguageID = CurrentLanguageID

        self._LocalTimeZone = infer_local_timezone(Latitude, Longitude)


    def to_dict(self):
        d = {key: value for key, value in self.__dict__.items() if key[0] != "_"}
        d["StartDate"] = self._StartDateUTC.astimezone(self._LocalTimeZone).strftime('%d/%m/%Y')
        d["EndDate"] = self._EndDateUTC.astimezone(self._LocalTimeZone).strftime('%d/%m/%Y')
        d["StartTime"] = self._StartDateUTC.astimezone(self._LocalTimeZone).strftime('%H:%M')
        d["EndTime"] = self._EndDateUTC.astimezone(self._LocalTimeZone).strftime('%H:%M')
        return d
    
    def is_url_encoded(self) -> bool:
        return True

class GetBookingListPayload(Payload):
    def __init__(
        self,
        CurrentLanguageID: int = 2,
        Type: int = 1
    ):
        self.Type = Type
        self.CurrentLanguageID = CurrentLanguageID

    def to_dict(self):
        return self.__dict__
    
    def is_url_encoded(self) -> bool:
        return True
    
class GetFlexDisponibilityUrlParameter(Payload):
    def __init__(
            self, 
            BranchID: int,
            CityID: int,
            LanguageID: int = 2
        ):
        self.BranchID = BranchID
        self.CityID = CityID
        self.LanguageID = LanguageID
    def to_dict(self):
        return self.__dict__
    
    def is_url_encoded(self) -> bool:
        return True
    
class BookFlexPayload(Payload):
    def __init__(
            self,
            CarVIN: str,
            BranchID: int
        ):
        self.BranchID = BranchID
        self.CarVIN = CarVIN
    def to_dict(self):
        return self.__dict__
    
    def is_url_encoded(self) -> bool:
        return False
    
class CancelFlexBookingPayload(Payload):
    def __init__(
            self, 
            BranchID: int
        ):
        self.BranchID = BranchID
    def to_dict(self):
        return self.__dict__
    
    def is_url_encoded(self) -> bool:
        return False

class GetCurrentFlex(Payload):
    def __init__(
            self, 
            BranchID: int
        ):
        self.BranchID = BranchID
    def to_dict(self):
        return self.__dict__
    
    def is_url_encoded(self) -> bool:
        return False

PAYLOAD_FACTORY = {
    AspScript.GET_CAR_DISPONIBILITY: GetCarDisponibilityPayload,
    AspScript.BOOK_CAR: BookCarPayload,
    AspScript.GET_BOOKING: GetBookingPayload,
    AspScript.CANCEL_BOOKING: CancelBookingPayload,
    AspScript.GET_BOOKING_LIST: GetBookingListPayload,
    LSIRoute.GET_FLEX_DISPONIBILITY: GetFlexDisponibilityUrlParameter,
    LSIRoute.BOOK_FLEX: BookFlexPayload,
    LSIRoute.CANCEL_BOOKING_FLEX: CancelFlexBookingPayload,
    LSIRoute.GET_CURRENT_FLEX: GetCurrentFlex
}

def get_payload(script_name: str, payload_args: dict) -> Payload:
    return PAYLOAD_FACTORY[script_name](**payload_args)