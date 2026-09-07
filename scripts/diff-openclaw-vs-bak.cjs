// Compare openclaw.json current vs .bak as text (bak may not be pure JSON)
const fs = require('fs');

const cur = JSON.parse(fs.readFileSync('C:/Users/ClawLabs/.openclaw/openclaw.json', 'utf8'));
const bakRaw = fs.readFileSync('C:/Users/ClawLabs/.openclaw/openclaw.json.2026-09-06T20-51-19-580Z.bak', 'utf8');

// Try to extract JSON from bak (may have comment lines or prefixed text)
function tryParse(raw) {
  // strip // and /* */ comments carefully (naive: line-based)
  const lines = raw.split('\n').filter(l => {
    const t = l.trim();
    return !t.startsWith('//') && !t.startsWith('/*') && !t.startsWith('*') && t !== '';
  });
  const stripped = lines.join('\n');
  try { return JSON.parse(stripped); } catch (e) { return null; }
}
const bak = tryParse(bakRaw);

console.log('=== bak parse ===');
if (!bak) {
  console.log('could not parse bak as JSON; first 300 chars:');
  console.log(bakRaw.slice(0, 300));
} else {
  console.log('bak parsed OK. top keys:', Object.keys(bak).join(', '));
  const bp = bak?.models?.providers?.['antigravity-proxy']?.models?.map(m => m.id) || [];
  const cp = cur.models.providers['antigravity-proxy'].models.map(m => m.id);
  console.log('\nbak antigravity models (' + bp.length + '):');
  console.log(bp.join('\n'));
  console.log('\ncur antigravity models (' + cp.length + '):');
  console.log(cp.join('\n'));

  console.log('\n=== removed by autofix (in bak but missing now) ===');
  console.log(bp.filter(x => !cp.includes(x)).join('\n') || 'none');

  console.log('\n=== added since bak (present now, not in bak) ===');
  console.log(cp.filter(x => !bp.includes(x)).join('\n') || 'none');

  // allow list diff
  const ba = bak?.agents?.defaults?.modelPolicy?.allow || [];
  const ca = cur.agents.defaults.modelPolicy.allow || [];
  console.log('\n=== allow missing now (in bak, not cur) ===');
  console.log(ba.filter(x => !ca.includes(x)).join('\n') || 'none');
  console.log('\n=== allow added since bak (in cur, not bak) ===');
  console.log(ca.filter(x => !ba.includes(x)).join('\n') || 'none');

  // aliases diff
  const bAl = bak?.models?.aliases || {};
  const cAl = cur.models?.aliases || {};
  const allKeys = new Set([...Object.keys(bAl), ...Object.keys(cAl)]);
  console.log('\n=== aliases diff ===');
  for (const k of allKeys) {
    if (JSON.stringify(bAl[k]) !== JSON.stringify(cAl[k])) {
      console.log(k + ': bak=' + JSON.stringify(bAl[k]) + ' cur=' + JSON.stringify(cAl[k]));
    }
  }
}