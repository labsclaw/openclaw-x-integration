// Final reconciliation: provider = source of truth (probe-verified OK + transient), allow aligned.
const fs = require('fs');
const OPENCLAW_JSON = 'C:/Users/ClawLabs/.openclaw/openclaw.json';

// Verified by live probe 2026-09-07T17:51Z
const OK_IDS = [
  'claude-opus-4-6-thinking',   // 200
  'claude-sonnet-4-6',          // 200
  'gemini-3.5-flash-lite',      // 200
  'gemini-3.5-flash-low',       // 200
  'gemini-3.5-flash-extra-low', // 200
  'gemini-3.1-flash-lite',      // 200
  'gemini-3.1-flash-image',     // 200
  'gemini-3-flash-agent',       // 200
  'gemini-2.5-flash',           // 200
  'gemini-2.5-flash-lite'       // 200
];
// Transient (5xx/timeout) - keep in provider, proxy may recover
const TRANSIENT_IDS = ['grok-4.5-build-free', 'grok-4.5'];

const DESIRED = [...OK_IDS, ...TRANSIENT_IDS];

const cfg = JSON.parse(fs.readFileSync(OPENCLAW_JSON, 'utf8'));
const prov = cfg.models.providers['antigravity-proxy'];

// Preserve existing model objects (with any custom fields), add missing as {id}
const byId = new Map();
for (const m of prov.models) byId.set(m.id || m, typeof m === 'object' ? m : { id: m });
prov.models = DESIRED.map(id => byId.get(id) || { id });

// Align allow: every provider model must be allowed
const pol = cfg.agents.defaults.modelPolicy;
const allowed = new Set(pol.allow || []);
for (const id of DESIRED) allowed.add('antigravity-proxy/' + id);
// Keep any antigravity-proxy/* entries that are NOT blocked (defensive)
for (const m of pol.allow || []) {
  if (m.startsWith('antigravity-proxy/')) allowed.add(m);
}
pol.allow = [...allowed];

// Purge aliases pointing at models no longer in provider
if (cfg.models.aliases) {
  for (const [k, v] of Object.entries(cfg.models.aliases)) {
    if (typeof v === 'string' && v.startsWith('antigravity-proxy/')) {
      const short = v.replace('antigravity-proxy/', '');
      if (!DESIRED.includes(short)) { delete cfg.models.aliases[k]; console.log('alias purged:', k, '=>', v); }
    }
  }
}

const tmp = OPENCLAW_JSON + '.tmp';
fs.writeFileSync(tmp, JSON.stringify(cfg, null, 2), 'utf8');
fs.renameSync(tmp, OPENCLAW_JSON);

console.log('FINAL provider (' + prov.models.length + '):', prov.models.map(m => m.id).join(', '));
console.log('FINAL allow antigravity:', pol.allow.filter(m => m.startsWith('antigravity-proxy/')).join(', '));