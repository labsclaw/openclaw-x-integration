// Helper: Registra watchdog via cron para tarefa longa
// Uso: node scripts/long-task-watchdog.js <task-name> <timeout-seconds>
//
// Cria um cron job agentTurn que dispara em (agora + timeout + 30s).
// O job me acorda na sessão atual pra verificar se a tarefa concluiu.
// O job NÃO se auto-destrói automaticamente com deleteAfterRun.
//
// ⚠️ IMPORTANTE: Após o watchdog disparar, remover manualmente:
//    cron(action="remove", jobId="<id>")
//
// Exemplo:
//   node scripts/long-task-watchdog.js "benchmark-m3" 120
//     → dispara em 150s, me acorda pra verificar

const [,, taskName, timeoutSec] = process.argv;

if (!taskName || !timeoutSec) {
  console.error('Uso: node long-task-watchdog.js <taskName> <timeoutSec>');
  console.error('  taskName   - identificador único da tarefa');
  console.error('  timeoutSec - timeout esperado em segundos');
  process.exit(1);
}

const delay = (parseInt(timeoutSec) + 30) * 1000;
const fireAt = new Date(Date.now() + delay).toISOString();
const donePath = `logs/tasks/${taskName}.done`;

const cronDef = {
  name: `wd:${taskName}`,
  description: `Watchdog: ${taskName}. Remover manualmente após disparo.`,
  schedule: { kind: 'at', at: fireAt },
  sessionTarget: 'current',
  deleteAfterRun: false,
  enabled: true,
  payload: {
    kind: 'agentTurn',
    message: `🔔 [WATCHDOG] Tarefa "${taskName}" — prazo expirou.
   Arquivo de conclusão esperado: ${donePath}
   Se existe: tarefa OK — remover cron job e ignorar.
   Se NÃO existe: a tarefa pode ter falhado. Investigar.
   cleanup: cron(action="list") → pegar jobId → cron(action="remove", jobId="<id>")`
  },
  delivery: { mode: 'announce' }
};

process.stdout.write(JSON.stringify(cronDef, null, 2));
