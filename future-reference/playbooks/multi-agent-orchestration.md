# Multi-Agent Orchestration

**Adapted from [everything-claude-code](https://github.com/affaan-m/everything-claude-code) by Affaan Madooei**

> The 13-agent architecture: how to organize, deploy, and coordinate specialized agents to handle different responsibilities in a development workflow. From single agents to agent swarms.

---

## Table of Contents

1. [The 13-Agent Model](#the-13-agent-model)
2. [Responsibility-Based Organization](#responsibility-based-organization)
3. [When to Invoke Each Agent](#when-to-invoke-each-agent)
4. [Parallel Execution Patterns](#parallel-execution-patterns)
5. [Context Isolation & Handoff](#context-isolation--handoff)
6. [Artifact Specification](#artifact-specification)
7. [Failure Recovery](#failure-recovery)
8. [System-Level Failure Recovery](#system-level-failure-recovery)
9. [Scaling from 1 Agent to 13](#scaling-from-1-agent-to-13)

---

## The 13-Agent Model

The everything-claude-code architecture deploys 13 specialized agents, each with a single responsibility. This differs from the "one big agent that does everything" model because:

- **Specialization** — Each agent is expert-level at one task (code review, testing, security)
- **Parallelism** — Multiple agents work simultaneously on independent tasks
- **Failure isolation** — One agent failing doesn't block others
- **Reusability** — Each agent's prompt evolves independently based on success/failure

### The 13 Agents & Their Roles

| Agent | Responsibility | Triggers | Model | Typical Cost |
|---|---|---|---|---|
| **Planner** | Break task into steps, estimate scope | User says "do X" | Sonnet | $0.005 |
| **Architect** | Design system, review architecture | "Large feature" or "refactor" | Opus | $0.010 |
| **TDD Guide** | Write failing tests, minimal implementation | "Implement feature per spec" | Sonnet | $0.008 |
| **Code Reviewer** | Review code for style, security, performance | After implementation | Sonnet | $0.007 |
| **Security Reviewer** | Deep security audit, attack surface analysis | High-risk features | Opus | $0.012 |
| **Debugger** | Diagnose failures, root cause analysis | Tests fail or runtime errors | Sonnet | $0.006 |
| **Linter** | Check style, formatting, compliance | Before commit | Haiku | $0.001 |
| **Test Generator** | Create comprehensive test cases | "Missing coverage" | Sonnet | $0.006 |
| **Documentation** | Write docs, API references, guides | Feature complete | Sonnet | $0.006 |
| **Optimizer** | Performance tuning, refactoring | "Too slow" or "simplify" | Sonnet | $0.007 |
| **Deployment** | Setup CI/CD, environment config | "Deploy to prod" | Sonnet | $0.005 |
| **Monitor** | Setup observability, alerts, dashboards | In production | Sonnet | $0.005 |
| **Learner** | Extract patterns, update CLAUDE.md | At session end | Haiku | $0.001 |

---

## Responsibility-Based Organization

Unlike capability-based organization ("use Opus for hard things, Haiku for easy things"), responsibility-based organization assigns agents by **what they're accountable for**.

### Why Responsibility-Based Matters

**Capability-based:** "Use bigger models for harder tasks"
- Problem: Definition of "hard" changes per task
- Result: Inconsistent model selection, agents fighting over same problem

**Responsibility-based:** "This agent is responsible for security, this one for performance"
- Clear ownership: each agent has a domain
- Parallel execution: multiple agents can work simultaneously without stepping on each other
- Learning: each agent's prompt evolves based on successes in that specific domain

### Mapping Agents to Responsibilities

```
Core Development Loop:
├─ Planner (Plan phase)
├─ Architect (Design phase)
├─ TDD Guide (Implement phase)
├─ Code Reviewer (Review phase)
│  ├─ Checks correctness, style
│  └─ Flags for Security Reviewer if needed
├─ Security Reviewer (Security phase)
│  └─ Deep audit if Code Reviewer flagged
└─ Debugger (Fix phase if tests fail)

Supporting Loop (Parallel):
├─ Test Generator (Expand test coverage)
├─ Optimizer (Performance improvements)
└─ Learner (Extract patterns for next time)

Deployment:
├─ Linter (Final style check)
├─ Deployment Agent (CI/CD setup)
└─ Monitor (Observability setup)

Post-Deploy:
└─ Learner (Update CLAUDE.md with lessons)
```

---

## When to Invoke Each Agent

**Proactive Triggers** (automatic, no user request needed):

```
Planner:
├─ User submits task description
├─ Task description > 1 paragraph
└─ No existing plan document

Code Reviewer:
├─ New code written
├─ Before merging to main
└─ Automatically triggered post-implementation

Security Reviewer:
├─ Code Reviewer flags security concern
├─ Feature touches user data, auth, or payments
├─ Automatic for high-risk domains

Debugger:
├─ Test suite fails
├─ Runtime error in logs
└─ Automatic on error detection
```

**Reactive Triggers** (user explicitly requests):

```
"Add comprehensive tests" → Test Generator
"This is too slow" → Optimizer
"Review this code" → Code Reviewer
"Design the system" → Architect
"I need documentation" → Documentation
```

---

## Harness Coordination Across Agents

**What is an agent's harness?** The prompt structure, tool description format, context formatting, and feedback loop design that surrounds each agent. In a 13-agent system, each agent has its own harness — and how well those harnesses align with each other (and with inter-agent handoffs) significantly affects system performance.

### The Harness Coordination Problem

In a naive 13-agent setup, each agent's prompt was designed independently:
- Planner expects task descriptions in natural language
- Architect expects plan.md with specific sections
- TDD Guide expects architecture.md with specific format
- Code Reviewer expects code + standards document

If the Planner's output format doesn't match what the Architect expects, the Architect has to work harder to parse or reinterpret. This creates friction, context bloat, and failures.

**Coordinated harnesses** align agent inputs and outputs so each agent produces exactly what the next agent expects.

### Coordinating Harness Patterns Across Agents

**Pattern 1: Standardize Artifact Schemas**

Define what each artifact (plan, architecture, code, review) should contain. Each agent's prompt includes the schema it should follow:

```
Planner prompt includes:
  "Output plan as JSON with schema:
  {
    'goals': [...],
    'phases': [...],
    'assumptions': [...],
    'risks': [...]
  }"

Architect prompt includes:
  "Input will be plan.json matching this schema. [...] 
   Output architecture.json with schema:
  {
    'components': [...],
    'interfaces': [...],
    'rationale': {...}
  }"
```

When Architect receives Planner's output, it's already in the expected format. No re-interpretation needed.

**Pattern 2: Optimize the Handoff Harness** (Orchestrator-Specific)

The orchestrator's prompt is the "coordinating harness" — it decides which agent to invoke, what context to pass, how to handle failures. Optimize this separately from individual agents.

Orchestrator optimization differs from individual agent optimization: focus on reducing decision latency (how fast it picks the right agent) and context bloat (how much context it loads before delegating). See: [`agentic-engineering/agentic-engineering.md` lines 842–1076](../LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md) (Automated Harness Optimization) for the systematic approach.

**Pattern 3: Agent Specialization via Harness, Not Prompts**

Rather than writing 13 different prompts from scratch, define:
1. **Base harness:** Common structure (goal, input, output format, tool list)
2. **Specialization:** Domain-specific instructions injected into slots

Example:
```
Base harness:
  "You are a {ROLE}.
   Input: {INPUT_SCHEMA}
   Output: {OUTPUT_SCHEMA}
   Tools: {TOOL_LIST}
   Key principles: {PRINCIPLES}"

Planner harness:
  Role: Task Planner
  Principles: ["Break into discrete phases", "Identify blockers early"]

Code Reviewer harness:
  Role: Code Quality Expert
  Principles: ["Security over elegance", "Catch common mistakes"]
```

This approach makes harnesses maintainable — you update the base harness once, all agents benefit.

### When to Coordinate vs. When to Let Agents Diverge

**Coordinate these harnesses:**
- **Inter-agent handoff schemas** — must match so data flows cleanly
- **Tool descriptions** — same tool should be described consistently across agents
- **Context format** — if agents share context, format should be consistent

**Let these diverge:**
- **Reasoning style** — Code Reviewer's thinking process differs from Architect's
- **Output verbosity** — Linter produces brief output; Architect produces detailed design docs
- **Error handling** — Debugger has special "what went wrong" prompts; Test Generator doesn't

### Optimizing Multi-Agent Harnesses (High-Traffic Systems)

Once your 13-agent system is stable and handling significant volume (10k+ invocations/week):

1. **Profile each agent separately:** Measure accuracy, latency, token usage per agent
2. **Identify bottleneck agents:** Which agent's harness causes most downstream failures?
3. **Optimize bottleneck harnesses first:** Run systematic optimization on the highest-impact agents (typically Planner, Architect, Code Reviewer)
4. **Validate coordination:** After optimizing one agent's harness, test that outputs still match downstream agents' expected input format

Expected result: 8–15% accuracy improvement on individual agents, 5–10% cost reduction for the full orchestrated system (from fewer token retries and cleaner handoffs).

---

## Parallel Execution Patterns

### Single-Message Parallelism (Most Efficient)

**KEY PRINCIPLE:** All agents you want to run in parallel **must be invoked in a single message**. Otherwise they run sequentially.

**Example:** After implementation, invoke Code Reviewer + Security Reviewer + Test Generator + Optimizer in one message:

```
[Orchestrator sends single message with 4 sub-agent invocations]
├─ Code Reviewer reads code, generates review
├─ Security Reviewer audits in parallel
├─ Test Generator creates test cases in parallel
└─ Optimizer identifies performance opportunities in parallel

[All finish ~simultaneously, e.g., 60 seconds total]
[Instead of sequential: 4 × 60 = 240 seconds]
```

Timing: 4 agents in parallel = ~4 minutes. Sequential = ~16 minutes. **4× speedup from one architectural decision** *(illustrative timing from everything-claude-code parallel execution pattern).*

### Dependency-Based Sequencing

Some agents must wait for others:

```
Sequential (blocked):
Planner → Architect → TDD Guide → Code Reviewer → Debugger
[Each waits for previous]

Parallel with Dependencies:
Planner
├─ (blocks on) → Architect
│              ├─ (blocks on) → TDD Guide
│                             ├─ (parallel) Code Reviewer
│                             ├─ (parallel) Test Generator
│                             └─ (parallel) Optimizer
└─ (parallel) Documentation can start anytime
```

Architect must wait for Plan. TDD must wait for Architect. But Code Review, Testing, and Optimization can happen in parallel.

---

## Context Isolation & Handoff

Each agent sees **only what it needs** to avoid context bloat.

### What Each Agent Receives

```
Planner receives:
├─ Task description
└─ Current project state

Architect receives:
├─ Task description
├─ Plan document
└─ Existing codebase architecture

TDD Guide receives:
├─ Plan document
├─ Existing codebase structure
└─ Existing test patterns

Code Reviewer receives:
├─ Plan document (to verify compliance)
├─ New code (what changed)
└─ Existing style/standards
```

**NOT:**
- Entire conversation history
- All previous commits
- Unrelated code files
- Debugging logs

### Handoff via Artifacts

Agents communicate via files (the "source of truth"), not via context:

```
Planner writes: plan.md

Architect reads: plan.md
Architect writes: architecture.md

TDD Guide reads: plan.md + architecture.md
TDD Guide writes: test file + implementation

Code Reviewer reads: plan.md + new code
Code Reviewer writes: review-comments.md

Debugger reads: review-comments.md + test failures
Debugger writes: fixes
```

Each agent produces a clear artifact that becomes input for the next. No context explosion.

### Preventing Context Contamination in Parallel Execution

When invoking multiple agents in parallel (e.g., Code Reviewer + Security Reviewer + Test Generator in one message), each agent's context must remain isolated to preserve steering accuracy. The orchestrator should:

1. **Keep artifact handoffs explicit** — agents communicate via files, not through accumulated context clutter.
2. **Use lightweight registries** — maintain ≤200-token summaries of each agent's state, not full context.
3. **Serialize steering requests** — if multiple agents request decision support (agent introspection, debugging), isolate each agent's context during steering rather than serving multiple agents' requests from shared context.

This is especially critical as agent count scales: contamination effects compound with N. Empirical evidence (200-trial study at 4 decision-density levels): baseline shared-context approach achieves 0–14% wrong-agent contamination at N=3–5; isolated-context approach (with lightweight registries + per-agent focus during steering) eliminates contamination entirely, improving steering accuracy from ~40% to ~95%. [2604.07911v1 — Dynamic Attentional Context Scoping, 2026]

---

## Artifact Specification

The handoff diagram above names files (plan.md, review-comments.md) but doesn't specify what goes inside them. Without a consistent structure, agents develop implicit contracts that break silently when one agent's output format changes.

### Artifact Schema

Every inter-agent handoff should be a typed, versioned artifact:

```json
{
  "artifact_type": "research_summary",
  "version": "1.0",
  "producing_agent": "researcher",
  "timestamp": "2025-03-21T14:30:00Z",
  "status": "complete",
  "content": { ... },
  "confidence": "high",
  "caveats": ["Found no results for X, assumed Y"],
  "next_agent": "writer"
}
```

**Status values:** `complete` | `partial` | `failed`
**Confidence values:** `high` | `medium` | `low`

### Why This Schema Matters

**Without explicit types:** The Planner writes `plan.md` in one format in March. You update the Planner prompt in April. The Architect's prompt still expects the old format. The failure is silent — the Architect reads what it can, proceeds with an incomplete plan, and you get bad output with no error. Debugging takes hours.

**With explicit types:** The Architect checks `artifact_type` and `version` before reading. Format mismatch surfaces immediately, before any downstream damage.

### Partial Artifacts

When an agent cannot fully complete its task — a researcher hits a rate limit, a code reviewer runs out of context — it should produce a partial artifact rather than failing outright:

```json
{
  "artifact_type": "code_review",
  "status": "partial",
  "content": { "reviewed_files": ["auth.py", "models.py"], "skipped_files": ["api.py"] },
  "caveats": ["api.py not reviewed — context limit reached"],
  "next_agent": "orchestrator"
}
```

The receiving agent (or orchestrator) then decides: is the partial output sufficient to proceed? Does it need to retry just the skipped portion? Partial artifacts prevent the all-or-nothing failure mode where one agent's incomplete run kills the whole pipeline.

### Artifact Storage

| Pipeline duration | Steps | Recommended storage |
|---|---|---|
| < 30 minutes | < 5 | In-memory passing (dict/object) |
| 30 min – 2 hours | 5–10 | JSON files on disk, keyed by run ID |
| > 2 hours or restartable | Any | Redis or SQLite, keyed by `run_id + artifact_type` |

The key insight: in-memory artifacts vanish if the orchestrator crashes. For any pipeline that matters, write artifacts to disk before invoking the next agent. Recovery from a crash then means reading the last written artifact and resuming from that stage.

---

## Failure Recovery

### Agent Failure Patterns

**Planner fails:**
- Symptom: Plan is vague or incomplete
- Recovery: Re-invoke with clearer task description or examples
- Escalation: If re-plan fails, ask human for clarification

**TDD Guide fails:**
- Symptom: Tests don't pass or implementation doesn't match spec
- Recovery: Invoke Debugger to diagnose
- Escalation: If Debugger can't fix in 2 iterations, escalate to human

**Code Reviewer fails:**
- Symptom: Review misses obvious issues (validated by human)
- Recovery: Update Code Reviewer prompt based on what it missed
- Escalation: For complex domains, also invoke Security Reviewer

**Security Reviewer fails:**
- Symptom: Security issue slips through
- Recovery: Document the issue as a new security test case
- Escalation: Escalate to security expert for review

### Hard Limits

```
Each phase can be attempted max N times:
├─ Planning: 2 iterations (if 2nd fails, ask human)
├─ Implementation: 3 iterations (Debugger helps on 2nd/3rd)
├─ Code Review: 2 iterations (if needed revisions fail, escalate)
└─ Security Review: 1 iteration (no retry; escalate if concerns)
```

**Rationale:** Prevents infinite loops; escalates early when agent capacity is exhausted.

---

## System-Level Failure Recovery

The section above addresses what to do when an individual agent fails. This section addresses what happens when failures interact — when agent A's failure causes agent B to fail, and agent B's failure causes agent C to fail.

### The Cascading Failure Pattern

```
Agent A (researcher) → fails, returns error
Agent B (writer) → receives error as input, itself fails
Agent C (reviewer) → receives error from B, also fails
Result: entire pipeline down from one root failure
```

This is the most common multi-agent failure mode and the hardest to debug, because the logged failure is Agent C — the last one to fail — not Agent A, which caused everything.

**Prevention:** Each agent must have a defined behavior for receiving error inputs. Acceptable behaviors:
- Produce a partial artifact with `status: "partial"` and a caveat describing the gap
- Escalate to the orchestrator rather than propagating downstream
- Apply a fallback strategy (e.g., if the researcher failed, the writer proceeds with a noted assumption)

What is not acceptable: an agent that receives an error artifact and simply re-emits an error without attempting any of the above. That agent is not recovering — it's just relaying failure.

### Failure Isolation in Parallel Pipelines

Parallel execution creates a natural isolation boundary. If three agents are running in parallel and one fails, the other two should complete regardless:

```
Orchestrator dispatches parallel:
├─ Agent A (task 1) → fails
├─ Agent B (task 2) → completes ✓
└─ Agent C (task 3) → completes ✓

Synthesis step receives:
├─ Agent A result: { status: "failed" }
├─ Agent B result: { status: "complete", content: ... }
└─ Agent C result: { status: "complete", content: ... }

Synthesis produces: partial synthesis, notes gap from Agent A
```

The synthesis step should not halt because one of three inputs failed. It should produce a partial synthesis with an explicit caveat and let the orchestrator decide whether to retry Agent A, flag for human review, or accept the degraded output.

**Design rule:** Failure scope should be bounded to the failing agent and the minimal downstream steps that strictly require its output. Parallel peers should be unaffected.

### System-Level Circuit Breaker

Individual retry limits prevent loops on a per-agent basis. The circuit breaker operates at the pipeline level: if too many agents are failing in a single run, halt the entire pipeline rather than letting a degraded system run indefinitely producing garbage.

**Rule of thumb:** Halt and escalate to a human if more than 30% of agents in the current pipeline have reached their failure limit.

For the 13-agent model: halt if 4+ agents fail. For a 3-agent pipeline: halt if 1 agent fails (any failure in a 3-agent system is a 33% failure rate).

What "halt" means in practice:
1. Stop dispatching new agents
2. Write a system-level failure artifact capturing the state (see post-incident structure below)
3. Notify a human — do not silently exit

The reason for the explicit threshold rather than "halt on any failure": some pipelines are designed to continue despite partial failures (a research pipeline that handles a missing source gracefully). The 30% threshold is a conservative backstop for those cases.

### Post-Incident Analysis Structure

After any system-level failure (circuit breaker triggered, or a cascade that produced garbage output), capture:

1. **Which agent failed first** — not which agent was last to fail
2. **What input it received** — the exact artifact passed to it
3. **System state at failure time** — which other agents were running, what they had produced
4. **Transient or persistent?** — did the failure reproduce on retry? (Transient = infra issue; persistent = prompt/logic issue)
5. **Was the cascade preventable?** — which downstream agents received the error artifact and propagated it instead of isolating?

Without this structure, multi-agent systems accumulate invisible failure modes. The same root cause recurs because the symptom (Agent C's failure) gets fixed and the root cause (Agent A's behavior on bad input) doesn't.

Store post-incident artifacts alongside the run's other artifacts. Over time, they become a corpus for improving agent failure behavior.

---

## Scaling from 1 Agent to 13

The 13-agent model is a destination. Most teams that try to adopt it all at once fail — not because the architecture is wrong, but because you can't debug 13 interacting agents if you've never debugged 3. The right path is staged.

### Stage 1: Single Agent

```
[User] → [Multipurpose Agent] → [Output]
```

One agent does everything: planning, execution, review. Cost is low, orchestration complexity is zero.

**The actual purpose of Stage 1 is not to ship with it.** It's to establish a baseline and surface failures. Run a representative sample of tasks through the single agent and catalog where it consistently fails. Typical patterns:
- Plans that are too vague to execute reliably
- Code that passes its own review but fails human review
- Outputs that vary widely on the same input

These failure modes are the candidates for specialization. If the agent never fails at a task, don't add an agent for that task.

### Stage 2: Planner + Executor + Reviewer (3–4 Agents)

```
[User] → [Planner] → [Executor] → [Reviewer]
                         ↑
                    [Debugger] (add if execution fails often)
```

Split on the single-agent's most common failure mode: poor planning leading to poor execution. The Planner and Reviewer exist to catch what the Executor misses.

**Gate for advancing:** This configuration should be reliably producing quality output on the task types that failed in Stage 1. If it isn't, the agent specifications are wrong — fix them before adding more agents. Adding agents to a broken Stage 2 just adds complexity to the debugging problem.

**Cost checkpoint:** Measure cost per task at Stage 2. It will be higher than Stage 1. Verify the quality improvement is worth it before going further.

### Stage 3: Domain Specialists (6–8 Agents)

```
[User] → [Planner] → [Architect]
                         ↓
              [Domain Specialists in parallel]
              ├─ TDD Guide
              ├─ Security Reviewer
              └─ (other specialists)
                         ↓
                     [Reviewer]
```

Add specialists for the domains where the Stage 2 Executor most often fails. The Planner and Reviewer remain. The Executor is replaced (or supplemented) by domain-specific agents.

**Test for Stage 3 validity:** Run the same test suite that validated Stage 2. Quality on the specialized domains should improve. Quality on other domains should not decrease. If generalist quality decreases when adding specialists, the specialists are interfering — likely through context contamination or overlapping responsibilities.

**Cost checkpoint:** Domain specialists typically use Sonnet or Opus on tasks where Haiku or Sonnet-mini was sufficient before. Verify that the quality delta justifies the model cost delta.

### Stage 4: Coordination Agents (13+ Agents)

```
[User] → [Planner] → [Router]
                         ↓
              [Specialists] (parallel, Stage 3 agents)
                         ↓
                   [Aggregator]
                         ↓
              [Quality Controller]
                         ↓
                      [Output]
```

Add coordination agents — routers, aggregators, quality controllers — only when Stage 3 agents are demonstrably producing high-quality results and the bottleneck is coordination, not individual agent quality. If your Stage 3 specialists are producing inconsistent output, adding a Quality Controller doesn't fix that — it just adds a layer that will also produce inconsistent output.

Coordination agents are also where system-level failure complexity concentrates. A Router that fails can take down all downstream specialists. A Quality Controller that has an unclear standard will pass bad output inconsistently. These agents need the most careful specification.

**Cost checkpoint:** Coordination agents add token cost (they read all specialist outputs and produce orchestration logic) without directly producing deliverable content. At Stage 4, measure cost per quality unit, not just cost per task.

### Migration Testing Discipline

At each stage transition, run the same test suite that validated the current stage. This is non-negotiable. The most common migration failure pattern: quality looks fine on new tasks added at the new stage, while regressing on the tasks that worked at the previous stage. Without a fixed test suite, this regression is invisible.

A minimal test suite: 10–20 representative tasks that cover the failure modes Stage 1 identified. Run them at each stage. If any task that passed at Stage N fails at Stage N+1, diagnose before advancing.

### Migration Summary

| Stage | Agents | Add when | Gate before advancing |
|---|---|---|---|
| 1 | 1 | Always start here | Catalog failure modes |
| 2 | 3–4 | Stage 1 failures identified | Stage 1 test suite passes reliably |
| 3 | 6–8 | Stage 2 Executor fails in specific domains | Stage 2 test suite passes; cost justified |
| 4 | 13+ | Stage 3 quality is high; bottleneck is coordination | Stage 3 test suite passes; cost justified |

---

## Self-Organizing Multi-Agent Systems (Dochkina 2026)

### When to Use This Pattern

The 13-agent model works well for structured development workflows with **known, fixed responsibilities**. But some problems benefit from a different approach: agents that **discover their own roles dynamically** based on task context, without pre-assignment.

**Use self-organizing when:**
- Task structure is ambiguous (agents should decide what needs doing)
- Task complexity varies widely (self-abstention optimizes for different scales)
- You want emergent specialization rather than pre-designed roles
- Cost matters (voluntary self-abstention at scale reduces token consumption)

**Stick with 13-agent model when:**
- Roles are well-defined and stable
- Parallel execution of fixed responsibilities is your priority
- You need deterministic behavior (debugging is easier with assigned roles)

### The Sequential Protocol: Core Implementation

Instead of assigning roles upfront, use the **Sequential Protocol** (Dochkina 2026, 25,000-task study):

1. **Initialize N identical agents** — no role assignment, only mission statement
   ```python
   agents = [Agent(model=claude, instruction="You are a team member analyzing this task.") for _ in range(N)]
   ```

2. **Run agents in fixed order** — each agent observes completed outputs of predecessors
   ```
   For agent_i in agents:
     completed_work = [outputs from agent_0 to agent_i-1]
     agent_i analyzes: "What role should I play? What's missing?"
     if agent_i.can_add_value(completed_work):
       contribute_output()
     else:
       ABSTAIN  # voluntary, endogenous
   ```

3. **Measure emergence:** Track RSI (role specialization index → 0), abstention rate (8–15% healthy), quality per task

**Why Sequential beats alternatives:**
- **Coordinator (centralized):** One agent's judgment bottleneck → 14% quality loss
- **Shared (fully autonomous):** Agents work blind, duplicate roles → 44% quality loss
- **Sequential (hybrid):** Agents see factual predecessor outputs → optimal information for role decisions

### Deployment Checklist

**Phase 1 — Design (2 hours)**
- [ ] Define mission + values (NOT role assignments)
- [ ] Choose protocol: Sequential (default) or Coordinator (weak models only)
- [ ] Select model tier: Claude/DeepSeek (L3–L4), GLM-5 (L2–L3), Gemini (L1 only)
- [ ] Design evaluation: 5-criteria LLM-as-judge (accuracy, completeness, coherence, actionability, mission relevance)

**Phase 2 — Implementation (4 hours)**
- [ ] Initialize agents (identical instructions)
- [ ] Implement Sequential loop (see code pattern above)
- [ ] Set up judge model (separate from agents, consistent across runs)
- [ ] Test on small task set (N=8)

**Phase 3 — Scaling (4 hours)**
- [ ] Run 8→16→32→64 agent progression
- [ ] Verify quality stability (p > 0.05, no significant degradation)
- [ ] Monitor self-abstention (target: 8–15%)
- [ ] Measure role diversity (RSI → 0, unique roles increasing)

**Phase 4 — Production (ongoing)**
- [ ] Deploy with multi-model strategy (cheap models L1–L2, strong models L3–L4)
- [ ] Route tasks by complexity level (auto-classifier or manual)
- [ ] Monitor resilience (recovery within 1 iteration after perturbations)
- [ ] Expected cost savings: 40–50% vs. all-strong-model

### Cost Optimization: Multi-Model Routing

Don't use one model for all tasks. Route by task complexity:

| Level | Type | Example | Model Choice | Cost |
|---|---|---|---|---|
| **L1** | Simple, single-domain | API review | Gemini-3-flash | $0.08/MTok |
| **L2** | Cross-domain | Architecture with 2 domains | GLM-5 or DeepSeek | $0.15–0.20/MTok |
| **L3** | Multi-phase | Zero-trust migration | DeepSeek v3.2 (95% quality, 24× cheaper) | $0.20/MTok |
| **L4** | Adversarial | CEO vs. Legal conflicts | Claude Sonnet 4.6 | $4.50/MTok |

**Result:** 40–50% cost reduction, 92–97% quality retention vs. all-Claude.

### Validation Metrics

Monitor three signals that emergence is working:

1. **RSI (Role Specialization Index):** Converges to ~0 (agents invent new roles per task, not recycling)
   - Target: Unique role count at N=64 ≈ 5,000+ across sample tasks
   - Bad: Same agents doing same roles repeatedly (mission unclear)

2. **Self-Abstention Rate:** Agents recognizing when they can't add value
   - Target: 8–15% at N=8–16; 20–45% at N=64–256
   - Low (< 2%): Agents lack self-reflection; switch to Coordinator protocol
   - High (> 70%): Task too simple; reduce agents or increase complexity

3. **Quality Stability at Scale:** No degradation from N=8 to N=64
   - Target: Kruskal-Wallis p > 0.05 (no statistical difference)
   - Cost grows only ~12% while agent count increases 8×

### For Deep Dive

See **agentic-engineering.md, Section "Self-Organizing Multi-Agent Systems: The Endogeneity Paradox"** for:
- Complete system architecture and empirical findings
- Model selection with capability thresholds
- Scaling mechanics to 256 agents
- Failure modes and guardrails
- Resilience to perturbations (agent removal, model substitution)

---

## Implementation Checklist

**Architecture**
- [ ] Start at Stage 1 (single agent) and catalog failure modes before splitting
- [ ] Define agents for your workflow — start with 3–4 (Planner + Executor + Reviewer)
- [ ] Map each agent to a single responsibility, not a capability
- [ ] Determine proactive vs. reactive triggers for each agent
- [ ] Design parallel execution (which agents can work simultaneously without depending on each other?)
- [ ] Define context isolation (what does each agent see — and what does it explicitly not see?)

**Artifact Specification**
- [ ] Define artifact schema: artifact_type, version, producing_agent, status, content, confidence, caveats, next_agent
- [ ] Define status values for your pipeline: complete / partial / failed
- [ ] Decide artifact storage strategy: in-memory (< 30 min), disk JSON, or Redis/SQLite (restartable pipelines)
- [ ] Write artifacts before invoking the next agent (crash recovery depends on this)

**Failure Recovery**
- [ ] Set per-agent retry limits (2–3 max; escalate on exhaustion)
- [ ] Specify each agent's behavior when it receives an error artifact (partial output, escalate, or fallback — never just re-emit the error)
- [ ] Define parallel failure isolation: parallel peers should complete even if one peer fails
- [ ] Set circuit breaker threshold: halt pipeline if > 30% of agents fail in one run
- [ ] Define post-incident capture fields: first failure, input received, system state, transient/persistent, cascade preventability

**Migration**
- [ ] Build a fixed test suite (10–20 tasks) before advancing to Stage 2
- [ ] Run full test suite at each stage transition — no regressions allowed
- [ ] Measure cost per task at each stage; verify quality delta justifies cost delta
- [ ] Do not add coordination agents (routers, aggregators) until individual specialist quality is high

**Iteration**
- [ ] Iterate agent prompts based on specific failures, not vague quality concerns
- [ ] Log post-incident artifacts; review them for recurring root causes

---

## Claude Code Agent Teams: Native Multi-Agent Primitive

> **Status:** Experimental (Claude Code v2.1.32+, disabled by default). Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json.
> **Full reference:** `LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agent-teams.md`

The patterns in this playbook — 13-agent models, responsibility-based organization, self-organizing sequential protocols — are architecture-level frameworks. You build them using whatever tools you have: API calls, subagents, your own orchestration code.

Claude Code Agent Teams is a *native platform primitive* for a specific subset of these patterns. Rather than building your coordination infrastructure (task queue, messaging, state management), you get it pre-built. The tradeoff: less flexibility, much faster time to a working team. Understanding when to reach for the native primitive versus rolling your own matters for every project involving parallel agent work.

### How It Compares to the Frameworks in This Playbook

The **13-agent model** defines roles at the architecture level — Planner, Executor, Reviewer, Communicator, etc. These roles exist whether you implement them via API orchestration code, subagents, or Claude Code Agent Teams. The 13-agent model is the *what*; agent teams is one implementation of the *how*.

**Self-organizing systems (Dochkina protocol)** spawn identical agents that discover their own roles. Agent Teams differs: roles are assigned at spawn time, coordination is explicit, and the lead directs rather than emerging from sequential observation. Self-organizing systems are better for variable-structure problems where the task itself determines what roles are needed. Agent Teams are better for known-structure problems where you can define roles in advance.

**When to use Agent Teams instead of custom orchestration:**
- You want a working multi-agent system in minutes, not days
- Your task decomposes naturally into 3–5 independent workstreams
- You need peer communication (teammates talking to each other), not just result aggregation
- You're prototyping before committing to a full custom orchestration implementation
- The team will run once or episodically, not as a production pipeline

**When to build custom orchestration instead:**
- Production pipeline requiring restartable state (Agent Teams lacks session resumption)
- Team size > 10 (coordination overhead and token costs compound significantly)
- Nested hierarchies needed (Agent Teams has a flat lead/teammate structure; no nested teams)
- Fine-grained per-agent permissions at spawn time required
- Non-Claude Code execution environments (API-only, cloud functions, etc.)

### Deployment Patterns

These are the patterns where Agent Teams consistently add value over other approaches. Each maps to a specific class of problem, not a specific project.

---

**Pattern 1: Parallel Research with Structured Debate**

*Problem class:* Synthesizing a topic where a single researcher will anchor on the first plausible framework they find and stop looking.

*Why teams help:* Multiple independent investigators, each starting cold, surface different framings. The debate phase — where each investigator actively tries to find flaws in the others' conclusions — produces conclusions that survive genuine scrutiny.

```text
Create a research team on [topic]. Spawn three teammates:
- Researcher A: focus on [angle 1] — primary sources and empirical evidence
- Researcher B: focus on [angle 2] — practitioner experience and real-world implementation
- Skeptic: your job is to find where Researchers A and B are wrong or oversimplifying.
  Challenge their conclusions directly.

After each researcher reports findings, have them debate the contradictions.
Synthesize the conclusions that survive the debate.
```

*Best for:* Technical topic synthesis, market analysis, architecture decisions with competing valid approaches, pre-mortem analysis before a major decision.

---

**Pattern 2: Multi-Layer Technical Build**

*Problem class:* A system with independent technical layers (frontend/backend, API/database, service A/service B) where each layer has its own concerns but must ultimately integrate.

*Why teams help:* Sequential layer development forces a single agent to context-switch between domains, losing depth on each. Parallel ownership lets each teammate develop deep context within their layer while a shared task list with dependencies handles integration sequencing.

```text
Create a build team for [system]. Spawn teammates:
- Frontend teammate: owns [UI layer] — components, state management, API contracts
- Backend teammate: owns [API layer] — endpoints, business logic, data validation
- Testing teammate: owns integration tests — starts only after frontend and backend mark
  their tasks complete (set task dependencies accordingly)

Frontend and backend teammates: communicate directly on API contract decisions.
Testing teammate: validate that integration points actually work end-to-end.
```

*Key detail:* Set task dependencies so the testing teammate is blocked until implementation is complete. This encodes the waterfall constraint within an otherwise parallel workflow.

*Best for:* Feature builds with defined layer boundaries, system migrations where each layer migrates independently, API redesigns where client and server need to coordinate.

---

**Pattern 3: Competing Hypotheses Investigation**

*Problem class:* A bug, failure, or unexpected behavior where the root cause is genuinely unclear and sequential investigation would anchor on the first plausible explanation.

*Why teams help:* Each teammate commits to a specific hypothesis before seeing others' work. This forces genuine parallel exploration. The adversarial structure — teammates are explicitly tasked with disproving each other's theories — means the surviving hypothesis has been stress-tested.

```text
[System] is exhibiting [behavior]. The root cause is unclear.

Spawn 4 teammates to investigate competing hypotheses:
- Teammate 1: hypothesis — [theory A]
- Teammate 2: hypothesis — [theory B]
- Teammate 3: hypothesis — [theory C]
- Teammate 4: hypothesis — [theory D]

Rules:
1. Each teammate investigates their assigned hypothesis independently first.
2. After initial investigation, teammates share findings and actively try to disprove
   each other's theories using evidence.
3. Update shared findings.md with evidence for and against each hypothesis.
4. The hypothesis with the strongest surviving evidence after debate is the working theory.
```

*Best for:* Production incidents with unclear root cause, performance regressions where multiple components are candidates, security vulnerability investigations, behavioral drift in ML systems.

---

**Pattern 4: Multi-Domain Analysis**

*Problem class:* A decision or proposal that requires different expert lenses applied simultaneously — not sequentially, because each lens should be applied to the same raw problem, not to the previous lens's conclusions.

*Why teams help:* Sequential analysis taints later perspectives with earlier ones. If the technical review runs first and finds no issues, the security review is unconsciously anchored toward finding no issues either. Parallel domain analysis avoids this contamination.

```text
Analyze [proposal/decision/architecture] from multiple independent domains.
Spawn teammates:
- Technical teammate: feasibility, implementation complexity, architectural risks
- Security teammate: attack surface, data exposure, trust boundaries
- Operational teammate: deployment complexity, monitoring requirements, failure modes
- Strategic teammate: alignment with system goals, opportunity cost, long-term maintenance

Each teammate: review the proposal independently and produce a structured report
(findings, risks, recommendations, confidence level).

Lead: synthesize after all four complete. Flag areas where domain analyses conflict.
```

*Best for:* Architecture review boards, vendor evaluations, policy decisions with multi-stakeholder impact, pre-launch readiness checks.

---

**Pattern 5: Quality-Gated Pipeline**

*Problem class:* A multi-phase workflow where each phase has clear completion criteria, and later phases genuinely depend on earlier phases completing correctly — not just completing.

*Why teams help:* Task dependencies in the shared task list encode phase gates directly. Combined with `TaskCompleted` hooks that validate exit criteria, you get a pipeline where each handoff is programmatically verified rather than assumed.

```text
Build a [deliverable] using a quality-gated pipeline:
- Phase 1 (Researcher teammate): gather requirements and constraints
- Phase 2 (Designer teammate): design approach — blocked until Phase 1 complete
- Phase 3 (Implementer teammate): build — blocked until Phase 2 approved
- Phase 4 (Reviewer teammate): validate against original requirements — blocked until Phase 3 complete

Lead: require plan approval from Designer and Implementer before they proceed.
Only approve plans that explicitly address the constraints from Phase 1.
```

*Best for:* Structured document production (RFPs, PRDs, technical specs), code generation with requirements traceability, content pipelines with defined editorial stages.

---

**Pattern 6: Parallel Security Audit**

*Problem class:* A codebase or system that needs security review across multiple independent attack surfaces, where each surface requires specialized focus.

*Why teams help:* Security vulnerabilities don't cluster by file — they emerge from the interaction of authentication, authorization, input handling, data exposure, and dependency risk. A single reviewer scanning all surfaces tends to spend time unevenly, getting deep on whichever surface they check first. Parallel specialist reviewers cover more ground with more depth.

```text
Create a security audit team for [system]. Spawn:
- Auth reviewer: authentication flows, session management, token handling, password policies
- Input reviewer: injection vulnerabilities (SQL, command, XSS), input validation, output encoding
- Authorization reviewer: access control, privilege escalation, IDOR, permission boundaries
- Dependency reviewer: known CVEs in dependencies, outdated packages, supply chain risk
- Data reviewer: PII handling, encryption at rest and in transit, logging practices

All reviewers: produce findings with severity ratings (critical/high/medium/low)
and specific remediation recommendations.
Lead: synthesize findings, prioritize by severity × exploitability.
```

*Best for:* Pre-launch security review, periodic audits, post-incident security assessment, third-party code integration review.

### Quality Gate Hookset

A reusable hook configuration that enforces process discipline across all patterns above. Add to `settings.json`:

```json
{
  "hooks": {
    "TeammateIdle": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/require-output-artifact.sh"
          }
        ]
      }
    ],
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/validate-task-completion.sh"
          }
        ]
      }
    ]
  }
}
```

```bash
# ~/.claude/hooks/require-output-artifact.sh
# Require teammates to produce a written summary before going idle
#!/bin/bash
TEAM_NAME=$(jq -r '.team_name // empty' < /dev/stdin)
TEAMMATE_NAME=$(jq -r '.teammate_name' < /dev/stdin)

# Check if findings file exists for this teammate
FINDINGS_FILE="/tmp/${TEAM_NAME}-${TEAMMATE_NAME}-findings.md"
if [[ ! -f "$FINDINGS_FILE" ]]; then
  echo "Write your findings to $FINDINGS_FILE before finishing. Include: what you found, what you tested, confidence level." >&2
  exit 2
fi
exit 0
```

```bash
# ~/.claude/hooks/validate-task-completion.sh
# Prevent premature task completion — require evidence
#!/bin/bash
TASK_ID=$(jq -r '.task_id' < /dev/stdin)
TASK_SUBJECT=$(jq -r '.task_subject' < /dev/stdin)

# Tasks with "implement" in subject require test evidence
if echo "$TASK_SUBJECT" | grep -qi "implement\|build\|create\|write"; then
  EVIDENCE_FILE="/tmp/task-${TASK_ID}-evidence.txt"
  if [[ ! -f "$EVIDENCE_FILE" ]]; then
    echo "Implementation tasks require test evidence. Write test results to $EVIDENCE_FILE before completing." >&2
    exit 2
  fi
fi
exit 0
```

### Decision: This Playbook's Frameworks vs Agent Teams

The patterns in this playbook (13-agent model, responsibility-based organization, self-organizing systems) describe *how to think about* multi-agent coordination. Agent Teams is a *specific implementation tool* for a subset of those patterns.

**Use this playbook's frameworks when:**
- You're designing the architecture for a production multi-agent system
- You need the full 13-agent spectrum (communicator, evaluator, scheduler, etc.)
- You're building for scale, restartability, or fine-grained control
- Your workflow is recurring and worth the investment in custom orchestration

**Use Agent Teams when:**
- You want a working multi-agent workflow in one session
- The task maps cleanly to one of the six deployment patterns above
- 3–5 independently-owned workstreams cover your decomposition needs
- You're exploring whether parallel agent work helps before committing to architecture

They're not competitors. A production system might use the 13-agent architecture as its structural model and Agent Teams as the mechanism for running specific phases within that architecture.

---

## Sources & Notes on Illustrative Examples

**Core Framework & Agent Model:**
- everything-claude-code: 13-agent architecture, responsibility-based organization, parallel execution patterns, context isolation via artifact handoff

**Illustrative Metrics:**
- The "4× speedup" from parallel execution (60 seconds parallel vs. 240 seconds sequential) demonstrates the pattern from everything-claude-code but uses illustrative timing. Real-world speedup depends on agent complexity, API latency, and number of agents invoked in parallel.
- Model assignments per agent (Haiku vs. Sonnet vs. Opus) are illustrative based on everything-claude-code's cost-optimization principles; actual model selection depends on your quality requirements and cost budget.

**Additional Sources:**
- Production AI teams: Failure recovery limits, iteration bounds, context isolation strategies
- Stripe Minions: Responsibility-based (rather than capability-based) agent organization principles
- Artifact Specification section: Typed artifact schema (artifact_type, version, status, confidence, caveats) synthesized from distributed systems contract patterns applied to LLM agent pipelines; partial artifact pattern from production agentic systems
- System-Level Failure Recovery section: Cascading failure pattern, failure isolation, circuit breaker threshold (30%), and post-incident structure synthesized from production multi-agent system practices
- Scaling section: Stage-gating discipline, migration test suite requirement, and cost checkpoint pattern synthesized from production AI engineering practices
