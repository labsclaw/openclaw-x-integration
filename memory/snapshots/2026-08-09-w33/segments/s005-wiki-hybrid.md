# Segment: s005 — Wiki & Hybrid Memory Architecture

## Resumo
Pesquisa e implementação da arquitetura híbrida LLM-Wiki + vector DB. Paper draft completo. Hyper-Extract, qmd, agentmemory instalados e funcionando.

## Conteúdo

### Inspiração: Karpathy LLM-Wiki (2026-06-26)
- Padrão: LLM compila conhecimento uma vez → wiki vivo que cresce
- Inverso de RAG: knowledge compounding vs stateless retrieval
- 3 camadas: fontes brutas → wiki markdown → interface (Obsidian)

### Pesquisa: 14 Links Analisados
- **agentmemory** (rohitg00) — ⭐⭐⭐⭐⭐ BM25+Vector+Graph, R@5=95.2%
- **qmd** (tobi) — ⭐⭐⭐⭐⭐ Search engine híbrido, GGUF local
- **Hyper-Extract** (yifanfeng97) — ⭐⭐⭐⭐⭐ 80+ templates YAML, exporta Obsidian
- **memU** (NevaMind) — ⭐⭐⭐⭐ Workspace runtime 3 camadas
- **claude-mem** (thedotmack) — ⭐⭐⭐⭐ SQLite+ChromaDB, 7 hooks
- **graphify** (safishamsi) — ⭐⭐⭐ Knowledge graph visual
- Descartados: MemSkill (acadêmico), antigravity-skills (vazio), autoresearch (inspiração)

### Arquitetura Híbrida — 6 Camadas
```
Layer 6: Interface        → Obsidian, Telegram, MCP
Layer 5: Memory           → claude-mem, agentmemory (operacional)
Layer 4: Search           → qmd (BM25 + Vector + Reranking)
Layer 3: Vector           → agentmemory (embeddings + graph)
Layer 2: Wiki             → Markdown interlinkado
Layer 1: Compilation      → Hyper-Extract
Layer 0: Raw Sources      → Fontes imutáveis
```

### OKF — Google Open Knowledge Format (2026)
- Google formalizou o padrão LLM-Wiki como formato portável
- Bundle = diretório de markdown + YAML frontmatter
- Princípios: minimally opinionated, producer/consumer independence
- Google Knowledge Catalog usa OKF em produção (Bloomberg)
- Convergência total com nossa abordagem

### Wiki Implementado
- **Estrutura**: entities/, concepts/, sources/, synthesis/, projects/, comparisons/
- **Páginas**: 18+ páginas com [[wikilinks]] e YAML frontmatter
- **Hyper-Extract**: 34 nodes + 21 edges extraídos do gist Karpathy
- **Obsidian**: 141 arquivos, vault configurado com graph view colorido

### Dreaming + Wiki Maintenance
- Dreaming nativo: Light → Deep → REM (MEMORY.md)
- Wiki maintenance: heartbeat leve sem LLM (contagem, verificação, sync)
- Separação: dreaming = memória operacional, wiki = conhecimento mundo
- Custo zero: status check + agentmemory sync sob demanda

### Ferramentas Instaladas
| Ferramenta | Versão | Status |
|---|---|---|
| Hyper-Extract | v0.3.0 | ✅ Nemotron Nano 30B (free) |
| qmd | v2.5.3 | ✅ 84 chunks, BM25 funcional |
| agentmemory | v0.9.27 | ✅ 13→18 memórias, iii-engine v0.11.2 |
| Obsidian | v1.12.7 | ✅ Vault configurado |

### Descoberta Importante
Free-tier (Nemotron Nano 30B) extraiu +89% mais entidades que gpt-4o-mini para knowledge extraction. Custo total: $0.00.

## Checkpoint
- `ckpt-2026-06-26` — Fase 1-3 completa, wiki + paper draft

### Wiki Health Stats (2026-07-25)
- **Arquivos**: 89 files
- **Link coverage**: 25.8%
- **Orphan files**: 66 (mostly knowledge-abstracts Obsidian export fragments — expected for hyper-extract output)
- **Broken links**: 1 ([[research/artificial-intelligence]] — página não existe)
- **Contradiction Check Script**: `scripts/contradiction-check.cjs` criado e verificado (0 contradições)

## Tags
wiki, hybrid-memory, karpathy, hyper-extract, qmd, agentmemory, obsidian, OKF, paper, arquitetura, contradiction-check

## Último checkpoint: 2026-07-25
