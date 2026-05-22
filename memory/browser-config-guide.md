# Guia de Configuração e Uso do Browser no OpenClaw

Este documento contém instruções para usar o navegador Chromium-based do OpenClaw com o perfil do usuário (cookies, logins, extensões etc.).

## 1. Verificar Estado do Navegador
Antes de qualquer ação, confirme que o servidor de controle do navegador está ativo.

```json
{
  "action": "status"
}
```

- Se retornar `{"ready": true}` → prossiga
- Caso contrário, execute `{"action": "start"}` ou `{"action": "doctor"}` para diagnóstico

## 2. Listar Perfis Disponíveis
Veja se o perfil do seu usuário está configurado.

```json
{
  "action": "profiles"
}
```

Saída típica:
```json
{
  "profiles": [
    { "id": "default", "label": "Isolado (OpenClaw)" },
    { "id": "user", "label": "Seu perfil do Chrome" }
  ]
}
```

Procure por um perfil com `"id": "user"` (ou similar) - ele contém seus cookies, logins, extensões etc.

## 3. Abrir Aba com Perfil do Usuário
Use a ação `open` com `profile="user"` (ou o id que você viu no passo 2). Dê um label para referência futura.

```json
{
  "action": "open",
  "profile": "user",
  "url": "https://mail.google.com", // exemplo: abrir Gmail já logado
  "label": "gmail"
}
```

O retorno contém um `targetId` (ex.: `"t1"` ou o próprio label `"gmail"`). Guarde esse identificador.

## 4. (Opcional) Verificar a Aba Antes de Interagir
Para garantir que você está na aba correta e evitar refs obsoletos, tire um snapshot com refs estáveis (ARIA).

```json
{
  "action": "snapshot",
  "targetId": "gmail", // ou o targetId retornado no passo 3
  "refs": "aria",
  "urls": true,
  "labels": true
}
```

Isso devolve a estrutura da página com refs como `ax12`, `ax15`, etc., que você pode usar nas próximas etapas.

## 5. Executar Ação Desejada (Clique, Preenchimento, Navegação)
Use a ação `act` passando o ref obtido no snapshot.

Exemplo para clicar no botão “Compor” do Gmail (supondo que o snapshot tenha retornado um ref `ax7` com rótulo “Compor”):

```json
{
  "action": "act",
  "targetId": "gmail",
  "kind": "click",
  "ref": "ax7"
}
```

## 6. Gerenciar Abas (Fechar, Reutilizar, Evitar Duplicatas)
- Antes de abrir uma nova aba, liste as existentes: `{ "action": "tabs" }`
- Reutilize uma aba com o mesmo label quando ainda estiver válida – isso evita janelas fantasma
- Para fechar a aba após terminar: `{ "action": "close", "targetId": "gmail" }`

## 7. Tratamento de Bloqueios (Login, 2FA, Permissões)
Se durante o fluxo o navegador exibir uma tela de login, pedido de 2FA, permissão de câmera/microfone ou qualquer outro diálogo que exija intervenção humana:
1. Pare o script
2. Informe ao usuário exatamente o que aparece (texto do diálogo, botões necessários)
3. Aguarde a ação do usuário
4. Continue o script após a resolução

## 8. Boas-Práticas (da skill browser-automation)
- Sempre siga o fluxo: **navegar → snapshot → act → snapshot novamente** após mudanças de estado (modal, navegação, envio de formulário)
- Nunca confie em "blind waits" (esperas arbitrárias)
- Use refs estáveis (ARIA) sempre que possível para maior confiabilidade
- Após ações que mudam o estado da página (como navegação ou envio de formulário), tire um novo snapshot antes de continuar

## 9. Comandos Úteis do OpenClaw Browser
- `openclaw browser status` - Verifica status
- `openclaw browser start` - Inicia o navegador
- `openclaw browser stop --all` - Para todas as instâncias
- `openclaw browser profiles` - Lista perfis disponíveis

## Resumo dos Comandos Essenciais (JSON para a tool browser)

| Etapa | Comando JSON |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Verificar status | { "action": "status" } |
| Listar perfis | { "action": "profiles" } |
| Abrir URL no perfil do usuário | { "action": "open", "profile": "user", "url": "https://exemplo.com", "label": "minha_aba" } |
| Snapshot (refs ARIA) | { "action": "snapshot", "targetId": "minha_aba", "refs": "aria", "urls": true, "labels": true } |
| Clicar em elemento | { "action": "act", "targetId": "minha_aba", "kind": "click", "ref": "ax<number>" } |
| Preencher campo | { "action": "act", "targetId": "minha_aba", "kind": "fill", "ref": "ax<number>", "text": "valor a digitar" } |
| Navegar (URL direta) | { "action": "open", "profile": "user", "url": "https://outro.site", "targetId": "minha_aba" } |
| Fechar aba | { "action": "close", "targetId": "minha_aba" } |

## Observações Finais

• Não é necessário instalar plug‑ins externos; tudo vem com o OpenClaw (browser tool + a skill browser-automation).
• Se algum dia precisar de um navegador totalmente isolado (sem suas cookies), basta omitir profile="user" ou usar profile="default".
• Para fluxos mais complexos (login automático, tratamento de modais, espera por elementos), siga rigorosamente o loop da skill: status → tabs → open → snapshot → act → snapshot → ….

Pronto! Agora você pode abrir o Chrome com a sua sessão de usuário e realizar qualquer tarefa web usando apenas as ferramentas nativas do OpenClaw. Boa automação! 🚀