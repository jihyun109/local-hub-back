"""부산 관광 시드 데이터를 SQLite(localhub.db)에 적재한다.

테이블별 SQL 파일을 순서대로 실행한다.

실행 예:
    python -m scripts.seed_database
    python -m scripts.seed_database scripts
    python -m scripts.seed_database scripts/seed_districts.sql
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import text

from app.db.init_db import init_db
from app.db.session import engine

SCRIPT_DIR = Path(__file__).parent
SEED_FILES = (
    SCRIPT_DIR / "seed_districts.sql",
    SCRIPT_DIR / "seed_place_types.sql",
    SCRIPT_DIR / "seed_post_categories.sql",
    SCRIPT_DIR / "seed_places.sql",
    SCRIPT_DIR / "seed_posts.sql",
)
SEEDED_TABLES = ("자치구", "place_type", "post_category", "place", "post")


def seed(target: Path | None = None) -> None:
    init_db()

    if target is None or target.is_dir():
        paths = SEED_FILES
    else:
        paths = [target]

    for path in paths:
        if not path.exists():
            raise SystemExit(f"SQL 파일을 찾을 수 없습니다: {path}")
        print(f"실행: {path}")
        _execute_sql(path)


def _execute_sql(sql_path: Path) -> None:
    sql = sql_path.read_text(encoding="utf-8")
    with engine.raw_connection() as raw:
        cursor = raw.cursor()
        # 각 시드 파일이 자기 테이블만 DELETE하므로, 재실행 시 다른 테이블이 참조 중인
        # 상위 테이블(자치구, place_type 등)을 지우려 하면 FK 위반이 난다. 시드 스크립트
        # 실행 중에는 일시적으로 FK 검사를 끄고, 끝나면 다시 켠다.
        cursor.execute("PRAGMA foreign_keys=OFF")
        cursor.executescript(sql)
        raw.commit()
        cursor.execute("PRAGMA foreign_keys=ON")


def report() -> None:
    with engine.connect() as conn:
        for table in SEEDED_TABLES:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"  {table}: {count}건")


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    seed(target)
    print("적재 완료:")
    report()


if __name__ == "__main__":
    main()
