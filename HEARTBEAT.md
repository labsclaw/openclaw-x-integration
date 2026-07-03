# HEARTBEAT.md

## Status
- Last check: 2026-07-01 06:00 GMT-3
- Cron jobs healthy
- Wiki index current
- No active alerts
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

### 3. Lightweight lint
- Report orphan pages
- Report obvious contradictions
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
