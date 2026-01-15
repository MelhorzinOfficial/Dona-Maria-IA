---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments: []
date: 2026-01-15
author: Raposo
status: complete
---

# Product Brief: Dona-Maria-IA

<!-- Content will be appended sequentially through collaborative workflow steps -->

## Executive Summary

**Dona-Maria-IA** é um modelo de linguagem revolucionário construído do zero com um princípio fundamental: **honestidade radical**. Em um cenário onde IAs frequentemente "alucinam" informações e tentam parecer certas mesmo quando erradas, Dona Maria quebra esse paradigma ao admitir incerteza, pesquisar ativamente na internet quando não sabe uma resposta, e usar probabilidade estatística para se aproximar ao máximo da verdade.

O nome é uma homenagem bem-humorada à clássica figura brasileira da "Dona Maria" — a senhora que fica na porta de casa e sabe de tudo sobre todos. Assim como ela, nossa IA busca saber de tudo, mas com uma diferença crucial: **ela só conta o que é verdade**.

---

## Core Vision

### Problem Statement

As IAs generativas atuais sofrem de um problema crítico de confiabilidade: elas **inventam informações** (alucinações) e apresentam respostas incorretas com a mesma confiança de fatos verificados. Isso cria uma crise de confiança onde usuários não sabem quando podem acreditar na IA.

### Problem Impact

- **Desinformação**: Usuários tomam decisões baseadas em informações fabricadas
- **Perda de produtividade**: Desenvolvedores perdem horas debugando código sugerido por IAs que "pareciam certas"
- **Erosão da confiança**: Profissionais abandonam ferramentas de IA por não poderem confiar nelas
- **Riscos legais/éticos**: Informações falsas apresentadas como fatos podem ter consequências sérias

### Why Existing Solutions Fall Short

| Solução Atual         | Limitação                                        |
| --------------------- | ------------------------------------------------ |
| ChatGPT, Claude, etc. | Alucinam e apresentam incerteza como certeza     |
| Perplexity AI         | Pesquisa, mas ainda pode enviesar resultados     |
| Modelos com RAG       | Dependem da qualidade da base de dados           |
| Nenhum modelo atual   | Usa probabilidade estatística para transparência |

### Proposed Solution

**Dona-Maria-IA** é um LLM construído do zero com três pilares:

1. **Honestidade Radical**: Quando não sabe, diz "não sei" e vai pesquisar
2. **Pesquisa Ativa**: Consulta múltiplos artigos na internet para fundamentar respostas
3. **Probabilidade Estatística**: Apresenta grau de confiança nas respostas (ex: "87% de certeza baseado em 12 fontes")

Além disso, possui expertise especializada em **código e desenvolvimento**, oferecendo sugestões de alta qualidade para devs.

### Key Differentiators

- 🎯 **99.9% verdade** como meta (porque 100% não existe)
- 🔍 **Pesquisa multi-fonte** em tempo real
- 📊 **Transparência estatística** sobre confiabilidade das respostas
- 💻 **Especialização em código** para desenvolvedores
- 🇧🇷 **DNA brasileiro** — construída com a filosofia de "falar a verdade doa a quem doer"

---

## Target Users

### Primary Users

#### 👨‍💻 "Dev Duvidoso" — O Desenvolvedor Cético

**Nome:** Carlos, 28 anos, Desenvolvedor Full-Stack

**Contexto:** Carlos trabalha em uma startup e usa IA diariamente para codar. Já foi queimado várias vezes por código sugerido por ChatGPT que parecia perfeito mas tinha bugs sutis. Agora ele copia código da IA e gasta mais 30 minutos verificando tudo.

**Frustração Atual:**

- "Não confio mais no que a IA me diz, mas também não tenho tempo de verificar tudo"
- Perdeu uma tarde inteira debugando um código que a IA jurou que funcionava

**O que ele quer:** Uma IA que diga "não tenho certeza disso, deixa eu verificar" em vez de inventar

**Momento "Aha!":** Quando Dona Maria responde: _"Tenho 73% de certeza baseado em 8 fontes. Quer que eu aprofunde?"_

---

#### 🔍 "Pesquisador Paranoico" — O Profissional que Precisa de Fatos

**Nome:** Marina, 35 anos, Analista de Dados / Jornalista / Pesquisadora

**Contexto:** Marina precisa de informações precisas para tomar decisões ou publicar conteúdo. Já passou vergonha usando dados "inventados" por IA em uma apresentação.

**Frustração Atual:**

- "A IA me dá respostas com tanta confiança que eu acreditei. Nunca mais."
- Agora ela verifica TUDO em 3-4 fontes, perdendo horas

**O que ela quer:** Uma IA que já faça essa verificação por ela e mostre as fontes

**Momento "Aha!":** Quando Dona Maria diz: _"Consultei 12 artigos. 9 concordam com X, 3 dizem Y. Aqui estão as fontes."_

---

### Secondary Users

#### 🏢 CTOs e Tech Leads

Líderes técnicos buscando uma IA confiável para suas equipes de desenvolvimento, que não introduza bugs ou informações falsas no código-base.

#### 📚 Estudantes e Autodidatas

Pessoas aprendendo programação ou pesquisando assuntos, que precisam de informações corretas sem ter experiência para identificar erros.

---

### User Journey

| Fase                   | Experiência                                                                                         |
| ---------------------- | --------------------------------------------------------------------------------------------------- |
| **Descoberta**         | Dev frustrado vê no Twitter/Reddit: "Essa IA admite quando não sabe e pesquisa antes de responder"  |
| **Primeira Impressão** | Faz uma pergunta técnica. Dona Maria responde com % de confiança e fontes. Dev fica impressionado.  |
| **Core Usage**         | Usa diariamente para código e pesquisa. Confia nas respostas porque vê a transparência estatística. |
| **Momento Aha!**       | Dona Maria diz "Não tenho certeza, deixa eu pesquisar..." e volta com resposta fundamentada         |
| **Longo Prazo**        | Se torna ferramenta principal. Recomenda para colegas. "É a única IA que eu confio"                 |

---

## Success Metrics

### User Success Metrics

| Métrica                | Target                                  | Como Medir                          |
| ---------------------- | --------------------------------------- | ----------------------------------- |
| **Taxa de Confiança**  | >85% dos usuários confiam nas respostas | Survey NPS + feedback qualitativo   |
| **Tempo Economizado**  | -50% tempo verificando informações      | Comparação antes/depois por usuário |
| **Precisão Percebida** | >90% de respostas consideradas úteis    | Thumbs up/down em respostas         |
| **Adoção Diária**      | >60% DAU/MAU ratio                      | Analytics de uso                    |

### Business Objectives

**3 Meses:**

- 1.000 usuários beta ativos
- Taxa de retenção D7 > 40%
- Feedback qualitativo validando proposta de valor

**12 Meses:**

- 50.000 usuários ativos
- Modelo de monetização validado (API/Pro tier)
- Reconhecimento como "a IA honesta" no mercado

**Longo Prazo:**

- Referência em IA transparente e confiável
- Comunidade ativa de devs contribuindo
- Expansão para mercados internacionais

### Key Performance Indicators

| KPI                | Definição                                         | Target       |
| ------------------ | ------------------------------------------------- | ------------ |
| **Accuracy Score** | % de respostas verificadas como corretas          | >95%         |
| **Honesty Rate**   | % de vezes que admite incerteza quando apropriado | >80%         |
| **Source Quality** | Média de fontes consultadas por resposta          | >5 fontes    |
| **User Retention** | Usuários que voltam em 7 dias                     | >40%         |
| **Code Quality**   | % de código sugerido que funciona sem bugs        | >90%         |
| **Response Time**  | Tempo médio de resposta (com pesquisa)            | <10 segundos |

---

## MVP Scope

### Core Features

#### 🎯 Must Have (MVP)

1. **Motor de Honestidade**

   - Detecta quando não sabe uma resposta
   - Expressa níveis de confiança (ex: "75% certeza")
   - Admite limitações explicitamente

2. **Pesquisa Multi-Fonte**

   - Busca em tempo real na internet
   - Consulta múltiplos artigos/fontes
   - Agrega e sintetiza informações

3. **Transparência Estatística**

   - Mostra % de confiança em cada resposta
   - Lista fontes consultadas
   - Indica consenso/divergência entre fontes

4. **Especialização em Código**

   - Sugestões de código com alta precisão
   - Explica trade-offs e alternativas
   - Indica quando código precisa de teste adicional

5. **Interface Conversacional**
   - Chat simples e intuitivo
   - Histórico de conversas
   - Feedback de qualidade (thumbs up/down)

---

### Out of Scope for MVP

| Feature                 | Razão para Adiar               |
| ----------------------- | ------------------------------ |
| API pública             | Foco em validar UX primeiro    |
| Plugins/Integrações IDE | Complexidade técnica alta      |
| Múltiplos idiomas       | Foco em PT-BR primeiro         |
| Fine-tuning por usuário | Requer base de usuários maior  |
| Mobile app              | Web-first para iteração rápida |
| Modo offline            | Pesquisa em tempo real é core  |

---

### MVP Success Criteria

**Gate para V1.0:**

- [ ] 500+ usuários beta com feedback positivo
- [ ] > 90% das respostas verificáveis estão corretas
- [ ] Usuários reportam economia de tempo vs outras IAs
- [ ] Taxa de "Dona Maria admitiu não saber" > 10% (prova que funciona)
- [ ] Tempo de resposta < 15 segundos mesmo com pesquisa

---

## Future Vision

### Fase 2 (Pós-MVP)

- **API para Desenvolvedores** — Integrar Dona Maria em outros produtos
- **Plugin VS Code** — Assistente de código direto na IDE
- **Modo Expert** — Configurar profundidade de pesquisa por domínio

### Fase 3 (6-12 meses)

- **Memória de Longo Prazo** — Lembrar contexto de conversas anteriores
- **Colaboração** — Times compartilhando conhecimento via Dona Maria
- **Marketplace de Especialistas** — Fontes verificadas por domínio

### Visão 2-3 Anos

> _"Dona Maria se torna sinônimo de IA confiável. Quando alguém quer uma resposta que pode confiar, pensa em Dona Maria. Somos a Wikipedia das IAs — não a mais chamativa, mas a mais confiável."_

---

## Appendix

### Documento Gerado Por

- **Workflow:** BMAD Product Brief
- **Data:** 2026-01-15
- **Autor:** Raposo
- **Agente:** Mary (Business Analyst)

### Próximos Passos Recomendados

1. **PRD (Product Requirements Document)** — Detalhar requisitos técnicos
2. **Arquitetura Técnica** — Definir stack e infraestrutura
3. **UX Design** — Wireframes e fluxos de usuário
