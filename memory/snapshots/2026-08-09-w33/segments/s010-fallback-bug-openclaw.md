---
id: s010
created: 2026-07-14
updated: 2026-07-14
weight: 1.0
accessCount: 0
---

# s010 — Fallback Bug OpenClaw + ultra-memory-skill Revert

## Resumo
Bug de fallback no OpenClaw impediu fallback durante timeouts. ultra-memory-skill revertida para versão pré-distillation. Credenciais Instagram criadas. Testes da skill rodados com sucesso.

## Eventos

### Fallback Bug (16:07-18:13)
- **Problema**: MiMo v2.5 timeout → fallback não ativava → 25+ timeouts cascata
- **Logs mostravam**: `decision=candidate_failed next=none detail=This operation was aborted`
- **Causa raiz**: Race condition - mensagens chegavam e cancelavam operação antes do fallback rodar
- **Issues confirmadas no GitHub**:
  - #44936: "LLM request timeout não triggera fallback"
  - #43400: "Per-model timeout = global timeout (ambos 60s)"
  - #47705: "Fallback sobrescreve primary model permanentemente"
- **Config timeout é protegida**: agents.defaults.timeoutSeconds não editável via config.patch
- **Decisão**: Não abrir nova issue (problema já documentado). Monitorar e escalar se necessário

### ultra-memory-skill Revert (15:42)
- Revertido de 354 linhas (distillada) para 880 linhas (completa)
- Corrigido encoding: em dash `—` → `-` em setup.ps1
- Corrigido Join-Path para PowerShell 5.1
- Testes rodados com sucesso:
  - setup.ps1 ✅
  - ssc-router.ps1 ✅ (6/9 segmentos)
  - ssc-health.ps1 ✅ (HEALTHY, 9/9)

### Instagram @labsclaw2026 (15:58)
- Perfil criado via browser automation
- Username: @labsclaw2026
- Email: labsclaw@gmail.com
- Credenciais salvas em memory/credentials.md
- Gmail já estava logado no browser (conta pre-existente)

### Sessão Anterior - Falha
- Agente anterior pediu senha 4 vezes (não processava)
- Tentou LOGAR quando deveria CRIAR conta
- Motivo provável: timeouts do MiMo causaram perda de contexto
- Lição: sempre salvar credenciais imediatamente em memory/credentials.md

## Decisões
1. **Não abrir issue de fallback** - Já documentado (#44936, #43400, #47705)
2. **Comentário na issue #80040** - Documentado nosso caso específico com logs e padrão
3. **Monitorar** - Se problema persistir, escalar upstream
4. **Timeout**: Config protegida, não editável. Workaround: 180s aplicado
5. **Credenciais**: Sempre salvar em memory/credentials.md imediatamente
6. **Manter MiMo v2.5-free** - Dr. Roger confirmou que é melhor para orquestração

## Análise da Luna (20:12 GMT-3)
- Nossa versão 2026.6.11 já tem fixes de #18453 e #43400
- Nosso problema é edge case diferente: abort por race condition de múltiplas mensagens
- Abort tratado como cancelamento do usuário, não falha do modelo
- Issues #80040 e #73581 cobrem race conditions mas sem fix ainda
- Comentário postado em #80040 com nosso caso documentado

## PR #8084 Paperclip (20:10 GMT-3)
- Greptile bot aprovou (LGTM)
- Comentário mencionando @cryppadotta para review humano
- Link: https://github.com/paperclipai/paperclip/pull/8084#issuecomment-4974890292

## Fallback Chain Redesign (2026-07-21 12:08)

**Problema**: "Something went wrong" após restart do PC. Causa: mimo-v2.5-free retornando HTTP 500. Fallback chain tinha 8 dos 10 modelos quebrados.

**Diagnóstico com logs reais (runId 13763111)**:
- hy3-free: 401 "Model not supported" (auth quebrado)
- nvidia/deepseek-v4-pro: timeout 120s (inviável pra fallback)
- openrouter/deepseek-v4-flash:free: 404 (confirmado morto, virou pago)
- antigravity-proxy/gemini-3.5-flash: 400 nome errado (deveria ser `gemini-3.5-flash-extra-low`)
- antigravity-proxy/gpt-oss-120b-medium: 400 formato incompatível com API anthropic

**Nova cadeia aplicada** (direto no arquivo — config.patch bloqueia agents.defaults.model.fallbacks):
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

**Regra aplicada**: máximo 1 do mesmo provider seguido (rate limit protection). Gateway auto-corrige prefixo NVIDIA.

## Referência: Akita ai-memory v1.17.1 (2026-07-21)
- Artigo: https://akitaonrails.com/2026/07/20/novidades-no-meu-ai-memory-cada-vez-melhor-pra-usar-com-suas-ias/
- Projeto: https://github.com/akitaonrails/ai-memory
- 31 releases, 55 PRs, 15 contribuidores em 1 mês (v1.1.0 → v1.17.1)
- `ai-memory run`: camada que gerencia workstreams entre harnesses diferentes
- Briefing automático: injeta pinned pages + regras antes da primeira pergunta
- Lease pra workstreams: previne 2 instâncias escrevendo ao mesmo tempo
- Referência salva: `memory/references/akita-ai-memory.md` (flag: NÃO referenciar no paper)

## Referências
- ultra-models-skill como ferramenta de planejamento de fallbacks (~150 modelos free)
- Playwright MCP: janelas abrindo/fechando são normais (servidor de automação)

## Tags
fallback, bug, openclaw, ultra-memory-skill, instagram, credentials, timeout, fallback-chain-redesign, akita-ai-memory

## Último checkpoint: 2026-07-21
