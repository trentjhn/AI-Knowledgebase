# Project Planning Template

Use this template when starting a new AI project. Fill in each section, then reference the full meta-workflow.md for detailed guidance. Share this with your team or Claude for collaborative design.

**Project Name:** [...]
**Owner:** [...]
**Date Started:** [...]

---

## Phase 0: High-Level Ideation

### Problem Statement (1 sentence)
[What's the actual problem, not the solution?]

### Ideation Canvas

**1. Problem Statement** (The real pain point)
[...]

**2. Users Affected** (Who specifically?)
[...]

**3. Current State** (How is it done today?)
[...]

**4. Desired State** (What does success look like?)
[...]

**5. Key Constraint** (What matters most? Speed? Accuracy? Cost?)
[...]

**6. Scope Boundary** (What are we NOT solving?)
[...]

**7. Success Metrics** (Measurable outcomes)
[...]

**8. Non-Negotiables** (Must-haves)
[...]

### Gate: Phase 0 Done?
- [ ] Problem is stated clearly (not solution-focused)
- [ ] 3+ people agree on real problem
- [ ] Success metrics are measurable
- [ ] Constraints are explicit
- [ ] Scope is bounded

---

## Phase 1: Specification

### Pre-Phase Brainstorm
**Who defines "done"?** [...]
**What detail matters most?** [...]
**What could we drop if pressured?** [...]
**What might change?** [...]

### Acceptance Criteria (BDD Format)

**Feature:** [Brief description]

```
- [ ] Given [input], When [action], Then [output]
- [ ] Example: Given [specific example], When [action], Then [expected result with confidence %]
- [ ] System handles [edge case] by [behavior]
```

**Performance:**
- Metric 1: [measurement] ≤ [threshold]
- Metric 2: [measurement] ≤ [threshold]

**Out of Scope:**
- Not implementing: [...]
- Not supporting: [...]

### Spec Properties Checklist (7 Properties)
- [ ] **Complete:** No assumed context needed
- [ ] **Unambiguous:** Every term has one meaning (not "fast" or "smart")
- [ ] **Consistent:** No contradicting requirements
- [ ] **Verifiable:** Output is testable
- [ ] **Bounded:** Scope is explicit
- [ ] **Prioritized:** Trade-offs are stated
- [ ] **Grounded:** Abstract goals linked to examples

### Playbook Selection

**Decision Tree Result:** [Which playbook path did you take?]

**Playbook(s) Selected:**
- [ ] Building AI Agents
- [ ] Building RAG Pipelines
- [ ] Building Chatbots
- [ ] Multi-Agent Orchestration
- [ ] Cost-Optimized LLM Workflows
- [ ] Writing Production Prompts
- [ ] Fine-Tuning

**Why these?** [Justify your selection]

### Gate: Spec Done?
- [ ] All 7 properties present
- [ ] Acceptance criteria testable
- [ ] Playbook(s) selected
- [ ] Team agrees on scope

---

## Phase 2: Architecture & Design

### Pre-Phase Brainstorm
**Dominant constraint?** [Cost? Latency? Accuracy? Reliability?]
**Which pattern fits?** [Plan-Build-Review? ReAct? Orchestrator? Multi-Agent?]
**Where does context go?** [Which 8 components matter?]
**What could break?** [Hallucinations? Cost explosion? Context overflow?]

### Four Pillars

**Pillar 1: Prompt**
- System instructions: [...]
- Constraints: [...]
- Format: [...]

**Pillar 2: Model**
- Choice: [Claude Sonnet / Opus / Haiku / Other]
- Reasoning: [...]
- Cost ceiling: $[...]/month

**Pillar 3: Context**
- What goes in: [System prompt? History? RAG? State?]
- What's omitted: [To avoid context overflow]
- Memory strategy: [Stateless? Session-based? Persistent?]

**Pillar 4: Tools**
- Available: [List actions]
- Restricted: [Forbidden actions]
- Fallback: [If tool fails, what happens?]

### Decision Matrix (Cost vs. Complexity vs. Speed vs. Reliability)

**Constraint from Phase 0:** [Primary concern]

| Option | Cost/month | Complexity | Speed (latency) | Reliability | Notes |
|--------|-----------|-----------|-----------------|-------------|-------|
| A: [...] | $[...] | Low/Med/High | [...] | [...] % | |
| B: [...] | $[...] | Low/Med/High | [...] | [...] % | |
| C: [...] | $[...] | Low/Med/High | [...] | [...] % | |

**Winner:** [Option] because [...]

### Pattern Selected
[Plan-Build-Review / ReAct / Orchestrator / HITL / Expert Swarm / Persistent Memory / Simple Classifier]

**Why?** [...]

### Gate: Architecture Done?
- [ ] Four Pillars filled
- [ ] Decision matrix completed
- [ ] Pattern selected
- [ ] Trade-offs acknowledged
- [ ] Risks identified

---

## Phase 3: Development & Prototyping

### Pre-Phase Brainstorm
**Minimal feature set?** [Absolute minimum to test architecture]
**What can we mock?** [Don't build unnecessary dependencies]
**How will we test?** [What does "it works" mean?]
**Where will we discover problems?** [What's uncertain?]

### Minimal Implementation Checklist

- [ ] Core pipeline works (input → model → output)
- [ ] One happy-path example runs end-to-end
- [ ] Error handling for 3 failure modes
- [ ] Logging/monitoring in place
- [ ] Basic test passes
- [ ] Performance measured (cost, latency)

### Testing Strategy

**Unit Testing:**
Example: Given [input], parser outputs [expected structure]

**Functional Testing:**
Example: Full [task] → [action] → output matches [expected format]

**Behavioral Testing:**
Example: System meets spec? [Accuracy ≥ X%? Latency ≤ Xms?]

### Gate: Prototype Done?
- [ ] Minimal feature set works end-to-end
- [ ] Happy-path test passes
- [ ] Performance measured
- [ ] 3 failure modes handled
- [ ] Code is reviewable

---

## Phase 4: Scale & Harden

### Pre-Phase Brainstorm
**What breaks first at scale?** [Cost? Latency? Accuracy?]
**What do we need to see?** [Logs, metrics, alerts?]
**How do we recover from failures?** [Retry? Fallback? Escalate?]

### Context Management

- [ ] Define what goes in context (token budget: [...])
- [ ] Define what's omitted (compression strategy: [...])
- [ ] Handle overflow (if context > limit: [...])
- [ ] Test with realistic volumes

### Observability (Logging)

```
Log per request:
{
  "timestamp": "...",
  "request_id": "...",
  "input": "...",
  "model": "...",
  "output": "...",
  "latency_ms": ...,
  "cost_cents": ...,
  "error": null
}
```

### Cost Optimization

**Current cost:** $[...]/month at current volume
**Budget:** $[...]/month
**Optimization strategy:** [Model routing? Caching? Compression?]

### Failure Recovery (Failure Taxonomy)

| Symptom | Root Cause | Recovery |
|---------|-----------|----------|
| [What breaks?] | [Why?] | [What to do?] |
| [...] | [...] | [...] |

### Gate: Hardened & Ready?
- [ ] Context management tested
- [ ] Logging in place
- [ ] Cost tracked and under budget
- [ ] 5+ failure modes handled
- [ ] Accuracy ≥ spec threshold
- [ ] Latency within tolerance

---

## Phase 5: Production Deployment

### Pre-Phase Brainstorm
**Rollout strategy?** [All at once? Gradual? Canary?]
**Success metrics in prod?** [Different from dev?]
**Failure response?** [Rollback plan?]
**Access control?** [Who can use it?]

### Safety Rules Applied

- [ ] Rule 1: Database migrations immutable + versioned
- [ ] Rule 2: Schema changes auto-generate migrations
- [ ] Rule 3: Features fully tested before prod (feature flags)
- [ ] Rule 4: Infrastructure as code (CI/CD, not manual)
- [ ] Rule 5: Dependencies pinned exactly
- [ ] Rule 6: Code follows established patterns

### Agentic Pattern Considerations

**Pattern:** [Simple Classifier / Agent / Multi-Agent / Persistent Memory]
**Safety level:** [High / Medium / Low]
**Key monitoring:** [...]

### Deployment Checklist

- [ ] Code reviewed
- [ ] All tests pass
- [ ] Feature flag ready
- [ ] Staging tested (≈ prod)
- [ ] Monitoring dashboards live
- [ ] Alerts configured
- [ ] Rollback plan documented
- [ ] Documentation updated

### Gate: Production-Ready?
- [ ] Safety rules applied
- [ ] Monitoring in place
- [ ] Rollback plan tested
- [ ] Team trained
- [ ] Go/No-go decision: [GO / NO-GO]

---

## Phase 6: Production Operation & Evolution

### Pre-Phase Brainstorm
**What metrics matter?** [From Phase 0 success criteria]
**What will we do with data?** [Weekly reviews? Daily?]
**When do we iterate?** [If accuracy drops? Cost increases?]
**When do we stop?** [Iteration stopping criteria?]

### Metric Templates

**Metric 1: [...]**
- Current: [measurement] | Target: [goal] | Alarm: < [threshold]

**Metric 2: [...]**
- Current: [measurement] | Target: [goal] | Alarm: < [threshold]

### Iteration Triggers

| Trigger | Go Back To | Recovery |
|---------|-----------|----------|
| [Symptom drops below target] | Phase [X] | [Action] |
| [...] | [...] | [...] |

### Stopping Criteria

- [ ] All success metrics met for 2+ weeks
- [ ] Cost ≤ budget
- [ ] Accuracy ≥ spec target
- [ ] Team satisfied
- [ ] No actionable improvements left

### 4-Week Reflection Checklist

- [ ] Metrics still valid? (or did problem change?)
- [ ] Are we hitting targets?
- [ ] What's the biggest blocker?
- [ ] Which phase should we revisit?
- [ ] Loop or stop?

---

## Summary

**Project Status:** [Planning / Building / Deployed / Operating]

**Key Decisions:**
- Model: [...]
- Pattern: [...]
- Primary Constraint: [...]
- Playbook(s): [...]

**Next Steps:**
1. [...]
2. [...]
3. [...]

**Last Updated:** [Date]
**Next Review:** [Date]

---

## How to Use This Template

1. **Kickoff:** Fill in Phases 0-1 in your first meeting. Lock in problem + spec.
2. **Design:** Collaboratively fill Phase 2. Debate the decision matrix, pick the pattern.
3. **Build:** Use Phase 3 checklist to guide development.
4. **Harden:** Fill Phase 4 as you approach prod. Identify failure modes now.
5. **Deploy:** Use Phase 5 checklist for launch readiness.
6. **Operate:** Use Phase 6 to track metrics and decide when to iterate.

**Share with Claude:** Copy the filled template, paste into chat: "Let's review Phase 2 architecture together. Here's where we are..." Claude can help you refine decisions or spot gaps.

**Version Control:** Store in your project repo. Update after major decisions. Becomes your project's decision record.
