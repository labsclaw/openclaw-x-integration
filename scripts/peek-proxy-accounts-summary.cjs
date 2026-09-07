// Inspect proxy accounts: full list, enabled state, subscription, quota models (redacted)
const fs = require('fs');
const p = 'C:/Users/ClawLabs/.config/antigravity-proxy/accounts.json';
const data = JSON.parse(fs.readFileSync(p, 'utf8'));

console.log('total accounts:', data.accounts.length);
for (const a of data.accounts) {
  console.log('\n=== ' + a.email + ' ===');
  console.log('enabled:', a.enabled, '| source:', a.source, '| isInvalid:', a.isInvalid, a.invalidReason || '');
  console.log('subscription:', JSON.stringify(a.subscription));
  const rl = Object.keys(a.modelRateLimits || {}).filter(k => a.modelRateLimits[k].isRateLimited);
  console.log('rateLimited models:', rl.length ? rl.join(', ') : 'none');
  const q = a.quota?.models ? Object.entries(a.quota.models) : [];
  const ok = q.filter(([, v]) => v.remainingFraction > 0).map(([k]) => k);
  const zero = q.filter(([, v]) => v.remainingFraction === 0).map(([k]) => k);
  console.log('quota models with remaining>0 (' + ok.length + '):', ok.join(', '));
  console.log('quota models exhausted (' + zero.length + '):', zero.join(', ') || 'none');
}