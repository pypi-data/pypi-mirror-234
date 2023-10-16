from typing import List, Optional
from pydantic import BaseModel


class Language(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None


class Streams(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    license: Optional[str] = None
    url: Optional[str] = None
    language: Optional[Language] = None


class StreamUrl(BaseModel):
    thumbUrl: Optional[str] = None
    streams: Optional[List[Streams]] = None
