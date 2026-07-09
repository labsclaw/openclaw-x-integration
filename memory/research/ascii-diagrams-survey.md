# ASCII Diagrams Skill Research — 2026-07-08

## Repos Surveyed

### 1. jasnell/opencode-skill-ascii-art-diagrams
- **Best from:** Mandatory 3-phase workflow (PLAN → DRAW → VERIFY)
- **Key innovation:** Python grid.py for precise column placement, verify.py for automated checking
- **Character whitelist:** Only `+ - | > < ^ v / \`
- **Junction rule:** Every `|` touching horizontal line needs `+` at exact column
- **Templates:** Flowcharts, decision trees, sequence, state machines, UML class, nested components, star networks, fan-out/fan-in pipelines, RFC packets, git branches, memory layouts
- **Reference:** Comprehensive REFERENCE.md with box construction patterns, connection templates, common mistakes

### 2. github/awesome-copilot plantuml-ascii
- **Best from:** PlantUML integration for auto-generating ASCII from .puml files
- **Key innovation:** `-txt` (pure ASCII) and `-utxt` (Unicode-enhanced) output modes
- **Supports:** Sequence, class, flowchart, state, component, deployment, use case diagrams
- **Use case:** When manual construction is too complex, delegate to PlantUML

### 3. tjboudreaux/cc-plugin-text-visualizations
- **Best from:** 5 focused skills for different diagram types
- **Skills:** workflows, architecture, state machines, cheatsheets, retrospectives
- **Key innovation:** /diagram unified command, /ops-standup, /ops-retro
- **Use case:** Domain-specific diagram generation with consistent style

### 4. agavra/yuzudraw
- **Best from:** Visual canvas editor + DSL for precise diagram construction
- **Key innovation:** macOS-native app with agent skill, DSL for rects/arrows/groups/layers
- **DSL features:** Auto-sizing, relative positioning (right-of, below), style variants (rounded, double, heavy), shadows, fills
- **Export:** ASCII, PNG, SVG
- **Use case:** Generate ASCII, then refine visually on canvas

### 5. gianlucamazza/mcp-ascii-charts
- **Best from:** Data visualization (line, bar, scatter, histogram, sparkline)
- **Key innovation:** MCP server for chart generation, ANSI colors, configurable dimensions
- **Use case:** When diagram is about DATA (not structure), use chart-specific rendering

## Synthesis: What went into the ultra skill

| Source | Contribution |
|--------|-------------|
| jasnell | PLAN/DRAW/VERIFY workflow, junction rules, character whitelist, box patterns |
| awesome-copilot | PlantUML fallback for complex diagrams |
| cc-plugin | Family classification (workflows, arch, state, cheatsheets, retro) |
| yuzudraw | DSL reference, visual editing integration, family selection logic |
| mcp-ascii-charts | Data chart rendering (line, bar, scatter, histogram, sparkline) |

## Key Design Decisions

1. **Plan-first approach** (from jasnell): Column ruler before drawing eliminates alignment errors
2. **Character whitelist** (from jasnell): Only ASCII chars for structural diagrams; Unicode allowed for data charts
3. **Family classification** (from yuzudraw): Classify request into dominant diagram type first
4. **Data vs Structure split** (from mcp-ascii-charts): Data charts use different rendering rules than structural diagrams
5. **Optional integrations** (from yuzudraw + awesome-copilot): PlantUML and YuzuDraw as fallbacks, not requirements
