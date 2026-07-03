# TOOLS.md - Local Notes

Keep environment-specific notes here.
Do not store shared behavioral rules here.

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

## Rule
This file is a local cheat sheet.
Keep it practical, specific, and environment-bound.
