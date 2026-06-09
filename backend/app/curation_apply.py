from backend.app.database import (
    find_lookup_id,
    get_curation_decision,
    insert_personagem,
    mark_curation_applied,
    mark_curation_error,
    personagem_exists,
    sanitize_personagem_text_lengths,
)


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
    if curation["status"] not in {"Aprovado", "Erro"}:
        raise ValueError("Apenas curadorias aprovadas ou com erro podem ser aplicadas.")
    if curation["entidade"] != "personagem":
        raise ValueError("Preview de aplicacao disponivel apenas para personagem.")

    proposal = curation["proposta"]
    personagem = proposal.get("suggested_records", {}).get("personagem") or {}
    normalized = normalize_personagem(personagem)
    resolved_fields, warnings = resolve_personagem_fields(normalized)
    apply_overrides(resolved_fields, overrides or {})
    resolved_fields, length_warnings = sanitize_personagem_text_lengths(resolved_fields)
    warnings.extend(length_warnings)
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
    for key, value in overrides.items():
        normalized_key = str(key).lower()
        if normalized_key in PERSONAGEM_INSERT_FIELDS and value not in ("", None):
            resolved_fields[normalized_key] = normalize_override_value(normalized_key, value)


def normalize_override_value(field: str, value):
    integer_fields = {
        "idtipopersonagem",
        "idcla",
        "idarcoaparicao",
        "idarcomorte",
        "idocupacaoclassico",
        "idocupacaoshippuden",
        "idvila",
        "idadeclasico",
        "idadeshippuden",
        "missoescompletas",
    }
    decimal_fields = {"alturaclassico", "alturashippuden"}

    if field in integer_fields:
        return int(value)
    if field in decimal_fields:
        return float(value)

    return value


def apply_curation_to_database(curation_id: int, overrides: dict | None = None) -> dict:
    try:
        preview = build_apply_preview(curation_id, overrides=overrides)

        if preview["status"] != "ready" or not preview["operations"]:
            raise ValueError("Preview ainda possui campos criticos pendentes.")

        operation = preview["operations"][0]
        data = operation["data"]

        if personagem_exists(data["nome"], data.get("sobrenome")):
            raise ValueError("Personagem ja existe no banco com o mesmo nome e sobrenome.")

        personagem_id = insert_personagem(data)
        mark_curation_applied(curation_id)

        return {
            "status": "Aplicado",
            "idpersonagem": personagem_id,
            "operation": operation,
        }
    except Exception as error:
        mark_curation_error(curation_id, str(error))
        raise


def normalize_personagem(personagem: dict) -> dict:
    normalized = {str(key).lower(): value for key, value in personagem.items()}

    sexo = normalized.get("sexo")
    if isinstance(sexo, str):
        normalized["sexo"] = "Masculino" if sexo.lower().startswith("masc") else "Feminino" if sexo.lower().startswith("fem") else sexo

    estado = normalized.get("estado")
    if isinstance(estado, str):
        estado_normalizado = estado.strip().lower()
        if estado_normalizado in {"vivo", "viva", "alive"}:
            normalized["estado"] = "Vivo"
        elif estado_normalizado in {"morto", "morta", "falecido", "falecida", "dead"}:
            normalized["estado"] = "Morto"
        else:
            normalized["estado"] = estado

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
