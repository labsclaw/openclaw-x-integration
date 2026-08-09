# Segment: s009 — Error Tracking & Self-Improvement

## Resumo
Sistema de registro estruturado de erros (meus e de sub-agents) para auto-improvement. Lacuna identificada em 2026-07-08.

## Por Que Importa
Erros são o combustível do auto-improvement. Sem registro estruturado, cometemos os mesmos erros novamente. Cada erro registrado vira lição que melhora comportamento futuro.

## Formato de Registro

### Campo de Erro (para entries individuais)

```markdown
### [DATA] Categoria: Breve Descrição

- **O que aconteceu:** [Descrição objetiva do erro]
- **Contexto:** [O que estava fazendo, qual task]
- **Causa raiz:** [Por que aconteceu]
- **Impacto:** [O que foi afetado]
- **Resolução:** [Como foi corrigido]
- **Lições aprendidas:** [O que mudar pra não repetir]
- **Ação preventiva:** [Regra ou checklists adicionado]
- **Sub-agent?** [Sim/Nome do sub-agent]
```

### Categorias

| Categoria | Exemplo |
|-----------|---------|
| `tool-misuse` | Uso errado de tool (ex: copiar arquivo pra origem) |
| `wrong-assumption` | Assumir estado sem verificar |
| `timeout` | Processo morto por timeout sem verificação |
| `incomplete-output` | Reportar sucesso sem confirmar |
| `sub-agent-failure` | Sub-agent falhou ou produziu output inválido |
| `configuration` | Erro de config, encoding, path |
| `communication` | Resposta incorreta ou incompleta ao usuário |

## Erros Registrados

### [2026-07-08] tool-misuse: Copy-Item pra diretório de origem

- **O que aconteceu:** Tentei copiar `ultra-confluence-docs` de `~/.openclaw/skills/` para `~/.openclaw/skills/ultra-confluence-docs` (mesmo path)
- **Contexto:** Instalação local da skill após push pro GitHub
- **Causa raiz:** Não verifiquei se origem e destino eram o mesmo diretório antes de executar
- **Impacto:** Erro PowerShell, mensagem confusa pro usuário
- **Resolução:** Informei ao Dr. Roger que era erro meu, skill já estava no local correto
- **Lições aprendidas:** Antes de copiar, comparar caminhos resolvidos. Se origem == destino, pular.
- **Ação preventiva:** Adicionar check `if (source -eq dest)` antes de Copy-Item em workflows futuros
- **Sub-agent?** Não

### [2026-07-12] wrong-assumption: Não sabia padrão de nomenclatura de skills

- **O que aconteceu:** Criei skills com nomes `chrome-stealth-navigator` e `browser-stealth-timing` em pasta `skills/` em vez de `ultra-*-skill` em `openclaw-skills/`
- **Contexto:** Dr. Roger mandou documentação de chrome-stealth-navigator e pediu pra melhorar skill de browser
- **Causa raiz:** Não verifiquei o padrão existente antes de criar. Assumi kebab-case simples sem prefixo
- **Impacto:** Dr. Roger corrigiu, precisei mover arquivos
- **Resolução:** Renomeei pra `ultra-chrome-stealth-navigator-skill` e `ultra-browser-stealth-timing-skill`, movi pra `openclaw-skills/`
- **Lições aprendidas:** SEMPRE verificar padrão de nomenclatura E localização ANTES de criar skill. O padrão é `ultra-*-skill` em `openclaw-skills/`
- **Ação preventiva:** Regra salva em s004-skills.md. Check `Get-ChildItem openclaw-skills` antes de criar qualquer skill
- **Sub-agent?** Não

### [2026-07-08] communication: Primeira resposta sobre Confluence skill

- **O que aconteceu:** Dr. Roger mandou URL do repo bybren-llc com a intenção de transformar em ultra skill. Eu descrevi a skill e perguntei "Quer que eu adapte ou era só referência?"
- **Contexto:** Mensagem com URL, sem contexto explícito da intenção
- **Causa raiz:** Não inferi a intenção a partir do contexto (já temos padrão de ultra skills no GitHub)
- **Impacto:** Dr. Roger teve que explicar "Era pra transformar em uma das nossas ultra skills"
- **Lições aprendidas:** Quando Dr. mandar URL de skill/conceito, considerar o padrão: ele quer integrar/transformar, não só ver descrição
- **Ação preventiva:** Na dúvida entre "só referência" vs "transformar", assumir transformação e confirmar com ação concreta em vez de pergunta passiva
- **Sub-agent?** Não

## Padrões Identificados

_(Atualizar conforme erros se acumulam)_

1. **Verificar antes de copiar** — sempre comparar source/dest
2. **Inferir intenção, não descrever** — quando o contexto sugere ação, propôr a ação

## Métricas (atualizar mensalmente)

- Total de erros registrados: 2
- Erros repetidos: 0
- Taxa de melhoria: N/A (mês 1)
