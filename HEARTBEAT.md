# HEARTBEAT.md

## Status
- Last check: 2026-07-25 06:00 GMT-3
- Cron jobs: not checked this run (manual heartbeat)
- check-free-models-weekly: confirmed fixed, lastRunStatus=ok (fixed 2026-07-18 03:00)
- Raw sources: 2 files from 2026-07-12. No new files.
- Contradiction check: `scripts/contradiction-check.cjs` exists and runs (0 contradictions found)
- Wiki health: 89 files, 25.8% link coverage, 66 orphans, 1 broken link ([[research/artificial-intelligence]])
- Gateway: Running (PID 12408)
- PM2: 3 processes healthy (antigravity-proxy, openclaw-gateway, paperclip)
- SSC v4.0: 33/33 tests passing
- Segments: 14 files (s001-s012 + subagent-evolution + cross-agent-coordination)
- Checkpoints: 6 total (last: ckpt-2026-07-24)

## Purpose
Heartbeat exists to check continuity, detect drift, and report status with minimal cost.

## Checklist

### 1. Status check
- Count wiki pages by area: 89 total (index + concepts + entities + knowledge-abstracts + projects + raw + synthesis + checkpoints + scripts)
- Confirm `index.md` is current (last updated 2026-07-04)
- Check agentmemory status: SSC v4.0 deployed, stable
- Check whether `raw/` has new files: No new files since 2026-07-12

### 2. New sources
- If new raw files exist, report them
- Do not ingest automatically

**New raw sources (memory/raw/, captured 2026-07-12):**
- `eclipse-dom-engine-analysis.md` — open-source Perplexity Comet alternative; multi-agent loop (Planner/Executor/Validator) + `@agentic-intelligence/dom-engine` npm lib (agenticPurposeId pattern, human-like clicks, smart scroll)
- `perplexity-comet-analysis.md` — leaked Comet system prompt; tool architecture, hidden vs visible tabs, parallel execution, ID system, browser isolation, security guidelines
- Both already in digested/analysis form with "lessons for our setup" sections. NOT ingested (per heartbeat economy rule). Candidate move to `memory/segments/` or `memory/research/` on next dedicated pass.

### 3. Lightweight lint
- Report orphan pages: 66 orphan files (mostly knowledge-abstracts Obsidian export fragments)
- Run contradiction check: `node scripts/contradiction-check.cjs --dry-run` → 0 contradictions found
- Report flagged contradictions: None
- Do not run heavy LLM-based lint during heartbeat
- Wiki index has 1 broken link: [[research/artificial-intelligence]]

### 4. Memory sync
- If the wiki materially changed, sync the relevant memory layer
- Otherwise skip
- Wiki has not materially changed since last checkpoint (2026-07-24)

### 5. Checkpoint
- Every 7 days, write a checkpoint with counts and notable status changes
- Last checkpoint: 2026-07-24 (1 day ago) — not due yet

## Economy rule
Heartbeat should be cheap.
Do not ingest sources, rewrite pages, or run expensive transformations unless explicitly requested.

## Escalation
Escalate only when you find:
- new raw sources
- broken index state
- repeated false positives
- stale or inconsistent workspace state