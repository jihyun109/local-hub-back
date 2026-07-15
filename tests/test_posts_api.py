from app.db.base import Base
from app.db.init_db import seed_default_data
from app.models.district import District
from app.models.post_category import PostCategory
from tests.conftest import TestingSessionLocal, engine


def test_seed_default_data_creates_lookup_rows():
    Base.metadata.create_all(bind=engine)
    try:
        with TestingSessionLocal() as db:
            seed_default_data(db)
            assert db.query(PostCategory).filter(PostCategory.code == "REVIEW").count() == 1
            assert db.query(District).filter(District.name == "해운대구").count() == 1
    finally:
        Base.metadata.drop_all(bind=engine)


def test_post_crud_flow(client, refs):
    """게시물 CRUD 전체 흐름 테스트"""
    # 1. 게시물 생성
    create_payload = {
        "category_id": refs["category_id"],
        "title": "축제 후기",
        "content": "좋았어요.",
        "author_name": "바다돌이",
        "password": "1234",
        "district_id": refs["district_id"],
        "place_ids": [],
    }

    create_response = client.post("/api/posts", json=create_payload)
    assert create_response.status_code == 201
    post = create_response.json()
    assert post["title"] == "축제 후기"
    assert post["category"]["id"] == refs["category_id"]
    assert post["district"]["id"] == refs["district_id"]

    # 2. 비밀번호 확인
    verify_response = client.post(f"/api/posts/{post['id']}/verify-password", json={"password": "1234"})
    assert verify_response.status_code == 200
    assert verify_response.json()["detail"] == "비밀번호가 확인되었습니다."

    # 3. 게시물 수정
    update_response = client.put(
        f"/api/posts/{post['id']}",
        json={
            "category_id": refs["category_id"],
            "title": "수정된 제목",
            "content": "수정된 내용",
            "district_id": refs["district_id"],
            "place_ids": [],
        },
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "수정된 제목"
    assert updated["content"] == "수정된 내용"

    # 4. 좋아요 추가
    like_response = client.post(f"/api/posts/{post['id']}/like")
    assert like_response.status_code == 200
    assert like_response.json()["likes"] == 1

    # 5. 게시물 삭제
    delete_response = client.request("DELETE", f"/api/posts/{post['id']}", json={"password": "1234"})
    assert delete_response.status_code == 200

    # 6. 게시물 목록 조회 (삭제 후 0개 확인)
    list_response = client.get("/api/posts")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 0
