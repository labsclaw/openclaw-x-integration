# Segment: s003 — Heartbeat e Alert Storm

## Resumo
Tempestade de alertas de heartbeat (25+ wake events sem trabalho), diagnóstico, e solução.

## Conteúdo

### Heartbeat Alert Storm (2026-06-07 → 2026-06-08)
- **~25+ wake events consecutivos** (04:50 GMT-3 → 07:25 GMT-3 dia seguinte)
- Zero trabalho acionável para o agente CEO em cada wake

### Root Cause
- opencode_local adapter NÃO de-duplicando por `originFingerprint` (RLA-207)

### Impacto
- ~25 wake events × chamadas API = compute desperdiçado, logs ruidosos

### Recomendações
1. **Desabilitar** stale run monitoring do opencode_local até fix de RLA-207
2. **CTO retomar RLA-132** — high priority, stalled 48h+
3. **CEO parar heartbeat wake** se não houver issues — padrão atual é puro desperdício

### Cron Jobs
- `paperclip-log-cleanup`: ✅ Último ran 2026-06-28 02:00 GMT-3
- `backup-paperclip-openclaw`: ✅ Último ran 2026-06-28 06:00 GMT-3
- `paperclip-status-check`: ⏸️ Desabilitado

### Stale Run Detection — Cascade (2026-06-03 → 2026-06-04)
- Run `ee426440` gerou **183+ false positives** (RLA-47 até RLA-183)
- Run `4fe2558e` gerou **60+ false positives** adicionais
- Root cause: opencode_local adapter não verifica `run.status === 'completed'` antes de criar review
- Fix necessário: pré-check no heartbeat/issue services antes de criar RLA review
- RLA-132 atribuída ao CTO, stalled 48h+

### Alert Storm (2026-06-08)
- **25+ wake events** consecutivos (04:50 → 07:25 GMT-3)
- Zero trabalho acionável em cada wake
- Cron `paperclip-status-check` desabilitado

### Backup Script Deleted (2026-06-15)
- `backup-routine.ps1` foi deletado — backup rodou com lógica inline
- pgdata backup stale (último: June 1, 14 dias)
- Recomendação: recriar script de backup

### Documentação
- Criado `DEFINITIONS-IMPROVE\heartbeats-instructions.md` com procedimentos de heartbeat (2026-06-06)

### HEARTBEAT.md Drift (2026-07-19)
- Referência a `scripts/contradiction-check.js` que NÃO existe
- Ou adicionar o script ou remover a referência do step 3

### HEARTBEAT.md Atualização (2026-07-22)
- Última verificação: 2026-07-22 06:30 GMT-3
- Cron jobs: check-free-models-weekly confirmado fix, lastRunStatus=ok (fixed 2026-07-18 03:00)
- Raw sources: 2 arquivos de 2026-07-12 (eclipse-dom-engine-analysis.md, perplexity-comet-analysis.md). Sem novos arquivos.

## Status: RESOLVIDO
- Alert storm parou após RLA-207 estabilizada
- Watchdog corrigido para restart via PM2 (não Scheduled Tasks)
- Heartbeats agora saudáveis (4 cron jobs, zero alert storms)
- Último check: 2026-07-25 06:00 GMT-3 — NORMAL

### Contradiction Check Script Verificado (2026-07-25)
- `scripts/contradiction-check.cjs` existe e substitui a referência quebrada `contradiction-check.js` no HEARTBEAT.md
- Primeiro dry-run: 0 contradições encontradas
- HEARTBEAT.md atualizado com status corrente (PM2 healthy, 3 processos)

## Checkpoint
- `ckpt-2026-06-07` — Tempestade diagnosticada, RLA-207 identificada como root cause
- `ckpt-2026-07-22` — HEARTBEAT.md atualizado, drift note registrada

## Tags
heartbeat, alert-storm, RLA-207, RLA-132, opencode_local, operações, bug, contradiction-check

### Gateway Instability (2026-07-29)
- Gateway: online, PID 29260, 34s uptime, **106 restarts** (↑25 desde último check)
- antigravity-proxy: online, 3D uptime, 23 restarts
- paperclip: online, 7D uptime, 8 restarts
- Contradiction check: 0 found (clean)
- **Instabilidade persiste**: 106 restarts, reciclos frequentes

### HEARTBEAT.md Atualização (2026-07-22)
- Referência a `scripts/contradiction-check.js` que NÃO existe
- Ou adicionar o script ou remover a referência do step 3
- **Resolvido**: contradiction-check.cjs existe e substitui referência quebrada

## Checkpoint
- `ckpt-2026-06-07` — Tempestade diagnosticada, RLA-207 identificada como root cause
- `ckpt-2026-07-22` — HEARTBEAT.md atualizado, drift note registrada

## Tags
heartbeat, alert-storm, RLA-207, RLA-132, opencode_local, operações, bug, contradiction-check, gateway-restarts

## Último checkpoint: 2026-07-29
