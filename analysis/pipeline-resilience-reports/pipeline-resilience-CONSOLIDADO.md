# RELATÓRIO CONSOLIDADO: Pipeline Resilience & Anti-Session-Crash

**Versão:** 3.1 (Consolidação Final — Robin + Sonnet 5 + Gemini PRO)  
**Data:** 2026-07-02  
**Status:** COMPLETO  
**Autores:** Robin (Bando) + Claude Sonnet 5 + Gemini PRO

---

## PARTE 1: RELATÓRIO TÉCNICO

---

### 1. RESUMO EXECUTIVO

Implementar sistema de **pipeline resilience** para OpenClaw que garante:
1. Tarefas longas sobrevivem a crashes de sessão
2. Progresso é persistido em disco com contexto comprimido
3. Retomada automática via "hydration" do estado
4. Monitoramento proativo com proteção contra zumbis

**Não é gambiarra.** É checkpointing — padrão canônico de sistemas distribuídos.

---

### 2. DIAGNÓSTICO CONSOLIDADO

#### 2.1 O que cada consultoria identificou

| Aspecto | Robin (original) | Sonnet 5 (correções) | Gemini PRO (amadurecimento) |
|---------|-------------------|----------------------|----------------------------|
| **Abordagem** | 4 mecanismos nativos | Correções técnicas precisas | Elevação para padrão arquitetural |
| **State files** | Nice-to-have | Necessário (único caminho) | **Handoff protocol** — compressão de contexto |
| **Sub-agents** | Delegação básica | Bug #24852 (sem SOUL.md) | **Monitoramento de zumbis** + timeout |
| **Goals** | 1 por módulo ❌ | 1 guarda-chuva ✅ | **Wrapper automático** (não manual) |
| **update_plan** | Uso livre | Experimental (config) | State file como alternativa robusta |
| **Principal falha** | "Não usamos consistentemente" | Detalhes técnicos faltando | **Falta de dimensionamento** pelo timeout da API |

#### 2.2 Correções Críticas Acumuladas

**🔴 Sem essas correções, a skill falha silenciosamente:**

1. **1 goal apenas por sessão** — progresso dos steps vai no state file, não no goal
2. **Bug #24852** — sub-agents NÃO recebem SOUL.md/IDENTITY.md → usar attachAs com .md escopados
3. **update_plan é experimental** — precisa habilitar `tools.experimental.planTool`
4. **Goal só aceita `complete`/`blocked`** — sem status intermediários
5. **Leaf sub-agents não recebem session tools** — não podem spawnar próprios sub-agents
6. **Dimensionamento pelo timeout da API** — cada step deve caber no timeout do provider

---

### 3. ARQUITETURA FINAL

#### 3.1 O Protocolo de "Handoff" (Gemini PRO)

> "Quem termina o trabalho, prepara o resumo para o próximo."

A chave não é salvar o output bruto — é criar um **resumo de handoff** comprimido que contenha apenas:
- O que foi feito (1-2 linhas)
- O que precisa ser feito next (1-2 linhas)
- Dados essenciais para continuidade (máximo 500 tokens)

#### 3.2 Arquitetura Completa

```
┌──────────────────────────────────────────────────────────────────┐
│                      SESSÃO PRINCIPAL                            │
│                                                                   │
│  1. Verificar state file → RETOMAR ou INICIAR NOVA               │
│  2. create_goal(1 guarda-chuva) + write state file               │
│  3. Para cada step:                                              │
│     a. Ler state → próximo pending                               │
│     b. Atualizar → "running"                                     │
│     c. Comprimir contexto do step anterior                       │
│     d. sessions_spawn(task=handoff) + attachments (rules)        │
│     e. sessions_yield (sem poll loop)                            │
│     f. Receber completion event                                  │
│     g. Atualizar state file com handoff_payload                  │
│  4. Se todos done → update_goal(complete) + limpar               │
│                                                                   │
│  MONITOR: Cron (10 min) detecta zumbis → retry 3x               │
│  RETOMADA: Heartbeat → hydration (~500 tokens)                   │
└──────────────────────────────────────────────────────────────────┘
```

---

### 4. STATE FILE — ESPECIFICAÇÃO TÉCNICA

#### 4.1 Schema Completo

```json
{
    "id": "pipeline-<unique-id>",
    "name": "Descrição da Pipeline",
    "version": "1.0",
    "startedAt": "ISO-8601",
    "goalId": "<id-do-goal>",
    "status": "running|completed|failed",
    "steps": [
        {
            "name": "step-name",
            "status": "pending|running|completed|failed",
            "file": "path/to/output.py",
            "testFile": "path/to/test.py",
            "subAgent": {
                "sessionKey": "<childSessionKey>",
                "runId": "<runId>",
                "startedAt": "ISO-8601",
                "timeout": 300
            },
            "handoff": {
                "summary": "Resumo do que foi feito (max 200 tokens)",
                "outputPath": "path/to/output",
                "nextSteps": "O que o próximo deve fazer (max 100 tokens)",
                "context": "Dados essenciais (max 200 tokens)",
                "tokenCount": 450
            },
            "retries": 0,
            "maxRetries": 3,
            "startedAt": "ISO-8601",
            "completedAt": "ISO-8601",
            "error": null
        }
    ],
    "lastCheck": "ISO-8601",
    "alerts": 0
}
```

#### 4.2 Regras de Compressão (Gemini PRO)

| Dado | Antes (errado) | Depois (correto) |
|------|----------------|------------------|
| Output do módulo | Salvar .py inteiro | APENAS path + resumo (3 linhas) |
| Erros | Stack trace completo | Mensagem + causa raiz (1 linha) |
| Testes | Output completo do pytest | "237/237 passed" |
| Contexto | Tudo que o agente pensou | Decisões que afetam o próximo step |

**Regra de ouro:** Se o próximo step não precisa do dado, NÃO salve no handoff.

#### 4.3 Exemplo de Handoff Payload

```json
{
    "completed_summary": "BinomialTree implementado. CRR 200 steps. American/European. Greeks via bump-and-reprice. 26 testes passando.",
    "output_file": "crew/quantmind/tools/binomial_tree.py",
    "critical_vars": {
        "_valuation()": "Método interno sem Greeks (evita recursão)",
        "DiscreteDividend": "dataclass para dividendos discretos"
    },
    "design_decisions": [
        "_valuation() separado de price() para que _compute_greeks() não recurse",
        "Dividendos Europeanos: subtrai PV do spot inicial"
    ],
    "next_step_instructions": "Implementar black76.py — Black-76 para futures. Seguir padrão de options_pricing.py."
}
```

---

### 5. DIMENSIONAMENTO PELO TIMEOUT DA API

| Provider | Timeout típico | Max step | Ação se exceder |
|----------|----------------|----------|-----------------|
| OpenCode (big-pickle) | ~5 min | 3.5 min | Decompor em sub-steps |
| NVIDIA NIM (MiniMax M3) | ~30s connect | Variável | Monitorar de perto |
| OpenRouter (fallback) | ~10 min | 7 min | Mais folga |

**Regra:** `TEMPO MÁXIMO POR STEP = Timeout × 0.7`

---

### 6. PROTEÇÃO CONTRA ZUMBIS

```python
# Cron monitor detecta:
if step["status"] == "running" and elapsed > timeout * 1.5:
    # ZUMBI → marcar failed → retry (max 3x) → alertar Olliver
```

| Contexto | Timeout | Retry | Ação |
|----------|---------|-------|------|
| Sub-agent | 5 min | 3x | Re-spawn |
| Cron check | 10 min | 1x | Alertar |
| Sessão principal | 15 min | 0 | Cron detecta |

---

### 7. WRAPPER AUTOMÁTICO

A skill detecta automaticamente tarefas que precisam de resilience:
- > 2 passos
- > 5 minutos estimados
- Keywords: "implementar", "pipeline", "módulo"

Trigger → cria goal + state file + cron automaticamente.

---

### 8. PROTOCOLO DE RETOMADA (HYDRATION)

```
Você é um agente retomando pipeline interrompida.

Objetivo Global: {global_goal}

Passos concluídos:
1. {step1.completed_summary}
   Arquivo: {step1.output_file}

Sua tarefa IMEDIATA: Executar Step {current_step_index} - {step_name}

{handoff_payload.current_step_instructions}

Inicie trabalho a partir das informações acima.
```

**Total:** ~400-500 tokens. Nunca histórico completo.

---

### 9. CHECKLIST DE IMPLEMENTAÇÃO

**Pré-requisitos:**
- [ ] Verificar `tools.experimental.planTool`
- [ ] Criar `memory/pipelines/`
- [ ] Testar sessions_spawn + sessions_yield
- [ ] Verificar timeout do provider

**Implementação:**
- [ ] Criar `skills/pipeline-resilience/SKILL.md`
- [ ] Schema do state file
- [ ] Lógica de handoff (compressão)
- [ ] Wrapper automático
- [ ] Monitor de zumbis (cron)
- [ ] Protocolo de retomada
- [ ] Testar com pipeline real
- [ ] Testar crash simulado

---

### 10. CENÁRIOS E2E

**Execução Normal:** 3 steps → spawn sequencial → completion events → goal complete → cleanup

**Crash + Retomada:** Sessão cai → heartbeat detecta state file → identifica pendente → re-spawn → continua

**Sub-agent Falha:** Completion com erro → alerta → retry (max 3x) → sucesso ou escalate

---

### 11. MÉTRICAS

| Métrica | Target |
|---------|--------|
| Retomada bem-sucedida | 100% |
| Tempo de retomada | < 30s |
| Perda de trabalho | 0% |
| Handoff payload | < 500 tokens |
| Zumbis detectados | 100% |

---

### 12. RISCOS

| Risco | Gravidade | Mitigação |
|-------|-----------|-----------|
| Bug #24852 (sem SOUL.md) | **Alta** | attachAs com .md escopados |
| 1 goal apenas | **Alta** | State file pra progresso |
| update_plan experimental | **Média** | State file como fallback |
| Handoff muito grande | **Média** | Limite de 500 tokens |
| Provider timeout | **Média** | Margem de 30% |
| State file corrompido | **Baixa** | Atomicidade (.tmp → rename) |

---

### 13. ESCOLHA: JSON > SQLite

| Critério | JSON | SQLite |
|----------|------|--------|
| Compatibilidade nativa | ✅ write/read/edit | ❌ exec + python |
| Atomicidade | ✅ oldText/newText | ✅ transactions |
| Debuggability | ✅ cat state.json | ❌ query |
| Portabilidade | ✅ viaja com workspace | ❌ path + conexao |
| Complexidade | ✅ zero setup | ❌ migrations |

**Decisão:** JSON estático + handoff comprimido.

---

### 14. TIERING DE MODELS

| Função | Modelo | Tier |
|--------|--------|------|
| Cron monitor | big-pickle | 2 (rápido) |
| Recovery prompt | big-pickle | 2 (rápido) |
| Execução do step | mimo-v2.5 | 1 (forte) |

---

### 15. PRÓXIMOS PASSOS

1. ✅ Relatório consolidado
2. ✅ Respostas integradas
3. ✅ memory/rules/ criado
4. ✅ AGENTS.md atualizado
5. ⏳ Aprovação para implementar skill
6. ⏳ Criar SKILL.md
7. ⏳ Testar com pipeline real
8. ⏳ Documentar para replicação

---

## PARTE 2: RESPOSTAS ORIGINAIS DO GEMINI PRO

---

### Resposta 1: Persistência (JSON vs SQLite)

A análise do "Robin" foi cirúrgica. Interrupções por _timeout_ em sessões _stateless_ são, de fato, o calcanhar de Aquiles na orquestração de agentes autônomos complexos.

Respondendo diretamente à proposta: **Sim, a criação dessa skill de _pipeline resilience_ é uma excelente decisão arquitetural.**

Inclusive, discordo da avaliação final do Robin: **isso não é uma "gambiarra"**. Implementar persistência de estado (_Checkpointing_) aliada à delegação assíncrona para _sub-agents_ é um padrão de design canônico e essencial para sistemas distribuídos robustos.

**4 Pontos Críticos:**

1. **Dimensionamento Visando o Setup dos Modelos** — os _steps_ precisam ser dimensionados para que a execução de cada nó ocorra dentro do limite de tempo de resposta da API, evitando que o corte ocorra antes da escrita do _checkpoint_ no disco.

2. **Payload do Arquivo de Estado** — registrar apenas "completed" não é suficiente. O arquivo precisa armazenar o _output_ consolidado e o contexto estritamente necessário para o próximo passo.

3. **Monitoramento de Sub-agents ("Zumbis")** — se o sub-agente sofrer falha fatal e nunca emitir completion event, a sessão principal fica aguardando indefinidamente. A skill precisa de timeout + retry.

4. **Execução Transparente (Wrapper)** — a skill deve atuar como um _wrapper_ automático. Se a tarefa passar de X etapas, força criação de Goal + Plan + state file.

**Pergunta central:** Como estruturar a injeção do payload de recuperação garantindo que a nova sessão retome do ponto de interrupção sem comprometer a janela de contexto?

**Arquitetura em 4 Fases:**

- **Fase 1:** Protocolo de Handoff (compressão na saída) — "quem termina, prepara o resumo para o próximo"
- **Fase 2:** State File como "cérebro pausado" com handoff_payload
- **Fase 3:** Recovery Boot — prompt dinâmico de reanimação (~400 tokens)
- **Fase 4:** Tiering via openclaw.json — modelos leves para cron, modelos fortes para execução

---

### Resposta 2: Bug #24852 / attachAs

A **opção (b) usar attachAs com um .md customizado** é a única rota arquiteturalmente sólida.

Aguardar fix (opção c) gera paralisia. Injetar no task string (opção a) é armadilha de prompt engineering.

**Racional:**

1. **Separação de Responsabilidades (SoC):** Task string = "O QUE fazer". Arquivo anexado = "COMO se comportar" / "O QUE NÃO fazer".

2. **Modularidade Tática:** Sub-agent matemático não precisa de regras médicas. attachAs força contextos escopados.

3. **Imunidade à ausência de ferramentas:** Leaf sub-agents são "cegos e mudos". attachAs garante payload estático e garantido.

**Padrão:** Criar `memory/rules/` com fragmentos escopados. Quando o bug for corrigido, escopados continuam superiores a SOUL.md monolítico.

---

## PARTE 3: RESPOSTA DO ROBIN AO GEMINI PRO

---

### Sobre persistência:

JSON estático. Compatibilidade nativa (write/read/edit), atomicidade suficiente (edit por campo), debuggabilidade (`cat state.json`), portabilidade (viaja com workspace). SQLite é overengineering para nosso nivel.

### Sobre bug #24852:

Concordo com attachAs. Mas preciso de orientação: para sub-agents que processam dados matemáticos (binomial_tree.py, black76.py), quais regras são relevantes? Apenas `rules-quantmind.md` (padrões de código + testes) seria suficiente, ou devo incluir `rules-general.md` (segurança) também?

### Pergunta ao Gemini:

> Para sub-agents leaf processando código quantitativo, qual o escopo mínimo de rules via attachAs? Apenas regras do domínio (quantmind) ou também regras gerais (segurança)?

### Resposta do Gemini PRO (FINAL):

**Apenas `rules-quantmind.md`.** Não incluir regras gerais ou de segurança.

**Justificativa:** Sub-agent leaf tem maxSpawnDepth=1 e não herda ferramentas de sessão (sem acesso à rede, gravação indiscriminada no disco, git). Injetar "não commitar chaves de API" é desperdício de tokens — o agente não tem meios sistêmicos para violar essas regras.

Cada token de atenção deve ser direcionado à convergência do algoritmo, cálculo correto das Greeks, e passagem dos testes. Excesso de contexto irrelevante dilui a capacidade de raciocínio.

### Avaliação da Execução (Gemini PRO):

- **Limite rígido de tokens no handoff:** State.json com tetos rígidos (max 200 tokens por campo) é "uma defesa perfeita contra degradação de contexto em pipelines longas"
- **Margem de timeout (×0.7):** "Solução elegante" que evita corrupção do handoff durante escrita
- **Bug como feature:** Arquivos .md escopados transformam limitação do SOUL.md em vantagem arquitetural
- **Tiering:** Otimização avançada de orçamentos de inferência

**Veredicto:** "O plano passou de uma ideia para uma especificação técnica sólida."

---

## PARTE 4: RULES ESCOPADOS (attachAs)

---

### rules-quantmind.md

```markdown
# Regras — QuantMind Squad

## Padrões de Código
- Seguir estilo dos módulos existentes (risk_metrics.py, momentum.py, options_pricing.py)
- Dataclasses para resultados (com to_dict() e summary())
- Type hints em todas as funções públicas
- Docstrings no formato Google

## Testes
- Todo módulo NOVO deve ter testes em crew/quantmind/tools/tests/
- pytest como framework padrão
- Cobrir: import, pricing básico, edge cases, Greek ranges, roundtrip IV
- Mínimo: 10 testes por módulo

## Arquitetura
- Módulos ficam em crew/quantmind/tools/
- Tests ficam em crew/quantmind/tools/tests/
- Usar sys.path.insert(0, TOOLS_DIR) nos testes
- Dependências: numpy, scipy, pandas (já instalados)

## Decisões de Design
- Cada módulo é autocontido
- options_pricing.py é a referência de padrão
- Greeks via bump-and-reprice (não fórmulas analíticas no binomial tree)
- IV solver: scipy.optimize.brentq
```

### rules-health-squad.md

```markdown
# Regras — Health Squad

## 🚨 REGRAS CRÍTICAS (nunca violar)
1. Dr. Chopper é a autoridade máxima em saúde e protocolo hormonal
2. Verificação dupla obrigatória: todo cronograma hormonal revisado 2x
3. Não inventar schedule por conta própria
4. Saúde > pressa. Antes de responder rápido, responder certo.

## Regras de Protocolo
- Enantato: 50mg ds2dn
- Masteron: 50mg ds2dn
- HCG: 250UI seg/qui
- Próximo exame: 25/07/2026
```

### rules-pipeline.md

```markdown
# Regras — Pipeline Resilience

## Protocolo de Handoff
1. Ao concluir step, gerar handoff_payload (max 500 tokens)
2. Nunca salvar output bruto — apenas resumo comprimido
3. Incluir: resumo, arquivos, decisões, instruções next

## State File
- Localização: memory/pipelines/<id>.json
- Escrita: substituição atômica (.tmp → rename)
- Quem escreve: apenas step executor
- Quem lê: cron, heartbeat, sessão de retomada

## Anti-Zumbis
- Timeout: provider_timeout × 0.7
- Zumbi: running há > timeout × 1.5
- Retry: máx 3 tentativas
- Após 3 falhas: alertar Olliver
```

### rules-general.md

```markdown
# Regras Gerais — Bando Pirata

## Segurança
- NUNCA exfiltrar dados privados
- NUNCA commitar chaves de API
- trash > rm
- Quando em dúvida, perguntar ao Olliver

## Comunicação
- Founders and CEOs: chatId -1004226997838
- Canal Announcements: chatId -1003990750529
- NUNCA usar nome do grupo como target
```

---

**FIM DO DOCUMENTO CONSOLIDADO**

**Status:** COMPLETO — Pronto para revisão final pelo Gemini PRO.
