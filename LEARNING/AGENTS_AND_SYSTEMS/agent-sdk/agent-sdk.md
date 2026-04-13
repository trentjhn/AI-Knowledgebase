# Claude Agent SDK Patterns

**Sources:** Anthropic Claude Cookbooks — `claude_agent_sdk/`, `managed_agents/`, `patterns/agents/`, `tool_use/` *(2025)*

---

## Table of Contents

1. [SDK vs. Base API — What's Different](#1-sdk-vs-base-api--whats-different)
2. [Core Abstractions](#2-core-abstractions)
3. [Pattern 1: The Research Agent](#3-pattern-1-the-research-agent)
4. [Pattern 2: Chief-of-Staff Multi-Agent Orchestration](#4-pattern-2-chief-of-staff-multi-agent-orchestration)
5. [Pattern 3: Parallel Subagents with Model Tiering](#5-pattern-3-parallel-subagents-with-model-tiering)
6. [Pattern 4: Programmatic Tool Calling (PTC)](#6-pattern-4-programmatic-tool-calling-ptc)
7. [Pattern 5: Semantic Tool Routing at Scale](#7-pattern-5-semantic-tool-routing-at-scale)
8. [Pattern 6: Evaluator-Optimizer Loop](#8-pattern-6-evaluator-optimizer-loop)
9. [Choosing Between Patterns](#9-choosing-between-patterns)
10. [Cost Optimization Across Patterns](#10-cost-optimization-across-patterns)
11. [Anti-Patterns](#11-anti-patterns)

---

## 1. SDK vs. Base API — What's Different

The base Claude API gives you a powerful but low-level interface: you send a messages array, you get a response. If you want a multi-turn conversation, you manage the history yourself. If you want to call a tool, you parse the response and handle it yourself. If you want to spawn a subagent, you write that infrastructure from scratch.

The Claude Agent SDK is the layer above that. Think of the base API as the engine and the SDK as the car — the engine works great on its own, but the car gives you steering, brakes, a fuel gauge, and a seat. The SDK provides first-class concepts designed specifically for production agent systems:

- **Sessions** — persistent, resumable conversations with server-side state management. You don't have to pass the full message history on every call.
- **Task tool** — built-in mechanism for delegating work to specialized subagents. One agent can spawn another, pass it a task, and receive the result.
- **Vaults** — per-user credential stores for multi-tenant systems. Your agents can access user-specific credentials without those credentials ever touching your application code.
- **Events and webhooks** — the SDK emits structured events at key lifecycle points (agent created, tool called, session paused, etc.) that your application can subscribe to.

**When to use the SDK vs. the base API:**

| Use base API when | Use Agent SDK when |
|---|---|
| Single-turn or simple multi-turn chat | Long-running tasks that need state across turns |
| One model, one conversation | Multiple agents coordinating |
| You're managing history manually | You need server-side session persistence |
| Simple tool use (1-5 tools) | Complex tool ecosystems, credential management |
| Prototyping | Production deployment |

The patterns in this document draw from official Anthropic cookbook examples. Implementation specifics (exact method signatures, SDK versions) should be verified against the current SDK documentation — what matters here is the *pattern* and its tradeoffs.

---

## 2. Core Abstractions

Before the patterns, four SDK concepts worth understanding on their own:

### `query()` — Stateless Requests

The simplest SDK entry point. Stateless: you provide a system prompt and a message, you get a response. No session overhead, no state management. Best for:
- Independent research tasks that don't need history
- Single-purpose extraction or analysis
- Parallelizable subtasks where each is self-contained

Think of it as "smart function call" — input in, output out, nothing persists.

### Sessions — Stateful Conversations

Sessions wrap a persistent conversation with full state managed server-side. A session can be paused, resumed, and inspected. Sessions emit structured events your application can consume. This is the foundation for any agent that needs to:
- Maintain context across multiple interactions
- Be paused mid-task for human review
- Track what's been done vs. what's pending

### The Task Tool — Subagent Delegation

The Task tool is the Agent SDK's mechanism for multi-agent coordination. An orchestrator agent calls the Task tool, specifying which subagent to invoke and what context to pass. The subagent executes in its own isolated session — separate conversation history, separate tool set, separate system prompt — and returns a result to the orchestrator.

This isolation is intentional and important. Subagents see only what they need. They can't accidentally act on information from another agent's context. Their results are returned cleanly rather than polluting the orchestrator's conversation with implementation details.

### Vaults — Credential Isolation

In production systems with multiple users, each user's credentials (GitHub tokens, Slack tokens, etc.) need to be isolated. Vaults store credentials per-user and are referenced by ID when creating sessions. The agent uses the vault to make authenticated calls, but the actual token never appears in the conversation or your application logic. This enables multi-tenant deployments where one agent deployment safely serves thousands of users.

---

## 3. Pattern 1: The Research Agent

**What it is:** A focused, stateless agent that investigates a specific question and returns findings. The simplest pattern — one model, one task, no state.

**When to use it:**
- Well-defined research tasks with a clear output format
- Tasks that don't need history from previous interactions
- Components of a larger multi-agent workflow (the orchestrator calls many research agents)
- Anything that benefits from parallel execution (multiple research agents running simultaneously)

**How it works:**

```
query(
  system: "You are a research specialist for [domain]. Return findings in [format]."
  message: "[specific research question]"
  tools: [search, fetch_url, read_file]
)
→ structured findings
```

The key design decisions:
1. **Specialize the system prompt** — a research agent for financial analysis behaves differently from one for security research. Narrow prompts produce more useful outputs than generic "research anything" prompts.
2. **Constrain with `allowed_tools`** — don't give the research agent write tools. It doesn't need them, and restricting access reduces the surface area for mistakes.
3. **Structure the output** — ask for output in a consistent format (XML, JSON, structured prose) so the orchestrator can reliably parse and compose results.
4. **Size to the question** — research tasks that fit in one `query()` call are cheaper and faster than sessions with full state overhead. Use sessions only when state actually matters.

**The pattern fails when:**
- The research requires iterative follow-up (use a session-based agent instead)
- The research task is too vague (refine the question before calling the agent)
- You try to pack multiple unrelated questions into one call (split into parallel calls)

---

## 4. Pattern 2: Chief-of-Staff Multi-Agent Orchestration

**What it is:** A coordinating orchestrator agent that routes tasks to specialized subagents via the Task tool. The orchestrator doesn't do the work — it decides who does the work and synthesizes the results.

**The analogy:** A chief of staff doesn't personally write every memo, run every analysis, or attend every meeting. They coordinate — assigning work to specialists, gathering results, and synthesizing a coherent picture for the decision-maker. The value is in the coordination, not the execution.

**When to use it:**
- Tasks that span multiple domains (financial analysis + legal review + PR assessment)
- Situations where different parts of the task require different tools or context
- When you want domain-specific expertise without a single monolithic agent
- When parallel execution would improve throughput

**Architecture:**

```
Orchestrator (Claude Opus)
├── System prompt: role awareness, delegation authority, synthesis responsibility
├── Tools: Task tool (for delegation), synthesis tools
└── Behavior: decompose → delegate → wait for results → synthesize

Subagent A (Claude Sonnet/Haiku)
├── System prompt: specialized for domain A
├── Tools: only domain A tools
└── Context: isolated — doesn't see other agents' work

Subagent B
├── System prompt: specialized for domain B
├── Tools: only domain B tools
└── Context: isolated — fresh session per invocation

...
```

**Key design principles:**

**1. Context isolation is a feature, not a limitation.** Each subagent gets its own conversation history. This means a subagent working on financial analysis can't accidentally be influenced by code review context from another subagent. It also means each subagent's conversation is smaller, faster, and cheaper.

**2. The orchestrator should not do domain work.** If you find your orchestrator writing code or analyzing financials, you've collapsed the pattern. The orchestrator's job is to decide *what* to delegate, *to whom*, and how to *combine* the results. Domain reasoning belongs in specialized subagents.

**3. Pass sufficient context in each delegation.** Subagents don't share memory. If Subagent B needs a result from Subagent A, the orchestrator must pass it explicitly. Design your delegation calls like API calls — they should be self-contained.

**4. Synthesize at the orchestrator level.** The orchestrator is responsible for reconciling results from multiple subagents, resolving conflicts, and producing the final coherent output. Don't have subagents call each other — keep routing centralized.

**Example decomposition for a hiring decision:**

```
Task: "Evaluate candidate John Smith for senior engineer role"

Orchestrator delegates:
├── Background check agent    → flags, employment history
├── Technical assessment agent → code quality, depth of experience
├── Cultural fit agent         → communication style, team signals
└── Compensation agent         → market rate, budget constraints

Orchestrator synthesizes → hire/pass recommendation with rationale
```

Each of these runs in parallel. Each has only the tools it needs. The orchestrator combines four specialized analyses into one recommendation.

---

## 5. Pattern 3: Parallel Subagents with Model Tiering

**What it is:** A parent agent (typically Opus) generates specialized prompts and delegates to multiple child agents (typically Haiku or Sonnet) running concurrently via `ThreadPoolExecutor`. The parent synthesizes results after all children complete.

**Why this matters:** Most workloads that look like "one big job" are actually "many smaller, independent jobs." Processing 20 financial reports sequentially takes 20x as long and costs the same as processing them in parallel. If the reports are independent, there's no reason to wait.

The model tiering is the second optimization: Opus is expensive and powerful, good for synthesis and strategic reasoning. Haiku is cheap and fast, good for extraction and pattern matching. By using Opus to generate targeted extraction prompts and Haiku to execute them, you get Opus-quality problem decomposition with Haiku economics for the bulk of the work.

**How it works:**

```python
# Parent (Opus) generates specialized prompts for each document
specialized_prompts = opus_agent.query(
    "Generate a specialized extraction prompt for each of these financial reports. 
     Each prompt should focus on the metrics most relevant to Q-over-Q comparison."
)

# Spawn parallel Haiku workers
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [
        executor.submit(haiku_query, doc, specialized_prompts[i])
        for i, doc in enumerate(documents)
    ]
    results = [f.result() for f in futures]

# Parent (Opus) synthesizes
synthesis = opus_agent.query(f"Synthesize these {len(results)} analyses: {results}")
```

**When this pattern applies:**
- Document processing (PDFs, reports, records) — any corpus of independent items
- Multi-source research — pulling from different data sources simultaneously
- Parallel code analysis — reviewing multiple files or modules independently
- Batch extraction — pulling structured data from many similar unstructured sources

**Cost math:** 10 documents processed by Haiku in parallel costs ~1/15 of 10 sequential Opus calls, and completes in the time of one Haiku call instead of 10 Opus calls. For anything at scale, this pattern pays for itself quickly.

**Design considerations:**
- **Prompt specialization matters.** Generic prompts to workers produce generic results. The Opus-generated specialized prompts are what make Haiku workers produce analysis-quality output instead of generic summaries.
- **Size the worker pool to your rate limits.** `max_workers=10` is a common starting point. Watch for rate limit errors and tune accordingly.
- **Aggregate before synthesizing.** Return structured outputs from each worker (XML or JSON), aggregate into a single synthesis call, and let Opus reason over the structured set. Don't chain synthesis calls.
- **Handle failure per-worker.** If one worker fails, you shouldn't lose the entire batch. Wrap individual futures in try/except and accumulate errors alongside successes.

---

## 6. Pattern 4: Programmatic Tool Calling (PTC)

**What it is:** Instead of making tool calls through the standard request-response round trip, Claude is given access to a code execution environment and writes Python code that orchestrates tool calls directly. The code runs in a sandbox, applies conditional logic, and returns results.

**Why this is meaningfully different:** Standard tool calling works like this: model decides to call a tool → sends tool call to your server → your server executes → result goes back to model → model processes result → potentially calls another tool. Each round trip has latency and token cost.

PTC collapses this. The model writes code that says: "load this dataset, filter for records where expense > budget, and only call the budget API for those records." The code executes, the conditional logic runs locally, and the model sees filtered results instead of paying for API calls and tokens on irrelevant records.

**Example — expense audit:**

Without PTC:
```
Model → call get_all_expenses() → 500 expense records returned → model processes 500 records → 
calls check_budget(employee_id) 500 times → 500 round trips, 500 API calls
```

With PTC:
```python
# Model writes this code
expenses = get_all_expenses()
over_budget = [e for e in expenses if e['amount'] > e['budget_limit']]
return [check_budget(e['employee_id']) for e in over_budget]
# Only calls check_budget for the 12 employees actually over budget
```

**Latency and cost profile:**

| Metric | Standard Tool Calling | PTC |
|---|---|---|
| Round trips | One per tool call | One code execution |
| Filtering | At model level (expensive) | At code level (cheap) |
| Token cost | All results to model | Only relevant results |
| Latency | Additive per tool | Parallel in code |

**When PTC applies:**
- Filtering datasets before making targeted API calls
- Conditional tool logic (call tool A only if condition X, tool B if condition Y)
- Any workflow where most records/items don't need downstream processing
- Multi-step computations that don't benefit from model reasoning at each step

**When to stick with standard tool calling:**
- Each tool call genuinely requires model-level reasoning to decide what to do next
- The dataset is small enough that filtering overhead isn't worth the complexity
- You need interpretability of each decision (code execution is harder to audit than model reasoning)

---

## 7. Pattern 5: Semantic Tool Routing at Scale

**What it is:** Tools are stored with pre-computed embeddings of their descriptions. When an agent needs a tool, it queries the tool store semantically rather than having all tool definitions loaded in context. Only the relevant tools are loaded on demand.

**The problem it solves:** As tool catalogs grow, loading all tool definitions into context gets expensive fast. 100 tools × average 500 tokens per definition = 50,000 tokens of context just for tools — before any messages. At 1,000 tools, this becomes impractical.

Semantic routing inverts this: tool definitions live in a vector store, not in the context window. The agent calls a `tool_search` function with a query, and gets back the 3-5 most relevant tool definitions. Context stays small regardless of catalog size.

**How it works:**

```python
# Setup (one-time)
tools = load_tool_catalog()  # all 500+ tools
embeddings = embed([f"{t.name}: {t.description} Params: {t.params}" for t in tools])
vector_store = VectorStore(tools, embeddings)

# Runtime — Claude calls this tool when it needs to find a capability
def tool_search(query: str, top_k: int = 5) -> list[ToolDefinition]:
    query_embedding = embed(query)
    return vector_store.similarity_search(query_embedding, top_k)

# Claude's context only ever has ~5 tools loaded at once
# Instead of 500 tool definitions sitting unused
```

**Measured impact:**
- Context reduction: 90%+ vs. pre-loading all tool definitions
- Quality: tool selection accuracy comparable to pre-loading (often higher, because fewer irrelevant tools appear as candidates)

**Variation — deferred loading:** For smaller tool sets where you want to preserve prompt caching, you can describe tools in natural language in the system prompt (without full parameter schemas) and load the full definition only when the tool is invoked. This preserves the cache hit on the system prompt while avoiding the full definition weight in context.

**When to use semantic routing:**
- Tool catalogs with 20+ tools
- Multi-domain systems where different tasks use entirely different tool sets
- Any system where context cost is a primary concern

**When deferred loading is sufficient:**
- 10-30 tools where most calls need 5 or fewer
- When you want simpler implementation without a vector store
- When tool descriptions are already in the system prompt for discoverability

---

## 8. Pattern 6: Evaluator-Optimizer Loop

**What it is:** Two agents in a feedback loop — a generator that produces output and an evaluator that assesses quality and provides structured improvement guidance. The loop runs until the evaluator signals PASS or a max iteration count is reached.

**The pattern:** This is quality enforcement through structure rather than prompt hoping. Instead of "write good code" followed by "is this good? try again," you have a formal contract: the generator produces, the evaluator provides specific critique, the generator incorporates it, and the loop closes.

```
Generator Agent                    Evaluator Agent
├── Produces initial output   →    ├── Assesses against criteria
                                   ├── Returns: PASS / NEEDS_IMPROVEMENT / FAIL
                                   └── If NEEDS_IMPROVEMENT: specific critique

← Generator incorporates critique  
└── Produces revised output   →    └── Re-evaluates

(repeat until PASS or max iterations)
```

**Key design decisions:**

**1. Evaluator criteria must be explicit.** A vague evaluator ("is this good?") produces vague feedback. The evaluator's system prompt should list the exact criteria it's assessing against, with examples of passing and failing outputs.

**2. Structured evaluation status prevents ambiguity.** Use discrete signals: PASS, NEEDS_IMPROVEMENT, FAIL. Don't use free-text pass/fail — parseable states allow the loop to make deterministic decisions about whether to continue.

**3. The evaluator should have memory of prior attempts.** Providing the full iteration history lets the evaluator notice when the generator is looping (making the same mistake repeatedly) and escalate rather than continuing pointlessly.

**4. Cap iterations.** Every loop needs a hard exit condition. `max_iterations = 5` is a reasonable starting point for most tasks. At the cap, return the best output so far with the evaluator's outstanding critique attached.

**Where this pattern appears:**
- Code quality loops (write → review → revise)
- Prompt optimization (generate prompt → test against cases → refine)
- Document drafting (draft → editorial review → revise)
- SQL query generation (generate query → test execution → fix)

**Anti-pattern — infinite retry:** Don't run the loop until the evaluator passes without a cap. Some tasks have criteria that can't be fully satisfied (or the evaluator has a bug). Always cap, always return something.

---

## 9. Choosing Between Patterns

The patterns aren't mutually exclusive — they're composable. A chief-of-staff can delegate to parallel subagents that each use PTC internally. But starting with the right pattern for your use case matters.

**Decision framework:**

```
Is the task a single, well-defined question?
└── YES → Research Agent (query())

Does the task naturally decompose into independent domain chunks?
└── YES → Chief-of-Staff with specialized subagents

Are the chunks uniform and parallelizable (same task, many items)?
└── YES → Parallel Subagents with model tiering

Does the task involve filtering large datasets before targeted API calls?
└── YES → Programmatic Tool Calling

Is your tool catalog growing beyond 20+ tools?
└── YES → Semantic Tool Routing

Does the task require iterative quality refinement?
└── YES → Evaluator-Optimizer Loop
```

**Complexity signal:** If you find yourself building custom orchestration logic to handle something the SDK patterns already solve, you've likely chosen the wrong pattern. Fit the pattern to the task, not the task to the pattern.

---

## 10. Cost Optimization Across Patterns

A few cross-cutting cost principles that apply regardless of which pattern you use:

**Model tiering is the highest-leverage optimization.** Opus → Haiku cost difference is roughly 15×. Anything that doesn't require deep reasoning (extraction, classification, format conversion, pattern matching) should run on Haiku. Reserve Opus for synthesis, strategic decomposition, and judgment calls.

| Task type | Recommended model |
|---|---|
| Bulk extraction / pattern matching | Haiku |
| Structured output generation | Haiku or Sonnet |
| Code generation | Sonnet |
| Architecture decisions, synthesis | Opus |
| Judgment calls with ambiguity | Opus |

**Context isolation reduces cost per agent.** Subagents with isolated contexts don't inherit the full conversation history of the orchestrator. A subagent that needs 500 tokens of context costs 500 tokens — not 10,000 because it inherited the orchestrator's history.

**Parallel execution doesn't increase cost, only throughput.** Ten parallel Haiku calls cost the same as ten sequential Haiku calls, but complete in the time of one. For independent tasks, always parallelize.

**Semantic tool routing scales better than caching tool definitions.** Caching large tool definition lists helps but still burns context tokens on every call. Semantic routing keeps context small regardless of how the catalog grows.

---

## 11. Anti-Patterns

**Orchestrators that do domain work.** If the orchestrator is writing code, analyzing data, or doing anything other than coordinating, you've collapsed the pattern. It becomes a monolithic agent again, losing the specialization benefits.

**Shared context between subagents.** Subagents should not communicate directly or share a context window. Route everything through the orchestrator. Direct subagent communication creates coupling that makes the system hard to debug and reason about.

**No exit conditions on loops.** Every evaluator-optimizer loop needs a hard cap. Loops without caps can run indefinitely if the evaluator has a bug or the task has unsatisfiable criteria.

**Giving all subagents all tools.** Domain-specific agents should have domain-specific tools. A financial analysis subagent doesn't need file deletion tools. Restricting tools by agent role reduces risk and simplifies reasoning.

**Using Opus for everything.** The cheapest model that can reliably do the task is the right model. Using Opus for bulk extraction or classification is like using a surgeon to carry luggage — technically capable, but wasteful.

**Parallel without error handling.** `ThreadPoolExecutor` exceptions are swallowed unless you explicitly handle them. Wrap each future in try/except and accumulate errors alongside results so a single worker failure doesn't silently corrupt the aggregate.

**Sessions for stateless tasks.** Sessions have state management overhead. `query()` is cheaper and simpler for tasks that don't need history. Match the tool to the requirement.
