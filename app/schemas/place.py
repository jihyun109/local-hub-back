from pydantic import BaseModel


class PlaceTypeSchema(BaseModel):
    id: int
    code: str
    name: str


class DistrictSchema(BaseModel):
    id: int
    name: str


class PlaceMainItem(BaseModel):
    """메인 페이지 top10 반환용 스키마."""
    place_type: PlaceTypeSchema
    name: str
    description: str | None = None
    likes: int
    latitude: float
    longitude: float
    district_name: str


class PlaceSummaryItem(BaseModel):
    """관광/축제 목록 및 필터 반환용 스키마."""
    place_type: PlaceTypeSchema
    name: str
    description: str | None = None
    latitude: float
    longitude: float
    district: DistrictSchema


class PlaceDetailItem(BaseModel):
    """상세 페이지 반환용 스키마."""
    place_type: PlaceTypeSchema
    name: str
    description: str | None = None
    address: str | None = None
    operating_info: str | None = None
    latitude: float
    longitude: float
