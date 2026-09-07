// model-health-autofix.cjs
// Self-healing monitor for antigravity-proxy models in openclaw.json.
//
// How it works:
//   1. Reads the live model list under models.providers['antigravity-proxy'].
//   2. Probes each model via POST /v1/messages WITHOUT an x-api-key header
//      (the proxy config has an empty apiKey; sending a bogus key caused a
//      mass false-positive 403 on 2026-09-07 that wiped good models).
//   3. Classifies results:
//        BLOCKED   -> 403/401 with permission/age/eligibility message, or
//                     400 invalid model / not found / unknown model.
//        TRANSIENT -> 5xx, network error, timeout, 429 (never auto-remove).
//   4. SAFEGUARD: if more than 50% of the probed models classify as BLOCKED,
//      abort without touching the config (likely bad auth / proxy down, not
//      real blocks). Logs and exits 1.
//   5. On confirmed blocks (<=50%), atomically rewrites openclaw.json:
//      - removes blocked ids from provider models
//      - removes them from agents.defaults.modelPolicy.allow
//      - purges aliases that point to removed models
//      - strips blocked ids from entry model.primary/fallbacks
//      A timestamped backup is written first.
//
// Safe to run on a schedule. Requires Node 18+ (global fetch).
const fs = require('fs');
const path = require('path');

const OPENCLAW_JSON = process.env.OPENCLAW_JSON || 'C:/Users/ClawLabs/.openclaw/openclaw.json';
const PROXY_CHAT_URL = process.env.PROXY_CHAT_URL || 'http://127.0.0.1:8080/v1/messages';
const LOG_FILE = process.env.MODEL_HEALTH_LOG || 'C:/Users/ClawLabs/.openclaw/workspace/memory/logs/model-health-autofix.log';
const QUIET = process.env.QUIET === '1';
const MAX_BLOCK_RATIO = parseFloat(process.env.MAX_BLOCK_RATIO || '0.5');

const TEST_PROMPT = 'Reply with the single word: pong';
const MAX_PROMPT_TOKENS = 8;
const REQUEST_TIMEOUT_MS = 20000;

function log(...args) {
  if (QUIET) return;
  const ts = new Date().toISOString();
  console.log(`[model-health-autofix ${ts}]`, ...args);
}

function fileLog(line) {
  try {
    fs.mkdirSync(path.dirname(LOG_FILE), { recursive: true });
    fs.appendFileSync(LOG_FILE, line + '\n', 'utf8');
  } catch (e) { /* ignore */ }
}

async function probeModel(modelId) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    // NOTE: no x-api-key header on purpose. The proxy config has apiKey: "".
    // Sending a bogus key made the proxy 403 every model (mass false positive).
    const res = await fetch(PROXY_CHAT_URL, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: modelId,
        max_tokens: MAX_PROMPT_TOKENS,
        messages: [{ role: 'user', content: TEST_PROMPT }]
      }),
      signal: controller.signal
    });
    if (res.ok) return { ok: true, status: res.status };
    let body = {};
    try { body = await res.json(); } catch {}
    const err = body?.error || {};
    return {
      ok: false,
      status: res.status,
      type: String(err?.type || ''),
      message: String(err?.message || '').slice(0, 200)
    };
  } catch (e) {
    return { ok: false, error: e.message };
  } finally {
    clearTimeout(timer);
  }
}

// A blocking failure is a definitive upstream rejection for THIS account/config:
// permission denied (403), auth (401) with eligibility/permission language,
// or "invalid model" (400). Timeouts, 5xx, 429, aborts are transient.
function isBlocking(result) {
  if (result.ok) return false;
  if (result.error) return false; // network/timeout -> transient
  const m = (result.message || '').toLowerCase();
  const type = (result.type || '').toLowerCase();
  if (result.status === 400 && /invalid model|not found|unknown model/i.test(m)) return true;
  if (result.status === 401 || result.status === 403) {
    if (/not eligible|not allowed|restricted_age|forbidden|permission|age|eligible/i.test(m + ' ' + type)) return true;
  }
  return false;
}

function main() {
  const raw = fs.readFileSync(OPENCLAW_JSON, 'utf8');
  let cfg;
  try { cfg = JSON.parse(raw); } catch (e) { log('FATAL: openclaw.json is not valid JSON:', e.message); process.exit(1); }

  const prov = cfg.models?.providers?.['antigravity-proxy'];
  if (!prov || !Array.isArray(prov.models) || prov.models.length === 0) {
    log('no antigravity-proxy models configured; nothing to do');
    return;
  }
  if (!cfg.agents?.defaults?.modelPolicy?.allow) {
    log('FATAL: agents.defaults.modelPolicy.allow missing; aborting (config shape unexpected)');
    process.exit(1);
  }

  const modelIds = prov.models.map(m => m.id || m).filter(Boolean);
  const results = [];

  (async () => {
    for (const id of modelIds) {
      const r = await probeModel(id);
      const verdict = r.ok ? 'OK' : (isBlocking(r) ? 'BLOCKED' : 'TRANSIENT');
      results.push({ id, verdict, ...r });
      if (!QUIET) {
        const tail = (r.message || r.error || '').replace(/\s+/g, ' ').slice(0, 80);
        log(`probe ${id} -> ${verdict} [${r.status || '-'}] ${tail}`);
      }
    }

    const blocked = results.filter(r => r.verdict === 'BLOCKED');
    const ratio = modelIds.length ? blocked.length / modelIds.length : 0;

    if (blocked.length === 0) {
      log('no blocking failures detected');
      return;
    }

    if (ratio > MAX_BLOCK_RATIO) {
      const msg = `ABORT: ${blocked.length}/${modelIds.length} models classified BLOCKED (ratio ${(ratio * 100).toFixed(0)}% > ${(MAX_BLOCK_RATIO * 100).toFixed(0)}%). Likely bad auth/proxy down. Config NOT touched.`;
      log(msg);
      fileLog(`${new Date().toISOString()} ${msg}`);
      console.error(msg);
      process.exit(1);
    }

    // Write a timestamped backup before mutating
    const stamp = new Date().toISOString().replace(/[:.]/g, '-');
    const bakPath = OPENCLAW_JSON + '.autofix-' + stamp + '.bak';
    fs.writeFileSync(bakPath, raw, 'utf8');
    log('backup written:', bakPath);

    const blockedPrefixed = blocked.map(b => 'antigravity-proxy/' + b.id);
    let changed = false;

    const before = prov.models.length;
    prov.models = prov.models.filter(m => !blockedPrefixed.includes('antigravity-proxy/' + (m.id || m)));
    if (prov.models.length !== before) changed = true;

    const pol = cfg.agents.defaults.modelPolicy;
    const n0 = pol.allow.length;
    pol.allow = pol.allow.filter(m => !blockedPrefixed.includes(m));
    if (pol.allow.length !== n0) changed = true;

    if (cfg.models?.aliases) {
      for (const [k, v] of Object.entries(cfg.models.aliases)) {
        if (typeof v === 'string' && blockedPrefixed.includes(v)) {
          delete cfg.models.aliases[k];
          changed = true;
        }
      }
    }

    const entries = cfg.agents?.entries || {};
    for (const [name, entry] of Object.entries(entries)) {
      const m = entry?.model;
      if (!m) continue;
      if (typeof m === 'string' && blockedPrefixed.includes(m)) { entries[name].model = null; changed = true; }
      else if (m && typeof m === 'object') {
        if (blockedPrefixed.includes(m.primary)) { m.primary = null; changed = true; }
        if (Array.isArray(m.fallbacks)) {
          const f0 = m.fallbacks.length;
          m.fallbacks = m.fallbacks.filter(f => !blockedPrefixed.includes(f));
          if (m.fallbacks.length !== f0) changed = true;
        }
      }
    }

    if (!changed) {
      log('blocked models detected but config already clean');
      return;
    }

    const tmp = OPENCLAW_JSON + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(cfg, null, 2), 'utf8');
    fs.renameSync(tmp, OPENCLAW_JSON);
    const removed = blocked.map(b => b.id).join(', ');
    const line = `${new Date().toISOString()} removed: ${removed} (provider now ${prov.models.length} models)`;
    log('config updated: ' + line);
    fileLog(line);
  })().catch(e => {
    log('FATAL', e.message);
    process.exit(1);
  });
}

main();