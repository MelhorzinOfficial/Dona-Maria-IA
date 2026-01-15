# Architecture Document — Dona-Maria-IA

**Versão:** 1.0.0  
**Data:** 2026-01-15  
**Autor:** Raposo  
**Arquiteto:** Winston

---

## Executive Summary

Este documento define a arquitetura técnica do **Dona-Maria-IA** — um LLM revolucionário construído com o princípio de **honestidade radical**. A arquitetura prioriza:

- 🎯 **Honestidade** — Motor de detecção de incerteza e admissão de limitações
- 🔍 **Pesquisa Multi-Fonte** — Integração com múltiplas APIs de busca
- 📊 **Transparência Estatística** — Cálculo e exibição de confiança em tempo real
- ⚡ **Performance** — Streaming de respostas com latência otimizada
- 🔧 **Escalabilidade** — Arquitetura cloud-native pronta para crescer

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DONA-MARIA-IA ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                           CLIENT LAYER                                   │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                   │   │
│  │  │   Next.js    │  │   React      │  │  Tailwind    │                   │   │
│  │  │   App Router │  │   Components │  │  CSS + UI    │                   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                           API GATEWAY                                    │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                   │   │
│  │  │   Auth       │  │   Rate       │  │   WebSocket  │                   │   │
│  │  │   Middleware │  │   Limiter    │  │   Handler    │                   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        APPLICATION LAYER                                 │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐   │   │
│  │  │   Honesty    │  │   Research   │  │  Confidence  │  │   Code     │   │   │
│  │  │   Engine     │  │   Orchestrator│ │  Calculator  │  │   Analyzer │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                           LLM LAYER                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                   │   │
│  │  │   Model      │  │   Prompt     │  │   Response   │                   │   │
│  │  │   Router     │  │   Builder    │  │   Streamer   │                   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        DATA LAYER                                        │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐   │   │
│  │  │   PostgreSQL │  │   Redis      │  │   Vector     │  │   S3/Blob  │   │   │
│  │  │   (Primary)  │  │   (Cache)    │  │   DB (RAG)   │  │   Storage  │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      EXTERNAL SERVICES                                   │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐   │   │
│  │  │   Search     │  │   LLM        │  │   Auth       │  │   CDN      │   │   │
│  │  │   APIs       │  │   Providers  │  │   Providers  │  │   (Assets) │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend

| Tecnologia         | Versão | Justificativa                                   |
| ------------------ | ------ | ----------------------------------------------- |
| **Next.js**        | 15.x   | App Router, Server Components, streaming nativo |
| **React**          | 19.x   | Concurrent features, Suspense para streaming    |
| **TypeScript**     | 5.x    | Type safety, melhor DX                          |
| **Tailwind CSS**   | 4.x    | Design system customizável, performance         |
| **Zustand**        | 5.x    | State management leve e eficiente               |
| **TanStack Query** | 5.x    | Server state, caching, mutations                |

### Backend

| Tecnologia    | Versão | Justificativa                         |
| ------------- | ------ | ------------------------------------- |
| **Python**    | 3.12+  | Ecossistema ML/AI maduro              |
| **FastAPI**   | 0.115+ | Async nativo, WebSocket, OpenAPI auto |
| **LangChain** | 0.3.x  | Orquestração de LLMs, chains, agents  |
| **LangGraph** | 0.2.x  | Workflows complexos de AI             |
| **Pydantic**  | 2.x    | Validação de dados, serialização      |

### LLM & AI

| Tecnologia        | Uso                                   |
| ----------------- | ------------------------------------- |
| **Claude 3.5**    | Modelo principal para raciocínio      |
| **GPT-4o**        | Fallback e comparação de respostas    |
| **Mistral Large** | Opção open-weight para reduzir custos |
| **OpenRouter**    | API gateway para múltiplos provedores |

### Database & Storage

| Tecnologia     | Uso                                        |
| -------------- | ------------------------------------------ |
| **PostgreSQL** | Dados relacionais (users, conversations)   |
| **Redis**      | Cache de respostas, sessões, rate limiting |
| **Pinecone**   | Vector DB para RAG e busca semântica       |
| **S3/R2**      | Storage de arquivos e exports              |

### Infrastructure

| Tecnologia         | Uso                             |
| ------------------ | ------------------------------- |
| **Vercel**         | Deploy frontend, Edge Functions |
| **Railway/Fly.io** | Backend Python, auto-scaling    |
| **Cloudflare**     | CDN, WAF, DDoS protection, R2   |
| **Upstash**        | Redis serverless                |

---

## Core Components

### 1. Honesty Engine (Motor de Honestidade)

O coração diferencial do Dona-Maria-IA. Responsável por detectar incerteza e decidir quando pesquisar.

```python
# services/honesty_engine.py

from enum import Enum
from pydantic import BaseModel
from typing import Optional

class ConfidenceLevel(Enum):
    HIGH = "high"           # 80-100% - resposta direta
    MEDIUM = "medium"       # 50-79% - resposta com ressalvas
    LOW = "low"             # 20-49% - pesquisa recomendada
    UNKNOWN = "unknown"     # 0-19% - pesquisa obrigatória

class HonestyAssessment(BaseModel):
    confidence_score: float          # 0.0 - 1.0
    confidence_level: ConfidenceLevel
    should_research: bool
    uncertainty_signals: list[str]   # sinais detectados
    knowledge_gaps: list[str]        # lacunas identificadas
    reasoning: str                   # explicação da decisão

class HonestyEngine:
    """
    Motor de detecção de incerteza e honestidade.
    Analisa a query e o conhecimento do modelo para decidir a melhor ação.
    """

    UNCERTAINTY_THRESHOLD = 0.6  # Abaixo disso, pesquisar

    UNCERTAINTY_SIGNALS = [
        "não tenho certeza",
        "acredito que",
        "provavelmente",
        "talvez",
        "pode ser",
        "não sei ao certo",
        "baseado no meu conhecimento até",
        "preciso verificar",
    ]

    async def assess(
        self,
        query: str,
        preliminary_response: str,
        model_confidence: float
    ) -> HonestyAssessment:
        """
        Avalia a honestidade necessária para uma resposta.
        """
        # 1. Detectar sinais de incerteza na resposta preliminar
        uncertainty_signals = self._detect_uncertainty_signals(preliminary_response)

        # 2. Identificar lacunas de conhecimento na query
        knowledge_gaps = await self._identify_knowledge_gaps(query)

        # 3. Calcular score de confiança composto
        confidence_score = self._calculate_confidence(
            model_confidence=model_confidence,
            uncertainty_count=len(uncertainty_signals),
            knowledge_gap_count=len(knowledge_gaps)
        )

        # 4. Determinar nível e ação
        confidence_level = self._determine_level(confidence_score)
        should_research = confidence_score < self.UNCERTAINTY_THRESHOLD

        return HonestyAssessment(
            confidence_score=confidence_score,
            confidence_level=confidence_level,
            should_research=should_research,
            uncertainty_signals=uncertainty_signals,
            knowledge_gaps=knowledge_gaps,
            reasoning=self._generate_reasoning(confidence_score, uncertainty_signals)
        )

    def _detect_uncertainty_signals(self, text: str) -> list[str]:
        """Detecta frases que indicam incerteza no texto."""
        found = []
        text_lower = text.lower()
        for signal in self.UNCERTAINTY_SIGNALS:
            if signal in text_lower:
                found.append(signal)
        return found

    async def _identify_knowledge_gaps(self, query: str) -> list[str]:
        """
        Identifica tópicos na query que podem ter lacunas de conhecimento.
        Ex: datas recentes, eventos específicos, dados estatísticos.
        """
        gaps = []

        # Detectar referências a tempo recente
        if any(word in query.lower() for word in ["2025", "2026", "hoje", "ontem", "semana passada"]):
            gaps.append("informação recente (após cutoff do modelo)")

        # Detectar pedidos de dados específicos
        if any(word in query.lower() for word in ["quantos", "porcentagem", "estatística", "dados"]):
            gaps.append("dados estatísticos específicos")

        # Detectar perguntas sobre pessoas/empresas específicas
        if any(word in query.lower() for word in ["quem é", "o que aconteceu", "empresa"]):
            gaps.append("informação factual específica")

        return gaps

    def _calculate_confidence(
        self,
        model_confidence: float,
        uncertainty_count: int,
        knowledge_gap_count: int
    ) -> float:
        """Calcula score de confiança composto."""
        # Penalizar por sinais de incerteza
        uncertainty_penalty = uncertainty_count * 0.1

        # Penalizar por lacunas de conhecimento
        gap_penalty = knowledge_gap_count * 0.15

        # Calcular score final
        score = model_confidence - uncertainty_penalty - gap_penalty

        return max(0.0, min(1.0, score))  # Clamp entre 0 e 1

    def _determine_level(self, score: float) -> ConfidenceLevel:
        """Determina o nível de confiança baseado no score."""
        if score >= 0.8:
            return ConfidenceLevel.HIGH
        elif score >= 0.5:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.2:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.UNKNOWN

    def _generate_reasoning(
        self,
        score: float,
        signals: list[str]
    ) -> str:
        """Gera explicação legível da decisão."""
        if score >= 0.8:
            return "Alta confiança baseada no conhecimento do modelo."
        elif score >= 0.5:
            return f"Confiança média. Sinais de incerteza: {', '.join(signals) if signals else 'nenhum específico'}."
        else:
            return "Baixa confiança. Recomendada pesquisa em fontes externas para validação."
```

### 2. Research Orchestrator (Orquestrador de Pesquisa)

Coordena a busca em múltiplas fontes e agrega resultados.

```python
# services/research_orchestrator.py

import asyncio
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Source(BaseModel):
    id: str
    title: str
    url: str
    snippet: str
    authority_score: float       # 0.0 - 1.0
    publication_date: Optional[datetime]
    domain: str

class ResearchResult(BaseModel):
    query: str
    sources: list[Source]
    consensus_score: float       # Quanto as fontes concordam
    consensus_summary: str
    divergences: list[str]       # Pontos de divergência
    total_sources_consulted: int
    research_time_ms: int

class ResearchOrchestrator:
    """
    Orquestra pesquisa multi-fonte em paralelo.
    """

    MIN_SOURCES = 5
    MAX_SOURCES = 15
    TIMEOUT_SECONDS = 8

    def __init__(
        self,
        search_providers: list,  # Tavily, Serper, Brave, etc.
        source_ranker,           # Rankeia fontes por autoridade
        consensus_analyzer,      # Analisa consenso entre fontes
    ):
        self.search_providers = search_providers
        self.source_ranker = source_ranker
        self.consensus_analyzer = consensus_analyzer

    async def research(self, query: str) -> ResearchResult:
        """
        Executa pesquisa paralela em múltiplos provedores.
        """
        start_time = datetime.now()

        # 1. Buscar em todos os provedores em paralelo
        search_tasks = [
            self._search_provider(provider, query)
            for provider in self.search_providers
        ]

        results = await asyncio.gather(
            *search_tasks,
            return_exceptions=True
        )

        # 2. Combinar e deduplicar resultados
        all_sources = self._combine_results(results)

        # 3. Rankear por autoridade
        ranked_sources = await self.source_ranker.rank(all_sources)

        # 4. Selecionar top N fontes
        top_sources = ranked_sources[:self.MAX_SOURCES]

        # 5. Analisar consenso e divergências
        consensus = await self.consensus_analyzer.analyze(top_sources)

        research_time = (datetime.now() - start_time).total_seconds() * 1000

        return ResearchResult(
            query=query,
            sources=top_sources,
            consensus_score=consensus.score,
            consensus_summary=consensus.summary,
            divergences=consensus.divergences,
            total_sources_consulted=len(all_sources),
            research_time_ms=int(research_time)
        )

    async def _search_provider(self, provider, query: str) -> list[Source]:
        """Busca em um provedor específico com timeout."""
        try:
            return await asyncio.wait_for(
                provider.search(query),
                timeout=self.TIMEOUT_SECONDS
            )
        except asyncio.TimeoutError:
            return []
        except Exception as e:
            # Log error, return empty
            return []

    def _combine_results(self, results: list) -> list[Source]:
        """Combina resultados e remove duplicatas por URL."""
        seen_urls = set()
        combined = []

        for result in results:
            if isinstance(result, Exception):
                continue
            for source in result:
                if source.url not in seen_urls:
                    seen_urls.add(source.url)
                    combined.append(source)

        return combined
```

### 3. Confidence Calculator (Calculador de Confiança)

Calcula o percentual de confiança baseado em múltiplos fatores.

```python
# services/confidence_calculator.py

from pydantic import BaseModel
from typing import Optional

class ConfidenceBreakdown(BaseModel):
    overall_score: float              # Score final 0-100%
    model_confidence: float           # Confiança do modelo base
    source_agreement: float           # Concordância entre fontes
    source_authority: float           # Média de autoridade das fontes
    recency_factor: float             # Quão recentes são as fontes
    components_explanation: str       # Explicação legível

class ConfidenceCalculator:
    """
    Calcula score de confiança composto baseado em múltiplos fatores.
    """

    # Pesos para cada componente
    WEIGHTS = {
        "model_confidence": 0.25,
        "source_agreement": 0.35,
        "source_authority": 0.25,
        "recency_factor": 0.15,
    }

    def calculate(
        self,
        model_confidence: float,
        sources: list,
        consensus_score: float,
    ) -> ConfidenceBreakdown:
        """
        Calcula confiança baseado em todos os fatores.
        """
        # 1. Calcular autoridade média das fontes
        source_authority = self._calculate_authority_average(sources)

        # 2. Calcular fator de recência
        recency_factor = self._calculate_recency_factor(sources)

        # 3. Score de concordância vem do consensus analyzer
        source_agreement = consensus_score

        # 4. Calcular score final ponderado
        overall_score = (
            self.WEIGHTS["model_confidence"] * model_confidence +
            self.WEIGHTS["source_agreement"] * source_agreement +
            self.WEIGHTS["source_authority"] * source_authority +
            self.WEIGHTS["recency_factor"] * recency_factor
        )

        # Converter para percentual
        overall_percentage = round(overall_score * 100, 1)

        return ConfidenceBreakdown(
            overall_score=overall_percentage,
            model_confidence=round(model_confidence * 100, 1),
            source_agreement=round(source_agreement * 100, 1),
            source_authority=round(source_authority * 100, 1),
            recency_factor=round(recency_factor * 100, 1),
            components_explanation=self._generate_explanation(
                overall_percentage,
                len(sources),
                source_agreement
            )
        )

    def _calculate_authority_average(self, sources: list) -> float:
        """Média de autoridade das fontes."""
        if not sources:
            return 0.0
        return sum(s.authority_score for s in sources) / len(sources)

    def _calculate_recency_factor(self, sources: list) -> float:
        """
        Fontes mais recentes = maior confiança.
        Fontes sem data = score neutro.
        """
        from datetime import datetime, timedelta

        if not sources:
            return 0.5

        now = datetime.now()
        recency_scores = []

        for source in sources:
            if source.publication_date:
                days_old = (now - source.publication_date).days
                if days_old <= 30:
                    recency_scores.append(1.0)
                elif days_old <= 180:
                    recency_scores.append(0.8)
                elif days_old <= 365:
                    recency_scores.append(0.6)
                else:
                    recency_scores.append(0.4)
            else:
                recency_scores.append(0.5)  # Neutro se não tiver data

        return sum(recency_scores) / len(recency_scores)

    def _generate_explanation(
        self,
        score: float,
        source_count: int,
        agreement: float
    ) -> str:
        """Gera explicação legível do cálculo."""
        agreement_pct = round(agreement * 100)

        if score >= 80:
            return f"Alta confiança baseada em {source_count} fontes com {agreement_pct}% de concordância."
        elif score >= 50:
            return f"Confiança moderada. {source_count} fontes consultadas, algumas divergências encontradas."
        else:
            return f"Baixa confiança. Fontes divergem significativamente ou informação não pôde ser verificada."
```

### 4. Response Streamer (Streaming de Respostas)

Gerencia o streaming de respostas em tempo real.

```python
# services/response_streamer.py

import asyncio
from typing import AsyncGenerator
from pydantic import BaseModel

class StreamChunk(BaseModel):
    type: str              # "text" | "confidence" | "sources" | "done"
    content: str | dict    # Conteúdo do chunk
    timestamp: float       # Timestamp para ordenação

class ResponseStreamer:
    """
    Gerencia streaming de respostas com confiança em tempo real.
    """

    async def stream_response(
        self,
        llm_stream: AsyncGenerator,
        confidence_data: dict,
        sources: list,
    ) -> AsyncGenerator[StreamChunk, None]:
        """
        Combina streaming do LLM com metadados de confiança.
        """
        import time

        # Enviar metadados de confiança primeiro
        yield StreamChunk(
            type="confidence",
            content={
                "score": confidence_data["overall_score"],
                "level": confidence_data["level"],
                "sources_count": len(sources),
            },
            timestamp=time.time()
        )

        # Stream do texto da resposta
        async for chunk in llm_stream:
            yield StreamChunk(
                type="text",
                content=chunk,
                timestamp=time.time()
            )

        # Enviar fontes no final
        yield StreamChunk(
            type="sources",
            content={
                "sources": [
                    {
                        "title": s.title,
                        "url": s.url,
                        "snippet": s.snippet,
                        "authority": s.authority_score
                    }
                    for s in sources
                ],
                "consensus": confidence_data.get("consensus_summary", ""),
                "divergences": confidence_data.get("divergences", [])
            },
            timestamp=time.time()
        )

        # Sinalizar fim
        yield StreamChunk(
            type="done",
            content={},
            timestamp=time.time()
        )
```

---

## Data Models

### Database Schema (PostgreSQL)

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    display_name VARCHAR(100),
    avatar_url TEXT,
    auth_provider VARCHAR(50) DEFAULT 'email', -- email, google, github
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    folder_id UUID REFERENCES conversation_folders(id),
    is_shared BOOLEAN DEFAULT FALSE,
    share_slug VARCHAR(100) UNIQUE,
    message_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- user, assistant, system
    content TEXT NOT NULL,
    confidence_score DECIMAL(5,2),
    confidence_data JSONB,
    sources JSONB,
    tokens_used INTEGER,
    model_used VARCHAR(100),
    feedback_rating SMALLINT, -- -1 (down), 0 (none), 1 (up)
    feedback_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Sources Cache
CREATE TABLE sources_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_hash VARCHAR(64) NOT NULL,
    sources JSONB NOT NULL,
    consensus_score DECIMAL(5,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_sources_cache_hash ON sources_cache(query_hash);
CREATE INDEX idx_sources_cache_expires ON sources_cache(expires_at);

-- Conversation Folders
CREATE TABLE conversation_folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(7),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User Sessions
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    device_info JSONB,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Feedback Analytics
CREATE TABLE feedback_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID REFERENCES messages(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    rating SMALLINT NOT NULL,
    category VARCHAR(50), -- accuracy, helpfulness, sources
    details TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Redis Keys Structure

```
# Sessions
session:{user_id}:{session_id} -> {user_data, expires_at}

# Rate Limiting
rate:{user_id}:minute -> counter (TTL: 60s)
rate:{user_id}:hour -> counter (TTL: 3600s)

# Response Cache
cache:response:{query_hash} -> {response, confidence, sources} (TTL: 1h)

# Active Streaming
stream:{conversation_id}:{message_id} -> {status, chunks}

# User Preferences Cache
prefs:{user_id} -> {preferences_json} (TTL: 24h)
```

---

## API Design

### REST Endpoints

```yaml
# OpenAPI 3.0 Summary

/api/v1:
 # Authentication
 /auth:
  /register:
   POST: Criar conta
  /login:
   POST: Login (email/password)
  /oauth/{provider}:
   GET: OAuth redirect (google, github)
  /oauth/{provider}/callback:
   GET: OAuth callback
  /logout:
   POST: Logout
  /refresh:
   POST: Refresh token
  /forgot-password:
   POST: Solicitar reset
  /reset-password:
   POST: Reset com token

 # Conversations
 /conversations:
  GET: Listar conversas
  POST: Criar conversa
  /{id}:
   GET: Obter conversa com mensagens
   PATCH: Atualizar título/folder
   DELETE: Deletar conversa
  /{id}/export:
   GET: Exportar (markdown, pdf)
  /{id}/share:
   POST: Gerar link de compartilhamento

 # Messages
 /conversations/{id}/messages:
  GET: Listar mensagens (paginado)
  POST: Enviar mensagem (inicia streaming)

 /messages/{id}:
  GET: Obter mensagem específica
  POST: Feedback (rating)

 # User
 /user:
  /profile:
   GET: Obter perfil
   PATCH: Atualizar perfil
  /preferences:
   GET: Obter preferências
   PUT: Atualizar preferências
  /delete-account:
   DELETE: Deletar conta e dados

 # Shared
 /shared/{slug}:
  GET: Visualizar conversa compartilhada (público)
```

### WebSocket Protocol

```typescript
// WebSocket para streaming de respostas

// Cliente -> Servidor
interface ClientMessage {
	type: 'send_message' | 'stop_generation' | 'ping';
	payload: {
		conversation_id?: string;
		content?: string;
		preferences?: {
			confidence_threshold?: number;
			force_research?: boolean;
		};
	};
}

// Servidor -> Cliente
interface ServerMessage {
	type: 'chunk' | 'confidence' | 'sources' | 'error' | 'done' | 'pong';
	payload: {
		// chunk
		text?: string;

		// confidence (enviado primeiro)
		score?: number;
		level?: 'high' | 'medium' | 'low' | 'unknown';
		is_researching?: boolean;

		// sources (enviado no final)
		sources?: Source[];
		consensus?: string;
		divergences?: string[];

		// error
		code?: string;
		message?: string;
	};
	timestamp: number;
}
```

---

## Integrations

### Search Providers

```python
# integrations/search/base.py

from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class SearchProvider(ABC):
    """Interface para provedores de busca."""

    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> List[Source]:
        pass

# Implementações específicas:

class TavilyProvider(SearchProvider):
    """Tavily - otimizado para AI research."""

    async def search(self, query: str, max_results: int = 10) -> List[Source]:
        # Tavily tem ótima relevância para pesquisa técnica
        pass

class SerperProvider(SearchProvider):
    """Serper - Google Search API."""

    async def search(self, query: str, max_results: int = 10) -> List[Source]:
        # Google Search tem maior cobertura
        pass

class BraveSearchProvider(SearchProvider):
    """Brave Search - privacidade + qualidade."""

    async def search(self, query: str, max_results: int = 10) -> List[Source]:
        # Brave tem bons resultados técnicos
        pass
```

### LLM Providers

```python
# integrations/llm/router.py

class LLMRouter:
    """
    Roteador inteligente entre múltiplos LLMs.
    Escolhe o melhor modelo baseado na tarefa.
    """

    MODELS = {
        "reasoning": "claude-3-5-sonnet-20241022",  # Raciocínio complexo
        "code": "claude-3-5-sonnet-20241022",       # Código (Claude é excelente)
        "fast": "gpt-4o-mini",                      # Respostas rápidas
        "fallback": "mistral-large-latest",         # Fallback econômico
    }

    async def route(self, task_type: str, query: str):
        """Seleciona o modelo apropriado para a tarefa."""
        model = self.MODELS.get(task_type, self.MODELS["reasoning"])
        return await self._call_model(model, query)
```

---

## Security Architecture

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Email/Password                                          │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐      │
│  │ Client │───▶│  API   │───▶│ Verify │───▶│  JWT   │      │
│  │        │    │Gateway │    │Password│    │Generate│      │
│  └────────┘    └────────┘    └────────┘    └────────┘      │
│                                                             │
│  2. OAuth (Google/GitHub)                                   │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐      │
│  │ Client │───▶│ OAuth  │───▶│Provider│───▶│Callback│      │
│  │        │    │Redirect│    │ Auth   │    │+ JWT   │      │
│  └────────┘    └────────┘    └────────┘    └────────┘      │
│                                                             │
│  3. Token Refresh                                           │
│  ┌────────┐    ┌────────┐    ┌────────┐                    │
│  │Refresh │───▶│ Verify │───▶│  New   │                    │
│  │ Token  │    │ Token  │    │ Access │                    │
│  └────────┘    └────────┘    └────────┘                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Security Measures

| Medida               | Implementação                    |
| -------------------- | -------------------------------- |
| **Password Hashing** | bcrypt com cost factor 12        |
| **JWT**              | RS256, 15min access, 7d refresh  |
| **Rate Limiting**    | 60 req/min, 1000 req/hora        |
| **CORS**             | Whitelist de domínios            |
| **XSS Protection**   | CSP headers, sanitização         |
| **CSRF**             | Double submit cookie             |
| **SQL Injection**    | Prepared statements (SQLAlchemy) |
| **Input Validation** | Pydantic models                  |
| **Secrets**          | Environment variables, Vault     |

---

## Deployment Architecture

### Infrastructure Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PRODUCTION INFRASTRUCTURE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        CLOUDFLARE                                │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │   │
│  │  │   CDN   │  │   WAF   │  │  DDoS   │  │   DNS   │            │   │
│  │  │ Assets  │  │Firewall │  │ Shield  │  │ Routing │            │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                          ┌─────────┴─────────┐                         │
│                          ▼                   ▼                         │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐     │
│  │         VERCEL              │  │      RAILWAY / FLY.IO       │     │
│  │  ┌─────────────────────┐   │  │  ┌─────────────────────┐    │     │
│  │  │   Next.js Frontend  │   │  │  │   FastAPI Backend   │    │     │
│  │  │   (Edge Functions)  │   │  │  │   (Auto-scaling)    │    │     │
│  │  └─────────────────────┘   │  │  └─────────────────────┘    │     │
│  │  ┌─────────────────────┐   │  │  ┌─────────────────────┐    │     │
│  │  │   Server Components │   │  │  │   WebSocket Server  │    │     │
│  │  └─────────────────────┘   │  │  └─────────────────────┘    │     │
│  └─────────────────────────────┘  └─────────────────────────────┘     │
│                                    │                                    │
│                          ┌─────────┴─────────┐                         │
│                          ▼                   ▼                         │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐     │
│  │        DATABASES            │  │     EXTERNAL SERVICES       │     │
│  │  ┌─────────┐  ┌─────────┐  │  │  ┌─────────┐  ┌─────────┐   │     │
│  │  │ Neon    │  │ Upstash │  │  │  │ OpenAI  │  │ Tavily  │   │     │
│  │  │Postgres │  │ Redis   │  │  │  │ Claude  │  │ Serper  │   │     │
│  │  └─────────┘  └─────────┘  │  │  └─────────┘  └─────────┘   │     │
│  │  ┌─────────┐  ┌─────────┐  │  │  ┌─────────┐  ┌─────────┐   │     │
│  │  │Pinecone │  │   R2    │  │  │  │ Google  │  │ GitHub  │   │     │
│  │  │ Vector  │  │ Storage │  │  │  │  OAuth  │  │  OAuth  │   │     │
│  │  └─────────┘  └─────────┘  │  │  └─────────┘  └─────────┘   │     │
│  └─────────────────────────────┘  └─────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Environment Configuration

```yaml
# docker-compose.yml (Development)

version: '3.8'

services:
 frontend:
  build:
   context: ./frontend
   dockerfile: Dockerfile.dev
  ports:
   - '3000:3000'
  volumes:
   - ./frontend:/app
   - /app/node_modules
  environment:
   - NEXT_PUBLIC_API_URL=http://localhost:8000
   - NEXT_PUBLIC_WS_URL=ws://localhost:8000
  depends_on:
   - backend

 backend:
  build:
   context: ./backend
   dockerfile: Dockerfile.dev
  ports:
   - '8000:8000'
  volumes:
   - ./backend:/app
  environment:
   - DATABASE_URL=postgresql://dona:maria@postgres:5432/donamaria
   - REDIS_URL=redis://redis:6379
   - OPENAI_API_KEY=${OPENAI_API_KEY}
   - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
   - TAVILY_API_KEY=${TAVILY_API_KEY}
  depends_on:
   - postgres
   - redis

 postgres:
  image: postgres:16-alpine
  ports:
   - '5432:5432'
  environment:
   - POSTGRES_USER=dona
   - POSTGRES_PASSWORD=maria
   - POSTGRES_DB=donamaria
  volumes:
   - postgres_data:/var/lib/postgresql/data

 redis:
  image: redis:7-alpine
  ports:
   - '6379:6379'

volumes:
 postgres_data:
```

---

## Monitoring & Observability

### Logging Strategy

```python
# config/logging.py

import structlog
from typing import Any

def configure_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

# Uso:
log = structlog.get_logger()

async def process_query(user_id: str, query: str):
    log.info(
        "processing_query",
        user_id=user_id,
        query_length=len(query),
        query_hash=hashlib.md5(query.encode()).hexdigest()
    )
```

### Metrics

```python
# config/metrics.py

from prometheus_client import Counter, Histogram, Gauge

# Request metrics
REQUEST_COUNT = Counter(
    'donamaria_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'donamaria_request_latency_seconds',
    'Request latency',
    ['endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

# LLM metrics
LLM_TOKENS = Counter(
    'donamaria_llm_tokens_total',
    'Total LLM tokens used',
    ['model', 'type']  # type: input/output
)

LLM_LATENCY = Histogram(
    'donamaria_llm_latency_seconds',
    'LLM response latency',
    ['model']
)

# Research metrics
RESEARCH_SOURCES = Histogram(
    'donamaria_research_sources_count',
    'Sources consulted per research',
    buckets=[1, 3, 5, 8, 10, 15, 20]
)

CONFIDENCE_SCORES = Histogram(
    'donamaria_confidence_scores',
    'Distribution of confidence scores',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

# Active users
ACTIVE_USERS = Gauge(
    'donamaria_active_users',
    'Currently active users'
)
```

---

## Performance Optimizations

### Caching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    CACHING LAYERS                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  L1: Browser Cache                                          │
│  ├── Static assets (CSS, JS, images) - 1 year              │
│  └── API responses with Cache-Control headers              │
│                                                             │
│  L2: CDN (Cloudflare)                                       │
│  ├── Static pages (landing, docs) - 1 hour                 │
│  └── API responses (GET only) - 5 minutes                  │
│                                                             │
│  L3: Redis (Application Cache)                              │
│  ├── Response cache por query hash - 1 hora                │
│  ├── User sessions - 24 horas                              │
│  └── Rate limiting counters - TTL por janela               │
│                                                             │
│  L4: Database Query Cache                                   │
│  └── PostgreSQL prepared statements + connection pool      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Response Streaming Optimization

```python
# services/optimized_streamer.py

class OptimizedStreamer:
    """
    Otimizações para streaming de respostas.
    """

    CHUNK_SIZE = 10  # Tokens por chunk
    CONFIDENCE_UPDATE_INTERVAL = 5  # Segundos

    async def stream_with_prefetch(
        self,
        query: str,
        user_preferences: dict
    ) -> AsyncGenerator:
        """
        Inicia pesquisa em paralelo com geração inicial.
        """
        # Iniciar pesquisa em background
        research_task = asyncio.create_task(
            self.research_orchestrator.research(query)
        )

        # Gerar resposta inicial enquanto pesquisa
        preliminary = await self.llm.generate_preliminary(query)

        # Avaliar honestidade
        assessment = await self.honesty_engine.assess(
            query,
            preliminary,
            model_confidence=0.7  # Placeholder
        )

        # Se precisa pesquisar, aguardar
        if assessment.should_research:
            research_result = await research_task
            # Regenerar com contexto das fontes
            async for chunk in self._stream_with_sources(
                query,
                research_result
            ):
                yield chunk
        else:
            # Cancelar pesquisa desnecessária
            research_task.cancel()
            async for chunk in self._stream_direct(preliminary):
                yield chunk
```

---

## Project Structure

```
dona-maria-ia/
├── frontend/                      # Next.js App
│   ├── app/
│   │   ├── (auth)/               # Auth routes group
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   └── forgot-password/
│   │   ├── (app)/                # Main app routes
│   │   │   ├── chat/
│   │   │   │   └── [id]/
│   │   │   ├── settings/
│   │   │   └── history/
│   │   ├── shared/               # Public shared conversations
│   │   │   └── [slug]/
│   │   ├── api/                  # API routes (BFF)
│   │   ├── layout.tsx
│   │   └── page.tsx              # Landing
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatInput.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── ConfidenceBadge.tsx
│   │   │   ├── SourcesPanel.tsx
│   │   │   └── StreamingText.tsx
│   │   ├── ui/                   # Design system components
│   │   └── layout/
│   ├── lib/
│   │   ├── api.ts               # API client
│   │   ├── websocket.ts         # WS client
│   │   └── utils.ts
│   ├── stores/
│   │   ├── chat.ts              # Chat state (Zustand)
│   │   └── user.ts              # User state
│   └── styles/
│       └── globals.css
│
├── backend/                       # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── conversations.py
│   │   │   │   ├── messages.py
│   │   │   │   └── users.py
│   │   │   └── websocket.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── deps.py
│   │   ├── services/
│   │   │   ├── honesty_engine.py
│   │   │   ├── research_orchestrator.py
│   │   │   ├── confidence_calculator.py
│   │   │   ├── response_streamer.py
│   │   │   └── llm_router.py
│   │   ├── integrations/
│   │   │   ├── search/
│   │   │   │   ├── tavily.py
│   │   │   │   ├── serper.py
│   │   │   │   └── brave.py
│   │   │   └── llm/
│   │   │       ├── openai.py
│   │   │       ├── anthropic.py
│   │   │       └── openrouter.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   └── main.py
│   ├── alembic/                  # Migrations
│   ├── tests/
│   └── requirements.txt
│
├── shared/                        # Shared types/schemas
│   └── types/
│
├── docs/                          # Documentation
│
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

---

## Key Architecture Decisions (ADRs)

### ADR-001: LLM Provider Strategy

**Decisão:** Usar múltiplos provedores LLM (Claude, GPT-4, Mistral) via OpenRouter.

**Razão:**

- Redundância em caso de indisponibilidade
- Otimização de custo por tipo de tarefa
- Flexibilidade para testar novos modelos

**Consequências:**

- Complexidade adicional no routing
- Necessidade de normalizar respostas entre provedores

### ADR-002: Streaming First Architecture

**Decisão:** Toda resposta é streamed por padrão, nunca buffered.

**Razão:**

- UX crítica para chatbots (feedback imediato)
- Permite mostrar confiança antes da resposta completa
- Alinhado com estado da arte em LLM UIs

**Consequências:**

- WebSocket obrigatório para full experience
- Fallback HTTP para SSE se WS falhar

### ADR-003: Research on Demand

**Decisão:** Pesquisa externa só é ativada quando confiança < threshold.

**Razão:**

- Custo de APIs de busca ($$)
- Latência adicional (2-5s)
- Maioria das queries técnicas não precisa

**Consequências:**

- Motor de honestidade precisa ser preciso
- Usuário pode forçar pesquisa manualmente

### ADR-004: PostgreSQL + Redis Combo

**Decisão:** PostgreSQL para dados persistentes, Redis para cache/sessions.

**Razão:**

- PostgreSQL: confiabilidade, ACID, JSON support
- Redis: velocidade para cache e rate limiting
- Stack provada e escalável

**Consequências:**

- Dois sistemas para gerenciar
- Consistência eventual em alguns cenários

### ADR-005: Next.js App Router

**Decisão:** Usar Next.js 15 com App Router para o frontend.

**Razão:**

- Server Components para performance
- Streaming nativo via React 19
- DX excelente para iteração rápida

**Consequências:**

- Learning curve para Server Components
- Algumas bibliotecas ainda não compatíveis

---

## Success Metrics & Validation

### Technical KPIs

| Métrica            | Target  | Método          |
| ------------------ | ------- | --------------- |
| Time to First Byte | < 200ms | Lighthouse      |
| Streaming Start    | < 2s    | Custom timing   |
| Research Complete  | < 10s   | P95 latency     |
| Accuracy Score     | > 95%   | Manual sampling |
| Honesty Rate       | > 80%   | Flag tracking   |
| Uptime             | > 99.5% | Monitoring      |

### Business KPIs

| Métrica      | Target 3M | Target 12M |
| ------------ | --------- | ---------- |
| MAU          | 1,000     | 50,000     |
| DAU/MAU      | > 40%     | > 60%      |
| D7 Retention | > 40%     | > 50%      |
| NPS          | > 30      | > 50       |

---

## Next Steps

1. **Setup do Projeto** — Criar estrutura de pastas e configurar tooling
2. **Backend Core** — Implementar Honesty Engine e Research Orchestrator
3. **Frontend Chat** — UI de chat com streaming e confiança
4. **Integration** — Conectar provedores de busca e LLM
5. **Auth** — Sistema de autenticação completo
6. **Deploy** — CI/CD e infraestrutura de produção

---

**Documento gerado por:** Winston (Architect Agent)  
**Data:** 2026-01-15  
**Status:** ✅ Completo
