# MEMORY.md - Long-term memory for Dr. Roger Oliveira

- Name: Dr. Roger Oliveira
- Expertise: Engenharia reversa e infraestrutura de AI
- Telegram: @SmartNewbieBR
- X: @SmartNewbieBR
- Timezone: America/Sao_Paulo (GMT-3)
- Current interest: Criando novas empresas lucrativas de sucesso no paperclip (2026-05-21)
- **Eng. Percepção rule**: Use Nemotron "omni" (non-reasoning) sempre para visão computacional. Nunca usar reasoning.
- **Encoding bug (FIXED 2026-05-22)**: Era `String(chunk)` em `adapter-utils/dist/server-utils.js` stdout/stderr data handlers (L1532, L1548). No Windows `String(buffer)` usa CP850, nao UTF-8. Fix: `typeof chunk === "string" ? chunk : chunk.toString("utf8")`. Ainda precisa restartar Paperclip pra recarregar o modulo (npx cache).
- **NVIDIA/OpenRouter env vars**: Copiados do `~/.openclaw/.env` para User env vars do Windows (2026-05-22). Agents Paperclip acessam direto via process.env agora.
- **CEO session 2026-05-22**: Cleanup de waste (cancelou productivity reviews, fechou issues completas), encoding fix aplicado, env vars injetadas.

## Wake Event 36ae4027 - heartbeat_timer (2026-06-07 08:05 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO

