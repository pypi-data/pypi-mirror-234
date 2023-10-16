from dataclasses import dataclass
import json
from typing import Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class Station:
    StationID: int
    StationNo: str
    Longitude: float
    Latitude: float
    Distance: float
    StationName: str
    CarID: int
    CarNo: str
    NbrRes: int
    Accessories: int
    lngModel: int
    Brand: str
    Model: str
    Color: str
    CarDesc: str
    HasZone: bool
    EstimatedRangeKm: Optional[float] = None

    def __eq__(self, other):
        return self.Distance == other.Distance
        
    def __lt__(self, other):
        return self.Distance < other.Distance
        
    def __gt__(self, other):
        return self.Distance > other.Distance

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
