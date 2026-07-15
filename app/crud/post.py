from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from app.models.district import District
from app.models.place import Place
from app.models.post import Post
from app.models.post_category import PostCategory


# DB 모델을 응답용 딕셔너리로 변환
def _serialize_post(db: Session, post: Post) -> dict[str, Any]:
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_name": post.author_name,
        "category": {
            "id": post.category.id,
            "code": post.category.code,
            "name": post.category.name,
        },
        "district": (
            {"id": post.district.id, "name": post.district.name} if post.district else None
        ),
        "places": [{"id": place.id, "name": place.name} for place in post.places],
        "views": post.views,
        "likes": post.likes,
        "created_at": post.created_at,
    }


# 조건에 맞는 게시글 목록을 조회
def list_posts(
    db: Session,
    *,
    page: int = 1,
    size: int = 20,
    category_id: int | None = None,
    district_id: int | None = None,
    keyword: str | None = None,
    sort: str = "recent",
) -> dict[str, Any]:
    query = db.query(Post)

    if category_id is not None:
        query = query.filter(Post.category_id == category_id)
    if district_id is not None:
        query = query.filter(Post.district_id == district_id)
    if keyword:
        keyword_term = f"%{keyword.lower()}%"
        query = query.filter(
            or_(
                Post.title.ilike(keyword_term),
                Post.content.ilike(keyword_term),
            )
        )

    if sort == "views":
        query = query.order_by(desc(Post.views), desc(Post.created_at))
    elif sort == "likes":
        query = query.order_by(desc(Post.likes), desc(Post.created_at))
    else:
        query = query.order_by(desc(Post.created_at))

    total = query.count()
    posts = query.offset((page - 1) * size).limit(size).all()

    for post in posts:
        db.refresh(post)

    return {
        "items": [_serialize_post(db, post) for post in posts],
        "total": total,
        "page": page,
        "size": size,
    }


# 게시글 한 건 조회
def get_post(db: Session, post_id: int) -> dict[str, Any]:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")
    db.refresh(post)
    return _serialize_post(db, post)


# 새 게시글 생성
def create_post(db: Session, payload: dict[str, Any]) -> dict[str, Any]:
    category = db.query(PostCategory).filter(PostCategory.id == payload["category_id"]).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="카테고리를 찾을 수 없습니다.")

    district = None
    if payload.get("district_id") is not None:
        district = db.query(District).filter(District.id == payload["district_id"]).first()
        if not district:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="지역을 찾을 수 없습니다.")

    place_ids = payload.get("place_ids", []) or []
    places = []
    if place_ids:
        places = db.query(Place).filter(Place.id.in_(place_ids)).all()

    post = Post(
        category_id=payload["category_id"],
        title=payload["title"],
        content=payload["content"],
        author_name=payload["author_name"],
        password=payload["password"],
        district_id=payload.get("district_id"),
        views=1,
        likes=0,
        created_at=datetime.now(),
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    if places:
        post.places = places
        db.commit()
        db.refresh(post)

    return get_post(db, post.id)


# 비밀번호 확인
def verify_password(db: Session, post_id: int, password: str) -> dict[str, str]:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")
    if post.password != password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="비밀번호가 올바르지 않습니다.")
    return {"detail": "비밀번호가 확인되었습니다."}


# 게시글 수정
def update_post(db: Session, post_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")

    category = db.query(PostCategory).filter(PostCategory.id == payload["category_id"]).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="카테고리를 찾을 수 없습니다.")

    district = None
    if payload.get("district_id") is not None:
        district = db.query(District).filter(District.id == payload["district_id"]).first()
        if not district:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="지역을 찾을 수 없습니다.")

    place_ids = payload.get("place_ids", []) or []
    places = []
    if place_ids:
        places = db.query(Place).filter(Place.id.in_(place_ids)).all()

    post.category_id = payload["category_id"]
    post.title = payload["title"]
    post.content = payload["content"]
    post.district_id = payload.get("district_id")
    post.places = places

    db.commit()
    db.refresh(post)
    return get_post(db, post.id)


# 게시글 삭제
def delete_post(db: Session, post_id: int, password: str) -> dict[str, str]:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")
    if post.password != password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="비밀번호가 올바르지 않습니다.")

    db.delete(post)
    db.commit()
    return {"detail": "게시글이 삭제되었습니다."}


# 좋아요 증가
def like_post(db: Session, post_id: int) -> dict[str, Any]:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")

    post.likes += 1
    db.commit()
    db.refresh(post)
    return {"id": post.id, "likes": post.likes}
