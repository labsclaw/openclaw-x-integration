# RELATÓRIO TÉCNICO: Pipeline Resilience & Anti-Session-Crash

**Versão:** 3.0 (FINAL — Consolidação Sonnet 5 + Gemini PRO)  
**Data:** 2026-07-02  
**Status:** APROVADO PARA IMPLEMENTAÇÃO  
**Autores:** Robin (Bando) + Claude Sonnet 5 + Gemini PRO

---

## 1. RESUMO EXECUTIVO

Implementar sistema de **pipeline resilience** para OpenClaw que garante:
1. Tarefas longas sobrevivem a crashes de sessão
2. Progresso é persistido em disco com contexto comprimido
3. Retomada automática via "hydration" do estado
4. Monitoramento proativo com proteção contra zumbis

**Não é gambiarra.** É checkpointing — padrão canônico de sistemas distribuídos.

---

## 2. DIAGNÓSTICO CONSOLIDADO

### 2.1 O que cada consultoria identificou

| Aspecto | Robin (original) | Sonnet 5 (correções) | Gemini PRO (amadurecimento) |
|---------|-------------------|----------------------|----------------------------|
| **Abordagem** | 4 mecanismos nativos | Correções técnicas precisas | Elevação para padrão arquitetural |
| **State files** | Nice-to-have | Necessário (único caminho) | **Handoff protocol** — compressão de contexto |
| **Sub-agents** | Delegação básica | Bug #24852 (sem SOUL.md) | **Monitoramento de zumbis** + timeout |
| **Goals** | 1 por módulo ❌ | 1 guarda-chuva ✅ | **Wrapper automático** (não manual) |
| **update_plan** | Uso livre | Experimental (config) | State file como alternativa robusta |
| **Principal falha** | "Não usamos consistently" | Detalhes técnicos faltando | **Falta de dimensionamento** pelo timeout da API |

### 2.2 Correções Críticas Acumuladas

**🔴 Sem essas correções, a skill falha silenciosamente:**

1. **1 goal apenas por sessão** — progresso dos steps vai no state file, não no goal
2. **Bug #24852** — sub-agents NÃO recebem SOUL.md/IDENTITY.md → injetar no task
3. **update_plan é experimental** — precisa habilitar `tools.experimental.planTool`
4. **Goal só aceita `complete`/`blocked`** — sem status intermediários
5. **Leaf sub-agents não recebem session tools** — não podem spawnar próprios sub-agents
6. **Dimensionamento pelo timeout da API** — cada step deve caber no timeout do provider

---

## 3. ARQUITETURA FINAL

### 3.1 O Protocolo de "Handoff" (Conceito Central do Gemini PRO)

> "Quem termina o trabalho, prepara o resumo para o próximo."

A chave não é salvar o output bruto — é criar um **resumo de handoff** comprimido que contenha apenas:
- O que foi feito (1-2 linhas)
- O que precisa ser feito next (1-2 linhas)
- Dados essenciais para continuidade (máximo 500 tokens)

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO DE HANDOFF                         │
│                                                              │
│  STEP N termina                                              │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────────────┐                                    │
│  │ Comprimir output    │  Output bruto → Resumo executivo   │
│  │ (não salvar tudo)   │  Max 500 tokens                   │
│  └─────────┬───────────┘                                    │
│            ▼                                                 │
│  ┌─────────────────────┐                                    │
│  │ Escrever state file │  memory/pipelines/<id>.json        │
│  │ + contexto next     │  Inclui: resumo + próximos passos  │
│  └─────────┬───────────┘                                    │
│            ▼                                                 │
│  ┌─────────────────────┐                                    │
│  │ Spawn sub-agent     │  sessions_spawn(task=handoff)      │
│  │ com contexto        │  → O sub-agent "acorda" sabendo    │
│  │ comprimido          │    exatamente onde parar            │
│  └─────────────────────┘                                    │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Arquitetura Completa

```
┌──────────────────────────────────────────────────────────────────┐
│                      SESSÃO PRINCIPAL                            │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. Verificar se há pipeline pendente (state file)        │   │
│  │    → Se sim: RETOMAR (passo 4)                           │   │
│  │    → Se não: INICIAR NOVA (passo 2)                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 2. INICIALIZAÇÃO                                          │   │
│  │    a. create_goal(1 goal guarda-chuva)                   │   │
│  │    b. write state file + handoff payload                  │   │
│  │    c. Criar cron monitor (10 min)                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 3. EXECUÇÃO POR STEP                                      │   │
│  │    a. Ler state file → identificar próximo pending        │   │
│  │    b. Atualizar state → "running"                         │   │
│  │    c. Comprimir contexto do step anterior (se houver)     │   │
│  │    d. sessions_spawn(task=handoff_payload)                │   │
│  │    e. sessions_yield(message="Aguardando step N...")      │   │
│  │    f. Receber completion event                            │   │
│  │    g. Processar resultado + atualizar state               │   │
│  │    h. Se há mais steps → voltar a (a)                     │   │
│  │    i. Se todos done → update_goal(complete)               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 4. RETOMADA (se detectou state file pendente)             │   │
│  │    a. Ler state file                                      │   │
│  │    b. Identificar último completed + próximo pending      │   │
│  │    c. Injetar contexto comprimido do último completed     │   │
│  │    d. Spawn sub-agent com handoff payload                 │   │
│  │    e. Continuar fluxo normal (passo 3)                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 5. MONITORAMENTO                                          │   │
│  │    a. Cron a cada 10 min verifica state file              │   │
│  │    b. Detecta steps "running" há >15 min → ZUMBI         │   │
│  │    c. Marca como "failed" + alerta Olliver                │   │
│  │    d. Heartbeat como fallback se cron falhar              │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. STATE FILE — ESPECIFICAÇÃO TÉCNICA

### 4.1 Schema Completo

```json
{
    "id": "pipeline-<unique-id>",
    "name": "Descrição da Pipeline",
    "version": "1.0",
    "startedAt": "ISO-8601",
    "goalId": "<id-do-goal-criado>",
    "status": "running|paused|completed|failed",
    
    "steps": [
        {
            "name": "step-1-name",
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
                "summary": "Resumo executivo do que foi feito (max 200 tokens)",
                "outputPath": "path/to/output/artifact.py",
                "nextSteps": "O que o próximo step deve fazer (max 100 tokens)",
                "context": "Dados essenciais para continuidade (max 200 tokens)",
                "tokenCount": 450
            },
            "retries": 0,
            "maxRetries": 3,
            "startedAt": "ISO-8601",
            "completedAt": "ISO-8601",
            "error": null,
            "duration": 125
        }
    ],
    
    "lastCheck": "ISO-8601",
    "alerts": 0,
    "completedAt": null,
    "totalTokens": 1250,
    "maxTokens": 5000
}
```

### 4.2 Regras de Compressão (Gemini PRO)

**Output de cada step NÃO deve ser salvo inteiro.** Em vez disso:

| Dado | Antes (errado) | Depois (correto) |
|------|----------------|------------------|
| Output do módulo | Salvar .py inteiro no state file | Salvar APENAS o path + resumo (3 linhas) |
| Erros | Stack trace completo | Mensagem de erro + causa raiz (1 linha) |
| Testes | Output completo do pytest | "237/237 passed" ou "3 failed: [nomes]" |
| Contexto | Tudo que o agente pensou | Apenas decisões de design que afetam o próximo step |

**Regra de ouro:** Se o próximo step não precisa de某个 dado para executar, NÃO salve no handoff.

### 4.3 Exemplo de Handoff Payload

```json
{
    "summary": "Implementado binomial_tree.py com CRR, American/European, dividends, Greeks. Todos os 26 testes passando.",
    "outputPath": "crew/quantmind/tools/binomial_tree.py",
    "nextSteps": "Implementar black76.py — Black-76 para futures options. Seguir padrão do options_pricing.py.",
    "context": "BinomialTree._valuation() é o método interno sem Greeks (evita recursão). DiscreteDividend dataclass para dividendos. Usar scipy.optimize.brentq para IV.",
    "tokenCount": 180
}
```

---

## 5. DIMENSIONAMENTO PELO TIMEOUT DA API

### 5.1 O problema que o Gemini identificou

Cada provider tem timeout diferente:

| Provider | Timeout típico | Impacto |
|----------|----------------|---------|
| OpenCode (big-pickle) | ~5 min | Steps devem completar em < 4 min |
| NVIDIA NIM (MiniMax M3) | ~30s timeout de connect, mas execução longa | Sub-agents podem demorar |
| OpenRouter (fallback) | ~10 min | Mais folga |

**Se o step demora mais que o timeout → sessão corta → handoff incompleto → state file corrompido.**

### 5.2 Regra de Dimensionamento

```
TEMPO MÁXIMO POR STEP = (Timeout do provider × 0.7) - margem de segurança

Exemplo:
- Provider: OpenCode big-pickle (timeout ~5 min)
- Tempo máximo por step: 5 × 0.7 = 3.5 min
- Se step estimado > 3.5 min → DIVIDIR em sub-steps
```

### 5.3 Decomposição de Tarefas Longas

| Tarefa original | Decomposição | Tempo estimado |
|-----------------|--------------|----------------|
| "Implementar módulo completo" | 1. Escrever código | ~2 min |
| | 2. Escrever testes | ~1 min |
| | 3. Rodar + fix bugs | ~1 min |
| "Code review completo" | 1. Revisar lógica | ~1 min |
| | 2. Revisar testes | ~1 min |

---

## 6. PROTEÇÃO CONTRA ZUMBIS (Gemini PRO)

### 6.1 O problema

Sub-agent sofre falha fatal na API → nunca emite completion event → sessão principal fica aguardando indefinidamente via `sessions_yield`.

### 6.2 Solução: Timeout + Dead Letter Queue

```python
# No cron monitor (a cada 10 min):
state = read("memory/pipelines/<id>.json")

for step in state["steps"]:
    if step["status"] == "running":
        started = parse(step["subAgent"]["startedAt"])
        elapsed = now() - started
        
        if elapsed > step["subAgent"]["timeout"] * 1.5:
            # ZUMBI DETECTADO
            step["status"] = "failed"
            step["error"] = f"Timeout: {elapsed}s > {step['subAgent']['timeout'] * 1.5}s"
            step["retries"] += 1
            
            if step["retries"] <= step["maxRetries"]:
                # Retry automático
                step["status"] = "pending"
                alert("♻️ Retry automático step {step['name']} (tentativa {step['retries']})")
            else:
                # Max retries atingido
                alert("🚨 Step {step['name']} falhou após {step['maxRetries']} tentativas")
                state["status"] = "failed"
```

### 6.3 Timeouts por Contexto

| Contexto | Timeout | Retry | Ação |
|----------|---------|-------|------|
| Sub-agent (background) | 5 min | 3x | Re-spawn com mesmo handoff |
| Cron monitor check | 10 min | 1x | Alertar Olliver |
| Sessão principal (yield) | 15 min | 0 | Cron detecta e retoma |

---

## 7. WRAPPER AUTOMÁTICO (Gemini PRO)

### 7.1 O problema

A skill não deve depender de invocação manual. "Vamos criar a skill de pipeline resilience" → esquece → falha.

### 7.2 Solução: Hook no início de qualquer tarefa complexa

```python
# Adicionar no AGENTS.md ou SOUL.md:

## 🚨 Auto-Resilience Hook

ANTES de qualquer tarefa com > 2 passos ou estimativa > 5 minutos:

1. Verificar se update_plan está habilitado
2. create_goal(objetivo_geral)
3. write state file em memory/pipelines/
4. Criar cron monitor
5. Delegar via sessions_spawn + sessions_yield
6. Atualizar state file a cada step

SE ESQUECER: O cron monitor detecta e alerta.
```

### 7.3 Detecção Automática

```python
# Heurística para decidir se precisa de resilience:
def needs_resilience(task_description, estimated_steps, estimated_time_min):
    if estimated_steps > 2:
        return True
    if estimated_time_min > 5:
        return True
    if "implementar" in task_description.lower() and "módulo" in task_description.lower():
        return True
    if "pipeline" in task_description.lower():
        return True
    return False
```

---

## 8. PROTOCOLO DE RETOMADA (HYDRATION)

### 8.1 O que o Gemini perguntou

> "Como você planeja estruturar a injeção do payload de recuperação a partir do arquivo de estado, garantindo que a nova sessão retome exatamente do ponto de interrupção sem comprometer o limite de tokens úteis da janela de contexto?"

### 8.2 Resposta: Prompt de Reanimação Comprimido

Quando a sessão retoma, o prompt deve conter APENAS:

```
=== RETOMADA DE PIPELINE ===
Pipeline: <id>
Step: <nome-do-step-pendente>
Status anterior: <ultimo-completado>

CONTEXTO DO STEP ANTERIOR:
<handoff.summary> (máx 200 tokens)

O QUE FAZER AGORA:
<handoff.nextSteps> (máx 100 tokens)

DADOS NECESSÁRIOS:
<handoff.context> (máx 200 tokens)

ARQUIVOS RELEVANTES:
- Output: <handoff.outputPath>
- Testes: <step.testFile>

=== FIM RETOMADA ===
```

**Total:** ~500 tokens (vs. milhares se injetássemos histórico completo)

### 8.3 Fluxo de Hydration

```
1. Heartbeat detecta state file pendente
2. Lê memory/pipelines/<id>.json
3. Identifica: último completed + próximo pending
4. Extrai handoff do último completed
5. Monta prompt de reanimação (~500 tokens)
6. Cria sessão isolada com o prompt
7. Sessão "acorda" sabendo exatamente o que fazer
8. Executa o próximo step
9. Atualiza state file
10. Se há mais steps → repete
```

---

## 9. CHECKLIST DE IMPLEMENTAÇÃO

### 9.1 Pré-requisitos

- [ ] Verificar se `tools.experimental.planTool` está habilitado
- [ ] Criar diretório `memory/pipelines/`
- [ ] Testar sessions_spawn com task simples (validar bug #24852)
- [ ] Testar sessions_yield (validar completion event)
- [ ] Verificar timeout do provider padrão (openclaw.json)

### 9.2 Implementação da Skill

- [ ] Criar `skills/pipeline-resilience/SKILL.md`
- [ ] Definir schema do state file
- [ ] Implementar lógica de handoff (compressão)
- [ ] Implementar wrapper automático (detecção de tarefa complexa)
- [ ] Implementar monitor de zumbis (cron)
- [ ] Implementar protocolo de retomada (hydration)
- [ ] Testar com pipeline real (3 módulos)
- [ ] Testar cenário de crash simulado
- [ ] Documentar para replicação

### 9.3 Validação

- [ ] Sub-agents recebem task completa (testar com Hello World)
- [ ] State files persistem entre sessões
- [ ] Cron monitor funciona em sessionTarget="isolated"
- [ ] Retomada funciona (simular crash)
- [ ] Handoff payload não excede 500 tokens
- [ ] Zumbis são detectados e retry funciona

---

## 10. CENÁRIO COMPLETO (E2E)

### 10.1 Setup

```
12:00:00 - Robin detecta tarefa complexa (>2 steps, >5 min)
12:00:01 - create_goal("Fechar gaps QuantMind: 3 módulos options")
12:00:02 - write state file (3 steps pending)
12:00:03 - Criar cron monitor (10 min)
12:00:04 - Spawn sub-agent #1 (binomial_tree)
12:00:05 - sessions_yield("Aguardando binomial_tree...")
```

### 10.2 Execução Normal

```
12:03:30 - Completion event: binomial_tree OK
12:03:31 - Robin processa resultado
12:03:32 - Atualiza state file (step 1 = completed + handoff)
12:03:33 - Spawn sub-agent #2 (black76) com handoff de #1
12:03:34 - sessions_yield("Aguardando black76...")
12:05:45 - Completion event: black76 OK
12:05:46 - Atualiza state file (step 2 = completed + handoff)
12:05:47 - Spawn sub-agent #3 (scenario_analysis) com handoff de #2
12:05:48 - sessions_yield("Aguardando scenario_analysis...")
12:08:10 - Completion event: scenario_analysis OK
12:08:11 - Atualiza state file (step 3 = completed)
12:08:12 - Roda testes completos: 237/237 ✅
12:08:13 - update_goal(complete)
12:08:14 - Deleta cron monitor
12:08:15 - Limpa state file
```

### 10.3 Crash + Retomada

```
12:00:05 - sessions_yield (aguardando binomial_tree)
12:02:00 - 💥 SESSÃO CRASHA (rate limit)

--- 30 minutos depois ---

12:30:00 - Heartbeat detecta state file
12:30:01 - Lê memory/pipelines/phase4.json
12:30:02 - Step "binomial_tree" = running há 30 min → ZUMBI
12:30:03 - Marca como "failed", retries = 1
12:30:04 - Re-spawn sub-agent #1b (binomial_tree)
12:03:30 - Completion event: binomial_tree OK
12:03:31 - Continua fluxo normal...
```

### 10.4 Sub-agent Falha

```
12:00:04 - Spawn sub-agent #1 (binomial_tree)
12:03:30 - Completion event com ERRO
12:03:31 - Robin: step "failed", retries = 0
12:03:32 - Alerta Olliver: "⚠️ binomial_tree falhou: [erro]"
12:04:00 - Olliver: "Tente novamente"
12:04:01 - Reseta para "pending", retries = 1
12:04:02 - Spawn novo sub-agent #1b
12:07:30 - Completa com sucesso ✅
```

---

## 11. MÉTRICAS DE SUCESSO

| Métrica | Target | Como Medir |
|---------|--------|------------|
| Sessões que crasham e retomam | 100% | Contar crashes vs retomadas |
| Tempo de retomada | < 30s | Heartbeat detecta → sub-agent inicia |
| Perda de trabalho | 0% | Steps completed não re-executados |
| Falsos alertas | < 5% | Alertas vs problemas reais |
| Cobertura | 100% | Todas as tarefas > 2 steps |
| Handoff payload | < 500 tokens | Contar tokens no state file |
| Zumbis detectados | 100% | Sub-agents sem completion |

---

## 12. RISCOS E MITIGAÇÕES

| Risco | Gravidade | Mitigação |
|-------|-----------|-----------|
| Sub-agents sem SOUL.md (bug #24852) | **Alta** | Injetar regras críticas no task |
| 1 goal apenas por sessão | **Alta** | State file pra progresso |
| update_plan experimental | **Média** | Verificar config; state file como fallback |
| Goal só aceita complete/blocked | **Média** | Não usar status intermediários |
| Handoff payload muito grande | **Média** | Enforcar limite de 500 tokens |
| Provider timeout variável | **Média** | Dimensionar steps com margem de 30% |
| State file corrompido | **Baixa** | Checksum + backup |
| Cron monitor falha | **Baixa** | Heartbeat como fallback |

---

## 13. REFERÊNCIAS

- **OpenClaw Docs:** sessions_spawn, sessions_yield, create_goal
- **Bug #24852:** Sub-agents não carregam SOUL.md/IDENTITY.md
- **Goal Command Plugin:** closed-loop execution para /goal
- **CLI Transcripts:** persistCliTurnTranscript() (histórico, não progresso)
- **Consultoria:** Claude Sonnet 5 + Gemini PRO (02/07/2026)
- **Conceito:** Checkpointing em sistemas distribuídos (Gemini PRO)

---

## 14. PRÓXIMOS PASSOS

### Imediato (hoje):
1. ✅ Relatório v3.0 consolidado
2. Aprovação do Dr. Roger
3. Verificar config do gateway (update_plan habilitado?)

### Curto prazo (esta semana):
4. Criar skill `pipeline-resilience/SKILL.md`
5. Testar com pipeline real
6. Documentar para replicação

### Médio prazo:
7. Integrar com todos os squads
8. Dashboard de status
9. Métricas automatizadas

---

## 15. ESCOLHA DE PERSISTÊNCIA (Resposta ao Gemini PRO)

### Pergunta:
> "Qual abordagem você prefere para o armazenamento desse estado: JSON estático em memory/pipelines/ ou SQLite?"

### Resposta: JSON estático.

| Critério | JSON | SQLite | Veredicto |
|----------|------|--------|-----------|
| **Compatibilidade nativa** | write/read/edit já existem | Precisa exec + python script | JSON |
| **Atomicidade** | Edit por campo (oldText/newText) | Transactions + locks | JSON (suficiente) |
| **Debuggability** | `cat state.json` | `sqlite3 -query "..."` | JSON |
| **Portabilidade** | Viaja com o workspace | Path relativo + conexao | JSON |
| **Complexidade** | Zero setup | Setup + migrations | JSON |

**Quando SQLite faria sentido:** 50+ pipelines simultaneas com queries analyticas. Nao e nosso caso.

**Decisão final:** JSON + handoff_payload comprimido. Simples, debuggavel, nativo.

### Especificação do Payload de Handoff (Gemini PRO Fase 1)

O sub-agent ao concluir deve gerar:

```json
{
    "completed_summary": "BinomialTree implementado. CRR com 200 steps. American/European. Greeks via bump-and-reprice.",
    "output_file": "crew/quantmind/tools/binomial_tree.py",
    "critical_vars": {
        "_valuation()": "Método interno sem Greeks (evita recursão)",
        "DiscreteDividend": "dataclass para dividendos discretos"
    },
    "design_decisions": [
        "_valuation() separado de price() para que _compute_greeks() não recurse",
        "Dividendos Europeanos: subtrai PV do spot inicial",
        "Dividendos Americanos: ajusta intrínseco no backward induction"
    ],
    "next_step_instructions": "Implementar black76.py — Black-76 para futures. Seguir padrão de options_pricing.py."
}
```

### Recovery Boot Prompt (Gemini PRO Fase 3)

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

**Total:** ~400 tokens. Suficiente para o modelo saber exatamente onde está.

### Tiering de Modelos (Gemini PRO Fase 4)

| Função | Modelo sugerido | Justificativa |
|--------|-----------------|---------------|
| **Cron monitor** (leitura de state) | Tier 2/3 (rápido, barato) | Só lê JSON, não precisa de raciocínio |
| **Recovery prompt** (montar handoff) | Tier 2/3 | Concatenação simples |
| **Execução do step** (código pesado) | Tier 1 (forte) | Raciocínio complexo |

**No nosso caso:** big-pickle (Tier 2) para cron/recovery, mimo-v2.5 (Tier 1) para execução.

---

## 16. RESOLUÇÃO DO BUG #24852 (Resposta do Gemini PRO)

### Pergunta Original:
> Sub-agents leaf não recebem SOUL.md (bug #24852). Qual abordagem para regras de negócio críticas? (a) injetar no task, (b) attachAs com .md customizado, (c) aguardar fix?

### Resposta do Gemini PRO: **Opção (b) — attachAs com .md escopados**

**Por que (a) é armadilha:** Injetar regras globais no task string gera dívida técnica imediata — mistura "O QUE fazer" com "COMO se comportar", confundindo o modelo ("lost in the middle").

**Por que (c) é paralisia:** Aguardar fix do bug #24852 gera paralisia de desenvolvimento. Não se depende de bugfix de terceiros pra avançar.

**Por que (b) é superior:**

1. **Separação de Responsabilidades (SoC):**
   - Task string = "O QUE fazer" (instrução da ação imediata)
   - attachAs = "COMO se comportar" / "O QUE NÃO fazer" (guardrails)

2. **Modularidade Tática:**
   - Sub-agent matemático NÃO precisa de regras de validação médica
   - Sub-agent de saúde NÃO precisa de regras de formatação de código
   - attachAs força contextos **escopados**: `rules_validation.md`, `rules_math.md`

3. **Imunidade à ausência de ferramentas:**
   - Leaf sub-agents são "cegos e mudos" (maxSpawnDepth=1, sem session tools)
   - attachAs garante que o payload de regras seja embutido na inicialização de forma **estática e garantida**

### Padrão de Implementação

```
memory/rules/
├── rules-health-squad.md      # Dr. Chopper: validação médica, doses
├── rules-quantmind.md         # QuantMind: padrões de código, testes
├── rules-pipeline.md          # Pipeline resilience: handoff, state files
└── rules-general.md           # Regras gerais: segurança, não exfiltrar dados
```

**Quando spawnar sub-agent:**
```python
sessions_spawn(
    task="Implementar binomial_tree.py...",
    attachments=[{"name": "rules-quantmind.md", "content": "..."}],
    # ou attachAs com path para arquivo existente
)
```

**Vantagem futura:** Quando o bug #24852 for corrigido, arquivos escopados continuam SUPERIORES a um SOUL.md gigante. Não precisa reescrever nada.

---

## 17. SUMÁRIO EXECUTIVO FINAL

### Fontes Consultadas
| Fonte | Contribuição | Status |
|-------|-------------|--------|
| Robin (Bando) | Diagnóstico + 4 mecanismos nativos | ✅ Integrado |
| Claude Sonnet 5 | Correções técnicas (bug #24852, 1 goal, update_plan, sessions_yield) | ✅ Integrado |
| Gemini PRO | Amadurecimento arquitetural (handoff, dimensionamento, zumbis, wrapper, tiering, atomicidade, attachAs) | ✅ Integrado |

### Decisões Técnicas Finalizadas

| Decisão | Escolha | Justificativa |
|---------|---------|---------------|
| **Persistência** | JSON estático | KISS, nativo, debuggável, portável |
| **Atomicidade** | Write .tmp → rename | Previne truncamento por crash |
| **Handoff** | Comprimido (~500 tokens) | Passagem de bastão, não log |
| **Regras de negócio** | attachAs com .md escopados | SoC, modularidade, imune ao bug #24852 |
| **Retomada** | Prompt de reanimação dinâmico | ~400 tokens, sem histórico completo |
| **Monitoring** | Cron (10 min) + heartbeat fallback | Anti-zumbis, retry 3x |
| **Goals** | 1 guarda-chuva por sessão | Limitação nativa do OpenClaw |
| **update_plan** | State file como alternativa | update_plan é experimental |
| **Tiering** | big-pickle (cron) + mimo-v2.5 (execução) | Custo-benefício |

### Próximos Passos

1. ✅ Relatório v3.0 completo
2. ✅ Respostas do Gemini PRO integradas
3. ✅ Estrutura memory/rules/ criada (4 arquivos)
4. ✅ AGENTS.md atualizado com seção Pipeline Monitoring
5. ⏳ Aprovação do Olliver para implementação da skill
6. ⏳ Criar `skills/pipeline-resilience/SKILL.md`
7. ⏳ Testar com pipeline real
8. ⏳ Documentar para replicação

### Documentos Produzidos

| Arquivo | Conteúdo |
|---------|----------|
| `crew/finding/pipeline-resilience-report.md` | Relatório v3.0 COMPLETO |
| `crew/finding/gemini-pro-resposta-pipeline.md` | Resposta original Gemini PRO (persistência) |
| `crew/finding/gemini-pro-bug24852-resposta.md` | Resposta Gemini PRO (bug #24852 / attachAs) |
| `memory/rules/rules-quantmind.md` | Regras escopadas para QuantMind |
| `memory/rules/rules-health-squad.md` | Regras escopadas para Health Squad |
| `memory/rules/rules-pipeline.md` | Regras escopadas para Pipeline Resilience |
| `memory/rules/rules-general.md` | Regras gerais do Bando |

---

**FIM DO RELATÓRIO v3.0**

**Status:** COMPLETO — Todas as perguntas respondidas, todas as decisões tomadas.
**Aguardando:** Aprovação do Olliver para implementação da skill.
