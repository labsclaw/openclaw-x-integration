---
id: s006
created: 2026-06-27
updated: 2026-07-22
weight: 1.0
accessCount: 0
---

# s006 — SSC Memory System: Da v2 ao v4.0

## Resumo
Evolução completa do Sparse Selective Cache (SSC) de v2 (semantic pyramid) a v4.0 (BM25 hybrid + classification gate + pre-compact guard). Decisão: caminho leve sem MCP Server.

## SSC v4.0 — O que foi implementado (2026-07-22)

### Componente 1: Rebuild Engine (`ssc-rebuild.cjs`)
- Schema v4.0 com BM25 IDF corpus statistics
- Tier 1: Segments (peso x2.0) — conhecimento curado de domínio
- Tier 2: Daily Logs (peso x0.5) — contexto efêmero bruto
- Calcula: frequência de termos, comprimento médio de docs, IDF (Inverse Document Frequency)
- Zero dependências externas

### Componente 2: Router Híbrido (`ssc-router.cjs` + `ssc-router.ps1`)
- BM25 probabilístico + casamento de keywords + tags
- Word boundary estrito (elimina falsos positivos em números/palavras curtas)
- Multiplier por tier: Segments x2.0, Daily x0.5
- Output: terminal ou JSON (--json) para sub-agentes
- Atualiza accessCount no index.json automaticamente

### Componente 3: Classification Gate (`memory-classify.cjs`)
- 4 categorias: ADR (Decisões), LESSON (Lições/Correções), INCIDENT, CONFIG_CHANGE
- Patterns regex por categoria
- Flag --commit: anexa em memory/corrections.md ou diário da data
- Flag --dry-run: inspeciona sem modificar

### Componente 4: Pre-Compaction Snapshot Guard (`pre-compact-guard.cjs`)
- Captura: hot.md, resumo do diário, resumo do índice (version, counts)
- Salva em memory/checkpoints/YYYY-MM-DD-pre-compact-TIMESTAMP.json
- Previne perda de contexto em sessões longas com múltiplas compacções

### Test Suite (`test-ssc-v4.cjs`)
- 6 suítes, 33 asserções, 100% pass
- Suite 1: Rebuild Engine (9 assertions)
- Suite 2: Router Engine (10 assertions)
- Suite 3: PowerShell Interface (2 assertions)
- Suite 4: Classification Gate (4 assertions)
- Suite 5: Pre-Compaction Guard (5 assertions)
- Suite 6: Edge Cases & Resilience (3 assertions)

## Decisão: Caminho Leve (sem MCP)
- Dr. Roger confirmou: NÃO implementar MCP Server
- SSC v4.0 usa scripts executáveis via exec (Node.js + PowerShell)
- Zero overhead de infra, zero dependência de servidor MCP
- Sub-agentes chamam `node scripts/ssc-router.cjs query "termo" --json` via exec

## Matriz Comparativa: Obsidian-Mind vs SSC v4.0

| Dimensão | Obsidian-Mind | SSC v4.0 | Gap |
|---|---|---|---|
| Motor de Busca | QMD (SQLite + Vector 328MB + Reranker 1.28GB) | BM25 hybrid (zero deps, ~50KB index) | OM tem semântica vetorial; nós temos busca determinística ultra-leve |
| Interface Sub-Agentes | Servidor MCP nativo (.mcp.json) | Scripts via exec (--json output) | OM padroniza como contrato MCP; nós usamos exec |
| Classificação por Mensagem | Hook UserPromptSubmit (tempo real) | memory-classify.cjs (--commit/--dry-run) | OM classifica em tempo real; nós classificamos pós-turno |
| Validação de Escrita | Hook PostToolUse (síncrono) | cron assíncrono (ssc-health-check) | OM corrige na escrita; nós corrigimos em background |
| Pré-Compacção | Hook PreCompact (automático) | pre-compact-guard.cjs (manual/invocado) | OM salva automaticamente; nós invocamos manualmente |
| Custo Injeção | ~2k tokens (SessionStart) | ~80k-98k tokens (startup files) | OM otimiza agressivamente; nós temos overhead maior |

## Deploy

### openclaw-x-integration (master)
- Commit f69f173: feat(ssc): upgrade memory system to SSC v4.0
- Scripts: ssc-rebuild.cjs, ssc-router.cjs, memory-classify.cjs, pre-compact-guard.cjs, test-ssc-v4.cjs
- memory/index.json v4.0 (12 segments + 86 dailies + BM25 stats)

### openclaw-skills (master)
- Commit d4b4a85: fix(ultra-memory-skill): remove hardcoded ClawLabs paths
- Commit b44c84b: feat(ultra-memory-skill): upgrade to SSC v4.0
- Branch feat/crag-ssc-router mergeado em master

### Lições de Deploy
1. **Paths hardcoded** — NUNCA commitar paths absolutos em repo compartilhado. Usar findWorkspace() + env OPENCLAW_WORKSPACE
2. **Branch errada** — Push para feat/ em vez de master. Confirmar branch default antes de push para release

## Referências
- Obsidian-Mind: https://github.com/breferrari/obsidian-mind
- Análise: memory/references/obsidian-mind.md
- Paper: paper/sections/paper-draft.md v0.7
- Nubank/Aurora: Nubank migrou NuPay (135M clientes, 31B linhas, 7.5TB) de PostgreSQL self-managed pra Aurora. 1.900x melhoria query, zero downtime regulatório. Ref: https://aws.amazon.com/pt/blogs/database/migrating-mission-critical-payments-at-nubank-to-amazon-aurora-postgresql/

## Cron Jobs
- ssc-health-check: diário 03:00
- check-free-models-weekly: semanal
