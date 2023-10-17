from datetime import datetime
from enum import Enum
from fastapi_camelcase import CamelModel
from pydantic import Field
from typing import List, Optional

from ..models import Label
from ..types import ObjectId


class NewsArticleType(str, Enum):
    NEWS = "news"
    PRESS_RELEASE = "press release"


class NewsArticle(CamelModel):
    company_id: ObjectId = Field(..., description="Internal company ID")
    url: str = Field(..., description="Article URL")
    type: NewsArticleType = Field(..., description="Type of article")
    published: datetime = Field(..., description="When the article was published")
    snippet: str = Field(
        ..., description="Snippet of the article mentioning the company"
    )
    language: Optional[str] = Field(
        description="Original language of the article in ISO 639 code"
    )
    labels: Optional[List[Label]]
    title: str = Field(..., description="Article title")
    added: datetime = Field(..., description="When the article was added to delphai")


class NewsArticles(CamelModel):
    results: List[NewsArticle]
    total: int = Field(..., description="Number of results")
