# System-Level Test Design — Dona-Maria-IA

**Data:** 2026-01-15  
**Autor:** Raposo  
**Test Architect:** Murat (TEA Agent)  
**Status:** Draft  
**Fase:** 3 - Solutioning (Testability Review)

---

## Executive Summary

Este documento apresenta a **avaliação de testabilidade** da arquitetura do Dona-Maria-IA, identificando pontos fortes, preocupações e recomendações para garantir uma implementação testável desde o Sprint 0.

### Resumo de Testabilidade

| Critério        | Status      | Score    |
| --------------- | ----------- | -------- |
| Controllability | ✅ PASS     | 9/10     |
| Observability   | ✅ PASS     | 8/10     |
| Reliability     | ⚠️ CONCERNS | 7/10     |
| **Overall**     | **PASS**    | **8/10** |

### Riscos Arquiteturalmente Significativos

- **3** ASRs de alta prioridade (Score ≥6)
- **5** ASRs de média prioridade (Score 3-5)
- **2** ASRs de baixa prioridade (Score 1-2)

---

## Testability Assessment

### 1. Controllability (Controle de Estado) — ✅ PASS

**Definição:** Capacidade de controlar o estado do sistema para testes.

| Aspecto              | Avaliação    | Detalhes                                              |
| -------------------- | ------------ | ----------------------------------------------------- |
| API Seeding          | ✅ Excelente | FastAPI com Pydantic permite factories tipadas        |
| Database Reset       | ✅ Excelente | PostgreSQL + Docker Compose para isolamento           |
| Mock de Dependências | ✅ Bom       | Interfaces claras para SearchProvider, LLMRouter      |
| Dependency Injection | ✅ Excelente | Arquitetura orientada a interfaces                    |
| Trigger de Erros     | ⚠️ Parcial   | Precisa expor endpoints de teste para fault injection |

**Pontos Fortes:**

- ✅ Arquitetura com interfaces abstratas (`SearchProvider`, `LLMRouter`) facilita mocking
- ✅ Docker Compose configurado com PostgreSQL e Redis para testes locais
- ✅ Pydantic models garantem validação de dados de teste
- ✅ Separação clara de camadas (Client → API Gateway → Application → LLM → Data)

**Recomendações para Sprint 0:**

```python
# Criar endpoint de teste para fault injection
@app.post("/test/inject-failure")
async def inject_failure(failure_type: str, duration_seconds: int):
    """Simula falhas de LLM, Search API, ou Database."""
    pass
```

### 2. Observability (Observabilidade) — ✅ PASS

**Definição:** Capacidade de inspecionar o estado do sistema durante e após testes.

| Aspecto             | Avaliação    | Detalhes                                      |
| ------------------- | ------------ | --------------------------------------------- |
| Logging Estruturado | ✅ Excelente | structlog com JSON configurado                |
| Metrics             | ✅ Excelente | Prometheus metrics definidas                  |
| Tracing             | ⚠️ Ausente   | Não há distributed tracing definido           |
| Determinismo        | ⚠️ Parcial   | LLM responses não são deterministicas         |
| NFR Validation      | ✅ Bom       | Histogramas para latência e confidence scores |

**Pontos Fortes:**

- ✅ Metrics Prometheus definidas: `REQUEST_LATENCY`, `LLM_LATENCY`, `CONFIDENCE_SCORES`
- ✅ Logging estruturado com contexto (user_id, query_hash)
- ✅ Histogramas com buckets apropriados para SLO validation

**Preocupações:**

- ⚠️ **Distributed Tracing:** Não há OpenTelemetry ou similar para rastrear requests através de LLM providers
- ⚠️ **LLM Determinism:** Respostas de LLM são não-determinísticas por natureza

**Recomendações para Sprint 0:**

```python
# Adicionar OpenTelemetry para tracing
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

tracer = trace.get_tracer("dona-maria-ia")

async def process_query(query: str):
    with tracer.start_as_current_span("process_query") as span:
        span.set_attribute("query.length", len(query))
        # ... processing
```

### 3. Reliability (Confiabilidade de Testes) — ⚠️ CONCERNS

**Definição:** Capacidade de executar testes de forma isolada, paralela e reproduzível.

| Aspecto           | Avaliação    | Detalhes                                   |
| ----------------- | ------------ | ------------------------------------------ |
| Isolamento        | ✅ Bom       | Redis keys namespaced, PostgreSQL schemas  |
| Paralelização     | ⚠️ Parcial   | WebSocket pode ter race conditions         |
| Reprodutibilidade | ⚠️ Baixa     | LLM providers retornam respostas variáveis |
| Cleanup           | ✅ Excelente | CASCADE deletes no schema, Redis TTL       |
| Loose Coupling    | ✅ Excelente | Interfaces bem definidas                   |

**Preocupações Críticas:**

1. **LLM Non-Determinism:**

   - Respostas de Claude/GPT-4o variam entre execuções
   - Confidence scores podem flutuar para mesma query
   - **Mitigação:** Usar mocks para testes funcionais, reservar LLM real para E2E smoke tests

2. **WebSocket State:**

   - Streaming de respostas pode ter race conditions em testes paralelos
   - **Mitigação:** Usar conversation_id único por teste, implementar cleanup hooks

3. **Search API Variability:**
   - Tavily, Serper, Brave retornam resultados diferentes ao longo do tempo
   - **Mitigação:** HAR recording para testes determinísticos

**Recomendações para Sprint 0:**

```typescript
// Playwright: HAR capture para Search API mocking
test.beforeEach(async ({ page }) => {
	await page.routeFromHAR('tests/fixtures/search-api.har', {
		url: '**/api/search/**',
		update: false,
	});
});
```

---

## Architecturally Significant Requirements (ASRs)

### High-Priority (Score ≥6) — Requerem Mitigação Imediata

| ASR ID | Categoria | Requisito                                | Prob | Impact | Score | Testability Challenge                           |
| ------ | --------- | ---------------------------------------- | ---- | ------ | ----- | ----------------------------------------------- |
| ASR-01 | PERF      | NFR2: Respostas com pesquisa <10s (P95)  | 3    | 3      | **9** | Multi-provider latency é variável               |
| ASR-02 | SEC       | NFR10: Proteção XSS, CSRF, SQL Injection | 2    | 3      | **6** | Requer security test automation                 |
| ASR-03 | DATA      | FR11-15: Honesty Engine accuracy         | 2    | 3      | **6** | LLM confidence calibration é difícil de validar |

### Medium-Priority (Score 3-5) — Monitorar

| ASR ID | Categoria | Requisito                          | Prob | Impact | Score | Testability Challenge                          |
| ------ | --------- | ---------------------------------- | ---- | ------ | ----- | ---------------------------------------------- |
| ASR-04 | PERF      | NFR5: 10.000 usuários concorrentes | 2    | 2      | **4** | Load testing infrastructure needed             |
| ASR-05 | TECH      | FR16-20: Multi-source research     | 2    | 2      | **4** | External API mocking complexity                |
| ASR-06 | OPS       | NFR21: 99.5% uptime                | 2    | 2      | **4** | Chaos engineering não definido                 |
| ASR-07 | BUS       | FR21-25: Statistical transparency  | 1    | 3      | **3** | Validação de % accuracy requer golden datasets |
| ASR-08 | PERF      | NFR1: Streaming <2s                | 2    | 1      | **2** | Network variability                            |

### Low-Priority (Score 1-2) — Monitor

| ASR ID | Categoria | Requisito              | Prob | Impact | Score | Action                          |
| ------ | --------- | ---------------------- | ---- | ------ | ----- | ------------------------------- |
| ASR-09 | OPS       | NFR15: CDN para assets | 1    | 1      | **1** | Standard implementation         |
| ASR-10 | TECH      | NFR26: OpenAPI 3.0     | 1    | 1      | **1** | FastAPI generates automatically |

---

## Test Levels Strategy

Baseado na arquitetura (Web SaaS + LLM + Multi-API), recomendo a seguinte distribuição:

### Recommended Test Pyramid

```
                    ┌─────────────────┐
                    │      E2E        │ 10%
                    │   (Playwright)  │
                    ├─────────────────┤
                    │   Integration   │ 25%
                    │ (API + Service) │
               ─────┴─────────────────┴─────
                    │      Unit       │ 65%
                    │ (Vitest/Pytest) │
                    └─────────────────┘
```

### Justificativa por Nível

| Nível           | %   | Justificativa                                                         | Ferramentas                                 |
| --------------- | --- | --------------------------------------------------------------------- | ------------------------------------------- |
| **Unit**        | 65% | Honesty Engine, Confidence Calculator, Data Factories são lógica pura | Pytest (Backend), Vitest (Frontend)         |
| **Integration** | 25% | API contracts, Database operations, Service boundaries                | Pytest + TestClient, Playwright API Testing |
| **E2E**         | 10% | Critical user journeys, streaming UI, WebSocket                       | Playwright                                  |

### Test Level Selection per Component

| Component             | Unit       | Integration | E2E        | Rationale                    |
| --------------------- | ---------- | ----------- | ---------- | ---------------------------- |
| Honesty Engine        | ✅ Primary | ✅ LLM mock | -          | Pure logic + LLM integration |
| Research Orchestrator | ✅         | ✅ Primary  | -          | Multi-provider coordination  |
| Confidence Calculator | ✅ Primary | -           | -          | Pure math, no I/O            |
| Response Streamer     | ✅         | ✅ Primary  | ✅         | WebSocket behavior           |
| Auth Flow             | -          | ✅ Primary  | ✅         | Security critical            |
| Chat UI               | -          | -           | ✅ Primary | User interaction             |

---

## NFR Testing Approach

### Security (NFR6-NFR11)

| NFR                  | Test Approach                          | Tool                   | Priority |
| -------------------- | -------------------------------------- | ---------------------- | -------- |
| NFR6: HTTPS/TLS 1.3  | Certificate validation, redirect check | Playwright + curl      | P0       |
| NFR7: bcrypt cost 12 | Unit test hash verification            | Pytest                 | P0       |
| NFR8: JWT 24h expiry | Token expiration E2E                   | Playwright             | P0       |
| NFR9: Rate limiting  | Burst request test                     | k6                     | P1       |
| NFR10: XSS/CSRF/SQLi | Security scan + manual vectors         | OWASP ZAP + Playwright | P0       |
| NFR11: Audit logs    | Log assertion in tests                 | Pytest + log capture   | P1       |

**Security Test Strategy:**

```typescript
// tests/security/auth.spec.ts
test.describe('Security NFR: Authentication', () => {
	test('JWT tokens expire after 24 hours', async ({ request }) => {
		// Generate token with known timestamp
		const { token, expiresAt } = await request.post('/api/auth/login', {
			data: { email: 'test@test.com', password: 'secure123' },
		});

		// Verify expiration is within 24h
		const expirationDelta = new Date(expiresAt).getTime() - Date.now();
		expect(expirationDelta).toBeLessThanOrEqual(24 * 60 * 60 * 1000);
	});

	test('Rate limiting blocks after 60 requests/minute', async ({ request }) => {
		const requests = Array(65)
			.fill(null)
			.map(() => request.get('/api/health'));
		const results = await Promise.all(requests);
		const blocked = results.filter((r) => r.status() === 429);
		expect(blocked.length).toBeGreaterThanOrEqual(5);
	});
});
```

### Performance (NFR1-NFR5)

| NFR                    | Test Approach                  | Tool                               | SLO              |
| ---------------------- | ------------------------------ | ---------------------------------- | ---------------- |
| NFR1: Streaming <2s    | Time-to-first-byte measurement | Playwright + performance.now()     | P95 < 2000ms     |
| NFR2: Research <10s    | End-to-end with mocked search  | Playwright                         | P95 < 10000ms    |
| NFR3: 60fps streaming  | Frame rate assertion           | Playwright + requestAnimationFrame | No frame drops   |
| NFR4: Initial load <3s | Lighthouse CI                  | Lighthouse                         | Performance > 80 |
| NFR5: 10k concurrent   | Load test                      | k6                                 | Error rate < 1%  |

**Performance Test Strategy:**

```typescript
// tests/performance/response-time.spec.ts
test('NFR1: Streaming starts within 2 seconds', async ({ page }) => {
	await page.goto('/chat');

	const startTime = performance.now();

	// Send message
	await page.getByPlaceholder('Digite sua mensagem').fill('Olá, Dona Maria!');
	await page.keyboard.press('Enter');

	// Wait for first chunk
	await page.waitForSelector('[data-testid="streaming-chunk"]');

	const firstChunkTime = performance.now() - startTime;
	expect(firstChunkTime).toBeLessThan(2000);
});
```

### Reliability (NFR21-NFR25)

| NFR                         | Test Approach           | Tool                  | Validation     |
| --------------------------- | ----------------------- | --------------------- | -------------- |
| NFR21: 99.5% uptime         | Synthetic monitoring    | Checkly/Pingdom       | Monthly report |
| NFR22: RTO <1h              | Disaster recovery drill | Manual + runbook      | Quarterly      |
| NFR23: RPO <15min           | Backup restoration test | Pytest + DB restore   | Monthly        |
| NFR24: Daily backups        | Backup verification     | Cron + assertion      | Daily          |
| NFR25: Graceful degradation | Chaos engineering       | Chaos Monkey / manual | Per release    |

**Graceful Degradation Test:**

```typescript
// tests/reliability/degradation.spec.ts
test('NFR25: Shows cached response when LLM unavailable', async ({ page }) => {
	// Mock LLM to fail
	await page.route('**/api/llm/**', (route) => route.abort('failed'));

	await page.goto('/chat');
	await page.getByPlaceholder('Digite sua mensagem').fill('Olá!');
	await page.keyboard.press('Enter');

	// Should show graceful error, not crash
	await expect(page.getByText(/Serviço temporariamente indisponível/i)).toBeVisible();

	// Should not show stack trace or technical error
	await expect(page.content()).not.toContain('Error:');
});
```

### Maintainability (Observability + Code Quality)

| Aspect           | Test Approach               | Tool                   | Target               |
| ---------------- | --------------------------- | ---------------------- | -------------------- |
| Code Coverage    | Unit + Integration coverage | Coverage.py + Istanbul | >80%                 |
| Code Duplication | Static analysis             | SonarQube              | <3%                  |
| Observability    | Log/metric assertions       | Pytest + structlog     | All endpoints logged |
| Type Safety      | Static type checking        | MyPy + TypeScript      | Zero errors          |

---

## Test Environment Requirements

### Local Development

```yaml
# Ambiente completo via Docker Compose
services:
 - PostgreSQL 16 (dados)
 - Redis 7 (cache/sessions)
 - Localstack (mock S3/R2)
```

### CI/CD (GitHub Actions)

```yaml
# Matrix de testes
test:
 strategy:
  matrix:
   test-type: [unit, integration, e2e]
   browser: [chromium] # Playwright
 services:
  postgres:
   image: postgres:16-alpine
  redis:
   image: redis:7-alpine
```

### Staging

- Vercel Preview Deployments (Frontend)
- Railway Preview Environments (Backend)
- Neon Branch Databases (PostgreSQL)
- Upstash Dev Instance (Redis)

### Production-Like (Pre-release)

- Full infrastructure clone
- Real LLM providers (with budget limits)
- Synthetic traffic generation

---

## Testability Concerns

### 🔴 Blockers (Devem ser resolvidos antes de implementação)

**Nenhum blocker identificado.** A arquitetura é fundamentalmente testável.

### 🟡 Concerns (Requerem atenção durante implementação)

| ID    | Concern                               | Impact                                    | Mitigation                                                          |
| ----- | ------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------- |
| TC-01 | LLM responses são não-determinísticas | Testes de confidence podem ser flaky      | Mock LLM para testes funcionais, golden tests com ranges aceitáveis |
| TC-02 | Search APIs retornam dados variáveis  | Research orchestrator tests podem falhar  | HAR recording, mock providers para CI                               |
| TC-03 | WebSocket streaming complexity        | Race conditions em testes paralelos       | Unique conversation IDs, sequential E2E for streaming               |
| TC-04 | Multi-provider failover               | Difícil testar todos os paths de fallback | Chaos engineering, fault injection endpoints                        |

### 🟢 Strengths (Pontos positivos da arquitetura)

- ✅ Interfaces bem definidas facilitam mocking
- ✅ Docker Compose pronto para testes locais
- ✅ Logging estruturado facilita debugging de testes
- ✅ Metrics Prometheus permitem SLO assertions
- ✅ CASCADE deletes no schema facilitam cleanup

---

## Recommendations for Sprint 0

### 1. Test Framework Setup (`*framework` workflow)

```bash
# Frontend (Next.js)
pnpm add -D vitest @testing-library/react @playwright/test

# Backend (FastAPI)
pip install pytest pytest-asyncio httpx faker factory-boy
```

### 2. Test Directory Structure

```
├── frontend/
│   ├── tests/
│   │   ├── unit/           # Vitest
│   │   ├── integration/    # Vitest + MSW
│   │   └── e2e/            # Playwright
│   └── playwright.config.ts
├── backend/
│   ├── tests/
│   │   ├── unit/           # Pytest
│   │   ├── integration/    # Pytest + TestClient
│   │   └── fixtures/       # Factories
│   └── pytest.ini
└── .github/
    └── workflows/
        └── test.yml        # CI pipeline
```

### 3. CI Pipeline Setup (`*ci` workflow)

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]

jobs:
 unit:
  runs-on: ubuntu-latest
  steps:
   - uses: actions/checkout@v4
   - name: Run Unit Tests
     run: |
      pnpm test:unit
      cd backend && pytest tests/unit/

 integration:
  runs-on: ubuntu-latest
  services:
   postgres:
    image: postgres:16-alpine
    env:
     POSTGRES_PASSWORD: test
   redis:
    image: redis:7-alpine
  steps:
   - name: Run Integration Tests
     run: pytest tests/integration/

 e2e:
  runs-on: ubuntu-latest
  steps:
   - name: Run E2E Tests
     run: pnpm playwright test
```

### 4. Mock Infrastructure

```python
# backend/tests/fixtures/mock_llm.py
class MockLLMRouter:
    """Mock determinístico para testes."""

    async def route(self, task_type: str, query: str) -> str:
        # Respostas determinísticas baseadas em query hash
        responses = {
            "hello": "Olá! Sou Dona Maria. 85% confidence.",
            "default": "Resposta mock para: {query}"
        }
        return responses.get(query.lower(), responses["default"].format(query=query))
```

### 5. Data Factories

```python
# backend/tests/fixtures/factories.py
from factory import Factory, Faker, LazyAttribute
from models import User, Conversation, Message

class UserFactory(Factory):
    class Meta:
        model = User

    email = Faker('email')
    display_name = Faker('name')
    password_hash = LazyAttribute(lambda _: hash_password('test123'))

class ConversationFactory(Factory):
    class Meta:
        model = Conversation

    user = SubFactory(UserFactory)
    title = Faker('sentence')
```

---

## Quality Gate Criteria (Pre-Implementation)

### Pass Criteria (Testability Review)

- [x] Controllability ≥7/10
- [x] Observability ≥7/10
- [x] Reliability ≥6/10
- [x] No blockers identified
- [x] All high-priority ASRs have mitigation plans

### Gate Decision: ✅ **PASS**

A arquitetura do Dona-Maria-IA é **testável** e pode prosseguir para implementação com as seguintes condições:

1. **Sprint 0 deve incluir:**

   - Setup de test framework (Playwright + Pytest)
   - CI pipeline com unit/integration/E2E stages
   - Mock infrastructure para LLM e Search APIs
   - Data factories para User, Conversation, Message

2. **Concerns a monitorar:**
   - LLM non-determinism (usar mocks para testes funcionais)
   - WebSocket race conditions (unique conversation IDs)
   - Search API variability (HAR recording)

---

## Follow-on Workflows

Após aprovação do gate de implementação:

- [ ] **`*framework`** — Setup de test framework com Playwright + Pytest
- [ ] **`*ci`** — Scaffold de CI/CD pipeline com quality gates
- [ ] **`*atdd`** — Geração de testes P0 antes da implementação (per-epic)

---

## Appendix

### Knowledge Base References

- `nfr-criteria.md` — NFR validation framework
- `test-levels-framework.md` — Test level selection
- `risk-governance.md` — Risk scoring methodology
- `test-quality.md` — Test quality Definition of Done

### Related Documents

- [PRD](prd.md) — Product Requirements
- [Architecture](architecture.md) — Technical Architecture
- [Epics](epics.md) — Epic Breakdown
- [UX Design](ux-design-specification.md) — Design Specification

### Risk Category Legend

- **TECH**: Technical/Architecture (flaws, integration, scalability)
- **SEC**: Security (access controls, auth, data exposure)
- **PERF**: Performance (SLA violations, degradation, resource limits)
- **DATA**: Data Integrity (loss, corruption, inconsistency)
- **BUS**: Business Impact (UX harm, logic errors, revenue)
- **OPS**: Operations (deployment, config, monitoring)

---

**Generated by:** BMad TEA Agent — Murat, Master Test Architect  
**Workflow:** `_bmad/bmm/workflows/testarch/test-design`  
**Version:** 4.0 (BMad v6)
