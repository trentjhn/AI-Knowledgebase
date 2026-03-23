# Cost-Optimized LLM Workflows

**Adapted from [everything-claude-code](https://github.com/affaan-m/everything-claude-code) by Affaan Madooei**

> Building production AI systems at scale requires treating cost as a first-class architectural concern, not an optimization afterthought. This playbook teaches systematic cost control through model routing, budget enforcement, and intelligent retry strategies.

---

## Table of Contents

1. [The Cost-Architecture Relationship](#the-cost-architecture-relationship)
2. [How to Calculate Your Actual Costs](#how-to-calculate-your-actual-costs)
3. [Model Routing by Task Complexity](#model-routing-by-task-complexity)
4. [Classifying Task Complexity](#classifying-task-complexity)
5. [Budget Enforcement Patterns](#budget-enforcement-patterns)
6. [How to Set Per-Task Budgets](#how-to-set-per-task-budgets)
7. [Intelligent Retry Strategies](#intelligent-retry-strategies)
8. [Prompt Caching & Reuse](#prompt-caching--reuse)
9. [Prompt Caching Economics](#prompt-caching-economics)
10. [Real-World Cost Audit](#real-world-cost-audit)

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

## How to Calculate Your Actual Costs

The numbers in the rest of this playbook are illustrative. Before you can route, budget, or optimize anything, you need to know what your pipeline actually costs. Here is the methodology.

### The Unit Cost Formula

Every LLM call has a cost that can be calculated exactly:

```
cost_per_call = (input_tokens × input_price_per_M / 1_000_000)
              + (output_tokens × output_price_per_M / 1_000_000)
```

Prices are per-million tokens, published on each provider's pricing page. Check current pricing before building any cost model — prices shift frequently and have generally trended downward.

### Measuring Actual Token Usage

Every Anthropic, OpenAI, and Google API response includes a `usage` field with exact token counts. Anthropic returns `input_tokens` and `output_tokens`; OpenAI uses `prompt_tokens` and `completion_tokens`; Google uses `promptTokenCount` and `candidatesTokenCount`. Log these per call, not per session.

The distribution matters more than the mean. In most systems, p50 costs are 2–5× lower than p95 costs because a small fraction of queries trigger very long completions — complex inputs, edge cases, or prompts that produce verbose outputs. If you only track averages, those tail queries will surprise you in production.

### Task Cost Profiling Process

Run this before you route any task to a model tier:

1. **Sample your actual query distribution.** Run 50–100 representative queries through the pipeline — sampled from real user inputs, not a convenience sample you constructed. The distribution matters.
2. **Log per call:** `input_tokens`, `output_tokens`, model name, and wall-clock latency.
3. **Compute:** mean cost, p50, p95, p99 for each task type.
4. **Identify tail drivers.** Which query types produce the p95/p99 costs? Those are your highest-leverage optimization targets — fix the tail before optimizing the mean.
5. **Use these numbers for projection**, not provider estimates or rule-of-thumb figures.

Example profile output for a document-summarization step:

```
Task: summarize_document
Model: claude-sonnet
Samples: 100

input_tokens:   mean=1,840  p50=1,620  p95=3,900  p99=5,200
output_tokens:  mean=310    p50=280    p95=620     p99=890
cost_usd:       mean=$0.006 p50=$0.005 p95=$0.014  p99=$0.019

Tail driver: documents >4,000 input tokens (11% of sample, 38% of cost)
Action: chunk documents >3,500 tokens before summarization
```

### Multi-Step Pipeline Cost

In agentic systems, a single user interaction may involve 5–20 LLM calls. The cost that matters is total cost per user interaction, not cost per individual call.

Track and sum every call in a single request path. A pipeline that does:

```
Call 1: query rewrite (Haiku)
Calls 2–5: retrieval grading, 4 documents (Haiku × 4)
Call 6: answer generation (Sonnet)
Call 7: output validation (Haiku)
─────────────────────────────
Total: 7 calls = true cost of one interaction
```

If you only monitor call 6 (the generation step), you're blind to 60% of your cost.

### Extrapolating to Production

Once you have per-interaction cost from profiling:

```
monthly_cost = avg_cost_per_interaction × daily_interactions × 30
```

Add 20% headroom for tail queries and traffic spikes. This headroom is not conservative padding — it reflects the difference between your p50 profiling cost and the p95 reality at production traffic levels.

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

## Classifying Task Complexity

The routing decision tree above assumes you already know a task's complexity tier. In practice, determining the right tier for a novel task type requires empirical work, not intuition.

### Complexity Signals

Use these as a starting hypothesis, not a final answer:

**High complexity — reasoning model or frontier model (Tier 1)**
- Multi-step logical inference where intermediate steps affect later steps
- Code with subtle bugs that require understanding intent, not just syntax
- Tasks where the model must consider and reject multiple approaches before converging
- Adversarial, ambiguous, or edge-case content
- Tasks where the cost of a wrong output is high (security review, financial logic, medical content)

**Medium complexity — capable mid-tier model (Tier 2)**
- Summarization of substantial content (>1,000 words)
- Drafting structured documents (reports, specs, emails) where format and quality both matter
- Multi-turn dialog that requires retaining context across turns
- Tasks where judgment is needed but the answer space is reasonably constrained

**Low complexity — small/fast model (Tier 3)**
- Classification into a fixed set of categories
- Extraction of specific fields from structured content
- Simple reformatting (JSON → Markdown, extract name/date/amount)
- Yes/no decisions with clear criteria
- Routing decisions themselves (including deciding which tier to use)

### The Empirical Test

When you're uncertain about a task's tier, run the test — don't guess.

1. Take 20–30 representative examples of the task
2. Run them through the tier you think is appropriate
3. Evaluate quality (human eval or an automated metric you trust)
4. Run the same examples through the tier above
5. If the higher tier doesn't improve quality by >10%, you don't need it — stay at the lower tier

This is the only reliable way to classify novel task types. Complexity signals are a starting hypothesis; the empirical test is the answer.

### Calibration Signal

Use your test-set accuracy to determine tier assignment:

| Small-model accuracy on test set | Recommendation |
|---|---|
| >90% correct | Small model is the right tier — ship it |
| 70–85% correct | Gray zone — implement cascade routing (try small, escalate on low-confidence outputs) |
| <70% correct | Escalate to next tier and re-run the test |

The 70–85% gray zone is where cascade routing earns its complexity cost. Below 70%, cascade routing won't save you — you need the better model on all calls.

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

## How to Set Per-Task Budgets

Setting a budget of "$0.50 per task" is meaningless unless you know where that number came from. Use one of these three approaches, or combine them.

### Approach 1: Cost-of-Wrong

For tasks where errors have a measurable business cost, set the model budget proportional to that cost.

Ask: "What does it cost us when this task produces a wrong output?"

- If a wrong output requires 30 minutes of human review at $40/hr → that's $20 in error cost. Spending $1.00 on a better model to reduce that error rate is clearly rational.
- If a wrong output requires clicking "retry" → that's essentially $0 in error cost. Spending $0.50 on a premium model to avoid that is hard to justify.

A rough rule: model spend on a task should be less than 10% of the cost-of-wrong for that task type. If the error cost is $20, spending up to $2 on the model is defensible. If the error cost is $0.10, your model budget should be a fraction of a cent.

### Approach 2: Competitive Profiling

Run the task on multiple model tiers and find the cheapest tier that clears your quality bar.

1. Define a quality threshold (e.g., >90% accuracy on your test set, or a human eval score of ≥4/5)
2. Run the task on Tier 3 → measure quality
3. If it clears the threshold, you're done — Tier 3 is your tier
4. If not, try Tier 2 → measure quality
5. Repeat up the stack until you find the cheapest tier that clears threshold
6. Set your per-task budget to **1.5× the cost of that tier** — the headroom accounts for prompt drift (prompts get longer over time), traffic spikes, and model updates that may shift cost

### Approach 3: Revenue Ratio

For user-facing features, model cost per interaction should be a small fraction of the revenue that interaction generates.

```
acceptable_model_cost = revenue_per_interaction × target_margin_fraction
```

A feature that generates $0.10 in revenue per interaction (via subscription proration, conversion value, or ad revenue) should not cost $0.08 in model calls — that leaves no room for infrastructure, support, or profit. A reasonable target is model costs at <5–15% of interaction revenue, depending on your margin structure.

If you can't estimate revenue per interaction directly, use the inverse: if the feature is free and exists to drive retention, estimate the LTV impact of retaining vs. losing the user, then work backward to an acceptable per-interaction cost.

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

## Prompt Caching Economics

The existing section explains what caching is. This section explains when it's worth implementing and how to confirm it.

### How Prefix Caching Works (Anthropic Implementation)

Prefix caching stores the KV (key-value) state of a repeated prompt prefix on the provider's servers. On subsequent calls that share the same prefix, the provider skips recomputing that prefix and charges a reduced cache read price — typically 10% of the normal input token price for the cached portion.

The cache persists for approximately 5 minutes after last use (Anthropic as of early 2025). This means caching is most effective for high-frequency workloads where the same prefix is used repeatedly within short windows — not for low-volume or batch pipelines with long gaps between calls.

Provider support as of early 2025: Anthropic (Claude 3+ models), OpenAI (GPT-4o and newer), Google (Gemini 1.5+). Each has slightly different cache window duration and minimum cacheable length. Check current documentation before implementing.

### Break-Even Analysis

Before implementing caching, calculate whether it will pay off:

```
daily_savings = cached_tokens × 0.9 × input_price_per_token × cache_hit_rate × daily_calls
```

Where `0.9` represents the 90% price reduction on cache reads, and `cache_hit_rate` is the fraction of calls that actually hit the cache (not all calls to the same endpoint will — the prefix must match exactly and the cache must still be warm).

Example:
```
System prompt: 2,500 tokens
Input price: $3.00 / 1M tokens → $0.000003 per token
Cache hit rate: 70% (reasonable for a high-traffic endpoint)
Daily calls: 5,000

daily_savings = 2,500 × 0.9 × $0.000003 × 0.70 × 5,000
              = $23.63 / day → $700 / month
```

If implementing caching takes 4 hours of engineering time at $75/hr, break-even is less than one day. Worth it.

### Practical Minimums

- **Below ~500 cached tokens:** Savings are negligible. Don't add implementation complexity for this.
- **500–2,000 cached tokens with high hit rate (>70%):** Evaluate using the formula above — often worth it for high-traffic endpoints.
- **Above 2,000 cached tokens with >50% hit rate:** Almost always worth implementing.

### What to Cache and What Not To

Structure your prompts so stable content sits at the top (gets cached) and dynamic content sits at the bottom (doesn't need to be cached):

```
[CACHEABLE — put at top]
- System prompt
- Few-shot examples
- Reference documents, schemas, or policy text
- Tool definitions

[NOT CACHEABLE — put at bottom]
- The user's actual query
- Dynamic user-specific context (account details, session state)
- Retrieval results (change per query)
- Conversation history (grows per turn)
```

If you mix dynamic content into the middle of your prompt, the cache prefix breaks at that point and everything after it is re-computed. Keep the boundary clean.

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

**Before you route or budget anything:**
- [ ] Profile 50–100 representative queries per task type; log input_tokens, output_tokens, model
- [ ] Compute mean, p50, p95, p99 cost per task type — identify tail drivers
- [ ] Calculate per-interaction cost across all LLM calls in a single user request path
- [ ] Extrapolate to monthly cost with 20% headroom

**Routing and classification:**
- [ ] Classify each task type using complexity signals (high/medium/low)
- [ ] Run empirical test (20–30 examples per candidate tier) for any task type you're uncertain about
- [ ] Implement cascade routing for task types in the 70–85% accuracy gray zone
- [ ] Define model routing rules for each task type

**Budget setting:**
- [ ] Apply cost-of-wrong, competitive profiling, or revenue ratio to set per-task budgets
- [ ] Set per-task budget limits in config (1.5× the cost of the cheapest passing tier)
- [ ] Implement immutable cost tracking dataclass
- [ ] Add cost monitoring & alert rules

**Caching:**
- [ ] Identify cacheable contexts (>500 tokens, reused frequently within cache window)
- [ ] Run break-even formula for each candidate: `cached_tokens × 0.9 × price × hit_rate × daily_calls`
- [ ] Restructure prompts with stable content at top, dynamic content at bottom

**Ongoing:**
- [ ] Design retry strategies per task type
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
- The task cost profiling example (summarize_document) and caching break-even calculation are illustrative methodology examples; run the same process against your actual pipeline to get real numbers.

**Additional Sources:**
- Anthropic: Prompt caching technical documentation (cache window duration, pricing structure, minimum cacheable prefix length)
- Provider pricing pages: Anthropic, OpenAI, Google — check current pricing before building any cost model, as prices change frequently
- Production AI teams: Budget enforcement patterns, cost-of-wrong framing, and revenue ratio methodology
