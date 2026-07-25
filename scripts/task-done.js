// Helper: Marca uma tarefa como concluída, invalidando watchdogs
// Uso: node scripts/task-done.js <task-name>
//
// Cria um arquivo .done que o watchdog pode verificar.
// Também limpa o cron watchdog se ele ainda não disparou.

const fs = require('fs');
const path = require('path');

const [,, taskName] = process.argv;
if (!taskName) {
  console.error('Uso: node task-done.js <taskName>');
  process.exit(1);
}

const doneDir = path.join(__dirname, '..', 'logs', 'tasks');
fs.mkdirSync(doneDir, { recursive: true });

const doneFile = path.join(doneDir, `${taskName}.done`);
fs.writeFileSync(doneFile, JSON.stringify({
  task: taskName,
  completedAt: new Date().toISOString(),
  pid: process.pid
}, null, 2));

console.log(`✅ ${taskName} marcada como concluída em ${doneFile}`);
console.log(`Caminho do marcador: ${doneFile}`);
