# S011 — Cross-Agent Coordination

**Status:** Ativo
**Criado:** 2026-07-24

## Contexto

Coordenação entre agentes (Justus/CEO, Robin/CTO, Luna/CMO) falhou via Telegram (síncrono, sem estrutura, perde contexto). GitHub privado (`paperclip-openclaw-handoff`) provou funcionar.

## Mecanismo

- **Repositório:** `labsclaw/paperclip-openclaw-handoff` (privado)
- **Espelho local:** `coordination/` no workspace
- **Pull frequente:** Sempre verificar inbox antes de agir

## Regras

1. Todo agente lê seu inbox no primeiro turno da sessão
2. `active.md` é atualizado ao iniciar/concluir tarefa cross-funcional
3. `decisions.md` é append-only — nunca editar
4. Handoff = tarefa no inbox do destino + commit + push

## Melhorias Pendentes

- Script de automação: `git pull` no início da sessão + notificar se inbox mudou
- Template de handoff com checklist
