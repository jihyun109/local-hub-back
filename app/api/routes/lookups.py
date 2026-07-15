# 담당: 공용 (드롭다운용 조회 API)
from fastapi import APIRouter

from app.api.deps import DbSession
from app.crud.district import get_districts
from app.schemas.place import DistrictSchema

router = APIRouter()


@router.get("/districts", response_model=list[DistrictSchema])
def list_districts(db: DbSession):
    """자치구 목록(id, name)을 조회합니다."""
    return get_districts(db)


# TODO: 엔드포인트 추가 (GET /place-types, /post-categories)
