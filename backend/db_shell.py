"""
Connects to the Postgres database using the DATABASE_URL from .env,
and drops you into a simple interactive SQL prompt.

USAGE:
    python db_shell.py

Type any SQL command and press Enter. Type 'exit' or 'quit' to leave.
Example commands to try:
    SELECT COUNT(*) FROM schemes;
    SELECT name, department FROM schemes LIMIT 5;
    \dt   (not supported here -- use: SELECT table_name FROM information_schema.tables WHERE table_schema='public';)
"""

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL or not DATABASE_URL.startswith("postgresql"):
    raise SystemExit("DATABASE_URL in .env doesn't look like a Postgres URL.")

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

print(f"Connected to: {DATABASE_URL.split('@')[-1]}")
print("Type SQL commands, or 'exit' to quit.\n")

while True:
    query = input("vittvaani> ").strip()
    if query.lower() in ("exit", "quit"):
        break
    if not query:
        continue
    try:
        cur.execute(query)
        if cur.description:  # SELECT-type query
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            print(colnames)
            for row in rows:
                print(row)
            print(f"({len(rows)} rows)")
        else:
            print("OK.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

cur.close()
conn.close()
