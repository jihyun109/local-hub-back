from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.district import District
from app.models.place_type import PlaceType
from app.models.post_category import PostCategory

# 테스트는 운영 DB 파일 대신 인메모리 SQLite를 쓴다.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def refs() -> dict[str, int]:
    """조회 테이블에 기본 행을 넣고 각 id를 돌려준다 (FK 참조용)."""
    with TestingSessionLocal() as db:
        ptype = PlaceType(code="TOURIST", name="명소")
        category = PostCategory(code="REVIEW", name="축제 후기")
        district = District(name="해운대구")
        db.add_all([ptype, category, district])
        db.commit()
        return {
            "type_id": ptype.id,
            "category_id": category.id,
            "district_id": district.id,
        }
