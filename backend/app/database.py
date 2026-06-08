import os

import psycopg2
from psycopg2.extras import RealDictCursor

from backend.app.config import get_env


def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg2.connect(database_url)

    return psycopg2.connect(
        host=get_env("host"),
        user=get_env("user"),
        port=int(get_env("port")),
        password=get_env("password"),
        database=get_env("database"),
    )


def load_database_structure() -> dict[str, list[str]]:
    structure: dict[str, list[str]] = {}

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
                """
            )
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                cursor.execute(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = %s
                    ORDER BY ordinal_position;
                    """,
                    (table_name,),
                )
                structure[table_name] = [column[0] for column in cursor.fetchall()]

    return structure


def run_select_query(query: str) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
