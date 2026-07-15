from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.post_place import post_place


class Post(Base):
    """익명 커뮤니티 게시글."""

    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("post_category.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    author_name: Mapped[str] = mapped_column(String(50), nullable=False)
    # ERD 기준 평문 저장. 익명 게시글 수정/삭제용 비밀번호.
    password: Mapped[str] = mapped_column(String(50), nullable=False)

    # 작성 지역. NULL이면 '부산 전역'을 의미한다.
    district_id: Mapped[int | None] = mapped_column(
        ForeignKey("district.id", ondelete="SET NULL"), index=True
    )

    views: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), index=True
    )

    category: Mapped["PostCategory"] = relationship(back_populates="posts")  # noqa: F821
    district: Mapped["District | None"] = relationship(back_populates="posts")  # noqa: F821
    places: Mapped[list["Place"]] = relationship(  # noqa: F821
        secondary=post_place, back_populates="posts"
    )

    __table_args__ = (Index("ix_post_category_created_at", "category_id", "created_at"),)
