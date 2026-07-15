from sqlalchemy import Column, ForeignKey, Table

from app.db.base_class import Base

# post ↔ place 다대다 연결 테이블.
# 한 게시글이 여러 관광 콘텐츠를 태그할 수 있고, 한 콘텐츠도 여러 글에 엮인다.
# (place_id, post_id) 두 컬럼이 함께 기본키(복합 PK)가 된다.
post_place = Table(
    "post_place",
    Base.metadata,
    Column("place_id", ForeignKey("place.id", ondelete="CASCADE"), primary_key=True),
    Column("post_id", ForeignKey("post.id", ondelete="CASCADE"), primary_key=True),
)
