# 담당: A (관광/축제 + 지도)
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud.place import get_place_by_id, get_places, get_top_places
from app.db.session import get_db
from app.schemas.place import (
    DistrictSchema,
    PlaceDetailItem,
    PlaceMainItem,
    PlaceSummaryItem,
    PlaceTypeSchema,
)

router = APIRouter()


@router.get("/main", response_model=list[PlaceMainItem])
def get_main_places(db: Session = Depends(get_db)):
    """메인 페이지: likes 기반 top10 place 정보를 조회합니다."""
    rows = get_top_places(db, limit=10)
    return [
        PlaceMainItem(
            place_type=PlaceTypeSchema(
                id=place.type.id,
                code=place.type.code,
                name=place.type.name,
            ),
            name=place.name,
            description=place.description,
            likes=likes,
            latitude=place.latitude,
            longitude=place.longitude,
            district_name=place.district.name,
        )
        for place, likes in rows
    ]


@router.get("", response_model=list[PlaceSummaryItem])
def get_place_list(
    district_id: int | None = Query(None, description="자치구 ID로 필터링"),
    place_type_id: int | None = Query(None, description="place type id로 필터링"),
    keyword: str | None = Query(
        None,
        description="place name 또는 description 검색 키워드",
    ),
    db: Session = Depends(get_db),
):
    """관광&축제 페이지: 전체 또는 필터링된 place 목록을 조회합니다."""
    places = get_places(
        db,
        district_id=district_id,
        place_type_id=place_type_id,
        keyword=keyword,
    )
    return [
        PlaceSummaryItem(
            place_type=PlaceTypeSchema(
                id=place.type.id,
                code=place.type.code,
                name=place.type.name,
            ),
            name=place.name,
            description=place.description,
            latitude=place.latitude,
            longitude=place.longitude,
            district=DistrictSchema(id=place.district.id, name=place.district.name),
        )
        for place in places
    ]


@router.get("/{place_id}", response_model=PlaceDetailItem)
def get_place_detail(
    place_id: int,
    db: Session = Depends(get_db),
):
    """상세 페이지: place ID로 축제/관광 상세 정보를 조회합니다."""
    place = get_place_by_id(db, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return PlaceDetailItem(
        place_type=PlaceTypeSchema(
            id=place.type.id,
            code=place.type.code,
            name=place.type.name,
        ),
        name=place.name,
        description=place.description,
        address=place.address,
        operating_info=place.operating_info,
        latitude=place.latitude,
        longitude=place.longitude,
    )
