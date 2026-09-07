// Probe ALL antigravity-proxy models with the correct auth (no x-api-key header)
// to classify real blocks vs transient. Reads provider list from openclaw.json.
const fs = require('fs');
const cfg = JSON.parse(fs.readFileSync('C:/Users/ClawLabs/.openclaw/openclaw.json', 'utf8'));
const models = cfg.models.providers['antigravity-proxy'].models.map(m => m.id);
const PROXY = 'http://127.0.0.1:8080/v1/messages';

async function probe(id) {
  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(), 20000);
  try {
    const res = await fetch(PROXY, {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'anthropic-version': '2023-06-01' },
      body: JSON.stringify({
        model: id,
        max_tokens: 8,
        messages: [{ role: 'user', content: 'Reply with the single word: pong' }]
      }),
      signal: controller.signal
    });
    if (res.ok) return { ok: true, status: res.status };
    let body = {};
    try { body = await res.json(); } catch {}
    const err = body.error || {};
    return { ok: false, status: res.status, type: err.type, message: String(err.message || '').slice(0, 120) };
  } catch (e) {
    return { ok: false, error: e.message };
  } finally { clearTimeout(t); }
}

(async () => {
  const results = [];
  for (const id of models) {
    const r = await probe(id);
    results.push({ id, ...r });
    console.log((r.ok ? 'OK  ' : 'FAIL') + ' ' + id + (r.status ? ' [' + r.status + ']' : '') + (r.type || '') + ' ' + (r.message || r.error || '').slice(0, 100));
  }
  const blocked = results.filter(r => !r.ok && (r.status === 401 || r.status === 403 || (r.status === 400 && /invalid model|not found/i.test(r.message || ''))));
  console.log('\n=== REAL BLOCKED (' + blocked.length + ') ===');
  blocked.forEach(b => console.log(b.id + ' [' + b.status + '] ' + (b.type || '') + ' ' + (b.message || '').slice(0, 90)));
})().catch(e => { console.error('FATAL', e); process.exit(1); });