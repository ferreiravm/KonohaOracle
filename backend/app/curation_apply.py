from backend.app.database import find_lookup_id, get_curation_decision


PERSONAGEM_INSERT_FIELDS = [
    "idtipopersonagem",
    "idcla",
    "idarcoaparicao",
    "idarcomorte",
    "idocupacaoclassico",
    "idocupacaoshippuden",
    "idvila",
    "nome",
    "sobrenome",
    "idadeclasico",
    "idadeshippuden",
    "sexo",
    "datanascimento",
    "alturaclassico",
    "alturashippuden",
    "corcabelo",
    "corolhos",
    "corpele",
    "descricaoroupaclassico",
    "descricaoroupashippuden",
    "missoescompletas",
    "descricao",
    "historiapersonagem",
    "estado",
]

REQUIRED_PERSONAGEM_FIELDS = [
    "idtipopersonagem",
    "idarcoaparicao",
    "nome",
    "sexo",
    "estado",
]


def build_apply_preview(curation_id: int, overrides: dict | None = None) -> dict:
    curation = get_curation_decision(curation_id)
    if not curation:
        raise ValueError("Curadoria nao encontrada.")
    if curation["status"] != "Aprovado":
        raise ValueError("Apenas curadorias aprovadas podem ser aplicadas.")
    if curation["entidade"] != "personagem":
        raise ValueError("Preview de aplicacao disponivel apenas para personagem.")

    proposal = curation["proposta"]
    personagem = proposal.get("suggested_records", {}).get("personagem") or {}
    normalized = normalize_personagem(personagem)
    resolved_fields, warnings = resolve_personagem_fields(normalized)
    apply_overrides(resolved_fields, overrides or {})
    critical_missing = [field for field in REQUIRED_PERSONAGEM_FIELDS if not resolved_fields.get(field)]

    operations = []
    if not critical_missing:
        insert_data = {
            field: resolved_fields[field]
            for field in PERSONAGEM_INSERT_FIELDS
            if resolved_fields.get(field) is not None
        }
        operations.append(
            {
                "table": "Personagens",
                "action": "insert",
                "data": insert_data,
            }
        )

    return {
        "curation_id": curation_id,
        "status": "blocked" if critical_missing else "ready",
        "entity": curation["entidade"],
        "query": curation["consulta"],
        "operations": operations,
        "resolved_fields": resolved_fields,
        "critical_missing": critical_missing,
        "warnings": warnings,
        "next_required_action": (
            "Complete os campos criticos antes de aplicar ao banco."
            if critical_missing
            else "Preview pronto para a futura etapa de aplicacao."
        ),
    }


def apply_overrides(resolved_fields: dict, overrides: dict) -> None:
    allowed_overrides = {
        "idtipopersonagem",
        "idarcoaparicao",
        "estado",
        "sexo",
        "idcla",
        "idvila",
        "idocupacaoclassico",
        "idocupacaoshippuden",
        "idarcomorte",
    }

    for key, value in overrides.items():
        normalized_key = str(key).lower()
        if normalized_key in allowed_overrides and value not in ("", None):
            resolved_fields[normalized_key] = value


def normalize_personagem(personagem: dict) -> dict:
    normalized = {str(key).lower(): value for key, value in personagem.items()}

    sexo = normalized.get("sexo")
    if isinstance(sexo, str):
        normalized["sexo"] = "Masculino" if sexo.lower().startswith("masc") else "Feminino" if sexo.lower().startswith("fem") else sexo

    estado = normalized.get("estado")
    if isinstance(estado, str):
        normalized["estado"] = "Vivo" if estado.lower() == "vivo" else "Morto" if estado.lower() == "morto" else estado

    return normalized


def resolve_personagem_fields(personagem: dict) -> tuple[dict, list[str]]:
    resolved = {field: personagem.get(field) for field in PERSONAGEM_INSERT_FIELDS}
    warnings = []

    if not resolved.get("idcla") and personagem.get("sobrenome"):
        clan_id = find_lookup_id("clas", "idcla", "nome", personagem["sobrenome"])
        if clan_id:
            resolved["idcla"] = clan_id
        else:
            warnings.append(f"Cla nao encontrado para sobrenome '{personagem['sobrenome']}'.")

    if not resolved.get("idvila"):
        description = f"{personagem.get('descricao') or ''} {personagem.get('historiapersonagem') or ''}".lower()
        if "konohagakure" in description or "konoha" in description:
            village_id = find_lookup_id("vilas", "idvila", "nome", "Vila Oculta da Folha")
            if village_id:
                resolved["idvila"] = village_id

    if resolved.get("sexo") not in {None, "Masculino", "Feminino"}:
        warnings.append("Sexo precisa ser 'Masculino' ou 'Feminino'.")

    if resolved.get("estado") not in {None, "Vivo", "Morto"}:
        warnings.append("Estado precisa ser 'Vivo' ou 'Morto'.")

    return resolved, warnings
