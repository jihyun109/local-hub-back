from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class PostCategory(Base):
    """게시글 카테고리 조회 테이블 (예: REVIEW=축제 후기, AD=홍보/광고)."""

    __tablename__ = "post_category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="category")  # noqa: F821
