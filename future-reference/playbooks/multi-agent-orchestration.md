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
6. [Failure Recovery](#failure-recovery)
7. [Scaling from 1 Agent to 13](#scaling-from-1-agent-to-13)

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

## Scaling from 1 Agent to 13

### Stage 1: Single Agent (MVP)
```
[User] → [Multipurpose Agent] → [Code]
├─ Does everything: planning, coding, review, testing
├─ Cost: Low
├─ Quality: Medium (one agent can't be expert at 13 things)
└─ Use when: Prototype, learning, low stakes
```

### Stage 2: Core Split (3 Agents)
```
[User] → [Planner] → [Implementer] → [Reviewer]
├─ Separates planning, implementation, review
├─ Cost: Higher than Stage 1
├─ Quality: High (each agent focused)
└─ Use when: Production, quality matters
```

### Stage 3: Full Specialization (13 Agents)
```
[User] → [Planner] → [Architect] → [TDD] → [Reviewer + Security + Tests]
         ├→ [Optimizer]
         ├→ [Documentation]
         ├→ [Deployment]
         └→ [Monitor + Learner]
├─ Cost: Higher (more agents) but lower per-agent (cheaper models)
├─ Quality: Highest (domain experts for each responsibility)
└─ Use when: Critical systems, continuous improvement
```

### Migration Path

**Don't try to adopt all 13 agents at once.** Start with Stage 1 or Stage 2, add agents as needs grow:

1. Start with: Planner + TDD Guide + Code Reviewer (Stage 2)
2. Add when tests fail often: Debugger
3. Add when style issues arise: Linter
4. Add for high-risk code: Security Reviewer
5. Add for slowness: Optimizer
6. Continue adding as workflow matures

---

## Implementation Checklist

- [ ] Define agents for your workflow (start with 3-5)
- [ ] Map each agent to a responsibility
- [ ] Determine proactive vs. reactive triggers
- [ ] Design parallel execution (which agents can work simultaneously?)
- [ ] Define context isolation (what does each agent see?)
- [ ] Create handoff artifacts (plan.md, architecture.md, etc.)
- [ ] Set failure recovery limits (max 2-3 iterations)
- [ ] Document agent prompts (why is each expert?)
- [ ] Test with a small task first
- [ ] Measure: quality improvements vs. cost increases
- [ ] Iterate agent prompts based on successes/failures

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
