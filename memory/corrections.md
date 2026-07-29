# Corrections Log

> Last 50 corrections. Promote to segment after 3x pattern.

## Recent

### [2026-07-29] infra: Exec shell não usava PS7 — App Execution Alias, não %ComSpec%

**O que aconteceu:** Comandos com `&&` falhavam. Diagnóstico inicial apontou %ComSpec% como culpado.

**Causa raiz:** `pwsh.exe` existia apenas como App Execution Alias (0 bytes em `WindowsApps\`). O `fs.existsSync()` do Node.js não detecta esses aliases como arquivos reais. O OpenClaw já tenta resolver `pwsh.exe` via `%ProgramFiles%\PowerShell\7\` e PATH, mas o alias falhava silenciosamente.

**Falsa pista corrigida:**
- %ComSpec% NÃO controla o `exec` tool do OpenClaw (ignorado pelo código)
- `resolvePowerShellPath()` já busca `pwsh.exe` — o bug era o alias virtual não ser detectado

**Correção:** Instalar PS7 MSI real no `%ProgramFiles%\PowerShell\7\pwsh.exe`. OpenClaw detectou automaticamente. Zero patch necessário.

**Lições:**
1. App Execution Aliases do Windows (0 bytes em `WindowsApps\`) não são detectáveis por `fs.existsSync()`
2. Sempre verificar se um executável é real vs alias virtual antes de culpar o código que o procura
3. Ao debuggar falha de execução, testar o caminho de resolução manualmente antes de assumir que o código está errado

### [2026-07-22] behavior: Dúvida técnica → spawnar Opus como consultor
- **O que aconteceu:** Dr. Roger me corrigiu: quando tiver dúvida técnica, deveria spawnar Opus como seção técnica pra decidir a melhor solução, e depois relatar.
- **Liçao:** Justus orquestra, Opus deep-dives. Não tentar resolver tudo sozinho quando existe um modelo melhor pro trabalho.
- **Ação:** Adicionado em SOUL.md (Technical Consultation Protocol) e AGENTS.md (Delegation rules).

### [2026-07-22] tool-misuse: Hardcoded paths in multi-env scripts
- **O que aconteceu:** Subi 5 scripts .cjs com path hardcoded `C:\Users\ClawLabs\.openclaw\workspace`.
- **Causa raiz:** Não verifiquei se o path era específico do meu ambiente antes de commitar.
- **Resolução:** Substituí todos os hardcoded paths por `findWorkspace()` com auto-detection + env var `OPENCLAW_WORKSPACE`.
- **Liçao:** NUNCA commitar paths absolutos específicos de um ambiente quando o código vai para repo compartilhado.

### [2026-07-22] tool-misuse: Push para branch errada do GitHub
- **O que aconteceu:** Push para `feat/crag-ssc-router` em vez de `master`.
- **Liçao:** Confirmar qual branch é a default/visível antes de push. Para release, ir para `master`.

### [2026-07-23] process-violation: Spawn sem monitoramento (Opus estourou cota)
- **O que aconteceu:** Spawnei Opus sem criar pipeline ou watchdog. Falhou silenciosamente.
- **Resolução:** Implementei Pre-Spawn Gate em AGENTS.md como fonte única.
- **Liçao:** AGENTS.md é dono da regra. SOUL.md e TOOLS.md referenciam ele.
