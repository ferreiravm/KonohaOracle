import json
from typing import Literal
from urllib.parse import urlencode

import httpx
from openai import OpenAI

from backend.app.config import get_openai_api_key
from backend.app.database import load_database_structure, save_curation_decision


EntityType = Literal["personagem", "jutsu", "arco", "vila", "cla", "grupo", "ferramenta"]


def _wikipedia_search_url(query: str) -> str:
    params = urlencode(
        {
            "action": "opensearch",
            "search": query,
            "limit": 3,
            "namespace": 0,
            "format": "json",
        }
    )
    return f"https://pt.wikipedia.org/w/api.php?{params}"


def search_public_context(query: str) -> list[dict]:
    with httpx.Client(timeout=12.0, follow_redirects=True) as client:
        search_response = client.get(_wikipedia_search_url(query))
        search_response.raise_for_status()
        payload = search_response.json()

        titles = payload[1] if len(payload) > 1 else []
        descriptions = payload[2] if len(payload) > 2 else []
        urls = payload[3] if len(payload) > 3 else []

        results = []
        for index, title in enumerate(titles[:3]):
            summary_url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{title}"
            summary_response = client.get(summary_url)
            summary = ""
            if summary_response.status_code == 200:
                summary = summary_response.json().get("extract", "")

            results.append(
                {
                    "title": title,
                    "description": descriptions[index] if index < len(descriptions) else "",
                    "url": urls[index] if index < len(urls) else "",
                    "summary": summary,
                }
            )

    return results


class CurationService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=get_openai_api_key())

    def propose(self, entity: EntityType, query: str, notes: str = "") -> dict:
        sources = search_public_context(f"{query} Naruto")
        database_structure = load_database_structure()

        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Voce e um assistente de curadoria de dados para um banco PostgreSQL "
                        "sobre Naruto. Gere apenas JSON valido, sem markdown. "
                        "Nao invente dados que nao estejam nas fontes fornecidas. "
                        "Quando a informacao for incerta, use null e registre em pendencias."
                    ),
                },
                {
                    "role": "user",
                    "content": f"""
Tipo de entidade: {entity}
Consulta do curador: {query}
Notas do curador: {notes}

Estrutura atual do banco:
{database_structure}

Fontes publicas encontradas:
{json.dumps(sources, ensure_ascii=False, indent=2)}

Gere um JSON neste formato:
{{
  "entity": "{entity}",
  "confidence": 0.0,
  "summary": "resumo curto da proposta",
  "suggested_records": {{
    "personagem": null,
    "jutsus": [],
    "habilidades": [],
    "relacionamentos": []
  }},
  "duplicates_to_check": [],
  "missing_required_fields": [],
  "pending_questions": [],
  "source_notes": []
}}
""",
                },
            ],
            temperature=0.1,
            max_tokens=1000,
        )

        raw_content = response.choices[0].message.content or "{}"
        proposal = json.loads(raw_content)

        return {
            "entity": entity,
            "query": query,
            "sources": sources,
            "proposal": proposal,
        }


def save_decision(
    entity: str,
    query: str,
    status: Literal["Aprovado", "Rejeitado"],
    proposal: dict,
    sources: list[dict],
    note: str | None = None,
) -> int:
    return save_curation_decision(
        entity=entity,
        query=query,
        status=status,
        proposal_json=json.dumps(proposal, ensure_ascii=False),
        sources_json=json.dumps(sources, ensure_ascii=False),
        note=note,
    )
