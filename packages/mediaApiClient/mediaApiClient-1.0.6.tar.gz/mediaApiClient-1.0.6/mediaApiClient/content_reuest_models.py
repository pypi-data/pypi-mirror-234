from typing import Optional
from enum import Enum
from datetime import date
from pydantic import BaseModel


class IntervalFilter(Enum):
    ALL = "ALL"
    OTHER = "OTHER"
    TODAY = "TODAY"
    YESTERDAY = "YESTERDAY"
    WEEK = "WEEK"
    MONTH = "MONTH"


class ContentType(Enum):
    FILM = "FILM"
    SERIAL = "SERIAL"
    SHOW = "SHOW"
    ALL = "ALL"


class Service(Enum):
    AMEDIATEKA = "1"
    START = "2"
    PREMIER = "3"
    ALL = "ALL"


class ContentFilter(BaseModel):
    type: str
    intervalFilter: str
    serviceId: str
    dateFrom: Optional[date] = None
    dateTo: Optional[date] = None
