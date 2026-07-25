# Grok Build Analysis

Repo: https://github.com/xai-org/grok-build
Data: 2026-07-25
Source: Clone do repo (2896 files, 50+ crates Rust)

---

## 1. Como Chamar API Grok (Integracao estilo Antigravity)

### Endpoints xAI (inferidos do codigo)

| Backend | Path | Formato |
|---------|------|---------|
| Chat Completions | `POST /v1/chat/completions` | OpenAI-compativel |
| Responses API | `POST /v1/responses` | OpenAI Responses API |
| Anthropic Messages | `POST /v1/messages` | Anthropic Messages API |
| Embeddings | `POST /v1/embeddings` | OpenAI-compativel |

### Authentication

O client suporta dois esquemas:
- **Bearer**: `Authorization: Bearer <api-key>`
- **XApiKey**: `X-Api-Key: <api-key>`

Configuracao via `SamplerConfig`:
```rust
SamplerConfig {
    api_key: Option<String>,
    base_url: String,          // ex: "https://api.x.ai/v1"
    model: String,             // ex: "grok-4.5"
    auth_scheme: AuthScheme,   // Bearer (default) ou XApiKey
    api_backend: ApiBackend,   // ChatCompletions (default), Responses, Messages
    extra_headers: IndexMap,   // headers extras
    force_http1: bool,
    max_retries: Option<u32>,
    stream_tool_calls: bool,
}
```

Nao ha nada especial no esquema de auth -- e OpenAI-compativel. **Podemos adicionar Grok como modelo no antigravity proxy simplesmente apontando pra `https://api.x.ai/v1` com `Authorization: Bearer <xai-key>`.**

### Models Disponiveis

Do `default_models.json`:
```json
{
  "default": "grok-4.5",
  "models": [
    {
      "id": "grok-4.5",
      "model": "grok-4.5",
      "context_window": 500000,
      "api_backend": "responses",
      "supports_reasoning_effort": true,
      "reasoning_effort": "high",
      "reasoning_efforts": ["high", "medium", "low"]
    }
  ]
}
```

500K tokens de contexto. Suporta `reasoning_effort` (high/medium/low).

### Streaming

SSE padrao OpenAI. Usam `eventsource-stream` crate. Incluem:
- `stream: true` + `stream_options: { include_usage: true }`
- Tratamento de BOM UTF-8 (byte 0xEF 0xBB 0xBF)
- `[DONE]` como terminador
- Erro de transporte so emitido uma vez (scan com `had_transport_error`)

### Web Search Nativo

O modelo Grok tem search **nativa** (nao e tool -- e parametro do request):
```json
{
  "search_parameters": {
    "mode": "on" | "off" | "auto",
    "sources": [
      { "type": "web", "allowed_websites": [...], "country": "BR", "safe_search": true },
      { "type": "x", "included_x_handles": [...], "excluded_x_handles": [...] },
      { "type": "news", "excluded_websites": [...], "country": "BR" },
      { "type": "rss", "links": [...] }
    ],
    "from_date": "YYYY-MM-DD",
    "to_date": "YYYY-MM-DD",
    "return_citations": true,
    "max_search_results": 10
  }
}
```

Isso e **gigante** -- o modelo decide quando buscar, sem precisar de tool call explicita. O search e feito server-side.

### Resposta com Citacoes

```json
{
  "citations": ["https://..."],
  "choices": [{
    "message": {
      "citations": ["https://..."],
      "reasoning_content": "..."
    }
  }]
}
```

---

## 2. Tecnicas & Skills Capturaveis

### 2.1 ACP (Agent Client Protocol)

O grok-build implementa o **ACP** -- um protocolo JSON sobre stdin/stdout que permite:
- Embedar o agente em qualquer editor/IDE
- Comunicacao bidirecional (agente envia eventos, cliente envia comandos)
- Tipos: `AcpAgentMessage`, `AcpClientMessage`, `AcpMethod`, `AcpRequest`
- Canal: `AcpChannel` com `AgentGatewaySender/Receiver`

**Pra gente:** Implementar um ACP adapter no Paperclip permitiria usar grok-build como runtime de agente. E um protocolo aberto e simples.

### 2.2 Sistema de Ferramentas (Tools)

Arquitetura:
- `xai-grok-tools` contem TODAS as implementacoes de ferramentas
- `xai-tool-runtime` gerencia execucao
- `xai-tool-protocol` define tipos de protocolo
- Ferramentas bridge (opencode, codex) adaptam tools de outros ecossistemas

Tools implementadas:
- **BashTool** - execucao de comandos
- **ReadFile/WriteFile/EditFile** - operacoes de arquivo
- **SearchReplaceTool** - busca e substitui
- **GrepTool** - busca em codigo
- **ListDirTool** - listagem de diretorios
- **WebSearchTool** - busca na web (via Responses API)
- **WebFetchTool** - fetch de URL
- **MemoryGet/MemorySearch** - memoria persistente
- **TaskTool** - tasks em background
- **TodoWriteTool** - checklist tracking
- **UseTool** - usar output de outra tool como input
- **LSP tools** - integracao com LSP (completions, diagnostics, hover, references, formatting)
- **Skill tools** - sistema de skills
- **AskUserQuestion** - perguntar ao usuario
- **EnterPlanMode/ExitPlanMode** - modo de planejamento

Cada tool tem: definicao (schema JSON), implementacao (trait), e tipos de input/output.

### 2.3 Sistema de Memoria (RAG)

Implementacao propria, nao depende de servico externo:
- **Storage**: arquivos Markdown em `~/.grok/memory/`
- **Escopo**: global (`MEMORY.md`) e por workspace (`{hash}/MEMORY.md`)
- **Sessoes**: logs em `sessions/YYYY-MM-DD-{slug}-{sid8}.md`
- **Chunker**: divide markdown em chunks
- **Embedding**: API OpenAI-compativel (`POST /v1/embeddings`)
- **Index**: sqlite-vec (sqlite com extensao vetorial)
- **Search**: busca por similaridade + MMR (Maximum Marginal Relevance) pra diversificar resultados
- **Query Expansion**: expande a query do usuario pra melhorar recall
- **Watcher**: monitora arquivos por mudancas
- **Archive**: compactacao de sessoes antigas
- **Dream**: replay de sessoes pra consolidar conhecimento (ciclo noturno)

**Pra gente:** Nosso SSC ja faz algo similar mas em Node. O diferencial do grok e o sqlite-vec + MMR. Podemos capturar a ideia de chunking markdown + query expansion.

### 2.4 Sistema de Skills

Skills sao ferramentas carregadas dinamicamente:
- **Discovery**: encontra skills no workspace (similar ao nosso `clawhub`)
- **Skill**: definicao, ciclo de vida, execucao
- **Types**: schemas de input/output

### 2.5 MCP (Model Context Protocol)

Crate `xai-grok-mcp` implementa:
- Cliente MCP (conexao com servidores MCP)
- Ferramentas expostas via MCP
- Resources (arquivos, etc) via MCP
- Suporta stdio e SSE como transporte

### 2.6 Sistema de Agentes (xai-grok-agent)

- **Agent** = tools + system prompt + reminder policy + compaction + model config
- **AgentBuilder**: constroi Agent fluentemente
- **AgentDefinition**: serializavel, pode vir de config
- **System prompt assembly**: composicao de prompts
- **CompactionPolicy**: quando e como compactar historico
- **ReminderPolicy**: lembretes periodicos pro modelo
- **Plugins**: hooks de plugins no ciclo de vida do agente
- **Discovery**: descobre agents configurados

### 2.7 Sandbox

Crate `xai-grok-sandbox`:
- Isolamento de execucao de codigo
- Limitacao de recursos
- Seguranca para ferramentas bash

### 2.8 HTTP Client com Pool Health

O `xai-grok-http` tem tecnicas de resiliencia notaveis:
- Pool idle timeout (30s) -- evita conexoes mortas do LB
- HTTP/2 keepalive ping (20s) -- detecta conexoes half-dead
- `send_with_retry_escaping_pool` -- ultima tentativa usa cliente HTTP/1.1 FRESCO (sem pool) pra escapar de pool envenenado
- `TransportFailureKind` classifica erro como Unreachable/Interrupted/Permanent
- `error_cause_chain()` junta cadeia de causes do reqwest

### 2.9 Model Resolution Pipeline

```
CLI flag > ENV var > config.toml > remote settings > defaults_models.json
```

Cada modelo tem:
- `api_backend` (ChatCompletions | Responses | Messages)
- `context_window` (para auto-compact)
- `reasoning_effort` (high/medium/low)
- `compactions_remaining` (controle de quantas compactacoes restam)

### 2.10 Doom Loop Recovery

Mecanismo anti-loop:
- Header `x-grok-doom-loop-check` opt-in
- Servidor reporta triggers de loop como eventos SSE
- `DoomLoopSignalCollector` absorve eventos e sinaliza loop
- `DoomLoopRecoveryPolicy` define threshold (max 8 triggers, 2 retries)

### 2.11 TUI (xai-grok-pager)

Full-screen terminal UI em Rust com ratatui:
- Scrollback infinito
- Modais interativos
- Renderizacao eficiente
- Suporte a mouse
- Temas customizaveis
- PTY harness para subprocessos

### 2.12 Hooks e Plugins

- **Hooks** (`xai-grok-hooks`): gatilhos em eventos do ciclo de vida (pre-tool, post-tool, etc)
- **Plugins** (`xai-grok-plugin-marketplace`): descoberta e instalacao de plugins
- **Plugin types** (`xai-hooks-plugins-types`): definicoes de tipos compartilhados

---

## 3. Conclusao: O Que Podemos Usar

### Acao Imediata

1. **Adicionar Grok no antigravity proxy** -- API OpenAI-compativel em `https://api.x.ai/v1`. So precisa de API key xAI. Modelo `grok-4.5` com 500K context.

2. **Usar `search_parameters` no ChatCompletionRequest** -- search nativo do Grok e superior a web_search tool. Basta passar `search_parameters.mode: "auto"` no request.

### Para Capturar (Tecnicas)

| Tecnica | Pra que serve |
|---------|---------------|
| ACP protocol | Embedar agentes em editors |
| sqlite-vec + MMR | Nosso SSC poderia usar sqlite-vec em vez de pesquisa linear |
| query expansion | Melhorar recall da busca semantica |
| doom loop recovery | Nosso agente tambem precisa |
| pool-escaping retry | Cliente HTTP mais resiliente |
| markdown chunker | Nosso memory system |
| LSP integration | Tools que entendem o codigo (completions, diags) |
| bridge tools (opencode, codex) | Adaptar tools de outros ecossistemas |
| skill discovery | Similar ao clawhub |
