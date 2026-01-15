# 🤖 Dona Maria IA

> Uma assistente de IA que prioriza **honestidade** e **transparência** - ela admite quando não sabe e pesquisa quando precisa.

## 📋 Sobre o Projeto

Dona Maria IA é uma assistente conversacional que se diferencia por sua abordagem honesta:

- 🎯 **Expressa níveis de confiança** em suas respostas
- 🔍 **Pesquisa automaticamente** quando detecta incerteza
- 📊 **Cita fontes** e mostra consenso/divergência entre elas
- 💬 **Admite limitações** de forma clara e natural

## 🏗️ Arquitetura

```
dona-maria-ia/
├── frontend/          # Next.js 15 com App Router
├── backend/           # FastAPI com Python 3.12+
├── docker/            # Configurações Docker
└── docker-compose.yml # Orquestração de serviços
```

### Stack Técnica

| Componente | Tecnologia   | Versão |
| ---------- | ------------ | ------ |
| Frontend   | Next.js      | 15.x   |
| React      | React        | 19.x   |
| Styling    | Tailwind CSS | 4.x    |
| Backend    | FastAPI      | 0.115+ |
| Python     | Python       | 3.12+  |
| Database   | PostgreSQL   | 16     |
| Cache      | Redis        | 7      |

## 🚀 Quick Start

### Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose
- [Node.js](https://nodejs.org/) 20+ (para desenvolvimento local)
- [Python](https://www.python.org/) 3.12+ (para desenvolvimento local)

### Executando com Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/MelhorzinOfficial/Dona-Maria-IA.git
cd Dona-Maria-IA

# Copie as variáveis de ambiente
cp .env.example .env

# Inicie todos os serviços
docker-compose up -d

# Acesse:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - Swagger Docs: http://localhost:8000/docs
```

### Desenvolvimento Local

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Backend

```bash
cd backend

# Usando uv (recomendado)
uv sync
uv run uvicorn app.main:app --reload

# Ou usando pip
pip install -e .
uvicorn app.main:app --reload
```

## 🧪 Testes

### Frontend

```bash
cd frontend
npm test           # Executa testes
npm run test:cov   # Com cobertura
```

### Backend

```bash
cd backend
uv run pytest              # Executa testes
uv run pytest --cov        # Com cobertura
```

## 🔧 Configuração

### Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```env
# Database
DATABASE_URL=postgresql://dona:maria@localhost:5432/donamaria

# Redis
REDIS_URL=redis://localhost:6379

# API Keys (adicione conforme necessário)
OPENAI_API_KEY=your-key-here
```

## 📚 Documentação

- [Arquitetura do Sistema](docs/architecture.md)
- [Guia de Contribuição](CONTRIBUTING.md)
- [API Reference](http://localhost:8000/docs)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Desenvolvido com ❤️ por [Melhorzin Official](https://github.com/MelhorzinOfficial)
