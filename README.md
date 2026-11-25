# Agente de diagnóstico de incidentes

Código-base da prática de construção progressiva de um agente com LangChain, LangGraph e Groq.

O arquivo `agent.py` já contém os imports, as métricas simuladas, os logs simulados e o prompt de sistema. Durante a prática, a implementação começa pelas ferramentas e avança por estado, nós, roteamento, montagem e persistência.

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

Abra o arquivo `.env` e substitua o valor de `GROQ_API_KEY` pela sua chave:

```dotenv
GROQ_API_KEY=gsk_sua-chave-aqui
MODEL_ID=llama-3.3-70b-versatile
```

O arquivo `.env` está no `.gitignore` e não deve ser enviado ao repositório.

## 6. Começar a prática

Abra `agent.py` e continue a implementação a partir do comentário:

```python
# A implementação das ferramentas e do grafo começa aqui durante a prática.
```

Depois de concluir a implementação, execute:

```bash
python agent.py
```
