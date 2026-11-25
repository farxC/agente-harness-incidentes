# Agente de diagnóstico de incidentes

Código-base da prática de construção progressiva de um agente com LangChain, LangGraph e Groq.

O repositório inclui:

- `service.py`: minisserviço FastAPI com métricas e logs simulados;
- `agent.py`: imports, configuração do modelo, URL do minisserviço e prompt de sistema;
- `requirements.txt`: dependências da prática;
- `.env.example`: exemplo das variáveis de ambiente.

Durante a prática, a implementação do agente começa pelas ferramentas HTTP e avança por estado, nós, roteamento, montagem e persistência.

## Pré-requisitos

- Python 3.11 ou superior;
- Git;
- uma chave de API da Groq.

Crie sua chave em [GroqCloud — API Keys](https://console.groq.com/keys).

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
MODEL_ID=llama-3.3-70b-versatile
INCIDENT_SERVICE_URL=http://127.0.0.1:8000
```

O arquivo `.env` está no `.gitignore` e não deve ser enviado ao repositório.

## 6. Iniciar o minisserviço

No primeiro terminal, com a `.venv` ativa, execute:

```bash
uvicorn service:app --reload --port 8000
```

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
# A implementação das ferramentas e do grafo começa aqui durante a prática.
```

Depois de concluir a implementação, com o minisserviço ainda ativo, execute:

```bash
python agent.py
```
