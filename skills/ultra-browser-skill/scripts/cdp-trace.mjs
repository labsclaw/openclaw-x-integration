#!/usr/bin/env node
/**
 * CDP Trace Capture for OpenClaw
 * 
 * Adapted from browserbase/skills browser-trace pattern.
 * Connects to a Chrome instance via CDP WebSocket and captures:
 * - Network requests/responses
 * - Console messages
 * - Runtime exceptions
 * - Page navigations
 * - Periodic screenshots via OpenClaw browser tool
 * 
 * Usage:
 *   node cdp-trace.mjs start <ws-url-or-port> [run-id]
 *   node cdp-trace.mjs stop <run-id>
 *   node cdp-trace.mjs bisect <run-id>
 *   node cdp-trace.mjs status <run-id>
 * 
 * Output goes to .o11y/<run-id>/
 *   manifest.json, cdp/raw.ndjson, cdp/summary.json
 *   screenshots/, dom/, index.jsonl
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { WebSocket } from 'ws' in process.binding ? 'ws' : 'node:child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const O11Y_ROOT = process.env.O11Y_ROOT || '.o11y';

// ── Helpers ──────────────────────────────────────────────────────────────────

function runDir(runId) { return path.join(O11Y_ROOT, runId); }
function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }
function isoUtc() { return new Date().toISOString().replace(/\.\d+Z$/, 'Z'); }
function isoStamp() { return new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, ''); }

function readJson(p, fallback = null) {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return fallback; }
}
function writeJson(p, obj) {
  ensureDir(path.dirname(p));
  fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n');
}
function readJsonl(p) {
  if (!fs.existsSync(p)) return [];
  return fs.readFileSync(p, 'utf8').split('\n').filter(Boolean).map(l => {
    try { return JSON.parse(l); } catch { return null; }
  }).filter(Boolean);
}
function writeJsonl(p, items, { skipEmpty = false } = {}) {
  if (skipEmpty && items.length === 0) {
    if (fs.existsSync(p)) fs.unlinkSync(p);
    return;
  }
  ensureDir(path.dirname(p));
  fs.writeFileSync(p, items.map(o => JSON.stringify(o)).join('\n') + (items.length ? '\n' : ''));
}

// CDP domain buckets
const BUCKETS = [
  ['network/requests',    m => m === 'Network.requestWillBeSent'],
  ['network/responses',   m => m === 'Network.responseReceived'],
  ['network/finished',    m => m === 'Network.loadingFinished'],
  ['network/failed',      m => m === 'Network.loadingFailed'],
  ['network/websocket',   m => m.startsWith('Network.webSocket')],
  ['console/logs',        m => m === 'Runtime.consoleAPICalled'],
  ['console/exceptions',  m => m === 'Runtime.exceptionThrown'],
  ['runtime/all',         m => m.startsWith('Runtime.')],
  ['log/entries',         m => m === 'Log.entryAdded'],
  ['page/navigations',    m => m === 'Page.frameNavigated'],
  ['page/lifecycle',      m => m === 'Page.lifecycleEvent'],
  ['page/dialogs',        m => m.startsWith('Page.javascriptDialog')],
  ['page/frames',         m => m.startsWith('Page.frame')],
  ['page/all',            m => m.startsWith('Page.')],
  ['dom/all',             m => m.startsWith('DOM.')],
];

function isTopNav(ev) {
  return ev?.method === 'Page.frameNavigated' && 
    (ev?.params?.frame?.parentId ?? null) === null;
}

// ── Commands ─────────────────────────────────────────────────────────────────

async function cmdStart(target, runIdArg) {
  const runId = runIdArg || isoStamp();
  const RD = runDir(runId);
  
  ensureDir(path.join(RD, 'cdp'));
  ensureDir(path.join(RD, 'screenshots'));
  ensureDir(path.join(RD, 'dom'));

  // Resolve ws URL
  let wsUrl = target;
  if (/^\d+$/.test(target)) {
    // It's a port number, fetch ws URL from /json/version
    const resp = await fetch(`http://127.0.0.1:${target}/json/version`);
    const info = await resp.json();
    wsUrl = info.webSocketDebuggerUrl;
  }

  writeJson(path.join(RD, 'manifest.json'), {
    run_id: runId,
    target: wsUrl,
    started_at: isoUtc(),
    domains: 'Network Console Runtime Log Page',
  });

  // Connect via raw WebSocket and capture
  const ws = new (await import('ws')).default(wsUrl);
  let msgId = 1;
  const rawStream = fs.createWriteStream(path.join(RD, 'cdp', 'raw.ndjson'));

  ws.on('open', () => {
    // Enable domains
    for (const domain of ['Network', 'Console', 'Runtime', 'Log', 'Page']) {
      ws.send(JSON.stringify({ id: msgId++, method: `${domain}.enable` }));
    }
    console.log(`Capturing on ${wsUrl} → ${RD}`);
  });

  ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    // Only record events (messages with .method, not id responses)
    if (msg.method) {
      rawStream.write(JSON.stringify(msg) + '\n');
    }
  });

  ws.on('error', (err) => {
    console.error('CDP WebSocket error:', err.message);
  });

  // Write PID for cleanup
  fs.writeFileSync(path.join(RD, '.ws.pid'), String(process.pid));
  
  // Keep alive
  process.on('SIGTERM', () => { ws.close(); process.exit(0); });
  process.on('SIGINT', () => { ws.close(); process.exit(0); });
}

async function cmdBisect(runId) {
  const RD = runDir(runId);
  const rawPath = path.join(RD, 'cdp', 'raw.ndjson');
  
  if (!fs.existsSync(rawPath)) {
    console.error(`No raw.ndjson at ${rawPath}`);
    process.exit(1);
  }

  const events = readJsonl(rawPath);
  const manifest = readJson(path.join(RD, 'manifest.json'), {});
  const startedMs = manifest.started_at ? new Date(manifest.started_at).getTime() : null;

  // Assign page IDs
  let pid = -1;
  for (const ev of events) {
    if (isTopNav(ev)) pid++;
    ev._pid = pid < 0 ? 0 : pid;
  }

  // Session-wide buckets
  for (const [bucket, predicate] of BUCKETS) {
    const matched = events.filter(e => predicate(e.method ?? '')).map(({_pid, ...r}) => r);
    writeJsonl(path.join(RD, 'cdp', `${bucket}.jsonl`), matched, { skipEmpty: true });
  }

  // Per-page slices
  const pagesRoot = path.join(RD, 'cdp', 'pages');
  if (fs.existsSync(pagesRoot)) fs.rmSync(pagesRoot, { recursive: true, force: true });
  ensureDir(pagesRoot);

  const pageMap = new Map();
  for (const ev of events) {
    if (!pageMap.has(ev._pid)) pageMap.set(ev._pid, []);
    pageMap.get(ev._pid).push(ev);
  }
  if (pageMap.size === 0) pageMap.set(0, []);

  const pageSummaries = [];
  for (const [thisPid, pageEvents] of [...pageMap.entries()].sort((a, b) => a[0] - b[0])) {
    const pdir = path.join(pagesRoot, String(thisPid).padStart(3, '0'));
    ensureDir(pdir);

    const navEv = pageEvents.find(isTopNav);
    const url = navEv?.params?.frame?.url ?? '(initial)';
    fs.writeFileSync(path.join(pdir, 'url.txt'), url + '\n');
    writeJsonl(path.join(pdir, 'raw.jsonl'), pageEvents.map(({_pid, ...r}) => r));

    for (const [bucket, predicate] of BUCKETS) {
      const matched = pageEvents.filter(e => predicate(e.method ?? '')).map(({_pid, ...r}) => r);
      writeJsonl(path.join(pdir, `${bucket}.jsonl`), matched, { skipEmpty: true });
    }

    const counts = {};
    for (const ev of pageEvents) {
      const domain = ev.method?.split('.')[0] || 'Other';
      counts[domain] = (counts[domain] || 0) + 1;
    }
    pageSummaries.push({ pageId: thisPid, url, eventCount: pageEvents.length, domains: counts });
  }

  const summary = {
    sessionId: manifest.run_id || runId,
    totalEvents: events.length,
    pages: pageSummaries,
  };
  writeJson(path.join(RD, 'cdp', 'summary.json'), summary);
  console.log(JSON.stringify(summary, null, 2));
}

async function cmdStatus(runId) {
  const RD = runDir(runId);
  if (!fs.existsSync(path.join(RD, 'manifest.json'))) {
    console.error(`Run ${runId} not found`);
    process.exit(1);
  }
  const manifest = readJson(path.join(RD, 'manifest.json'));
  const rawPath = path.join(RD, 'cdp', 'raw.ndjson');
  const eventCount = fs.existsSync(rawPath) ? 
    fs.readFileSync(rawPath, 'utf8').split('\n').filter(Boolean).length : 0;
  
  console.log(JSON.stringify({
    runId,
    started: manifest.started_at,
    target: manifest.target,
    eventCount,
  }, null, 2));
}

// ── Main ─────────────────────────────────────────────────────────────────────

const [cmd, ...args] = process.argv.slice(2);

switch (cmd) {
  case 'start':
    await cmdStart(args[0], args[1]);
    break;
  case 'bisect':
    await cmdBisect(args[0]);
    break;
  case 'status':
    await cmdStatus(args[0]);
    break;
  default:
    console.log(`Usage: cdp-trace.mjs <start|bisect|status> [args]

Commands:
  start <ws-url|port> [run-id]   Begin capturing CDP events
  bisect <run-id>                 Split raw.ndjson into per-page buckets
  status <run-id>                 Show capture status`);
}
