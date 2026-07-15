# 익명 게시판 API 명세 (담당 B)

- Base URL: `/api/v1`
- Router prefix: `/posts`
- 설명: 익명 커뮤니티 게시글의 목록 조회, 상세 조회, 작성, 수정, 삭제, 좋아요 기능을 제공합니다.

## 공통 응답

### 성공 응답
- `200 OK`: 조회/수정/삭제/좋아요 성공
- `201 Created`: 생성 성공

### 실패 응답
- `400 Bad Request`: 요청 데이터 검증 실패
- `403 Forbidden`: 비밀번호 불일치
- `404 Not Found`: 게시글 없음

### 공통 에러 바디
```json
{
  "detail": "메시지"
}
```

---

## 1) 게시글 목록 조회

### `GET /api/v1/posts`

### Query Parameters
- `page` (int, optional, default: 1)
- `size` (int, optional, default: 20)
- `category_id` (int, optional)
- `district_id` (int, optional)
- `keyword` (string, optional)
- `sort` (string, optional, default: `recent`)  
  - `recent`: 최신순
  - `views`: 조회수순
  - `likes`: 좋아요순

### Success Response `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "title": "축제 후기",
      "content": "내용입니다.",
      "author_name": "바다돌이",
      "category": {
        "id": 1,
        "code": "REVIEW",
        "name": "축제 후기"
      },
      "district": {
        "id": 3,
        "name": "해운대구"
      },
      "places": [
        {
          "id": 10,
          "name": "광안리 해변"
        }
      ],
      "views": 120,
      "likes": 42,
      "created_at": "2026-07-15T10:30:00"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}
```

---

## 2) 게시글 상세 조회

### `GET /api/v1/posts/{post_id}`

### Path Parameters
- `post_id` (int, required)

### Success Response `200 OK`
```json
{
  "id": 1,
  "title": "축제 후기",
  "content": "내용입니다.",
  "author_name": "바다돌이",
  "category": {
    "id": 1,
    "code": "REVIEW",
    "name": "축제 후기"
  },
  "district": {
    "id": 3,
    "name": "해운대구"
  },
  "places": [
    {
      "id": 10,
      "name": "광안리 해변"
    }
  ],
  "views": 121,
  "likes": 42,
  "created_at": "2026-07-15T10:30:00"
}
```

---

## 3) 게시글 작성

### `POST /api/v1/posts`

### Request Body
```json
{
  "category_id": 1,
  "title": "축제 후기",
  "content": "좋았던 경험을 적어보아요.",
  "author_name": "바다돌이",
  "password": "1234",
  "district_id": 3,
  "place_ids": [10]
}
```

### Validation
- `title`: required, max 200
- `content`: required
- `author_name`: required, max 50
- `password`: required, min 4, max 50
- `category_id`: required

### Success Response `201 Created`
```json
{
  "id": 2,
  "title": "축제 후기",
  "content": "좋았던 경험을 적어보아요.",
  "author_name": "바다돌이",
  "category": {
    "id": 1,
    "code": "REVIEW",
    "name": "축제 후기"
  },
  "district": {
    "id": 3,
    "name": "해운대구"
  },
  "places": [
    {
      "id": 10,
      "name": "광안리 해변"
    }
  ],
  "views": 1,
  "likes": 0,
  "created_at": "2026-07-15T10:35:00"
}
```

---

## 4) 수정 권한 확인

### `POST /api/v1/posts/{post_id}/verify-password`

이 API는 프론트에서 수정 버튼 클릭 후, 수정 페이지로 진입하기 전에 비밀번호가 맞는지 먼저 확인하는 용도입니다.

### Request Body
```json
{
  "password": "1234"
}
```

### Validation
- `password`: required
- 비밀번호가 일치하지 않으면 `403 Forbidden`

### Success Response `200 OK`
```json
{
  "detail": "비밀번호가 확인되었습니다."
}
```

---

## 5) 게시글 수정

### `PUT /api/v1/posts/{post_id}`

수정 페이지로 진입한 뒤 실제 내용을 반영할 때 사용하는 API입니다.

### Request Body
```json
{
  "category_id": 2,
  "title": "수정된 제목",
  "content": "수정된 내용입니다.",
  "district_id": 3,
  "place_ids": [10, 11]
}
```

### Validation
- `password`는 이 API에서 받지 않고, 앞선 비밀번호 확인 API에서 인증된 상태로 가정한다.
- 수정 시 게시글이 없으면 `404 Not Found`

### Success Response `200 OK`
```json
{
  "id": 1,
  "title": "수정된 제목",
  "content": "수정된 내용입니다.",
  "author_name": "바다돌이",
  "category": {
    "id": 2,
    "code": "AD",
    "name": "홍보/광고"
  },
  "district": {
    "id": 3,
    "name": "해운대구"
  },
  "places": [
    {
      "id": 10,
      "name": "광안리 해변"
    },
    {
      "id": 11,
      "name": "해운대 시장"
    }
  ],
  "views": 121,
  "likes": 42,
  "created_at": "2026-07-15T10:30:00"
}
```

---

## 6) 게시글 삭제

### `DELETE /api/v1/posts/{post_id}`

### Request Body
```json
{
  "password": "1234"
}
```

### Success Response `200 OK`
```json
{
  "detail": "게시글이 삭제되었습니다."
}
```

---

## 7) 좋아요 증가

### `POST /api/v1/posts/{post_id}/like`

### Success Response `200 OK`
```json
{
  "id": 1,
  "likes": 43
}
```

---

## 참고
- 현재 프로젝트의 게시글 모델 기준으로 `category_id`, `district_id`, `place_ids`를 사용한다.
- 프론트에서 비밀번호 확인 후 수정/삭제가 이루어지므로, 서버는 수정/삭제 요청에서 비밀번호를 검증한다.
