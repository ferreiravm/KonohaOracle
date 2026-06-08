import os
from pathlib import Path

import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variavel de ambiente ausente: {name}")
    return value


try:
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        conn = psycopg2.connect(database_url)
    else:
        conn = psycopg2.connect(
            host=get_required_env("host"),
            user=get_required_env("user"),
            port=int(get_required_env("port")),
            password=get_required_env("password"),
            dbname=get_required_env("database"),
        )

    cursor = conn.cursor()
    print("Conectado ao PostgreSQL com sucesso!")

except OperationalError as e:
    print("Erro ao conectar:", e)
