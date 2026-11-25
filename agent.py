import json
import operator
import os
from typing import Annotated, Literal
from urllib.parse import quote

import httpx
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


load_dotenv()

MODEL_ID = os.getenv("MODEL_ID", "openai/gpt-oss-20b")
INCIDENT_SERVICE_URL = os.getenv(
    "INCIDENT_SERVICE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

SYSTEM_PROMPT = """
Você é um agente de diagnóstico de incidentes.

Regras:
- use consultar_metricas para verificar a saúde do serviço citado;
- quando houver anomalia ou o usuário pedir evidências, use consultar_logs;
- diferencie fatos observados de hipóteses;
- não invente métricas, logs ou causas;
- apresente evidências, hipótese principal e próxima ação recomendada;
- se o serviço não existir, informe os serviços disponíveis;
- se o minisserviço estiver indisponível, explique como iniciá-lo.
""".strip()


def consultar_minisservico(
    caminho: str,
    parametros: dict[str, str] | None = None,
) -> str:
    """Executa uma consulta HTTP no minisserviço e normaliza o resultado."""
    try:
        resposta = httpx.get(
            f"{INCIDENT_SERVICE_URL}{caminho}",
            params=parametros,
            timeout=5.0,
        )
        resposta.raise_for_status()
        return json.dumps(resposta.json(), ensure_ascii=False)
    except httpx.HTTPStatusError as erro:
        return json.dumps(
            {
                "erro": "resposta_invalida",
                "status": erro.response.status_code,
                "detalhe": erro.response.text,
            },
            ensure_ascii=False,
        )
    except httpx.RequestError as erro:
        return json.dumps(
            {
                "erro": "minisservico_indisponivel",
                "detalhe": str(erro),
            },
            ensure_ascii=False,
        )


# A implementação das ferramentas e do grafo começa aqui durante a prática.
