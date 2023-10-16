from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, constr
from mediaApiClient.services_models import LightWeightService


class EUserStatus(Enum):
    ACTIVE = "ACTIVE"
    REMOVED = "REMOVED"


class UserStatus(BaseModel):
    id: int
    title: str
    description: Optional[str] = None


class LightWeightAccount(BaseModel):
    id: int
    accountId: str
    status: UserStatus
    created: datetime
    services: Optional[List[str]] = None


class AccountFullInfo(BaseModel):
    accountId: str
    connectedServices: Optional[List[LightWeightService]] = None


class AccountToCreate(BaseModel):
    accountId: constr(strip_whitespace=True, min_length=1)
    servicesIds: List[int]
