# Segment: s004 — Skills e Projetos

## Resumo
Skills construídas: Telegram, Ultra Find, Ultra Create. Projetos em andamento.

## Conteúdo

### Diretiva Permanente: Continuous Improvement Pipeline (2026-08-08)
Dr. Roger estabeleceu como regra de operação:
> Sempre que encontrarmos um repositório, paper, ou post relevante que tenha algo a contribuir com a melhoria do nosso sistema, planejamos a implementação/adoção dessa melhoria e documentamos a nossa evolução.

Fluxo: encontrar → documentar no repo `labsclaw/agentic-ai-maturity` → planejar implementação → documentar evolução (o que adotamos, adaptamos, descartamos).

Fontes aplicáveis: repo open-source, paper acadêmico, blog post, release de ferramenta, benchmark, análise de concorrente.

### Telegram Skill (2026-06-06)
- Skills estudadas: awrshift/skill-telegram, NousResearch/hermes-agent
- Arquivos criados: SKILL.md, package.json, tg_setup.js, tg_read.js, tg_fetch_channels.js
- Canal configurado: `-1003990750529` com `requireMention: false`
- Grupo: `-1004226997838` (Founders e CEOs)

### Lição Aprendida
- **Não inventar usernames** — inventei @robin_nascimento aleatoriamente em vez de perguntar o real (@RobinBRIAbot)
- Telegram channels precisam do bot como admin (não apenas inscrito)

### Ultra Skills - Naming Convention (OBRIGATÓRIO)
- **Local:** `openclaw-skills/` (não `skills/`)
- **Pattern:** `ultra-<nome>-skill` (prefixo `ultra-`, sufixo `-skill`)
- **Formato:** kebab-case
- **Exemplos:** `ultra-chrome-stealth-navigator-skill`, `ultra-browser-stealth-timing-skill`, `ultra-x-stealth-skill`
- **NUNCA criar skill sem o prefixo/sufixo ou na pasta errada**

### Ultra Skills - Pattern Inspiration (2026-06-07)
- **ultra-create-skill** ✅ — Template engine + validação + Python scripts
- **ultra-find-skill** ✅ — Busca híbrida com 3 scripts funcionais
  - `search_catalog.py` — Busca no catálogo antigravity (1520 skills)
  - `find_local_skills.py` — Skills locais instaladas
  - `rank_matches.py` — Ranqueamento híbrido local/catalog
- Status: Material adicional pendente para conclusão

### Identidade
- Justus — amigo, CEO, sharp 🥇
- Nota telegram 2026-06-06: "Humano Digital" no grupo "Founders e CEOs"

## Checkpoint
- `ckpt-2026-06-06` — Telegram skill implementada
- `ckpt-2026-06-07` — Ultra skills parcialmente concluídas

## X/Twitter
- Perfil: @LabsClawAgent (https://x.com/LabsClawAgent)\- Conta: Labs Claw DEV
- Primeira thread postada: 2026-06-13 (Memory Caching paper)
- Postar via browser (login ativo no OpenClaw browser profile)

### Antigravity Proxy — PR #354 (2026-06-16)
- Repo: `badrisnarayanan/antigravity-claude-proxy`
- URL: https://github.com/badrisnarayanan/antigravity-claude-proxy/pull/354
- Title: feat: add GPT-OSS model family support
- Estado: **OPEN** — sem reviews ainda
- O que faz: adiciona `gpt-oss` como família de modelo reconhecida (antes só Claude/Gemini)
- Commit: c14b147 (1 commit limpo)
- **ACOMPANHAR**: pingar maintainer se não responder até 2026-06-30

### Paperclip — PR #7710 (2026-06-07)
- Repo: `paperclipai/paperclip`
- URL: https://github.com/paperclipai/paperclip/pull/7710
- Title: feat: add antigravity local adapter for paperclip
- Estado: **OPEN** — 9 commits, review Greptile comentou
- O que faz: adapter `antigravity_local` para Paperclip.spawn agy como subprocess
- **ACOMPANHAR**: CI pode ter passado, checar status

### Perplexity Pro Bridge Skill (2026-05-22)
- Skill criada em `skills/perplexity-pro-bridge/SKILL.md`
- Workflow completo para browser tool com Perplexity AI
- Modelos mapeados: Sonar 2, GPT-5.4, GPT-5.5 Max, Gemini 3.1 Pro, Claude Sonnet 4.6, Claude Opus 4.7 Max, Kimi K2.6, Nemotron 3 Super
- Browser tool 100% funcional no profile `openclaw`

### Browser Config Instructions (2026-05-22)
- Usar `profile="user"` para cookies/logins do usuário
- Fluxo: navegar → snapshot → agir → snapshot (nunca blind waits)
- Gerenciamento de abas: listar existentes antes de abrir nova, reutilizar por label
- Bloqueios (login/2FA): pausar e informar ao usuário

### Ultra-Models-Skill v2 (2026-07-14)
- Sistema de alocação inteligente por capability map (inspirado GPT 5.6)
- Scripts: `_shared.ps1`, `sync-config.ps1`, `build-model-map.ps1`, `plan-routing.ps1`, `report-final.ps1`
- 142 modelos canonicos, 11 capacidades por modelo, 10 papeis de agente
- Fallback de 3 niveis + circuit breaker + diversidade de familia

### Chrome-Stealth & DOM Engine Skills (2026-07-12)
- `ultra-chrome-stealth-navigator-skill` — browser stealth via CDP attach
- `ultra-browser-stealth-timing-skill` — timing comportamental
- `ultra-dom-engine-skill` — dom-engine auto-contido (inject-dom-engine.js)
- Referências: Perplexity Comet system prompt, Eclipse (alternativa open-source)

### Incidente: Skills fora do local padrão (2026-07-20)
- Dr. Roger compartilhou posts do X sobre Kimi K3 e pediu pra usar nossas skills
- FALHEI: não usei ultra-find-skill, li skills erradas (stealth/chrome-assistente)
- Fui direto pro browser manual com evaluate, multiple passes, erros de snapshot
- **Correção**: repo `labsclaw/openclaw-skills` tem 12 skills não instaladas localmente
- `ultra-browser-skill` estava numa subpasta `skills/` do repo
- Sincronizadas 10 skills do repo → `~/.openclaw/skills/`
- **Lição**: SEMPRE usar ultra-find-skill antes de decidir qual skill usar

### Autoevolução — Princípio Estabelecido (2026-07-20)
- Dr. Roger: autoevolução é FUNDAMENTAL, não opcional
- Toda sessão deve potencialmente melhorar skills, memória, conhecimento
- Knowledge adquirido → site-memory, modules, SKILL.md
- Padrões aprendidos → observe-act cache
- Correções → skill updates imediatas

### Rigor Pack Analysis (2026-07-09)
- Baixou e analisou "Iwo's Rigor Pack" — 6 skills testadas em Claude Opus 4.8
- Resultado: 12 wins, 0 losses, 2 ties
- Skills: plan-gate, adversarial-verify, live-state-truth, scope-fence, ruthless-editor, memory-hygiene
- Key insight: skills movem modelos de "lazy mode" pra "careful mode" — ~7% overhead de tokens
- v1 de adversarial-verify e live-state-truth FALHARAM — narraram processo no deliverable
- v3 fixou: "findings in the deliverable, never the narration"
- FENCE REPORT template é o maior takeaway prático
- Benchmarks mostram skills NÃO ajudam em tarefas simples (Opus já pega bugs sem ajuda)

### Skills Repo Updates (2026-07-09)
- Criadas 6 novas entries `ultra-*-skill` derivadas do Rigor Pack
- Renomeadas `ultra-confluence-docs` → `ultra-confluence-docs-skill` (padrão)
- Aplicadas lições de benchmark em 7 skills ativas
- Total: 19 skills no repo openclaw-skills

### Free Models Script Fix (2026-07-09)
- Robin reportou MiniMax M3 no NVIDIA NIM — script não capturava
- Root cause: filtrava só `owned_by: "nvidia"`, perdia free de terceiros
- Fix: agora captura qualquer model sem pricing ou pricing=0
- Resultado: 45 → 121 free models no NVIDIA NIM
- MiniMax M3 confirmado no NIM, NÃO no OpenCode Zen
- Configurado `minimaxai/minimax-m3` no gateway (nvidia provider, 196K ctx)

### Weekly Free Models Cron (2026-07-09)
- `check-free-models-weekly` — Sábados 03:00 São Paulo, announce no Telegram
- Roda `list-free-models.ps1` e resume novos modelos
- Fix 2026-07-18: adicionado `to: telegram:908406251` (faltava delivery target)

### Skill Distillation Pipeline (2026-07-09)
- Objetivo: destilar SKILL.md grandes em referências concisas usando DeepSeek V4 Pro + MiniMax M3
- 9 skills distilladas (redução de 5% a 68%)
- MiniMax M3: melhor estrutura (seções por função, Anti-Patterns, Verification Checklist)
- DeepSeek: bom conteúdo mas headers garbled em algumas saídas
- Merge strategy: MiniMax M3 como base + peças únicas do DeepSeek
- Paralelo com sub-agents bateu RPS limits — 1-2 simultâneos é mais seguro

### Compare-Free-Models Script v2 (2026-07-10)
- PR: https://github.com/labsclaw/openclaw-skills/pull/4 (merged)
- Location: `ultra-models-skill/scripts/compare-free-models.ps1`
- Detecção dinâmica do OpenClaw home, API OpenRouter (não HTML parsing), `-Ping`, `-Json`
- Report: 37 free models em 6 providers, 6 REMOVIDOS, 28 NEW free disponíveis
- Pendente: Dr. Roger não decidiu limpar orphans ou adicionar novos free

### Hy3 Free Integration (2026-07-10)
- Tencent Hy3: 295B MoE (21B active), 256K ctx, Apache 2.0, reasoning configurável
- Benchmarks: SWE-Bench Verified 78.0, GPQA Diamond 90.4, Terminal-Bench 2.1 71.7
- OpenRouter free rank: #1 Python (13.6%), #2 tool calls (9.6%), #2 NL (11.7%)
- Adicionado como 1st fallback após mimo no openclaw.json
- Availability: `opencode/hy3-free` (permanent free) + `tencent/hy3:free` OpenRouter (expira 21 Jul)

### OpenCode Monitoring Tutorial (2026-07-10)
- Tutorial de Dr. Roger: monitorar mudanças no OpenCode CLI (headers, baseUrl, Mitmproxy)
- Salvo em `docs/opencode-monitoring-tutorial.md`

## Tags
skills, telegram, ultra-skills, projetos, identidade, X, Twitter, antigravity, PRs-abertos, perplexity, browser, stealth, models, autoevolução, rigor-pack, distillation, free-models, hy3

## Último checkpoint: 2026-07-20
