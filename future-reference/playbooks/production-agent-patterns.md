# Production Agent Patterns

**Sources:** Anthropic Claude Cookbooks — `managed_agents/CMA_gate_human_in_the_loop`, `CMA_operate_in_production`, `CMA_orchestrate_issue_to_pr`, `CMA_prompt_versioning_and_rollback`, `slack_data_bot` *(2025)*

> **Who this is for:** Teams moving agents from prototype to production. The patterns here address what breaks when you add real users, real credentials, real failure modes, and real time constraints.

---

## 1. Human-in-the-Loop (HITL) Approval Workflows

### The Core Problem

An autonomous agent shouldn't make all decisions independently. Some decisions are high-stakes, irreversible, or policy-sensitive. For these, the agent should identify the need for human judgment and pause — not fail silently or proceed anyway.

The design question is: *how do you pause an agent mid-task and resume it after a human decides?*

There are two patterns, one for development and one for production. They have different tradeoffs on simplicity vs. scalability.

### Pattern A — Synchronous (Development / Low-Frequency Decisions)

The agent calls a custom `escalate()` tool. Your application handles the escalation synchronously: prompt the human, wait for input, return the decision to the agent. The agent continues immediately.

```
Agent calls escalate(reason="Expense exceeds $10K threshold. Approve?", context={...})
→ Application receives event, prompts user
→ User decides: approve / reject / modify
→ Application returns decision to agent
→ Agent continues with decision incorporated
```

**When to use:**
- Development and testing — immediate feedback loop
- Low-volume workflows where you can afford to wait for human input
- CLI tools and internal scripts where a blocking prompt is acceptable
- When the human and agent are interactive in the same session

**Limitation:** Blocks the agent session until the human responds. Not viable if the decision might take hours or the system serves many concurrent users.

### Pattern B — Asynchronous (Production / Webhook-Based)

The agent calls the same `escalate()` tool, but instead of blocking, the session pauses and emits a webhook. Your application queues the escalation for human review asynchronously. When the human decides, your application resumes the session with the decision.

```
Agent calls escalate() → session pauses → webhook fires
→ Human review queue receives item (could be minutes or hours later)
→ Human decides
→ Application calls session.resume(decision=...)
→ Agent continues from where it paused
```

**When to use:**
- Production systems with human reviewers on their own schedule
- High-value or irreversible actions (deploys, financial transactions, data deletions)
- Multi-tenant systems where one agent deployment handles many users' workflows

**The calibration problem:** Too many escalation points → reviewers get fatigued and start rubber-stamping. Too few → the agent makes decisions it shouldn't. Calibrate by listing every action the agent can take, then marking which ones are high-stakes based on: irreversibility, cost, user impact, and policy sensitivity.

### What Makes a Good Escalation Tool

The `escalate()` tool should include:
- **Reason** — why the agent is escalating (specific, not "needs human review")
- **Context** — the relevant state the human needs to make a decision
- **Options** — what the human can decide (approve/reject/modify, or custom options)
- **Urgency** — whether the decision is time-sensitive

Without these, human reviewers are making decisions in the dark, which defeats the purpose.

---

## 2. Stateful Multi-Turn Workflow Orchestration

### The Problem

Complex agent tasks — "resolve this GitHub issue end-to-end," "migrate this database schema," "onboard this new user" — span many turns and many tools. They fail mid-way. They discover unexpected state. They need to recover gracefully rather than restarting from scratch.

Stateless agents can't do this well. A stateless agent that fails on step 7 of 12 either restarts from step 1 (expensive) or fails entirely (bad user experience).

### Session Filesystem Pattern

Store task state as files within the session filesystem. At each turn, the agent reads current state, does one increment of work, and writes updated state. If the session fails, it can be resumed by reading the state files.

```
Session filesystem:
├── task.md         ← overall goal and constraints
├── progress.md     ← what's been done, what's pending
├── context.md      ← discovered state (repo structure, schema, etc.)
└── errors.md       ← failures encountered and recovery actions taken
```

This makes the agent's work auditable and recoverable. You can inspect exactly where it failed and what it knew at that point.

### Mid-Chain Adaptive Recovery

When an action fails, the agent shouldn't just retry the same action. It should:
1. Read the actual error (not just check if it succeeded)
2. Update its model of the situation
3. Choose a recovery action based on the specific failure

Example: A deploy fails because a dependency isn't installed. A retry will fail again. The adaptive response is to install the dependency first, then retry. This requires the agent to interpret errors, not just observe success/failure.

Design principle: **error as signal, not just state.** Error messages contain information about what actually went wrong. Prompting agents to extract that information before choosing recovery actions produces better outcomes than simple retry logic.

### Multi-Tool State Management

Long-running tasks typically involve a mix of read tools (search, fetch, read file) and write tools (create file, call API, deploy). A useful pattern:
- **Investigation phase** — read-only tools only. Map the state of the world before changing anything.
- **Remediation phase** — write tools enabled. Execute changes based on what investigation revealed.
- **Verification phase** — read-only again. Confirm the changes had the intended effect.

This phase separation makes agents more predictable and easier to review. It also enables human checkpoints between phases for high-stakes operations.

---

## 3. Multi-Tenant Credential Management

### The Problem

In production, your agent serves many users. Each user has their own credentials — GitHub tokens, Slack tokens, payment credentials. These need to be:
- Isolated (user A's agent can't access user B's credentials)
- Auditable (you can see which user's credentials were used for each action)
- Revocable (if a user revokes access, the agent stops working for that user)
- Never in conversation context (tokens in the message history are a security risk)

### The Vault Pattern

Vaults are per-user credential stores. Users register their credentials once, and vaults assign them an ID. When creating an agent session for a user, you reference their vault ID — the session can use the credentials without the actual token appearing anywhere in the conversation.

```
User onboarding:
vault_id = vault.register(user_id, credentials={
    "github_token": "ghp_...",
    "slack_token": "xoxb-..."
})

Session creation:
session = agents.create(
    agent_id="...",
    vault_id=vault_id  # agent can use credentials, but token never enters conversation
)
```

**Audit trail:** Because credentials are referenced by vault ID rather than passed directly, every action the agent takes is traceable to a specific user's vault. This satisfies compliance requirements and makes debugging production issues much easier.

**Credential refresh:** Vaults handle token refresh automatically. If a user's OAuth token expires, the vault refreshes it without the agent needing to handle it. This removes a common source of production failures.

### Least-Privilege Tool Sets

Pair vault-based credentials with scoped tool sets. A user's GitHub vault ID should grant read/write access to their repos — but not delete access. A user's Slack vault ID should allow posting messages — but not deleting channel history.

Define tool sets per user role or permission level, not per agent. This way, the same agent can serve users with different permission levels by receiving different tool sets at session creation.

---

## 4. Prompt Versioning and Production Stability

### The Problem

Agents in production need to be updated — prompts improved, behaviors changed, edge cases handled. But naive prompt updates break active sessions. Users in the middle of a task suddenly have a different agent behavior, often at the worst possible moment.

### Server-Side Prompt Versioning

Store prompts server-side with immutable version numbers. Production sessions reference a pinned version:

```python
# Development: update freely
agents.update("my-agent", system_prompt="improved instructions...")
# → returns version: 47

# Production sessions: pin to tested version
session = agents.create(
    agent_id="my-agent",
    version=46  # known-good version from last week
)
```

**What this enables:**
- Active sessions continue on their pinned version — no mid-task behavior changes
- New sessions start on the latest version
- Rollback is a version number change, not a code deployment
- Canary testing: route 5% of sessions to version 47, compare quality metrics

**Deployment decoupling:** One of the most important production stability principles for agents is decoupling prompt iteration from code deployments. Prompts change frequently (often daily during active development). Requiring a code deployment for every prompt change is a bottleneck that slows iteration and increases deployment risk.

Server-side versioning means prompts are first-class configuration, not code. Prompt engineers can iterate on prompts without touching deployment pipelines.

### Canary Testing Prompts

New prompt versions should roll out gradually:
1. Version 47 passes offline evals (test set from `eval-harness` skill)
2. Route 5% of sessions to v47, 95% to v46
3. Compare: task completion rate, error rate, user satisfaction
4. Roll forward if v47 wins, roll back if it doesn't

Never roll a new prompt version to 100% of production without canary data. This is the same discipline as gradual feature rollouts, applied to prompts.

---

## 5. Real-Time Platform Integration (Event-Driven Agents)

### The Pattern

Some agents need to respond to external events: a Slack message arrives, a GitHub issue is filed, a monitoring alert fires. These agents are driven by webhooks and must respond within tight timing constraints.

**The Slack bot architecture** is the canonical example:
```
Slack sends event → your webhook receives it → you ack within 3 seconds
→ Start agent session in background thread
→ Stream agent responses back to Slack as they arrive
→ Session terminates when task completes
```

The 3-second ack requirement is hard. If you start the agent synchronously in the webhook handler, you'll time out. The pattern is: ack immediately, process in a background thread.

### Session Persistence Across Events

For chatbot-style integrations where a user expects to continue a conversation across multiple messages, you need to persist the session ID and resume it when the next message arrives.

```
Message 1 → create session → session_id → store in {user_id: session_id} map
Message 2 → look up session_id by user_id → resume session → continue conversation
```

Session persistence is what separates a stateful assistant from a stateless chatbot. Without it, every message starts a new session and the agent has no memory of what was discussed.

### Streaming to External Systems

When an agent session produces output over multiple turns, you often want to relay that output to the user incrementally rather than waiting for the session to complete. The SDK emits `message.delta` events that you can forward to the external system as they arrive.

This is what makes agent responses feel responsive — users see output being generated rather than waiting for a long pause followed by a complete response.

---

## 6. When to Apply Which Pattern

| Situation | Pattern |
|---|---|
| Agent might make high-stakes decisions | HITL — start with synchronous, move to webhook for production |
| Task spans many tools and might fail mid-way | Stateful orchestration with session filesystem |
| Multiple users, each with their own credentials | Vault pattern + scoped tool sets |
| Prompts need iteration without breaking active users | Server-side prompt versioning |
| Agent responds to external events (Slack, GitHub, alerts) | Event-driven with background threads + session persistence |
| All of the above, in production | All of the above, combined |

These patterns compose. A production agent often needs: vaults (for credentials), prompt versioning (for stability), HITL webhooks (for risky actions), and stateful orchestration (for complex tasks). Don't implement them all at once — sequence them by risk:

1. Vault + tool scoping (security baseline)
2. Prompt versioning (stability)
3. Stateful orchestration (reliability)
4. HITL (governance)
5. Event-driven integration (reach)

---

## See Also

- `LEARNING/AGENTS_AND_SYSTEMS/agent-sdk/agent-sdk.md` — SDK patterns (research agent, chief-of-staff, PTC, semantic routing)
- `LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md` — conceptual patterns (orchestrator, ReAct, expert swarm)
- `future-reference/playbooks/multi-agent-orchestration.md` — agent team topologies
- `future-reference/playbooks/building-ai-agents.md` — end-to-end agent build guide
