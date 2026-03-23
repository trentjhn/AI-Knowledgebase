# Tool Use

## Tool Design Principles

### Provide Usage Examples

JSON schemas define structural validity but can't teach *when* and *how* to use a tool. Add 1-5 concrete examples per tool.

**Example structure for a support ticket API:**
1. **Minimal** — title-only task (shows the floor)
2. **Partial** — feature request with some metadata (shows selective use)
3. **Full** — critical bug with all fields (shows the ceiling)

Use realistic data, not placeholders. Focus examples on ambiguity areas not obvious from schema alone.

**Results:** Internal testing showed accuracy improvement from 72% → 90% on complex parameter handling.

### Write Descriptions That Include "When NOT to Use"

Instead of "searches the database," specify what it handles vs. doesn't:

```markdown
### search_codebase
Use when: You need to find where something is defined or used
Parameters:
  - query (string): The search term
  - file_type (optional): Limit to specific extensions
Returns: List of matching file paths with line numbers

Do NOT use for: Reading file contents (use read_file instead)
```

The "Do NOT use for" section prevents common misuse patterns.

### Tool Names Should Be Self-Documenting

- Use domain-specific prefixes: `git_commit`, `git_push` (not `commit`, `push`)
- Avoid versioned names that confuse purpose: `finder_v2`, `search_tool_2`
- Overlapping tools need clear differentiation in descriptions

---

## Tool Selection

Tool selection is **prompt-driven reasoning**, not keyword matching. Models match tool names and descriptions to task requirements.

### Context-Driven Filtering

Reduce the visible tool pool to prevent overwhelm:
- **Role-based restrictions** — not every agent needs every tool
- **Dynamic discovery** — only load tool definitions when relevant
- **Skill activation** — load specialized tool sets on demand

**Rule of thumb:** More than ~50 tools degrades selection performance. Implement dynamic discovery or role-based filtering when approaching this threshold.

### Comparison Tables for Overlapping Tools

When similar tools exist, explicitly clarify boundaries:

| Tool | Use For | Not For |
|------|---------|---------|
| `read_file` | Full file contents | Searching for text |
| `search_codebase` | Finding definitions/references | Reading content |
| `grep_file` | Pattern matching within a known file | Finding which file |

---

## Tool Restrictions as Security Boundaries

Treat tool restrictions like production IAM: **deny-all by default, allowlist only what each subagent needs.**

### Role-Based Tool Assignment

| Agent Role | Tools | Rationale |
|-----------|-------|-----------|
| Reviewer/Analyzer | Read, Grep, Glob | Read-only safety |
| Test Runner | Bash, Read, Grep | Execution with verification |
| Builder/Implementer | Read, Edit, Write, Grep, Glob | Full modification |
| Orchestrator | Task, Read, Glob | Routing with minimal access |
| Scout/Explorer | Read, Grep, Glob, WebFetch | Discovery only |

**Tool restriction as forcing function:** When orchestrators use different tools than subagents, natural separation of concerns emerges. Read-only scouts *cannot* modify — they are architecturally forced to report.

**Anti-pattern:** Giving all agents full tool access "for flexibility." Permission sprawl compounds. Start restrictive and expand only when necessary.

---

## Tool Validation Before Execution

Validation is what separates fragile tool use from reliable tool use. Two layers are required: schema validation catches malformed calls, semantic validation catches dangerous ones.

### Schema Validation

Before invoking any tool, validate the model's generated parameters against the tool's JSON schema. If the model produces a wrong type, omits a required field, or passes an invalid enum value, catch it before the call rather than receiving a cryptic API error.

**Python — jsonschema:**
```python
import jsonschema

def validate_tool_call(tool_name: str, params: dict, schema: dict) -> tuple[bool, str | None]:
    try:
        jsonschema.validate(instance=params, schema=schema)
        return True, None
    except jsonschema.ValidationError as e:
        return False, f"Schema validation failed for '{tool_name}': {e.message} at {'.'.join(str(p) for p in e.path)}"
```

**TypeScript — zod:**
```typescript
import { z } from "zod";

const DateRangeSchema = z.object({
  start_date: z.string().datetime(),
  end_date: z.string().datetime(),
  timezone: z.enum(["UTC", "US/Eastern", "US/Pacific"]),
});

function validateToolCall(params: unknown): { valid: boolean; error?: string } {
  const result = DateRangeSchema.safeParse(params);
  return result.success
    ? { valid: true }
    : { valid: false, error: result.error.issues.map(i => `${i.path.join(".")}: ${i.message}`).join("; ") };
}
```

### Semantic Validation

Schema correctness doesn't mean the call is safe. A `file_read` call with path `../../../../etc/passwd` is schema-valid and semantically dangerous. Semantic validation checks whether the values make sense in context.

**Key checks to implement:**
- **Path containment**: assert `resolved_path.startswith(ALLOWED_ROOT)` before any file operation
- **SQL injection screening**: reject queries containing `--`, `DROP`, `; DELETE`, or UNION statements outside parameterized values
- **Date range coherence**: assert `start < end` before calling any time-series or reporting tool
- **URL allowlisting**: for HTTP tools, verify the target hostname is in an approved domain list
- **Numeric bounds**: reject obviously wrong values (`page_limit=100000`, `timeout_ms=-1`)

```python
def validate_file_path(path: str, allowed_root: str = "/workspace") -> tuple[bool, str | None]:
    import os
    resolved = os.path.realpath(path)
    if not resolved.startswith(os.path.realpath(allowed_root)):
        return False, f"Path '{path}' resolves outside allowed directory '{allowed_root}'"
    return True, None
```

### Returning Actionable Errors to the Agent

When validation fails, don't throw a raw exception — return a structured error the agent can act on. Agents that receive actionable errors correct their calls in the next step; agents that receive Python stack traces usually fail or loop.

**Effective error structure:**
```json
{
  "error": "ValidationError",
  "field": "date_range.end_date",
  "message": "end_date must be after start_date. You provided start=2024-03-15, end=2024-03-01. Please swap the dates or adjust the range.",
  "received": { "start_date": "2024-03-15", "end_date": "2024-03-01" }
}
```

**Ineffective (do not return this):**
```
Traceback (most recent call last):
  File "tools.py", line 47, in execute
    assert params["end_date"] > params["start_date"]
AssertionError
```

The error message should specify: (1) which field failed, (2) what the constraint is, (3) what was received, (4) how to fix it.

### Pre-Execution Dry Runs

For destructive tools (file delete, database write, API POST that modifies state), add a `dry_run=True` parameter. The dry run validates the call and describes what it would do without executing.

```python
def delete_records(table: str, where_clause: str, dry_run: bool = False) -> dict:
    # Validate first regardless
    validate_sql_where(where_clause)  # raises on injection patterns

    count = db.query(f"SELECT COUNT(*) FROM {table} WHERE {where_clause}").scalar()

    if dry_run:
        return {
            "dry_run": True,
            "would_delete": count,
            "table": table,
            "condition": where_clause,
            "message": f"Would permanently delete {count} rows from '{table}'. Call with dry_run=False to execute."
        }

    db.execute(f"DELETE FROM {table} WHERE {where_clause}")
    return {"deleted": count, "table": table}
```

The agent calls `dry_run=True`, confirms the planned action in its reasoning, then calls with `dry_run=False`. This turns single-step destructive calls into a review-then-commit pattern.

---

## Error Recovery and Retry Strategies

### Transient vs. Persistent Failures

Retry transient failures. Do not retry persistent failures — a retry loop against a 404 or 403 wastes budget without any chance of success.

**Error code classification:**

| Code | Type | Action |
|------|------|--------|
| 429 | Transient (rate limit) | Retry with backoff |
| 503 | Transient (service unavailable) | Retry with backoff |
| 504 | Transient (gateway timeout) | Retry with backoff |
| 401 | Persistent (invalid credentials) | Fail immediately |
| 403 | Persistent (permission denied) | Fail immediately |
| 404 | Persistent (resource not found) | Fail immediately |
| 400 | Persistent (bad request) | Fail immediately |

The distinction matters because the agent's response to each is different. Transient → wait and retry. Persistent → change approach, escalate, or use a fallback.

### Exponential Backoff with Jitter

```python
import random, time

def call_with_retry(fn, *args, max_attempts=4, base_wait=1.0, max_wait=60.0, **kwargs):
    TRANSIENT_CODES = {429, 503, 504}

    for attempt in range(max_attempts):
        try:
            return fn(*args, **kwargs)
        except ToolCallError as e:
            if e.status_code not in TRANSIENT_CODES:
                raise  # Persistent failure — don't retry
            if attempt == max_attempts - 1:
                raise  # Exhausted retries

            wait = min(base_wait * (2 ** attempt) + random.uniform(0, 1), max_wait)
            time.sleep(wait)
```

**Typical values:** `base=1s`, `max_wait=60s`, jitter=`random.uniform(0, 1)`, cap at 3-5 retries. The jitter prevents thundering herd when multiple agents retry simultaneously.

### Graceful Degradation

When a tool persistently fails, don't halt the agent — fall back to a simpler alternative where one exists. Design tools in tiers:

| Primary | Fallback | Fallback-Fallback |
|---------|----------|-------------------|
| `semantic_search` (vector DB) | `keyword_search` (SQL LIKE) | `file_read` on cached export |
| `database_query` | `file_read` on CSV snapshot | Return partial results with warning |
| `advanced_analytics` | `basic_statistics` | None — escalate to human |

The agent needs to know what alternatives exist. Include a `fallback_tools` field in your tool metadata so the retry handler can surface options automatically.

### Reporting Failure to the Agent

When a tool fails after all retries, return a structured failure report rather than raising an exception that halts the run:

```json
{
  "status": "failed",
  "tool": "semantic_search",
  "attempts": 4,
  "final_error": "503 Service Unavailable after 4 attempts over 45s",
  "alternatives": ["keyword_search", "file_read"],
  "recommendation": "Use keyword_search with the same query. It's slower but available. If results are insufficient, request a manual data export."
}
```

The agent receives this as a tool result, not an exception. It can reason about the alternatives and adapt its plan.

### Budget-Aware Retry

In multi-step agents, track remaining token/cost budget against the retry cost. An expensive tool that costs $0.08 per call shouldn't be retried 4 times if $0.25 remains in the session budget — that leaves nothing for the actual task.

```python
def should_retry(attempt: int, tool_cost_estimate: float, remaining_budget: float) -> bool:
    # Don't retry if retries would consume >50% of remaining budget
    projected_retry_cost = tool_cost_estimate * (attempt + 1)
    if projected_retry_cost > remaining_budget * 0.5:
        return False
    return attempt < MAX_RETRIES
```

---

## Scaling Tool Use

### Dynamic Tool Discovery

When tool schemas exceed ~10K tokens, defer tool definitions. Rather than loading all tool definitions upfront, search for relevant tools and expand definitions only when discovered.

**Problem example:** A typical MCP setup with multiple services (GitHub, Slack, Sentry, Grafana, Splunk) consumes ~55K tokens in schemas alone.

**Result:** 85% reduction in token usage while maintaining full tool library access, with improved selection accuracy.

**When to use:** Total tool definitions > 10K tokens. Always-available baseline: keep 3-5 frequently-used tools loaded.

#### The Core Algorithm

Dynamic discovery applies RAG to tool descriptions instead of documents. The steps:

1. At startup, embed all tool descriptions and store them in a lightweight vector store (in-memory is fine for fewer than 1,000 tools)
2. When the agent indicates it needs to call a tool (by describing its intent), extract that description and embed it
3. Retrieve the top-5 tool schemas by cosine similarity
4. Inject only those 5 schemas into the current context
5. The agent selects from those 5, or requests a different search if none fit

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class ToolRegistry:
    def __init__(self, tools: list[Tool]):
        self.tools = {t.name: t for t in tools}
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        # Embed all descriptions at startup
        descriptions = [t.description for t in tools]
        self.embeddings = self.model.encode(descriptions, normalize_embeddings=True)
        self.tool_names = [t.name for t in tools]

    def discover(self, intent: str, top_k: int = 5) -> list[Tool]:
        query_emb = self.model.encode([intent], normalize_embeddings=True)
        scores = (self.embeddings @ query_emb.T).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [self.tools[self.tool_names[i]] for i in top_indices]
```

#### The Meta-Tool: search_available_tools

The agent needs an escape hatch when the auto-discovered tools don't match what it needs. Provide a meta-tool that the agent can call to search the tool library by plain-language description:

```json
{
  "name": "search_available_tools",
  "description": "Search the available tool library when you need a tool but aren't sure what it's called. Describe what you need to do in plain language.",
  "parameters": {
    "query": {
      "type": "string",
      "description": "Plain language description of what you need to do. Example: 'send a Slack message to a channel'"
    },
    "max_results": {
      "type": "integer",
      "default": 5,
      "description": "Number of tool summaries to return"
    }
  }
}
```

The meta-tool returns tool names and one-line descriptions. The agent reviews summaries, requests the full schema for the tool it wants, and the system injects that schema into context.

#### Static vs. Dynamic: The Threshold

| Tool Count | Recommendation |
|-----------|----------------|
| < 15 tools | Static loading — embed + search overhead costs more than it saves |
| 15–50 tools | Dynamic discovery starts yielding gains; implement if token budget is constrained |
| > 50 tools | Dynamic discovery required; selection accuracy degrades with full static loading |

Below 15 tools, load everything upfront. Above 15-20, dynamic discovery consistently improves both token efficiency and tool selection accuracy because the model is no longer distracted by irrelevant schemas.

### Programmatic Tool Orchestration

For multi-step workflows requiring 3+ dependent tool calls: instead of sequential agent-to-tool interactions, generate code that orchestrates multiple tool calls in a sandboxed environment. Results process in-place rather than re-entering the agent's context.

**Result:** 37% token reduction on multi-tool workflows.

**When to use:**
- Multi-step workflows with 3+ dependent tool calls
- Parallel operations needing result filtering/transformation
- Large datasets that would overwhelm context if returned directly

---

## Skills as Meta-Tools

Skills are **temporary behavioral modifications** that change how the agent reasons about specialized domains — not actions the agent takes.

### Three Differences from Traditional Tools

| Aspect | Traditional Tools | Skills |
|--------|------------------|--------|
| **Mechanism** | Direct actions (read file, call API) | Injected instructions + permission changes |
| **Selection** | Algorithmic matching | LLM reasoning about descriptions |
| **Token Cost** | ~100 tokens per invocation | ~1,500+ tokens per invocation |
| **Purpose** | Execute specific operations | Specialize agent behavior |

### The Trade

Skills trade token overhead for contextual specialization. Rather than front-loading every skill instruction into the base prompt, skills use progressive disclosure — the agent discovers capabilities through metadata, then loads full instructions only when needed.

**Example flow:**
1. Agent sees skill metadata: "Python debugging skill available"
2. Agent encounters Python bug, invokes Skill tool with "python-debugging"
3. System injects debugging instructions + enables relevant tools (Bash, Read)
4. Agent now reasons with debugging strategies in context
5. After task completion, injected instructions expire

### Token Cost by Feature Type

| Feature Type | Tokens per Invocation | Primary Cost Driver |
|--------------|----------------------|---------------------|
| Traditional Tools | ~100 tokens | Call overhead |
| Skills | ~1,500+ tokens | Discovery metadata + execution context |
| Subagents | Full conversation history | Isolated context per subagent |
| MCP Servers | 10,000+ tokens | Rich integration schemas |

**Decision framework:**
1. How often will this be invoked? One-time → Tool. Weekly+ → Skill. Continuous → MCP.
2. Does the agent need to discover it autonomously? No → Tool. Yes → Skill or MCP.
3. Is context isolation valuable? Yes → Subagent. No → Tool/Skill.
4. How rich is the integration schema? Simple → Tool. Complex → MCP.

---

## Rich User Questioning

When clarification is needed before acting, use structured multi-option questions rather than open-ended text prompts.

**Core insight:** Users don't know what they want until they see the options. Showing 4 options with descriptions, trade-offs, and a recommended choice enables informed decisions.

**Structure:**
- 4 questions addressing different decision dimensions
- 4 options per question with rich descriptions
- Trade-offs and implications explicit
- Recommended option guides optimal choice

**Good fit:**
- Request admits multiple valid interpretations
- Choices meaningfully affect implementation approach
- Actions are difficult to reverse

**Poor fit:**
- Decisions are obvious from context
- Only one reasonable approach exists
- User already provided detailed requirements
