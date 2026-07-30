# ultra-browser-skill v2.0

Browser automation with CDP trace capture, self-improving loops, cookie sync, and dom-engine injection.

## Capabilities

### 1. CDP Trace Capture (`scripts/cdp-trace.mjs`)

Capture full DevTools protocol firehose from any Chrome instance with remote debugging enabled.

```bash
# Start capturing
node scripts/cdp-trace.mjs start <ws-url|port> [run-id]

# Split raw events into per-page buckets
node scripts/cdp-trace.mjs bisect <run-id>

# Check status
node scripts/cdp-trace.mjs status <run-id>
```

Output: `.o11y/<run-id>/`
- `manifest.json` — run metadata
- `cdp/raw.ndjson` — full CDP firehose (one JSON object per line)
- `cdp/summary.json` — aggregated stats + per-page breakdown
- `cdp/pages/000/` — per-page slices (url.txt, raw.jsonl, network/, console/, page/, runtime/, log/)
- `screenshots/` — periodic PNG captures
- `dom/` — periodic HTML dumps
- `index.jsonl` — screenshot/DOM/URL timeline

### 2. Self-Improving Loop (`scripts/self-improving-loop.mjs`)

Iterative task execution with automatic strategy refinement.

```bash
node scripts/self-improving-loop.mjs --task <name> --url <url> [--max-iterations 5] [--workspace <path>]
```

Workflow:
1. Read `autobrowse/tasks/<task>/task.md` (goal + steps)
2. Read `strategy.md` (current approach)
3. Execute via OpenClaw browser tool
3. Capture trace via `cdp-trace.mjs`
4. Analyze failures
5. Update `strategy.md` with improvements
6. Repeat until pass or max iterations

Artifacts:
- `autobrowse/tasks/<task>/task.md` — goal, URL, steps, expected output
- `autobrowse/tasks/<task>/strategy.md` — living document of approaches + lessons
- `autobrowse/traces/<task>/iter-XXX/` — trace per iteration
- `autobrowse/reports/<task>.json` — final report

### 3. Cookie Sync (`scripts/cookie-sync.mjs`)

Extract cookies from local Chrome profile and inject into browser sessions.

```bash
node scripts/cookie-sync.mjs --domains x.com,github.com --profile "Default" --output cookies.json
```

### 4. Dom-Engine Injection (`scripts/inject-dom-engine.js`)

Semantic element identification via agenticPurposeId. Inject once per page:

```javascript
await browser.act.evaluate({ fn: "injectDomEngine" });
const ctx = await browser.act.evaluate({ fn: "getInteractiveContext" });
await browser.act.evaluate({ fn: "executeActions", args: [{ agenticPurposeId: "tweetButton", actionType: "click" }] });
```

## Tool Fallback Hierarchy

```
1. Built-in browser tool (snapshot/click/navigate)
   → Simple actions, single page checks, ARIA refs

2. Camoufox (anti-detection)
   → Sites with bot detection (Cloudflare, LinkedIn, X.com)
   → Fingerprint spoofing, human-like profiles

3. CDP Real Browser (port 9222)
   → Logged-in sessions needing auth cookies
   → Multi-step flows with existing Chrome profile

4. Dom-Engine Injection (semantic elements)
   → When refs are generic/unreliable (e1, e2, e3...)
   → When you need stable element IDs across DOM changes
   → When Playwright selectors break on SPA re-renders

5. CDP Trace + Self-Improving Loop
   → When debugging silent failures
   → When building reliable skills for specific sites
   → When you need per-page evidence
```

## Quick Reference

```bash
# Start trace on Chrome port 9222
node scripts/cdp-trace.mjs start 9222 grok-mascot

# Run self-improving task
node scripts/self-improving-loop.mjs --task grok-mascot --url https://x.com/i/grok --max-iterations 5

# Bisect trace
node scripts/cdp-trace.mjs bisect grok-mascot

# Sync cookies for x.com
node scripts/cookie-sync.mjs --domains x.com --profile "Default" --output x-cookies.json

# Inject dom-engine
browser.act.evaluate({ fn: "injectDomEngine" })
```

## Integration Notes

- All scripts use Node stdlib only — no npm install needed
- Works with OpenClaw's built-in browser tool via `browser act evaluate`
- Traces stored in `.o11y/` (configurable via `O11Y_ROOT` env)
- Self-improving loop workspace: `autobrowse/` in `OPENCLAW_WORKSPACE` or repo root
- Cookie sync outputs JSON compatible with browser tool import

## Source

Adapted from browserbase/skills (MIT):
- browser-trace → cdp-trace.mjs
- autobrowse → self-improving-loop.mjs
- cookie-sync → cookie-sync.mjs
- dom-engine injection via @agentic-intelligence/dom-engine concepts