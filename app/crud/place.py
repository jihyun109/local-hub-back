from sqlalchemy import func, desc, or_
from sqlalchemy.orm import Session, joinedload

from app.models.district import District
from app.models.place import Place
from app.models.place_type import PlaceType
from app.models.post import Post
from app.models.post_place import post_place


def get_top_places(db: Session, limit: int = 10) -> list[tuple[Place, int]]:
    """likes 기반으로 top N place 데이터를 조회합니다.

    place 자체에 likes 컬럼이 없으므로, place와 연결된 post의 likes 합계를 기준으로 순위를 계산합니다.
    """
    query = (
        db.query(Place, func.coalesce(func.sum(Post.likes), 0).label("likes"))
        .outerjoin(post_place, post_place.c.place_id == Place.id)
        .outerjoin(Post, Post.id == post_place.c.post_id)
        .join(PlaceType, Place.type_id == PlaceType.id)
        .join(District, Place.district_id == District.id)
        .options(joinedload(Place.type), joinedload(Place.district))
        .group_by(Place.id)
        .order_by(desc("likes"))
        .limit(limit)
    )
    return query.all()


def get_places(
    db: Session,
    district_id: int | None = None,
    place_type_id: int | None = None,
    keyword: str | None = None,
) -> list[Place]:
    """전체 place 목록 또는 필터링된 place 목록을 조회합니다."""
    query = db.query(Place).options(joinedload(Place.type), joinedload(Place.district))
    if district_id is not None:
        query = query.filter(Place.district_id == district_id)
    if place_type_id is not None:
        query = query.filter(Place.type_id == place_type_id)
    if keyword is not None:
        search = f"%{keyword}%"
        query = query.filter(
            or_(Place.name.ilike(search), Place.description.ilike(search))
        )
    return query.order_by(Place.name).all()


def get_place_names(db: Session):
    """전체 place의 id, name만 조회합니다."""
    return db.query(Place.id, Place.name).order_by(Place.name).all()


def get_place_by_id(db: Session, place_id: int) -> Place | None:
    """ID로 단일 place 상세 정보를 조회합니다."""
    return (
        db.query(Place)
        .options(joinedload(Place.type), joinedload(Place.district))
        .filter(Place.id == place_id)
        .first()
    )
