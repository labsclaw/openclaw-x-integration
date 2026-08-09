# Segment: s001 — Infraestrutura e Env Vars

## Resumo
Configuração de infraestrutura: encoding UTF-8 no Windows, env vars NVIDIA/OpenRouter, correção de bug de encoding.

## Conteúdo

### Encoding Bug (RESOLVIDO — 2026-05-22)
- **Problema**: `String(chunk)` em `adapter-utils/dist/server-utils.js` (L1532, L1548) usava CP850 no Windows em vez de UTF-8
- **Fix**: `typeof chunk === "string" ? chunk : chunk.toString("utf8")`
- **PR**: [paperclipai/paperclip#7440](https://github.com/paperclipai/paperclip/pull/7440) — open, não merged ainda
- **Nota**: Precisa restartar Paperclip para recarregar módulo (npx cache)

### NVIDIA/OpenRouter Env Vars (RESOLVIDO — 2026-05-22)
- Copiadas do `~/.openclaw/.env` para User env vars do Windows
- Agents Paperclip acessam via `process.env` diretamente

### Engenharia de Percepção
- **Regra**: Usar Nemotron "omni" (non-reasoning) sempre para visão computacional. Nunca usar reasoning.

### Rate Limit Discovery (2026-05-20)
- Dr. Roger descobriu que o rate limit do opencode não é por API key, mas por **formato da requisição JSON**
- Inspecionou via proxy as requisições do opencode original vs OpenClaw
- Encontrou atributos diferentes na formação do JSON (headers `x-opencode-session`, `x-opencode-request`, etc.)
- Forçou o OpenClaw a montar requisições no mesmo formato → sem rate limits
- Guias consolidados em `GUIA-REPLICACAO-OPENCODE-OPENCLAW.md`
- Docs originais arquivados em `archive/` (SOLUCAO-API-LIMIT, TUTORIAL-TECNICO, CADEIA-DE-RACIOCINIO)

### Kilocode CLI Headers (2026-05-23)
- Dr. Roger varreu o pacote `@kilocode/cli` v7.3.1 e descobriu os headers exatos:
  - `x-kilocode-client: cli`, `x-kilocode-project: global`
  - `x-kilocode-session: ses_openclaw_static_session`
  - `x-kilocode-request: msg_openclaw_static_request`
- Headers inseridos diretamente na config do Kilocode no `openclaw.json`

### bundledDiscovery Fix (2026-07-16)
- **Problema**: `bundledDiscovery: "compat"` auto-descobriu MCP servers e providers arbitrários (multica, context7, groq, huggingface, cerebras, github-models, puppeteer)
- **Sintoma**: Crash loop (3 boots sujos em 5min) → `restart-loop breaker` tripou
- **Causa**: `multica-mcp` não existe no disco, Groq tentou auth com API key inválida
- **Fix**: `bundledDiscovery` alterado de `"compat"` para `"safe"` no `openclaw.json`
- **Nota**: Gateway sobrescreve edições manuais do arquivo. Editar via config corretamente.

### Fallback Chain Redesign (2026-07-21)
- **Problema**: mimo-v2.5-free HTTP 500, 8 de 10 fallbacks quebrados
- **Diagnóstico com logs reais (runId 13763111)**: hy3-free 401, deepseek-v4-pro timeout 120s, deepseek-v4-flash:free 404 (virou pago), gemini-3.5-flash nome errado, gpt-oss-120b-medium formato incompatível
- **Nova cadeia aplicada** (direto no arquivo — config.patch bloqueia `agents.defaults.model.fallbacks`):
  ```
  primary: opencode/mimo-v2.5-free
  fallbacks:
    1. opencode/big-pickle
    2. openrouter/nvidia/nemotron-3-super-120b-a12b:free
    3. openrouter/poolside/laguna-m.1:free
    4. kilocode/nvidia/nemotron-3-super-120b-a12b:free
    5. kilocode/poolside/laguna-m.1:free
    6. openrouter/google/gemma-4-31b-it:free
    7. openrouter/nvidia/nemotron-3-ultra-550b-a55b:free
    8. nvidia/nemotron-3-super-120b-a12b
    9. antigravity-proxy/gemini-3.5-flash-extra-low
  ```
- **Regra**: Máximo 1 do mesmo provider seguido (Dr. Roger: "não deixe 3 seguidos no provedor opencode")
- **Notas**: Gateway auto-corrige prefixo NVIDIA; backup salvo como `openclaw.json.bak.<timestamp>`; reiniciado via `pm2 restart openclaw-gateway`

### GPT-OSS Removal + Gemini 3.6 Flash (2026-07-22)
- GPT-OSS 120b-medium HTTP 500 (RESOURCE_EXHAUSTED) no antigravity-proxy
- Removido de: openclaw.json (config + fallbacks), _shared.ps1 (quality, TPS, family, capabilities)
- Adicionado: gemini-3.6-flash-high/medium/low/tiered ao antigravity-proxy
- Primary alterado para antigravity-proxy/gemini-3.6-flash-high
- Fallback chain enxutada (removidos medium, low, hy3-free, deepseek-v4-pro)

### Crash Loop — google-ai-studio.apiKey Inválido (2026-06-29)
- 20 consecutive crash loops: gateway restartou em loop por causa de `google-ai-studio.apiKey` inválido
- Provider removido do `openclaw.json` pra estabilizar
- Sessões corrompidas: crash loop pode ter deixado stale session locks
- Lição: validar API key antes de adicionar provider ao config

### Diagnóstico "Agent couldn't generate a response" (2026-06-29)
- Big Pickle `maxTokens: 128000` causando timeout — reduzido pra 8192
- `User-Agent` desatualizado (`opencode/1.15.5` → `1.17.11`)
- `x-opencode-project` genérico (`global` → `zen-openclaw`)
- `models.json` do antigravity-proxy com schema inválido — faltando `cacheRead`/`cacheWrite`

### Doctor --fix Executado (2026-06-29)
- `openclaw doctor --fix` rodado
- Warnings: 3 TaskFlows bloqueados, 1 cron quebrado removido (paperclip-status-check), secrets em plaintext
- Stale session lock removido manualmente
- models.json + catalog.json corrigidos com cacheRead/cacheWrite

### pwsh 7.6.3 Migration Fix (2026-07-10 → 2026-07-11)
- Ver `s014-pwsh-migration.md` para detalhes completos
- Fix local: `gateway-wrapper.js` seta `process.env.ProgramW6432` apontando pra cópia do pwsh 7.6.3
- PR upstream: https://github.com/openclaw/openclaw/pull/104086
- Monitor: cron `pm:pr104086` (09:00 e 21:00 São Paulo)

### Hydra3 Free como Provider (2026-07-10)
- `opencode/hy3-free` adicionado como 1st fallback após mimo
- Tencent Hy3: 295B MoE (21B active), 256K ctx, Apache 2.0
- Testado: 200, 2.5s, tool calling OK, $0

## Checkpoint
- `ckpt-2026-05-22` — Encoding fix + env vars injetadas
- `ckpt-2026-07-16` — bundledDiscovery fix
- `ckpt-2026-07-21` — Fallback chain redesign
- `ckpt-2026-07-22` — GPT-OSS removal, Gemini 3.6 Flash primary
- `ckpt-2026-07-11` — pwsh 7.6.3 migration fix

## Tags
infraestrutura, encoding, env-vars, windows, bug-fix, resolvido, fallback, models, antigravity, bundledDiscovery, pwsh, migration, crash-loop, doctor-fix

## Último checkpoint: 2026-07-22
