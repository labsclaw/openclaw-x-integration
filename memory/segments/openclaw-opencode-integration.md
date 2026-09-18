# OpenClaw OpenCode Integration & Solução do Erro 403 Zen

<!-- project: github.com/labsclaw/openclaw-opencode-integration -->

- **Data:** 2026-09-18
- **Repositório:** `https://github.com/labsclaw/openclaw-opencode-integration`
- **Organização:** `labsclaw`
- **Ambiente:** OpenClaw 2026.9.3, OpenCode CLI 1.18.30, Node.js v26.1.0, Windows 11

## Contexto e Diagnóstico

Em setembro de 2026, o endpoint Zen da OpenCode (`https://opencode.ai/zen/v1`) passou a validar se as requisições aos modelos gratuitos originam-se legitimamente de dentro do binário `opencode`. A emulação estática de headers HTTP (`x-opencode-session`, `x-opencode-project`, `User-Agent`, etc.) passou a retornar:

```
HTTP 403: OpenCode's free tier can only be used from within OpenCode
```

Além disso, o suporte a raciocínio estendido (**thinking**) nos modelos do OpenCode (como `mimo-v2.5-free`, `big-pickle`, etc.) é emitido nativamente pelo runtime local via streaming de eventos SSE (`reasoning`), e não por seletores de variantes nos headers HTTP.

## Arquitetura de Duas Rotas

Para resolver a causa raiz e garantir resiliência contra mudanças na API, foram desenvolvidas e validadas duas rotas:

### Rota A — Agente Nativo via ACPX (`opencode acp`)
- **Protocolo:** Agent Client Protocol (ACP) sobre stdio via JSON-RPC 2.0.
- **Implementação:** `src/acp-harness.js` gerencia subprocesso `opencode acp`, IDs correlacionados e eventos assíncronos.
- **Validação:** Handshake `initialize` com `protocolVersion: 1` e criação de sessão `session/new` (`test/test-acp.js`). O servidor OpenCode retornou capacidades ativas (`loadSession`, `promptCapabilities`, `sessionCapabilities`) e catálogo dinâmico de modelos.

### Rota B — CLI Backend para Fallbacks (`opencode run`)
- **Protocolo:** CLI Backend do OpenClaw (`@labsclaw/openclaw-opencode-cli`).
- **Implementação:** 
  - `src/adapter.js`: executa `opencode run --format json --thinking`, processa eventos SSE (`reasoning`, `text`, `step_finish`).
  - `src/cli-backend.js`: descritor canônico para `api.registerCliBackend` com suporte a reutilização de sessão (`-s {sessionId}`).
- **Validação:** Teste com `opencode/mimo-v2.5-free` capturando raciocínio em tempo real, sem 403 e com custo $0.00.

## Alterações de Configuração no Gateway (`openclaw.json`)

1. **Limpeza de headers legados:** Removidos os cabeçalhos de spoofing em `models.providers.opencode.headers`.
2. **Habilitação ACP:** Configurado bloco `acp` com `backend: "acpx"`, `dispatch.enabled: true` e `allowedAgents: ["claude", "codex", "gemini", "opencode"]`.
3. **Cadeia de Fallback:** Adicionado `opencode/mimo-v2.5-free` em `agents.defaults.model.fallbacks`.
4. **Backup:** Criado `openclaw.json.bak-phase3`.

## Ação Operacional Pendente
- **Restart PM2:** O Gateway precisa ser reiniciado no host (`pm2 restart openclaw-gateway`) quando o operador estiver no desktop para inicializar o listener do bloco `acp` desde o bootstrap.
