# Sub-Agent System Evolution Task

## Problema Identificado (2026-07-18)
O modelo atual (mimo-v2.5-free) entrou em loop de repetição — a mesma mensagem foi gerada 4x consecutivas. Isso indica:
1. Sem deduplicação de sub-agents spawned
2. Sem detecção de loops de resposta
3. Sem rate limit em spawn de sessões
4. Modelo sem circuit breaker pra output repetido

## Objetivo
Evoluir o sistema de sub-agents pra ser tão robusto quanto o sistema de memória que construímos.

## Áreas de Melhoria

### 1. Spawn Deduplication
- Antes de spawnar sub-agent, verificar se já existe tarefa equivalente ativa
- Usar sessions_list pra checar sessões recentes com mesmo task/tipo
- Implementar lock por task signature (hash do task description)

### 2. Loop Detection
- Monitorar output do modelo: se N respostas consecutivas são idênticas (>90% similarity), cortar
- Implementar no gateway ou como wrapper do sessions_spawn
- Circuit breaker: após 2 repetições, forçar stop e alertar

### 3. Sub-Agent Health Monitoring
- Pipeline monitor precisa rastrear health dos sub-agents, não só progresso
- Se sub-agent retorna mesma resposta >2x, marcar como unhealthy
- Auto-restart ou fallback pra modelo diferente

### 4. Model Rotation
- Se modelo entra em loop, tentar fallback pra outro modelo
- Configurar fallbacks no cron/sessions_spawn
- Log de qual modelo causou loop pra pattern detection

### 5. Spawn Rate Control
- Max N sub-agents simultâneos
- Cooldown entre spawns pra mesma tarefa
- Queue system pra tarefas concorrentes

## Priorização
1. **Loop Detection** — impacto imediato, evita desperdício de tokens
2. **Spawn Deduplication** — previne o problema raiz
3. **Model Rotation** — resiliência quando um modelo falha
4. **Health Monitoring** — visibilidade
5. **Rate Control** — proteção de capacidade

## Métricas de Sucesso
- Zero respostas duplicadas em 7 dias
- Sub-agents completam sem loop em 95% dos casos
- Tempo médio de detecção de loop < 30s
