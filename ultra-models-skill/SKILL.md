# Ultra Models Skill

Monitora, compara e mantém modelos free de todos os provedores (OpenRouter, OpenCode, KiloCode, NVIDIA) em dia com a config do OpenClaw.

## Quando usar

- Auditoria periódica de modelos free disponíveis
- Verificar se modelos no config ainda existem nas APIs
- Descobrir novos modelos free worth adding
- Diagnosticar fallbacks quebrados silenciosamente

## Scripts

### list-free-models.ps1
Lista todos os modelos free de cada provedor consultando as APIs diretamente.
```powershell
powershell -ExecutionPolicy Bypass -File "ultra-models-skill/scripts/list-free-models.ps1"
```

### kilo-free-detail.ps1
Detalhes expandidos dos modelos free do KiloCode (nome, owner, descrição).
```powershell
powershell -ExecutionPolicy Bypass -File "ultra-models-skill/scripts/kilo-free-detail.ps1"
```

### compare-config.ps1
Cruza o que a API retorna com o que está no `openclaw.json` — identifica modelos mortos, novos e aliases órfãos.
```powershell
powershell -ExecutionPolicy Bypass -File "ultra-models-skill/scripts/compare-config.ps1"
```

## Requisitos

- Chaves no `.env`: `OPENROUTER_API_KEY`, `OPENCODE_API_KEY`, `KILOCODE_API_KEY`, `NVIDIA_API_KEY`
- PowerShell 5.1+ (Windows)

## Workflow recomendado

1. Rodar `list-free-models.ps1` pra ver o panorama atual
2. Rodar `compare-config.ps1` pra ver gaps entre API e config
3. Decidir se quer adicionar/remover/renomear modelos
4. Atualizar `openclaw.json` manualmente ou via agent
5. Reiniciar gateway

## Notas

- Os scripts são **read-only** — nunca modificam o config automaticamente
- Modelos mudam sem aviso (renomeados, removidos, adicionados)
- Preferir sempre testar um modelo novo com chamada direta antes de adicionar aos fallbacks
- O OpenCode pode renomear modelos (ex: `super` → `ultra`) sem manter compatibilidade
