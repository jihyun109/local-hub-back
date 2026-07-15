from sqlalchemy import Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.post_place import post_place


class Place(Base):
    """관광지/축제 콘텐츠."""

    __tablename__ = "place"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    type_id: Mapped[int] = mapped_column(
        ForeignKey("place_type.id"), nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(Text)

    district_id: Mapped[int] = mapped_column(
        ForeignKey("district.id"), nullable=False, index=True
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    address: Mapped[str | None] = mapped_column(String(200))
    operating_info: Mapped[str | None] = mapped_column(String(200))

    image_url_1: Mapped[str | None] = mapped_column(String(255))
    image_url_2: Mapped[str | None] = mapped_column(String(255))

    type: Mapped["PlaceType"] = relationship(back_populates="places")  # noqa: F821
    district: Mapped["District"] = relationship(back_populates="places")  # noqa: F821
    posts: Mapped[list["Post"]] = relationship(  # noqa: F821
        secondary=post_place, back_populates="places"
    )

    __table_args__ = (Index("ix_place_lat_lng", "latitude", "longitude"),)
