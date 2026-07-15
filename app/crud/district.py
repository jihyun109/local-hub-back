from sqlalchemy.orm import Session

from app.models.district import District


def get_districts(db: Session) -> list[District]:
    """전체 자치구 목록을 조회합니다."""
    return db.query(District).order_by(District.name).all()
