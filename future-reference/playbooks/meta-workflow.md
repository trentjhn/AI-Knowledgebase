# Meta-Workflow: Problem → Production AI System

A comprehensive decision framework for building AI projects from ideation through production, with iterative brainstorming at every phase to catch missing details early.

---

## Introduction & Quick Start

**When to use this:** Starting any new AI project (agents, RAG, chatbots, classifiers, fine-tuned models), in interviews when asked to design a solution, or when co-brainstorming with AI to move from raw problem to comprehensive implementation plan.

**Core premise:** One-shot specifications miss critical details that surface later (at significant cost). This workflow builds brainstorming checkpoints into every phase so you refine requirements iteratively rather than discovering gaps at deployment.

**Three ways to use this:**
1. **Personal reference:** Open this doc during project kickoff, work through each phase with your team or with an AI assistant
2. **Interview tool:** Get a problem statement → Phase 0 + Phase 1 → walk out with a solid PRD and architecture
3. **AI-assisted brainstorming:** Share this doc with Claude, work through a phase together, co-generate specs/plans

**Structure:** 6 operational phases (0–6) that every project moves through. Each phase has:
- **Pre-phase brainstorm** — questions to explore before deciding
- **Execution steps** — what to do
- **Decision gate** — what "done" looks like
- **Common failure** — what usually breaks here and how to recover
- **Leverage points** — from Agentic Engineering §2, ranked by impact

**One document, fully scannable:** Each phase is ~100 lines. Jump to what you need.

---

## Phase 0: High-Level Ideation

**Purpose:** Clarify the actual problem you're solving before writing a single requirement.

**Why this matters:** Most projects fail because the problem statement is fuzzy. "Build an AI agent" is not a problem. "We manually review 500 support tickets per day and only handle 60% correctly" is a problem.

### Pre-Phase Brainstorm

Ask yourself (or brainstorm with your team/AI):
- **What's the real problem?** Not the solution idea. The actual pain point.
- **Who suffers from this?** Which users/processes?
- **What does "solved" look like?** What changes when this is fixed?
- **Why haven't we solved this yet?** Cost? Complexity? Didn't exist before?
- **What's the constraint?** Time? Budget? Accuracy? Latency? Scalability?

### Ideation Canvas (8 Components)

Use this template to flesh out the problem:

```
1. Problem Statement (1 sentence)
   "We need to _______ so that _______"

2. Users Affected
   Who specifically? (support team, customers, internal ops?)

3. Current State
   How is it done today? What's the cost/pain?

4. Desired State
   What does success look like? (30% faster? 95% accuracy?)

5. Key Constraint
   What matters most? Speed? Accuracy? Cost? Simplicity?

6. Scope Boundary
   What are we NOT solving?

7. Success Metrics
   How do we measure if it works? (e.g., "time per ticket drops from 8m to 3m")

8. Non-Negotiables
   What must be true? (e.g., "works offline", "cost < $500/month")
```

### Example: Support Ticket AI

```
1. Problem: "We need to auto-classify support tickets so that our team can prioritize and respond faster"

2. Users: 12 support agents processing 500 tickets/day, 60% misclassified by current keyword system

3. Current: Regex-based classifier, 60% accuracy, 1 min per ticket for manual review

4. Desired: 95%+ accuracy, auto-triage to right agent, < 30 sec per ticket

5. Constraint: Cost is secondary; accuracy and speed are primary

6. Scope: Classification only. Not: response generation, sentiment analysis, or customer satisfaction tracking (phase 2+)

7. Metrics: Accuracy %, time per ticket, human override rate

8. Non-negotiables: Works in 3 languages, GDPR-compliant (sensitive data)
```

### Gate: Phase 0 Done When

- [ ] Problem is stated in one sentence (not solution-focused)
- [ ] 3+ people (or you + AI) agree on the real problem
- [ ] Success metrics are measurable (not "better" or "good")
- [ ] Constraints are explicit (not assumed)
- [ ] Scope is bounded (we know what's NOT in scope)

**If gate fails:** Stop. Clarify the problem. The wrong problem perfectly solved = wrong output.

---

## Phase 1: Specification

**Purpose:** Convert the problem into an unambiguous, executable specification that guides design and development.

**Why separate from design:** A spec is "what we need to do." Architecture is "how we do it." You need clarity on WHAT before deciding HOW.

### Pre-Phase Brainstorm: Spec Prioritization

Before writing the spec, decide:
- **Who defines "done"?** Whose acceptance criteria matter most?
- **What detail matters?** Input examples? Output format? Constraints?
- **What could we drop if pressured?** Which requirements are "must-have" vs. "nice-to-have"?
- **What might change?** Where do we expect iteration?

### Spec Writing: 7 Properties of Executable Specs

Your spec must have these 7 properties (from Specification Clarity):

| Property | What It Means | Example Check |
|----------|---------------|---------------|
| **Complete** | No assumed context needed | Can a new engineer read this and know what to build? |
| **Unambiguous** | Every term has one interpretation | "Fast" is ambiguous; "< 500ms p95 latency" is not |
| **Consistent** | Requirements don't contradict | If spec says "always respond in 1 sec" but also "wait for full response", that's inconsistent |
| **Verifiable** | Output is testable | "Tickets are correctly classified" is vague; "98%+ accuracy on validation set" is testable |
| **Bounded** | Scope is explicit | "Generate AI features" is unbounded; "Classify support tickets into 12 categories" is bounded |
| **Prioritized** | Trade-offs are stated | "Accuracy matters more than latency" guides all future decisions |
| **Grounded** | Abstract goals linked to examples | Good: "Correctly classify this ticket: [example] into category X". Bad: "Be smart" |

### Concrete Acceptance Criteria Template

```
**Feature:** [One-line description]

**Acceptance Criteria:**
- [ ] Given [input], When [action], Then [output] (BDD format)
- [ ] Example: Given ticket: "Order not arriving", When classification runs, Then output "Logistics" with 90%+ confidence
- [ ] System handles [edge case] by [behavior]
- [ ] Performance: [metric] ≤ [threshold] in [conditions]
- [ ] Errors: [failure mode] → [recovery] (e.g., "On API timeout → retry 3x with exponential backoff")

**Out of Scope (explicitly):**
- Not implementing: [feature]
- Not supporting: [data type, language, use case]

**Success Metrics:**
- Metric 1: [measurement] (current: X, target: Y)
- Metric 2: [measurement]

**Constraints:**
- Cost: ≤ $[budget]/month
- Latency: ≤ [milliseconds]
- Accuracy: ≥ [%] on [dataset]
- Other: [language support, data residency, etc.]
```

### Playbook Selector: Which Playbooks Apply?

Now that you have a spec, which of the 7 playbooks do you need?

**Decision Tree (YES/NO flow):**

```
START: What's the core task?

1. Does the system make independent decisions and take actions?
   YES → Use "Building AI Agents"
   NO → Go to 2

2. Does it search/retrieve external knowledge?
   YES → Use "Building RAG Pipelines"
   NO → Go to 3

3. Is it a conversational interface (chat)?
   YES → Use "Building Chatbots"
   NO → Go to 4

4. Does it have multiple agents/workers coordinating?
   YES → Use "Multi-Agent Orchestration" (+ #1)
   NO → Go to 5

5. Is cost/efficiency a primary concern?
   YES → Use "Cost-Optimized LLM Workflows"
   NO → Check decision tree again or use "Writing Production Prompts"

6. Loop detection? If you answer YES to multiple above:
   - Agents + RAG → Use #1 (Agents) + "Agentic RAG" pattern
   - Agents + Cost concern → Use #1 + #5
   - RAG + Chat → Use #3 + #2
```

**Attribute Matrix (Alternative view):**

Check which apply to your project:

| Attribute | Present? | Implies Playbook |
|-----------|----------|------------------|
| Tool use (API calls, database queries, code execution) | Yes/No | Agents |
| Multi-step reasoning / planning | Yes/No | Agents |
| External knowledge retrieval | Yes/No | RAG Pipelines |
| Conversational interaction | Yes/No | Chatbots |
| Real-time updates needed | Yes/No | Event-driven or Async patterns |
| Multiple parallel agents | Yes/No | Multi-Agent Orchestration |
| Budget/cost is constraint | Yes/No | Cost-Optimized Workflows |
| Model fine-tuning candidate | Yes/No | Fine-Tuning playbook |

**Common failure:** Picking the wrong playbook (or forgetting to pick any). If your spec has agent-like traits but you pick the "Writing Production Prompts" playbook, you'll discover mid-Phase-3 that you need architecture work you skipped.

### Gate: Spec Done When

- [ ] Spec has all 7 properties (complete, unambiguous, consistent, verifiable, bounded, prioritized, grounded)
- [ ] Someone reads it and correctly implements without asking questions
- [ ] Acceptance criteria are testable (not fuzzy)
- [ ] Playbook(s) selected and confirmed with team
- [ ] Out-of-scope items explicitly listed

**If gate fails:** Go back to Phase 0 or re-brainstorm Phase 1. Don't advance with ambiguous specs.

---

## Phase 2: Architecture & Design

**Purpose:** Turn the spec into an architecture that fills the Four Pillars and optimizes for your constraints.

**Why separate from Phase 1:** Spec says WHAT. Architecture says HOW. Different concerns, different expertise.

### Pre-Phase Brainstorm: Architecture Ideation

- **What's the dominant constraint?** Cost? Latency? Accuracy? Reliability?
- **Which patterns fit?** (Plan-Build-Review, ReAct, Orchestrator, Multi-Agent, etc. from Agentic Eng §7)
- **Where does context go?** Which of the 8 context components matter most? (System message, history, retrieved knowledge, tools, state, etc.)
- **What could break?** Hallucinations? Cost overrun? Latency? Context overflow?

### Four Pillars: Fill Each One

From Agentic Engineering §1, every AI system has these 4 pillars. Your architecture must specify each:

| Pillar | Decision | Example |
|--------|----------|---------|
| **Prompt** | System instructions, tone, constraints | "You are a support ticket classifier. Classify each ticket into one of [12 categories]. Only respond with category + confidence. If uncertain, respond 'UNCLASSIFIED'." |
| **Model** | Which model? Which tier? | Claude Sonnet (good balance of cost/capability) vs. Opus (more capable but 3x cost) vs. Haiku (cheaper but limited reasoning) |
| **Context** | What goes into the context window? (from Context Engineering §3) | System prompt (always) + ticket text + category definitions + retrieval examples (RAG if needed) + feedback from last phase |
| **Tools** | What actions can the system take? | (In this case: none — pure classification. In agents: API calls, database writes, file operations.) |

**Template:**

```
**Pillar 1: Prompt**
- System instructions: [what is the agent's role?]
- Constraints: [what must it NOT do?]
- Format: [what output format exactly?]
- Tone: [how should it sound?]

**Pillar 2: Model**
- Choice: [model name + reasoning]
- Speed tradeoff: [latency target vs. capability needed]
- Cost ceiling: [$/month budget]

**Pillar 3: Context**
- What goes in: [System prompt? History? Retrieved knowledge? State?]
- What to omit: [what we DON'T send to avoid context overflow]
- Memory strategy: [stateless per request? Session-based? Persistent?]

**Pillar 4: Tools**
- Available: [list actions the system can take]
- Restricted: [what actions are forbidden?]
- Fallback: [if tool fails, what happens?]
```

### Architecture Decision Matrix: Cost vs. Complexity vs. Speed vs. Reliability

You likely have 2-3 ways to solve the spec. Evaluate each on these 4 axes:

**4-Axis Matrix Template:**

```
Option A: [Brief name & approach]
- Cost: $[estimate]/month
- Complexity: [Low/Medium/High] - effort to build/maintain
- Speed (latency): [ms, or "real-time" / "batch"]
- Reliability: [uptime %, or "brittle" / "robust"]

Option B: [Alternative]
- Cost: $
- Complexity:
- Speed:
- Reliability:

Option C: [Another alternative]
- Cost:
- Complexity:
- Speed:
- Reliability:
```

**Weighting (optional, if you're stuck):**

If you have competing options, assign weights based on your Phase 0 constraint:

```
If COST is primary: Weight [Cost: 50%, Complexity: 20%, Speed: 20%, Reliability: 10%]
If SPEED is primary: Weight [Cost: 10%, Complexity: 20%, Speed: 50%, Reliability: 20%]
If RELIABILITY is primary: Weight [Cost: 20%, Complexity: 10%, Speed: 10%, Reliability: 60%]
```

Then score each option 1-5 on each axis, multiply by weight, sum.

**Example: Support Ticket Classification**

```
Option A: Simple classifier (keyword + model)
- Cost: $50/month (Haiku-based)
- Complexity: Low (prompt engineering only)
- Speed: 100ms (real-time)
- Reliability: Medium (might hallucinate on edge cases)

Option B: RAG + fewshot (retrieve examples + model)
- Cost: $200/month (retrieval overhead + Sonnet)
- Complexity: Medium (needs retrieval setup)
- Speed: 400ms (latency from retrieval)
- Reliability: High (grounds in examples)

Option C: Fine-tuned model
- Cost: $500/month (infrastructure + inference)
- Complexity: High (data collection, training pipeline)
- Speed: 50ms (optimized)
- Reliability: Very High (custom to domain)

Constraint: Accuracy is PRIMARY. Cost is secondary.
Weighting: Accuracy/Reliability 60%, Cost 20%, Speed 10%, Complexity 10%

Scores (1-5):
Option A: (Medium reliability 3) * 0.6 + (Low cost 5) * 0.2 + (Fast 5) * 0.1 + (Low complexity 5) * 0.1 = 3.7
Option B: (High reliability 4) * 0.6 + (Medium cost 3) * 0.2 + (Slower 3) * 0.1 + (Med complexity 3) * 0.1 = 3.8
Option C: (High reliability 5) * 0.6 + (High cost 1) * 0.2 + (Fast 5) * 0.1 + (High complexity 1) * 0.1 = 3.6

Winner: Option B (barely). Or choose Option C if budget allows and accuracy > cost.
```

### Pattern Selection: Which Agentic Pattern?

From Agentic Engineering §7, pick the pattern that matches your spec:

- **Plan-Build-Review:** System plans steps, builds, reviews its own work. For complex multi-step tasks.
- **ReAct:** System reasons aloud, then acts. Good for interactive tasks, tool use.
- **Orchestrator:** Central agent coordinates sub-agents. For multi-agent systems.
- **HITL (Human-in-the-Loop):** System gets human feedback at key gates. For high-stakes decisions.
- **Expert Swarm:** Multiple specialized agents vote/compete. For consensus or diverse perspectives.
- **Persistent Memory:** Agent learns from past interactions. For long-running systems.
- **Simple Classifier/Generator:** No loops. Just: input → model → output. For single-pass tasks (like ticket classification).

Choose based on: complexity of task, need for iteration, availability of human feedback, multi-agent needs.

### Gate: Architecture Done When

- [ ] Four Pillars are filled (prompt, model, context, tools)
- [ ] Decision matrix completed for all options considered
- [ ] Pattern selected (or reason documented why none fit)
- [ ] Trade-offs acknowledged ("we're choosing cost over latency")
- [ ] Risk identified ("this relies on model's reasoning, might hallucinate on ambiguous tickets")

**If gate fails:** Go back to Phase 1 (spec didn't constrain enough) or redesign.

---

## Phase 3: Development & Prototyping

**Purpose:** Build the minimal version that proves the concept works.

**Key principle:** Minimal ≠ incomplete. It means feature-complete but not polished. Focus on whether the architecture works, not whether the UI is beautiful.

### Pre-Phase Brainstorm: Implementation Scope

- **What's the absolute minimum feature set?** (not everything from the spec, but enough to test the architecture)
- **What can we mock/fake?** (don't build unnecessary dependencies)
- **How will we test it?** (what does "it works" actually look like?)
- **Where will we discover problems?** (what are we uncertain about?)

### Minimal Implementation Checklist

```
- [ ] Core data pipeline working (input → model → output)
- [ ] One happy-path example running end-to-end
- [ ] Error handling for 3 failure modes (API timeout, invalid input, hallucination)
- [ ] Logging/monitoring so we can see what's happening
- [ ] Basic test covering the happy path
- [ ] Performance measured (how fast? how much does it cost?)
```

Do NOT build yet:
- UI/frontend polish
- Scalability (clustering, caching, load balancing)
- Advanced monitoring (dashboards, alerting)
- Documentation (comment your code, but not comprehensive docs)

### Testing Strategy: What "Working" Means

Define this NOW, before coding:

```
Testing Levels (from evaluation-ready architecture):

1. Unit: Individual functions (prompt formatting, response parsing)
   Example: Given ticket [X], parser outputs dict with keys [category, confidence]

2. Functional: End-to-end for one example
   Example: Full ticket → classification → output matches expected format

3. Behavioral: Does it meet the spec?
   Example: 95%+ accuracy on validation set

4. Failure: What happens when it breaks?
   Example: On API timeout, system retries 3x; on hallucination, marks UNCLASSIFIED
```

Start with level 1-2 (unit + functional). Level 3-4 are for Phase 4.

### Common Failure Mode in Phase 3

**"It works on my laptop but breaks in production"**

Root causes:
- Environment differences (API keys not set, wrong model tier)
- Edge cases not covered (empty input, very long input, special characters)
- Assumptions about data (assumed all tickets are in English)

Recovery: Test against diverse inputs (Phase 4). Add explicit error handling (retry, fallback, logging).

### Gate: Prototype Done When

- [ ] Minimal feature set runs end-to-end
- [ ] One happy-path test passes
- [ ] Performance measured (cost per call, latency p50/p95)
- [ ] 3 failure modes have explicit handling
- [ ] Code is reviewable (doesn't need to be perfect, but readable)

**If gate fails:** Debug. Don't move to Phase 4 with broken architecture.

---

## Phase 4: Scale & Harden

**Purpose:** Make the system reliable, observable, and cost-efficient at scale.

**Why separate:** Phase 3 proves the concept. Phase 4 makes it production-grade.

### Pre-Phase Brainstorm: Hardening Priorities

- **What will break first at scale?** (cost? latency? accuracy drift?)
- **What do we need to see?** (logs, metrics, alerts?)
- **How will we recover from failures?** (retry? fallback? escalate?)

### Hardening Checklist

#### Context Management (from Context Engineering §3)

- [ ] Define what goes in context (system prompt, history, retrieval, state)
- [ ] Define what's excluded (how much history? how many examples?)
- [ ] Implement context compression if needed (summarize old history)
- [ ] Handle context overflow (what happens if input + history > window limit?)
- [ ] Test with realistic data volumes

Example for support tickets:
```
Context allocated: 4k tokens
- System prompt: 500 tokens (ticket categories, instructions)
- Current ticket: 1000 tokens (full ticket text)
- Retrieval examples: 1500 tokens (5 examples of each category)
- History: 500 tokens (last 3 agent interactions)

If ticket is huge: Compress to first 500 + last 200 tokens
If retrieval slow: Cache examples or pre-rank
```

#### Observability (from AI System Design §9)

Implement logging for:
- [ ] Each request: input, model chosen, latency, cost
- [ ] Each model output: response, confidence, fallback triggered?
- [ ] Each failure: error type, retry count, recovery action
- [ ] Periodically: overall accuracy, cost drift, latency percentiles

```
Log structure:
{
  "timestamp": "2026-03-08T14:23:45Z",
  "request_id": "abc123",
  "input": "Order not arriving",
  "model": "claude-sonnet",
  "output_category": "Logistics",
  "output_confidence": 0.94,
  "latency_ms": 245,
  "cost_cents": 2.1,
  "error": null,
  "fallback_triggered": false
}
```

#### Cost Optimization

- [ ] Track cost per request (input + output tokens * model price)
- [ ] Identify expensive patterns (long context? many retries?)
- [ ] Consider model routing: send easy questions to Haiku, hard ones to Sonnet
- [ ] Set cost alarms (e.g., "if daily cost > $1000, alert")

Example:
```
Decision tree:
- If ticket < 200 tokens AND confidence > 0.8 from first pass → use Haiku (cost: 0.5¢)
- Otherwise → use Sonnet (cost: 1.5¢)
- Estimated cost reduction: 30% without accuracy loss
```

### Failure Taxonomy: Symptom → Root Cause → Recovery

**This is NEW. Not in other KB sections.** Map failures to root cause and recovery action:

| Symptom | Likely Root Cause | Phase(s) Failed | Recovery Action |
|---------|-------------------|-----------------|-----------------|
| "Accuracy dropped from 95% to 80%" | Model degradation OR data drift OR context overflow | Phase 1 (spec clarity) / Phase 2 (architecture) / Phase 3 (implementation) | 1. Check logs for patterns. 2. Measure accuracy on old vs. new data. 3. If context overflow: compress context. 4. If drift: re-run Phase 1 (problem might have changed). |
| "System hallucinates on ambiguous tickets" | Prompt is too permissive OR model doesn't have enough grounding | Phase 2 (architecture) / Phase 3 (prompt engineering) | 1. Add "UNCLASSIFIED" option for ambiguous cases. 2. Use retrieval (RAG) to ground decisions. 3. If retrieval unavailable: use fewshot examples in prompt. |
| "Cost is $5k/month, over budget" | Model choice too expensive OR context is bloated OR volume unexpected | Phase 2 (architecture) / Phase 4 (cost optimization) | 1. Implement model routing (use cheaper models when possible). 2. Compress context. 3. Cache retrieval results. 4. If none help: revisit Phase 1 (can we relax accuracy requirement to use cheaper model?). |
| "Latency is 2s, need < 500ms" | Too many steps OR context retrieval is slow OR model too large | Phase 2 (architecture) / Phase 4 (optimization) | 1. Parallelize steps if possible. 2. Cache retrieval. 3. Consider smaller model (Haiku vs. Sonnet). 4. Async processing (return fast, process later). |
| "System fails on non-English tickets" | Spec assumed English only, but data includes other languages | Phase 1 (scope boundary) / Phase 3 (error handling) | 1. Go back to Phase 0/1: do we need multi-language support? 2. If yes: update spec, update prompt to specify language. 3. Test with multilingual examples. |

**When to use this table:** Something breaks. Find the symptom. Follow the root cause and recovery.

### Gate: Hardened & Ready for Prod When

- [ ] Observability in place (logging for every request)
- [ ] Cost tracked and under budget
- [ ] 5+ failure modes handled explicitly
- [ ] Context management tested (no overflow, no memory leaks)
- [ ] Accuracy measured on validation set ≥ spec threshold
- [ ] Latency measured, within tolerance
- [ ] Retry/fallback strategies documented

**If gate fails:** Debug the specific failure. Don't ship.

---

## Phase 5: Production Deployment

**Purpose:** Ship to production safely, with monitoring and rollback capability.

### Pre-Phase Brainstorm: Deployment Strategy

- **How do we roll this out?** (all at once? gradual? canary?)
- **How do we measure success in production?** (different metrics than dev?)
- **What do we do if it fails?** (rollback plan? circuit breaker?)
- **Who has access?** (internal only? customers? regional rollout?)

### Six Production Safety Rules (from AI System Design §10)

Apply these non-negotiable rules:

| Rule | What It Means | For Our System |
|------|---------------|--------|
| **1. Database migrations are immutable, versioned, tested** | Never modify past migrations. New changes = new migration. | Store classifications in versioned schema. No altering past records. |
| **2. Schema changes generate migrations automatically** | Use tools/frameworks (Alembic for SQLAlchemy, Rails migrations) | If adding new classification category: auto-generate migration, test, review. |
| **3. Features fully tested before reaching prod** | Feature flags, staging==prod, no untested code in production | Classification feature hidden behind flag until 100% tested. Staging env identical to prod. |
| **4. Infrastructure is code** | Terraform, CloudFormation, Kubernetes YAML. No manual setup. | Deployment via code commit (CI/CD). No clicking buttons in console. |
| **5. Dependencies pinned exactly** | requirements.txt specifies exact versions. Intentional upgrades only. | `claude-sdk==1.2.3` not `claude-sdk>=1.0`. Upgrades reviewed + tested. |
| **6. Code follows established patterns** | Linting, ADRs (Architecture Decision Records), generators for boilerplate. | All handlers follow same structure (input validation, model call, output parsing, logging, error handling). |

### Agentic-Pattern-Specific Considerations

Different patterns have different deployment concerns:

```
Simple Classifier (like our example):
- Safety: High (stateless, single decision)
- Concerns: Model accuracy drift, API failures
- Monitoring: Request success rate, accuracy, latency

Agent with Tool Use:
- Safety: Medium (makes external API calls)
- Concerns: Tool failures, hallucinated commands, infinite loops
- Monitoring: Tool call success rate, loop depth, cost per request

Multi-Agent Orchestration:
- Safety: Low (complex interactions, hard to predict)
- Concerns: Deadlocks, cascading failures, context corruption
- Monitoring: Agent communication logs, decision tree visibility, failure correlation

Persistent Memory:
- Safety: Medium (state management risk)
- Concerns: Memory corruption, privacy leaks, unbounded growth
- Monitoring: Memory size, stale data, privacy violations
```

### Deployment Checklist

```
- [ ] Code reviewed (at least 1 other person)
- [ ] All tests pass (unit + functional + behavioral)
- [ ] Feature flag ready (system can be toggled off instantly)
- [ ] Staging environment tested (identical to prod config)
- [ ] Monitoring dashboards created (cost, latency, accuracy, errors)
- [ ] Alerts configured (anomaly detection on key metrics)
- [ ] Rollback plan documented (if something breaks, how do we revert?)
- [ ] Documentation updated (API docs, runbooks, debugging guides)
- [ ] Compliance checked (GDPR, data residency, etc. from Phase 1 constraints)
- [ ] Load tested (can it handle peak traffic?)
```

### Gate: Production-Ready When

- [ ] All 6 safety rules applied
- [ ] Monitoring in place
- [ ] Rollback plan documented and tested
- [ ] Team trained on runbooks
- [ ] Go/No-go decision made (metrics show readiness)

**If gate fails:** Wait. Don't force prod deployment.

---

## Phase 6: Production Operation & Evolution

**Purpose:** Run the system, measure success, iterate based on real-world performance.

### Pre-Phase Brainstorm: Metrics & Iteration

- **What metrics matter?** (from Phase 0 success criteria)
- **What will we do with the data?** (weekly reviews? daily?)
- **When do we iterate?** (if accuracy drops? if cost increases?)
- **When do we stop?** (when is it "good enough"?)

### Metric Templates

Connect Phase 0 success criteria to actual measurements:

```
Phase 0 Goal: "95%+ accuracy on support ticket classification"

Production Metrics:
- Accuracy: % of tickets classified correctly (measured by human spot-check weekly)
- Current: 94.2% | Target: 95%+ | Alarm: < 92%

- Confidence: % of classifications where model is confident (> 0.9)
- Current: 78% | Target: 85%+ | Alarm: < 70%

- Unclassified rate: % of tickets marked "UNCLASSIFIED" because ambiguous
- Current: 3.1% | Target: < 2% | Alarm: > 5%

Phase 0 Goal: "Time per ticket drops from 8m to 3m"

Production Metrics:
- Agent efficiency: Average time per ticket (auto-routed + classification)
- Current: 4.2m | Target: < 3m | Alarm: > 5m

- Route accuracy: % of tickets sent to correct team
- Current: 93% | Target: 95%+ | Alarm: < 90%
```

### Iteration Triggers: When to Revisit Earlier Phases

```
Trigger: Accuracy drops below target for 3 consecutive days
→ Go back to Phase 1 (spec: did problem change?)
→ Then Phase 3 (prompt engineering: can we improve?)
→ Then Phase 4 (debugging: is context overflow causing confusion?)

Trigger: Cost doubles unexpectedly
→ Go back to Phase 4 (cost optimization: why?)
→ Check: are we calling model for every ticket? Can we cache?
→ Consider: Phase 2 (model routing: use cheaper model for easy cases?)

Trigger: Customer complaints about misclassifications
→ Go back to Phase 0 (did the problem scope change?)
→ Then Phase 1 (spec: are we missing a category?)
→ Then Phase 3 (prompt: clarify instructions)

Trigger: 4 weeks of steady performance, cost under budget, accuracy > target
→ Consider: expanding scope (Phase 1) to add more categories
→ Or: optimize further (Phase 4) to reduce cost more
```

### Stopping Criteria: When to Stop Iterating

```
Stop iterating when:
- [ ] All success metrics from Phase 0 are met and stable (2+ weeks)
- [ ] Cost is ≤ budget and stable
- [ ] Accuracy is ≥ spec target and stable
- [ ] Team is satisfied (not spending 10+ hours per week on fixes)
- [ ] No actionable improvements left (diminishing returns)

Do NOT stop just because:
- "It's good enough" (Define "good enough" in Phase 0)
- "We ran out of time" (Plan better next time)
- "It's working now" (What about next month?)

Do continue if:
- Metrics trending wrong (accuracy down 5% in a week)
- New data reveals problems (new ticket types coming)
- Cost is out of control
```

### Continuous Learning Loop

Every 4 weeks, reflect:

1. **What metrics matter today?** (from Phase 0, still valid?)
2. **Are we hitting them?** (data-driven honest assessment)
3. **What's the biggest blocker?** (accuracy? cost? latency? scaling?)
4. **Which phase should we revisit?** (use Failure Taxonomy to trace root cause)
5. **Do we re-run phases 1-5, or just tune (phase 3-4)?**

---

## Quick Reference Tools

### All-Phases Checklist

Quick copy-paste for your project:

```
[ ] Phase 0: High-Level Ideation
    [ ] Problem stated clearly
    [ ] Success metrics defined
    [ ] Constraints explicit

[ ] Phase 1: Specification
    [ ] Spec has 7 properties (complete, unambiguous, consistent, verifiable, bounded, prioritized, grounded)
    [ ] Acceptance criteria testable
    [ ] Playbook(s) selected

[ ] Phase 2: Architecture & Design
    [ ] Four Pillars filled (prompt, model, context, tools)
    [ ] Decision matrix completed (cost vs. complexity vs. speed vs. reliability)
    [ ] Pattern selected

[ ] Phase 3: Development & Prototyping
    [ ] Minimal version runs end-to-end
    [ ] Test passes
    [ ] Performance measured

[ ] Phase 4: Scale & Harden
    [ ] Context management tested
    [ ] Observability in place
    [ ] Cost optimized
    [ ] 5+ failure modes handled

[ ] Phase 5: Production Deployment
    [ ] 6 safety rules applied
    [ ] Monitoring dashboards live
    [ ] Rollback plan documented

[ ] Phase 6: Production Operation & Evolution
    [ ] Metrics tracked
    [ ] Iteration cycle established
    [ ] Team trained on runbooks
```

### Decision Matrix Template (Empty)

Copy-paste for your project:

```
**Constraint from Phase 0:** [What matters most?]

**Option A: [Approach Name]**
- Cost: $[]/month | Complexity: [Low/Med/High] | Speed: [ms] | Reliability: [%]

**Option B: [Approach Name]**
- Cost: $[]/month | Complexity: [Low/Med/High] | Speed: [ms] | Reliability: [%]

**Option C: [Approach Name]**
- Cost: $[]/month | Complexity: [Low/Med/High] | Speed: [ms] | Reliability: [%]

**Weighting:** Cost [%] + Complexity [%] + Speed [%] + Reliability [%] = 100%

**Scoring (1-5 per axis):**
| Option | Cost | Complexity | Speed | Reliability | Weighted Score |
|--------|------|-----------|-------|-------------|----------------|
| A | [score] | [score] | [score] | [score] | [result] |
| B | [score] | [score] | [score] | [score] | [result] |
| C | [score] | [score] | [score] | [score] | [result] |

**Winner:** [Option] because [reason]
```

### Failure Taxonomy (Reference)

**Full failure table from Phase 4:**

| Symptom | Root Cause | Phase(s) | Recovery |
|---------|-----------|---------|----------|
| Accuracy drops | Model degradation / data drift / context overflow | 1,2,3 | Check logs → measure → fix context/prompt/spec |
| Hallucinations | Prompt too permissive / insufficient grounding | 2,3 | Add guardrails → use RAG/fewshot → test |
| Cost explosion | Wrong model / bloated context / high volume | 2,4 | Route models → compress → cache → re-spec |
| Latency high | Too many steps / slow retrieval / large model | 2,4 | Parallelize → cache → smaller model → async |
| Edge case failures | Spec incomplete / error handling missing | 1,3 | Expand spec → test edge cases → add handling |
| Privacy/compliance issues | Data handling misaligned with spec | 1,5 | Audit spec → data residency → GDPR checks |
| Cascading failures (multi-agent) | Agent interactions not bounded | 2,4 | Add circuit breakers → timeouts → monitoring |

### Leverage Points Quick Reference

From Agentic Engineering §2, ranked by impact. Focus on high-leverage first:

**High Impact (1-4): Focus in Phases 0-2**
1. ADWs (AI Developer Workflows) — how work flows between components
2. Templates — reusable output structure
3. Plans — detailed task scope before coding
4. Architecture — codebase is intuitive to navigate

**Medium Impact (5-8): Focus in Phases 3-4**
5. Tests — meaningful behavioral verification
6. Documentation — agent can navigate codebase
7. Types — consistent typing (Python type hints, etc.)
8. Observability — clear logs and visibility

**Low Impact (9-12): Focus in Phases 5-6 (tuning)**
9. Tools — what actions available
10. Prompt — instructions clarity
11. Model — capability tier
12. Context — what agent knows

**Implication:** Don't spend weeks on prompt engineering (point 10) if architecture (point 4) is broken.

### KB Section Links (What to Read for Each Phase)

Jump to full KB docs for deep understanding:

- **Phase 0-1 (Problem & Spec):** Read `specification-clarity.md` (lines 1–89)
- **Phase 2 (Architecture):** Read `agentic-engineering.md` §1 (Four Pillars) + §2 (Leverage Points) + §7 (Patterns)
- **Phase 2 (Context decisions):** Read `context-engineering.md` (lines 60–131, 8 components + 4 strategies)
- **Phase 3 (Prompting):** Read `prompt-engineering.md` (lines 43–280, core techniques)
- **Phase 4 (Evaluation):** Read `evaluation.md` (lines 1–300, testing strategies)
- **Phase 4 (Security):** Read `ai-security.md` for threat model relevant to your pattern
- **Phase 5 (Production):** Read `ai-system-design.md` (lines 800–871, safety rules + observability)
- **Phase 6 (Evolution):** Read `evaluation.md` (lines 600–756, RAG eval + monitoring patterns)

---

## How to Use This Document

**Personal reference:** Bookmark this. When starting a project, open it. Work through phases 0-1 with your team. Share with Claude AI when brainstorming. Jump to decision matrices when stuck.

**Interview preparation:** Get a problem statement. Read Phase 0 + Phase 1. Spend 30 minutes with an AI brainstorming the spec. Walk into the interview with a solid starting point.

**AI-assisted co-design:** Share this whole document with Claude. Say "I want to design X. Can we work through the meta-workflow together?" Go phase-by-phase, let AI prompt you with brainstorm questions, co-generate specs and architecture decisions.

**Team guidance:** Use as a checklist for code reviews. "Did we define Phase 0 clearly?" "Is the spec actually unambiguous or are we guessing?" "Does the architecture fill all Four Pillars?"

---

## Conclusion: Why This Workflow Matters

Traditional project management assumes requirements are stable. AI projects are different: requirements are fuzzy, models behave unpredictably, and iteration is constant. This workflow bakes iteration into every phase so you don't discover critical gaps at the worst times (e.g., in production, or during interviews when you're trying to impress).

The six phases are:
- **Universal:** Every AI project moves through them
- **Iterative:** Brainstorming at each phase catches missed details
- **Decision-focused:** Gates force clarity before advancing
- **Failure-aware:** Failure taxonomy helps you recover fast
- **AI-assisted:** Designed to be co-created with Claude or other AI partners

Use this as your decision framework. Adapt it to your context. But don't skip phases just because you're in a hurry — that's where mistakes happen.

---

**Last Updated:** March 2026
**Source:** Synthesized from AI Knowledgebase (agentic-engineering, specification-clarity, context-engineering, ai-system-design, evaluation)
**Status:** Production-ready reference guide for personal and shareable use
