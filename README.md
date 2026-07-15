# local-hub-back

부산 관광 콘텐츠 + 익명 커뮤니티 게시판 API (FastAPI + SQLAlchemy + SQLite)

## 실행

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

copy .env.example .env
python -m scripts.seed_database  # 샘플 데이터 (담당 A 구현 예정)

uvicorn app.main:app --reload
```

- API 문서: http://localhost:8000/docs
- 헬스체크: http://localhost:8000/health

> 앱 기동 시 테이블은 자동 생성된다(마이그레이션 도구 없이 `init_db`). DB 파일은 `localhub.db`.

## 디렉토리 구조

```
app/
  main.py               FastAPI 앱, CORS, 라우터 등록
  core/
    config.py           환경변수 설정
    security.py         비밀번호 해시/검증 (bcrypt)
  db/
    base_class.py       SQLAlchemy Base
    base.py             create_all용 모델 모음
    session.py          engine, SessionLocal, get_db
    init_db.py          테이블 생성
  models/               ERD 테이블 (place_type, place, district,
                        post_category, post, post_place)
  schemas/              Pydantic 요청/응답 스키마   ← 스켈레톤
  crud/                 DB 접근 로직               ← 스켈레톤
  services/
    chat_service.py     챗봇 서비스                ← 스켈레톤
  api/
    deps.py             DbSession 의존성
    router.py           /api 하위 라우터 통합
    routes/             places, posts, lookups, chat 엔드포인트  ← 스켈레톤
scripts/
  seed_places.py        샘플 데이터 삽입            ← 스켈레톤
tests/
```

## 역할 분담 (백엔드)

DB 모델과 앱 골격은 완성돼 있고, 아래 로직 파일은 **빈 스켈레톤**이라 담당자가 채운다.

| 담당 | 파일 |
| --- | --- |
| A (관광/축제·지도) | `schemas/place.py`, `crud/place.py`, `routes/places.py`, `scripts/seed_database.py` |
| B (익명 게시판) | `schemas/post.py`, `crud/post.py`, `routes/posts.py` |
| C (인프라·챗봇) | `schemas/chat.py`, `routes/chat.py`, `services/chat_service.py`, 앱 골격 유지보수 |
| 공용 | `schemas/lookup.py`, `crud/lookup.py`, `routes/lookups.py` (드롭다운용 조회 API) |

라우터가 비어 있는 동안에는 서버가 뜨지 않는다. 각 담당자가 자기 `routes/*.py`에
`router = APIRouter()`와 엔드포인트를 채우면 `app/api/router.py`가 이를 묶어 기동된다.

## API (구현 목표)

### lookups (공용 조회 — 프론트 드롭다운용)

| 메서드 | 경로 | 설명 |
| --- | --- | --- |
| GET | `/api/place-types` | 장소 유형 목록 |
| GET | `/api/districts` | 자치구 목록 |
| GET | `/api/post-categories` | 게시글 카테고리 목록 |

### places

| 메서드 | 경로 | 설명 |
| --- | --- | --- |
| GET | `/api/places` | 목록 (`type_id`, `district_id`, `keyword`, `page`, `size`) |
| GET | `/api/places/{id}` | 상세 |

관광 콘텐츠는 공공데이터 시딩으로 채우는 것을 기본으로 한다(사용자 등록 없음).

### posts

| 메서드 | 경로 | 설명 |
| --- | --- | --- |
| GET | `/api/posts` | 목록 (`category_id`, `place_id`, `district_id`, `keyword`, `page`, `size`) |
| GET | `/api/posts/{id}` | 상세 (조회수 증가) |
| POST | `/api/posts` | 작성 (`password` 필요) |
| PATCH | `/api/posts/{id}` | 수정 (`password` 필요) |
| POST | `/api/posts/{id}/delete` | 삭제 (`password` 필요) |
| POST | `/api/posts/{id}/likes` | 좋아요 |

- 작성 바디: `category_id`, `title`, `content`, `author_name`, `password`,
  `district_id`(선택, NULL=부산 전역), `place_ids`(선택, 태그할 관광 콘텐츠 다대다).
- 익명 게시판이라 삭제에도 비밀번호를 본문에 담아야 해서 `DELETE`가 아닌 `POST /{id}/delete`를 쓴다.
- 비밀번호는 ERD상 `post.password` 컬럼에 저장한다. `core/security.py`의 해시 유틸로 강화할 수 있다.

### chat

`POST /api/chat` — 대화 기록은 DB에 저장하지 않는다. 클라이언트가 `history`를 매 요청에 함께 보낸다.

```json
{
  "message": "해운대 근처 문화시설을 알려줘",
  "history": [
    { "role": "user", "content": "실내 관광지를 찾고 있어" },
    { "role": "assistant", "content": "부산 지역의 실내 관광지를 안내해드릴게요." }
  ]
}
```

`services/chat_service.py`는 아직 비어 있다(담당 C). DB 키워드 검색 스텁으로 시작해 LLM으로 확장할 수 있다.
