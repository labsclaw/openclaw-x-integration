#!/usr/bin/env node
/**
 * Self-Improving Browser Loop
 * 
 * Adapted from browserbase/skills autobrowse pattern.
 * Iterates: run task → capture trace → analyze failures → improve strategy → repeat.
 * 
 * Usage:
 *   node self-improving-loop.mjs --task <name> --url <url> [--max-iterations 5]
 * 
 * Workflow:
 *   1. Read task.md for the goal and steps
 *   2. Read strategy.md for current approach
 *   3. Execute the task via OpenClaw browser tool
 *   4. Capture trace (CDP events + screenshots)
 *   5. Analyze what went wrong
 *   6. Update strategy.md with improvements
 *   7. Repeat until pass or max iterations
 * 
 * Output: improved strategy.md + trace history in .o11y/<task>/
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.resolve(__dirname, '../../..');

// ── CLI args ─────────────────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { task: null, url: null, maxIterations: 5, workspace: WORKSPACE };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--task' && args[i + 1]) result.task = args[++i];
    else if (args[i] === '--url' && args[i + 1]) result.url = args[++i];
    else if (args[i] === '--max-iterations' && args[i + 1]) result.maxIterations = parseInt(args[++i]);
    else if (args[i] === '--workspace' && args[i + 1]) result.workspace = args[++i];
  }

  if (!result.task) {
    console.error('Usage: self-improving-loop.mjs --task <name> --url <url> [--max-iterations N]');
    process.exit(1);
  }

  return result;
}

// ── File helpers ─────────────────────────────────────────────────────────────

function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }

function readMd(p, fallback = '') {
  try { return fs.readFileSync(p, 'utf8'); } catch { return fallback; }
}

function writeMd(p, content) {
  ensureDir(path.dirname(p));
  fs.writeFileSync(p, content, 'utf8');
}

function readJson(p, fallback = null) {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return fallback; }
}

function writeJson(p, obj) {
  ensureDir(path.dirname(p));
  fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n');
}

// ── Core loop ────────────────────────────────────────────────────────────────

function getTaskDir(config) {
  return path.join(config.workspace, 'autobrowse', 'tasks', config.task);
}

function getStrategyPath(config) {
  return path.join(getTaskDir(config), 'strategy.md');
}

function getTaskPath(config) {
  return path.join(getTaskDir(config), 'task.md');
}

function getTraceDir(config, iteration) {
  const dir = path.join(config.workspace, 'autobrowse', 'traces', config.task, `iter-${String(iteration).padStart(3, '0')}`);
  ensureDir(dir);
  return dir;
}

function getReportPath(config) {
  return path.join(config.workspace, 'autobrowse', 'reports', `${config.task}.json`);
}

function scaffoldTask(config) {
  const taskDir = getTaskDir(config);
  ensureDir(taskDir);
  
  const taskPath = getTaskPath(config);
  if (!fs.existsSync(taskPath)) {
    writeMd(taskPath, `# Task: ${config.task}

## Goal
Describe what this task should accomplish.

## URL
${config.url || 'TBD'}

## Steps
1. Navigate to the URL
2. [Add specific steps here]

## Expected Output
Describe what success looks like.

## Failure Conditions
- What would constitute a failure?
`);
    console.log(`Created task template at ${taskPath}`);
  }

  const strategyPath = getStrategyPath(config);
  if (!fs.existsSync(strategyPath)) {
    writeMd(strategyPath, `# Strategy: ${config.task}

## Approach
Start with the simplest approach:
1. Navigate to the URL
2. Identify key elements by accessibility role/name
3. Interact with elements using browser tool
4. Verify result

## Lessons Learned
(none yet)

## Anti-patterns
(none yet)
`);
    console.log(`Created strategy template at ${strategyPath}`);
  }
}

function analyzeIteration(traceDir, taskDir) {
  const summaryPath = path.join(traceDir, 'cdp', 'summary.json');
  const summary = readJson(summaryPath);
  
  if (!summary) {
    return { passed: false, reason: 'No trace summary found', errors: [], networkErrors: [], consoleErrors: [] };
  }

  const errors = [];
  const networkErrors = [];
  const consoleErrors = [];

  // Check for network failures
  const failedPath = path.join(traceDir, 'cdp', 'network', 'failed.jsonl');
  if (fs.existsSync(failedPath)) {
    const failedLines = fs.readFileSync(failedPath, 'utf8').split('\n').filter(Boolean);
    for (const line of failedLines) {
      try {
        const ev = JSON.parse(line);
        networkErrors.push({
          requestId: ev.params?.requestId,
          errorText: ev.params?.errorText,
          type: ev.params?.type,
        });
      } catch {}
    }
  }

  // Check for console errors
  const consolePath = path.join(traceDir, 'cdp', 'console', 'logs.jsonl');
  if (fs.existsSync(consolePath)) {
    const logLines = fs.readFileSync(consolePath, 'utf8').split('\n').filter(Boolean);
    for (const line of logLines) {
      try {
        const ev = JSON.parse(line);
        if (ev.params?.type === 'error') {
          consoleErrors.push({
            text: ev.params?.args?.[0]?.value || 'Unknown error',
            url: ev.params?.source,
          });
        }
      } catch {}
    }
  }

  // Check for runtime exceptions
  const exceptionsPath = path.join(traceDir, 'cdp', 'console', 'exceptions.jsonl');
  if (fs.existsSync(exceptionsPath)) {
    const exLines = fs.readFileSync(exceptionsPath, 'utf8').split('\n').filter(Boolean);
    for (const line of exLines) {
      try {
        const ev = JSON.parse(line);
        errors.push({
          text: ev.params?.exceptionDetails?.text,
          url: ev.params?.exceptionDetails?.url,
        });
      } catch {}
    }
  }

  return {
    passed: errors.length === 0 && networkErrors.filter(e => !e.type?.includes('image')).length === 0 && consoleErrors.length === 0,
    reason: errors.length > 0 ? `${errors.length} runtime exceptions` :
            networkErrors.length > 0 ? `${networkErrors.length} network failures` :
            consoleErrors.length > 0 ? `${consoleErrors.length} console errors` : 'All checks passed',
    errors,
    networkErrors,
    consoleErrors,
    summary,
  };
}

function updateStrategy(config, iteration, analysis, strategyContent) {
  const timestamp = new Date().toISOString();
  const newSection = `\n\n## Iteration ${iteration} (${timestamp})\n\n### Result: ${analysis.passed ? 'PASSED' : 'FAILED'}\n\n`;
  
  let additions = '';
  
  if (analysis.errors.length > 0) {
    additions += `### Runtime Errors\n`;
    for (const err of analysis.errors) {
      additions += `- ${err.text} (at ${err.url || 'unknown'})\n`;
    }
    additions += `\n**Lesson:** These are JavaScript exceptions. Check element selectors and timing.\n`;
  }
  
  if (analysis.networkErrors.length > 0) {
    additions += `### Network Failures\n`;
    for (const err of analysis.networkErrors) {
      additions += `- ${err.errorText} (${err.type || 'unknown type'})\n`;
    }
    additions += `\n**Lesson:** Some resources failed to load. Consider retrying or using different approach.\n`;
  }
  
  if (analysis.consoleErrors.length > 0) {
    additions += `### Console Errors\n`;
    for (const err of analysis.consoleErrors) {
      additions += `- ${err.text}\n`;
    }
    additions += `\n**Lesson:** Console errors indicate underlying issues. Investigate root cause.\n`;
  }
  
  if (analysis.passed) {
    additions += `### Success! Strategy is working.\n`;
    additions += `Keep this approach for future runs.\n`;
  }

  const updated = strategyContent + newSection + additions;
  writeMd(getStrategyPath(config), updated);
  return updated;
}

async function runIteration(config, iteration) {
  const traceDir = getTraceDir(config, iteration);
  const taskDir = getTaskDir(config);
  
  console.log(`\n=== Iteration ${iteration} ===`);
  
  // Read current strategy
  const strategy = readMd(getStrategyPath(config));
  const task = readMd(getTaskPath(config));
  
  // Save iteration metadata
  writeJson(path.join(traceDir, 'iteration.json'), {
    task: config.task,
    iteration,
    timestamp: new Date().toISOString(),
    url: config.url,
  });
  
  // The actual browser execution would be done by the OpenClaw agent
  // This script provides the analysis and strategy update framework
  console.log(`Task: ${config.task}`);
  console.log(`URL: ${config.url}`);
  console.log(`Trace: ${traceDir}`);
  console.log(`Strategy length: ${strategy.length} chars`);
  
  return { traceDir, taskDir, strategy };
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const config = parseArgs();
  
  console.log(`Self-Improving Loop: ${config.task}`);
  console.log(`URL: ${config.url || 'from task.md'}`);
  console.log(`Max iterations: ${config.maxIterations}`);
  console.log(`Workspace: ${config.workspace}`);
  
  // Scaffold task directory
  scaffoldTask(config);
  
  // Initialize or load existing report
  const reportPath = getReportPath(config);
  const existingReport = readJson(reportPath, {
    task: config.task,
    iterations: [],
    finalStrategy: null,
  });
  
  const report = {
    ...existingReport,
    task: config.task,
    startedAt: new Date().toISOString(),
    iterations: existingReport.iterations || [],
  };
  
  // Save report
  writeJson(reportPath, report);
  
  console.log(`\nTask directory: ${getTaskDir(config)}`);
  console.log(`Report: ${reportPath}`);
  console.log(`\nReady for OpenClaw agent to execute iterations.`);
  console.log(`The agent should:`);
  console.log(`1. Read ${getTaskPath(config)} for the goal`);
  console.log(`2. Read ${getStrategyPath(config)} for current approach`);
  console.log(`3. Execute the task using browser tools`);
  console.log(`4. Capture trace using cdp-trace.mjs`);
  console.log(`5. Run: node ${path.join(__dirname, 'self-improving-loop.mjs')} --task ${config.task} --analyze ${iteration}`);
}

// Also support analysis mode
if (process.argv.includes('--analyze')) {
  const config = parseArgs();
  const iterIdx = process.argv.indexOf('--analyze') + 1;
  const iteration = parseInt(process.argv[iterIdx]) || 0;
  
  const traceDir = getTraceDir(config, iteration);
  const analysis = analyzeIteration(traceDir, getTaskDir(config));
  
  console.log(JSON.stringify(analysis, null, 2));
  
  // Update strategy
  const strategyContent = readMd(getStrategyPath(config));
  updateStrategy(config, iteration, analysis, strategyContent);
  
  // Update report
  const reportPath = getReportPath(config);
  const report = readJson(reportPath, { iterations: [] });
  report.iterations.push({
    iteration,
    timestamp: new Date().toISOString(),
    passed: analysis.passed,
    reason: analysis.reason,
    errorCount: analysis.errors.length,
    networkErrorCount: analysis.networkErrors.length,
    consoleErrorCount: analysis.consoleErrors.length,
  });
  report.finalStrategy = readMd(getStrategyPath(config));
  writeJson(reportPath, report);
  
  process.exit(analysis.passed ? 0 : 1);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
