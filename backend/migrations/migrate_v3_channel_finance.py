"""Migration v3 - add channel-finance fields to schemes and profile (VittVanni).

Idempotent for SQLite and PostgreSQL. Run from backend/:
    python -m migrations.migrate_v3_channel_finance
"""

import os
import sys

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import inspect, text  # noqa: E402

from app.database import engine  # noqa: E402

# (column, base DDL fragment without dialect prefix)
SCHEME_COLUMNS = [
    ("loan_category", "VARCHAR(30)"),
    ("channel_financed", "BOOLEAN DEFAULT false"),
    ("interest_rate_min", "FLOAT"),
    ("interest_rate_max", "FLOAT"),
    ("moratorium_min_months", "INTEGER"),
    ("moratorium_max_months", "INTEGER"),
    ("max_coverage_pct", "INTEGER"),
    ("max_project_cost", "INTEGER"),
    ("tenure_min_months", "INTEGER"),
    ("tenure_max_months", "INTEGER"),
    ("income_ceiling", "INTEGER"),
]

PROFILE_COLUMNS = [
    ("annual_family_income", "VARCHAR(30)"),
    ("education_status", "VARCHAR(30)"),
    ("estimated_project_cost", "INTEGER"),
]


def _run(table: str, column: str, ddl: str) -> None:
    with engine.begin() as conn:
        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}"))


def migrate() -> int:
    insp = inspect(engine)
    changed = 0
    for table, columns in (("schemes", SCHEME_COLUMNS), ("entrepreneur_profiles", PROFILE_COLUMNS)):
        if not insp.has_table(table):
            print(f"[skip] table {table} not found")
            continue
        existing = {c["name"] for c in insp.get_columns(table)}
        for column, ddl in columns:
            if column in existing:
                continue
            _run(table, column, ddl)
            print(f"[ok] {table}.{column} ({ddl})")
            changed += 1
    return changed


if __name__ == "__main__":
    n = migrate()
    print(f"Migration complete. {n} column(s) added.")