from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Query


app = FastAPI(
    title="Minisserviço de incidentes",
    description="Expõe métricas e logs simulados para a prática de agentes.",
    version="1.0.0",
)

SERVICOS_MONITORADOS = {
    "pagamentos": {
        "metricas": {
            "status": "degradado",
            "latencia_p95_ms": 2_840,
            "taxa_erros_percentual": 18.7,
            "disponibilidade_percentual": 81.3,
        },
        "logs": [
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
    },
    "autenticacao": {
        "metricas": {
            "status": "saudavel",
            "latencia_p95_ms": 180,
            "taxa_erros_percentual": 0.4,
            "disponibilidade_percentual": 99.96,
        },
        "logs": [
            {
                "nivel": "WARN",
                "mensagem": "Tentativa de login com token expirado",
                "ocorrencias": 4,
            }
        ],
    },
}


def obter_servico(nome: str) -> dict:
    servico = SERVICOS_MONITORADOS.get(nome.lower())
    if servico is None:
        raise HTTPException(
            status_code=404,
            detail={
                "erro": "servico_nao_encontrado",
                "servico": nome,
                "servicos_disponiveis": sorted(SERVICOS_MONITORADOS),
            },
        )
    return servico


@app.get("/")
def inicio() -> dict:
    return {
        "nome": "minisservico-de-incidentes",
        "documentacao": "/docs",
        "servicos": sorted(SERVICOS_MONITORADOS),
    }


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "observado_em": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/services")
def listar_servicos() -> dict:
    return {"servicos": sorted(SERVICOS_MONITORADOS)}


@app.get("/services/{nome}/metrics")
def consultar_metricas(nome: str) -> dict:
    servico = obter_servico(nome)
    return {
        "servico": nome.lower(),
        "observado_em": datetime.now(timezone.utc).isoformat(),
        **servico["metricas"],
    }


@app.get("/services/{nome}/logs")
def consultar_logs(
    nome: str,
    nivel: str | None = Query(default=None, description="ERROR, WARN ou INFO"),
) -> dict:
    servico = obter_servico(nome)
    logs = servico["logs"]

    if nivel:
        nivel_normalizado = nivel.upper()
        logs = [log for log in logs if log["nivel"] == nivel_normalizado]
    else:
        nivel_normalizado = None

    return {
        "servico": nome.lower(),
        "nivel": nivel_normalizado,
        "observado_em": datetime.now(timezone.utc).isoformat(),
        "logs": logs,
    }
