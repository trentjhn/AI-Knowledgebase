# AI Knowledgebase

A unified reference for AI engineering — synthesized at practitioner depth, organized by learning path, and wired into a meta workflow that applies it automatically to every new project.

*Last Updated: 2026-05-02*

## Why I Built This

AI engineering knowledge is scattered across 100+ sources of wildly varying depth. Most tutorials are either too shallow for practitioners or benchmark-focused (and decay fast). I built this to synthesize core concepts, frameworks, and operational playbooks at practitioner depth — in a form that ages well and actively drives decisions, not just sits on a shelf.

---

## Magnum Opus + `/cook` — The Meta Workflow

The most important thing in this repo isn't any single doc. It's the system that uses all of them together.

**Magnum Opus** is a 9-phase workflow for scaffolding any new AI project from first principles. It is the decision engine — when you start a project, it traverses the KB, fires relevant patterns, asks targeted questions, and produces a complete, production-ready project structure grounded in everything captured here. Recent additions: **Phase 1.6 Premortem Gate** (mandatory for paying clients — runs `/premortem` after spec confirmation, before architecture), and **Phase 2.7 Vibe Coding Oversight Toolkit** (real-time red flags + 8-prompt "Ask Don't Know" checklist for operator oversight during AI-assisted builds).

**`/cook`** is the executor. It reads Magnum Opus and runs every phase interactively: domain research, architecture decisions, agent + skill selection, scaffold generation. When Cook finishes, the project is ready to build.

### Why it's different

Most people start a project by opening a blank file and prompting from memory. Magnum Opus starts a project by querying a curated knowledge library and grounding every decision in captured best practices.

What the scaffold produces isn't just files. It's a **self-describing operating environment**:

- **`CLAUDE.md`** — Session Start Protocol (7-step ordered startup sequence), Development Workflow (exact skill chain for this project type), and Required Rules including enforced session handoffs
- **`AGENTS.md`** — Mission statement + Role Directory (task-level agent routing table, every agent mapped to a trigger condition) + Sequential Protocol Ordering for multi-agent projects
- **`docs/plans/implementation.md`** — Every task annotated with `**Agent: [name]**` so execution-time routing is baked in, not improvised
- **`.claude/agents/`** — Selected agent definitions from the catalog, ready to dispatch
- **`.claude/skills/`** — Selected workflow skills, pre-wired to the project type

**The cold-start problem is solved by design.** When a new session opens on a Cook-scaffolded project, it doesn't need to reconstruct context. The Session Start Protocol instructs it to: load SOUL.md → read AGENTS.md → check the latest handoff → Glob `.claude/agents/*` for fleet discovery → check git log for new agents → invoke the next skills from the handoff. Everything the session needs is already in the scaffold.

**Session continuity is enforced, not hoped for.** Every Cook-generated CLAUDE.md includes a Required Rule: "Before ending any session — complete or interrupted — invoke the `session-handoff` skill. This is not optional." Handoffs capture current workflow phase, active agent fleet, and exact next invocations — so any session can resume from where the last one stopped.

→ **[Magnum Opus hub document](future-reference/playbooks/magnum-opus.md)** — full 9-phase workflow, rationale, done-gates, maintenance contract  
→ **[`/cook` skill](future-reference/skills-catalog/meta/cook/)** — portable executor with install guide  

---

## 📚 LEARNING (Core Reference Topics)

Organized by **learning path**: Foundations → Building → Production. Total ~10,000+ lines across 13 topics.

### [**FOUNDATIONS**](LEARNING/FOUNDATIONS/) — Start Here
**Understand how LLMs work: prompting, context, reasoning**

~1,700 lines | ~6 hours | Prerequisites: none

- [**Prompt Engineering**](LEARNING/FOUNDATIONS/prompt-engineering/) — 9 core techniques (CoT, self-consistency, APE, ReAct) with research results
- [**Context Engineering**](LEARNING/FOUNDATIONS/context-engineering/) — 4 strategies (Write/Select/Compress/Isolate), 4 failure modes, token budgeting; includes the 2026 finding that agentic "memory" is lookup not memory, with provable capability consequences
- [**Reasoning LLMs**](LEARNING/FOUNDATIONS/reasoning-llms/) — When to use reasoning models (o3, Claude 3.7), thinking tiers, design patterns; adaptive retrieval during reasoning
- [**Operator Oversight**](LEARNING/FOUNDATIONS/operator-oversight/) — Vibe coding oversight toolkit: three knowledge domains, minimum competency checks, real-time red flags catalog, "Ask Don't Know" 8-prompt checklist, 4-tier constraint encoding patterns with canonical CLAUDE.md blocks

**→ Next:** Move to [AGENTS_AND_SYSTEMS](LEARNING/AGENTS_AND_SYSTEMS/)

---

### [**AGENTS & SYSTEMS**](LEARNING/AGENTS_AND_SYSTEMS/) — Build (Mid-Level)
**Design and build AI agents and systems**

~5,000 lines | ~11-12 hours | Prerequisites: complete FOUNDATIONS

- [**Agentic Engineering**](LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/) — Four Pillars, Twelve Leverage Points, 6 patterns, tool design, context management, agent teams; includes the Procedural Task Exception (in-context prompting beats LangGraph for step-sequence workflows) and RecursiveMAS research horizon
- [**Agent SDK Patterns**](LEARNING/AGENTS_AND_SYSTEMS/agent-sdk/) — 6 implementation patterns: research agent, chief-of-staff/Task tool, parallel subagents with model tiering, PTC, semantic tool routing, evaluator-optimizer loop
- [**MCP**](LEARNING/AGENTS_AND_SYSTEMS/mcp/) — Model Context Protocol: connecting agents to external systems, tool integrations
- [**Skills**](LEARNING/AGENTS_AND_SYSTEMS/skills/) — Agent Skills standard, testing, composability, portability

**→ Next:** Move to [PRODUCTION](LEARNING/PRODUCTION/)

---

### [**PRODUCTION**](LEARNING/PRODUCTION/) — Ship (Advanced)
**Quality, security, optimization: shipping reliable systems**

~2,400 lines | ~8-9 hours | Prerequisites: complete AGENTS_AND_SYSTEMS

- [**Evaluation**](LEARNING/PRODUCTION/evaluation/) — 3-level eval stack, LLM-as-judge, Eval-Driven Development, frameworks
- [**AI Security**](LEARNING/PRODUCTION/ai-security/) — OWASP Top 10, Zero Trust, sandboxing, agent configuration security
- [**Specification Clarity**](LEARNING/PRODUCTION/specification-clarity/) — 7-property framework, BDD acceptance criteria
- [**Fine-tuning**](LEARNING/PRODUCTION/fine-tuning/) — LoRA/QLoRA, RLHF vs DPO, data requirements, costs
- [**Inference Optimization**](LEARNING/PRODUCTION/inference-optimization/) — Latency, throughput, cost at production scale

**→ Next:** Use [FUTURE-REFERENCE playbooks](future-reference/playbooks/) for practical application

---

## 🎯 CAREER (PM, Interview, Professional Development)

Resources for AI PM roles, interview preparation, and career navigation.

| Section | What's in it |
|---------|-------------|
| [**PM Context**](CAREER/pm-context/) | AI PM role fundamentals, PM frameworks, interview scenarios, AI concepts→PM decision mapping |

---

## 🔧 FUTURE-REFERENCE (Practical Tools & Applied Work)

Ready-to-use guides, templates, and specifications for building AI systems.

| Section | Contents |
|---------|----------|
| [**Magnum Opus**](future-reference/playbooks/magnum-opus.md) | The meta workflow hub. 9-phase project scaffolding: intake → domain research → classification → spec → harness design → methodology → capability selection → scaffold output → eval baseline. Routes to KB; never contains KB content itself. |
| [**`/cook` Skill**](future-reference/skills-catalog/meta/cook/) | The Magnum Opus executor. Runs all 9 phases interactively and writes a complete, session-continuity-ready project structure to disk. Portable — install guide inside. |
| [**Agent Catalog**](future-reference/agent-catalog/) | 24 agent role definitions across 6 categories (core, quality, design, product, AI-specialist, meta). Agents self-select roles via Sequential protocol. See [CATALOG.md](future-reference/agent-catalog/CATALOG.md). |
| [**Playbooks**](future-reference/playbooks/) | 9 practical guides: magnum-opus, production agent patterns, building agents, chatbots, RAG pipelines, cost optimization, multi-agent orchestration, autonomous loops, AI SaaS |
| [**Skills Catalog**](future-reference/skills-catalog/) | Pull-ready skills organized by category (workflow, design, engineering, production, meta). Notable: `/premortem` (mandatory Phase 1.6 gate for SignalWorks engagements), `/sweep` (multi-agent deploy gate), `/cook` (Magnum Opus executor). See [CATALOG.md](future-reference/skills-catalog/CATALOG.md). |
| [**Prompt Catalog**](future-reference/prompt-catalog/) | 16 reusable prompt patterns, example prompts by domain (design, analysis, research). See [CATALOG.md](future-reference/prompt-catalog/CATALOG.md). |

---

## Quick Navigation

**I'm new to AI and want to learn:**
→ Start with [LEARNING/FOUNDATIONS/prompt-engineering](LEARNING/FOUNDATIONS/prompt-engineering/)

**I understand prompting and want to build agents:**
→ Jump to [LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering](LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/)

**I'm building systems and need production guidance:**
→ Read [LEARNING/PRODUCTION/](LEARNING/PRODUCTION/)

**I want to scaffold a new project with all best practices applied:**
→ Use the [/cook skill](future-reference/skills-catalog/meta/cook/) — runs Magnum Opus and writes the full project structure to disk

**I want to deploy agents safely in production with real users:**
→ Read [FUTURE-REFERENCE/playbooks/production-agent-patterns.md](future-reference/playbooks/production-agent-patterns.md)

**I need an agent for my project:**
→ Browse [FUTURE-REFERENCE/agent-catalog/CATALOG.md](future-reference/agent-catalog/CATALOG.md)

**I want to stress-test a plan before committing to it:**
→ Run [`/premortem`](future-reference/skills-catalog/workflow/premortem/) — assumes it already failed 6 months from now, identifies failure modes, routes revised-plan items to spec changes / CLAUDE.md constraints / waivers

**I need prompt templates:**
→ Check [FUTURE-REFERENCE/prompt-catalog/](future-reference/prompt-catalog/)

**I want the full index:**
→ See [KB-INDEX.md](KB-INDEX.md)

---

## Learning Timeline

| Phase | Content | Time | Outcome |
|-------|---------|------|---------|
| **Phase 1** | [LEARNING/FOUNDATIONS/](LEARNING/FOUNDATIONS/) | 6 hours | Understand LLM prompting, context, reasoning, and operator oversight |
| **Phase 2** | [LEARNING/AGENTS_AND_SYSTEMS/](LEARNING/AGENTS_AND_SYSTEMS/) | 11-12 hours | Build functioning AI agents and systems |
| **Phase 3** | [LEARNING/PRODUCTION/](LEARNING/PRODUCTION/) | 8-9 hours | Ship production systems: measurable, secure, reliable |
| **Ongoing** | [FUTURE-REFERENCE/](future-reference/) | As needed | Apply knowledge to real projects via Magnum Opus + Cook |

**Total learning time:** ~25-27 hours (recommend 2-3 hours/week over 8-12 weeks)
