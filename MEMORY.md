# MEMORY.md — Online Memory (auto-gerada)

> **Arquitetura**: Memory Caching (inspirado em arXiv 2602.24281)
> **Última atualização**: 2026-06-28 09:37
> **Segmentos ativos**: 7 | **Checkpoints**: 5

## Sobre Dr. Roger Oliveira
- Doutor em Modelagem Computacional, expert em engenharia reversa e infraestrutura de AI
- Telegram: @SmartNewbieBR | X: @SmartNewbieBR
- Timezone: America/Sao_Paulo (GMT-3)

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

---

> Este arquivo é gerado automaticamente a partir dos segmentos em `memory/segments/`.
> Não edite diretamente — atualize os segmentos e rode manutenção.
