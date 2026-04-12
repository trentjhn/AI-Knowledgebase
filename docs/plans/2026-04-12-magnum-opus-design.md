# Magnum Opus — Design Document

**Date:** 2026-04-12  
**Status:** Approved, ready for implementation  
**Scope:** `/cook` skill + `magnum-opus.md` hub document + supporting infrastructure

---

## What We're Building

Two things that work together:

1. **`magnum-opus.md`** — A hub document in `future-reference/playbooks/` that serves as the decision engine for any new project. Contains workflow phases, decision gates, and pointers to the KB and catalogs. ~400–500 lines. Never contains KB content itself — only routes to it.

2. **`/cook` skill** — A Claude Code system-level skill at `~/.claude/skills/cook/`. The executor. Reads the hub document, traverses KB-INDEX and CATALOG.md files, asks targeted questions, and writes a complete project scaffold to disk.

---

## Architecture — Three Layers

```
LAYER 1 — WORKFLOW LAYER
  magnum-opus.md (hub document)
  "What to do and in what order"
  Update when: workflow phases change, new KB domains are added

LAYER 2 — KNOWLEDGE LAYER
  KB-INDEX.md + LEARNING/ docs
  "What the best practices actually are"
  Update when: new research is captured (existing rule in CLAUDE.md)

LAYER 3 — CAPABILITY LAYER
  CATALOG.md files in agent-catalog/, skills-catalog/, prompt-catalog/
  "What tools and roles are available"
  Update when: any agent/skill/prompt is added (catalog-first convention)

THE SKILL (/cook)
  Reads all three layers, makes decisions, writes files
  Update when: layer interfaces change or new scaffold outputs are added
```

**Runtime flow:**
```
User: "I want to build X"
  → Skill reads magnum-opus.md (workflow phases)
  → Skill reads KB-INDEX.md + CLAUDE.md pattern recognition (relevant KB sections)
  → Skill reads CATALOG.md files (available agents, skills, prompts)
  → Skill asks targeted questions grounded in KB best practices
  → Skill writes complete scaffold to new project directory
```

---

## The Six Phases of magnum-opus.md

### Phase 0: Intake
- Check `.sessions/` for prior investigation context on this topic
- Capture the idea in one sentence (not solution-focused)
- Run CLAUDE.md pattern recognition → route to KB-INDEX.md → read targeted sections only
- **Output:** List of load-bearing KB sections for this project

### Phase 0.5: Domain Research
- Run `last30days` for project domain (HN + YouTube, 30 days)
- Surface what practitioners have discovered recently
- Session context only — informs classification, not saved to files

### Phase 1: Project Classification
- Type: AI/agentic | product/UI | pure engineering | hybrid
- Greenfield vs. existing codebase
- Single agent vs. multi-agent determination
- Select primary playbook(s) from playbooks/README.md
- **Gate:** Project type confirmed, playbooks selected

### Phase 1.5: Specification + Pre-flight
- Write spec using 7-property framework (specification-clarity.md)
- BDD acceptance criteria for every key behavior
- Measurable success metrics — not "better," not "fast"
- Explicit scope boundary: what is NOT in scope
- Pre-flight failure mode check (building-ai-saas.md — four failure modes):
  1. Infrastructure not validated before features
  2. External API fragility not stress-tested
  3. Silent failures (no error handling contract)
  4. Cross-cutting middleware scope leakage
- **Gate:** Spec passes all 7 properties. Someone could implement from it without asking questions.

### Phase 2: Harness Design
- Explicit brainstorm gate: "Has the problem been sufficiently explored?"
- **Four Pillars** (agentic-engineering.md §1):
  - Prompt: system instructions, constraints, output format
  - Model: selection, tier, cost ceiling
  - Context: what loads, what stays out, context budget
  - Tools: available actions, restricted actions, fallbacks
- Context window architecture + token budget (context-engineering.md)
- Memory architecture: short-term / episodic / semantic decisions
- RAG decision gate → building-rag-pipelines.md if retrieval needed
- MCP integration decision → mcp.md if external tools needed
- Execution topology for multi-agent (5 topologies — agentic-engineering.md ~2899)
- Loop pattern selection: ReAct / Plan-Build-Review / Sequential / event-driven
- HITL gate decisions: where humans must approve before execution
- Cost/model tier decision → cost-optimized-llm-workflows.md
- Error handling contract: how failures are surfaced, no silent failures
- SOUL.md character design: functional personality grounded in KB values
- **Gate:** All pillars filled. Topology decided. Error contract written. Character designed.

### Phase 2.5: Build Methodology
- Select from 15 methodologies, 6-tier pyramid (agentic-engineering.md 2865–2935)
- BMAD pattern for complex/multi-agent: docs-as-truth, code-as-consequence
- Adversarial review gates between BMAD phases
- Git workflow + branching strategy

### Phase 3: Capability Selection
- Read `agent-catalog/CATALOG.md` — full pool traversal, select roles
- Read `skills-catalog/CATALOG.md` — select skills
- Read `prompt-catalog/CATALOG.md` — select prompt templates if relevant
- Sequential protocol ordering: define phase sequence for agent pool
- Hook configuration selection (skills-catalog/production/hooks-reference.md)
- **Gate:** All selected catalog entries have CATALOG.md entries (catalog-first verified)

### Phase 4: Scaffold Output

Files written to new project directory:

```
[project-root]/
├── CLAUDE.md                    ← project-specific, KB-grounded operational rules
│                                   Must include: "Read SOUL.md before anything else"
├── AGENTS.md                    ← mission + Sequential protocol ordering (NOT role assignments)
├── SOUL.md                      ← functional personality from SOUL-TEMPLATE.md + Phase 2 decisions
├── README.md                    ← project overview, how to use /cook output
├── .gitignore
├── .claude/
│   ├── agents/                  ← selected role definitions from agent-catalog/
│   ├── skills/                  ← selected skills from skills-catalog/
│   └── settings.json            ← hook configurations
├── docs/
│   ├── kb-references.md         ← POINTERS ONLY (file + line ranges), never copies
│   └── plans/
│       ├── design.md            ← architecture decisions made during phases 1-2
│       └── implementation.md    ← ordered build plan grounded in KB
└── .sessions/[project-name]/   ← local workspace for investigation notes
```

For AI projects, additionally:
```
└── docs/
    └── prompts/                 ← system prompts designed in Phase 2
```

**Done-gate checklist:**
- [ ] All files present
- [ ] `docs/kb-references.md` has pointers for every load-bearing KB section
- [ ] `docs/plans/design.md` captures all Phase 2 decisions
- [ ] Eval criteria defined (before first line of code)
- [ ] Security threat model started
- [ ] `SOUL.md` reflects Phase 2 character decisions, not just default template

### Phase 5: Eval + Security Baseline
- EDD: define success metrics before writing any code (evaluation.md)
- LLM-as-judge setup if output quality needs automated evaluation
- Threat model (ai-security.md — agent-specific attack vectors)
- Observability signals: what you monitor, what alerts you
- Harness optimization path: when to run Meta-Harness after baseline (agentic-engineering.md 842–1746)
- `builds-log.md` update reminder when the project ships

---

## Scaffold Output: Agent Selection Philosophy

Agents self-select roles via Sequential protocol — they are NOT pre-assigned.

**What the scaffold provides:**
- `AGENTS.md`: mission statement + fixed phase ordering
- `.claude/agents/`: the available pool (role definitions without assignments)
- `agent-catalog/CATALOG.md`: traversal index with "when to self-select" per role

**What the scaffold does NOT do:**
- Does not assign specific agents to specific tasks
- Does not hardcode "agent A = security, agent B = architecture"

Agents read the pool, see what predecessors produced, and select the most complementary role. The ordering is fixed; the selection is emergent.

---

## Agent Catalog — New Structure

The existing `future-reference/skills-catalog/agents/` moves to a dedicated `future-reference/agent-catalog/` with this structure:

```
agent-catalog/
├── CATALOG.md          ← flat index: all agents, when to self-select, what they produce
├── README.md           ← catalog structure + soul.md convention documentation
├── SOUL-TEMPLATE.md    ← functional personality template
│
├── core/               ← every project: architect, planner, code-reviewer
├── quality/            ← hardening: security-reviewer, tdd-guide, performance-optimizer, harness-optimizer
├── design/             ← UI/UX (first-class, not optional): ux-researcher, ui-designer,
│                          design-system-architect, accessibility-reviewer, product-designer
├── product/            ← PM layer: product-strategist, spec-writer, technical-writer
├── ai-specialist/      ← AI/agentic only: context-architect, eval-designer, prompt-engineer, kb-navigator
└── meta/               ← coordination: chief-of-staff, loop-operator
```

New agent definitions to create as part of implementation:
- `design/ux-researcher.md`
- `design/ui-designer.md`
- `design/design-system-architect.md`
- `design/accessibility-reviewer.md`
- `design/product-designer.md`
- `product/product-strategist.md`
- `product/spec-writer.md`
- `product/technical-writer.md`
- `ai-specialist/context-architect.md`
- `ai-specialist/eval-designer.md`
- `ai-specialist/prompt-engineer.md`
- `ai-specialist/kb-navigator.md`

---

## Index-First Convention

Every directory that agents traverse must have a `CATALOG.md` flat index.

**Rule:** Write the `CATALOG.md` entry before creating the file (catalog-first).  
**Format:** `name | when to use | what it produces`  
**Enforcement:** `/cook` skill always writes catalog entry first. Post-edit hook validates on file creation.

Applies to:
- `agent-catalog/CATALOG.md`
- `skills-catalog/CATALOG.md`
- `prompt-catalog/CATALOG.md`
- `playbooks/` — extend existing README.md to match format

---

## SOUL.md Convention

SOUL.md encodes functional personality — character traits that improve performance, not aesthetic decoration.

**Lives at:** project root  
**Loaded by:** CLAUDE.md explicit instruction ("Read SOUL.md before anything else")  
**Template:** `agent-catalog/SOUL-TEMPLATE.md`

Core values baked into every SOUL.md (from KB best practices):
- Produces work that looks considered and human, not generated
- Cites KB sections when making architectural decisions
- YAGNI — does not design for hypothetical future requirements
- Prefers reversible actions; flags irreversible ones before taking them
- Verifies before claiming completion
- Direct and skeptical — when something seems too easy, says so

Project-specific personality is layered on top during Phase 2 character design.

---

## Maintenance Contract

| What changes | What to update |
|---|---|
| New KB research captured | KB doc + KB-INDEX.md (existing rule) + review magnum-opus.md for relevant phase pointers |
| New agent added | `agent-catalog/CATALOG.md` first (catalog-first), then agent file |
| New skill added | `skills-catalog/CATALOG.md` first, then skill file |
| New prompt template added | `prompt-catalog/CATALOG.md` first, then template |
| New playbook added | `playbooks/README.md` + KB-INDEX.md |
| Workflow phase logic changes | `magnum-opus.md` + `/cook` skill |
| Scaffold output structure changes | `/cook` skill + this design doc |

This table lives in CLAUDE.md alongside the existing KB maintenance rules.

---

## What This Is Not

- Not a replacement for meta-workflow.md (that covers project management phases; this covers harness construction)
- Not a copy of KB content (hub document routes; KB docs contain the knowledge)
- Not a role assignment system (catalog provides the pool; Sequential protocol governs selection)
- Not a one-time document (maintained as the KB and catalogs grow)
