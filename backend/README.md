# Dona Maria IA - Backend

API Backend desenvolvida com FastAPI para a Dona Maria IA.

## Stack

- **FastAPI** 0.115+
- **Python** 3.12+
- **Pydantic** 2.x
- **PostgreSQL** 16
- **Redis** 7

## Setup Local

```bash
# Instalar dependências
pip install -e ".[dev]"

# Rodar servidor de desenvolvimento
uvicorn app.main:app --reload

# Rodar testes
pytest

# Linting
ruff check .
ruff format .

# Type checking
mypy app
```

## Estrutura

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── config/
│   │   └── settings.py   # Pydantic Settings
│   ├── api/
│   │   └── v1/
│   │       └── router.py # API routes
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   └── schemas/          # Pydantic schemas
└── tests/
    └── test_main.py
```

## Endpoints

- `GET /` - Informações da API
- `GET /health` - Health check
- `GET /docs` - Swagger UI
- `GET /api/v1/status` - Status da API v1
