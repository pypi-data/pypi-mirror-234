from typing import List, Optional, TypeVar, Generic
from pydantic import BaseModel, Field


class Rating(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    rating: Optional[float] = None


class Genre(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Country(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Actor(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Studio(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    logo: Optional[str] = None


class Poster(BaseModel):
    url: Optional[str] = None
    resizeable: Optional[bool] = None


class SerieMeta(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    originalTitle: Optional[str] = None
    description: Optional[str] = None
    number: Optional[int] = None
    duration: Optional[int] = None


class FilmMeta(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    originalTitle: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None


class SeasonMeta(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    originalTitle: Optional[str] = None
    description: Optional[str] = None
    number: Optional[int] = None
    episodes: Optional[List[SerieMeta]] = None


class ContentMeta(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    originalTitle: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    provider: Optional[str] = None
    releaseDate: Optional[int] = None
    ageRating: Optional[int] = None
    slug: Optional[str] = None
    ratingList: Optional[List[Rating]] = None
    genreList: Optional[List[Genre]] = None
    actors: Optional[List[Actor]] = None
    countryList: Optional[List[Country]] = None
    studioList: Optional[List[Studio]] = None
    horizontalPoster: Optional[Poster] = None
    verticalPoster: Optional[Poster] = None


class FilmFullMeta(ContentMeta):
    episode: FilmMeta


class SerialFullMeta(ContentMeta):
    seasons: List[SeasonMeta]


T = TypeVar('T')


class PageWithElements(BaseModel, Generic[T]):
    number: Optional[int] = Field(..., alias="number")
    size: Optional[int] = Field(..., alias="size")
    total_pages: Optional[int] = Field(..., alias="totalPages")
    total_elements: Optional[int] = Field(..., alias="totalElements")
    first: Optional[bool] = Field(..., alias="first")
    last: Optional[bool] = Field(..., alias="last")
    next: Optional[bool] = Field(..., alias="next")
    previous: Optional[bool] = Field(..., alias="previous")
    elements: Optional[List[T]] = Field(..., alias="elements")
