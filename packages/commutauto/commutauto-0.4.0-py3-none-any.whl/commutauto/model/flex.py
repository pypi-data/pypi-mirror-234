from dataclasses import dataclass
from typing import List
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class Flex:
    CarId: int
    CarVin: str
    CarPlate: str
    CarModel: str
    CarNo: int
    Latitude: float
    Longitude: float
    EnergyLevel: int
    LastUseDate: str
    LastUse: int
    isPromo: bool
    BoardComputerType: int
    BookingStatus: int
    CarBrand: str
    CarColor: str
    CarSeatNb: int
    CarAccessories: List[int]
    IsElectric: bool
    VehiclePromotions: int
    CityID: int
    Distance: int = -1

    def __eq__(self, other):
        return self.Distance == other.Distance
        
    def __lt__(self, other):
        return self.Distance < other.Distance
        
    def __gt__(self, other):
        return self.Distance > other.Distance

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
