# MEMORY.md — Online Memory (auto-gerada)

> **Arquitetura**: Memory Caching (inspirado em arXiv 2602.24281)
> **Última atualização**: 2026-07-13 16:16
> **Segmentos ativos**: 7 | **Checkpoints**: 5
> **Novo**: Hot Cache + BM25 + Ingest + Contradiction + Log Fold (5 melhorias baseadas em claude-obsidian)

## Sobre Dr. Roger Oliveira
- Doutor em Modelagem Computacional, expert em engenharia reversa e infraestrutura de AI
- Telegram: @SmartNewbieBR | X: @SmartNewbieBR
- Timezone: America/Sao_Paulo (GMT-3)

## Padrão Obrigatório de Skills
- **Local:** `openclaw-skills/`
- **Pattern:** `ultra-<nome>-skill` (prefixo `ultra-`, sufixo `-skill`, kebab-case)
- **NUNCA** criar skill sem esse padrão ou em pasta errada

## Segmentos Relevantes (carregar sob demanda)

| ID | Segmento | Status | Relevância |
|----|----------|--------|------------|
| s001 | [Infraestrutura](memory/segments/s001-infra.md) | ✅ Resolvido | encoding, env vars |
| s002 | [Paperclip Issues](memory/segments/s002-paperclip.md) | ⚠️ RLA-207 aberta | paperclip, issues, CEO |
| s003 | [Heartbeat Storm](memory/segments/s003-heartbeat.md) | ⚠️ Não resolvido | heartbeat, RLA-207, desperdício |
| s004 | [Skills & Projetos](memory/segments/s004-skills.md) | 🔄 Em andamento | telegram, ultra-skills |
| s005 | [Wiki & Hybrid Memory](memory/segments/s005-wiki-hybrid.md) | ✅ Completo | wiki, paper, arquitetura |
| s006 | [SSC & Incident](memory/segments/s006-ssc-skill-incident.md) | ✅ Resolvido | ssc-router, skill, incidente |
| s007 | [28/06 Ultra-Memory-Core](memory/segments/s007-2026-06-28.md) | 🔄 Em andamento | cognee, ultra-memory-core, paper-v0.2, stealth |

## Últimos Eventos
- **2026-06-28**: ultra-memory-core completo (43/43 testes), Cognee analisado, paper v0.2, thread X postada
- **2026-06-27**: SSC Router implementado, ultra-memory-skill publicado no GitHub
- **2026-06-27**: Incidente Telegram outage (~15h) — fix: PM2 restart, scheduled task disabled
- **2026-06-27**: Watchdog corrigido — restart via PM2 em vez de cmd.exe
- **2026-06-26**: Paper draft v0.1 completo (6 seções, 13+ referências)
- **2026-06-26**: Wiki híbrida implementada — 18 páginas, Hyper-Extract, qmd, agentmemory
- **2026-06-23**: Revisão de memória — identificados PRs pendentes

## PRs/Issues Pendentes (ACOMPANHAR)
- **PR #354** (antigravity-proxy): GPT-OSS model support — OPEN, pingar maintainer se não responder até 30/06
- **PR #7710** (paperclip): antigravity local adapter — OPEN, 9 commits
- **RLA-207**: opencode_local adapter não de-duplica por originFingerprint
- **RLA-132**: stale run detection false positive fix — stalled 48h+

## Regras Importantes
- **PM2 é o único dono do gateway** — nunca criar Scheduled Tasks (incidente 2026-06-27)
- Engenharia de Percepção: Nemotron "omni" (non-reasoning) para visão computacional
- Memory Caching: carregar `memory/index.json` → matcher → carregar apenas K segmentos relevantes
- Manutenção de memória: durante heartbeats, comprimir/fundir segmentos obsoletos

## Melhorias 2026-07-13 (baseado em claude-obsidian)

### Scripts Novos
| Script | O que faz | Uso |
|--------|-----------|-----|
| `memory/hot.md` | Fast cache: contexto imediato da sessão (~500 palavras) | Ler primeiro em toda sessão |
| `scripts/contradiction-check.cjs` | Detecta contradições entre páginas do wiki | `node scripts/contradiction-check.cjs` |
| `scripts/log-fold.cjs` | Rollup de daily logs em segments temáticos | `node scripts/log-fold.cjs` |
| `scripts/wiki-ingest.cjs` | Ingest automatizado de URLs/texto/file em wiki | `node scripts/wiki-ingest.cjs --url=<URL>` |
| `scripts/bm25-retrieve.cjs` | BM25 retrieval puro Node.js (sem deps) | `node scripts/bm25-retrieve.cjs build` / `query "..."` |

### Arquitetura Atualizada
```
Session Start → hot.md (fast cache) → MEMORY.md (slow cache) → SSC Router → Segments

Ingest: URL/text/file → wiki-ingest → entities + concepts + index.json
Retrieval: query → bm25-retrieve → top-K pages
Lint: contradiction-check → flag contradições
Fold: log-fold → daily → segments (a cada 7 dias)
```

---

> Este arquivo é gerado automaticamente a partir dos segmentos em `memory/segments/`.
> Não edite diretamente — atualize os segmentos e rode manutenção.
