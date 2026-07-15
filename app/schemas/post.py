from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import Message, Page


class PostCategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str


class DistrictOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class PlaceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class PostCreate(BaseModel):
    category_id: int
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    author_name: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=4, max_length=50)
    district_id: int | None = None
    place_ids: list[int] = Field(default_factory=list)


class PostUpdate(BaseModel):
    category_id: int
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    district_id: int | None = None
    place_ids: list[int] = Field(default_factory=list)


class PostVerifyPassword(BaseModel):
    password: str = Field(min_length=1)


class PostDelete(BaseModel):
    password: str = Field(min_length=1)


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author_name: str
    category: PostCategoryOut
    district: DistrictOut | None
    places: list[PlaceOut]
    views: int
    likes: int
    created_at: datetime


class LikeOut(BaseModel):
    id: int
    likes: int


class PostListItem(BaseModel):
    id: int
    category_id: int
    category_code: str
    category_name: str
    title: str
    views: int
    likes: int
    author_name: str
    place_name: str | None
    district_name: str | None


class PostListResponse(Page[PostListItem]):
    pass
