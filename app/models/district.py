from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class District(Base):
    """자치구 조회 테이블 (예: 해운대구)."""

    __tablename__ = "자치구"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    places: Mapped[list["Place"]] = relationship(back_populates="district")  # noqa: F821
    posts: Mapped[list["Post"]] = relationship(back_populates="district")  # noqa: F821
