# Agente de diagnóstico de incidentes

Código-base da prática de construção progressiva de um agente com LangChain, LangGraph e Groq.

O repositório inclui:

- `service.py`: minisserviço FastAPI com métricas e logs simulados;
- `agent.py`: configuração, cliente HTTP, ferramentas e modelo já preparados;
- `visualizacao.py`: exibição pronta do grafo e do fluxo de execução;
- `requirements.txt`: dependências da prática;
- `.env.example`: exemplo das variáveis de ambiente.

Durante a prática, as ferramentas e o modelo são revisados a partir do código pronto. A implementação começa pelo estado e avança por nós, roteamento, montagem e persistência. A visualização fica isolada para não consumir o tempo da aula.

## Pré-requisitos

- Python 3.11 ou superior;
- Git;
- uma chave de API da Groq.

Crie sua chave em [GroqCloud — API Keys](https://console.groq.com/keys).

> Use um Python com GIL (build padrão). Builds free-threaded, como `3.14t`, falham ao instalar o `orjson`.

## 1. Clonar o repositório

```bash
git clone https://github.com/farxC/agente-harness-incidentes.git
cd agente-harness-incidentes
```

## 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

## 3. Ativar o ambiente

No macOS ou Linux:

```bash
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 4. Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configurar as variáveis de ambiente

No macOS ou Linux:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Abra o `.env` e substitua o valor de `GROQ_API_KEY`:

```dotenv
GROQ_API_KEY=gsk_sua-chave-aqui
MODEL_ID=openai/gpt-oss-20b
INCIDENT_SERVICE_URL=http://127.0.0.1:8000
```

O arquivo `.env` está no `.gitignore` e não deve ser enviado ao repositório.

## 6. Iniciar o minisserviço

No primeiro terminal, com a `.venv` ativa, execute o comando para subir o servidor FastAPI:

```bash
uvicorn service:app --reload --port 8000
```

O `--reload` reinicia o servidor automaticamente quando `service.py` muda. O serviço fica em <http://127.0.0.1:8000>.

Verifique se o serviço está disponível:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/services/pagamentos/metrics
curl "http://127.0.0.1:8000/services/pagamentos/logs?nivel=ERROR"
```

A documentação interativa estará disponível em <http://127.0.0.1:8000/docs>.

Mantenha esse terminal aberto durante a execução do agente.

## 7. Começar a prática

Abra outro terminal, entre novamente no projeto e ative a `.venv`:

```bash
cd agente-harness-incidentes
source .venv/bin/activate
```

No Windows PowerShell, use:

```powershell
cd agente-harness-incidentes
.\.venv\Scripts\Activate.ps1
```

Abra `agent.py` e continue a implementação a partir do comentário:

```python
# A prática começa aqui: estado, nós, roteamento, grafo e persistência.
```

Depois de concluir a implementação, com o minisserviço ainda ativo, execute:

```bash
python agent.py
```

A saída final apresenta, nesta ordem:

1. o diagrama ASCII do grafo;
2. os nós, ferramentas e resultados percorridos durante a execução;
3. o diagnóstico produzido pelo modelo.

As funções prontas de `visualizacao.py` usam o *streaming* do LangGraph para mostrar o caminho executado. O pacote `grandalf`, instalado pelo `requirements.txt`, renderiza o diagrama no terminal.
