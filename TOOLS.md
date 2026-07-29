# TOOLS.md - Local Notes

Keep environment-specific notes here.
Do not store shared behavioral rules here.

## Environment
- **OS:** Windows 11 Pro (22H2/23H2)
- **Shell:** PowerShell 5.1 + PowerShell 7 (pwsh)
- **Node:** v26.1.0
- **Package Manager:** npm + pnpm
- **Git:** Git for Windows
- **GitHub CLI:** gh (authenticated)
- **Runtime:** OpenClaw Gateway on PM2

> **Shell: PowerShell 7 (pwsh 7.6.4)** instalado em `%ProgramFiles%\PowerShell\7\pwsh.exe`. O OpenClaw `exec` tool detecta automaticamente. Operadores tipo `&&` funcionam.
> ⚠️ **Python on Windows uses cp1252 by default.** Always set `$env:PYTHONIOENCODING = "utf-8"` before running Python scripts that handle Unicode (PDFs, international text, etc). 
> **Global fix (already applied):** `PYTHONIOENCODING=utf-8` + `PYTHONUTF8=1` set as user env vars. New Python processes pick these up automatically.

## What belongs here
- local hosts
- SSH aliases
- device names
- camera names
- preferred voices
- local scripts
- environment-specific shortcuts

## Network Services

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| OpenClaw Gateway | 18789 | `http://127.0.0.1:18789` | API Messaging & Telegram Integration |
| Paperclip Server | 3100 | `http://127.0.0.1:3100` | Agent Orchestration Engine |
| Antigravity Proxy | 8080 | `http://127.0.0.1:8080` | Model API Routing & Proxying |

## Common Commands

- **Restart Gateway:** `pm2 restart openclaw-gateway`
- **View Gateway Logs:** `pm2 logs openclaw-gateway`
- **Compare Config:** `powershell -File ultra-models-skill/scripts/compare-config.ps1`
- **Backup Workspace:** `powershell -File backup-routine.ps1`
- **Check Active Processes:** `node check-active.mjs`
- **Test Browser (Camofox):** `node test-camofox.mjs`
- **Check Webhook State:** `node check-webhook.mjs`

## PowerShell ↔ Linux Equivalents
| Linux | PowerShell |
|-------|------------|
| `head -n 20` | `Select-Object -First 20` |
| `tail -n 20` | `Select-Object -Last 20` |
| `cat file` | `Get-Content file` |
| `grep pattern` | `Select-String pattern` |
| `wc -l` | `(Get-Content file).Count` |
| `base64 -d` | `[Convert]::FromBase64String()` |
| `base64 -w0` | `[Convert]::ToBase64String()` |

## gh CLI no PowerShell
- **NUNCA** usar `--body "string"` direto — o PowerShell quebra aspas internas
- **SEMPRE** usar `--body-file path` com caminho ABSOLUTO sem til (~)
- Usar `Join-Path` ou caminhos com `/` em vez de `\` quando possível
- Pra strings multi-linha, escrever em arquivo temporário e usar `--body-file`
- Exemplo correto: `gh pr create --body-file C:/Users/ClawLabs/.openclaw/workspace/temp-body.md`
- Exemplo ERRADO: `gh pr create --body "texto com aspas"`

## Platform formatting
- Discord / WhatsApp: do not use markdown tables
- Discord: wrap multiple links in `<>` to suppress embeds
- WhatsApp: prefer short plain formatting over headers

## Repos
- Skills repo: `https://github.com/labsclaw/openclaw-skills`
- Workspace repo: `https://github.com/labsclaw/openclaw-x-integration`
- Instructions repo: `https://github.com/labsclaw/openclaw-instructions`

## Useful scripts
- `ultra-models-skill/scripts/list-free-models.ps1`
- `ultra-models-skill/scripts/compare-config.ps1`
- `scripts/pipeline-monitor.cjs` — pipeline status + zombie detection
- `scripts/long-task-watchdog.js` — single-shot watchdog
- `scripts/task-done.js` — mark task complete for watchdog

## Pipeline Monitoring Protocol

Regra definitiva em **`AGENTS.md` → Pre-Spawn Gate**. Tudo que preciso saber sobre monitoramento de sub-agentes está lá.

**TOOLS.md mantém só os comandos shell de referência:**

| Ação | Comando |
|------|---------|
| Pipeline status | `scripts/pipeline-monitor.cjs` |
| Watchdog | `scripts/long-task-watchdog.js` |
| Task done | `scripts/task-done.js` |

## Rule
This file is a local cheat sheet.
Keep it practical, specific, and environment-bound.
