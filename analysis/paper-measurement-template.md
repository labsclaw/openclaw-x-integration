# Template de Coleta de Dados — LLM Estimates vs Reality

**Objetivo:** Coletar dados sistemáticos de estimativa LLM vs tempo real de execução.
**Período:** 2026-07-04 até 2026-07-18 (2 semanas)
**Output:** Dataset para paper "Measuring the Gap"

---

## Como Usar

1. Antes de cada tarefa, pedir ao LLM a estimativa de tempo
2. Registrar a estimativa
3. Cronometrar a execução real
4. Preencher o registro abaixo
5. Ao final de 2 semanas, gerar análise estatística

---

## Registro de Medição

### Medição #001

- **Data:** 2026-07-03
- **Tarefa:** Análise completa do repo Coworker (1280 arquivos) + relatório técnico + review + implementação + deploy
- **Tipo:** code-analysis + review + implementation + deployment
- **Estimativa LLM:** 3-5 dias úteis (pergunta feita e resposta registrada)
- **Tempo real:** ~4 horas
- **Compressão:** 8-12x
- **Agente(s) envolvidos:** Justus (CEO), Robin (Bando)
- **Ferramentas:** git clone, web_fetch, read, edit, write, exec, cron, gateway
- **Notas:** Incluiu whale monitoring paralelo. Primeira medição do dataset.
- **Status:** ✅ Completo

---

## Categorias de Tarefa

| Código | Categoria | Exemplo |
|--------|-----------|---------|
| `CODE` | Análise/implementação de código | Repo analysis, feature dev, bug fix |
| `DOC` | Documentação/paper | Relatório técnico, paper, artigo |
| `DEPLOY` | Deploy/configuração | Skill deployment, cron setup, gateway config |
| `REVIEW` | Revisão/validação | Code review, skill validation, report review |
| `RESEARCH` | Pesquisa/investigação | Market research, competitor analysis, whale investigation |
| `COMPLEX` | Multi-step (várias categorias) | O caso de hoje: CODE+DOC+REVIEW+DEPLOY |

---

## Formato de Registro

Cada medição deve conter:

```json
{
  "id": "001",
  "date": "2026-07-03",
  "task_description": "Brief description",
  "category": "CODE|DOC|DEPLOY|REVIEW|RESEARCH|COMPLEX",
  "llm_estimate_minutes": 0,
  "actual_minutes": 0,
  "compression_ratio": 0,
  "agents_used": [],
  "tools_used": [],
  "parallel_tasks": true|false,
  "notes": "",
  "status": "complete|partial|failed"
}
```

---

## Pipeline de Coleta

### Antes da tarefa:
1. Perguntar ao LLM: "Quanto tempo estimado pra [descrição da tarefa]?"
2. Registrar resposta exata (screenshot ou copy)
3. Iniciar cronômetro

### Depois da tarefa:
4. Parar cronômetro
5. Preencher template
6. Calcular compression_ratio = llm_estimate / actual
7. Salvar em `memory/metrics/llm-estimates.json`

### Análise semanal (todo domingo):
8. Calcular média, mediana, desvio padrão por categoria
9. Identificar outliers
10. Gerar gráfico de distribuição
11. Atualizar `memory/metrics/weekly-summary.json`

---

## Métricas de Output

### Dataset Final (após 2 semanas)

```
memory/metrics/
├── llm-estimates.json          ← registros individuais
├── weekly-summary.json         ← resumo semanal
├── analysis.json               ← análise estatística final
└── paper-data.md               ← dados formatados pro paper
```

### Análise Estatística

Para cada categoria, calcular:
- **n** = número de amostras
- **mean** = média de compressão
- **median** = mediana (mais resistente a outliers)
- **std** = desvio padrão
- **min/max** = range
- **confidence_interval_95** = IC 95%
- **p_value** = teste t comparando estimativa vs real

### Gráficos pra paper

1. **Box plot** de compressão por categoria
2. **Scatter plot** de estimativa vs real (com linha de referência y=x)
3. **Histograma** de distribuição de compressão
4. **Timeline** de iterações ao longo das 2 semanas

---

## Checklist Diário

- [ ] Tarefa realizada hoje?
- [ ] Estimativa LLM registrada ANTES de começar?
- [ ] Tempo real cronometrado?
- [ ] Registro preenchido em `llm-estimates.json`?
- [ ] Compression ratio calculado?

---

## Notas Metodológicas

### Fonte de estimativa
- Sempre pedir a estimativa ANTES de começar
- Usar o modelo que estamos testando (mimo-v2.5-free por padrão)
- Registrar a resposta exata, não uma interpretação

### O que contar como "tempo real"
- Desde o primeiro tool call até o último
- Incluir tempo de thinking/reasoning
- Não incluir tempo de "espera" (ex: aguardando cron disparar)
- Incluir tempo de correção se o primeiro approach falhou

### Paralelismo
- Se tarefas rodam em paralelo, registrar cada uma separadamente
- Marcar `parallel_tasks: true` no registro
- A análise deve incluir e excluir paralelismo separadamente

### Outliers
- Se uma tarefa levar 10x mais que a média da categoria, investigar
- Pode ser: ferramenta quebrou, escopo mudou, erro humano
- Registrar motivo do outlier, não descartar do dataset
