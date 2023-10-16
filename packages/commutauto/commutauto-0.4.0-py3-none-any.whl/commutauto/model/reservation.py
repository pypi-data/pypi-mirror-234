from datetime import datetime
import pytz
import json
import logging

from commutauto.booking_service.date_manager import convert_datetime_to_utc

logger = logging.getLogger(__name__)

class Reservation:
    def __init__(self, ReservationID, CarID, CarNo, CarPlateNumber, StationID, StationName, StationPin, StartDate, StartDateISO, EndDate, EndDateISO, StartDateNextRes, StartDateNextResISO, CarMemoID, CarMemoStationID, FeeType, DestinationID, DestinationName, ReservationStatus, RPTEndDate, CarBranchID, CarAccessories, CarModel, CarDescription, CarEquipment, Accessories, ExpectedNbrKm, Note, LSI, Current, Longitude, Latitude, StationMemo, CarMemo, CreditCardAvailable, CityId, RentalId, Status):
        self.ReservationID = ReservationID
        self.CarID = CarID
        self.CarNo = CarNo
        self.CarPlateNumber = CarPlateNumber
        self.StationID = StationID
        self.StationName = StationName
        self.StationPin = StationPin
        self.StartDateNextRes = StartDateNextRes
        self.StartDateNextResISO = StartDateNextResISO
        self.CarMemoID = CarMemoID
        self.CarMemoStationID = CarMemoStationID
        self.FeeType = FeeType
        self.DestinationID = DestinationID
        self.DestinationName = DestinationName
        self.ReservationStatus = ReservationStatus
        self.RPTEndDate = RPTEndDate
        self.CarBranchID = CarBranchID
        self.CarAccessories = CarAccessories
        self.CarModel = CarModel
        self.CarDescription = CarDescription
        self.CarEquipment = CarEquipment
        self.Accessories = Accessories
        self.ExpectedNbrKm = ExpectedNbrKm
        self.Note = Note
        self.LSI = LSI
        self.Current = bool(Current)
        self.Longitude = Longitude
        self.Latitude = Latitude
        self.StationMemo = StationMemo
        self.CarMemo = CarMemo
        self.CreditCardAvailable = CreditCardAvailable
        self.CityId = CityId
        self.RentalId = RentalId
        self.Status = Status
        
        self.StartDateUTC = datetime.strptime(StartDateISO, '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.utc)
        self.EndDateUTC = datetime.strptime(EndDateISO, '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.utc)

        # NOTE: same result can be obtained using local time + gps based timezone inference
        # Don't know which is best. commutauto APIs are not consistant with date format
        # StartDate = datetime.strptime(StartDate, '%m/%d/%Y %I:%M:%S %p')
        # EndDate = datetime.strptime(EndDate, '%m/%d/%Y %I:%M:%S %p')
        # self.StartDateUTC = convert_datetime_to_utc(StartDate, self.Latitude, self.Longitude)
        # self.EndDateUTC = convert_datetime_to_utc(EndDate, self.Latitude, self.Longitude)

    def __str__(self):
        d = {key: value.isoformat() if isinstance(value, datetime) else value for key, value in self.__dict__.items()}
        return json.dumps(d, indent=4)

class ReservationShort:
    def __init__(self, ReservationID, StartDate, EndDate, CarID, CarNo, Station, Longitude, Latitude, Status, Current, Upcoming, LSI, npc, BranchID, RentalID, HasZone):
        self.ReservationID = ReservationID
        self.CarID = CarID
        self.CarNo = CarNo
        self.Station = Station
        self.Longitude = float(Longitude)
        self.Latitude =  float(Latitude)
        self.Status = Status
        self.Current = Current
        self.Upcoming = Upcoming
        self.LSI = LSI
        self.npc = npc
        self.BranchID = BranchID
        self.RentalID = RentalID
        self.HasZone = HasZone

        StartDate = datetime.strptime(StartDate, '%Y/%m/%d %H:%M:%S')
        EndDate = datetime.strptime(EndDate, '%Y/%m/%d %H:%M:%S')
        self.StartDateUTC = convert_datetime_to_utc(StartDate, self.Latitude, self.Longitude)
        self.EndDateUTC = convert_datetime_to_utc(EndDate, self.Latitude, self.Longitude)

    def __str__(self):
        d = {key: value.isoformat() if isinstance(value, datetime) else value for key, value in self.__dict__.items()}
        return json.dumps(d, indent=4)