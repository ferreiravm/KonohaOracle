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


def ensure_curation_table() -> None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS CuradoriaSugestoes (
                    IdCuradoria SERIAL PRIMARY KEY,
                    Entidade VARCHAR(50) NOT NULL,
                    Consulta TEXT NOT NULL,
                    Status VARCHAR(20) NOT NULL CHECK (Status IN ('Aprovado', 'Rejeitado')),
                    Proposta JSONB NOT NULL,
                    Fontes JSONB NOT NULL,
                    Observacao TEXT,
                    CriadoEm TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """
            )
        conn.commit()


def save_curation_decision(
    entity: str,
    query: str,
    status: str,
    proposal_json: str,
    sources_json: str,
    note: str | None,
) -> int:
    ensure_curation_table()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO CuradoriaSugestoes
                    (Entidade, Consulta, Status, Proposta, Fontes, Observacao)
                VALUES
                    (%s, %s, %s, %s::jsonb, %s::jsonb, %s)
                RETURNING IdCuradoria;
                """,
                (entity, query, status, proposal_json, sources_json, note),
            )
            curation_id = cursor.fetchone()[0]
        conn.commit()

    return curation_id


def list_curation_decisions(status: str | None = None, limit: int = 20) -> list[dict]:
    ensure_curation_table()
    safe_limit = max(1, min(limit, 100))

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if status:
                cursor.execute(
                    """
                    SELECT
                        IdCuradoria,
                        Entidade,
                        Consulta,
                        Status,
                        Proposta,
                        Fontes,
                        Observacao,
                        CriadoEm
                    FROM CuradoriaSugestoes
                    WHERE Status = %s
                    ORDER BY IdCuradoria DESC
                    LIMIT %s;
                    """,
                    (status, safe_limit),
                )
            else:
                cursor.execute(
                    """
                    SELECT
                        IdCuradoria,
                        Entidade,
                        Consulta,
                        Status,
                        Proposta,
                        Fontes,
                        Observacao,
                        CriadoEm
                    FROM CuradoriaSugestoes
                    ORDER BY IdCuradoria DESC
                    LIMIT %s;
                    """,
                    (safe_limit,),
                )

            return [dict(row) for row in cursor.fetchall()]


def get_curation_decision(curation_id: int) -> dict | None:
    ensure_curation_table()

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT
                    IdCuradoria,
                    Entidade,
                    Consulta,
                    Status,
                    Proposta,
                    Fontes,
                    Observacao,
                    CriadoEm
                FROM CuradoriaSugestoes
                WHERE IdCuradoria = %s;
                """,
                (curation_id,),
            )
            row = cursor.fetchone()

    return dict(row) if row else None


def find_lookup_id(table: str, id_column: str, name_column: str, name: str) -> int | None:
    allowed_tables = {
        "clas": ("idcla", "nome"),
        "vilas": ("idvila", "nome"),
        "tipopersonagens": ("idtipopersonagem", "relevancia"),
        "arcos": ("idarco", "nome"),
        "ocupacoes": ("idocupacao", "nome"),
    }

    expected_columns = allowed_tables.get(table.lower())
    if expected_columns != (id_column.lower(), name_column.lower()):
        raise ValueError("Lookup nao permitido.")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT {id_column}
                FROM {table}
                WHERE LOWER({name_column}) = LOWER(%s)
                LIMIT 1;
                """,
                (name,),
            )
            row = cursor.fetchone()

    return row[0] if row else None


def load_reference_options() -> dict[str, list[dict]]:
    queries = {
        "tipos_personagem": "SELECT IdTipoPersonagem AS id, Relevancia AS label FROM TipoPersonagens ORDER BY IdTipoPersonagem;",
        "arcos": "SELECT IdArco AS id, Nome AS label FROM Arcos ORDER BY IdArco;",
        "ocupacoes": "SELECT IdOcupacao AS id, Nome AS label FROM Ocupacoes ORDER BY IdOcupacao;",
        "vilas": "SELECT IdVila AS id, Nome AS label FROM Vilas ORDER BY IdVila;",
        "clas": "SELECT IdCla AS id, Nome AS label FROM Clas ORDER BY IdCla;",
    }

    options: dict[str, list[dict]] = {}

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            for key, query in queries.items():
                cursor.execute(query)
                options[key] = [dict(row) for row in cursor.fetchall()]

    options["estados"] = [
        {"id": "Vivo", "label": "Vivo"},
        {"id": "Morto", "label": "Morto"},
    ]
    options["sexos"] = [
        {"id": "Masculino", "label": "Masculino"},
        {"id": "Feminino", "label": "Feminino"},
    ]

    return options
