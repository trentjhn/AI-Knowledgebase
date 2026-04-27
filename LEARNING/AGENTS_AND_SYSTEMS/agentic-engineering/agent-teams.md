# Claude Code Agent Teams

> **Status:** Experimental. Requires Claude Code v2.1.32+. Disabled by default.
> **Source:** Official Anthropic Claude Code documentation, April 2026.

---

## What It Is

Most AI agent architectures work like a manager and staff: one central agent delegates work, workers report back, and everything flows through a single point of control. Even sophisticated multi-agent systems — orchestrators, subagent hierarchies, pipelines — preserve this hub-and-spoke structure. The hub has all the context; the workers have almost none.

Claude Code Agent Teams breaks this pattern. Instead of one session controlling many workers, it coordinates multiple *peer sessions* — each with its own context, its own conversation, its own terminal. The relationship is horizontal. Teammates can message each other directly. They share a task list and claim work autonomously. No single agent holds all the context; instead, findings are communicated across a network.

The analogy: the difference between a manager fielding all client questions and routing them to appropriate staff (the hub model) versus a cross-functional team where engineers, designers, and product owners communicate directly based on what each person needs to know.

---

## Why It Matters: The Problem It Solves

Section 15 of this KB describes "Multi-Agent Shared Context & Query Routing" as a frontier problem — one of the hardest unsolved challenges in multi-agent systems. The core difficulty: agents with isolated context windows need shared knowledge, but giving every agent full access to everything is too expensive and noisy, while selective retrieval introduces its own failures (agents don't know what they don't know).

Agent Teams doesn't solve the retrieval problem directly. Each teammate still has its own isolated context window, and knowledge doesn't flow automatically between them. What it provides instead is *communication infrastructure*: a mailbox system, a shared task list, and idle notifications so teammates can push relevant findings to each other deliberately rather than trying to pull context they might not know to ask for.

The practical effect is a different failure mode. In a pure retrieval architecture, agents miss context silently (they don't know what they failed to retrieve). In an agent team, agents can explicitly communicate findings, challenge each other's conclusions, and surface contradictions that no single agent working alone would have caught.

---

## Architecture

### The Four Components

**Team lead** — The Claude Code session that creates the team, spawns teammates, and coordinates overall direction. The lead is not a passive orchestrator; it can work on tasks itself, redirect teammates, and synthesize findings. The session that creates the team is the lead for its entire lifetime — this is fixed and cannot be transferred.

**Teammates** — Separate Claude Code instances, each running in its own context window. When spawned, a teammate receives a spawn prompt from the lead and loads project context automatically (CLAUDE.md, MCP servers, skills). It does *not* inherit the lead's conversation history. From that point forward, it operates independently.

**Shared task list** — Stored at `~/.claude/tasks/{team-name}/`. Three states: `pending → in progress → completed`. Tasks can have dependencies — a task won't be claimable until its dependencies are completed. File locking prevents race conditions when multiple teammates try to claim the same task simultaneously. The lead populates this list; teammates claim and complete items.

**Mailbox** — Push-based messaging between agents. When Teammate A sends a message to Teammate B, it arrives automatically — no polling required. The lead receives teammate messages automatically. Teammates can message any other teammate by name, or broadcast to all teammates simultaneously (though broadcast should be used sparingly — it scales token cost with team size).

### Storage

Both components are stored locally, not in the project directory:

- **Team config:** `~/.claude/teams/{team-name}/config.json` — Contains runtime state: session IDs, tmux pane IDs, team member names and agent IDs. Auto-generated and auto-updated. Never edit by hand; your changes will be overwritten on the next state update.
- **Task list:** `~/.claude/tasks/{team-name}/` — The shared work items the team uses to coordinate.

There is no project-level team configuration. A `.claude/teams/` file in your project directory is treated as an ordinary file, not as team configuration.

---

## When to Use

### The Fundamental Distinction

The decision between a single session, subagents, and agent teams maps to one question: **do your workers need to talk to each other?**

A single session handles everything through one context window. Use it when the task requires tight continuity — debugging a specific bug, writing code where later sections depend on earlier ones, iterating on a design. The coordination overhead of spawning other agents isn't worth it.

Subagents are disposable workers dispatched for side tasks. The parent session delegates something (research, verification, search), the subagent does the work, and the result comes back as a summary. The parent has all the context; the subagent has almost none. Use subagents when you need parallel execution and only the result matters — not the worker's reasoning process.

Agent teams are for parallel work where **cross-pollination improves the outcome**. When three researchers investigate the same question from different angles, the most valuable moment isn't when each one reports findings — it's when they compare notes and find contradictions. Agent teams enable that conversation to happen.

### Where Teams Add Genuine Value

**Research and synthesis with competing perspectives.** One teammate researches; another plays devil's advocate; a third checks practical implementation. They actively challenge each other. The surviving conclusions are more robust than any single agent would produce.

**Multi-layer technical work.** A system with independent frontend, backend, and infrastructure layers is a natural fit. Each layer has its own set of concerns, files, and decisions. Teammates can work in parallel because the coupling points are well-defined. The alternative — one agent handling all three sequentially — doesn't just take longer, it introduces context switching costs.

**Debugging with competing hypotheses.** When root cause is genuinely unclear, parallel investigation combats anchoring. Sequential investigation is biased: once a plausible explanation is found, subsequent work confirms rather than tests it. Multiple independent investigators actively trying to disprove each other's theories produce much stronger evidence.

**Multi-domain analysis.** Legal, technical, financial, and UX perspectives on the same decision. Market analysis of multiple competitors. Security audit with separate reviewers for different attack surfaces. When the same subject needs genuinely different lenses applied simultaneously, team exploration outperforms sequential single-agent analysis.

**Quality-gated pipelines.** Complex workflows where each phase has clear completion criteria and later phases genuinely depend on earlier phases completing first. Task dependencies in the shared task list encode this directly.

### Where Teams Don't Help

Agent teams add real overhead — coordination, token costs, communication complexity. They're counterproductive when:

- **Tasks are sequential.** If Step B requires Step A's output before it can start, parallel execution adds nothing. A single session handles this more efficiently.
- **Teammates edit the same files.** Two teammates modifying the same file will conflict. The architecture assumes each teammate owns a distinct domain.
- **Token budget is tight.** Each teammate runs its own context window. A 3-teammate team consumes roughly 3x the base tokens of a single session (more in plan mode — see Token Costs below).
- **Tasks are short.** Spawning teammates, distributing tasks, and coordinating results has fixed overhead. For a 10-minute task, that overhead isn't worth it.

### Decision Matrix

| Scenario | Recommendation | Reason |
|:---------|:---------------|:-------|
| Focused side task, result only matters | Subagent | Lower overhead, result summarized back |
| Sequential workflow | Single session | Coordination adds nothing |
| Same-file editing | Single session | Teammates conflict on shared files |
| Parallel work, no peer communication needed | Subagents | Cheaper, faster, result-focused |
| Parallel investigation needing cross-pollination | Agent teams | Peer messaging enables debate |
| Debugging with unclear root cause | Agent teams | Competing hypotheses stay independent |
| Multi-layer build (frontend/backend/tests) | Agent teams | Independent ownership per layer |
| Multi-domain analysis | Agent teams | Different lenses genuinely benefit |

---

## Setup

### Enable

Agent teams are disabled by default. Add to `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Or set in your shell environment:
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**Version requirement:** Claude Code v2.1.32 or later. Check with `claude --version`.

### Display Modes

Two modes for viewing teammate activity:

**In-process** — All teammates run inside your main terminal. Use `Shift+Down` to cycle through teammates. Type to message the active session. `Ctrl+T` toggles the task list view. Press `Enter` to view a session; `Escape` to interrupt a turn.

**Split panes** — Each teammate gets its own pane. Click into any pane to interact directly. Requires tmux or iTerm2 with the `it2` CLI.

The default is `"auto"`: split panes if you're already running inside a tmux session, in-process otherwise.

To set a permanent default, add to `~/.claude.json`:
```json
{
  "teammateMode": "in-process"
}
```

To force in-process for a single session:
```bash
claude --teammate-mode in-process
```

**Split panes do not work in:** VS Code's integrated terminal, Windows Terminal, Ghostty. If you use any of these, use in-process mode.

---

## Controlling Your Team

### Creating a Team

Tell Claude in natural language. It reads the task, decides on team composition, and spawns teammates based on your description. You can be explicit:

```text
Create an agent team with 3 teammates:
- One researcher focused on [domain A]
- One researcher focused on [domain B]
- One skeptic whose job is to find flaws in the other two's reasoning
```

Or you can give Claude the task and let it determine the structure:

```text
Analyze this architecture proposal from three different angles and find the weakest assumptions.
```

To get predictable teammate names you can reference later, name them explicitly in your spawn instruction.

### Assigning Tasks

The lead creates and manages the shared task list. Two assignment approaches:

**Explicit assignment:** Tell the lead to give a specific task to a specific teammate.

**Self-claim:** After finishing a task, a teammate picks up the next unassigned, unblocked item from the shared list. This is the default behavior and scales well for larger workflows.

For complex tasks, ask the lead to break work into 5–6 tasks per teammate. This keeps everyone productive and lets the lead reassign work if someone gets stuck, without needing to spawn new teammates.

### Direct Messaging

Talk to any teammate directly without going through the lead:

- **In-process:** `Shift+Down` to cycle to a teammate, then type
- **Split panes:** click into the teammate's pane

You can give additional instructions, ask follow-up questions, or redirect an approach that isn't working.

### Require Plan Approval

For risky or complex tasks, require teammates to plan before implementing:

```text
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

The teammate works in read-only plan mode until the lead approves. If rejected, the teammate revises and resubmits. Once approved, implementation begins.

To influence approval criteria, give the lead explicit rules: "Only approve plans that include test coverage" or "Reject any plan that touches the database schema."

### Shutting Down

To shut down a specific teammate:
```text
Ask the [name] teammate to shut down.
```

The lead sends a shutdown request; the teammate can approve or reject with explanation. To clean up the full team:
```text
Clean up the team.
```

This removes shared team resources. **Always clean up through the lead, not through a teammate** — teammate cleanup may not resolve the team context correctly, leaving resources in an inconsistent state. Always shut down active teammates before running cleanup.

---

## Quality Gates: The Hook System

Hooks are the mechanism for enforcing process discipline programmatically. Three hook events fire specifically during agent team operation.

### `TeammateIdle`

**When it fires:** A teammate is about to go idle (finish its current work).

**The use case:** Preventing a teammate from stopping before it has actually completed its work. The most common pattern is requiring tests to run before a teammate can idle.

| Exit code | Effect |
|:----------|:-------|
| `0` | Teammate goes idle normally |
| `2` | Teammate continues working; stderr is fed back to the model as instruction |
| Other | Teammate goes idle; stderr shown to user only |

Input fields include `teammate_name` and `team_name`.

```bash
#!/bin/bash
# Example: require test runner output before idle
TRANSCRIPT=$(jq -r '.transcript_path' < /dev/stdin)
TOOL_CALLS=$(grep -o '"tool_name":"[^"]*"' "$TRANSCRIPT" | tail -20)

if ! echo "$TOOL_CALLS" | grep -q '"Bash"'; then
  echo "Run your test suite and verify it passes before finishing." >&2
  exit 2
fi
exit 0
```

There is also a `continue: false` JSON response option that stops the teammate entirely (matching the `Stop` hook behavior), for cases where the work should halt rather than continue.

### `TaskCreated`

**When it fires:** A task is being created via the `TaskCreate` tool.

**The use case:** Enforcing naming conventions, requiring task descriptions, or preventing tasks that violate your architecture from being created at all.

| Exit code | Effect |
|:----------|:-------|
| `0` | Task is created normally |
| `2` | Task creation is blocked; stderr fed back as feedback |
| Other | Task is created; stderr shown to user |

Input fields include `task_id`, `task_subject`, `task_description`, `teammate_name`, and `team_name`.

```bash
#!/bin/bash
# Example: require task descriptions
DESCRIPTION=$(jq -r '.task_description // empty' < /dev/stdin)

if [[ -z "$DESCRIPTION" ]]; then
  echo "All tasks require a description. Add one before creating." >&2
  exit 2
fi
exit 0
```

### `TaskCompleted`

**When it fires:** A task is being marked as completed.

**The use case:** Validating completion criteria before a task can be marked done, preventing blocked dependent tasks from unblocking prematurely.

| Exit code | Effect |
|:----------|:-------|
| `0` | Task is marked complete |
| `2` | Completion is prevented; stderr fed back as feedback |
| Other | Task is completed; stderr shown to user |

```bash
#!/bin/bash
# Example: require tests to pass before completion
TASK_ID=$(jq -r '.task_id' < /dev/stdin)
RESULTS_FILE="/tmp/task-${TASK_ID}-results.txt"

if [[ ! -f "$RESULTS_FILE" ]] || ! grep -q "tests passed" "$RESULTS_FILE"; then
  echo "Test suite must pass before this task can be marked complete." >&2
  exit 2
fi
exit 0
```

### Designing a Quality Gate System

The three hooks compose naturally:

- `TaskCreated` enforces *entry criteria* — what constitutes a well-defined task
- `TeammateIdle` enforces *process criteria* — required steps before finishing
- `TaskCompleted` enforces *exit criteria* — required evidence of completion

A complete quality gate system uses all three and defines what "done" means programmatically, rather than relying on each teammate's individual judgment.

---

## Context and Communication

### What Teammates Receive at Spawn

When spawned, a teammate automatically loads:
- CLAUDE.md from the working directory
- MCP servers configured in project or user settings
- Skills from project or user settings
- The spawn prompt from the lead

The lead's **conversation history does not carry over**. This is intentional — each teammate gets a clean context. The spawn prompt is the primary mechanism for giving teammates task-specific context. Keep spawn prompts focused; everything in them adds to the teammate's initial context budget.

### What Teammates Don't Get

Teammates do not have access to:
- The lead's prior reasoning or conversation
- Other teammates' context windows (only explicit messages they've received)
- CLAUDE.md from the lead's working directory if they're launched with a different cwd

The isolation is a feature: it prevents anchoring (teammates can't be primed by each other's preliminary conclusions) and enables genuine parallel exploration. It only becomes a limitation if you forget to include necessary context in the spawn prompt.

### Spawn Prompt Design

The spawn prompt is everything. Treat it like a system prompt for the teammate's entire session:

```text
Spawn a security reviewer teammate with the prompt:
"Review the authentication module at src/auth/ for security vulnerabilities.
Focus on token handling, session management, and input validation.
The app uses JWT tokens stored in httpOnly cookies.
Report findings with severity ratings (critical/high/medium/low)."
```

Include:
- What the teammate should focus on
- Relevant technical context they need (not everything — just what they need)
- Any constraints on their approach
- Expected output format

Don't include:
- The lead's prior conversation history
- Context from other teammates (they'll communicate directly if needed)
- Everything in CLAUDE.md (that loads automatically)

---

## Subagent Definitions as Teammate Blueprints

You can reference an existing subagent definition when spawning a teammate, allowing you to define a role once and reuse it in both subagent and agent team contexts:

```text
Spawn a teammate using the security-reviewer agent type to audit the auth module.
```

When a subagent definition runs as a teammate:
- **Honored:** `tools` allowlist (tool restrictions apply), `model` (model selection applies)
- **Not honored:** `skills` and `mcpServers` frontmatter (teammates load these from project/user settings, same as a regular session)
- **Always available:** Team coordination tools (`SendMessage`, task management tools) even if the tools allowlist restricts other tools

This means you can create role definitions that are genuinely reusable: the same `security-reviewer.md` definition works as a disposable subagent in single-session workflows and as a peer teammate in multi-agent workflows.

---

## Token Costs

Agent teams are meaningfully more expensive than single sessions. Understand the cost profile before committing to the architecture:

**Cost scaling:**
- Each teammate is a separate Claude instance with its own context window
- Token usage scales roughly linearly with team size at baseline
- Plan mode costs approximately **7x more than a standard session** — each teammate planning before implementing runs through full thinking cycles independently
- Broadcast messages cost proportional to team size (one broadcast = N messages)

**Cost controls:**
- Use Sonnet for teammates; reserve Opus for the lead on complex synthesis tasks
- Keep spawn prompts focused — they add to every teammate's initial context
- Keep teams small: 3–5 teammates handles the vast majority of workflows
- Clean up teams when done — active teammates consume tokens even when idle
- Prefer point-to-point messages over broadcasts unless all teammates genuinely need the information
- 5–6 tasks per teammate is the practical optimum — keeps everyone productive without excessive context growth per teammate

**Rate limit recommendations:** For teams of developers using Claude Code with Agent Teams, the per-user TPM recommendations from the costs documentation apply. Individual teammates may temporarily spike above the steady-state rate; budget accordingly.

---

## Limitations

These are current experimental constraints, not permanent design decisions. Architectural planning should account for them now:

**No session resumption for in-process teammates.** `/resume` and `/rewind` do not restore in-process teammates. After resuming a session, the lead may attempt to message teammates that no longer exist. Workaround: use split-pane mode when session recovery matters, or design workflows to be completable in a single session.

**Task status lag.** Teammates sometimes fail to mark tasks as completed, which blocks dependent tasks. If a task appears stuck, verify whether the work is actually done and update status manually or have the lead send a nudge. The `TaskCompleted` hook can add verification, but the hook itself can't force a mark-complete — it can only prevent premature completion.

**Shutdown can be slow.** Teammates finish their current request or tool call before shutting down. For tool-heavy tasks, this can take time.

**One team per session.** A lead can only manage one team at a time. Clean up the current team before starting a new one.

**No nested teams.** Teammates cannot spawn their own teams or teammates. The hierarchy is flat: one lead, N teammates. For hierarchical decomposition, each teammate can still use subagents internally within their own session — that capability isn't affected.

**Lead is fixed.** The session that creates the team leads it for its lifetime. There is no mechanism to promote a teammate to lead or transfer leadership if the lead's session becomes problematic.

**Split panes require tmux or iTerm2.** In-process mode works in any terminal. Split-pane mode is not supported in VS Code's integrated terminal, Windows Terminal, or Ghostty.

**Permissions set at spawn.** All teammates start with the lead's permission settings. If the lead runs with `--dangerously-skip-permissions`, all teammates do too. Individual teammate modes can be changed after spawning, but not configured per-teammate at spawn time.

---

## Troubleshooting

**Teammates not appearing after creation:** In in-process mode, they may already be running — press `Shift+Down` to cycle through active teammates. If you requested split panes, verify tmux is installed and in your PATH: `which tmux`.

**Too many permission prompts:** Teammate permission requests bubble up to the lead. Pre-approve common operations in your permission settings before spawning teammates.

**Teammates stopping on errors:** Check their output via `Shift+Down` in in-process mode or by clicking the pane. Either give direct instructions or spawn a replacement teammate to continue the work.

**Lead finishing early:** The lead may decide the team is done before all tasks are complete. Tell it explicitly to wait: `"Wait for your teammates to complete their tasks before proceeding."` You can also instruct it to delegate rather than work itself: if you notice it implementing directly instead of waiting for teammates, redirect it.

**Orphaned tmux sessions after team cleanup:**
```bash
tmux ls                             # List sessions
tmux kill-session -t <session-name> # Kill the orphaned one
```

---

## Multi-Agent Patterns That Actually Work in Production (2026 Update)

> **Source:** Cognition, *"What We've Learned from Building Multi-Agent Systems"* (Walden Yan, 2026), updating the original 2025 *"Don't Build Multi-Agents"* position after a year of production deployment.

After a year of running agent teams in production at enterprise scale, a narrower set of multi-agent patterns has proven itself. The original warning against parallel-writer swarms still holds; what changed is the discovery of a specific class of coordination structures that work reliably.

### The Core Principle: Writes Stay Single-Threaded

The strongest practical finding: **multi-agent systems work best when write actions stay single-threaded and the additional agents contribute intelligence rather than actions.**

The original 2025 argument was that parallel writers make implicit decisions — style, error handling, edge case treatment, code patterns — that inevitably conflict with each other. Production experience has confirmed this. Systems that deploy multiple write-capable specialists in parallel fragment decision-making in ways that produce incoherent output.

What *does* work is single-writer topologies augmented by other agents that:

- Review what the writer produced (without prior context)
- Escalate tricky sub-tasks to stronger models
- Coordinate scope across sequential children

This contradicts the "fleet of write-capable specialists" architecture promoted by some platform vendors. For most real software work, the single-writer-plus-auxiliaries pattern produces more coherent results than parallel writers — at lower coordination cost.

### Pattern: Clean-Context Code Review Loops

The counterintuitive finding: **code review loops work better when the reviewer has no prior context from the coder.**

At Cognition, Devin Review catches an average of 2 bugs per PR on PRs written by Devin itself. About 58% are severe (logic errors, missing edge cases, security issues). Critically, this only works when the coding and reviewing agents share no context beforehand.

Three reasons a clean-context reviewer outperforms a shared-context one:

1. **Context Rot.** Attention heads are finite. A coder that has spent hours reading the repo, running commands, and fixing errors has built up a long context where important details get diluted. The reviewer starts fresh and only sees the diff.
2. **Forced reasoning-backward.** Without the spec, the reviewer must reason from implementation to intent. This surfaces assumptions the coder made that the spec never explicitly required — including cases where the user's instruction itself was subtly wrong.
3. **No shared biases.** Putting the same model in both roles does not produce the tight self-agreement intuition suggests. Agents are systems performing based on their context; a clean context genuinely functions as an independent reviewer.

The communication bridge matters: the coder needs to filter the reviewer's findings against its broader context of user instructions, decisions, and scope. Without that filtering, the loop devolves into scope creep or ignoring valid user constraints.

### Pattern: Capability Routing ("Smart Friend")

The emerging cost structure — frontier models becoming too expensive for every tool call — motivates a different pattern: a faster/cheaper primary model that delegates to a stronger model for hard sub-tasks.

The architecture: expose the smarter model as a *tool* the primary model can call when it judges a situation is tricky enough to be worth the escalation.

Current state of the art (2026):

- **Works today** across strong models (e.g., routing between Claude and GPT as capability-specific experts — one debugs better, one handles visual reasoning better). This is less an escalation ladder and more a capability router.
- **Doesn't yet work** when the primary is meaningfully weaker than the secondary. The gap is not a prompting problem; it's a training problem. A weaker model doesn't reliably know when it's at its limits. Cognition reports that SWE-1.5 couldn't hold up as the primary against Sonnet-4.5, but a trained-for-collaboration SWE-1.6 closes enough of the gap to pay off.

Two tuning questions that matter:

1. How does the primary decide when to escalate? (Today's best 80/20: always make at least one call to the stronger model for evaluation; let it decide if there's trickiness the primary missed.)
2. What does the stronger model send back? If the primary's context is incomplete, the stronger model should ask for specific files or missed context, not invent theories. An over-scoped smart friend that surfaces unasked-for guidance based on the trajectory often produces more value than one that answers only what was asked.

### Pattern: Manager + Children, Not Unstructured Swarm

For work that spans more than a single session — a product feature across ten PRs, a migration touching a dozen services, a week of work — the shape that actually holds coherence is **map-reduce-and-manage**: a manager breaks work into pieces, children execute, the manager synthesizes and reports back.

What doesn't work: arbitrary networks of agents negotiating with each other ("unstructured swarms"). Cognition's direct take after trying both: unstructured swarms are a distraction.

The practical failure modes of manager-plus-children, all of which require dedicated context engineering to fix:

- Managers trained on small-scoped delegation default to being overly prescriptive, which backfires when the manager lacks deep sub-context.
- Agents assume they share state with their children when they don't.
- Cross-agent communication (a child messaging peers through the manager) doesn't happen by default because models haven't been trained in environments that require it.

Each of these is fixable with current models via prompting, but the fixes don't generalize well. The next generation of models is expected to start closing these gaps natively.

### How This Updates the Decision Matrix Above

The "When to Use" decision matrix earlier in this doc still holds, with one significant refinement: when deciding whether to use agent teams for *write-capable* work, the stronger default is to centralize writes through a single agent (the team lead or a designated writer) and use teammates as review, verification, planning, and escalation agents rather than parallel writers.

The teammates-as-parallel-writers pattern (e.g., one teammate owning the frontend, another the backend, another the tests) can still work — but *only* when ownership boundaries are genuinely clean and no teammate edits another's files. The moment those boundaries blur, fragmented implicit decisions degrade the output.

### The Open Problems

Cognition's summary of where the research frontier sits:

- **Weaker-primary-to-stronger-secondary escalation** — a training problem, not a prompting problem.
- **Cross-agent discovery surfacing** — how does a child agent surface a discovery that should change its siblings' work? No reliable pattern yet.
- **Context transfer without drowning the receiver** — the interface between agents is consistently the bottleneck.

All three reduce to the same underlying issue: *communication is the hard part of multi-agent systems, and it's under-trained in current models.*

---

## References

- Claude Code Agent Teams documentation (Anthropic, April 2026): Primary source
- Claude Code Hooks reference (Anthropic, April 2026): TeammateIdle, TaskCreated, TaskCompleted hook specifications
- Claude Code Costs documentation (Anthropic, April 2026): Token cost guidance for agent teams, rate limit recommendations
- Cognition, *"What We've Learned from Building Multi-Agent Systems"* (Walden Yan, 2026): Source for the 2026 update — writes-stay-single-threaded principle, clean-context review loops, capability routing, manager-plus-children pattern
- Cognition, *"Don't Build Multi-Agents"* (2025): Original position paper that the 2026 update revises
- See agentic-engineering.md Section 16 for conceptual placement within the multi-agent architecture framework
- See multi-agent-orchestration.md playbook for operational deployment patterns
