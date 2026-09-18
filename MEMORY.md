# MEMORY.md — Hub Central

> Contexto carregado em toda sessão. Manter curto, atual e livre de regras operacionais duplicadas.
> Fonte detalhada: `memory/segments/` + `memory/index.json`.

## Segmentos SSC

| ID | Segmento | Arquivo |
|----|----------|---------|
| s001 | Infraestrutura & Env | `memory/segments/s001-infra.md` |
| s002 | Paperclip & Issues | `memory/segments/s002-paperclip.md` |
| s003 | Heartbeat & Alert Storm | `memory/segments/s003-heartbeat.md` |
| s004 | Skills & Projetos | `memory/segments/s004-skills.md` |
| s005 | Wiki & Hybrid Memory | `memory/segments/s005-wiki-hybrid.md` |
| s006 | SSC & Memory Architecture | `memory/segments/s006-ssc-skill-incident.md` |
| s007 | Ultra-Memory-Core | `memory/segments/s007-2026-06-28.md` |
| s008 | Finanças & Investimentos | `memory/segments/s008-finance.md` |
| s009 | Error Tracking | `memory/segments/s009-error-tracking.md` |
| s010 | Fallback Bug OpenClaw | `memory/segments/s010-fallback-bug-openclaw.md` |
| s011 | Cross-Agent Coordination | `memory/segments/s011-cross-agent-coordination.md` |
| s012 | Social Media | `memory/segments/s012-social-media.md` |
| s013 | Eval Results | `memory/segments/s013-eval-results.md` |
| s014 | PWSH Migration | `memory/segments/s014-pwsh-migration.md` |
| s015 | Memory Protection | `memory/segments/s015-memory-protection.md` |
| s017 | AI Engineering Coach | `memory/segments/s017-ai-engineering-coach.md` |
| s017b | Grok Bot Analysis | `memory/segments/s017-grok-bot-analysis.md` |
| s018 | AI Coworker Benchmark | `memory/segments/s018-ai-coworker-benchmark.md` |
| s019 | Workspace Cleanup | `memory/segments/s019-workspace-cleanup.md` |
| rla-639 | Prospecção Revendedores | `memory/segments/rla-639-prospecao-revendedores.md` |
| squad-dev-plan | Squad Dev Plan | `memory/segments/squad-dev-plan.md` |
| squad-dev-status | Squad Dev Status | `memory/segments/squad-dev-status.md` |
| subagent-evolution | Subagent Evolution | `memory/segments/subagent-evolution.md` |
| x-testing-profile | X-Testing, Perfil Institucional | `memory/segments/x-testing-company-profile.md` |
| x-testing-org | X-Testing, Organograma | `memory/segments/x-testing-org-chart.md` |
| x-testing-contract | X-Testing, Contrato SANASA | `memory/segments/x-testing-sanasa-contract.md` |
| x-testing-sanasa | X-Testing, Operação SANASA | `memory/segments/x-testing-sanasa-operation.md` |
| x-testing-baseline | X-Testing, Baseline de Referência | `memory/segments/x-testing-baseline.md` |
| x-testing-standards-metrics | X-Testing, Padrões TestLink e Métricas | `memory/segments/x-testing-standards-metrics.md` |
| x-testing-paperclip-architecture | X-Testing, Arquitetura Paperclip | `memory/segments/x-testing-paperclip-architecture.md` |
| x-testing-execution-plan | X-Testing, Plano de Execução | `memory/segments/x-testing-execution-plan.md` |
| decision-2026-09-05 | Fábrica de Testes X-Testing com Agentes | `memory/segments/decision-2026-09-05-implementa-o-da-f-brica-de-testes-x-testing-com-agentes.md` |
| paper-submission-strategy | Estratégia de Submissão do Paper | `memory/segments/paper-submission-strategy.md` |
| opencode-integration | OpenCode Integration & Zen 403 | `memory/segments/openclaw-opencode-integration.md` |

**Inventário atual:** 34 segmentos indexados. Recuperação: `node scripts/ssc-router.cjs "<consulta>"`.

## Regras canônicas

- Regras operacionais: `AGENTS.md`.
- Personalidade e comunicação: `SOUL.md` e `IDENTITY.md`.
- Preferências do usuário: `USER.md`.
- Rotina de continuidade: `HEARTBEAT.md`.
- Não duplicar aqui limites de ferramentas, política de silêncio ou procedimentos sujeitos a mudança.

## Estado recente de alto valor

- 2026-09-18: projeto labsclaw/openclaw-opencode-integration validado e sincronizado no GitHub (Fases 0 a 3). Rota A (Harness ACP) e Rota B (CLI Backend) operacionais, contornando o erro 403 Forbidden da API Zen e capturando reasoning/thinking em tempo real no modelo opencode/mimo-v2.5-free. Gateway atualizado: cabeçalhos estáticos legados limpos, bloco acp configurado (backend acpx e opencode permitido) e mimo-v2.5-free integrado à cadeia oficial de fallbacks. Restart do Gateway via PM2 pendente para quando o operador retornar ao desktop.
- 2026-09-14: estratégia de submissão do paper revisada (segment paper-submission-strategy). Submissão RBGeo/ReGeo descartada. Foco: periódicos de Computação/IA (JoIS, Applied Intelligence, Expert Systems with Applications). Restrição: sem APC obrigatória. Fase 2 concluída, preparação experimental pendente.
- 2026-09-07: modelo health probes concluídos (gpt-5/5.1-pro/5.2/5.3-pro indisponíveis WMOFF; grok-4.5 falhou). Plano Mestre X-Testing (16 KPIs, 6 WPs, 6 sprints) indexado. Decision segment: Fábrica de Testes X-Testing com agentes aprovado. Sprint 1 pendente (projeto Paperclip + kickoff conectores ALM).
- 2026-09-04: secrets hygiene scan identificou 13 plaintext keys (auth profiles SQLite + models.json providers). Heartbeat QAI alterado para 2h. XTE-25 in_review, XTE-33/XTE-20 blocked. RLA-677 blocked (fotografia física inacessível).
- 2026-09-03: API key AMD Radeon Cloud criada e testada (DeepSeek-V4-Flash). GPT-5.6 Sol confirmado como modelo primário. Tutorial AMD Cloud publicado.
- 2026-09-02: operação X-Testing/SANASA em andamento. Registros devem usar português do Brasil e a terminologia "OS SANASA". RLA-671 concluída (automotive-vision skill, 75% acurácia). Pipeline visual Archify implementado. RF002/RF027/RF043/RF050/RF046/RF047/RF058/RF061 executados.
- 2026-08-31: incidente crítico no Paperclip relacionado à exposição de chave privada ainda exige acompanhamento de segurança.
- Persistem verificações de higiene de segredos, integridade SSC e atualização de versões por crons dedicados.

## Registro desta revisão

- `memory/reports/openclaw-config-audit-2026-09-02.md`
- Atualização automática: 2026-09-18 (dream cron). Índice SSC reconstruído (34 segmentos, 144 diários).

Detalhes históricos permanecem nos segmentos, relatórios e diários. Este hub não deve virar log cronológico.
