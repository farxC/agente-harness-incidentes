import json
import operator
import os
from typing import Annotated, Literal

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


load_dotenv()

MODEL_ID = os.getenv("MODEL_ID", "llama-3.3-70b-versatile")

METRICAS = {
    "pagamentos": {
        "latencia_p95_ms": 2_840,
        "taxa_erros_percentual": 18.7,
    },
    "autenticacao": {
        "latencia_p95_ms": 180,
        "taxa_erros_percentual": 0.4,
    },
}

LOGS = {
    "pagamentos": [
        {
            "nivel": "ERROR",
            "mensagem": "Timeout ao chamar o gateway bancário",
            "ocorrencias": 37,
        },
        {
            "nivel": "ERROR",
            "mensagem": "Circuit breaker aberto para gateway bancário",
            "ocorrencias": 12,
        },
        {
            "nivel": "WARN",
            "mensagem": "Pool de conexões acima de 90%",
            "ocorrencias": 8,
        },
    ],
    "autenticacao": [
        {
            "nivel": "WARN",
            "mensagem": "Tentativa de login com token expirado",
            "ocorrencias": 4,
        }
    ],
}

SYSTEM_PROMPT = """
Você é um agente de diagnóstico de incidentes.

Regras:
- use consultar_metricas para verificar a saúde do serviço citado;
- quando houver anomalia ou o usuário pedir evidências, use consultar_logs;
- diferencie fatos observados de hipóteses;
- não invente métricas, logs ou causas;
- apresente evidências, hipótese principal e próxima ação recomendada;
- se o serviço não existir, informe quais serviços podem ser consultados.
""".strip()


# A implementação das ferramentas e do grafo começa aqui durante a prática.
