# Agentic Patterns

## Pattern Selection

**If unsure, start with Plan-Build-Review.**

| Task Characteristics | Primary Pattern |
|----------------------|----------------|
| Standard feature implementation | Plan-Build-Review |
| Complex multi-concern analysis | Orchestrator |
| Information-gathering with unknowns | ReAct |
| High-stakes irreversible operations | Human-in-the-Loop |
| Multiple independent domain tasks | Expert Swarm |
| Design decisions with competing tradeoffs | Multi-Agent Collaboration |

Patterns compose — orchestrators coordinate parallel Plan-Build-Review experts; Human-in-the-Loop gates fit naturally at phase transitions.

---

## Plan-Build-Review

**The default starting pattern.** Four phases: Research → Plan → Build → Improve.

### Why Research Matters First

"Bad research compounds exponentially" — foundational errors propagate throughout implementation. Research outputs should be **concrete artifacts with specific evidence**:

- Good: "Module X uses pattern Y (see lines 45-67 in file.py)"
- Bad: "The code probably does something with databases"

### Scale-Adaptive Execution

| Flow | When | Phases |
|------|------|--------|
| Quick Flow | Bug fixes, prototypes | Skip research/plan |
| Standard Flow | Typical features | Full 4 phases |
| Full Planning | New products | Extended research |
| Enterprise | Compliance-critical | Full + audits |

### Learning Loop

The Improve phase updates Expertise sections in Research/Plan/Build commands based on real-world outcomes, creating a self-improving cycle.

---

## Orchestrator Pattern

A main coordinator invokes specialized sub-agents, synthesizes their outputs, and manages workflow transitions. Hub-and-spoke architecture.

### Core Structure

```
Orchestrator (Main Coordinator)
├── Phase 1: Scout Agent (read-only exploration)
├── Phase 2: Planning Council (parallel domain experts)
│   ├── Architecture Expert
│   ├── Testing Expert
│   └── Security Expert
├── Phase 3: Build Agents (parallel, dependency-aware)
├── Phase 4: Review Panel (parallel experts)
└── Phase 5: Validation (execution)
```

### Critical Implementation Details

**Single-Message Parallelism:** All parallel agents MUST be invoked in one message for true concurrency. Sequential messages serialize execution.

```
# CORRECT: One message with multiple Task calls → concurrent
# INCORRECT: Sequential messages → serialized (10× slower)
```

**Spec File as Shared Context:** A single artifact flows through all phases. Scout finds it → planning creates it → builders reference it → reviewers check compliance against it.

**Phase Gating:** Mandatory prerequisites before phase transitions. If prerequisites fail, halt with remediation instructions.

**Context Isolation:** Each sub-agent gets a fresh context window. They return **synthesized summaries**, not raw data. This keeps the orchestrator's decision-making context clean.

### Capability Minimization

Tool restrictions aren't just security — they enforce architectural intent:

| Agent Role | Tools | Rationale |
|-----------|-------|-----------|
| Scout | Read, Glob, Grep | Cannot modify — forces reporting |
| Builder | Write, Edit, Read, Bash | Focused on implementation |
| Reviewer | Read, Grep, Bash (tests only) | Cannot fix findings |
| Validator | Bash (run only), Read | Executes without implementing |

### Communication

**Core identity:** "Absorb complexity, radiate simplicity." Never expose orchestration mechanics in user-facing output.

**Forbidden vocabulary:** "spawning subagents," "task graph analysis," "fan-out pattern," "map-reduce phase"

**Progress language:**
- Starting: "Breaking this into parallel tracks"
- Working: "Got several threads running"
- Synthesis: "Pulling it together now"

### Read vs. Delegate Threshold

- **Orchestrator reads directly:** 1-2 files (quick lookups, small configs)
- **Delegate to agents:** 3+ files (codebase exploration, pattern searching)

---

## ReAct Pattern (Reasoning + Acting)

Interleaved reasoning and acting: Thought → Action → Observation → Thought → ...

```
Thought: Analyze current state based on observations
Action: Select and invoke a tool
Observation: Record the tool's output
Thought: Analyze the new observation, decide next step
Action: Select next tool (or finish)
```

### Key Properties

1. **Grounded decisions:** Each action follows explicit reasoning about current observations. The model cannot claim to have information it hasn't retrieved.
2. **Observable traces:** The thought-action-observation chain creates a full audit trail.
3. **Adaptive behavior:** Each observation can redirect the plan. Unlike fixed multi-step plans, ReAct adjusts based on actual tool results.

### When to Use

**Good fit:**
- Information gathering requiring evidence (research, debugging)
- Unknown number of steps required
- Each step depends on what previous steps revealed
- Hallucination is high-risk (medical, legal, financial)
- Explainability matters (audit trails, user trust)

**Poor fit:**
- Well-defined procedures with known steps
- High-throughput scenarios where reasoning overhead is unacceptable
- Single-tool tasks (no interleaving needed)

### ReAct vs. Plan-Build-Review

| Aspect | Plan-Build-Review | ReAct |
|--------|-------------------|-------|
| Planning | Explicit, upfront | Implicit, emergent |
| Adaptability | Follows spec | Adjusts per observation |
| Best for | Complex multi-phase projects | Exploratory, information-gathering |

**Synthesis:** Use ReAct within the Research phase of Plan-Build-Review to discover information for planning.

### Anti-Patterns

- **Thought-free actions:** Always generate a Thought before every Action
- **Observation overload:** Limit observation size; summarize or truncate tool outputs
- **Infinite loops:** Limit maximum iterations (10-20); detect repeated actions; require explicit "Final Answer" action to terminate

---

## Human-in-the-Loop

Strategic insertion of human approval checkpoints to manage risk, ensure quality, and maintain oversight.

### Risk-Based Gate Criteria

| Risk Factor | Auto-proceed | Require Approval |
|-------------|-------------|-----------------|
| Reversibility | Git commit | Database migration |
| Blast radius | Single file | Production deployment |
| Sensitivity | Internal code | Credentials, payments |
| Precedent | Routine | First-time pattern |

**Always gate:** Production deployments, database schema changes, external API calls with side effects, credential changes, deleting data.

**Safe to auto-proceed:** Reading files, running tests (isolated environments), creating branches, generating documentation drafts.

### Gate Placement Strategies

**Pre-Action Gates:** Agent presents plan, waits for approval before execution. Best for irreversible operations.

**Post-Action Review Gates:** Agent executes, pauses for review before proceeding to next phase. Best for complex multi-step workflows where intermediate work is valuable.

**Checkpoint Gates (at phase transitions):** The recommended default. The spec file from planning serves as the approval artifact — humans review the spec, not raw code changes.

```
Research → [GATE: approve research findings]
         → Plan → [GATE: approve spec before implementation]
                → Build → [GATE: review before merge/deploy]
```

### Effective Approval Request Design

Must include: (1) Clear action statement, (2) Sufficient context, (3) Risk assessment with rollback plan, (4) Explicit options (not just approve/reject).

Every high-risk gate must include rollback plan. "No rollback plan = not ready for approval."

### Synchronous vs. Asynchronous Approval

**Synchronous (blocking):** Use for interactive sessions and high-stakes operations where delay is acceptable.

**Asynchronous (non-blocking):** Use for long-running workflows spanning hours/days. Requires workflow state management and resume capability.

### Anti-Patterns

- **Gate fatigue:** Too many gates → humans approve without reading. Reserve gates for genuinely high-risk operations.
- **Vague approval requests:** "Should I proceed?" without context → humans guess.
- **Missing rollback plans:** Approval with no recovery path.
- **Gates without audit trail:** Every approval needs timestamp, approver, decision, and modifications.

---

## Expert Swarm Pattern

Domain experts coordinate parallel workers that **inherit shared expertise**, achieving both scale and consistency.

### Core Structure

```
Expert Lead (domain expert with expertise.yaml)
    │
    ├─── expertise.yaml (single shared knowledge source)
    │
    ├─── Worker 1 (EXPERTISE_PATH: /path/to/expertise.yaml, Task: Section A)
    ├─── Worker 2 (EXPERTISE_PATH: /path/to/expertise.yaml, Task: Section B)
    └─── Worker N...
         │
    Join/Synthesis Phase (verify consistency, update indexes)
```

### Why Expertise Path-Passing Instead of Context Copying?

| Approach | Pro | Con |
|----------|-----|-----|
| Copy expertise into context | No file I/O | Pollutes context with 500-750 lines per worker; synchronization issues |
| Pass expertise path | Clean worker context; single source of truth | Requires file read |

**Path-passing keeps the orchestrator's context clean** while ensuring all workers reference the same knowledge source. When expertise.yaml updates, all future workers automatically benefit.

### Learning Separation (Critical)

Workers execute; **improve agents analyze afterward**.

**Why:** Allowing workers to update expertise during parallel execution creates race conditions. Sequential improve phase after swarm completion prevents conflicts.

```
Workers 1-10 execute (read-only access to expertise)
    ↓ Swarm completes → commit
Improve agent analyzes all 10 worker outputs
Improve agent updates expertise.yaml once
Next swarm benefits from all learnings
```

### Scale Evidence

10-agent swarm (commit 20500f1): 3,082 lines added, 7 files created, 15 modified, ~4 minutes wall-clock. Sequential estimate: 40 minutes. **10× speedup.**

Zero voice drift — all entries followed structure standards guided by shared expertise.yaml.

### Expertise File Governance

Target maximum ~750 lines for expertise.yaml to prevent context bloat. At 750 lines ≈ 3,000 tokens per worker, 10 workers = 30,000 tokens coordination overhead (manageable). Unbounded expertise.yaml breaks the pattern.

### When to Use Expert Swarm

**Good fit:** Multiple independent tasks within a single domain, well-documented expertise, consistency is critical, scale justifies overhead.

**Poor fit:** Simple single-file changes, tasks with sequential dependencies, domain expertise not yet codified.

---

## Multi-Agent Collaboration

Multiple specialized personas collaborate in a shared conversation space — agents respond to each other's ideas rather than executing in isolation.

### Core Pattern

```
User asks: "How should we handle authentication?"
    ↓
Orchestrator selects: Security Expert, Architect, Developer (2-3 agents per message)
    ↓
Security Expert: "Use OAuth2 with PKCE flow"
Architect: "Agree on OAuth2, but store tokens in Redis not localStorage"
Developer: "That adds Redis dependency — could we use httpOnly cookies?"
    ↓
User steers: "What about mobile apps?"
```

### Key Characteristics

1. **Selective participation** — orchestrator picks 2-3 relevant agents per message, not all agents
2. **Role authenticity** — agents maintain perspective (security experts worry about threats)
3. **Genuine disagreement** — agents disagree when perspectives conflict
4. **Building on ideas** — later responses reference earlier responses
5. **Human steering** — user guides direction at each turn

### When to Use

**Good fit:** Complex decisions with multiple tradeoffs, brainstorming and ideation, design reviews where different expertise matters, no single "right answer."

**Poor fit:** Execution tasks (code implementation), well-defined problems, simple enough that multiple perspectives add noise.

### Context Management

Multi-agent conversations consume context rapidly. Mitigation:
- Compressed history (pass only last 2-3 exchanges)
- Summary checkpoints (after 10 messages, summarize and start fresh)
- Agent-specific context (each agent sees conversation through their lens)

### Synthesis

After 5-10 rounds of dialogue, orchestrator must synthesize:
1. **Consensus points** — what all agents agree on
2. **Open tradeoffs** — what remains unresolved and why
3. **Recommendation** — proposed path forward
4. **Next steps** — concrete actions

### Anti-Patterns

- **All agents, every message** — creates noise and exhausts context window
- **Forced consensus** — real tradeoffs get hidden
- **Human passenger** — user watches without steering → conversation meanders
- **No synthesis** — exploration without resolution wastes effort

---

## Autonomous Loops (Ralph Wiggum)

Iteration-based pattern where the agent repeatedly attempts a task using git history as external memory, with fresh context per loop. Each iteration improves on prior attempts based on feedback signals (tests pass, lint clean, etc.).

**Best for:** Tasks with machine-verifiable success criteria, reversible operations, many small iterations.

**Contrast with Human-in-the-Loop:** Use autonomous loops when failure is acceptable learning data. Use HITL when human judgment is irreplaceable or operations are irreversible.

---

## Self-Improving Experts

Agents that update their own expertise sections based on execution outcomes. See [prompt-engineering.md: Level 6](prompt-engineering.md) for implementation details.

**Four-agent pattern:** Plan agent → Human approval → Build agent → Review agent → Learn/Improve agent.

---

## Progressive Disclosure Pattern

Tiered information loading to enable effectively unlimited expertise within fixed context budgets. See [context.md: Progressive Disclosure](context.md).

**In the context of patterns:** Use within orchestrators to manage domain knowledge — load category summaries first, expand specific sections when an expert activates.
