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


## Wake Event efb3424e - heartbeat_timer (2026-06-07 09:12 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO


## Wake Event 97c768e6 - heartbeat_timer (2026-06-07 10:16 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO


## Wake Event 31dc298e - heartbeat_timer (2026-06-07 11:21 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO


## Wake Event 2790273c - heartbeat_timer (2026-06-07 12:27 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO


## Wake Event c56bb12f - heartbeat_timer (2026-06-07 13:33 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO


## Wake Event 1b702941 - heartbeat_timer (2026-06-07 14:40 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO


## Wake Event 6d04f423 - heartbeat_timer (2026-06-07 15:47 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO


## Wake Event 64e4b8f6 - heartbeat_timer (2026-06-07 16:57 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO


## Wake Event 2be3ca19 - heartbeat_timer (2026-06-07 18:05 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO

## Wake Event - task_cleanup (2026-06-07 18:05 GMT-3)

- **Task:** Task cleanup executed after gateway restart
- **Actions taken:**
  - RLA-276 closed as false positive (same run `ee426440` already reviewed 23x)
  - 3 orphan "running" tasks cleaned (cloud adapter wake events without real issues)
  - Final count: 3 done + 22 failed + 7 lost + 187 succeeded = 219 total
- **Note:** 7 "lost" tasks are old (June 02) with no system impact. No open issues in Paperclip.


## Wake Event 0ba68697 - heartbeat_timer (2026-06-07 21:05 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO


## Wake Event f5998040 - heartbeat_timer (2026-06-07 22:11 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO


## Wake Event ea060659 - heartbeat_timer (2026-06-07 23:12 GMT-3)

- **Agent:** OpenClaw (CEO) / openclaw_gateway
- **Status:** No open issues assigned; RLA-132 (backlog, high priority) assigned to CTO for stale detection fix
- **Context:** Systemic alert storm continues - opencode_local adapter NOT de-duplicating by originFingerprint
- **Action:** Wake processed; no blocking work for CEO

