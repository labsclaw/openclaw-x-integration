---
name: "ultra-plan-with-diagrams"
description: "Generate structured implementation plans with Mermaid diagrams, task decomposition, and visual brainstorm outputs."
---

# ultra-plan-with-diagrams

> Generate structured plans, brainstorm visualizations, and architecture diagrams â€” all in one skill.

## When to Use

- User wants a plan, roadmap, or implementation strategy
- User wants to brainstorm ideas visually
- User needs architecture or flow diagrams in markdown
- Any multi-step project that benefits from visual structure

## Output Formats

| Format | When | Portable |
|--------|------|----------|
| **ASCII Box** | Primary â€” hierarchies, flows, tables, trees | Any markdown renderer |
| **Mermaid** | Fallback â€” only when ASCII cutoff triggered | GitHub, GitLab, Notion, Obsidian |
| **Structured Plan** | Task decomposition, implementation steps | Any markdown renderer |

Default: **ASCII + Structured Plan**. Mermaid only when ASCII is insufficient.

## ASCII is Primary

ASCII art renders everywhere â€” Telegram, Discord, terminals, any markdown viewer.
Mermaid requires renderer support. Always prefer ASCII unless the diagram triggers a cutoff.

## Skill Modes

### 1. Plan Mode (default)

When user provides: objective, requirements, or spec.

**Output structure:**

```markdown
# [Project Name] Plan

## Overview
[1-2 sentences: what this builds and why]

## Architecture
[ASCII diagram showing system/components/flow]

## Global Constraints
- [Tech stack, version requirements, naming conventions]

---

### Task N: [Component Name]

**Files:**
- Create: `path/to/file`
- Modify: `path/to/existing.py:123-145`
- Test: `tests/path/to/test.py`

**Interfaces:**
- Consumes: [what this uses from earlier tasks]
- Produces: [what later tasks depend on]

- [ ] **Step 1: Description**
  ```
  code or command here
  ```
- [ ] **Step 2: Verify**
  Run: `command`
  Expected: `output`
- [ ] **Step 3: Commit**
  ```bash
  git commit -m "feat: description"
  ```

---

### Task N+1: [Next Component]
...
```

**Rules:**
- Every plan starts with an Architecture diagram (ASCII or Mermaid)
- Each task has exact file paths, code blocks, and verification commands
- No placeholders: "TBD", "TODO", "implement later" are forbidden
- Tasks are independently testable and committable
- TDD when applicable: failing test â†’ implement â†’ verify â†’ commit
- Tasks ordered by dependency (Task N+1 can reference Task N's outputs)

### 2. Brainstorm Mode

When user says: "brainstorm", "ideias", "explore options", "think through".

**Output structure:**

```markdown
# Brainstorm: [Topic]

## Context
[What we're exploring and why]

## Visual Map
[ASCII mindmap or decision tree]

## Options Analysis

### Option 1: [Name]
- **What:** [description]
- **Pros:** [list]
- **Cons:** [list]
- **Effort:** [S/M/L]
- **Risk:** [low/medium/high]

### Option 2: [Name]
...

## Recommendation
[Which option and why â€” 2-3 sentences]

## Next Steps
- [ ] [Actionable item 1]
- [ ] [Actionable item 2]
```

### 3. Architecture Mode

When user says: "architecture", "design", "how should X connect", "system design".

**Output structure:**

```markdown
# Architecture: [System Name]

## Overview
[1 paragraph: what this system does]

## High-Level
[ASCII component diagram]

## Component Details

### [Component Name]
- **Responsibility:** [single sentence]
- **Interfaces:** [inputs/outputs]
- **Dependencies:** [what it needs]

## Data Flow
[ASCII sequence diagram]

## Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Q] | [A] | [why] |
```

## ASCII Box Diagram Rules

### Box Construction

Every box uses this template (width = content length + 4 padding):

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚    Box Content Here  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Rules:**
1. **Fixed width per row.** All boxes in the same row MUST have identical width.
2. **Count characters precisely.** Top border `â”Œ` + NÃ—`â”€` + `â”`. Bottom: `â””` + NÃ—`â”€` + `â”˜`.
3. **Side borders align.** Left `â”‚` at column 0, right `â”‚` at column N+1.
4. **Text centering.** Pad text with spaces: `â”‚  Content  â”‚`. Uneven splits go left (more space left).
5. **No trailing spaces inside boxes.** They break alignment in some renderers.
6. **All boxes in code block** (``` fenced). Monospace rendering is mandatory.

### Connecting Lines

**Rules:**
1. **Arrows point DOWN from center of box above.** Center = (width / 2) from left border.
2. **Vertical lines `â”‚` align with arrow `â–¼` directly below.**
3. **Horizontal connectors use `â”œâ”€â”€â”€â”€â”€â”€â”€â”¤` or `â””â”€â”€â”€â”€â”€â”€â”€â”˜`** at the same column positions as the boxes they connect.
4. **Spacing between rows:** exactly 1 blank line between bottom border and arrow/connector.

### Layout Templates

#### Linear Flow (horizontal)

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Step 1  â”‚â”€â”€â”€â–¶â”‚  Step 2  â”‚â”€â”€â”€â–¶â”‚  Step 3  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

Rules:
- Arrow `â”€â”€â”€â–¶` on SAME line as box content, between boxes.
- Arrow length = gap between right border of box N and left border of box N+1.
- All boxes in row have IDENTICAL height (same number of lines).

#### 2-Box Horizontal

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   Box A      â”‚          â”‚   Box B      â”‚
â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜          â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
       â”‚                         â”‚
       â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                    â”‚
              â”Œâ”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”
              â”‚  Box C    â”‚
              â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

#### 3-Box Horizontal

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   Box A      â”‚   â”‚   Box B      â”‚   â”‚   Box C      â”‚
â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
       â”‚                  â”‚                  â”‚
       â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â”‚
                    â”Œâ”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”
                    â”‚  Box D    â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

#### Tree (top-down)

```
         â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
         â”‚    Root      â”‚
         â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”
        â”‚                â”‚
  â”Œâ”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”
  â”‚  Child A  â”‚    â”‚  Child B  â”‚
  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

Rules:
- Parent connects to children via `â”œâ”€â”€â”€â”€â”€â”€â”€â”¤` horizontal bar.
- Horizontal bar width = distance from leftmost child center to rightmost child center.
- Each child drops `â”‚` from the horizontal bar at its center position.
- All children in same row have IDENTICAL box width.

### Alignment Checklist (run before every ASCII output)

- [ ] All boxes in same row have equal width (count characters!)
- [ ] All text centered within boxes (Â±1 char OK)
- [ ] Vertical lines `â”‚` align between parent and child
- [ ] Arrows `â–¼` or `â–¶` connect to correct positions
- [ ] No trailing spaces anywhere
- [ ] All diagrams wrapped in ``` code block (monospace)

### ASCII Cutoff â†’ Switch to Mermaid

If the diagram has ANY of these:
- More than 6 boxes in a single row
- Nested hierarchies deeper than 3 levels
- Cross-connections or bidirectional arrows
- Text longer than 24 characters in any box
- More than 4 parallel branches

â†’ Switch to Mermaid for that diagram. Keep ASCII for simpler diagrams in the same document.

## Mermaid Patterns Reference (fallback only)

### Flowchart
```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

### Sequence
```mermaid
sequenceDiagram
    A->>B: message
    B-->>A: response
    B->>C: forward
```

### Gantt
```mermaid
gantt
    title Project Timeline
    section Phase 1
    Task 1:a1, 2026-01-01, 7d
    Task 2:after a1, 5d
```

### Mindmap
```mermaid
mindmap
  root((Topic))
    Branch 1
      Leaf 1a
    Branch 2
      Leaf 2a
```

## Constraints

- **Never** use placeholder text ("TBD", "TODO", "fill in later")
- **Always** include at least one diagram per plan
- **Always** include verification steps (commands, expected output)
- **Always** use exact file paths when referencing code
- **Prefer** ASCII over Mermaid (portable everywhere)
- **Keep** diagrams to 5-9 nodes (readable, not dense)
- **Label** diagram nodes with short text (2-4 words max)
- **Count characters** before writing ASCII boxes

## Integration Notes

- ASCII renders on every platform â€” no renderer dependency
- For HTML output, use the diagram-maker skill instead
- For Excalidraw (editable), use the diagram-maker skill
- This skill targets **markdown-native** output only
