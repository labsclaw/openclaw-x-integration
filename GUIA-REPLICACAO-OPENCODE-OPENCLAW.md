# Guia de Replicação — opencode/big-pickle no OpenClaw

## Objetivo
Configurar o OpenClaw para usar o modelo `opencode/big-pickle` gratuitamente,
com a mesma velocidade e acesso que o CLI oficial do opencode, eliminando
erros `429 Rate limit exceeded / FreeUsageLimitError`.

## Pré-requisitos
- Node.js 20+ e npm instalados
- OpenClaw instalado globalmente: `npm install -g openclaw`
- CLI do opencode instalado (para extrair a API key)
- API key válida do opencode (free tier)

---

## 1. Obter a API Key do opencode

A API key fica no arquivo de configuração do CLI do opencode:

**Windows (PowerShell):**
```powershell
Get-Content "$env:USERPROFILE\.config\opencode\config.json"
```

**Linux/macOS:**
```bash
cat ~/.config/opencode/config.json
```

Copie o valor de `apiKey` (formato `sk-...`).

---

## 2. Arquivo de configuração de modelos

O OpenClaw busca configuração de modelos em dois lugares (por ordem de precedência):

1. **`~/.openclaw/agents/<agent-id>/agent/models.json`** — específico do agente (recomendado)
2. **`~/.openclaw/openclaw.json`** — configuração global (seção `models.providers`)

**Recomendação:** configure no `models.json` do agente (isolado por agente).
O gateway faz **hot reload** automático — não precisa reiniciar.

```bash
mkdir -p ~/.openclaw/agents/main/agent
```

---

## 3. Conteúdo do `models.json`

```json
{
  "providers": {
    "opencode": {
      "baseUrl": "https://opencode.ai/zen/v1",
      "api": "openai-completions",
      "headers": {
        "Accept": "*/*",
        "User-Agent": "opencode/1.15.5 ai-sdk/provider-utils/4.0.23 runtime/bun/1.3.14",
        "x-opencode-client": "cli",
        "x-opencode-project": "global",
        "x-opencode-session": "ses_minha_sessao",
        "x-opencode-request": "msg_minha_request"
      },
      "apiKey": "sk-xxx…xxxx",
      "models": [
        {
          "id": "big-pickle",
          "name": "Big Pickle",
          "reasoning": false,
          "input": ["text"],
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
          "contextWindow": 200000,
          "maxTokens": 128000,
          "compat": { "thinkingFormat": "deepseek" }
        },
        {
          "id": "deepseek-v4-flash-free",
          "name": "DeepSeek V4 Flash Free (OC)",
          "reasoning": false,
          "input": ["text"],
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
          "contextWindow": 262144,
          "maxTokens": 8192,
          "compat": { "thinkingFormat": "deepseek" }
        },
        {
          "id": "nemotron-3-super-free",
          "name": "Nemotron 3 Super Free (OC)",
          "reasoning": false,
          "input": ["text"],
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
          "contextWindow": 262144,
          "maxTokens": 8192
        },
        {
          "id": "minimax-m2.5-free",
          "name": "MiniMax M2.5 Free (OC)",
          "reasoning": false,
          "input": ["text"],
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
          "contextWindow": 196608,
          "maxTokens": 8192
        },
        {
          "id": "qwen3.6-plus-free",
          "name": "Qwen 3.6 Plus Free (OC)",
          "reasoning": false,
          "input": ["text"],
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
          "contextWindow": 262144,
          "maxTokens": 8192
        }
      ]
    }
  }
}
```

> **Nota sobre `apiKey`:** Colocar a chave direto no `models.json` é o mais
> simples para replicação. Se preferir usar o sistema de auth profiles do
> OpenClaw, veja a seção **Alternativa: usando auth profiles** no final.

---

## 4. 🔥 Headers — O Coração da Solução

Estes headers são **obrigatórios** para evitar o rate limit. O servidor
`opencode.ai` usa eles para identificar o cliente como oficial (CLI) vs
terceiro.

| Header | Valor | Obrigatório? |
|--------|-------|:---:|
| `Accept` | `*/*` | ✅ Sim |
| `User-Agent` | `opencode/1.15.5 ai-sdk/provider-utils/4.0.23 runtime/bun/1.3.14` | ✅ Sim |
| `x-opencode-client` | `cli` | ✅ Sim |
| `x-opencode-project` | `global` | ✅ Sim |
| **`x-opencode-session`** | **String estática qualquer (ex: `ses_openclaw`)** | **🔥 Essencial** |
| **`x-opencode-request`** | **String estática qualquer (ex: `msg_openclaw`)** | ✅ Sim |

### Por que funcionam?

A engenharia reversa revelou que o servidor diferencia requisições do CLI
oficial de clientes terceiros **exclusivamente pela presença desses headers**.
Sem eles o servidor aplica rate limits agressivos (429).

**Detalhe importante:** O servidor **não valida o conteúdo** de
`x-opencode-session` e `x-opencode-request` — apenas a **presença** dos
headers. Strings estáticas funcionam perfeitamente.

---

## 5. 🔥 `compat.thinkingFormat: "deepseek"` — Essencial para DeepSeek

O `big-pickle` roteia internamente para **DeepSeek V4 Flash**. DeepSeek
retorna `reasoning_content` nas respostas. Sem `thinkingFormat: "deepseek"`,
o OpenClaw **remove** esse campo do histórico antes da próxima requisição,
e a API do DeepSeek rejeita com:

```
400: The reasoning_content in the thinking mode must be passed back to the API
```

Adicione `compat` a **todo modelo que roteia para DeepSeek**:

```json
"compat": {
  "thinkingFormat": "deepseek"
}
```

Modelos **não-DeepSeek** (Nemotron, MiniMax, Qwen) **não precisam** desta
configuração.

---

## 6. ⚠️ `api: "openai-completions"` — Não use "openai-responses"

O modelo `big-pickle` **não aceita** o formato `openai-responses` (retorna 401).
Use exclusivamente:

```json
"api": "openai-completions"
```

---

## 7. Configurar modelo primário e fallbacks no `openclaw.json`

No `~/.openclaw/openclaw.json`, configure:

```json
{
  "agents": {
    "defaults": {
      "thinkingDefault": "off",
      "model": {
        "primary": "opencode/big-pickle",
        "fallbacks": [
          "nvidia/nemotron-3-super-120b-a12b",
          "openrouter/qwen/qwen3-coder:free",
          "opencode/deepseek-v4-flash-free"
        ]
      }
    }
  }
}
```

### Fallbacks recomendados

| Provedor | ID | Requer |
|----------|----|--------|
| NVIDIA (gratuito) | `nvidia/nemotron-3-super-120b-a12b` | Chave em https://build.nvidia.com |
| OpenRouter (gratuito) | `openrouter/qwen/qwen3-coder:free` | Chave em https://openrouter.ai |
| opencode (gratuito) | `opencode/deepseek-v4-flash-free` | Mesma chave do opencode |

### `thinkingDefault: "off"`

Desabilita thinking automático no agente — evita conflitos com modelos que
não suportam ou têm comportamento imprevisível com reasoning ativo.

---

## 8. Configurar provedores auxiliares

### NVIDIA
```bash
openclaw auth add nvidia:default
# Cole a chave gratuita de https://build.nvidia.com
```

No `models.json` ou `openclaw.json`, adicione o provedor:

```json
"nvidia": {
  "baseUrl": "https://integrate.api.nvidia.com/v1",
  "api": "openai-completions",
  "models": [
    {
      "id": "nvidia/nemotron-3-super-120b-a12b",
      "name": "Nemotron 3 Super 120B",
      "reasoning": false,
      "input": ["text"],
      "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
      "contextWindow": 262144,
      "maxTokens": 8192,
      "compat": { "requiresStringContent": true }
    }
  ]
}
```

### OpenRouter
```bash
openclaw auth add openrouter:default
# Cole a chave de https://openrouter.ai
```

```json
"openrouter": {
  "baseUrl": "https://openrouter.ai/api/v1",
  "api": "openai-completions",
  "headers": {
    "X-Title": "OpenClaw",
    "HTTP-Referer": "http://localhost:18789"
  },
  "models": [
    {
      "id": "openrouter/qwen/qwen3-coder:free",
      "name": "Qwen 3 Coder (OpenRouter)",
      "reasoning": false,
      "input": ["text"],
      "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
      "contextWindow": 131072,
      "maxTokens": 8192
    }
  ]
}
```

---

## 9. Recarregar e verificar

O gateway faz **hot reload** automático ao detectar mudanças nos arquivos
de configuração. Log esperado:

```
config hot reload applied (models.providers.opencode.models)
agent model: opencode/big-pickle (thinking=off, fast=off)
```

Se quiser forçar reinicialização:

```powershell
openclaw gateway restart
```

Verifique o status:

```powershell
openclaw gateway status
# Deve mostrar o modelo ativo como opencode/big-pickle
```

---

## 10. Diagnóstico de Problemas

### 429 FreeUsageLimitError
**Causa:** Headers `x-opencode-session` e/ou `x-opencode-request` ausentes.
**Solução:** Adicione os headers no provedor `opencode`.

### 401 Model not supported for format openai
**Causa:** `api` configurado como `"openai-responses"`.
**Solução:** Use `"api": "openai-completions"`.

### 400 reasoning_content must be passed back
**Causa:** Modelo DeepSeek sem `compat.thinkingFormat`.
**Solução:** Adicione `"compat": {"thinkingFormat": "deepseek"}` ao modelo.

### Model not found
**Causa:** Modelo não definido na lista `models` do provedor.
**Solução:** Adicione a entrada correspondente.

### Conversa cai para fallback sem motivo aparente
**Causa:** Gateway usando modelo diferente do esperado.
**Solução:** Verifique `openclaw gateway log --tail | grep "model_call"`.

### Sessões presas em "processing" / "model_call"
Durante o rate limit, sessões ficam presas. Remova manualmente:
```powershell
Remove-Item ~\.openclaw\agents\main\sessions\*.jsonl -ErrorAction SilentlyContinue
```

---

## 11. Alternativa: usando auth profiles (sem `apiKey` no models.json)

Se preferir não colocar a chave no `models.json`, configure via auth profiles:

No `openclaw.json`:
```json
{
  "auth": {
    "profiles": {
      "opencode:default": {
        "provider": "opencode",
        "mode": "api_key"
      }
    }
  }
}
```

E defina a chave:
```bash
openclaw auth add opencode:default
```

Nesse caso, **remova** o campo `apiKey` do provedor `opencode` no `models.json`,
e adicione a chave via variável de ambiente no `~/.openclaw/.env`:
```env
OPENCODE_API_KEY=sk-xxx…xxxx
```

---

## 12. Verificação final

Teste com uma requisição direta (equivalente ao que o CLI envia):

```bash
curl -X POST "https://opencode.ai/zen/v1/chat/completions" ^
  -H "Authorization: Bearer sk-xxx…xxxx" ^
  -H "Content-Type: application/json" ^
  -H "Accept: */*" ^
  -H "User-Agent: opencode/1.15.5 ai-sdk/provider-utils/4.0.23 runtime/bun/1.3.14" ^
  -H "x-opencode-client: cli" ^
  -H "x-opencode-project: global" ^
  -H "x-opencode-session: ses_openclaw" ^
  -H "x-opencode-request: msg_openclaw" ^
  -d "{\"model\":\"big-pickle\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}],\"max_tokens\":100}"
```

Se responder sem 429, a configuração está correta.

---

## Estrutura final dos arquivos

```
~/.openclaw/
├── openclaw.json                     # Config global (modelo primário, fallbacks, auth)
├── agents/
│   └── main/
│       └── agent/
│           └── models.json           # Modelos do agente "main"
├── archive/                          # Histórico da investigação (referência)
│   ├── CADEIA-DE-RACIOCINIO.md
│   ├── SOLUCAO-API-LIMIT-OPENCODE.md
│   └── TUTORIAL-TECNICO-API-LIMIT-OPENCODE.md
└── gateway.cmd
```

---

## Informações técnicas (resumo)

- O servidor `https://opencode.ai/zen/v1` roteia `big-pickle` → `deepseek-v4-flash`
- O rate limit é baseado em **fingerprint de headers**, não em API key
- `x-opencode-session` é o header **crítico** que separa requests "limitados" de "permitidos"
- Strings estáticas para `x-opencode-session` e `x-opencode-request` funcionam
- O gateway do OpenClaw faz **hot reload** automático de alterações em modelos

---

*Guia mantido por Dr. Roger Oliveira (@SmartNewbieBR).*
*Engenharia reversa original via proxy inspection do tráfego opencode × OpenClaw.*
