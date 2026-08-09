# Segment: s002 — Paperclip e Issues

## Resumo
Gestão de issues Paperclip, RLA-*, decisões de CEO, limpeza de waste.

## Conteúdo

### CEO Session (2026-05-22)
- Cleanup de waste: cancelou productivity reviews, fechou issues completas
- Encoding fix aplicado, env vars injetadas

### Issues Conhecidas
- **RLA-207** (aberta): opencode_local adapter NÃO de-duplica por originFingerprint
- **RLA-132** (alta prioridade, stale): stale run detection false positive fix — atribuída ao CTO, stalled 48h+
- **RLA-276** (fechada): false positive — mesmo run `ee426440` já revisado 23x

### Tarefas (2026-06-07 18:05 GMT-3)
- 3 orphan "running" tasks limpas (cloud adapter wake events sem issues reais)
- Contagem final: 3 done + 22 failed + 7 lost + 187 succeeded = 219 total
- 7 "lost" tasks antigas (Jun 02) sem impacto no sistema

### Política de Logs (2026-06-07)
- server.log ~31.5MB — abaixo do limiar crítico de 100MB
- Manutenção preventiva não justificada agora
- Monitorar apenas quando logs > 100MB

## Checkpoint
- `ckpt-2026-05-22` — CEO cleanup executado
- `ckpt-2026-06-07` — Task cleanup + decisão de logs

### CEO Cleanup Massiva (2026-06-18)
- Dr. Roger alertou: CEO estava abandonando empresa, perdendo companyId, fechando issues sem agir
- **555+ issues de review automático canceladas** via browser/API
- Issues manipuladas: RLA-650 (in progress), RLA-637 (blocked), RLA-32 (cancelled)
- Issues ativas restantes: 61 (de ~600+)
- API correta: `PATCH /api/issues/{identifier}` — companyId: `59aa149d-17b5-43a4-b322-8e315d04cdef`
- **Lição**: CEO não pergunta sem oferecer tradeoffs. Não abandonar issues — agir ou cancelar, nunca ignorar

### RLA-648 Productivity Review (2026-06-17)
- Eng. Dados opencode_local adapter: 100 runs, 0 tokens, 0 cost, 0 work products
- Causa raiz: adapter/infraestrutura, NÃO problema do agente
- RLA-650 criada para fix do adapter

### RLA-639 Prospecção de Revendedores (2026-06-16)
- Material de prospecção: 12+ revendedores, pitch deck, plano
- 4 child issues criadas para Tier 1: Grupo Sinal, Fator Brasil, Vipal, Semimix
- Templates de contato (LinkedIn/WhatsApp) documentados

### PR #7440 Status (2026-06-24)
- Greptile review: PASS (2m59s), todos 6 checks green, PR MERGEABLE
- Bloqueador: sem aprovação de maintainer (repo paperclipai/paperclip não é nosso)

### PR #8084 Paperclip (2026-07-14)
- Greptile bot aprovou (LGTM)
- Comentário mencionando @cryppadotta para review humano

### PR #104086 OpenClaw (2026-07-14)
- Pingado para review

### ORG Structure (2026-07-08)

```
CEO (Justus)
├── Especialista Automotivo
└── UX Designer (Research·Design)
    ├── Eng. Infra (DevOps)
    ├── Eng. Dados (Engineer)
    ├── Eng. Percepção (Research)
    └── Eng. Skills (Engineer)
```

URL: http://127.0.0.1:3100/RLA/org

### PR #8084 Merge Conflict Resolution (2026-07-19)
- **Repo:** labsclaw/paperclip (fork of paperclipai/paperclip)
- **Branch:** fix/windows-console-window-spam
- **PR:** #8084 — "fix: hide console windows on Windows by resolving .cmd wrappers to real executables"
- **File:** `packages/adapter-utils/src/server-utils.ts` (single conflict)
- **Conflicts resolved (4):**
  1. Import section: added `parseCmdWrapperContent` import after master's new `buildLocalProcessSandbox` import
  2. SpawnTarget.env type: kept master's `Record<string, string | undefined>` (PR had narrower `Record<string, string>`)
  3. resolveSpawnTarget(): inserted cmd wrapper try/catch block before cmd.exe fallback
  4. runChildProcess() spawn call: added `windowsHide: process.platform === "win32"`, preserved master's `childEnv` merge pattern
- **Commit pushed:** `1d7b0f0d` via GitHub API (Node.js script to handle large base64 payload)
- **Status at push:** `mergeable: true`, `merge_state: UNSTABLE` (CI running)
- **Resolution approach:** Node.js script reads master, applies PR's 4 additive changes, verifies with checks, pushes via `gh api PUT`

### PR Status Updates (2026-07-21)
- **PR #7440 (Paperclip): UTF-8 fix** — GREPTILE PASS, aguardando maintainer approval
- **PR #8084 (Paperclip): antigravity adapter** — GREPTILE LGTM, aguardando review humano (@cryppadotta mencionado)
- **PR #104086 (OpenClaw): pingado para review**
- **PR #354 (antigravity-proxy): GPT-OSS support** — reminder disparado 2026-06-28

## Checkpoint
- `ckpt-2026-05-22` — CEO cleanup executado
- `ckpt-2026-06-07` — Task cleanup + decisão de logs
- `ckpt-2026-06-18` — CEO cleanup 555+ issues, RLA decisions
- `ckpt-2026-07-19` — PR #8084 merge conflict resolution

## Tags
paperclip, issues, CEO, limpeza, operações, org, merge-conflict

## Último checkpoint: 2026-07-19