# HEARTBEAT.md

## Status
- Last check: 2026-07-13 06:00 GMT-3
- Cron jobs: 9 active (down from 11), all enabled, no current delivery errors
- check-free-models-weekly: config FIXED (delivery.to=telegram:908406251); cached lastRunStatus still "error" but that is the pre-fix run. Next run Sat 2026-07-18 03:00 will deliver correctly.
- Wiki: graphify-out minimal (no wiki/index.md)
- Memory: 139 files across 17 directories
- New raw sources in memory/raw/: 2 files (2026-07-12) — see report below
- Backup: completed 20260711-060116 (next run pending)
- Return `HEARTBEAT_OK` when no action is needed

## Purpose
Heartbeat exists to check continuity, detect drift, and report status with minimal cost.

## Checklist

### 1. Status check
- Count wiki pages by area
- Confirm `index.md` is current
- Check agentmemory status
- Check whether `raw/` has new files

### 2. New sources
- If new raw files exist, report them
- Do not ingest automatically

**New raw sources (memory/raw/, captured 2026-07-12):**
- `eclipse-dom-engine-analysis.md` — open-source Perplexity Comet alternative; multi-agent loop (Planner/Executor/Validator) + `@agentic-intelligence/dom-engine` npm lib (agenticPurposeId pattern, human-like clicks, smart scroll)
- `perplexity-comet-analysis.md` — leaked Comet system prompt; tool architecture, hidden vs visible tabs, parallel execution, ID system, browser isolation, security guidelines
- Both already in digested/analysis form with "lessons for our setup" sections. NOT ingested (per heartbeat economy rule). Candidate move to `memory/segments/` or `memory/research/` on next dedicated pass.

### 3. Lightweight lint
- Report orphan pages
- Run contradiction check: `node scripts/contradiction-check.js --dry-run`
- Report flagged contradictions
- Do not run heavy LLM-based lint during heartbeat

### 4. Memory sync
- If the wiki materially changed, sync the relevant memory layer
- Otherwise skip

### 5. Checkpoint
- Every 7 days, write a checkpoint with counts and notable status changes

## Economy rule
Heartbeat should be cheap.
Do not ingest sources, rewrite pages, or run expensive transformations unless explicitly requested.

## Escalation
Escalate only when you find:
- new raw sources
- broken index state
- repeated false positives
- stale or inconsistent workspace state
