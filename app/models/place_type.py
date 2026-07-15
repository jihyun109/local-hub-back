from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class PlaceType(Base):
    """장소 유형 조회 테이블 (예: FESTIVAL=축제, TOURIST=명소)."""

    __tablename__ = "place_type"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    places: Mapped[list["Place"]] = relationship(back_populates="type")  # noqa: F821
