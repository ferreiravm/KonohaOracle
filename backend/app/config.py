import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
PROTOCOL_PATH = ROOT_DIR / "Protocolos" / "protocolo.json"

load_dotenv(ROOT_DIR / ".env")


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"Variavel de ambiente ausente: {name}")
    return value


def get_optional_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def get_openai_api_key() -> str:
    return get_optional_env("OPENAI_API_KEY") or get_env("OPEN_API_KEY")


def get_cors_origins() -> list[str]:
    origins = get_optional_env("CORS_ORIGINS", "http://localhost:5173")
    return [origin.strip() for origin in origins.split(",") if origin.strip()]
