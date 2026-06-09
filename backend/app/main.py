import logging
from typing import Literal

from fastapi import Header, HTTPException, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.app.config import get_admin_token, get_cors_origins
from backend.app.curator import CurationService, EntityType, save_decision
from backend.app.database import list_curation_decisions
from backend.app.oracle import build_oracle_service


logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)


class ChatResponse(BaseModel):
    answer: str
    sql: str
    rows: list[dict]


class CurationProposeRequest(BaseModel):
    entity: EntityType
    query: str = Field(..., min_length=2, max_length=200)
    notes: str = Field(default="", max_length=1000)


class CurationProposeResponse(BaseModel):
    entity: str
    query: str
    sources: list[dict]
    proposal: dict


class CurationDecisionRequest(BaseModel):
    entity: str = Field(..., min_length=2, max_length=50)
    query: str = Field(..., min_length=2, max_length=200)
    status: Literal["Aprovado", "Rejeitado"]
    proposal: dict
    sources: list[dict]
    note: str | None = Field(default=None, max_length=1000)


class CurationDecisionResponse(BaseModel):
    id: int
    status: str


class CurationItem(BaseModel):
    idcuradoria: int
    entidade: str
    consulta: str
    status: str
    proposta: dict
    fontes: list[dict]
    observacao: str | None = None
    criadoem: str


app = FastAPI(title="Konoha Oracle API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


def require_admin_token(x_admin_token: str | None = Header(default=None)) -> None:
    try:
        expected_token = get_admin_token()
    except RuntimeError:
        raise HTTPException(status_code=503, detail="Admin nao configurado.") from None

    if x_admin_token != expected_token:
        raise HTTPException(status_code=401, detail="Token admin invalido.")


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    try:
        result = build_oracle_service().ask(payload.question)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        logger.exception("Erro inesperado ao processar pergunta.")
        raise HTTPException(status_code=500, detail="Erro ao processar pergunta.") from error

    return ChatResponse(**result)


@app.post("/admin/curation/propose", response_model=CurationProposeResponse)
def propose_curation(
    payload: CurationProposeRequest,
    x_admin_token: str | None = Header(default=None),
) -> CurationProposeResponse:
    require_admin_token(x_admin_token)

    try:
        result = CurationService().propose(payload.entity, payload.query, payload.notes)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        logger.exception("Erro ao gerar proposta de curadoria.")
        raise HTTPException(status_code=500, detail="Erro ao gerar proposta de curadoria.") from error

    return CurationProposeResponse(**result)


@app.post("/admin/curation/decision", response_model=CurationDecisionResponse)
def decide_curation(
    payload: CurationDecisionRequest,
    x_admin_token: str | None = Header(default=None),
) -> CurationDecisionResponse:
    require_admin_token(x_admin_token)

    try:
        curation_id = save_decision(
            entity=payload.entity,
            query=payload.query,
            status=payload.status,
            proposal=payload.proposal,
            sources=payload.sources,
            note=payload.note,
        )
    except Exception as error:
        logger.exception("Erro ao salvar decisao de curadoria.")
        raise HTTPException(status_code=500, detail="Erro ao salvar decisao de curadoria.") from error

    return CurationDecisionResponse(id=curation_id, status=payload.status)


@app.get("/admin/curation/items", response_model=list[CurationItem])
def list_curation_items(
    status: Literal["Aprovado", "Rejeitado"] | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    x_admin_token: str | None = Header(default=None),
) -> list[CurationItem]:
    require_admin_token(x_admin_token)

    try:
        rows = list_curation_decisions(status=status, limit=limit)
    except Exception as error:
        logger.exception("Erro ao listar curadorias.")
        raise HTTPException(status_code=500, detail="Erro ao listar curadorias.") from error

    return [CurationItem(**row) for row in rows]
