from typing import List, Optional
from pydantic import BaseModel


class LightWeightService(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
