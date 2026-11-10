"""Validate bundled CSVs and replace MySQL table rows in one transaction."""
from pathlib import Path
import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
}
database = os.getenv("MYSQL_DATABASE", "recruitment_analytics")
files = {"jobs": "jobs.csv", "sources": "sources.csv", "applications": "applications.csv", "stage_events": "stage_events.csv"}
data = {table: pd.read_csv(ROOT / "data" / filename) for table, filename in files.items()}

if any(frame.isna().any().any() for frame in data.values()):
    raise ValueError("An input CSV contains missing values; no database rows were changed.")
if not set(data["applications"].job_id).issubset(set(data["jobs"].job_id)):
    raise ValueError("applications.csv references an unknown job_id; no database rows were changed.")
if not set(data["applications"].source_id).issubset(set(data["sources"].source_id)):
    raise ValueError("applications.csv references an unknown source_id; no database rows were changed.")
if not set(data["stage_events"].application_id).issubset(set(data["applications"].application_id)):
    raise ValueError("stage_events.csv references an unknown application_id; no database rows were changed.")

connection = mysql.connector.connect(**config, autocommit=False)
try:
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci")
    cursor.execute(f"USE `{database}`")
    for statement in (ROOT / "sql" / "01_create_schema.sql").read_text(encoding="utf-8-sig").split(";"):
        statement = statement.strip()
        if statement and not statement.upper().startswith(("CREATE DATABASE", "USE ")):
            cursor.execute(statement)
    # Child-first delete order preserves foreign-key constraints. DML is rolled back on error.
    for table in ("stage_events", "applications", "sources", "jobs"):
        cursor.execute(f"DELETE FROM `{table}`")
    for table, frame in data.items():
        columns = list(frame.columns)
        sql = f"INSERT INTO `{table}` ({','.join(f'`{col}`' for col in columns)}) VALUES ({','.join(['%s'] * len(columns))})"
        rows = [tuple(row) for row in frame.astype(object).where(pd.notna(frame), None).itertuples(index=False, name=None)]
        cursor.executemany(sql, rows)
    counts = {}
    for table in files:
        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        counts[table] = cursor.fetchone()[0]
    connection.commit()
    for table, count in counts.items():
        print(f"{table}: {count} rows loaded")
except Exception:
    connection.rollback()
    raise
finally:
    connection.close()
