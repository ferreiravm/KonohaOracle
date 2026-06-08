from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.app.config import get_cors_origins
from backend.app.oracle import build_oracle_service


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)


class ChatResponse(BaseModel):
    answer: str
    sql: str
    rows: list[dict]


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


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    try:
        result = build_oracle_service().ask(payload.question)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="Erro ao processar pergunta.") from error

    return ChatResponse(**result)
