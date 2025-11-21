from fastapi import FastAPI
from pydantic import BaseModel

# OJO: según cómo ejecutes el proyecto, puede que necesites ajustar este import
from backend.rag.query import answer_question


app = FastAPI(
    title="Infolex API",
    description="API de Infolex para consultas jurídicas con RAG",
    version="0.1.0",
)


class Question(BaseModel):
    pregunta: str


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "infolex"}


@app.post("/ask")
def ask_endpoint(q: Question):
    """
    Endpoint principal de Infolex:
    Recibe una pregunta en español y devuelve:
    - respuesta_clara (texto)
    - fragmentos (artículos y textos relevantes)
    """
    respuesta = answer_question(q.pregunta)
    return respuesta
