# MEMORY.md - Online Memory (auto-gerada)

> **Arquitetura**: Memory Caching (inspirado em arXiv 2602.24281)
> **Ultima atualizacao**: 2026-07-22
> **Segmentos ativos**: 12

## Segmentos Relevantes (carregar sob demanda)

| ID | Segmento | Status | Relevancia |
|----|----------|--------|------------|
| s001 | Infraestrutura & Env Vars | Ativo | Encoding, rate limit, Kilocode headers |
| s002 | Paperclip & Issues | Ativo | CEO cleanup, RLA management, PRs |
| s003 | Heartbeat & Alert Storm | Ativo | Stale run cascade, backup, cron |
| s004 | Skills & Projetos | Ativo | Ultra-skills, Telegram, stealth, models |
| s005 | Wiki & Hybrid Memory | Ativo | Semantic pyramid, Graphify, paper |
| s006 | SSC & Memory Architecture | Ativo | SSC v4.0, BM25 hybrid, classification gate, pre-compact guard |
| s007 | Ultra-Memory-Core | Ativo | Cognee, H.M., thread X, stealth skill |
| s008 | Finanças & Investimentos | Ativo | MSTR/STRC analysis |
| s009 | Error Tracking | Ativo | Erros registrados, lições |
| s010 | Fallback Bug OpenClaw | Ativo | Timeout bug, Instagram, memory revert |
| s011 | Cross-Agent Coordination | Ativo | Handoff Justus/Robin/Luna via GitHub privado |
| s012 | Social Media | Ativo | Instagram, X/Twitter, LinkedIn |

## Ultimos Eventos

- **2026-07-24**: Cross-agent coordination estruturada no repo privado `labsclaw/paperclip-openclaw-handoff` — inbox por agente, active.md, decisions.md
- **2026-07-22**: SSC Memory System v4.0 implementado (BM25 hybrid search, classification gate, pre-compact guard, 33/33 tests pass). GPT-OSS removido (HTTP 500), Gemini 3.6 Flash High adicionado como primary. Caminho leve confirmado (sem MCP Server).
- **2026-07-14**: ultra-models-skill v2 (142 modelos, capability map), Instagram @labsclaw2026 criado, fallback bug analisado, ultra-memory-skill revertida
- **2026-07-12**: Chrome-stealth-navigator, ultra-dom-engine-skill, Perplexity Comet/Eclipse analysis
- **2026-07-06**: SSC v2 Semantic Pyramid, Graphify knowledge graph, SQLite memory store, paper v0.4
- **2026-07-03**: Whale monitor (Galaxy Digital $100M USDC), coworker analysis, pipeline skill v1.3, social media drafts
- **2026-06-28**: ultra-memory-core (43/43 tests), Cognee analysis, thread X postada, paper v0.2
- **2026-06-27**: SSC Router implementado, ultra-memory-skill publicada, Telegram outage resolvida, watchdog corrigido
- **2026-06-18**: CEO cleanup 555+ issues, RLA management lessons
- **2026-06-06**: Telegram skill, Ultra Create/Find skills
- **2026-05-22**: Encoding fix (String→toString utf8), env vars, Perplexity Pro Bridge
- **2026-05-20**: Rate limit discovery (request format, not API key)

11. **Coordenação cross-agent via GitHub privado** — Telegram falhou (síncrono, sem estrutura). GitHub `paperclip-openclaw-handoff` é o canal oficial. Cada agente checa inbox no primeiro turno.

## Decisões Importantes

1. **Zero vendor lock-in** — Copiar ideias, não código (Cognee → nosso graph reasoning)
2. **PM2 é o único dono do gateway** — NUNCA criar Windows Scheduled Tasks
3. **Nemotron omni para visão** — Nunca reasoning para computer vision
4. **Ultra skills naming** — `ultra-<nome>-skill` em `openclaw-skills/`
5. **Encoding UTF-8** — `chunk.toString("utf8")` em vez de `String(chunk)` no Windows
6. **Pipeline monitoring** — Toda tarefa >60s DEVE ter pipeline ou watchdog
7. **Credentials** — Sempre salvar em `memory/credentials.md` imediatamente
8. **CEO não abandona issues** — Agir ou cancelar, nunca ignorar
9. **Caminho leve sobre MCP** — SSC v4.0 usa scripts Node/PS executáveis via exec, não servidor MCP. Zero overhead de infra.
10. **Paths em repo compartilhado** — NUNCA hardcoded paths. Usar auto-detection ou env var (OPENCLAW_WORKSPACE).

## Lições Aprendidas

1. **Rate limit é por formato, não por key** — Proxy inspection descobriu que o formato JSON da requisição é o que o servidor valida
2. **"DNS unreachable" pode ser misleading** — Era conflito de processo, não problema de rede
3. **Inferir intenção, não descrever** — Quando Dr. manda URL de skill, quer transformação, não descrição
4. **Não inventar usernames** — Perguntar em vez de inventar (@robin_nascimento vs @RobinBRIAbot)
5. **Verificar antes de copiar** — Comparar source/dest antes de Copy-Item
6. **Alert storms são desperdício** — 25+ wake events sem trabalho = compute jogado fora

## PRs/Issues Pendentes

- **PR #7440** (Paperclip): UTF-8 fix — GREPTILE PASS, aguardando maintainer approval
- **PR #8084** (Paperclip): antigravity adapter — GREPTILE LGTM, aguardando review humano
- **PR #104086** (OpenClaw): pingado para review
- **PR #354** (antigravity-proxy): GPT-OSS support — reminder disparado 2026-06-28

## Cron Jobs Ativos

- `paperclip-log-cleanup` — diário 02:00
- `backup-paperclip-openclaw` — diário 06:00
- `ssc-health-check` — diário 03:00
- `check-opencode-version` — semanal

---

> Este arquivo e gerado automaticamente a partir dos segmentos em `memory/segments/`.
> Nao edite diretamente - atualize os segmentos e rode manutencao.
