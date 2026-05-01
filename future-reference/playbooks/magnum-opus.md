# Magnum Opus — Project Scaffold Workflow

> The complete decision framework for starting any project with Claude Code.
> Traverses the KB, selects agents and skills, and produces a production-ready scaffold.

**Last updated:** 2026-04-12  
**Used by:** `/cook` skill at `~/.claude/skills/cook/SKILL.md`

---

## Three Questions That Must Be Answerable Without Running Code

Before any phase below produces output, the operator (and `/cook`) must be able to answer three diagnostic questions for the system being built:

1. **Where does state live?** (Who owns the truth? Database / files / external service / in-memory / multiple distributed locations.)
2. **Where does feedback live?** (How do we know the system is working? Logs / metrics / alerts / dashboards / user feedback / silent until broken.)
3. **What breaks if I delete this?** (For every non-trivial component: blast radius. Everything fails / one feature degrades / silent wrong-answer / data corruption.)

**Why these come first:** per Peter Naur's 1985 paper "Programming as Theory Building," the program is the *mental model* of how pieces connect; the code is its shadow. AI generates the shadow on demand, but the theory must be deliberately built. These three questions surface the architectural facts that prevent the system from collapsing under its own complexity. Without them, AI-built systems become incoherent monoliths where state lives everywhere, feedback lives nowhere, and the impact of deleting anything is unknown — the failure mode from the video summary `7zCsfe57tpU`'s 7,000-line single-file horror story.

**Where these questions get asked:**
- **Phase 0 (Intake)** — at the very first capture of the project description, before any design work.
- **Phase 1.5 (Spec + Pre-flight)** — included in the 7-property spec framework; spec is incomplete if these aren't answerable.
- **Phase 4 (Scaffold Output)** — `docs/plans/design.md` includes mandatory sections "State Architecture", "Feedback Architecture", "Deletion Blast Radius."
- **Phase 5 (Eval + Security Baseline)** — re-asked because eval and security both depend on knowing where state and feedback live.
- **At every audit sweep** — code-correctness audit prompt flags if the answers can't be derived from current docs/code.

**The jagged frontier:** AI is sharp in some areas and surprisingly dull in others, often within the same session. Some decisions belong with the operator regardless of authority — novel-domain architecture, security-critical algorithm choice, state machine design, irreversible production operations, cross-system contracts, anything where probabilistic behavior could compound into wrong-answer-at-scale. These don't go in autonomous-decision lists; they go in pause-for-operator with explicit reasoning.

**Treat the doc spine as theory-building, not bureaucracy.** When the theory lives in `docs/plans/design.md` + `decision-log.md` + `invariants.md` + handoff chain, any operator (or fresh Claude session) can pick up cold. When it lives only in someone's head, the project dies if that person leaves.

---

## How This Document Works

This hub sits between two things: the workflow (what to do and in what order) and the knowledge (what the best practices actually are). It is deliberately a routing document — it contains no KB content itself. When it says "see context-engineering.md lines 132-204," that's where the actual knowledge lives. The hub stays lean so it can be read in full without overhead.

The three layers that make this system work:

- **This document** — defines the phases, the decision gates, and where to route for knowledge. Update when workflow phase logic changes.
- **KB-INDEX.md + LEARNING/ docs** — the actual best practices, updated as research is captured. Update when new knowledge is added.
- **agent-catalog/CATALOG.md + skills-catalog/CATALOG.md** — the available agents and skills. Update catalog entries before creating files (catalog-first convention).

The `/cook` skill reads this document first, then follows the phase sequence below in order. Phases are not optional. Gates are not optional. Skipping a phase trades short-term speed for downstream rework that is always more expensive.

The layer separation is intentional and load-bearing. If KB content were copied into this document, this document would need to be updated every time KB research is updated — creating a maintenance burden that guarantees staleness. If workflow logic were embedded in KB docs, those docs would be harder to read as reference material. The hub routes; the KB teaches; the catalogs list.

**What would go wrong without this document:** Each project would start from scratch, with no systematic connection to accumulated best practices. The KB exists but stays inert — read in some sessions, ignored in others. Projects built without a systematic pre-flight check hit the same failure modes that have already been studied and documented: infrastructure not validated, silent failures by design, specs that only one person understood. This document is what closes the loop between learning and building.

**How to read it:** Work through phases in order. At each gate, do not advance until the gate conditions are met. When a phase references a KB section, read that section — don't rely on prior knowledge or memory of what it said. The KB evolves; summaries of it don't.

---

## Phase 0: Intake

The intake phase has one job: capture what the project actually is before anyone starts designing a solution. Most wasted effort in project starts comes from solution-first thinking — someone describes the tool they want to build rather than the problem it solves, and the entire downstream scaffold is built around the wrong thing. The spec changes mid-build, the harness gets redesigned, agents produce work that doesn't connect.

**What goes wrong if you skip this:** You start designing a solution before understanding whether you're solving the right problem. This is the most expensive mistake in software, and it happens constantly because describing a solution feels like progress.

**Steps:**

1. **Check `.sessions/`** — Look in `/Users/t-rawww/AI-Knowledgebase/.sessions/` for any prior notes on this project or domain. If a prior session exists, read it first. Don't re-derive context that's already been captured. The `.sessions/` directory exists specifically to preserve mid-investigation context across sessions.

2. **One-sentence capture** — Ask: "Describe the project in one sentence — what problem does it solve for whom?" The sentence should be problem-focused, not solution-focused. "I want to build an AI that reads PDFs" is solution-focused. "Researchers spend 30 minutes skimming papers to decide if they're worth reading" is problem-focused. If the description is solution-focused, push back: "What problem causes you to want that solution?"

3. **Read and apply CLAUDE.md pattern recognition** — First, explicitly read `/Users/t-rawww/AI-Knowledgebase/CLAUDE.md` into context. If /cook is invoked from a project directory rather than the KB root, Claude Code will not auto-load the KB's CLAUDE.md — it must be read directly. Then apply the pattern rubric to the one-sentence description. Multiple patterns can fire simultaneously. Surface all matches — don't pick one silently. If agent teams, RAG, and evaluation all fire, say so explicitly and frame the decision about which to prioritize.

4. **Route to KB-INDEX.md** — For each fired pattern, read the corresponding KB section. Use KB-INDEX.md to find exact line ranges. Read targeted sections only — never the full doc. The KB is dense; targeted reads are the only sustainable way to use it.

**Gate output:** A list of load-bearing KB sections for this project, by file path and line range. These become the citations in `docs/kb-references.md` and the foundation for Phase 1.5 and Phase 2 decisions.

---

## Phase 0.5: Domain Research

Before classification, surface what practitioners have actually learned recently. Research papers and official docs are the authoritative sources on what has been proven — but they lag the field by 6-18 months. What practitioners are discovering now, on HN, in YouTube build logs, in open source issues, often surfaces failure modes and integration patterns that don't exist in formal literature yet.

**What goes wrong if you skip this:** You scaffold a project using KB knowledge that was accurate 6 months ago, missing a critical ecosystem change — a library deprecation, a new model capability, a failure mode that's become common since the KB was last updated. The KB is a baseline, not a live feed.

**Steps:**

1. Run the `last30days` skill for the project domain, specifying HN + YouTube with a 30-day window. For rapidly evolving domains — new model releases, breaking API changes, an ecosystem in flux — narrow to 7 days. The skill handles discovery; you synthesize.

2. Hold findings in session context only. Do not write to files. This research informs decisions; it is not a deliverable. If something warrants permanent capture, synthesize it into the relevant KB doc after the project is done.

3. Surface 2-3 practitioner findings that are relevant to the project. Frame them clearly: "Practitioners have found that [X]. This suggests [Y] may be a risk or opportunity for this project."

**Note:** Practitioner findings supplement, not replace, KB knowledge. When a practitioner finding contradicts KB best practices, flag the contradiction explicitly — explain which evidence is stronger and why. Don't quietly side with the newer finding just because it's newer.

---

## Phase 1: Project Classification

Classification determines which playbooks apply, what complexity level the project demands, and whether multi-agent coordination is warranted. Getting this wrong early cascades — a project classified as "simple single-agent" that's actually multi-agent will hit coordination problems at the worst possible time, when significant work has already been done in the wrong architecture.

**What goes wrong if you skip this:** You start building without knowing what you're building. Scope expands laterally. The wrong playbook gets applied. A project that needed BMAD process gets none; a simple 2-hour script gets over-engineered with agent orchestration.

**Type decision:**

An AI/agentic project uses LLM calls as core functionality — the model is doing work that drives the product's value. A product/UI project has user-facing interfaces as the primary value; AI features may be present but aren't the core. Engineering infrastructure is tooling, automation, pipelines — the output serves developers, not end users. Hybrid projects span two or more types and need to acknowledge that explicitly, since each type has different playbooks, different failure modes, and different success metrics.

**Greenfield vs. existing:**

Greenfield means starting from scratch in a new repo. Existing means adding to a codebase that has conventions, history, and constraints that were made by people who had reasons. Existing codebases require a read-first step before design — never design without understanding what's there. Check the git log, read the CLAUDE.md if present, read the main entry points. Design that ignores existing conventions creates maintenance debt immediately.

**Single agent vs. multi-agent vs. agent teams:**

These are meaningfully different architectures, and choosing between them shapes the entire build.

A single agent with good tools can handle most tasks. It has no coordination overhead, no communication failures between agents, and a single context that contains everything relevant. Default here unless there's a specific reason not to.

Multi-agent with a hierarchical orchestrator is warranted when tasks are genuinely parallel (different agents can work simultaneously without blocking each other), when fundamentally different expertise is needed, or when the task pool is large enough that one agent working sequentially is the bottleneck. In this pattern, an orchestrator delegates to workers and synthesizes their outputs. The orchestrator's context is where coherence lives.

Agent teams (source: `LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agent-teams.md`) are a distinct pattern: a pool of peer agents that share a task list and communicate directly with each other, without a fixed orchestrator. No single agent owns the workflow. Agents pick up tasks from the shared list, post their outputs, and message peers when a downstream agent needs to know something. This topology is best when: the task structure is emergent rather than fixed, different perspectives on the same problem add value (competing hypotheses, adversarial review), or the team needs to adapt dynamically as tasks produce unexpected subtasks.

Agent teams are not hierarchical. They are not "multi-agent with a flat org chart." The key differences: peer sessions share a task list visible to all agents; agents message each other directly rather than routing through an orchestrator; no agent has global visibility or control. This means coordination is distributed — powerful when the task benefits from it, fragile when the task needs tight sequential ordering.

Decision heuristic: use single agent for most tasks. Use hierarchical multi-agent when parallel execution of defined subtasks matters. Use agent teams when competing perspectives or emergent task structure is the point. If uncertain, single agent first.

**Playbook selection:**

Based on type and complexity, select from `future-reference/playbooks/README.md`:

- **AI/agentic projects** → `building-ai-agents.md` (primary); add `building-rag-pipelines.md` if retrieval is needed; add `building-ai-saas.md` for the four failure mode pre-flight check
- **Marketing sites and static frontends** → `building-professional-websites.md` — this playbook includes Lighthouse performance gate, Core Web Vitals targets, responsive QA at fixed breakpoints, and OG/metadata pass; do not use the AI agent or SaaS playbooks for these projects
- **Conversational products** → `building-chatbots.md`
- **Single LLM call pipelines** → `writing-production-prompts.md`
- **Hybrid projects** → apply all matching playbooks; state explicitly which takes precedence when they conflict

**Gate:** Project type confirmed. Playbooks selected. Multi-agent decision made and written down with a one-sentence justification.

---

## Phase 1.5: Specification + Pre-flight

Specifications exist to prevent the most common and expensive mistake in software: building the right solution to the wrong problem, or building the wrong solution to the right problem. A spec that satisfies all 7 properties means a developer can implement it without asking a single clarifying question. A spec that fails any one of them will produce ambiguous work that requires renegotiation mid-build.

**What goes wrong if you skip this:** Implementation begins before anyone agrees on what "done" means. Scope creeps because the boundaries weren't stated. Different people have different mental models of what the feature does. The build ends and it fails review because the acceptance criteria were never written.

**The 7-property framework** (source: `LEARNING/PRODUCTION/specification-clarity/specification-clarity.md`):

1. **Complete** — No context assumed. A new engineer with no context could implement it. If you have to explain something verbally that isn't in the spec, the spec is incomplete.
2. **Unambiguous** — Every term has exactly one interpretation. "Fast" is ambiguous. "< 200ms p95 latency measured at the API boundary" is unambiguous.
3. **Consistent** — Requirements don't contradict each other. "Must work offline" and "requires real-time API calls" is a contradiction. These need resolution before implementation.
4. **Verifiable** — Every requirement is testable. "Should feel good to use" is not testable. "Completes the core action in ≤ 3 interactions from any starting state" is testable.
5. **Bounded** — Scope is explicit. What is NOT in scope is listed. Unbounded specs grow until they consume the project.
6. **Prioritized** — Trade-offs are stated. "If latency and accuracy conflict, accuracy wins" is a prioritization. Without it, every trade-off becomes a debate during implementation.
7. **Grounded** — Abstract goals are linked to concrete examples. For every abstract requirement, there is at least one concrete scenario that illustrates what it means.

For each property, ask a targeted question until the property is satisfied. Don't proceed with partial specs — every gap will be filled by whoever is implementing, and their assumptions may be wrong.

**BDD acceptance criteria:** Write at least one Given/When/Then scenario for every key behavior. Scenarios are contracts, not documentation:

```
Given a user whose session has expired
When they attempt to load /dashboard
Then they are redirected to /login
And their intended URL is preserved as ?redirect=/dashboard
And the page shows: "Your session expired. Please log in again."
And no dashboard data is fetched before authentication
```

This scenario is not documentation of expected behavior — it is the definition of when "session expiry handling" is done.

**Success metrics:** Every metric must have a baseline and a target. "Users will find it helpful" is not a metric. "Support ticket volume for [error category] drops from 50/day to 15/day, measured in Zendesk, within 60 days of launch" is a metric. If you can't measure it, you can't know if you built it.

**Definition of done (`docs/done.md`)** (source: `future-reference/skills-catalog/workflow/project-done-definition/`):

Beyond the spec (what to build) and BDD scenarios (how behavior verifies), every project needs a completion contract that spans four axes: functional, quality, external validation, and operational. A spec defines *what*; `done.md` defines *when you can ship*. Write it before implementation begins — the template and stopping rule live in the skill linked above. A functionally complete but operationally dangerous project (secrets in repo, no rollback plan, no known-issues list) is not done. A technically perfect project that no stakeholder has ever used end-to-end is not done. Invoke the `project-done-definition` skill to generate `docs/done.md` with verifiable checklist items across all four sections — capped at ~15 items total, every item testable or observable. Projects scaffolded by /cook inherit this as a Phase 1.5 requirement, not an optional hardening.

**Pre-flight failure mode check** (source: `future-reference/playbooks/building-ai-saas.md`):

Run these four checks before committing to design. They surface the failure modes that kill projects after significant investment — not at the planning stage where they're cheap, but at the delivery stage where they're catastrophic:

1. **Infrastructure not validated before features** — Is the core technical foundation confirmed to work? Auth, data persistence, external API connectivity, deployment pipeline? If any of these are assumed rather than proven, validate them before feature work begins.
2. **External API fragility** — Does the project depend on external APIs? Have rate limits, error handling, uptime SLAs, and fallback behavior been documented? External API failures will happen in production. The question is whether you've designed for them.
3. **Silent failures** — Is there an error handling contract? When a model call fails, what happens? When output doesn't match the expected format? Silent failures — where the system proceeds as if nothing went wrong — are the hardest bugs to diagnose. They don't fail loudly; they produce subtly wrong results that may not be noticed for days.
4. **Cross-cutting scope leakage** — Are there middleware or cross-cutting concerns (logging, authentication, rate limiting, caching) whose scope could expand unpredictably? These have a history of consuming more implementation time than the core feature. Bound them explicitly.

**Gate:** Spec passes all 7 properties. Pre-flight check complete with explicit yes/no on each of the four failure modes. A developer who read only this spec could implement the feature correctly.

---

## Universal AI System Patterns

Two production-validated patterns that apply to any AI project, not just consulting work. Reference from Phase 2 (Harness Design) when designing prompts and eval loops.

### Expose the validation predicate's mechanism to the LLM, not just the rule

When an LLM's output is post-validated by code (grounding check, schema validation, regex match, allow-list), the system prompt should describe HOW the validation runs — not just the abstract rule. Example: instead of "do not paraphrase," include a `CRITICAL — VERBATIM RULE` callout: "The post-processing gate runs `display_text in raw_text` (whitespace-normalized, case-insensitive). If even one character was rephrased, normalized (e.g., 'Apr.' to 'April'), or had a typo 'fixed', the item is silently dropped."

Pair the rule with concrete ❌/✅ examples that mimic exact field-observed failure modes (date abbreviation, synonym swap, sentence merge). Models pattern-match against shapes they can satisfy more reliably than they comply with abstract directives.

**Concrete:** brett-roberts-la-metro v1.8 → v1.9 prompt revision. v1.8 said "do not paraphrase display_text"; model still paraphrased ~20-40% of items, dropped silently by post-processing. v1.9 exposed the gate mechanism + 3 ❌/✅ pairs; model then omitted items it couldn't span verbatim rather than producing paraphrases that fail silently. Provenance: brett-roberts-la-metro, 2026-04-25.

### Quantitative pass gate beats free-form self-grading in evaluator-optimizer loops

When iterating on a complex artifact (dashboard, prompt, agent output), define pass criteria with explicit weights and a numeric pass gate before dispatching evaluation. The score makes deltas legible across iterations; the per-criterion weights make it obvious which fixes matter. Force structured deductions tied to specific evidence (HTML lines, item counts, log strings).

**Never let an evaluator agent free-form "rate the work"** — they're charitable. Quantitative scoring with deductions tied to evidence catches real gaps; free-form scoring drifts toward "looks great."

**Concrete:** brett-roberts-la-metro Step 6 verification dispatched evaluator with 8 weighted criteria + 95/100 pass gate. Pass 1 = 76/100 with 3 cited deductions. After fixes, Pass 2 = 82/100 with remaining −13 traced to one root cause that was scoped out as deliberate deferral. Score deltas were legible; weights made priority obvious. Provenance: brett-roberts-la-metro, 2026-04-25.

---

## Phase 2: Harness Design

The harness is the set of decisions that determine how the AI system behaves. These decisions compound — a bad context architecture leads to degraded outputs at scale; poor model selection leads to cost overruns; no error contract means production failures that take hours to diagnose; no character design means behavioral variance that undermines trust.

Make these decisions explicitly. Write down the rationale. The rationale is not for documentation purposes — it is for the moment, three weeks later, when you need to know why a decision was made and whether that reason still applies.

**Brainstorm gate first:** Before filling out the Four Pillars, ask whether the problem has been sufficiently explored. If the user jumped from idea to solution without exploring alternatives, run the `brainstorming` skill. Premature commitment to a specific architecture before understanding the problem space is a leading cause of expensive rewrites. The cost of one brainstorming session is trivial compared to the cost of rebuilding an architecture.

**The Four Pillars** (source: `LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md` §1):

Each pillar is a distinct design dimension. Weakness in any one degrades the whole system.

**Prompt pillar:** What are the system instructions? What constraints must always be enforced, regardless of what the user asks? What output format is required for downstream consumers? Draft the system prompt now in rough form — it will be refined when writing the actual prompts in Phase 4, but the shape and key constraints should be clear. A prompt without explicit constraints will produce constraint violations in production.

**Model pillar:** Which model tier matches the task? Haiku for high-volume, low-complexity tasks where cost is primary; Sonnet for the majority of complex reasoning and generation work; Opus for architectural decisions, complex multi-step reasoning, and work where quality is primary. Set a cost ceiling per request and per session. Cost ceilings are not optional — without them, prompt design has no constraint, and unconstrained prompt design drifts toward expensive.

**Context pillar:** What information does the model need to perform this task well? What should stay out? This requires explicit design, not assumption. Overcrowded context degrades model performance as reliably as underpowered models — this has empirical backing. The failure mode is noise crowding out signal. Design what goes in and what stays out.

**Tools pillar:** What actions can the agent take? What actions are explicitly restricted? What is the fallback behavior if a tool call fails or returns unexpected output? Unrestricted tools in production systems create blast radius. Define the tool set as narrowly as the task allows — you can expand later.

**Context window architecture** (source: `LEARNING/FOUNDATIONS/context-engineering/context-engineering.md` lines 132-204):

Map the 8 context components (system prompt, user input, conversation history, retrieved knowledge, tool definitions, tool results, agent scratchpad, external memory) and decide for each: always present, conditional on some trigger, or never. Then define the token budget: what fraction of the window is allocated to each component, what the compaction trigger is (50% of window, not 90%), and what gets summarized when compaction fires.

**Memory architecture:** Three types with distinct purposes. Short-term memory is what survives the current turn — it's the conversation context and it resets. Episodic memory is what persists across sessions — interaction history, prior decisions, user corrections. Semantic memory is distilled knowledge that should always be available — facts that have been extracted and stored separately. Most projects only need short-term. Multi-session products with returning users need episodic. Knowledge-intensive applications need semantic.

**RAG decision gate:** If the project requires searching a document corpus, retrieving context relevant to a query, or answering questions over a knowledge base, stop here and route to `future-reference/playbooks/building-rag-pipelines.md`. RAG architecture is complex enough to warrant its own playbook. Don't design RAG inside a general harness design session.

**MCP decision gate:** If the project needs to connect to external tools, APIs, file systems, or services via the Model Context Protocol → route to `LEARNING/AGENTS_AND_SYSTEMS/mcp/mcp.md` for integration design. MCP changes what tools are available to the agent and requires its own design pass.

**Execution topology** (multi-agent only, source: `agentic-engineering.md` ~line 2899):

Select from the available topologies and match to the actual structure of the work:

- **Sequential:** Agents pass work down a pipeline in order. Each agent receives the previous agent's output. Use for ordered, deterministic workflows where dependencies are fixed.
- **Parallel:** Agents work simultaneously on independent tasks. Use when subtasks have no dependencies on each other and the bottleneck is throughput.
- **Expert Swarm:** Specialized parallel pattern for consistency-critical scale. A lead maintains a shared expertise file (expertise.yaml, max ~750 lines) that all workers read by path — never copied into context. Workers execute in parallel with read-only access; an improve agent analyzes all outputs and updates expertise once after the swarm completes (Learning Separation Rule — prevents race conditions). Each worker runs in its own git worktree for filesystem isolation. After swarm completion, a merger agent reconciles branches through tiered conflict resolution. Use when: multiple independent tasks within one domain, consistency across outputs is critical, domain expertise is codified. **Cost caveat:** a 20-agent swarm can cost 6.6× more than sequential work for the same result — default to single agent first, swarm only when embarrassing parallelism is genuine. Source: `agentic-engineering.md` Expert Swarm section.
- **Hierarchical:** An orchestrator delegates to specialized workers and synthesizes results. Use when coordination requires a central point of visibility and control.
- **Agent teams (peer):** Agents share a task list and communicate directly without a fixed orchestrator (source: `LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agent-teams.md`). Use when task structure is emergent, when competing perspectives add value, or when the team needs to self-organize around a complex problem. The key constraint: agents post to a shared task list and send direct messages — there is no global coordinator.
- **Event-driven:** Agents respond to asynchronous triggers rather than executing a fixed sequence. Use for reactive systems where the workflow is determined by external events.

Don't pick a topology because it sounds sophisticated. Match the topology to the task's actual coordination requirements.

**Loop pattern selection:** ReAct for tool-using agents that need to reason about intermediate results before taking the next action. Plan-Build-Review for tasks where the quality of the plan determines the quality of the output. Sequential pipelines for deterministic ordered work. Event-driven for systems that react to external signals rather than executing a fixed sequence.

**HITL gates:** Where must a human approve before execution continues? Mark these explicitly in the design document. The minimum for any production system: before any irreversible action. Deleting data, publishing content, sending messages, deploying to production — all require a HITL gate. "It works in testing" is not a justification for skipping these gates.

**Cost and model tier decision:** State the expected token volume, the acceptable cost ceiling per session or request, and the routing logic if multiple model tiers are used. For high-volume applications, the difference between Haiku and Sonnet is significant at scale.

**Error handling contract:** This must be explicit before any code is written. For every type of failure: model API failure, tool execution error, output format mismatch, rate limit, timeout — what is the behavior? Surface the error? Retry with exponential backoff? Fall back to a simpler approach? Log and continue? "Handle it gracefully" is not a contract. The contract specifies observable behavior for each failure type.

**SOUL.md character design:** What is the functional personality of this agent? This is not aesthetic — it is behavioral specification. Draw from `future-reference/agent-catalog/SOUL-TEMPLATE.md` for the core values (YAGNI, verify before claiming completion, reversible actions preferred, cite sources) and add project-specific character in the [PROJECT CHARACTER] section. Character design reduces variance. Without it, the agent's behavior under ambiguous conditions is undetermined.

**Gate:** All Four Pillars filled. Topology decided (if multi-agent). Error contract written for every failure type. Character designed. All decisions documented in `docs/plans/design.md` with rationale.

---

## Phase 2.5: Build Methodology

How you build matters as much as what you build. The wrong methodology for the project complexity leads to either over-process (writing full BMAD design docs for a 2-hour script, which is waste) or under-process (skipping design docs for a 3-month multi-agent system that will need debugging by multiple agents across sessions, which creates coordination chaos).

**Methodology selection** (source: `agentic-engineering.md` lines 2865-2935, the 15-methodology 6-tier pyramid):

The 6-tier pyramid maps complexity to methodology. Read the relevant section and match methodology to project complexity. The core principle: use the simplest methodology that won't break under the project's actual constraints. Add process when the cost of coordination failure or rework exceeds the cost of documentation.

**BMAD pattern** for complex/multi-agent projects: Behavior-driven Modeling and Design — docs-as-truth, code-as-consequence. Every architectural decision lives in a document before it lives in code. Documents are reviewed adversarially before implementation proceeds. When a decision changes, the document changes first. This is overhead that pays for itself on projects that span multiple sessions or multiple agents — because agents read documents to understand context, not code.

**Adversarial review gates** in BMAD: Between phases, a reviewer reads the preceding document looking for flaws, not for confirmation. The adversarial posture is not optional — a reviewer who is trying to validate will find fewer problems than a reviewer who is trying to break it.

**Git workflow:** Define the branching strategy before writing the first line of code. Feature branches with PRs for multi-contributor projects. Main-only for solo, fast-iteration work. The workflow should match team size and the frequency of deployment. Committing directly to main on a solo project that deploys on commit is a valid workflow. Doing the same on a team project is not.

**Expert Swarm isolation:** If Expert Swarm topology was selected in Phase 2, configure git worktrees before spawning workers (source: `superpowers:using-git-worktrees` skill). Each worker agent gets its own worktree on a dedicated branch — this is stronger isolation than context-only. Workers cannot accidentally overwrite each other's filesystem state. After the swarm completes, dispatch a merger agent from `agent-catalog/meta/merger.md` to reconcile worker branches through tiered conflict resolution before proceeding to Phase 3.

---

## Phase 2.7: Vibe Coding Oversight Toolkit

Effective AI-assisted development requires the operator to hold a working mental model of what correct looks like — not deep expertise, but enough to spot when the AI is drifting. This phase verifies that mental model exists, provides the real-time oversight tools for the build session, and encodes the technical constraints that make fragile AI defaults impossible to produce accidentally.

**Source:** `LEARNING/FOUNDATIONS/operator-oversight/operator-oversight.md` — read the full doc for educational depth on all three knowledge domains (architecture, networking, programming fundamentals). This phase contains the operational extracts for active use during a build.

**What goes wrong if you skip this:** The AI generates code that looks correct, passes review, and then fails at production scale or under unusual conditions. The most common failure modes — wrong data structures at scale, retry logic that creates duplicate actions, auth logic scattered across route handlers, destructive operations without guards — are systematically present in AI training data and will be reproduced unless explicitly constrained.

**Operator competency check (Phase 0 gate, repeated here as a reminder):**

Before the build begins, verify the operator can answer these three questions. If the answer is "I don't know," that's not a blocker — but it means the constraint blocks below carry more weight, because they substitute for judgment the operator can't yet supply.

1. Can you describe the data flow for this system from user action to persistence in plain English?
2. What would break if one specific component were removed?
3. Name one security boundary — what should never leave the server, what user input should never touch directly?

**Real-time red flags during generation:**

These are signals to act on *while the AI is generating*, not at audit time. Each one indicates either architectural drift or a systematic wrong default.

- AI creates a new file, directory, or abstraction for a problem that fits in ~50 lines → unnecessary complexity; push back and ask why the new boundary is needed
- AI adds an external dependency for something stdlib handles → training-data interpolation, not stack-aware; ask if the stdlib version would work
- The same concept appears in two places (two state representations, two data structures for the same entity) → agent lost the data model; clarify and consolidate
- Auth or permission logic appears inline in route handlers instead of middleware → enforcement will be inconsistent; ask for centralization
- `try/catch` with empty body, API call with no error path → A4 silent failure; ask what happens when the call fails
- AI presents "a few ways to do this" without recommending one → underspecified constraint; make the architectural decision explicitly and encode it in CLAUDE.md, not in conversation

**The "Ask, Don't Know" operator checklist:**

Use after any significant block of generated code. These are questions to ask the AI about its own output — not things to diagnose yourself. The AI will often catch its own mistakes when asked directly, especially when it doesn't have session context defending prior decisions.

1. "What happens to this performance with 100x more data?" — surfaces O(n²), wrong data structures
2. "Are there database, API, or file calls inside any loop?" — surfaces N+1 query problems
3. "What does this do if the input is empty, null, or the service is unavailable?" — surfaces happy-path-only code
4. "Can you describe what this function does without using 'and'?" — surfaces single-responsibility violations
5. "Does any part of this delete or permanently modify data? What prevents accidental trigger?" — surfaces missing guards
6. "Does any function use a variable that wasn't passed to it as a parameter?" — surfaces global state
7. "Is there similar logic elsewhere in the codebase this could reuse?" — surfaces parallel implementations that will diverge
8. "Are any URLs, timeouts, limits, or keys written directly in the code?" — surfaces hardcoded configuration

**Constraint encoding:** The most durable way to prevent fragile defaults is to make the right pattern easier than the wrong one. The two canonical constraint blocks (Networking and Code Quality) are defined in the Phase 4 CLAUDE.md template and must be present in every project scaffold. Rules in CLAUDE.md don't decay over a session; conversational instructions do.

---

## Phase 3: Capability Selection

With the project classified, spec'd, and harness designed, select the specific agents and skills that will execute the build. This phase translates the design decisions from Phases 1-2 into an actual team of capabilities.

**What goes wrong if you skip this:** Agents get picked arbitrarily, or default agents get used regardless of project type. A UI project launches without a design agent. An AI project launches without an eval designer. The capability gap only becomes visible when the work starts and something important is missing.

**Agent pool traversal:** Read `future-reference/agent-catalog/CATALOG.md` in full. The self-select column for each agent describes when it's appropriate. Core agents are included in every project — architect, planner, code-reviewer, and doc-updater cover the baseline. Quality agents depend on the hardening requirements and the risk tolerance of the project. Design agents are required for any project with a user-facing interface — not optional, not "nice to have if there's time." Product agents are required when vision is unclear or requirements are fuzzy. AI-specialist agents are required for any AI/agentic project — context architect and eval designer in particular. Meta agents are added only for projects with genuine multi-agent coordination complexity.

**Skills selection:** Read `future-reference/skills-catalog/CATALOG.md`. Skills operate in two tiers — apply different logic to each:

**Tier A — Guardrails (always include, every project):** These prevent quality failures regardless of project type. Skills only fire when their trigger phrases match, so installing them broadly has negligible overhead. Always include: `brainstorming`, `planning`, `smart-commit`, `deslop`, `pre-ship`. These are the floor, not the ceiling.

**Tier B — Domain skills (select based on project type):** These are powerful but context-specific. Include when the project actually calls for them — don't include when they'd never trigger. UI project → include `frontend-design`, `ui-ux-pro-max`. AI project → include `context-budget`, `eval-harness`. Auth or production exposure → include `security-review`. Session complexity → include `session-handoff`. When in doubt on a domain skill, lean toward including it. A skill that fires once and catches a problem earns its place.

**Prompt templates:** Read `future-reference/prompt-catalog/CATALOG.md`. Select templates for any repeating prompt patterns in the project. Prompt templates are not required for every project — only include them when there's a recurring prompt structure that benefits from a standardized starting point.

**Sequential protocol ordering:** For multi-agent projects, define the phase sequence explicitly in `AGENTS.md`. Which agent category goes first? What does it produce? What does the next category receive? The ordering is fixed so that agents don't need to negotiate sequence; the role selection within each phase is emergent — agents self-select from the catalog based on what predecessors have already produced and what's still needed.

**Hook configuration:** Review `future-reference/skills-catalog/production/hooks-reference.md` for relevant automation hooks. Pre-commit validation, post-file-creation catalog checks, post-edit verification — select hooks that reduce variance without adding overhead. A hook that fires on every file write is useful; a hook that runs a full test suite on every save is annoying.

**Gate:** All selected catalog entries have CATALOG.md entries (catalog-first verified — if a capability doesn't have a catalog entry, it doesn't belong in the scaffold). Sequential ordering documented in AGENTS.md. Hook configurations written to `.claude/settings.json`.

---

## Phase 4: Scaffold Output

Phase 4 writes the project structure to disk. The scaffold is not a starting point that will be cleaned up later — it is a production-grade foundation that reflects all decisions made in Phases 0-3. Every file has a purpose. No file is boilerplate.

**Required files for every project:**

```
[project-root]/
├── CLAUDE.md           ← project-specific, KB-grounded operational rules
│                           Must include: Session Start Protocol + Development Workflow + Required Rules
├── AGENTS.md           ← mission + Role Directory (all projects) + Sequential Protocol Ordering (multi-agent only)
├── SOUL.md             ← from SOUL-TEMPLATE.md + Phase 2 character decisions
├── README.md           ← project overview, quick start, how to use the scaffold
├── .gitignore
├── .claude/
│   ├── agents/         ← run cp for each agent selected in Phase 3; verify with ls after
│   ├── skills/         ← run cp -r for each skill selected in Phase 3; verify with ls after
│   └── settings.json   ← hook configurations
├── docs/
│   ├── kb-references.md    ← POINTERS ONLY (file + line ranges, never content copies)
│   └── plans/
│       ├── design.md       ← all Phase 2 decisions with rationale
│       └── implementation.md ← ordered build plan grounded in KB
└── .sessions/
    ├── [project-name]/     ← local workspace, never committed to git
    └── handoffs/           ← session continuity logs, never committed; write a handoff here before ending each session; most recent non-superseded file is source of truth
```

**For AI projects, additionally:**
```
└── docs/
    └── prompts/        ← system prompts designed in Phase 2, versioned
```

**File-by-file rationale:**

`CLAUDE.md` is the project's operating contract for Claude — it sets the constraints, the conventions, and the workflow protocol. Without it, Claude starts each session with default behavior. With it, Claude starts each session with project-specific constraints and a complete operational context. Every Cook-generated CLAUDE.md must contain four sections:

**(1) Session Start Protocol** — a numbered, ordered list every session executes before any work. Required steps, in order: (a) Read SOUL.md — load character before anything else. (b) Read AGENTS.md — load operational context and role directory. (c) Check `.sessions/handoffs/` for the most recent non-superseded handoff — read it to load phase state. (d) Glob `.claude/agents/*` — discover the actual agent fleet; the directory is authoritative and overrides any stale documentation. (e) Run `git log --oneline -5` — catch agent/config changes since last handoff (a commit like "add agent definitions" is a signal to read new files). (f) If handoff specifies "Next Session Invocations," invoke those skills via the Skill tool before proceeding; if no handoff exists, consult the Development Workflow section and start from the beginning. (g) Throughout this session — not just at startup — before invoking any skill, invoke it via the Skill tool to read its current content. Do not rely on memory of what a skill specifies.

**(2) Development Workflow section** — the project-specific skill chain written by Cook in Phase 4 from Phase 3 selections. Must distinguish: "First session (implementation plan already exists at docs/plans/implementation.md): skip to Execute" from "Per-feature / new work: Brainstorm → Plan → Execute → Review → Commit → Handoff." Must include: "When executing-plans or subagent-driven-development dispatches work, route tasks using the Role Directory in AGENTS.md. The implementation plan's Agent: annotations are authoritative for per-task routing."

**(3) Required Rules section** — must contain: "After completing any meaningful chunk of work, read back what you produced against the acceptance criteria, check for rough edges and missing requirements, and fix any issues before reporting done. Self-review happens per artifact, not only at the final gate." AND: "Before ending any session — whether complete or interrupted — invoke the `session-handoff` skill. This is not optional."

**(4) Technical Constraint Blocks** — two blocks copied verbatim from `LEARNING/FOUNDATIONS/operator-oversight/operator-oversight.md` (the "CLAUDE.md Constraint Blocks" section). These are the canonical source; do not paraphrase or abbreviate:
- `## Networking Constraints` — covers HTTP client instantiation, three-layer timeouts, retry rules with backoff+jitter, idempotency keys, transport selection (REST/SSE/WebSocket/webhook), status code semantics, and circuit breakers.
- `## Code Quality Constraints` — covers data structure selection (dict/set vs. list), the no-I/O-inside-loops rule, single-responsibility functions, destructive operation guards, no global state, configuration externalization, and error handling completeness.

Both blocks are enforced by default on all generation. Operators may override specific rules only when the project's stack or constraints justify deviation — document any override in `docs/plans/design.md` with the reason.

`AGENTS.md` defines the mission in one sentence, the Sequential Protocol Ordering for multi-agent work, and a Role Directory for task-level dispatch during execution. These are distinct sections with distinct purposes.

The **Sequential Protocol Ordering** section describes phase sequencing — which agent category goes first, what it produces, what the next category receives. Agents self-select within each phase based on what predecessors produced. This is NOT pre-assignment of specific tasks to specific agents — that is what the Role Directory handles.

The **Role Directory** is a routing table for task-level dispatch. When executing-plans spawns a subagent for a specific task, the Role Directory maps task type to agent. Populated in Phase 4 from Phase 3 selections. Each row: agent filename (without .md), model tier, project-specific trigger condition. The implementation plan's `**Agent:**` annotations take precedence over this table for individual tasks — the Role Directory is the reference and fallback.

Both sections belong in every project with agents in `.claude/agents/`. The Role Directory is not exclusive to multi-agent topologies — a single-session project with a code-reviewer agent still benefits from documenting when to use it. If `.claude/agents/` contains files not in the Role Directory, they must be read and added before execution begins.

`SOUL.md` encodes the functional personality. It must be loaded before any work begins — hence step (a) of the Session Start Protocol. Character without a loading mechanism is decorative.

`docs/kb-references.md` is a pointer file, not a content file. It says which KB sections are load-bearing for this project and why. It never copies text from the KB. The KB is the single source of truth; references point to it.

`docs/plans/design.md` captures every decision from Phases 2-3 with rationale. It answers: why this model tier, why this topology, why these agents, why these hooks. Without rationale, decisions look arbitrary when revisited.

`docs/plans/implementation.md` must annotate every task with the agent from AGENTS.md Role Directory that should execute it. Format: `**Agent: [agent-name]**` on the line after the task description. Tasks with no matching agent are noted as "inline — no agent delegation." This annotation is what executing-plans reads to dispatch the correct `.claude/agents/` definition. Without it, subagent dispatch operates without the fleet, and the Role Directory exists only as documentation.

**Done-gate checklist — verify before reporting scaffold complete:**
- [ ] All required files present and non-empty
- [ ] `.claude/agents/` contains at least one agent definition file — run `ls .claude/agents/` to confirm; directory existing is not sufficient
- [ ] `.claude/skills/` contains at least one skill file — run `ls .claude/skills/` to confirm; directory existing is not sufficient
- [ ] `docs/kb-references.md` has entries for every load-bearing KB section from Phase 0
- [ ] `docs/plans/design.md` captures all Four Pillars, topology, error contract, and character design
- [ ] `SOUL.md` reflects Phase 2 character decisions, not just the default template text
- [ ] Eval criteria defined in `docs/plans/design.md` before any implementation code exists
- [ ] Security threat model started in `docs/plans/design.md`
- [ ] `CLAUDE.md` has `## Session Start Protocol` section — do not duplicate its steps as individual rules elsewhere in the file
- [ ] `CLAUDE.md` has `## Development Workflow` section populated from actual Phase 3 skill selections — not generic template text, specific to this project's confirmed skills
- [ ] `CLAUDE.md` has `## Networking Constraints` block (copied from operator-oversight.md) — not paraphrased
- [ ] `CLAUDE.md` has `## Code Quality Constraints` block (copied from operator-oversight.md) — not paraphrased
- [ ] `AGENTS.md` has `## Role Directory` section populated with all agents in `.claude/agents/` — trigger conditions are project-specific, not generic catalog descriptions
- [ ] `docs/plans/implementation.md` tasks are annotated with `**Agent:**` from the Role Directory

---

## Phase 5: Eval + Security Baseline

Evaluation and security are not afterthoughts. They are designed before the first line of production code, because designing them after the code exists means designing them around what was built rather than around what should have been built.

**What goes wrong if you skip this:** The system ships and nobody can answer the question "does it work?" without gut feel. Security vulnerabilities go undiscovered until they're exploited. The first time a quality regression is caught is when a user reports it, not when a test catches it.

**Eval-driven development (EDD)** (source: `LEARNING/PRODUCTION/evaluation/evaluation.md`):

Define success metrics before writing any implementation code. For each metric: what it measures, how it's computed, baseline (current state, even if that baseline is "we have no data"), and target (where it needs to be for the project to be considered successful). Fuzzy metrics are not metrics — "Quality" is not a metric. "Faithfulness score ≥ 0.85 measured by LLM-as-judge on a 50-example held-out test set" is a metric.

For AI systems, the eval setup includes at minimum: an offline test set with gold labels, an eval method matched to the output type (exact match for structured output; LLM-as-judge for open-ended generation; human eval for calibration), and a regression threshold that triggers review when crossed. Without this setup, prompt changes are made by intuition, and regressions are discovered in production.

LLM-as-judge design notes: position bias mitigation is not optional. Positional order of compared outputs affects judge scores. Use reference-based evaluation where possible. The judge prompt should be evaluated against human judgments before being trusted.

**Threat model** (source: `LEARNING/PRODUCTION/ai-security/ai-security.md` lines 63-145):

AI and agentic systems have a different attack surface from traditional software. The most common agent-specific threats: prompt injection via tool results (an external document contains instructions that override the agent's system prompt), context poisoning (malicious content in retrieved documents shapes model behavior), goal hijacking (an attacker provides input that redirects the agent's goal), and excessive agency (the agent takes irreversible actions without appropriate HITL gates).

Write a first-pass threat model that covers: what external inputs reach the model (each is a potential injection vector), what actions the agent can take (each irreversible action needs a HITL gate), what data the model can access (each is a potential exfiltration vector), and what trust levels are assigned to different input sources.

This threat model does not need to be exhaustive at project start — it needs to exist so that security is a designed property, not a retrofit.

**HTTP client secret hygiene** (source: `LEARNING/PRODUCTION/ai-security/ai-security.md` §13; invocable skill: `future-reference/skills-catalog/production/http-client-hygiene/`):

Any project that calls a third-party API with a secret — especially one that accepts the key as a `?api_key=` query parameter (Hunter, Google Maps/Places legacy endpoints, SendGrid v2, most smaller SaaS APIs) — must run the four-point HTTP client hygiene checklist before shipping. The failure mode is silent: a key leaks through `requests.HTTPError.__str__()` into log files, stderr, and crash reports on every non-2xx response or network blip, because the library embeds the full URL in the exception message and Python's default traceback printer walks `__cause__` to print it. The checklist: (1) never interpolate the exception object into a log message — log only `type(e).__name__` and the sanitized context; (2) re-raise `HTTPError` with a scrubbed message using `from None` (not `from e`) to suppress `__cause__` printing; (3) prefer header auth over query-param auth when the API supports it; (4) write a regression test that asserts the secret does not appear in log capture or the raised exception's `str()`. Invoke the `http-client-hygiene` skill when writing or reviewing any authenticated HTTP client call — the skill pulls the checklist, scrubbed client skeleton, and test patterns into context together. Projects scaffolded by /cook that touch external APIs inherit this as a mandatory Phase 5 touchpoint, not an optional hardening.

**Observability signals:** What will you monitor in production? The minimum viable observability stack for AI systems: token usage per request (cost visibility), error rate and error types (reliability), response latency at p50/p95 (performance), and user correction rate or negative feedback rate (quality signal). Add domain-specific signals relevant to the project's success metrics.

**Audit stopping rule** (source: `future-reference/skills-catalog/workflow/project-done-definition/`):

Audits find problems; they do not measure completion. Default cadence is 2–3 rounds of 3 non-overlapping subagents, each round covering different angles from the coverage matrix (security, correctness, failure modes, performance/cost, operator UX, ship artifact, documentation, threat model, eval drift). Findings volume should decay ~30% per round. Stop when a round surfaces zero P0 and ≤3 P1 items — past that ceiling, you pay 10× the token cost for 10% more coverage and the severity curve flattens into polish territory. Ship with a known-issues list rather than audit-loop into perfectionism; one real user interaction finds more than ten audits. Invoke the `project-done-definition` skill when the question "is this done?" surfaces or after 2+ audit rounds when wondering whether to run another — the skill pulls the stopping signals, angle coverage matrix, and audit-exhaustion red flags (4th+ round "for safety," findings ≤2% of surface area, audit spend exceeding feature-work spend) into context together.

**Harness optimization path** (AI projects only, source: `agentic-engineering.md` lines 842-1746):

After a baseline is established and the system has processed real production traffic, the Meta-Harness pattern provides a systematic path for accuracy improvement. The optimal time to run it: after the first 50-100 production interactions, when you have real data about where the system struggles. Running it on synthetic data before production doesn't tell you what the real distribution of failures looks like.

The Meta-Harness takes the current prompt, context architecture, and tool configuration and systematically tests variations against the eval suite. It identifies which dimensions of the harness drive variance, then optimizes those dimensions while holding others fixed. This is expensive — run it when the baseline data justifies the cost, not as a first pass.

**Builds log reminder:** When this project ships — when it produces real value for real users — update `builds-log.md` with what was built, the key technical decisions, what worked as expected, and what failed or required revision. The builds log is the institutional memory of real-world outcomes, not theoretical best practices. Future projects benefit from it only if it's updated honestly, including the failures.

---

## Prohibited Patterns

The following are failure modes that appear when phases are skipped or rushed. Each one is listed here to be recognized and stopped — not as suggestions, not as acceptable trade-offs in some circumstances, but as things that must not happen in a properly executed scaffold.

**Do not describe the solution before the problem.** When a user says "I want to build X" where X is a tool, not a problem statement, stop and ask what problem makes them want to build X. A scaffold built around a preconceived solution that hasn't been validated against the actual problem will require rework. This is not a matter of style — it is a structural flaw that propagates through every downstream decision.

**Do not begin implementation without a written spec.** If the spec exists only in someone's head, it is not a spec — it is a set of assumptions that different people have formed differently. The test: can a developer implement the feature correctly without asking any clarifying questions? If the answer is no, the spec is not done and implementation must not start.

**Do not put everything in context because it might be relevant.** Context components must be explicitly justified. Overcrowded context degrades model performance predictably and measurably. Every item in context should earn its place. Items without justification belong out of context.

**Do not write evals after the fact.** Evals written after implementation to verify what was built measure what was built, not what should have been built. Evals belong before implementation. They define success. Writing them post-hoc is a different activity with a different and weaker outcome.

**Do not create agent or skill files before their CATALOG.md entry.** The catalog-first convention exists specifically to prevent a stale catalog. A file that exists without a catalog entry is invisible to agents traversing the catalog. Catalog entry first, file second — no exceptions.

**Do not copy SOUL-TEMPLATE.md without customizing the [PROJECT CHARACTER] section.** A SOUL.md that is identical to the template provides no project-specific behavioral specification. Character design is the act of deciding what this agent is — what it optimizes for, who it serves, what kind of voice it has. Copying the template without customizing this section produces a document that exists but does nothing.

---

## Maintenance Contract

This document stays accurate when people update the right layer for each type of change. Updating the wrong layer — putting KB content into this hub, or putting workflow decisions into KB docs — breaks the separation that makes the system maintainable.

| What changes | What to update |
|---|---|
| New KB research captured | KB doc + `KB-INDEX.md` + review this doc for relevant phase pointers |
| New agent added | `agent-catalog/CATALOG.md` first (catalog-first), then agent file |
| New skill added | `skills-catalog/CATALOG.md` first, then skill file |
| New prompt template added | `prompt-catalog/CATALOG.md` first, then template |
| New playbook added | `playbooks/README.md` + `KB-INDEX.md` |
| Workflow phase logic changes | This document + `/cook` skill |
| Scaffold output structure changes | `/cook` skill + the design doc |
| A phase needs to route to a new KB section | Update the phase pointer in this document |
| Agent added to `.claude/agents/` mid-project | AGENTS.md Role Directory + re-annotate affected `docs/plans/implementation.md` tasks |

The table above is duplicated in `CLAUDE.md` alongside the existing KB maintenance rules. When in doubt about which layer to update, consult the design doc at `docs/plans/2026-04-12-magnum-opus-design.md` which describes the rationale for the three-layer architecture.
