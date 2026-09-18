# Evolução da Memória SSC: Navegação Hierárquica por Árvore de Raciocínio (Tree Navigation RAG)

<!-- project: github.com/labsclaw/openclaw-x-integration -->

- **Data:** 2026-09-18
- **Status:** Arquitetura ativa em expansão
- **Referência Externa:** Paradigma PageIndex / VectifyAI (Vectorless Tree RAG)

---

## 1. Diagnóstico da Memória SSC Atual (v4.1)

O sistema de memória SSC (Segmented Semantic Context) do OpenClaw foi concebido para resolver a perda de contexto longitudinal sem incorrer em alucinações de modelos ou fragmentação arbitrária de embeddings:
- **Estrutura Atual:** Baseada em segmentos temáticos independentes (`memory/segments/s*.md`), diários cronológicos (`memory/daily/`) e índice invertido BM25 com roteamento semântico determinístico (`scripts/ssc-router.cjs`).
- **Limitação Identificada:** Em consultas complexas ou cross-domain (ex: regras de negócio que afetam simultaneamente infraestrutura, finanças e testes ALM), a busca plana por similaridade lexical (BM25) ou densa tende a ranquear nós individuais sem capturar o caminho de dependência hierárquica.

---

## 2. Princípio da Árvore de Raciocínio (Tree Navigation)

Inspirado na arquitetura do **PageIndex** (busca em árvore estilo AlphaGo):
> *"Similaridade não é Relevância. Relevância exige raciocínio sobre a estrutura hierárquica do conhecimento."*

A evolução para **SSC v4.2+** introduz a decomposição em árvore:

```
[SSC Master Knowledge Root]
   │
   ├─ [Domínio: Infraestrutura & Runtimes] ───────── s001-infra, opencode-integration
   ├─ [Domínio: Engenharia de Software & QA] ────── x-testing-*, sanasa-requirements
   ├─ [Domínio: Pesquisa Científica & Papers] ───── paper-submission-strategy, tree-rag
   ├─ [Domínio: Governança & Decisões] ───────────── decisions, org-chart, boardroom
   └─ [Domínio: Memória Longitudinal & Histórico] ── daily-logs, checkpoints
```

---

## 3. Diretrizes de Implementação

1. **Roteamento Top-Down:**
   - O roteador de memória avalia primeiro a pertinência no nível de **Domínio**, selecionando os ramos ativos.
   - Em seguida, percorre os **Segmentos** pertinentes e, dentro deles, identifica as **Seções/Nós** de alta relevância lógica.
2. **Eliminação do "Vibe Retrieval":**
   - A recuperação entrega ao agente o caminho de navegação completo (Domain -> Segment -> Section), garantindo explicabilidade e auditabilidade.
3. **Coexistência com BM25:**
   - O BM25 permanece como filtro rápido de suporte no nível de nós folha, enquanto a árvore guia a navegação estrutural.
