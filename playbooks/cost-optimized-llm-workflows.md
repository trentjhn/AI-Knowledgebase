# Cost-Optimized LLM Workflows

**Adapted from [everything-claude-code](https://github.com/affaan-m/everything-claude-code) by Affaan Madooei**

> Building production AI systems at scale requires treating cost as a first-class architectural concern, not an optimization afterthought. This playbook teaches systematic cost control through model routing, budget enforcement, and intelligent retry strategies.

---

## Table of Contents

1. [The Cost-Architecture Relationship](#the-cost-architecture-relationship)
2. [Model Routing by Task Complexity](#model-routing-by-task-complexity)
3. [Budget Enforcement Patterns](#budget-enforcement-patterns)
4. [Intelligent Retry Strategies](#intelligent-retry-strategies)
5. [Prompt Caching & Reuse](#prompt-caching--reuse)
6. [Real-World Cost Audit](#real-world-cost-audit)

---

## The Cost-Architecture Relationship

**Most teams treat cost as a performance dial:** "We can make it cheaper by using a smaller model, or faster by using a larger one." This framing misses the deeper insight: **cost is a design constraint that should shape architecture upfront.**

When cost is ignored during design:
- Single-model pipelines route all work through the most capable (and expensive) model
- Retry logic doubles down: fail → retry with same model instead of routing to different one
- Context is bloated: every agent sees the full system context instead of just its task
- Monitoring is reactive: you discover cost problems after they've compounded

When cost is a design constraint:
- Each step has a model assignment based on actual complexity
- Failures route to different strategies (smaller model, retrieval, external tool)
- Context is intentionally scoped: agents see only what they need
- Cost is tracked and budgeted like any other resource

---

## Model Routing by Task Complexity

The core insight: **not all tasks need the same model.** Classify work by complexity and route accordingly.

### The Three-Tier Model Hierarchy

| Tier | Models | Cost | Best For | Example |
|---|---|---|---|---|
| **Tier 1: High-Capability** | Opus, GPT-4 | ~$15/M output | Complex reasoning, architecture, first attempts, security-critical | "Design a multi-agent system for this codebase" |
| **Tier 2: Mid-Capability** | Sonnet, GPT-4o | ~$5/M input | 85% of production work, multi-step workflows, general reasoning | "Implement this feature per spec" |
| **Tier 3: Fast/Cheap** | Haiku, GPT-4 Mini | ~$1/M input | Routing, classification, repetitive tasks, worker agents | "Classify this input type" |

### Routing Decision Tree

```
New task arrives

├─ Is this the first attempt at this type of problem?
│  └─ YES → Route to Tier 1 (Opus)
│     └─ If Opus succeeds, downgrade future similar tasks to Tier 2
│     └─ If Opus fails, escalate to human
│
├─ Is the task well-defined with clear success criteria?
│  └─ YES → Route to Tier 3 (Haiku)
│     └─ Can Haiku complete it? Keep there.
│     └─ Does Haiku fail? Route to Tier 2.
│
├─ Does this require multi-step reasoning or judgment calls?
│  └─ YES → Route to Tier 2 (Sonnet)
│     └─ Standard default for production work
│
└─ Will this be called 100s/1000s of times?
   └─ YES → Route to Tier 3 with fallback to Tier 2
```

### Multi-Step Pipeline Routing Example

A document processing system (classify → summarize → fact-check):

```
Step 1: CLASSIFY (Haiku)
├─ Input: Document, category list
├─ Cost: ~$0.001 per document
└─ Success signal: Classification matches expected pattern

Step 2: SUMMARIZE (Sonnet)
├─ Input: Document + classification
├─ Cost: ~$0.005 per document
└─ Success signal: Summary is between 100-300 words

Step 3: FACT-CHECK (Sonnet)
├─ Input: Summary + source document
├─ Cost: ~$0.005 per document
└─ Success signal: Factual claims are grounded in source

Total per document: ~$0.011
If all steps used Opus: ~$0.045 (75% more expensive)
If all steps used Haiku: 0.003 (unreliable on complex steps)
```

---

## Budget Enforcement Patterns

Cost control without enforcement is just hope. These patterns make budgets enforceable at runtime.

### Pattern 1: Immutable Cost Tracking

Track cost as an immutable data structure (not a mutable counter). Pseudocode:

```python
@dataclass(frozen=True)
class TokenUsage:
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    timestamp: datetime

@dataclass(frozen=True)
class TaskCost:
    task_id: str
    usages: List[TokenUsage]

    @property
    def total_cost(self) -> float:
        return sum(u.cost_usd for u in self.usages)

    def with_usage(self, usage: TokenUsage) -> "TaskCost":
        return TaskCost(
            task_id=self.task_id,
            usages=[*self.usages, usage]
        )
```

**Why immutable?** Enables audit trails, prevents silent cost growth, allows diff-based budget alerts.

### Pattern 2: Per-Task Budget Limits

Assign a budget to each task type and enforce it:

```
Task: "Implement feature"
├─ Budget: $0.50
├─ Allowed retries: 2
├─ Model sequence: Sonnet → (if fail) Sonnet again → (if fail) Opus
└─ Escalation: If Opus fails or budget exceeded, escalate to human

Task: "Classify document"
├─ Budget: $0.01
├─ Allowed retries: 1
├─ Model sequence: Haiku → (if fail) Sonnet
└─ Escalation: If both fail, fallback to rule-based classification
```

Enforce at runtime: reject any request that would exceed budget.

### Pattern 3: Cost Alerts & Anomalies

Monitor cost per task type over time. Alert on:
- **Drift:** Cost per task increases >10% from baseline
- **Outliers:** Single task costs more than 3× median
- **Budget overrun:** Task type exceeds weekly budget

Example alert rule:
```
IF (avg_cost_this_week / avg_cost_last_week) > 1.1
  AND (task_count_this_week == task_count_last_week)
THEN alert("Cost drift in task type X: investigate model quality or context growth")
```

---

## Intelligent Retry Strategies

A naive retry (fail → same model again) wastes money. Smart retries route differently:

### Retry Decision Tree

```
Task fails

├─ Is it a timeout or transient error?
│  └─ YES → Retry same model (may have been temporary)
│
├─ Is the model at its quality ceiling for this task type?
│  └─ YES → Upgrade model tier
│  └─ NO → Refine prompt and retry
│
├─ Is the task under-specified?
│  └─ YES → Request clarification from user, don't retry
│
└─ Is the model refusing the request?
   └─ YES → Revise request to remove triggering content, retry
```

### Example: Cost-Efficient Multi-Attempt Pattern

Task: "Generate product description"

```
Attempt 1: Haiku ($0.001)
├─ Cost: $0.001
├─ If success: done (total: $0.001)
├─ If fail (generic failure): goto Attempt 2
└─ If refuse (safety issue): escalate to human

Attempt 2: Sonnet ($0.005)
├─ Cost: $0.006 cumulative
├─ If success: done
├─ If fail: goto Attempt 3
└─ If refuse: escalate to human

Attempt 3: Opus ($0.015)
├─ Cost: $0.021 cumulative
├─ If success: done
├─ If fail: escalate to human
```

**Success rates:** 95% succeed at Haiku, 4% at Sonnet, 1% at Opus = 99% overall success rate at 6x lower cost than all-Opus.

---

## Prompt Caching & Reuse

Large static contexts (codebases, documentation, system prompts) should be cached to avoid re-processing costs.

### Cache Eligibility

```
Cacheable (if > 1KB):
├─ System prompts (reused for every task)
├─ Company documentation (used by many agents)
├─ Reference code (same for all feature implementation)
└─ Evaluator prompts (used for every output)

Not Cacheable:
├─ User input (changes on every request)
├─ Dynamic context (retrieval results)
├─ Conversation history (grows per turn)
```

### Cache Hit Strategy

Per Anthropic's prompt caching: after the first request (full cost), subsequent requests with the same cache block pay ~10% of the original cost.

**Example:** System prompt (2000 tokens, Opus)
- Request 1: Full cost (~$0.06)
- Requests 2-100 with same system prompt: ~$0.006 each
- Savings: 90% on repeated context

Budget accordingly: first request is expensive, then drops dramatically.

---

## Real-World Cost Audit

### Scenario: Customer Support Chatbot

**Setup:**
- 10,000 daily requests
- Each request: retrieve context, generate response, log result
- Naive approach: Opus for all

**Cost Breakdown** *(illustrative example from everything-claude-code cost architecture pattern):*

| Approach | Cost/Request | Cost/Day | Cost/Year |
|---|---|---|---|
| All Opus | $0.015 | $150 | $54,750 |
| Smart routing (40% Haiku, 55% Sonnet, 5% Opus) | $0.004 | $40 | $14,600 |
| **Savings** | **73% per request** | **$110/day** | **$40K/year** |

**Routing logic:**
- Haiku (40%): Simple classification, FAQ lookups, routing to right department
- Sonnet (55%): Complex questions, reasoning, multi-step handling
- Opus (5%): Escalated cases, novel scenarios, high-stakes decisions

**Quality impact:** Measured via user satisfaction *(illustrative metrics):*
- All-Opus: 92% satisfaction
- Smart routing: 91% satisfaction (1pt drop from cheaper tiers)
- Decision: Trade 1% satisfaction for 73% cost reduction ✓

> **Note:** This audit demonstrates the cost-architecture pattern from everything-claude-code. The specific percentages are illustrative; real-world cost savings vary based on task distribution and model pricing at time of implementation.

---

## Implementation Checklist

- [ ] Define model routing rules for each task type
- [ ] Implement immutable cost tracking dataclass
- [ ] Set per-task budget limits in config
- [ ] Add cost monitoring & alert rules
- [ ] Design retry strategies per task type
- [ ] Identify cacheable contexts (>1KB)
- [ ] Set baseline costs for each task type
- [ ] Monitor cost drift weekly
- [ ] Document cost assumptions in CLAUDE.md

---

## Sources & Notes on Illustrative Examples

**Core Framework & Patterns:**
- everything-claude-code: Cost-architecture relationship, three-tier model hierarchy, budget enforcement patterns (immutable cost tracking, per-task limits, alerts), intelligent retry strategies

**Illustrative Metrics & Examples:**
- The "Real-World Cost Audit" scenario (73% savings, specific cost/request figures) demonstrates the cost routing pattern from everything-claude-code but uses illustrative percentages to show the principle. Real-world numbers vary significantly based on your task distribution, model pricing, and quality requirements.
- The prompt caching example (90% savings on repeated context) is based on Anthropic's documented prompt caching performance characteristics.

**Additional Sources:**
- Anthropic: Prompt caching technical documentation
- Production AI teams: Budget enforcement patterns and monitoring strategies
