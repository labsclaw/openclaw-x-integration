# Segment: s006 — Ultra Memory Skill & SSC Implementation

## Resumo
Implementação do SSC Router (Memory Caching), criação do ultra-memory-skill, publicação no GitHub, e incidente de Telegram outage.

## Conteúdo

### SSC Router (2026-06-27)
- Script PowerShell puro: `ssc-router.ps1` + `ssc-health.ps1`
- Scoring: keywords (2x) + tags (1x) + weight (0.5x)
- accessCount: incrementa a cada query, salva no index.json
- Modos: -Query, -List, -Stats, -DryRun
- Encoding UTF-8 corrigido (bug Windows CP850)

### Health Check (2026-06-27)
- Cron job diário 3h da manhã (isolado, announce only se issue)
- Verifica: segmentos, daily logs, checkpoints, index consistency
- Primeiro resultado: 4 segmentos saudáveis, 178KB total

### Ultra Memory Skill — Publicação (2026-06-27)
- Repo: `labsclaw/openclaw-skills/ultra-memory-skill/`
- Arquivos: scripts, templates, examples, references, SKILL.md, README.md
- Zero dependências de terceiros
- Revisão paper vs implementação: gaps documentados (Memory Soup, auto-split)

### Incidente: Telegram Outage (2026-06-27)
- Duração: ~15h (00:00–15:30)
- Causa: Windows Scheduled Task executava `gateway.cmd` inexistente → processo órfão
- Dois gateways no mesmo bot → conflito getUpdates
- Fix: matar processos, PM2 restart, desabilitar scheduled task
- Regra adicionada ao AGENTS.md: NUNCA criar Scheduled Tasks para gateway

### Watchdog Corrigido (2026-06-27)
- `openclaw-watchdog`: restart agora usa `pm2 restart` em vez de `cmd.exe`
- `install.ps1`: detecta PM2, desabilita Scheduled Tasks conflitantes
- SKILL.md: documenta método correto, referência ao incidente

### Unificação do AGENTS.md (2026-06-27)
- Workspace AGENTS.md e root AGENTS.md sincronizados (259 linhas, 11KB)
- Decisão: MC Architecture como primário, para-memory-files como fallback para grupos
- Nota técnica criada: `logs/incidents/2026-06-27-agents-md-technical-note.md`
- Referências cruzadas validadas (HEARTBEAT, SOUL, TOOLS, group-chats)

### Lições Aprendidas
- PM2 é o único dono do gateway — nunca usar cmd.exe ou schtasks
- Erro "DNS unreachable" pode ser misleading (era conflito de processo)
- Scripts PowerShell precisam de `-Encoding UTF8` no Windows
- PowerShell não suporta `&&` — usar `;` como separador
- Manter um único AGENTS.md — sincronizar entre workspace e root

## Checkpoint
- `ckpt-2026-06-27` — SSC implementado, skill publicada, incidente resolvido
- `ckpt-2026-06-27-agents-md-unification` — AGENTS.md unificado, decisão de memória

### SSC Health Check Cron (2026-06-27)
- Cron job diário 03:00 BRT, isolated, delivery: Telegram
- Verifica: segmentos, daily logs, checkpoints, index consistency
- Funcionando desde 2026-06-27

### Ultra-Memory-Core (2026-06-28)
- Módulo de graph reasoning + vector search em Node.js puro (ZERO deps npm)
- API: remember/recall/forget/improve (padrão Cognee)
- 43/43 testes passando
- Decisão: copiar ideia do Cognee, não o código — zero vendor lock-in

### SSC v2 — Semantic Pyramid (2026-07-06)
- 4-tier hierarchy (L0-L3) inspirada no TencentDB Agent Memory
- 46 atoms extraídos dos 8 segments existentes
- `drill-down.js` — retrieval hierárquico funcional
- Filosofia: adaptação sem vendor lock-in, 100% Markdown + JSON

### SQLite Memory Store (2026-07-06)
- `memory/scripts/store.js` — SQLite + FTS5 + vector embeddings
- Schema PostgreSQL-compatible (atoms, embeddings, segments, access_log)
- 46 atoms importados, FTS5 keyword + cosine similarity re-ranking

### Knowledge Graph — Graphify (2026-07-06)
- `graphify claw install` — seção adicionada ao AGENTS.md
- Padrão EXTRACTED vs INFERRED incorporado aos atoms
- Extração completa do workspace causa OOM no Windows — rodar em subdiretórios

## Tags
ssc-router, health-check, ultra-memory-skill, github, incidente, telegram, outage, watchdog, PM2, semantic-pyramid, sqlite, graphify

## Último checkpoint: 2026-07-06
