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
