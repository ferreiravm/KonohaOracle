import json
import re
from typing import Literal
from urllib.parse import quote
from urllib.parse import urlencode

import httpx
from openai import OpenAI

from backend.app.config import get_openai_api_key
from backend.app.database import load_database_structure, save_curation_decision


EntityType = Literal["personagem", "jutsu", "arco", "vila", "cla", "grupo", "ferramenta"]
WIKI_HEADERS = {
    "User-Agent": "KonohaOracle/1.0 (curation research; https://github.com/ferreiravm/KonohaOracle)",
}


def _mediawiki_search_url(base_url: str, query: str, limit: int = 3) -> str:
    params = urlencode(
        {
            "action": "opensearch",
            "search": query,
            "limit": limit,
            "namespace": 0,
            "format": "json",
        }
    )
    return f"{base_url}/w/api.php?{params}"


def _fandom_search_url(query: str, limit: int = 5) -> str:
    params = urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "format": "json",
        }
    )
    return f"https://naruto.fandom.com/api.php?{params}"


def _fandom_extract_url(title: str) -> str:
    params = urlencode(
        {
            "action": "parse",
            "page": title,
            "prop": "text",
            "format": "json",
        }
    )
    return f"https://naruto.fandom.com/api.php?{params}"


def search_public_context(query: str) -> list[dict]:
    with httpx.Client(timeout=12.0, follow_redirects=True, headers=WIKI_HEADERS) as client:
        results = []
        results.extend(search_wikipedia(client, "https://pt.wikipedia.org", "Wikipedia PT", query))

        if len(results) < 2:
            results.extend(search_wikipedia(client, "https://en.wikipedia.org", "Wikipedia EN", query))

        if len(results) < 2:
            results.extend(search_fandom(client, query))

    return dedupe_sources(results)[:6]


def search_wikipedia(client: httpx.Client, base_url: str, source_name: str, query: str) -> list[dict]:
    search_response = client.get(_mediawiki_search_url(base_url, query))
    if search_response.status_code >= 400:
        return []

    payload = search_response.json()
    titles = payload[1] if len(payload) > 1 else []
    descriptions = payload[2] if len(payload) > 2 else []
    urls = payload[3] if len(payload) > 3 else []

    results = []
    rest_base_url = base_url.replace("www.", "")
    for index, title in enumerate(titles[:3]):
        summary_url = f"{rest_base_url}/api/rest_v1/page/summary/{quote(title, safe='')}"
        summary_response = client.get(summary_url)
        summary = ""
        if summary_response.status_code == 200:
            summary = summary_response.json().get("extract", "")

        results.append(
            {
                "source": source_name,
                "title": title,
                "description": descriptions[index] if index < len(descriptions) else "",
                "url": urls[index] if index < len(urls) else "",
                "summary": summary,
            }
        )

    return results


def search_fandom(client: httpx.Client, query: str) -> list[dict]:
    search_response = client.get(_fandom_search_url(query))
    if search_response.status_code >= 400:
        return []

    search_results = search_response.json().get("query", {}).get("search", [])
    results = []

    for item in search_results[:5]:
        title = item.get("title", "")
        url = f"https://naruto.fandom.com/wiki/{quote(title.replace(' ', '_'), safe='/_:')}"
        summary = get_fandom_extract(client, title)
        if not summary:
            summary = re.sub("<[^<]+?>", "", item.get("snippet", ""))
        results.append(
            {
                "source": "Naruto Wiki/Fandom",
                "title": title,
                "description": "",
                "url": url,
                "summary": summary,
            }
        )

    return results


def get_fandom_extract(client: httpx.Client, title: str) -> str:
    response = client.get(_fandom_extract_url(title))
    if response.status_code >= 400:
        return ""

    html = response.json().get("parse", {}).get("text", {}).get("*", "")
    text = html_to_text(html)
    return text[:1500]


def html_to_text(html: str) -> str:
    text = re.sub(r"<table.*?</table>", " ", html, flags=re.DOTALL)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<sup.*?</sup>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^<]+?>", " ", text)
    text = re.sub(r"\[[^\]]+\]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def dedupe_sources(sources: list[dict]) -> list[dict]:
    seen = set()
    unique_sources = []

    for source in sources:
        key = (source.get("source", ""), source.get("title", ""), source.get("url", ""))
        if key in seen:
            continue
        seen.add(key)
        unique_sources.append(source)

    return unique_sources


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
        proposal = parse_json_response(raw_content)

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


def parse_json_response(raw_content: str) -> dict:
    cleaned = raw_content.strip().replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise
