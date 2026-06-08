import json

from openai import OpenAI

from backend.app.config import PROTOCOL_PATH, get_openai_api_key
from backend.app.database import load_database_structure, run_select_query


def load_protocol() -> dict:
    with PROTOCOL_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def clean_sql(raw_sql: str) -> str:
    return raw_sql.replace("```sql", "").replace("```", "").strip().rstrip(";")


def validate_query(query: str, forbidden_operations: list[str]) -> bool:
    q = query.upper()
    forbidden = [operation.upper() for operation in forbidden_operations]

    if not q.startswith("SELECT"):
        return False
    if ";" in q:
        return False
    if "--" in q or "/*" in q:
        return False
    if "INFORMATION_SCHEMA" in q or "PG_" in q:
        return False
    if any(operation in q for operation in forbidden):
        return False

    return True


class KonohaOracleService:
    def __init__(self) -> None:
        self.protocol = load_protocol()
        self.client = OpenAI(api_key=get_openai_api_key())

    def ask(self, question: str) -> dict:
        database_structure = load_database_structure()
        sql = self._generate_sql(question, database_structure)

        if not validate_query(sql, self.protocol["forbidden_operations"]):
            raise ValueError("Query bloqueada pelo protocolo de seguranca.")

        rows = run_select_query(sql)
        answer = self._generate_answer(question, database_structure, rows)

        return {
            "answer": answer,
            "sql": sql,
            "rows": rows,
        }

    def _generate_sql(self, question: str, database_structure: dict[str, list[str]]) -> str:
        system_prompt = f"""
Voce e um chatbot chamado Konoha Oracle.

Siga rigorosamente o protocolo abaixo:

{json.dumps(self.protocol, indent=2, ensure_ascii=False)}

Regras adicionais obrigatorias:
- Gere apenas a query SQL pura.
- Nunca use markdown.
- Nunca explique.
- Inclua LIMIT quando a consulta retornar listas.
"""

        user_prompt = f"""
Voce deve gerar queries baseadas na seguinte estrutura do banco de dados:
{database_structure}

Pergunta:
{question}

Resposta em SQL:
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=250,
            temperature=0,
        )

        return clean_sql(response.choices[0].message.content or "")

    def _generate_answer(
        self,
        question: str,
        database_structure: dict[str, list[str]],
        rows: list[dict],
    ) -> str:
        if not rows:
            return "Nao encontrei informacoes no banco para responder essa pergunta."

        natural_prompt = f"""
Voce e o Konoha Oracle.

Baseado exclusivamente nos dados abaixo retornados do banco,
que segue essa estrutura {database_structure},
responda a pergunta do usuario em linguagem natural.

Pergunta original:
{question}

Dados retornados:
{rows}

Responda de forma clara e organizada.
"""

        response = self.client.chat.completions.create(
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

        return response.choices[0].message.content or ""
