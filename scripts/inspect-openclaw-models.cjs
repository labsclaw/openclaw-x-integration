// Inspect openclaw.json for blocked model references + userAgent (redacted)
const fs = require('fs');
const p = 'C:/Users/ClawLabs/.openclaw/openclaw.json';
const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));

const blocked = ['antigravity-proxy/gemini-3.7-flash-tiered', 'antigravity-proxy/gemini-3.6-flash-tiered', 'antigravity-proxy/gemini-3.1-pro-high'];

function scan(obj, path, hits) {
  if (!obj || typeof obj !== 'object') return;
  if (Array.isArray(obj)) {
    for (const v of obj) scan(v, path, hits);
    return;
  }
  for (const [k, v] of Object.entries(obj)) {
    const p2 = path + '.' + k;
    if (typeof v === 'string' && blocked.includes(v)) hits.push(p2 + ' = ' + v);
    else scan(v, p2, hits);
  }
}
const hits = [];
scan(cfg, 'cfg', hits);
console.log('=== BLOCKED MODEL REFERENCES ===');
console.log(hits.length ? hits.join('\n') : 'none');

// modelPolicy allow list (defaults)
console.log('\n=== agents.defaults.modelPolicy.allow ===');
try {
  const allow = cfg.agents?.defaults?.modelPolicy?.allow || [];
  console.log(allow.length + ' entries');
  console.log(allow.join('\n'));
} catch (e) { console.log('ERR', e.message); }

// provider antigravity-proxy models (ids only)
console.log('\n=== models.providers.antigravity-proxy ===');
try {
  const prov = cfg.models?.providers?.['antigravity-proxy'];
  if (!prov) { console.log('provider not found'); }
  else {
    console.log('baseUrl:', prov.baseUrl);
    console.log('apiKey:', prov.apiKey && typeof prov.apiKey === 'object' ? JSON.stringify({...prov.apiKey, value: '***'}) : (prov.apiKey ? '***' : '(none)'));
    console.log('models:', (prov.models || []).map(m => m.id).join(', '));
  }
} catch (e) { console.log('ERR', e.message); }

// userAgent mentions
console.log('\n=== userAgent mentions ===');
const raw = fs.readFileSync(p, 'utf8');
const uaMatches = raw.match(/userAgent[^\n]{0,120}/gi) || [];
console.log(uaMatches.length ? uaMatches.join('\n') : 'none');

// entries model config (main)
console.log('\n=== agents.entries.main.model ===');
try {
  const m = cfg.agents?.entries?.main?.model;
  if (m && typeof m === 'object') {
    console.log('primary:', m.primary);
    console.log('fallbacks:', (m.fallbacks || []).join('\n'));
  } else {
    console.log(JSON.stringify(m));
  }
} catch (e) { console.log('ERR', e.message); }