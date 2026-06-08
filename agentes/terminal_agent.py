import json
import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from openai import OpenAI


PACKAGE_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = PACKAGE_DIR.parent
PROTOCOL_PATH = PACKAGE_DIR / "Protocolos" / "protocolo.json"

load_dotenv(PROJECT_DIR / ".env")
load_dotenv(PACKAGE_DIR / ".env", override=False)
load_dotenv(PACKAGE_DIR / "venv" / ".env", override=False)


def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variavel de ambiente ausente: {name}")
    return value


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


def load_protocol() -> dict:
    with PROTOCOL_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_database_structure() -> dict[str, list[str]]:
    colunas = {}

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE';
                """
            )
            tabelas = cursor.fetchall()

            for tabela in tabelas:
                cursor.execute(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = %s
                    AND table_schema = 'public';
                    """,
                    (tabela[0],),
                )
                colunas_tabela = cursor.fetchall()
                colunas[tabela[0]] = [coluna[0] for coluna in colunas_tabela]

    return colunas


def validate_query(query: str, forbidden_operations: list[str]) -> bool:
    q = query.upper()
    forbidden = [operation.upper() for operation in forbidden_operations]

    if not q.startswith("SELECT"):
        return False
    if any(operation in q for operation in forbidden):
        return False
    if "--" in q or "/*" in q:
        return False

    return True


def main() -> None:
    protocol = load_protocol()
    colunas = load_database_structure()
    pergunta_usuario = input("Faca sua pergunta: ")

    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_API_KEY")
    if not api_key:
        raise RuntimeError("Variavel de ambiente ausente: OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    system_prompt = f"""
Voce e um chatbot chamado Konoha Oracle.

Siga rigorosamente o protocolo abaixo:

{json.dumps(protocol, indent=2, ensure_ascii=False)}

Regras adicionais obrigatorias:
- Gere apenas a query SQL pura.
- Nunca use markdown.
- Nunca explique.
"""

    user_prompt = f"""
Voce deve gerar queries baseadas na seguinte estrutura do banco de dados: {colunas}

Pergunta: {pergunta_usuario}

Resposta em SQL:
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=250,
        temperature=0,
    )

    query_gerada = response.choices[0].message.content or ""
    query_gerada = query_gerada.replace("```sql", "").replace("```", "")
    query_gerada = query_gerada.strip().rstrip(";")

    if not validate_query(query_gerada, protocol["forbidden_operations"]):
        print("\nQuery bloqueada pelo protocolo de seguranca.")
        sys.exit(1)

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_gerada)
                resultado = cursor.fetchall()
    except Exception as error:
        print("\nErro ao executar query:")
        print(error)
        sys.exit(1)

    if not resultado:
        print("Nao encontrei informacoes no banco.")
        return

    natural_prompt = f"""
Voce e o Konoha Oracle.

Baseado exclusivamente nos dados abaixo retornados do banco,
que segue essa estrutura {colunas},
responda a pergunta do usuario em linguagem natural.

Pergunta original:
{pergunta_usuario}

Dados retornados:
{resultado}

Responda de forma clara, organizada e como um verdadeiro oraculo ninja.
"""

    natural_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "Voce e o Konoha Oracle. Responda de forma objetiva com base nos dados fornecidos.",
            },
            {"role": "user", "content": natural_prompt},
        ],
        temperature=0.2,
        max_tokens=350,
    )

    resposta_final = natural_response.choices[0].message.content
    print("\nResposta do Konoha Oracle\n")
    print(resposta_final)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(f"\nErro de configuracao: {error}")
        sys.exit(1)
