# 담당: A (관광/축제 + 지도)
from fastapi import APIRouter

from app.api.deps import DbSession
from app.models.place import Place
from app.schemas.place import PlaceListResponse, PlaceSummary

router = APIRouter()


@router.get("/name-district", response_model=PlaceListResponse)
def list_places(db: DbSession) -> PlaceListResponse:
    places = db.query(Place).all()
    return {
        "items": [
            PlaceSummary(
                id=place.id,
                name=place.name,
                district=place.district.name if place.district else "",
            )
            for place in places
        ]
    }
