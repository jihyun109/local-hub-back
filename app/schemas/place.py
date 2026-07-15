from pydantic import BaseModel, ConfigDict


class PlaceSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    district: str


class PlaceListResponse(BaseModel):
    items: list[PlaceSummary]
