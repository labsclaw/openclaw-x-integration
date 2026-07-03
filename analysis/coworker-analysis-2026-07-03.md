# Coworker Analysis — Technical Report

**Date:** 2026-07-03
**Source:** https://github.com/accomplish-ai/coworker (1280 files, MIT licensed)
**Author:** Justus (CEO Agent)
**Request:** Dr. Roger Oliveira

---

## Executive Summary

Coworker is an open-source desktop AI agent (Electron + React + daemon) that uses OpenCode as its LLM backend. Their architecture is desktop-first with a split design: `apps/web` (React UI), `apps/desktop` (Electron shell), `apps/daemon` (background task execution), and `packages/agent-core` (core business logic).

**Our stack is more robust in:** memory, scheduling, multi-agent orchestration, and channel integration.
**They are stronger in:** task completion enforcement, browser automation batching, permission gating, and skill structure.

This report identifies 7 actionable patterns to adopt, ranked by impact.

---

## 1. Conversational Bypass

**File:** `packages/agent-core/src/opencode/system-prompt-behaviors.ts`

### What they do
They detect when a message is "just chat" (greetings, thanks, simple questions) and skip the entire task workflow. No `start_task`, no `todowrite`, no `complete_task`. Direct response, done.

### Their implementation
```typescript
export const CONVERSATIONAL_BYPASS_BEHAVIOR = `<behavior name="conversational-bypass">
If a request can be completed without tools or multi-step execution (for example: greetings,
thanks, short acknowledgements, small talk, or simple direct questions), respond directly.

In conversational mode:
- Do NOT call start_task
- Do NOT call todowrite
- Do NOT call complete_task
- Keep responses concise by default (1-3 sentences)
- Do NOT proactively list capabilities

Conversational-bypass interactions are not task workflows. The global complete_task
requirement in TASK COMPLETION applies only to non-conversational task workflows.

Only enter task workflow when the request needs tools, file operations, browsing, or clear
multi-step execution.
</behavior>`;
```

### What we should do
Add a similar gate in our system prompt. When the user sends a trivial message (greeting, thanks, simple question), respond directly without engaging `update_plan` or `update_goal`. This saves context window and reduces latency.

### Implementation sketch
Add to SOUL.md or a new behavioral section:
```
## Conversational Bypass
If the request is a greeting, acknowledgment, simple question, or casual chat:
- Respond directly in 1-3 sentences
- Do NOT engage task workflow (update_plan, update_goal)
- Do NOT call tools unless explicitly needed
Only enter execution mode when the request requires multi-step work, tool usage, or delegation.
```

### Impact: HIGH
Every trivial interaction currently passes through the full pipeline. This wastes context and adds latency.

---

## 2. Completion Enforcement

**Files:**
- `packages/agent-core/src/opencode/completion/completion-enforcer.ts`
- `packages/agent-core/src/opencode/completion/completion-enforcer-rules.ts`
- `packages/agent-core/src/opencode/completion/completion-state.ts`

### What they do
A stateful enforcer that tracks task progress and prevents premature "done" claims:

1. **start_task** → records planned steps and verification criteria
2. **todowrite** → updates progress on each step (pending → in_progress → completed)
3. **complete_task** → enforcer checks:
   - Are ALL todos marked "completed" or "cancelled"?
   - If agent claims "success" but has incomplete todos → **auto-downgrades to "partial"**
   - Forces continuation until everything is actually done

### Key code
```typescript
// From completion-enforcer.ts
if (completeTaskArgs.status === 'success' && hasIncompleteTodos(this.currentTodos)) {
  const incompleteSummary = getIncompleteTodosSummary(this.currentTodos);
  this.callbacks.onDebug(
    'incomplete_todos',
    'Agent claimed success but has incomplete todos - downgrading to partial',
    { incompleteTodos: incompleteSummary },
  );
  // Auto-downgrade to partial, force continuation
}
```

### What we should do
We have `update_plan` and `update_goal`, but no enforcement. Add a pre-flight check before `update_goal(status="complete")`:
- Verify all plan steps are "completed"
- If any are still "pending" or "in_progress", block the completion and force continuation
- Log when this happens for visibility

### Implementation sketch
Add to AGENTS.md under "Task Execution Discipline":
```
### Completion Gate
Before calling update_goal(status="complete"), verify:
1. All plan steps are "completed" (no "pending" or "in_progress")
2. The original request has been fully addressed
3. If verification is impossible, report what couldn't be verified

If any step is incomplete, DO NOT call update_goal. Continue working or report the blocker.
```

### Impact: HIGH
Prevents the "I'm done" + "wait, you didn't do X" pattern. Forces thorough execution.

---

## 3. Safe File Deletion Gate

**File:** `packages/agent-core/mcp-tools/safe-file-deletion/SKILL.md`

### What they do
Before deleting ANY file, the system forces an explicit permission request:

```typescript
// Mandatory for ALL delete operations
request_file_permission({
  operation: "delete",
  filePath: "/path/to/file.txt"  // or filePaths: [...] for batch
})
// Wait for response
// Only proceed if "allowed"
// If "denied", acknowledge and do NOT delete
```

### Rules
- Applies to: `rm`, `unlink`, `fs.rm`, `fs.rmdir`, any script that removes files
- No workarounds: cannot bypass by emptying files, moving to temp, or using obscure commands
- Batch support: multiple files in one request via `filePaths` array

### What we should do
We have "never delete" in AGENTS.md, but it's a soft rule. Add a behavioral gate:
- Before any destructive file operation, confirm with Dr. Roger
- Log the intent (what, where, why)
- Never silently delete

### Implementation sketch
Add to AGENTS.md under "Security":
```
### Destructive Operations Gate
Before ANY destructive operation (delete, overwrite, drop, prune):
1. State what will be affected
2. Confirm with Dr. Roger (unless he explicitly pre-approved)
3. Log the operation intent
4. Only proceed after explicit confirmation

This applies to: file deletion, database drops, config overwrites, cache clears, log rotation.
```

### Impact: MEDIUM
We already follow this loosely, but formalizing it prevents edge cases.

---

## 4. Browser Batch Extraction

**File:** `packages/agent-core/mcp-tools/dev-browser/SKILL.md`

### What they do
`browser_batch_actions` visits N URLs, runs a JS extraction script on each, and returns compact JSON. One call, N pages.

```typescript
browser_batch_actions({
  urls: ["https://example.com/1", "https://example.com/2", "..."],
  extractScript: "return { title: document.querySelector('h1')?.textContent, price: document.querySelector('.price')?.textContent }",
  waitForSelector: "h1"
})
// Returns: compact JSON with results for each URL
// 30-second timeout per page, errors skipped per-URL
```

### When to use
- Price monitoring across multiple sources
- Competitor analysis
- Research that requires visiting multiple pages
- Any "collect data from N places" task

### What we should do
We currently do one URL at a time with `web_fetch` or `playwright`. Create a skill or pattern for batch extraction. Could be:
- A shell script that curls multiple URLs in parallel
- A playwright script that visits N pages and extracts data
- A sub-agent task that does the batch work

### Implementation sketch
Create skill: `browser-batch-extraction/SKILL.md`
```
# Browser Batch Extraction

For tasks requiring data from multiple URLs:

1. Collect URLs from search results or known list
2. Define extraction script (what data to pull from each page)
3. Execute in parallel with timeout per page
4. Aggregate results into structured output

Use exec + curl for simple HTML extraction.
Use playwright for JS-rendered pages.
Use sub-agent for >10 URLs or complex extraction.
```

### Impact: HIGH
5-10x faster for multi-page research tasks.

---

## 5. Skill Structure Standardization

**File:** `apps/desktop/bundled-skills/skill-creator/SKILL.md`

### Their standard
```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description, command)
│   └── Markdown instructions
├── scripts/     (optional) — Executable code
├── references/  (optional) — Documentation loaded as needed
└── assets/      (optional) — Files used in output
```

### Key principles
1. **"Context window is a public good"** — Skills share context with everything else. Be concise.
2. **"The AI is already very smart"** — Only add context it doesn't already have.
3. **Degrees of freedom** — Match specificity to task fragility:
   - High freedom (text instructions) for flexible tasks
   - Medium freedom (pseudocode) for preferred patterns
   - Low freedom (specific scripts) for fragile operations
4. **Mandatory verification** — After creating a skill, read it back to confirm it exists and is correct.

### What we should do
Our `skill_workshop` is functional but less structured. Adopt their frontmatter standard and bundled resource pattern.

### Implementation sketch
Update skill-creator or add to SKILL.md standards:
```yaml
---
name: skill-name
description: Clear description of when to use this skill (max 160 bytes)
command: /skill-name  # optional slash command
---
```

And the directory convention:
```
skill-name/
├── SKILL.md
├── scripts/       # Executable helpers
├── references/    # Docs loaded on demand
└── assets/        # Templates, images, etc.
```

### Impact: MEDIUM
Makes skills more discoverable, consistent, and maintainable.

---

## 6. Multi-Account Routing Pattern

**File:** `apps/desktop/bundled-skills/gws-multi-account/SKILL.md`

### Their rule
| Operation type | When `account` omitted | When `account` specified |
|---|---|---|
| **Read** (list, search, get) | Queries **all** accounts | Queries only specified |
| **Write** (send, create, delete) | **Ask the user** which account | Uses specified account |

### Why it's elegant
- Reads are safe — query everything, merge results
- Writes are dangerous — always confirm which account before sending/creating/deleting
- No exceptions, no guessing

### When we need this
If we integrate Gmail, Calendar, or any multi-account service. Currently Telegram-only, so not urgent.

### Impact: LOW (for now)
Store as a pattern for future integrations.

---

## 7. Connector System (OAuth Architecture)

**File:** `packages/agent-core/src/common/types/connector.ts`

### What they have
- 8 built-in OAuth connectors: Slack, Google, Jira, GitHub, monday.com, Notion, Lightdash, Datadog
- Dynamic Client Registration (DCR) support
- Token introspection endpoints
- Desktop-specific OAuth strategies (PKCE, fixed client, custom)
- Per-connector auth state stored securely

### What we should learn
Not the implementation (too complex for our needs), but the **pattern**:
- Each integration is a "connector" with standardized auth flow
- Auth state is centralized and queryable
- Tokens are validated periodically, not just at use time

### When we need this
If we add more integrations beyond Telegram. For now, our Telegram-native approach is simpler and more reliable.

### Impact: LOW (reference only)

---

## Comparative Matrix

| Capability | OpenClaw | Coworker | Gap |
|---|---|---|---|
| Memory system | ✅ Segments, SSC, daily logs | ❌ None | We're ahead |
| Cron/scheduling | ✅ at/every/cron, delivery modes | ⚠️ 60s tick, basic cron | We're ahead |
| Multi-agent | ✅ sessions_spawn, sub-agents | ❌ Single agent | We're ahead |
| Channel integration | ✅ Telegram, Discord, Signal | ⚠️ WhatsApp (limited) | We're ahead |
| Task completion enforcement | ⚠️ Soft (plan/goal) | ✅ Hard (enforcer) | **They're ahead** |
| Conversational bypass | ❌ Everything goes through pipeline | ✅ Auto-detect trivial msgs | **They're ahead** |
| Browser batch extraction | ❌ One URL at a time | ✅ N URLs in one call | **They're ahead** |
| Safe deletion gate | ⚠️ Soft rule | ✅ Technical gate | **They're ahead** |
| Skill structure | ⚠️ Functional | ✅ Standardized | **They're ahead** |
| Pipeline monitoring | ✅ Watchdogs, cron monitors | ❌ None | We're ahead |
| Permission system | ⚠️ AGENTS.md rules | ✅ Granular, per-operation | **They're ahead** |

---

## Implementation Roadmap

### Phase 1: Quick Wins (1-2 hours)
1. **Conversational Bypass** — Add behavioral rule to SOUL.md
2. **Completion Gate** — Add verification rule to AGENTS.md
3. **Safe Delete Gate** — Formalize destructive ops rule

### Phase 2: Skills (2-4 hours)
4. **Browser Batch Extraction** — Create skill with parallel fetch pattern
5. **Skill Structure** — Update skill_workshop to enforce frontmatter + bundled resources

### Phase 3: Architecture (if needed)
6. **Multi-account routing** — When we add Gmail/Calendar integration
7. **Connector system** — When we have >3 external integrations

---

## Source Files (for reference)

All code from `https://github.com/accomplish-ai/coworker` (commit depth=1, cloned 2026-07-03):

- `packages/agent-core/src/opencode/system-prompt-behaviors.ts` — Conversational bypass + task planning
- `packages/agent-core/src/opencode/completion/completion-enforcer.ts` — Task completion enforcement
- `packages/agent-core/src/opencode/completion/completion-enforcer-rules.ts` — Completion rules
- `packages/agent-core/src/opencode/completion/completion-state.ts` — Completion state machine
- `packages/agent-core/mcp-tools/safe-file-deletion/SKILL.md` — Safe deletion pattern
- `packages/agent-core/mcp-tools/dev-browser/SKILL.md` — Browser automation + batch extraction
- `apps/desktop/bundled-skills/skill-creator/SKILL.md` — Skill creation framework
- `apps/desktop/bundled-skills/gws-multi-account/SKILL.md` — Multi-account routing
- `apps/desktop/bundled-skills/gws-shared/SKILL.md` — Google Workspace shared patterns
- `apps/desktop/bundled-skills/google-sheets/SKILL.md` — Google Sheets automation
- `apps/desktop/bundled-skills/download-file/SKILL.md` — File download with popup handling
- `apps/desktop/bundled-skills/code-review/SKILL.md` — Code review checklist
- `apps/desktop/bundled-skills/web-research/SKILL.md` — Web research workflow
- `apps/desktop/bundled-skills/git-commit/SKILL.md` — Git commit conventions
- `packages/agent-core/src/common/types/connector.ts` — OAuth connector types
- `packages/agent-core/src/common/types/permission.ts` — Permission system
- `apps/daemon/src/scheduler-service.ts` — Cron scheduler
- `apps/daemon/src/task-service.ts` — Task service architecture
- `packages/agent-core/src/opencode/system-prompt.ts` — System prompt template
