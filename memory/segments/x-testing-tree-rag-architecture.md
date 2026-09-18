# Arquitetura Tree-RAG para Especificações e Requisitos SANASA (X-Testing)

<!-- project: github.com/labsclaw/openclaw-x-integration -->

- **Data:** 2026-09-18
- **Contexto:** Fábrica de Testes X-Testing — Operação SANASA (Campinas/SP)
- **Tecnologia:** PageIndex / Vectorless Reasoning-based Tree RAG

## 1. O Problema do RAG Vetorial Clássico em Requisitos de Engenharia

Na esteira de automação de testes da SANASA, as regras de negócio, editais de saneamento e requisitos funcionais (RF001 a RF061) apresentam alta interdependência estrutural:
- Regras de faturamento e medição de água dependem de premissas estipuladas em capítulos anteriores.
- A divisão arbitrária de PDFs em chunks vetoriais quebra o contexto contíguo, separando tabelas de parâmetros de suas condições de contorno.
- A busca por similaridade de cosseno ("vibe retrieval") recupera fragmentos superficialmente semelhantes, mas omite cláusulas essenciais descritas com vocabulário técnico divergente.

## 2. Solução: Ingestão Hierárquica em Árvore (Tree Indexing)

Inspirado na arquitetura do PageIndex (AlphaGo-style tree search), a esteira de QA da X-Testing adota a representação em árvore sem banco vetorial e sem chunking:

```
[Documento Mestre SANASA]
   │
   ├─ [Domínio 1: Regras Operacionais de OS]
   │    ├─ [Tipo de Serviço: Ligação de Água]
   │    │    ├─ RF002: Validação de Hidrômetro
   │    │    └─ RF043: Emissão de Ordem de Serviço em Campo
   │    └─ [Tipo de Serviço: Esgoto & Manutenção]
   │         └─ RF050: Vistoria e Interdição
   │
   ├─ [Domínio 2: Critérios de Aceite e Métricas]
   │    ├─ SLA de Resolução
   │    └─ Integração TestLink (Suites, Casos de Teste, Execuções)
   │
   └─ [Domínio 3: Regras Financeiras e Tarifárias]
        └─ RF058/RF061: Cálculo de Consumo e Penalidades
```

## 3. Benefícios Operacionais para os Agentes de Teste

1. **Rastreabilidade Fidedigna (Traceability):**
   - Cada nó da árvore preserva `node_id`, título, linha de início, contagem de caracteres e RFs associados.
   - O agente **QA Designer** navega da raiz até a folha específica, citando a seção exata no caso de teste exportado para o TestLink.
2. **Zero Alucinação de Dependências:**
   - Ao analisar o RF043, o agente inspeciona o ramo pai imediato ("Regras Operacionais de OS") e herda todas as premissas contratuais sem depender de match semântico probabilístico.
3. **Desempenho e Custo:**
   - Geração da árvore executada em milissegundos localmente (`scripts/sanasa-tree-indexer.py`).
   - Economia drástica de tokens: o LLM de teste navega apenas pelos nós do percurso de raciocínio, sem ingestão contínua de PDFs de 500 páginas na janela de contexto.

## 4. Implementação no Workspace

- **Indexador Operacional:** `scripts/sanasa-tree-indexer.py`
- **Artefato Consolidado:** `artifacts/x-testing/sanasa-requirements-tree.json`
- **Integração:** Consumido pelos agentes da esteira SANASA via Paperclip e conectores ALM.
