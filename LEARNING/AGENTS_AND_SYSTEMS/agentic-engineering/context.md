# Context Management

## Core Mental Model

Context is the agent's working memory — ephemeral, finite, and the single biggest determinant of output quality.

**Key beliefs:**
1. **Context is capability.** An agent at 20% context has more room to think than one at 80%.
2. **Quality over quantity.** What's in the context matters more than how much. High-signal context outperforms high-volume noise.
3. **Fresh starts are cheap.** When in doubt, boot a new agent. Salvaging a degraded context is almost never worth it.
4. **Injection for priming, retrieval for discovery.** Inject what the agent *must* know upfront. Let it retrieve what it *might* need.
5. **One agent, one task.** If a task balloons, kill and rescope rather than push through.

**The Pit of Success framing:** Does the agent's current context increase the likelihood that the next generated token will be correct and aligned with the task? If not, it shouldn't be there.

---

## Context vs. Memory

**Context** is ephemeral working memory — lives in the active window, dies with the session.

**Memory** is persistent knowledge — survives restarts, shared across sessions — but requires external storage mechanisms (databases, files). Agents don't have memory by default.

**The key architectural implication:** Trying to reconstruct state from context each session is expensive and error-prone. Trying to persist everything as state creates sync issues. Know which one you need.

### Memory Storage Options

Where you store persistent memory determines your retrieval options, latency profile, and failure modes. Match storage to scale and use case:

**In-memory (ephemeral session memory)**
- Suitable for: single session, development, low-volume
- Implementation: Python dict or dataclass, cleared on session end
- Cost: zero
- When to use: when you only need memory within one agent run

**File-based (durable, simple)**
- Suitable for: single-user tools, development, low-concurrency agents
- Implementation: JSON files, one per memory type (`facts.json`, `preferences.json`, `events.json`)
- Cost: negligible
- When to use: personal tools, CLI agents, testing
- Key risk: file locking in concurrent access — use atomic writes (write to temp file, rename)

**SQLite (durable, queryable, local)**
- Suitable for: single-machine agents with structured memory needs, local-first applications
- Implementation: standard Python `sqlite3`, tables per memory type, full SQL queries for retrieval
- Cost: negligible
- When to use: when you need structured queries ("find all preferences set in the last 7 days"), or when file-based JSON becomes unwieldy
- Advantage over files: ACID transactions, no corruption risk from partial writes, efficient queries

**Vector database (semantic retrieval at scale)**
- Suitable for: large memory corpora, multi-user systems, semantic retrieval requirements
- Options: Pinecone (managed), Weaviate (open-source), Chroma (lightweight local), pgvector (Postgres extension)
- When to use: when you need "find memories semantically similar to this query" rather than exact key lookup
- Trade-off: adds embedding step at write time and retrieval step at read time — significant latency overhead vs. direct lookup

**Redis (fast, expiring cache)**
- Suitable for: high-frequency access patterns, short-term memory with TTL, session state
- When to use: when you need sub-millisecond memory retrieval, or when memory should expire automatically (e.g., session memory that clears after 24 hours)

### Retrieval Strategy by Memory Type

| Memory Type | Retrieval Pattern |
|-------------|------------------|
| Always-relevant (user name, persistent preferences) | Load at session start, keep in context throughout — no retrieval needed |
| Episodic (past events, history) | Retrieve on demand via semantic search or time-based query ("events from last 7 days related to X") |
| Facts and knowledge | Embed the current query, find semantically similar stored facts |

**The multi-tier pattern:** Maintain all three strategies simultaneously. Always-relevant memory loads statically at session start; episodic and factual memory retrieve dynamically as needed. This keeps baseline context small while making the full memory corpus available.

### Memory Consistency in Multi-Agent Systems

When memory is shared across agents, write conflicts are the primary failure mode:

- **Simplest approach — one writer, many readers:** Only the orchestrator writes to shared memory; sub-agents read. No write conflicts, easy to reason about.
- **When multiple agents must write:** Route all writes through a dedicated memory manager agent via a message queue (Redis Streams, RabbitMQ). The queue serializes writes and prevents corruption.

---

## Capability Degradation Thresholds

Context fill correlates with capability drain:

| Context % Used | Status |
|----------------|--------|
| 0-30% | Healthy operation |
| 30-60% | Good checkpoint for intentional compaction |
| 60-80% | Consider fresh session at natural task boundaries |
| 80-95% | Begin graceful wrap-up |
| 95%+ | Boot new agent immediately |

**Not linear:** There may be capability cliffs at certain thresholds. Practice: treat 40% as a caution point.

**Context type matters more than context volume.** 30% filled with logging output vs. 30% filled with exemplary code from the relevant domain produces dramatically different capability — even at the same utilization level.

---

## Context Strategies

### Frequent Intentional Compaction (General Coding)

Proactive compression at 40-60% rather than reactive emergency compression at 95%.

**Why emergency compression fails:** Reactive summarization at critical thresholds produces "brevity bias" — progressive collapse toward short, generic prompts that discard domain-specific information.

### Structured Context Beats Prose

Markdown, JSON, and XML consistently outperform unstructured prose:
- Provide focus mechanisms for the model
- Enable reliable parsing
- Assist prompt engineering (structure cues what matters)

---

## Advanced Context Patterns

### Progressive Disclosure

Load information in tiers rather than all at once. Enables effectively unlimited expertise within fixed context budgets.

**Three tiers:**
1. **Metadata first** — Names, descriptions, summaries (~50-200 chars per item)
2. **Full content on selection** — Complete documentation when chosen (~500-5,000 words)
3. **Detailed resources on-demand** — Supporting files, source code (unbounded)

**Token economics example:** 10 items × 1,000 tokens each = 100k tokens (eager loading) vs. ~5k tokens (metadata + one activated item) with progressive disclosure.

**When to use:**
- Large knowledge bases where most content won't be needed
- Multi-domain expertise where the agent needs awareness but not full activation
- Tight context budgets requiring capability breadth

**When not to use:**
- Small, static knowledge sets (eager loading simpler)
- Guaranteed access patterns (you know what's needed)
- Latency-critical paths (additional tool calls unacceptable)

### Context Loading vs. Context Accumulation

| Accumulation (Default) | Loading (Payload Model) |
|------------------------|-------------------------|
| "What has accumulated?" | "What must I include to succeed?" |
| Context as a log (append-only) | Context as a payload (constructed fresh) |
| Grows over time, compresses when full | Precise, purpose-built for each call |

**The payload model:** For this specific call, load: base config + project context + tool definitions (only what this agent needs) + query + retrieved facts. Nothing else.

**Why this is counterintuitive:** Standard patterns treat context as a log. Loading treats it as a precision instrument. This is how small models work in orchestrator patterns — the orchestrator handles accumulation; scouts receive curated loads.

### When to Use Each Model

**Use the Payload Model** (fresh context each call) when:
- Tasks are largely independent — each call doesn't depend on the specifics of what came 20 steps earlier
- Context bloat is causing quality degradation in longer sessions
- You need clean reproducibility for debugging (fresh load = deterministic input)
- The agent rarely needs to refer back to early-session decisions

**Use Accumulation** when:
- Tasks are deeply sequential and each step builds on the last
- The agent frequently needs to refer to decisions made early in the session
- The session is short enough that context bloat won't occur

**Migration signal:** If you're running an accumulation system and output quality degrades as sessions get longer, that's the signal to switch to the Payload Model with explicit state files. The state files take over the persistence job that accumulation was doing implicitly.

### ACE Framework (Agentic Context Engineering)

The ACE framework challenges "shorter is always better." In knowledge-intensive domains, contexts should **grow** — comprehensive evolving playbooks outperform compressed prompts.

**Three roles:**
1. **Generator** — executes tasks using current playbook
2. **Reflector** — analyzes outcomes, extracts learnings
3. **Curator** — evolves the playbook based on reflections

**Playbook format (itemized with metadata):**
```markdown
## Authentication Patterns

- [AUTH-001] Use JWT tokens for stateless sessions
  Helpful: 12 | Harmful: 1

- [AUTH-002] Validate tokens on every API call
  Helpful: 15 | Harmful: 0
```

**Grow-and-Refine cycle:**
1. Growth phase: Add new learnings. Don't prune yet.
2. Refinement phase: Semantic deduplication. Remove contradicted patterns.

**Performance:** +12.5% on AppWorld benchmark, 82.3% latency reduction vs. GEPA. (Larger, well-structured contexts actually execute faster — the generator doesn't need to rediscover patterns.)

**When to use ACE:**
- Knowledge-intensive domains (medical, legal, scientific)
- Complex tool use where learned patterns accumulate
- Long-running projects spanning many sessions

**When not:** Simple QA, fixed-strategy problems, short-lived tasks.

---

## Multi-Agent Context

### Context Isolation Pattern

Each subagent maintains its own separate context window. Rather than sharing a massive context, subagents work in isolation and return only synthesized, relevant information to the orchestrator.

**Why it works:**
- Prevents context pollution (one agent's research doesn't bloat another's working memory)
- Enables true parallelism (simultaneous, independent processing)
- Natural compression (synthesis happens at the boundary)
- Predictable quality (each agent starts fresh with focused context)

**The cost:** ~15× more tokens than single-agent approaches. Token usage explains 80% of performance variance in multi-agent systems. The value is **deterministic quality**, not speed.

### Explicit Forking

`context: fork` in frontmatter provides declarative context isolation:
```yaml
---
name: isolated-researcher
description: Research task with fresh context
context: fork
tools: Read, Grep, Glob, WebFetch
---
```

- Sub-agent starts with a fresh context window
- No conversation history from parent carries over
- Results return to parent as synthesized summary

### Persistent State vs. Ephemeral Context

| Ephemeral Context | Persistent State |
|------------------|-----------------|
| Single session | Survives restarts |
| One agent's working memory | Shared across agents/sessions |
| Cost: tokens | Cost: storage + retrieval |
| Failure mode: context rot | Failure mode: stale data |

**What belongs where:**
- **Context:** Current task details, recent tool outputs, working hypotheses, intermediate reasoning
- **State:** User preferences, conversation history, accumulated knowledge, learned corrections

**Google ADK state prefixes (elegant scoping pattern):**

| Prefix | Lifetime | Use Case |
|--------|----------|----------|
| `session:` | Current conversation | Working memory, intermediate results |
| `user:` | Across sessions | Preferences, accumulated knowledge |
| `app:` | Application-wide | Shared configuration, global state |
| `temp:` | Single turn | Scratch space, discardable |

### Memory Architectures for Multi-Agent Systems

**Shared Pool** — All agents access a common memory store. Fast knowledge reuse, but **memory contamination** risk: incorrect information from one agent propagates as "ground truth."

**Local with Synchronization** — Each agent owns private memory, sharing via periodic sync. Isolation by default, fewer contention issues. Scales better than shared pools.

**Event Bus** — Agents communicate asynchronously via structured events. Maximum decoupling, but requires disciplined event schema governance.

**The Two-Tier convergence:** Production systems consistently separate short-lived operational context from long-lived knowledge (separate files, different storage backends) even when using entirely different implementations.

**Fresh context as strategy:** Starting every session with empty context is a deliberate design choice, not a limitation. Prevents accumulation of stale assumptions when paired with reliable external state. Cheaper to reload clean context than debug degraded reasoning.
