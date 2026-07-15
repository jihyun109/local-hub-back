"""부산 관광 시드 데이터를 SQLite(localhub.db)에 적재한다.

insert_data_sqlite.sql을 실행한다.

사용법:
    cd local-hub-back
    python -m scripts.seed_places
    # 다른 SQL 경로를 직접 지정하려면
    python -m scripts.seed_places "C:/path/to/insert_data_sqlite.sql"
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import text

from app.db.init_db import init_db
from app.db.session import engine

# SQL 위치
DEFAULT_SQL_PATH = Path(__file__).parent / "insert_data_sqlite.sql"

SEEDED_TABLES = ("district", "place_type", "place")


def seed(sql_path: Path) -> None:
    # 1) 테이블이 없으면 생성 (Base.metadata.create_all)
    init_db()

    # 2) 멀티 스테이트먼트 SQL 실행
    #    SQLAlchemy의 execute()는 여러 statement를 한 번에 못 돌리므로
    #    raw DBAPI 커넥션의 executescript()를 사용한다.
    sql = sql_path.read_text(encoding="utf-8")
    raw = engine.raw_connection()
    try:
        cursor = raw.cursor()
        cursor.executescript(sql)
        raw.commit()
    finally:
        raw.close()


def report() -> None:
    with engine.connect() as conn:
        for table in SEEDED_TABLES:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"  {table}: {count}건")


def main() -> None:
    sql_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SQL_PATH
    if not sql_path.exists():
        raise SystemExit(f"SQL 파일을 찾을 수 없습니다: {sql_path}")

    print(f"시드 SQL: {sql_path}")
    seed(sql_path)
    print("적재 완료:")
    report()


if __name__ == "__main__":
    main()
