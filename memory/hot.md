# HOT CACHE — Contexto Imediato da Sessão
# Reset a cada sessão. Máximo 500 palavras.

## Última sessão
- **Data**: 2026-07-22 05:09 GMT-3
- **Tema**: SSC Router v3.2 (Layered Indexing) & Upgrade Gemini 3.6 Flash
- **Status**: Concluído e 100% operacional

## Decisões & Mudanças
1. **Modelo Primary**: Atualizado para `antigravity-proxy/gemini-3.6-flash-high` (1.0M context, thinking high).
2. **Fallback Chain Enxuta**: Removido GPT-OSS (morto/HTTP 500) e enxugados modelos intermediários. Nova chain:
   `gemini-3.6-flash-high` → `nemotron-3-ultra-550b` → `deepseek-v4-flash` → `deepseek-v4-flash-free` → `hy3:free` → `big-pickle` → `gemini-3.5-flash` → `kimi-k2.6`.
3. **SSC Router v3.2 (Layered Indexing)**:
   - Tier 1: 12 Segments curados (`memory/segments/`, peso ×2.0).
   - Tier 2: 86 Daily Logs (`memory/daily/`, peso ×0.5).
   - Script de Rebuild automatizado (`scripts/ssc-rebuild.cjs`).
   - Zero-hit filtering no router (`memory/ssc-router.ps1`) para evitar falsos positivos.

## Próximos passos
- Monitorar performance do Gemini 3.6 Flash High durante tarefas complexas.
- Push dos novos scripts (`ssc-rebuild.cjs`, `ssc-router.ps1`) para o repositório de instruções/workspace.
