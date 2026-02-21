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

## Scaling Tool Use

### Dynamic Tool Discovery

When tool schemas exceed ~10K tokens, defer tool definitions. Rather than loading all tool definitions upfront, search for relevant tools and expand definitions only when discovered.

**Problem example:** A typical MCP setup with multiple services (GitHub, Slack, Sentry, Grafana, Splunk) consumes ~55K tokens in schemas alone.

**Result:** 85% reduction in token usage while maintaining full tool library access, with improved selection accuracy.

**When to use:** Total tool definitions > 10K tokens. Always-available baseline: keep 3-5 frequently-used tools loaded.

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
