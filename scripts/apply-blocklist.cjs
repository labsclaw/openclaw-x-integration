// Apply definitive block list to openclaw.json based on live probe results.
// Removes ONLY models proven blocked (403 permission / 400 invalid model).
// Keeps transient (5xx/abort) and OK models.
const fs = require('fs');
const OPENCLAW_JSON = 'C:/Users/ClawLabs/.openclaw/openclaw.json';

// From probe-all-antigravity.cjs run at 2026-09-07T17:51Z
const BLOCKED_IDS = [
  'claude-sonnet-4-6-thinking', // 400 invalid model (not in catalog)
  'gemini-3.1-pro-high',        // 403
  'gemini-3.5-flash',           // 400 invalid model
  'gemini-3.6-flash-high',      // 403
  'gemini-3.6-flash-medium',    // 403
  'gemini-3.6-flash-low',       // 403
  'gemini-3.6-flash-tiered',    // 403
  'gemini-3.8-flash-tiered',    // 403
  'gemini-3.1-pro-low',         // 403
  'gemini-pro-agent',           // 403
  'gemini-3-flash',             // 403
  'gemini-2.5-pro',             // 403
  'gemini-2.5-flash-thinking',  // 403
  'gemini-3.7-flash-tiered'     // 403 (was already removed; keep out)
];
const BLOCKED_PREFIXED = BLOCKED_IDS.map(id => 'antigravity-proxy/' + id);

const cfg = JSON.parse(fs.readFileSync(OPENCLAW_JSON, 'utf8'));
const prov = cfg.models.providers['antigravity-proxy'];

// 1. Provider models
const before = prov.models.length;
prov.models = prov.models.filter(m => !BLOCKED_PREFIXED.includes('antigravity-proxy/' + (m.id || m)));
console.log('provider models:', before, '->', prov.models.length);

// 2. modelPolicy.allow
const pol = cfg.agents.defaults.modelPolicy;
if (pol && Array.isArray(pol.allow)) {
  const n = pol.allow.length;
  pol.allow = pol.allow.filter(m => !BLOCKED_PREFIXED.includes(m));
  console.log('allow:', n, '->', pol.allow.length);
}

// 3. aliases referencing blocked
if (cfg.models && cfg.models.aliases) {
  for (const [k, v] of Object.entries(cfg.models.aliases)) {
    if (typeof v === 'string' && BLOCKED_PREFIXED.includes(v)) {
      delete cfg.models.aliases[k];
      console.log('alias removed:', k);
    }
  }
}

// 4. entries model primary/fallbacks
if (cfg.agents && cfg.agents.entries) {
  for (const [name, entry] of Object.entries(cfg.agents.entries)) {
    const m = entry && entry.model;
    if (!m) continue;
    if (typeof m === 'string' && BLOCKED_PREFIXED.includes(m)) { entry.model = null; console.log('entry', name, 'model cleared'); }
    else if (typeof m === 'object' && m) {
      if (m.primary && BLOCKED_PREFIXED.includes(m.primary)) { console.log('entry', name, 'primary was', m.primary); m.primary = null; }
      if (Array.isArray(m.fallbacks)) {
        const f0 = m.fallbacks.length;
        m.fallbacks = m.fallbacks.filter(f => !BLOCKED_PREFIXED.includes(f));
        if (m.fallbacks.length !== f0) console.log('entry', name, 'fallbacks:', f0, '->', m.fallbacks.length);
      }
    }
  }
}

// Save
const tmp = OPENCLAW_JSON + '.tmp';
fs.writeFileSync(tmp, JSON.stringify(cfg, null, 2), 'utf8');
fs.renameSync(tmp, OPENCLAW_JSON);
console.log('DONE. Remaining antigravity models:', prov.models.map(m => m.id).join(', '));