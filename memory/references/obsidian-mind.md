# Reference: obsidian-mind (Bruno Ferrari)

**Source:** https://github.com/breferrari/obsidian-mind
**Data de Análise:** 2026-07-22

## Visão Geral
Vault estruturado no Obsidian desenhado para dar memória persistente auto-organizável a agentes de código (Claude Code, Codex CLI, Gemini CLI). Combina lifecycle hooks, busca semântica via QMD, e grafo de notas.

## Principais Arquiteturas e Conceitos

### 1. QMD + MCP Server para Busca Semântica Local
- Usa `@tobilu/qmd` (Quick Markdown Database) rodando localmente com SQLite e modelos de embeddings.
- Expõe a busca como servidor MCP (`mcp__qmd__query`, `mcp__qmd__get`, `mcp__qmd__multi_get`).
- Permite que qualquer agente ou sub-agente consulte a memória de forma estruturada via MCP.

### 2. Ciclo de Vida Baseado em Hooks
- **SessionStart**: Indexação incremental no QMD, injeção leve do North Star, tarefas abertas, mudanças no git e lista de arquivos vault (~2k tokens).
- **UserPromptSubmit**: Hook executado a cada mensagem enviada, classifica a intenção (decisão, incidente, vitória, 1:1, arquitetura, pessoa) e injeta dicas de roteamento.
- **PostToolUse**: Executado após modificações em Markdown, valida frontmatter, links e avisa se a nota estiver grande demais (sugerindo split).
- **PreCompact**: Salva o transcript da sessão em `thinking/session-logs/` antes da compactação de contexto.
- **Stop**: Roda checklist e auditoria de higiene do vault.

### 3. Orquestração e Sub-Agentes Especializados
- `context-loader`: Carrega contexto sobre pessoa, projeto ou conceito.
- `cross-linker`: Encontra links ausentes, notas órfãs e backlinks quebrados.
- `vault-librarian`: Manutenção profunda de integridade do vault.
- `brag-spotter`: Detecta vitórias não capturadas para performance review.

## Comparativo com Nosso Setup (OpenClaw + SSC Router v3.2)

| Recurso | obsidian-mind | OpenClaw Setup |
|---|---|---|
| Motor de Recuperação | QMD (SQLite + Vector Embeddings + Reranker) | SSC Router v3.2 (Tier 1 Segments x2.0 + Tier 2 Daily x0.5) |
| Interface de Recuperação | MCP Server + CLI | PowerShell (`ssc-router.ps1`) + Node (`ssc-rebuild.cjs`) |
| Hooks de Mensagem | `UserPromptSubmit` (Classificação de intenção) | Transcrição padrão + Hot Cache (`memory/hot.md`) |
| Gestão de Contexto | Layered (~2k start + on-demand via QMD) | Dynamic Context Injection + Compaction |

## Lições e Ideias para Incorporar
1. **Message Classifier Hook**: Injetar contexto/dicas de memória de acordo com o tipo de mensagem do usuário.
2. **SSC Router como Ferramenta/MCP**: Expor a busca do SSC Router diretamente como contrato padrão para sub-agentes.
3. **Métrica de Custo de Injeção**: Exibir token meter para injeção inicial de contexto no startup.
