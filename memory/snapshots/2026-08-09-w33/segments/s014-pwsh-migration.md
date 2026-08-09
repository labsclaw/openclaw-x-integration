# Segment: s014 — Migração PowerShell 7.6.3

## Resumo
Fix do discovery gap do pwsh no OpenClaw: `resolveShellFromPath()` buscava `pwsh` sem `.exe`, Windows MSIX entrega `pwsh.exe`. Fix local via `gateway-wrapper.js` + PR upstream #104086.

## Conteúdo

### Causa Raiz Provada (2026-07-10 → 2026-07-11)
- `resolvePowerShellPath()` step 3: `resolveShellFromPath("pwsh")` procura `…\pwsh` SEM extensão `.exe`
- Store/MSIX entrega `pwsh.exe` → `fs.accessSync(entry/pwsh)` ENOENT → cai no PS 5.1
- `tools.exec.pathPrepend` é **IGNORADO para `host=node`** (bash-tools-Bvyb7cWG.js:2966 warning)
- Copy sem-ext (`pwsh` puro) NÃO é executável no Windows (testado)

### Fix Local (Admin-free, validada 2026-07-10)
- `C:\Users\ClawLabs\.openclaw\ps7\PowerShell\7\pwsh.exe` — cópia real do pwsh 7.6.3
- `gateway-wrapper.js` seta `process.env.ProgramW6432` = ps7 root antes de spawnar o gateway
- Step 2 da descoberta acha o pwsh real
- `exec` agora roda 7.6.3 (validado: `$PSVersionTable.PSVersion` = 7.6.3, UTF-8/emoji OK)
- Revert: remover a linha ProgramW6432 do wrapper + `pm2 restart`

### PR #104086 (OpenClaw upstream)
- URL: https://github.com/openclaw/openclaw/pull/104086
- Branch: `labsclaw:fix/windows-pwsh-path-discovery` → `openclaw:main`
- Fix: `resolveShellFromPath` agora também testa `.exe` no win32 (pattern já existente em `resolveWindowsBashPath`)
- `.cmd`/`.bat` EXCLUÍDOS de propósito (PTY path spawna shell direto sem `cmd.exe`)
- ClawSweeper review: inicialmente `patch is incorrect` por causa do `.cmd`/`.bat`; corrigido pra só `.exe`
- `gh pr edit --body-file` pode falhar silenciosamente (warning Projects classic aborta mutation). Usar `gh api -X PATCH` direto
- QA Smoke CI: FAIL por infra do upstream (repo `package.json` não tem `packageManager` pin). Independente do patch

### Monitor Ativo
- Cron `pm:pr104086` (id: c1f04c76-cc04-490b-a0c4-fc84dd99358d): roda 09:00 e 21:00 São Paulo
- Silencioso enquanto OPEN; avisa no Telegram e auto-remove quando merged/closed
- Só monitora o #104086 (Dr. Roger pediu "só o nosso")

### MSIX/WindowsApps Alias
- MSIX pwsh alias (WindowsApps) é reparse point: `fs.existsSync` não segue, mas `fs.accessSync` segue
- Mas `resolveShellFromPath` busca sem `.exe`, então step 3 não acha de qualquer forma
- Forwards de outras máquinas (ex: Luna, `C:\Users\Luna`) podem não bater com este host — sempre verificar no disco antes de aplicar

### Lições
- `gh pr edit --body-file` pode falhar silenciosamente (warning Projects classic). Usar `gh api -X PATCH` direto
- `gh run rerun` pode barar em forks ("workflow file may be broken")
- Sempre usar `gh api -X PATCH` em vez de `gh pr edit` quando mutation silenciosa é possível
- `pwsh` puro (sem extensão) não é executável no Windows — precisa ser `.exe`

## Checkpoint
- `ckpt-2026-07-10` — Fix local validado, PR aberto
- `ckpt-2026-07-11` — Monitor cron criado, smoke CI comments

## Tags
powershell, windows, pwsh, migration, fix, upstream, PR-104086, gateway-wrapper, MSIX

## Último checkpoint: 2026-07-11
