---
stepsCompleted: [step-01-init, step-02-discovery, step-03-success, step-04-journeys, step-05-domain, step-06-innovation, step-07-project-type, step-08-scoping, step-09-functional, step-10-nonfunctional, step-11-polish, step-12-complete]
inputDocuments: [product-brief-Dona-Maria-IA-2026-01-15.md]
workflowType: 'prd'
projectType: 'web_app'
domain: 'scientific'
domainComplexity: 'medium'
date: 2026-01-15
author: Raposo
status: complete
---

# Product Requirements Document - Dona-Maria-IA

**Author:** Raposo  
**Date:** 2026-01-15  
**Version:** 1.0.0

---

## Executive Summary

### Visão do Produto

**Dona-Maria-IA** é um Large Language Model (LLM) construído do zero com um princípio revolucionário: **honestidade radical**. Enquanto IAs atuais "alucinam" informações e apresentam incertezas como fatos, Dona Maria quebra esse paradigma ao admitir quando não sabe, pesquisar ativamente na internet e apresentar grau de confiança estatística em suas respostas.

### Diferencial Único

O nome homenageia a clássica figura brasileira da "Dona Maria" — a senhora que sabe de tudo sobre todos. Nossa IA busca saber de tudo, mas com uma diferença crucial: **ela só conta o que é verdade**.

### Problema Central

IAs generativas atuais sofrem de um problema crítico de confiabilidade:

- Inventam informações (alucinações)
- Apresentam respostas incorretas com a mesma confiança de fatos verificados
- Usuários não conseguem distinguir verdade de invenção

### Proposta de Valor

| Pilar                            | Descrição                                                            |
| -------------------------------- | -------------------------------------------------------------------- |
| 🎯 **Honestidade Radical**       | Admite quando não sabe e vai pesquisar                               |
| 🔍 **Pesquisa Multi-Fonte**      | Consulta múltiplos artigos na internet                               |
| 📊 **Transparência Estatística** | Apresenta % de confiança (ex: "87% de certeza baseado em 12 fontes") |
| 💻 **Especialização em Código**  | Sugestões de alta qualidade para desenvolvedores                     |

### Público-Alvo

- **Primário:** Desenvolvedores céticos que precisam de código confiável
- **Secundário:** Pesquisadores e profissionais que precisam de fatos verificáveis

---

## Success Criteria

### User Success

| Métrica            | Target                             | Método de Medição                 |
| ------------------ | ---------------------------------- | --------------------------------- |
| Taxa de Confiança  | >85% confiam nas respostas         | Survey NPS + feedback qualitativo |
| Tempo Economizado  | -50% tempo verificando informações | Comparação antes/depois           |
| Precisão Percebida | >90% respostas consideradas úteis  | Thumbs up/down em respostas       |
| Adoção Diária      | >60% DAU/MAU ratio                 | Analytics de uso                  |

### Business Success

**3 Meses:**

- 1.000 usuários beta ativos
- Taxa de retenção D7 >40%
- Feedback qualitativo validando proposta de valor

**12 Meses:**

- 50.000 usuários ativos
- Modelo de monetização validado (API/Pro tier)
- Reconhecimento como "a IA honesta" no mercado

**Longo Prazo:**

- Referência em IA transparente e confiável
- Comunidade ativa de devs contribuindo
- Expansão para mercados internacionais

### Technical Success

| KPI            | Definição                                         | Target       |
| -------------- | ------------------------------------------------- | ------------ |
| Accuracy Score | % respostas verificadas como corretas             | >95%         |
| Honesty Rate   | % de vezes que admite incerteza quando apropriado | >80%         |
| Source Quality | Média de fontes consultadas por resposta          | >5 fontes    |
| Code Quality   | % de código sugerido que funciona sem bugs        | >90%         |
| Response Time  | Tempo médio de resposta (com pesquisa)            | <10 segundos |

### Measurable Outcomes

1. **Momento "Aha!":** Usuário recebe resposta com % de confiança e fontes pela primeira vez
2. **Valor Percebido:** Usuário economiza tempo de verificação manual
3. **Lealdade:** Usuário recomenda para colegas: "É a única IA que eu confio"
4. **Diferenciação:** Dona Maria diz "Não tenho certeza, deixa eu pesquisar..." — algo que nenhuma IA concorrente faz

---

## Product Scope

### MVP (Must Have)

| Feature                   | Descrição                                                           |
| ------------------------- | ------------------------------------------------------------------- |
| Motor de Honestidade      | Detecta incerteza, expressa níveis de confiança, admite limitações  |
| Pesquisa Multi-Fonte      | Busca em tempo real, consulta múltiplos artigos, agrega informações |
| Transparência Estatística | Mostra % confiança, lista fontes, indica consenso/divergência       |
| Especialização em Código  | Alta precisão, explica trade-offs, indica necessidade de testes     |
| Interface Conversacional  | Chat intuitivo, histórico, feedback (thumbs up/down)                |

### Growth (Post-MVP)

- API pública para desenvolvedores
- Plugin VS Code
- Modo Expert (profundidade configurável por domínio)
- Memória de longo prazo

### Vision (6-12 meses)

- Colaboração em times
- Marketplace de especialistas
- Multilíngue

### Out of Scope (MVP)

| Feature                 | Razão                          |
| ----------------------- | ------------------------------ |
| API pública             | Foco em validar UX primeiro    |
| Plugins/Integrações IDE | Complexidade técnica alta      |
| Múltiplos idiomas       | Foco em PT-BR primeiro         |
| Fine-tuning por usuário | Requer base maior              |
| Mobile app              | Web-first para iteração rápida |
| Modo offline            | Pesquisa em tempo real é core  |

---

## User Journeys

### Journey 1: Carlos, o Dev Duvidoso — Código Confiável

**Persona:** Carlos, 28 anos, Desenvolvedor Full-Stack em startup

**Cena de Abertura:**
Carlos está debugando há 2 horas um bug que o ChatGPT "garantiu" que não existia. Ele copiou o código da IA confiando cegamente, e agora está frustrado. "Nunca mais", ele pensa.

**Ação Crescente:**
Carlos ouve de um colega sobre Dona Maria: "Essa IA admite quando não sabe". Cético, ele decide testar com uma pergunta sobre otimização de queries PostgreSQL.

**Clímax:**
Dona Maria responde: _"Tenho 73% de certeza sobre essa abordagem, baseado em 8 artigos. Os artigos divergem sobre o uso de índices parciais nesse caso. Quer que eu aprofunde nas fontes que discordam?"_

Carlos fica impressionado — pela primeira vez uma IA mostrou transparência.

**Resolução:**
Carlos adota Dona Maria como ferramenta principal. Ele economiza 30min/dia que gastava verificando código de outras IAs. Recomenda para todo o time.

**Capabilities Revealed:**

- Detecção de incerteza em código
- Pesquisa de artigos técnicos
- Apresentação de divergências entre fontes
- Aprofundamento sob demanda

---

### Journey 2: Marina, a Pesquisadora Paranoica — Fatos Verificáveis

**Persona:** Marina, 35 anos, Analista de Dados

**Cena de Abertura:**
Marina está preparando uma apresentação para diretoria. Na última vez, usou dados que o ChatGPT "inventou" e passou vergonha quando questionaram as fontes. Agora ela verifica TUDO em 3-4 fontes, perdendo horas.

**Ação Crescente:**
Marina descobre Dona Maria pelo Twitter: "Uma IA que mostra as fontes?". Ela testa com uma pergunta sobre tendências de mercado em SaaS B2B.

**Clímax:**
Dona Maria responde: _"Consultei 12 artigos. 9 concordam que o mercado cresceu 23% em 2025, 3 indicam crescimento de 18-20%. Aqui estão as fontes para cada posição. A divergência parece ser metodológica."_

Marina vê que as fontes são de Gartner, McKinsey e outros consultores respeitados.

**Resolução:**
Marina usa Dona Maria para preparar apresentações. Quando questionada sobre dados, ela pode mostrar as fontes em segundos. Sua credibilidade aumenta.

**Capabilities Revealed:**

- Agregação multi-fonte
- Identificação de consenso/divergência
- Citação de fontes verificáveis
- Explicação de divergências

---

### Journey 3: Tech Lead Avaliando Ferramenta para Time

**Persona:** Rafael, 42 anos, Tech Lead de empresa com 15 devs

**Cena de Abertura:**
Rafael está preocupado com a qualidade do código que seu time produz usando IAs. Bugs sutis estão passando pelo code review porque os devs confiam demais nas sugestões de IA.

**Ação Crescente:**
Rafael ouve sobre Dona Maria em um podcast de tecnologia. A proposta de "IA honesta" ressoa com seus problemas.

**Clímax:**
Rafael testa Dona Maria com uma pergunta sobre arquitetura de microsserviços. A resposta inclui: _"Essa abordagem funciona em 85% dos casos documentados, mas identifiquei 3 cenários onde pode falhar. Quer que eu detalhe os edge cases?"_

**Resolução:**
Rafael implementa Dona Maria como ferramenta oficial do time. A quantidade de bugs relacionados a sugestões de IA cai 60%. O time desenvolve o hábito de verificar os níveis de confiança.

**Capabilities Revealed:**

- Identificação de edge cases
- Análise de cenários de falha
- Suporte a decisões arquiteturais
- Integração em workflow de time

---

### Journey 4: Estudante Aprendendo a Programar

**Persona:** Juliana, 22 anos, estudante de Ciência da Computação

**Cena de Abertura:**
Juliana está aprendendo Python sozinha. Ela usa ChatGPT mas não tem experiência para saber quando a IA está errada. Já perdeu horas debugando código que "deveria funcionar".

**Ação Crescente:**
Um professor menciona Dona Maria como ferramenta mais segura para estudantes porque mostra níveis de confiança.

**Clímax:**
Juliana pergunta sobre recursão. Dona Maria responde com o código e adiciona: _"Essa implementação funciona, mas com 100% de certeza posso dizer que vai falhar para listas muito grandes por stack overflow. Quer que eu mostre uma versão iterativa mais segura?"_

**Resolução:**
Juliana passa a confiar em Dona Maria para aprender. Quando vê baixos níveis de confiança, ela pesquisa mais. Isso a torna uma programadora mais crítica.

**Capabilities Revealed:**

- Identificação de limitações em código
- Sugestão de alternativas
- Educação sobre trade-offs
- Formação de pensamento crítico

---

### Journey Requirements Summary

| Journey      | Capabilities Essenciais                                       |
| ------------ | ------------------------------------------------------------- |
| Dev Duvidoso | Motor de honestidade, pesquisa técnica, divergência de fontes |
| Pesquisadora | Agregação multi-fonte, citações, identificação de consenso    |
| Tech Lead    | Edge cases, cenários de falha, suporte a decisões             |
| Estudante    | Limitações de código, alternativas, educação sobre trade-offs |

---

## Domain Requirements

### Classificação de Domínio

- **Domínio:** Scientific/AI
- **Complexidade:** Média
- **Tipo de Projeto:** Web App (SaaS)

### Requisitos de Domínio Científico/IA

| Área              | Requisito                                                                  |
| ----------------- | -------------------------------------------------------------------------- |
| Reprodutibilidade | Mesma query deve retornar resultados consistentes (±5% variação aceitável) |
| Validação         | Metodologia de cálculo de confiança deve ser documentada e validável       |
| Transparência     | Fontes devem ser rastreáveis e verificáveis                                |
| Viés              | Sistema deve detectar e reportar potencial viés nas fontes                 |

### Considerações Éticas de IA

1. **Transparência Algorítmica:** Explicar como o % de confiança é calculado
2. **Prevenção de Desinformação:** Não apresentar informações não verificadas como fatos
3. **Viés de Fonte:** Diversificar fontes para evitar echo chambers
4. **Privacidade:** Não armazenar queries sensíveis do usuário sem consentimento

---

## Innovation Analysis

### Análise Competitiva

| Concorrente     | Limitação                            | Diferencial Dona Maria             |
| --------------- | ------------------------------------ | ---------------------------------- |
| ChatGPT/Claude  | Alucinam, não admitem incerteza      | Honestidade radical                |
| Perplexity AI   | Pesquisa, mas pode enviesar          | Transparência estatística          |
| Modelos RAG     | Dependem da qualidade da base        | Pesquisa multi-fonte em tempo real |
| Todos os atuais | Nenhum usa probabilidade estatística | % de confiança baseado em fontes   |

### Inovações Técnicas

1. **Motor de Detecção de Incerteza**

   - Análise semântica para identificar quando o modelo está "chutando"
   - Threshold de confiança para ativar pesquisa automática

2. **Agregador de Consenso Multi-Fonte**

   - Algoritmo de ponderação de fontes por autoridade
   - Detecção de divergências e padrões de consenso

3. **Interface de Transparência**
   - Visualização de % de confiança
   - Drill-down em fontes específicas
   - Comparação de posições divergentes

---

## Project-Type Requirements

### Web App (SaaS) Requirements

| Área            | Requisito                                         |
| --------------- | ------------------------------------------------- |
| Browser Support | Chrome, Firefox, Safari, Edge (últimas 2 versões) |
| Responsive      | Desktop-first, mobile-friendly                    |
| SEO             | Landing page otimizada para discovery             |
| Real-time       | Streaming de respostas durante geração            |
| Acessibilidade  | WCAG 2.1 AA compliance                            |

### SPA Architecture Requirements

- Single Page Application com routing client-side
- Server-Side Rendering (SSR) para landing page
- Progressive enhancement para features avançadas
- Offline graceful degradation (mostrar último estado)

---

## Functional Requirements

### User Authentication & Management

- FR1: Usuários podem criar conta com email ou OAuth (Google/GitHub)
- FR2: Usuários podem fazer login e logout
- FR3: Usuários podem resetar senha via email
- FR4: Usuários podem configurar preferências de conta
- FR5: Usuários podem deletar conta e dados associados

### Core Conversation

- FR6: Usuários podem iniciar nova conversa
- FR7: Usuários podem enviar mensagens de texto
- FR8: Usuários podem receber respostas em streaming (tempo real)
- FR9: Usuários podem visualizar histórico de conversas
- FR10: Usuários podem deletar conversas

### Honesty Engine

- FR11: Sistema detecta quando não possui conhecimento suficiente para responder
- FR12: Sistema expressa nível de confiança (0-100%) em cada resposta
- FR13: Sistema admite limitações explicitamente com linguagem clara
- FR14: Sistema diferencia entre "sei com certeza", "sei parcialmente" e "não sei"
- FR15: Sistema ativa pesquisa automática quando confiança está abaixo de threshold configurável

### Multi-Source Research

- FR16: Sistema busca informações em tempo real na internet quando necessário
- FR17: Sistema consulta no mínimo 5 fontes diferentes por pesquisa
- FR18: Sistema agrega e sintetiza informações de múltiplas fontes
- FR19: Sistema identifica consenso e divergência entre fontes
- FR20: Sistema filtra fontes por autoridade e credibilidade

### Statistical Transparency

- FR21: Sistema exibe % de confiança visualmente em cada resposta
- FR22: Sistema lista todas as fontes consultadas com links
- FR23: Sistema indica quantas fontes concordam/discordam
- FR24: Sistema permite drill-down em fontes específicas
- FR25: Sistema explica metodologia de cálculo de confiança sob demanda

### Code Specialization

- FR26: Sistema fornece sugestões de código com sintaxe correta
- FR27: Sistema explica trade-offs e alternativas de implementação
- FR28: Sistema identifica quando código precisa de testes adicionais
- FR29: Sistema detecta potenciais bugs e edge cases
- FR30: Sistema suporta múltiplas linguagens de programação (Python, JavaScript, TypeScript, Go, Rust, Java)

### Feedback System

- FR31: Usuários podem avaliar respostas com thumbs up/down
- FR32: Usuários podem reportar respostas incorretas com detalhes
- FR33: Sistema registra feedback para melhoria contínua
- FR34: Usuários podem sugerir fontes adicionais

### Conversation Management

- FR35: Usuários podem organizar conversas em pastas/categorias
- FR36: Usuários podem buscar no histórico de conversas
- FR37: Usuários podem exportar conversas (Markdown, PDF)
- FR38: Usuários podem compartilhar conversas via link público

### Settings & Preferences

- FR39: Usuários podem configurar threshold de confiança para pesquisa automática
- FR40: Usuários podem escolher nível de detalhamento das respostas
- FR41: Usuários podem configurar linguagens de programação preferidas
- FR42: Usuários podem ativar/desativar modo desenvolvedor

---

## Non-Functional Requirements

### Performance

| Requisito | Especificação                                                         |
| --------- | --------------------------------------------------------------------- |
| NFR1      | Respostas simples (sem pesquisa) iniciam streaming em <2 segundos     |
| NFR2      | Respostas com pesquisa completam em <10 segundos para 95th percentile |
| NFR3      | Interface mantém 60fps durante streaming de respostas                 |
| NFR4      | Tempo de carregamento inicial <3 segundos em conexão 3G               |
| NFR5      | Sistema suporta 10.000 usuários concorrentes sem degradação           |

### Security

| Requisito | Especificação                                   |
| --------- | ----------------------------------------------- |
| NFR6      | Todas as comunicações via HTTPS/TLS 1.3         |
| NFR7      | Senhas armazenadas com bcrypt (cost factor ≥12) |
| NFR8      | Tokens JWT com expiração máxima de 24 horas     |
| NFR9      | Rate limiting de 60 requests/minuto por usuário |
| NFR10     | Proteção contra XSS, CSRF e SQL Injection       |
| NFR11     | Logs de auditoria para ações sensíveis          |

### Scalability

| Requisito | Especificação                                              |
| --------- | ---------------------------------------------------------- |
| NFR12     | Arquitetura suporta escala horizontal                      |
| NFR13     | Sistema mantém performance com 10x crescimento de usuários |
| NFR14     | Cache de respostas frequentes com TTL de 1 hora            |
| NFR15     | CDN para assets estáticos                                  |

### Accessibility

| Requisito | Especificação                     |
| --------- | --------------------------------- |
| NFR16     | Conformidade WCAG 2.1 AA          |
| NFR17     | Suporte completo a screen readers |
| NFR18     | Navegação completa via teclado    |
| NFR19     | Contraste mínimo 4.5:1 para texto |
| NFR20     | Tamanho mínimo de fonte 16px      |

### Reliability

| Requisito | Especificação                                             |
| --------- | --------------------------------------------------------- |
| NFR21     | Uptime de 99.5% (excluindo manutenção programada)         |
| NFR22     | Recovery Time Objective (RTO) <1 hora                     |
| NFR23     | Recovery Point Objective (RPO) <15 minutos                |
| NFR24     | Backups automáticos diários                               |
| NFR25     | Graceful degradation quando fontes externas indisponíveis |

### Integration

| Requisito | Especificação                                              |
| --------- | ---------------------------------------------------------- |
| NFR26     | API RESTful com documentação OpenAPI 3.0                   |
| NFR27     | Webhooks para eventos de conversa (opcional, Growth phase) |
| NFR28     | Suporte a SSO via SAML 2.0 (Growth phase)                  |

---

## Technical Constraints

### Stack Recomendado (Não Prescritivo)

| Camada   | Tecnologia Sugerida           |
| -------- | ----------------------------- |
| Frontend | Next.js 14+ (App Router)      |
| Backend  | Python (FastAPI) ou Node.js   |
| LLM      | Modelo próprio ou fine-tuned  |
| Search   | Integration com APIs de busca |
| Database | PostgreSQL + Redis (cache)    |
| Hosting  | Vercel/AWS/GCP                |

### Constraints Técnicos

1. **Latência de Busca:** APIs de pesquisa adicionam 2-5s de latência
2. **Custos de API:** Cada pesquisa consome recursos de APIs externas
3. **Rate Limits:** Fontes externas têm limites de requisições
4. **Qualidade de Fonte:** Nem todas as fontes são igualmente confiáveis

---

## MVP Success Criteria

### Gates para Lançamento

- [ ] 500+ usuários beta com feedback positivo
- [ ] > 90% das respostas verificáveis estão corretas
- [ ] Usuários reportam economia de tempo vs outras IAs
- [ ] Taxa de "Dona Maria admitiu não saber" >10% (prova que funciona)
- [ ] Tempo de resposta <15 segundos mesmo com pesquisa
- [ ] Zero vulnerabilidades críticas de segurança
- [ ] WCAG 2.1 AA compliance verificado

---

## Appendix

### Documento Gerado Por

- **Workflow:** BMAD PRD Creation
- **Data:** 2026-01-15
- **Autor:** Raposo
- **Agente:** John (Product Manager)

### Referências

- [Product Brief - Dona-Maria-IA](product-brief-Dona-Maria-IA-2026-01-15.md)

### Próximos Passos Recomendados

1. **UX Design** — Criar wireframes e fluxos de usuário baseados nas User Journeys
2. **Arquitetura Técnica** — Definir stack e infraestrutura baseado nos FRs e NFRs
3. **Epics & Stories** — Quebrar FRs em épicos e histórias implementáveis

### Rastreabilidade

| Seção PRD                     | Alimenta               |
| ----------------------------- | ---------------------- |
| User Journeys →               | UX Flows               |
| Functional Requirements →     | Architecture + Epics   |
| Non-Functional Requirements → | Architecture Decisions |
| Success Criteria →            | Acceptance Tests       |

---

**FIM DO DOCUMENTO**
