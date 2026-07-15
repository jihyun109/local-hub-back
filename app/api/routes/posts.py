# 담당: B (익명 게시판)
from fastapi import APIRouter, Query

from app.api.deps import DbSession
from app.crud.post import create_post, delete_post, get_post, like_post, list_posts, update_post, verify_password
from app.schemas.common import Message
from app.schemas.post import (
    LikeOut,
    PostCreate,
    PostDelete,
    PostListResponse,
    PostOut,
    PostUpdate,
    PostVerifyPassword,
)

router = APIRouter()


# 게시글 목록 조회
@router.get("", response_model=PostListResponse)
def read_posts(
    db: DbSession,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category_id: int | None = None,
    category_code: str | None = None,
    district_id: int | None = None,
    keyword: str | None = None,
    sort: str = "recent",
) -> PostListResponse:
    return list_posts(
        db,
        page=page,
        size=size,
        category_id=category_id,
        category_code=category_code,
        district_id=district_id,
        keyword=keyword,
        sort=sort,
    )


# 게시글 상세 조회
@router.get("/{post_id}", response_model=PostOut)
def read_post(post_id: int, db: DbSession) -> PostOut:
    return get_post(db, post_id)


# 새 게시글 작성
@router.post("", response_model=PostOut, status_code=201)
def create_post_endpoint(payload: PostCreate, db: DbSession) -> PostOut:
    return create_post(db, payload.model_dump())


# 수정 전 비밀번호 확인
@router.post("/{post_id}/verify-password", response_model=Message)
def verify_password_endpoint(post_id: int, payload: PostVerifyPassword, db: DbSession) -> Message:
    return verify_password(db, post_id, payload.password)


# 게시글 수정
@router.put("/{post_id}", response_model=PostOut)
def update_post_endpoint(post_id: int, payload: PostUpdate, db: DbSession) -> PostOut:
    return update_post(db, post_id, payload.model_dump())


# 게시글 삭제
@router.delete("/{post_id}", response_model=Message)
def delete_post_endpoint(post_id: int, payload: PostDelete, db: DbSession) -> Message:
    return delete_post(db, post_id, payload.password)


# 좋아요 증가
@router.post("/{post_id}/like", response_model=LikeOut)
def like_post_endpoint(post_id: int, db: DbSession) -> LikeOut:
    return like_post(db, post_id)
