# Skill Structure Standard

Padrão para criação de skills no OpenClaw. Adotado do framework Coworker (v1.3) com adaptações pro nosso runtime.

## Estrutura de Diretórios

```
skill-name/
├── SKILL.md          (obrigatório)
├── scripts/          (opcional) — executáveis helpers
├── references/       (opcional) — docs carregadas sob demanda
├── examples/         (opcional) — exemplos de uso
├── evals/            (opcional) — testes de validação
└── assets/           (opcional) — templates, imagens, dados
```

## SKILL.md — Formato

### Frontmatter (obrigatório)

```yaml
---
name: skill-name
description: Quando usar esta skill (max 160 bytes)
---
```

**Regras:**
- `name`: lowercase, hífens, sem espaços
- `description`: ação + contexto. Ex: "Extract data from multiple URLs in parallel"
- Máximo 160 bytes na descrição

### Corpo do SKILL.md

Estrutura mínima recomendada:

```markdown
# Skill Name

## Quando Usar
- Trigger: [quando ativar]
- Exemplos: [casos de uso]
- Anti-patterns: [quando NÃO ativar]

## Como Funcionar
[Instruções claras e acionáveis]

## Exemplos
[Código ou passos concretos]

## Tratamento de Erros
[O que fazer quando algo falha]
```

**Princípios:**
1. "Context window é um bem público" — skills competem por tokens. Seja conciso
2. "O AI já é inteligente" — só adicione contexto que o modelo não tem
3. "Degrees of freedom" — instruções textuais pra tarefas flexíveis, scripts pra tarefas frágeis

## Regras de Criação

### O que deve ter uma skill
- [ ] Frontmatter com name e description
- [ ] Seção "Quando Usar" com triggers claros
- [ ] Instruções acionáveis (não teóricas)
- [ ] Pelo menos 1 exemplo concreto
- [ ] Tratamento de erros comuns

### O que NÃO deve ter
- [ ] Explicações óbvias (o modelo já sabe)
- [ ] Regras genéricas de segurança (ficam no AGENTS.md/SOUL.md)
- [ ] Código que o modelo já conhece (ex: `for` loops básicos)
- [ ] Mais de 200 linhas (dividir em sub-skills)

### Verificação pós-criação
1. Ler o SKILL.md criado
2. Confirmar que frontmatter está válido
3. Confirmar que descrição tem <160 bytes
4. Testar: a skill resolve o caso de uso?
5. Commit + push

## Exemplo: Frontmatter Válido

```yaml
---
name: whale-monitor
description: Monitor crypto wallet addresses for significant transfers and movements.
---
```

```yaml
---
name: browser-batch-extraction
description: Extract data from multiple URLs in parallel using browser automation.
---
```

```yaml
---
name: pipeline-resilience
description: Crash-safe pipeline orchestration with handoff, state persistence, and zombie detection.
---
```

## Exemplo: Frontmatter Inválido

```yaml
# ❌ sem name
---
description: uma skill legal
---

# ❌ description muito longa
---
name: my-skill
description: This skill does a lot of things including web scraping, data processing, and report generation for multiple use cases
---

# ❌ name com espaços
---
name: My Cool Skill
description: Does stuff
---
```

## Mapeamento: Skill Type → Directory Structure

| Tipo | Estrutura Recomendada |
|------|----------------------|
| Browser automation | SKILL.md + examples/ |
| Code generation | SKILL.md + scripts/ + examples/ |
| Data processing | SKILL.md + scripts/ + references/ |
| Integration (API) | SKILL.md + references/ |
| Monitoring | SKILL.md + scripts/ |
| Workflow/orchestration | SKILL.md + examples/ + evals/ |

## Skills Existentes — Status

| Skill | Frontmatter | Estrutura | Status |
|-------|-------------|-----------|--------|
| ultra-pipeline-resilience | ✅ | ✅ completa | v1.3 |
| browser-batch-extraction | ✅ | ✅ mínima | v1.0 |
| brave-search | ⚠️ | ⚠️ | Precisa padronizar |
| x-twitter | ⚠️ | ⚠️ | Precisa padronizar |
| watchdog | ⚠️ | ⚠️ | Precisa padronizar |

**Próximo passo:** Padronizar as skills existentes que não seguem o padrão.
