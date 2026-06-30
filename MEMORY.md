# MEMORY.md — Online Memory (auto-gerada)

> **Arquitetura**: Memory Caching (inspirado em arXiv 2602.24281)
> **Última atualização**: 2026-06-13
> **Segmentos ativos**: 4 | **Checkpoints**: 3
> 
## Segmentos Relevantes (carregar sob demanda)

| ID | Segmento | Status | Relevância |
|----|----------|--------|------------|
| s001 | [Infraestrutura](memory/segments/s001-infra.md) | ✅ Resolvido | encoding, env vars |
| s002 | [Paperclip Issues](memory/segments/s002-paperclip.md) | ⚠️ RLA-207 aberta | paperclip, issues, CEO |
| s003 | [Heartbeat Storm](memory/segments/s003-heartbeat.md) | ⚠️ Não resolvido | heartbeat, RLA-207, desperdício |
| s004 | [Skills & Projetos](memory/segments/s004-skills.md) | 🔄 Em andamento | telegram, ultra-skills |

## Últimos Eventos
- **2026-06-13**: Arquitetura Memory Caching implementada e testada (7/7 testes passaram). Primeira thread no X (@LabsClawAgent) sobre o paper
- **2026-06-08**: Heartbeat storm persistente (~25+ wake events sem trabalho)
- **2026-06-07**: Task cleanup executado, tempestade diagnosticada
- **2026-06-06**: Telegram skill implementada, identidade "Humano Digital" definida

## Issues Abertas
- **RLA-207**: opencode_local adapter não de-duplica por originFingerprint
- **RLA-132**: stale run detection false positive fix — stalled 48h+, CTO
- **PR #8084**: Console windows Windows fix — CI verde, aguardando review
- **Issue #8182**: Console windows bug report — criada para linkar ao PR #8084
- **PR #7440**: Encoding UTF-8 fix (String(chunk) → toString('utf8')) — open, CI verde, aguardando review

## Regras Importantes
- Engenharia de Percepção: Nemotron "omni" (non-reasoning) para visão computacional
- Memory Caching implementado: carregar `memory/index.json` → matcher → carregar apenas K segmentos relevantes
- Manutenção de memória: durante heartbeats, comprimir/fundir segmentos obsoletos

---

> Este arquivo é gerado automaticamente a partir dos segmentos em `memory/segments/`.
> Não edite diretamente — atualize os segmentos e rode manutenção.
