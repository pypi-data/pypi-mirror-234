from typing import Optional, List

from pydantic import BaseModel, Field

from mediaApiClient.content_meta_models import ContentMeta


class LightWeightCompilation(BaseModel):
    id: str
    title: str
    description: str
    provider: str
    tags: Optional[List[str]] = None
    contentIds: Optional[List[str]] = None


class CompilationRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    provider: Optional[str] = None
    tags: Optional[List[str]] = None
    contentIds: Optional[List[str]] = None


class CompilationWithContents(BaseModel):
    id: str
    title: str
    description: str
    provider: str
    tags: Optional[List[str]] = None
    contents: Optional[List[ContentMeta]] = None


class PageCompilationWithContents(CompilationWithContents):
    number: Optional[int] = Field(..., alias="number")
    size: Optional[int] = Field(..., alias="size")
    total_pages: Optional[int] = Field(..., alias="totalPages")
    total_elements: Optional[int] = Field(..., alias="totalElements")
    next: Optional[bool] = Field(..., alias="hasNext")
    previous: Optional[bool] = Field(..., alias="hasPrevious")
