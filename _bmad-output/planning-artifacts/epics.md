---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics, step-03-create-stories, step-04-final-validation]
inputDocuments: [prd.md, architecture.md, ux-design-specification.md]
workflowType: 'epics-and-stories'
projectType: 'web_app'
domain: 'AI/LLM'
date: 2026-01-15
author: Raposo
status: complete
---

# Dona-Maria-IA - Epic Breakdown

## Overview

Este documento fornece o breakdown completo de épicos e histórias para **Dona-Maria-IA**, decompondo os requisitos do PRD, UX Design e Arquitetura em histórias implementáveis organizadas por valor do usuário.

---

## Requirements Inventory

### Functional Requirements

**User Authentication & Management:**

- FR1: Usuários podem criar conta com email ou OAuth (Google/GitHub)
- FR2: Usuários podem fazer login e logout
- FR3: Usuários podem resetar senha via email
- FR4: Usuários podem configurar preferências de conta
- FR5: Usuários podem deletar conta e dados associados

**Core Conversation:**

- FR6: Usuários podem iniciar nova conversa
- FR7: Usuários podem enviar mensagens de texto
- FR8: Usuários podem receber respostas em streaming (tempo real)
- FR9: Usuários podem visualizar histórico de conversas
- FR10: Usuários podem deletar conversas

**Honesty Engine:**

- FR11: Sistema detecta quando não possui conhecimento suficiente para responder
- FR12: Sistema expressa nível de confiança (0-100%) em cada resposta
- FR13: Sistema admite limitações explicitamente com linguagem clara
- FR14: Sistema diferencia entre "sei com certeza", "sei parcialmente" e "não sei"
- FR15: Sistema ativa pesquisa automática quando confiança está abaixo de threshold

**Multi-Source Research:**

- FR16: Sistema busca informações em tempo real na internet quando necessário
- FR17: Sistema consulta no mínimo 5 fontes diferentes por pesquisa
- FR18: Sistema agrega e sintetiza informações de múltiplas fontes
- FR19: Sistema identifica consenso e divergência entre fontes
- FR20: Sistema filtra fontes por autoridade e credibilidade

**Statistical Transparency:**

- FR21: Sistema exibe % de confiança visualmente em cada resposta
- FR22: Sistema lista todas as fontes consultadas com links
- FR23: Sistema indica quantas fontes concordam/discordam
- FR24: Sistema permite drill-down em fontes específicas
- FR25: Sistema explica metodologia de cálculo de confiança sob demanda

**Code Specialization:**

- FR26: Sistema fornece sugestões de código com sintaxe correta
- FR27: Sistema explica trade-offs e alternativas de implementação
- FR28: Sistema identifica quando código precisa de testes adicionais
- FR29: Sistema detecta potenciais bugs e edge cases
- FR30: Sistema suporta múltiplas linguagens de programação

**Feedback System:**

- FR31: Usuários podem avaliar respostas com thumbs up/down
- FR32: Usuários podem reportar respostas incorretas com detalhes
- FR33: Sistema registra feedback para melhoria contínua
- FR34: Usuários podem sugerir fontes adicionais

**Conversation Management:**

- FR35: Usuários podem organizar conversas em pastas/categorias
- FR36: Usuários podem buscar no histórico de conversas
- FR37: Usuários podem exportar conversas (Markdown, PDF)
- FR38: Usuários podem compartilhar conversas via link público

**Settings & Preferences:**

- FR39: Usuários podem configurar threshold de confiança para pesquisa automática
- FR40: Usuários podem escolher nível de detalhamento das respostas
- FR41: Usuários podem configurar linguagens de programação preferidas
- FR42: Usuários podem ativar/desativar modo desenvolvedor

### Non-Functional Requirements

**Performance:**

- NFR1: Respostas simples iniciam streaming em <2 segundos
- NFR2: Respostas com pesquisa completam em <10 segundos (P95)
- NFR3: Interface mantém 60fps durante streaming
- NFR4: Tempo de carregamento inicial <3 segundos em 3G
- NFR5: Sistema suporta 10.000 usuários concorrentes

**Security:**

- NFR6: Todas as comunicações via HTTPS/TLS 1.3
- NFR7: Senhas armazenadas com bcrypt (cost factor ≥12)
- NFR8: Tokens JWT com expiração máxima de 24 horas
- NFR9: Rate limiting de 60 requests/minuto por usuário
- NFR10: Proteção contra XSS, CSRF e SQL Injection
- NFR11: Logs de auditoria para ações sensíveis

**Scalability:**

- NFR12: Arquitetura suporta escala horizontal
- NFR13: Sistema mantém performance com 10x crescimento
- NFR14: Cache de respostas frequentes com TTL de 1 hora
- NFR15: CDN para assets estáticos

**Accessibility:**

- NFR16: Conformidade WCAG 2.1 AA
- NFR17: Suporte completo a screen readers
- NFR18: Navegação completa via teclado
- NFR19: Contraste mínimo 4.5:1 para texto
- NFR20: Tamanho mínimo de fonte 16px

**Reliability:**

- NFR21: Uptime de 99.5%
- NFR22: Recovery Time Objective (RTO) <1 hora
- NFR23: Recovery Point Objective (RPO) <15 minutos
- NFR24: Backups automáticos diários
- NFR25: Graceful degradation quando fontes externas indisponíveis

**Integration:**

- NFR26: API RESTful com documentação OpenAPI 3.0
- NFR27: Webhooks para eventos de conversa (Growth phase)
- NFR28: Suporte a SSO via SAML 2.0 (Growth phase)

### Additional Requirements

**Da Arquitetura:**

- Stack: Next.js 15 + FastAPI + Python 3.12 + LangChain
- Database: PostgreSQL + Redis + Pinecone
- Multi-LLM: Claude 3.5 (principal), GPT-4o (fallback), Mistral Large (econômico)
- Search APIs: Tavily, Serper, Brave Search
- Infra: Vercel (frontend), Railway/Fly.io (backend), Cloudflare (CDN)
- Docker Compose para desenvolvimento local

**Do UX Design:**

- Design System: Tailwind CSS + Headless UI
- Theme: #333333 (base), #aeffde (primary), #e4f1ff (secondary)
- Typography: Inter (primary), JetBrains Mono (code)
- Desktop-first, mobile-friendly
- Confidence Badge visual em cada resposta
- SourcesPanel expandível

---

## FR Coverage Map

| FR   | Epic   | Story    | Descrição                    |
| ---- | ------ | -------- | ---------------------------- |
| FR1  | Epic 1 | 1.2, 1.3 | Registro com email e OAuth   |
| FR2  | Epic 1 | 1.4      | Login e logout               |
| FR3  | Epic 1 | 1.5      | Reset de senha               |
| FR4  | Epic 6 | 6.1      | Preferências de conta        |
| FR5  | Epic 6 | 6.4      | Deletar conta                |
| FR6  | Epic 2 | 2.1      | Iniciar conversa             |
| FR7  | Epic 2 | 2.2      | Enviar mensagens             |
| FR8  | Epic 2 | 2.3      | Streaming de respostas       |
| FR9  | Epic 2 | 2.4      | Histórico de conversas       |
| FR10 | Epic 2 | 2.5      | Deletar conversas            |
| FR11 | Epic 3 | 3.1      | Detecção de incerteza        |
| FR12 | Epic 3 | 3.2      | Nível de confiança           |
| FR13 | Epic 3 | 3.3      | Admissão de limitações       |
| FR14 | Epic 3 | 3.4      | Diferenciação de certeza     |
| FR15 | Epic 3 | 3.5      | Pesquisa automática          |
| FR16 | Epic 4 | 4.1      | Busca em tempo real          |
| FR17 | Epic 4 | 4.2      | Múltiplas fontes             |
| FR18 | Epic 4 | 4.3      | Agregação de fontes          |
| FR19 | Epic 4 | 4.4      | Consenso/divergência         |
| FR20 | Epic 4 | 4.5      | Filtro por autoridade        |
| FR21 | Epic 3 | 3.2      | Exibição visual de confiança |
| FR22 | Epic 4 | 4.6      | Lista de fontes              |
| FR23 | Epic 4 | 4.4      | Indicador de concordância    |
| FR24 | Epic 4 | 4.7      | Drill-down em fontes         |
| FR25 | Epic 3 | 3.6      | Explicação de metodologia    |
| FR26 | Epic 5 | 5.1      | Código com sintaxe correta   |
| FR27 | Epic 5 | 5.2      | Trade-offs de código         |
| FR28 | Epic 5 | 5.3      | Identificação de testes      |
| FR29 | Epic 5 | 5.4      | Detecção de bugs             |
| FR30 | Epic 5 | 5.5      | Múltiplas linguagens         |
| FR31 | Epic 2 | 2.6      | Thumbs up/down               |
| FR32 | Epic 2 | 2.7      | Report de erros              |
| FR33 | Epic 2 | 2.6, 2.7 | Registro de feedback         |
| FR34 | Epic 4 | 4.8      | Sugestão de fontes           |
| FR35 | Epic 7 | 7.1      | Pastas/categorias            |
| FR36 | Epic 7 | 7.2      | Busca em histórico           |
| FR37 | Epic 7 | 7.3      | Exportar conversas           |
| FR38 | Epic 7 | 7.4      | Compartilhar conversas       |
| FR39 | Epic 6 | 6.2      | Threshold de confiança       |
| FR40 | Epic 6 | 6.2      | Nível de detalhamento        |
| FR41 | Epic 6 | 6.3      | Linguagens preferidas        |
| FR42 | Epic 6 | 6.3      | Modo desenvolvedor           |

---

## Epic List

### Epic 1: Fundação e Autenticação de Usuários

Usuários podem se registrar, fazer login e gerenciar sua identidade de forma segura, estabelecendo a base técnica do projeto.
**FRs cobertos:** FR1, FR2, FR3
**NFRs relacionados:** NFR6, NFR7, NFR8, NFR9, NFR10

### Epic 2: Chat Conversacional com IA

Usuários podem conversar com Dona Maria em tempo real, recebendo respostas em streaming e gerenciando seu histórico de conversas.
**FRs cobertos:** FR6, FR7, FR8, FR9, FR10, FR31, FR32, FR33

### Epic 3: Motor de Honestidade e Transparência

Dona Maria expressa níveis de confiança, admite limitações e decide quando precisa pesquisar — o coração do diferencial do produto.
**FRs cobertos:** FR11, FR12, FR13, FR14, FR15, FR21, FR25

### Epic 4: Pesquisa Multi-Fonte Inteligente

Sistema busca informações em múltiplas fontes, analisa consenso/divergência e apresenta resultados com transparência total.
**FRs cobertos:** FR16, FR17, FR18, FR19, FR20, FR22, FR23, FR24, FR34

### Epic 5: Especialização em Código para Desenvolvedores

Dona Maria fornece código de alta qualidade com explicações de trade-offs, detecção de bugs e suporte a múltiplas linguagens.
**FRs cobertos:** FR26, FR27, FR28, FR29, FR30

### Epic 6: Configurações e Preferências do Usuário

Usuários personalizam sua experiência com preferências de confiança, detalhamento, linguagens e podem gerenciar/deletar sua conta.
**FRs cobertos:** FR4, FR5, FR39, FR40, FR41, FR42

### Epic 7: Gestão Avançada de Conversas

Usuários organizam conversas em pastas, buscam no histórico, exportam e compartilham publicamente.
**FRs cobertos:** FR35, FR36, FR37, FR38

---

## Epic 1: Fundação e Autenticação de Usuários

**Objetivo:** Estabelecer a infraestrutura base do projeto e permitir que usuários criem contas e façam login de forma segura.

### Story 1.1: Setup Inicial do Projeto

As a **desenvolvedor**,
I want **ter o projeto configurado com a stack definida na arquitetura**,
So that **possa começar a implementar features com a estrutura correta**.

**Acceptance Criteria:**

**Given** um novo repositório vazio
**When** o setup inicial é executado
**Then** o projeto contém:

- Frontend Next.js 15 com App Router configurado
- Backend FastAPI com estrutura de pastas conforme arquitetura
- Docker Compose funcional com PostgreSQL e Redis
- Variáveis de ambiente de exemplo (.env.example)
- ESLint, Prettier e TypeScript configurados no frontend
- Ruff e MyPy configurados no backend
  **And** `docker-compose up` inicia todos os serviços sem erros
  **And** frontend acessível em localhost:3000
  **And** backend acessível em localhost:8000/docs (Swagger)

---

### Story 1.2: Registro de Usuário com Email

As a **novo usuário**,
I want **criar uma conta usando meu email e senha**,
So that **possa ter acesso personalizado à Dona Maria**.

**Acceptance Criteria:**

**Given** um visitante na página de registro
**When** ele preenche email válido e senha (mínimo 8 caracteres)
**Then** uma nova conta é criada no banco de dados
**And** a senha é armazenada com bcrypt (cost factor 12)
**And** o usuário recebe um token JWT
**And** o usuário é redirecionado para o chat

**Given** um email já registrado
**When** tentativa de registro com mesmo email
**Then** erro "Email já cadastrado" é exibido
**And** nenhuma conta duplicada é criada

**Given** senha com menos de 8 caracteres
**When** tentativa de registro
**Then** erro de validação é exibido
**And** registro não é permitido

---

### Story 1.3: Registro com OAuth (Google e GitHub)

As a **novo usuário**,
I want **criar conta usando minha conta Google ou GitHub**,
So that **possa me registrar rapidamente sem criar nova senha**.

**Acceptance Criteria:**

**Given** um visitante na página de registro
**When** ele clica em "Continuar com Google"
**Then** é redirecionado para OAuth do Google
**And** após autorização, conta é criada/vinculada
**And** recebe token JWT e é redirecionado ao chat

**Given** um visitante na página de registro
**When** ele clica em "Continuar com GitHub"
**Then** é redirecionado para OAuth do GitHub
**And** após autorização, conta é criada/vinculada
**And** recebe token JWT e é redirecionado ao chat

**Given** email do OAuth já existe como conta local
**When** login via OAuth
**Then** contas são vinculadas automaticamente
**And** usuário pode usar ambos os métodos

---

### Story 1.4: Login e Logout

As a **usuário registrado**,
I want **fazer login e logout da minha conta**,
So that **possa acessar minhas conversas de forma segura**.

**Acceptance Criteria:**

**Given** usuário com conta existente
**When** insere email e senha corretos
**Then** recebe token JWT (access + refresh)
**And** é redirecionado para o chat
**And** sessão é registrada no Redis

**Given** credenciais incorretas
**When** tentativa de login
**Then** erro "Email ou senha incorretos" é exibido
**And** nenhum token é gerado

**Given** usuário logado
**When** clica em "Sair"
**Then** tokens são invalidados
**And** sessão é removida do Redis
**And** é redirecionado para landing page

**Given** token JWT expirado
**When** refresh token ainda válido
**Then** novo access token é gerado automaticamente
**And** sessão continua sem interrupção

---

### Story 1.5: Reset de Senha via Email

As a **usuário que esqueceu a senha**,
I want **resetar minha senha via email**,
So that **possa recuperar acesso à minha conta**.

**Acceptance Criteria:**

**Given** usuário na página "Esqueci minha senha"
**When** insere email cadastrado
**Then** email com link de reset é enviado
**And** link expira em 1 hora
**And** mensagem "Verifique seu email" é exibida

**Given** link de reset válido
**When** usuário define nova senha (mínimo 8 caracteres)
**Then** senha é atualizada com bcrypt
**And** todas as sessões existentes são invalidadas
**And** usuário é redirecionado para login

**Given** link de reset expirado
**When** tentativa de uso
**Then** erro "Link expirado" é exibido
**And** opção de solicitar novo link

---

## Epic 2: Chat Conversacional com IA

**Objetivo:** Permitir que usuários conversem com Dona Maria em tempo real, com respostas em streaming e gestão completa de conversas.

### Story 2.1: Criar Nova Conversa

As a **usuário logado**,
I want **iniciar uma nova conversa com Dona Maria**,
So that **possa fazer perguntas em um contexto limpo**.

**Acceptance Criteria:**

**Given** usuário autenticado no chat
**When** clica em "Nova Conversa" ou ícone +
**Then** nova conversa é criada no banco
**And** conversa aparece na sidebar
**And** área de chat é limpa
**And** input de mensagem está focado

**Given** conversa sem título
**When** primeira mensagem é enviada
**Then** título é gerado automaticamente baseado no conteúdo
**And** título aparece na sidebar

---

### Story 2.2: Enviar Mensagens de Texto

As a **usuário em uma conversa**,
I want **enviar mensagens de texto para Dona Maria**,
So that **possa fazer perguntas e receber respostas**.

**Acceptance Criteria:**

**Given** usuário em uma conversa ativa
**When** digita mensagem e pressiona Enter (ou clica enviar)
**Then** mensagem aparece na thread como "user"
**And** input é limpo
**And** indicador de "digitando" aparece
**And** mensagem é salva no banco

**Given** mensagem vazia
**When** tentativa de envio
**Then** envio é bloqueado
**And** nenhuma requisição é feita

**Given** mensagem muito longa (>10.000 caracteres)
**When** tentativa de envio
**Then** aviso de limite é exibido
**And** mensagem é truncada ou bloqueada

---

### Story 2.3: Receber Respostas em Streaming

As a **usuário que enviou uma pergunta**,
I want **ver a resposta de Dona Maria aparecer em tempo real**,
So that **tenha feedback imediato e melhor experiência**.

**Acceptance Criteria:**

**Given** mensagem enviada pelo usuário
**When** Dona Maria começa a responder
**Then** texto aparece caractere por caractere via WebSocket
**And** cursor de digitação pisca no final
**And** interface mantém 60fps durante streaming
**And** usuário pode scrollar durante streaming

**Given** streaming em andamento
**When** usuário clica em "Parar"
**Then** geração é interrompida
**And** resposta parcial é salva
**And** indicador de "resposta parcial" é exibido

**Given** erro durante streaming
**When** conexão é perdida
**Then** fallback para SSE é tentado
**And** se falhar, erro amigável é exibido
**And** opção de "Tentar novamente"

---

### Story 2.4: Visualizar Histórico de Conversas

As a **usuário logado**,
I want **ver meu histórico de conversas anteriores**,
So that **possa retomar conversas ou revisar informações**.

**Acceptance Criteria:**

**Given** usuário autenticado
**When** acessa o chat
**Then** sidebar mostra lista de conversas ordenadas por data
**And** cada conversa mostra título e preview
**And** conversa atual está destacada

**Given** lista de conversas
**When** clica em uma conversa
**Then** mensagens daquela conversa são carregadas
**And** área de chat mostra thread completa
**And** scroll posiciona no final

**Given** muitas conversas (>50)
**When** scroll na sidebar
**Then** paginação carrega mais conversas
**And** loading indicator é exibido

---

### Story 2.5: Deletar Conversas

As a **usuário**,
I want **deletar conversas que não preciso mais**,
So that **possa manter meu histórico organizado**.

**Acceptance Criteria:**

**Given** conversa na sidebar
**When** clica no menu "..." e seleciona "Deletar"
**Then** modal de confirmação aparece
**And** ao confirmar, conversa é removida
**And** todas as mensagens são deletadas (cascade)
**And** sidebar atualiza instantaneamente

**Given** conversa deletada
**When** era a conversa ativa
**Then** usuário é redirecionado para "Nova Conversa"

---

### Story 2.6: Avaliar Respostas (Thumbs Up/Down)

As a **usuário que recebeu uma resposta**,
I want **avaliar se a resposta foi útil ou não**,
So that **Dona Maria possa melhorar com meu feedback**.

**Acceptance Criteria:**

**Given** resposta de Dona Maria exibida
**When** usuário clica em 👍
**Then** ícone fica preenchido/destacado
**And** feedback é salvo no banco (rating: 1)
**And** toast "Obrigada pelo feedback!" aparece

**Given** resposta de Dona Maria exibida
**When** usuário clica em 👎
**Then** ícone fica preenchido/destacado
**And** modal opcional para detalhes aparece
**And** feedback é salvo (rating: -1)

**Given** já avaliou uma resposta
**When** clica no ícone oposto
**Then** avaliação é atualizada
**And** ícone anterior é desmarcado

---

### Story 2.7: Reportar Resposta Incorreta

As a **usuário que identificou erro**,
I want **reportar que uma resposta está incorreta com detalhes**,
So that **Dona Maria possa corrigir e melhorar**.

**Acceptance Criteria:**

**Given** usuário clicou em 👎
**When** modal de feedback aparece
**Then** pode selecionar categoria:

- Informação incorreta
- Código não funciona
- Fontes não confiáveis
- Outro
  **And** campo de texto para detalhes
  **And** botão "Enviar Report"

**Given** report enviado
**When** salvo no banco
**Then** inclui: message_id, user_id, categoria, detalhes, timestamp
**And** toast de agradecimento aparece

---

## Epic 3: Motor de Honestidade e Transparência

**Objetivo:** Implementar o coração do diferencial de Dona Maria — expressão de confiança, admissão de limitações e decisão de quando pesquisar.

### Story 3.1: Detectar Incerteza na Resposta

As a **sistema**,
I want **detectar quando não tenho conhecimento suficiente**,
So that **possa decidir se preciso pesquisar antes de responder**.

**Acceptance Criteria:**

**Given** query do usuário recebida
**When** processada pelo Honesty Engine
**Then** sinais de incerteza são detectados:

- Frases como "acredito que", "talvez", "não tenho certeza"
- Referências a datas recentes (após cutoff)
- Pedidos de dados estatísticos específicos
- Perguntas sobre eventos/pessoas específicas

**Given** múltiplos sinais de incerteza detectados
**When** score é calculado
**Then** penalidade é aplicada por sinal (-10% cada)
**And** score final determina ação

---

### Story 3.2: Expressar Nível de Confiança Visual

As a **usuário que recebe uma resposta**,
I want **ver o nível de confiança de Dona Maria visualmente**,
So that **saiba o quanto posso confiar na informação**.

**Acceptance Criteria:**

**Given** resposta gerada com confidence_score
**When** exibida na interface
**Then** ConfidenceBadge mostra:

- Porcentagem (ex: "87%")
- Cor baseada no nível:
  - Verde (#aeffde): 80-100%
  - Amarelo (#ffd966): 50-79%
  - Vermelho (#ff8080): 0-49%
- Ícone indicativo

**Given** ConfidenceBadge exibido
**When** usuário passa o mouse (hover)
**Then** tooltip mostra breakdown:

- Confiança do modelo: X%
- Concordância de fontes: Y%
- Autoridade das fontes: Z%

---

### Story 3.3: Admitir Limitações com Linguagem Clara

As a **Dona Maria**,
I want **admitir claramente quando não sei algo**,
So that **usuários confiem em minha honestidade**.

**Acceptance Criteria:**

**Given** confidence_score < 50%
**When** resposta é gerada
**Then** inclui frases como:

- "Não tenho certeza sobre isso, deixa eu pesquisar..."
- "Meu conhecimento sobre esse tema é limitado..."
- "Essa informação pode estar desatualizada..."

**Given** pesquisa foi necessária
**When** resposta final é gerada
**Then** indica claramente:

- "Pesquisei em X fontes para te dar essa resposta"
- "As fontes divergem nesse ponto..."

---

### Story 3.4: Diferenciar Níveis de Certeza

As a **Dona Maria**,
I want **comunicar claramente meu nível de certeza**,
So that **usuários saibam como interpretar minha resposta**.

**Acceptance Criteria:**

**Given** confidence_score >= 80%
**When** resposta é gerada
**Then** linguagem indica alta certeza:

- "Posso afirmar que..."
- "Com certeza, ..."

**Given** confidence_score entre 50-79%
**When** resposta é gerada
**Then** linguagem indica certeza parcial:

- "Provavelmente..."
- "Na maioria dos casos..."
- "Segundo meu conhecimento..."

**Given** confidence_score < 50%
**When** resposta é gerada
**Then** linguagem indica incerteza:

- "Não tenho certeza, mas..."
- "Deixa eu pesquisar para confirmar..."

---

### Story 3.5: Ativar Pesquisa Automática por Threshold

As a **sistema**,
I want **pesquisar automaticamente quando confiança está baixa**,
So that **usuários recebam informações verificadas**.

**Acceptance Criteria:**

**Given** confidence_score < threshold_configurado (default: 60%)
**When** resposta preliminar é avaliada
**Then** ResearchOrchestrator é ativado
**And** usuário vê indicador "🔍 Pesquisando..."
**And** resposta final inclui dados das fontes

**Given** threshold personalizado pelo usuário
**When** confidence_score < threshold_personalizado
**Then** pesquisa é ativada respeitando preferência

**Given** pesquisa em andamento
**When** usuário envia nova mensagem
**Then** pesquisa anterior continua
**And** nova mensagem entra na fila

---

### Story 3.6: Explicar Metodologia de Confiança

As a **usuário curioso**,
I want **entender como a % de confiança é calculada**,
So that **possa confiar no sistema de transparência**.

**Acceptance Criteria:**

**Given** ConfidenceBadge exibido
**When** usuário clica em "Como isso é calculado?"
**Then** modal/popover explica:

- Pesos dos componentes (modelo: 25%, fontes: 35%, etc.)
- Como autoridade de fonte é medida
- O que significa cada nível
- Link para documentação completa

**Given** usuário pergunta "como você calcula confiança?"
**When** Dona Maria responde
**Then** explica metodologia de forma conversacional
**And** menciona transparência como princípio core

---

## Epic 4: Pesquisa Multi-Fonte Inteligente

**Objetivo:** Buscar informações em múltiplas fontes em tempo real, analisar consenso e apresentar resultados com transparência.

### Story 4.1: Buscar em Tempo Real na Internet

As a **sistema com confiança baixa**,
I want **buscar informações em tempo real**,
So that **possa fornecer dados atualizados e verificados**.

**Acceptance Criteria:**

**Given** pesquisa é necessária (confidence < threshold)
**When** ResearchOrchestrator é ativado
**Then** queries são enviadas a provedores de busca
**And** timeout de 8 segundos por provedor
**And** resultados são coletados em paralelo

**Given** provedor falha ou timeout
**When** outros provedores respondem
**Then** pesquisa continua com resultados parciais
**And** graceful degradation

---

### Story 4.2: Consultar Múltiplas Fontes (Mínimo 5)

As a **ResearchOrchestrator**,
I want **consultar pelo menos 5 fontes diferentes**,
So that **tenha visão diversificada da informação**.

**Acceptance Criteria:**

**Given** pesquisa ativada
**When** provedores retornam resultados
**Then** no mínimo 5 fontes únicas são coletadas
**And** máximo de 15 fontes para não sobrecarregar
**And** duplicatas por URL são removidas

**Given** menos de 5 fontes encontradas
**When** após todas as tentativas
**Then** prossegue com o que tem
**And** indica na resposta "poucas fontes disponíveis"

---

### Story 4.3: Agregar e Sintetizar Informações

As a **sistema com múltiplas fontes**,
I want **agregar e sintetizar as informações encontradas**,
So that **usuário receba resposta coerente e completa**.

**Acceptance Criteria:**

**Given** fontes coletadas pelo ResearchOrchestrator
**When** LLM processa os resultados
**Then** informações são sintetizadas em resposta única
**And** mantém citações inline [1][2][3]
**And** não copia texto verbatim (paráfrase)

**Given** informações contraditórias
**When** síntese é criada
**Then** ambas as posições são apresentadas
**And** divergência é explicitada

---

### Story 4.4: Identificar Consenso e Divergência

As a **ConsensusAnalyzer**,
I want **identificar quando fontes concordam ou divergem**,
So that **usuário entenda a confiabilidade da informação**.

**Acceptance Criteria:**

**Given** múltiplas fontes sobre mesmo tópico
**When** análise de consenso é executada
**Then** consensus_score é calculado (0-1)
**And** pontos de concordância são identificados
**And** divergências são listadas separadamente

**Given** alta divergência (consensus < 0.5)
**When** resposta é gerada
**Then** indica claramente:

- "As fontes divergem neste ponto"
- "X fontes dizem A, Y fontes dizem B"
- "A divergência pode ser por [razão]"

---

### Story 4.5: Filtrar Fontes por Autoridade

As a **SourceRanker**,
I want **rankear fontes por autoridade e credibilidade**,
So that **priorizemos informações mais confiáveis**.

**Acceptance Criteria:**

**Given** lista de fontes coletadas
**When** ranking é executado
**Then** cada fonte recebe authority_score (0-1) baseado em:

- Domínio (gov, edu, org vs outros)
- Reconhecimento do site (Wikipedia, MDN, etc.)
- Data de publicação (mais recente = bonus)

**Given** fontes rankeadas
**When** seleção para resposta
**Then** top 10-15 fontes por autoridade são usadas
**And** fontes de baixa autoridade são descartadas

---

### Story 4.6: Listar Fontes com Links

As a **usuário que recebe resposta com pesquisa**,
I want **ver todas as fontes consultadas com links**,
So that **possa verificar e aprofundar por conta própria**.

**Acceptance Criteria:**

**Given** resposta com pesquisa finalizada
**When** SourcesPanel é exibido
**Then** lista todas as fontes com:

- Título do artigo/página
- URL clicável (abre em nova aba)
- Snippet relevante
- Authority badge (alto/médio/baixo)

**Given** muitas fontes (>5)
**When** panel é exibido
**Then** mostra top 5 inicialmente
**And** botão "Ver todas as X fontes" expande

---

### Story 4.7: Drill-down em Fontes Específicas

As a **usuário interessado em uma fonte**,
I want **ver mais detalhes sobre uma fonte específica**,
So that **possa entender sua relevância**.

**Acceptance Criteria:**

**Given** SourcesPanel expandido
**When** usuário clica em uma fonte
**Then** card expande mostrando:

- Snippet completo citado na resposta
- Data de publicação
- Authority score com explicação
- Link para abrir original

**Given** citação inline [1] na resposta
**When** usuário clica no número
**Then** scroll até a fonte no SourcesPanel
**And** fonte é destacada visualmente

---

### Story 4.8: Sugerir Fontes Adicionais

As a **usuário**,
I want **sugerir fontes que Dona Maria deveria ter consultado**,
So that **o sistema melhore suas pesquisas futuras**.

**Acceptance Criteria:**

**Given** SourcesPanel exibido
**When** usuário clica em "Sugerir fonte"
**Then** modal com campo de URL aparece
**And** pode adicionar comentário opcional

**Given** sugestão enviada
**When** salva no banco
**Then** registra: message_id, url_sugerida, comentário
**And** toast de agradecimento
**And** (futuro) fontes sugeridas frequentemente são priorizadas

---

## Epic 5: Especialização em Código para Desenvolvedores

**Objetivo:** Fornecer sugestões de código de alta qualidade com explicações de trade-offs, detecção de bugs e suporte a múltiplas linguagens.

### Story 5.1: Fornecer Código com Sintaxe Correta

As a **desenvolvedor pedindo código**,
I want **receber código com sintaxe correta e highlighting**,
So that **possa usar ou adaptar sem erros básicos**.

**Acceptance Criteria:**

**Given** usuário pede código (detectado por intent)
**When** Dona Maria responde
**Then** código é formatado em blocos markdown
**And** linguagem é detectada e indicada
**And** syntax highlighting é aplicado (JetBrains Mono)
**And** botão de copiar em cada bloco

**Given** código gerado
**When** exibido na interface
**Then** linha numbers são mostrados
**And** indentação é preservada corretamente

---

### Story 5.2: Explicar Trade-offs de Implementação

As a **desenvolvedor avaliando opções**,
I want **entender os trade-offs das soluções sugeridas**,
So that **possa escolher a melhor abordagem pro meu caso**.

**Acceptance Criteria:**

**Given** pergunta sobre implementação
**When** Dona Maria responde com código
**Then** inclui seção "Trade-offs":

- Prós da abordagem escolhida
- Contras/limitações
- Alternativas mencionadas
- Quando usar cada opção

**Given** múltiplas formas de resolver
**When** confidence é similar entre opções
**Then** apresenta as principais alternativas
**And** deixa usuário escolher

---

### Story 5.3: Identificar Necessidade de Testes

As a **Dona Maria analisando código**,
I want **identificar quando código precisa de testes específicos**,
So that **desenvolvedores não publiquem código sem cobertura**.

**Acceptance Criteria:**

**Given** código com lógica complexa
**When** análise é feita
**Then** sugere testes específicos:

- "Esse código deveria ter testes para edge case X"
- "Recomendo testar com input Y"
- "Mock necessário para dependência Z"

**Given** código sem tratamento de erros
**When** análise é feita
**Then** aponta:

- "Falta tratamento de exceção para..."
- "Considere o caso onde input é null/undefined"

---

### Story 5.4: Detectar Potenciais Bugs e Edge Cases

As a **desenvolvedor recebendo código**,
I want **saber de potenciais bugs antes de usar**,
So that **evite problemas em produção**.

**Acceptance Criteria:**

**Given** código gerado ou analisado
**When** Dona Maria responde
**Then** seção "⚠️ Atenção" lista:

- Potenciais bugs identificados
- Edge cases não tratados
- Problemas de performance conhecidos
- Race conditions se aplicável

**Given** bug potencial identificado
**When** exibido
**Then** inclui:

- Descrição do problema
- Quando/como ocorre
- Sugestão de correção

---

### Story 5.5: Suportar Múltiplas Linguagens

As a **desenvolvedor poliglota**,
I want **receber código em Python, JavaScript, TypeScript, Go, Rust e Java**,
So that **Dona Maria seja útil independente do meu stack**.

**Acceptance Criteria:**

**Given** pergunta sobre código
**When** linguagem não é especificada
**Then** Dona Maria pergunta ou infere do contexto
**And** usa linguagem preferida do usuário (se configurada)

**Given** linguagem específica solicitada
**When** é uma das suportadas (Python, JS, TS, Go, Rust, Java)
**Then** código é gerado nessa linguagem
**And** syntax highlighting correto é aplicado

**Given** linguagem não suportada
**When** solicitada
**Then** informa que não suporta
**And** sugere alternativa similar se possível

---

## Epic 6: Configurações e Preferências do Usuário

**Objetivo:** Permitir que usuários personalizem sua experiência e gerenciem sua conta de forma completa.

### Story 6.1: Configurar Preferências de Conta

As a **usuário**,
I want **configurar minhas preferências básicas de conta**,
So that **Dona Maria se adapte ao meu estilo**.

**Acceptance Criteria:**

**Given** usuário na página de configurações
**When** acessa aba "Perfil"
**Then** pode editar:

- Nome de exibição
- Avatar (upload ou URL)
- Tema (dark/light/system)

**Given** alterações feitas
**When** clica em "Salvar"
**Then** preferências são atualizadas no banco
**And** cache do Redis é invalidado
**And** toast de confirmação

---

### Story 6.2: Configurar Threshold de Confiança

As a **usuário exigente**,
I want **configurar quando Dona Maria deve pesquisar automaticamente**,
So that **tenha controle sobre o nível de verificação**.

**Acceptance Criteria:**

**Given** usuário nas configurações
**When** acessa aba "IA"
**Then** slider de threshold de confiança:

- Range: 30% a 90%
- Default: 60%
- Preview: "Dona Maria pesquisará quando confiança < X%"

**Given** threshold alterado
**When** próxima conversa
**Then** Honesty Engine usa novo threshold
**And** comportamento reflete a preferência

**Given** aba "IA"
**When** exibida
**Then** também mostra opção de nível de detalhamento:

- Conciso (respostas curtas)
- Balanceado (default)
- Detalhado (explicações completas)

---

### Story 6.3: Configurar Linguagens de Programação

As a **desenvolvedor**,
I want **configurar minhas linguagens preferidas**,
So that **código seja gerado na linguagem que uso**.

**Acceptance Criteria:**

**Given** usuário nas configurações
**When** acessa aba "Desenvolvedor"
**Then** pode:

- Selecionar linguagem primária
- Adicionar linguagens secundárias
- Ativar/desativar "Modo Dev" (mostra mais detalhes técnicos)

**Given** linguagem primária configurada
**When** pede código sem especificar linguagem
**Then** usa linguagem primária
**And** pode perguntar se quer em outra

---

### Story 6.4: Deletar Conta e Dados

As a **usuário**,
I want **deletar minha conta e todos os dados associados**,
So that **tenha controle sobre minha privacidade**.

**Acceptance Criteria:**

**Given** usuário nas configurações
**When** clica em "Deletar minha conta"
**Then** modal de confirmação aparece
**And** explica o que será deletado
**And** pede senha para confirmar

**Given** confirmação com senha correta
**When** deleção é executada
**Then** todas as conversas são deletadas
**And** todos os feedbacks são anonimizados
**And** sessões são invalidadas
**And** conta é removida
**And** redirecionado para landing com mensagem

---

## Epic 7: Gestão Avançada de Conversas

**Objetivo:** Permitir que usuários organizem, busquem, exportem e compartilhem suas conversas.

### Story 7.1: Organizar Conversas em Pastas

As a **usuário com muitas conversas**,
I want **organizar conversas em pastas/categorias**,
So that **encontre facilmente conversas sobre temas específicos**.

**Acceptance Criteria:**

**Given** usuário na sidebar de conversas
**When** clica em "Nova pasta"
**Then** pode criar pasta com:

- Nome (obrigatório)
- Cor (opcional, seletor de cor)

**Given** conversa existente
**When** arrasta para uma pasta (ou menu > Mover)
**Then** conversa é movida para a pasta
**And** aparece dentro da pasta na sidebar

**Given** pasta com conversas
**When** clica na pasta
**Then** expande/colapsa para mostrar conversas
**And** contador mostra quantidade

---

### Story 7.2: Buscar no Histórico de Conversas

As a **usuário procurando informação antiga**,
I want **buscar no histórico de todas as minhas conversas**,
So that **encontre rapidamente o que preciso**.

**Acceptance Criteria:**

**Given** usuário na sidebar
**When** clica no ícone de busca (ou Ctrl+K)
**Then** campo de busca aparece
**And** aceita texto livre

**Given** termo de busca inserido
**When** busca é executada
**Then** resultados mostram:

- Conversas com match no título
- Conversas com match no conteúdo
- Highlight do termo encontrado
- Preview do contexto

**Given** resultado clicado
**When** conversa abre
**Then** scroll até a mensagem com o termo
**And** termo é destacado

---

### Story 7.3: Exportar Conversas

As a **usuário que quer guardar conversas**,
I want **exportar conversas em Markdown ou PDF**,
So that **tenha backup ou possa compartilhar offline**.

**Acceptance Criteria:**

**Given** conversa aberta
**When** clica menu "..." > "Exportar"
**Then** opções aparecem:

- Markdown (.md)
- PDF

**Given** Markdown selecionado
**When** export é executado
**Then** arquivo .md é gerado com:

- Título da conversa
- Data de criação
- Todas as mensagens formatadas
- Código com syntax (```lang)
- Download automático

**Given** PDF selecionado
**When** export é executado
**Then** PDF é gerado com:

- Formatação visual bonita
- Código com highlighting
- Logo Dona Maria
- Data e título

---

### Story 7.4: Compartilhar Conversas Publicamente

As a **usuário que quer mostrar uma conversa**,
I want **gerar link público para compartilhar**,
So that **outros possam ver sem precisar de conta**.

**Acceptance Criteria:**

**Given** conversa aberta
**When** clica menu "..." > "Compartilhar"
**Then** modal de compartilhamento aparece
**And** gera slug único (ex: /shared/abc123)
**And** mostra preview do link

**Given** link gerado
**When** copiado e acessado por qualquer pessoa
**Then** conversa é exibida em modo read-only
**And** sem necessidade de login
**And** branding Dona Maria visível
**And** opção de "Iniciar sua conversa"

**Given** conversa compartilhada
**When** proprietário clica em "Revogar"
**Then** link é desativado
**And** acesso retorna 404

---

## Validation Summary

### FR Coverage: ✅ 100%

Todos os 42 requisitos funcionais estão cobertos por pelo menos uma história.

### NFR Compliance

| NFR                      | Epic/Story                             | Status |
| ------------------------ | -------------------------------------- | ------ |
| NFR1-5 (Performance)     | Story 2.3, arquitetura streaming       | ✅     |
| NFR6-11 (Security)       | Story 1.2, 1.4, 6.4                    | ✅     |
| NFR12-15 (Scalability)   | Arquitetura (Redis, CDN)               | ✅     |
| NFR16-20 (Accessibility) | Todas as Stories de UI                 | ✅     |
| NFR21-25 (Reliability)   | Infra + Story 4.1 graceful degradation | ✅     |
| NFR26-28 (Integration)   | Growth phase                           | ⏳     |

### Story Count by Epic

| Epic      | Stories | FRs Cobertos           |
| --------- | ------- | ---------------------- |
| Epic 1    | 5       | FR1, FR2, FR3          |
| Epic 2    | 7       | FR6-10, FR31-33        |
| Epic 3    | 6       | FR11-15, FR21, FR25    |
| Epic 4    | 8       | FR16-20, FR22-24, FR34 |
| Epic 5    | 5       | FR26-30                |
| Epic 6    | 4       | FR4, FR5, FR39-42      |
| Epic 7    | 4       | FR35-38                |
| **Total** | **39**  | **42 FRs**             |

### Dependency Flow

```
Epic 1 (Auth) ──────┐
                    ├──▶ Epic 2 (Chat) ──┐
                    │                     │
                    │                     ├──▶ Epic 5 (Code)
                    │                     │
                    │                     └──▶ Epic 7 (Gestão)
                    │
                    ├──▶ Epic 3 (Honesty) ──▶ Epic 4 (Research)
                    │
                    └──▶ Epic 6 (Settings)
```

Cada épico é standalone e habilita épicos futuros sem depender deles.

---

**Documento gerado por:** Murat (Test Architect)  
**Data:** 2026-01-15  
**Status:** ✅ Completo e Validado
