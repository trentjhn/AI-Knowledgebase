# Agent Skills

**Table of Contents**
1. [What Skills Are — and Why They Exist](#1-what-skills-are--and-why-they-exist)
2. [The Core Problem Skills Solve](#2-the-core-problem-skills-solve)
3. [Core Design Principles](#3-core-design-principles)
4. [Skills and MCP — How They Work Together](#4-skills-and-mcp--how-they-work-together)
5. [Anatomy of a Skill](#5-anatomy-of-a-skill)
6. [The YAML Frontmatter — The Most Important Part](#6-the-yaml-frontmatter--the-most-important-part)
7. [Writing Effective Instructions](#7-writing-effective-instructions)
8. [Three Categories of Skills](#8-three-categories-of-skills)
9. [Five Workflow Patterns](#9-five-workflow-patterns)
10. [Testing and Iteration](#10-testing-and-iteration)
11. [Distribution and Sharing](#11-distribution-and-sharing)
12. [Troubleshooting Common Failures](#12-troubleshooting-common-failures)
13. [Anti-Patterns](#13-anti-patterns)

---

## 1. What Skills Are — and Why They Exist

Imagine you hired a brilliant assistant who could learn any process you teach them. The catch: every morning, they wake up with no memory of yesterday. Every time you work together, you have to re-explain your preferences, your workflow, your style guide, your approval process from scratch. That's what working with an AI agent looks like without skills.

A **skill** is a portable folder of instructions that teaches an AI agent how to handle a specific task or workflow — and remembers that knowledge permanently, across every conversation, across different platforms, and for every user on your team. You teach it once; the agent applies it every time.

Technically, a skill is just a folder on your filesystem containing a required `SKILL.md` file (with a short header of structured metadata) and optional supporting files like scripts, reference docs, and templates. There's no code to compile, no server to run. It's closer to a well-written recipe than a software library.

Skills are an **open standard** — originally developed by Anthropic and adopted by a growing ecosystem of AI tools including Claude Code, Cursor, GitHub Copilot, Gemini CLI, and others. A skill you build today can work across all of these platforms without modification (as long as the platform supports the standard).

---

## 2. The Core Problem Skills Solve

Here's what happens without skills: a user connects an AI to their company's project management tool. The tool is connected, the AI can technically use it — but every conversation starts from scratch. The user has to explain "when you create a task, always add the team label, assign a due date two weeks out, and notify the #engineering channel." They explain this every single time. Different users explain it differently. Results are inconsistent. Users blame the tool when the real issue is missing workflow guidance.

With a skill, that institutional knowledge lives in a file. The agent loads it automatically when it's relevant, applies the workflow consistently, and new team members get the same quality output on their first day as a veteran user gets on their hundredth.

**The three situations where skills shine:**

- **Repeatable workflows** — Sprint planning, customer onboarding, document creation, code review. Any multi-step process you do more than once benefits from being captured in a skill.
- **Domain expertise** — Legal review checklists, financial compliance rules, brand voice guidelines, API best practices. Knowledge that would take paragraphs to explain every time can be embedded once.
- **MCP integrations** — When you give an agent access to a tool (via MCP, which stands for Model Context Protocol — a way of connecting agents to external services), a skill teaches the agent *how* to use that tool well, not just *that* it has access to it.

---

## 3. Core Design Principles

### Progressive Disclosure — Loading Only What's Needed

One of the most elegant ideas behind skills is that they don't load everything upfront. Instead, they use a three-level system designed to keep AI context windows lean:

**Level 1 — The YAML header** is always loaded in the agent's background instructions. It's tiny — just a name and a short description. The agent reads every skill's header silently, all the time, and uses it to decide: "Is any of this relevant to what the user just asked?"

**Level 2 — The SKILL.md body** only loads when the agent decides the skill is relevant. This is where the actual step-by-step instructions live. If you're asking about the weather, the sprint-planning skill stays quiet; its instructions never enter the context at all.

**Level 3 — Linked files** in the `references/` folder only load if the agent specifically needs them for the current task. Detailed API guides, templates, and reference docs stay dormant until the moment they're needed.

This design matters because AI agents have finite attention (their "context window") — the more instructions you load, the more diluted their focus becomes. Progressive disclosure means a skill library of 50 skills doesn't overwhelm the agent; it quietly waits until called upon.

### Composability — Skills Work Together

An agent can load multiple skills simultaneously for a single task. A skill shouldn't assume it's the only active one. If you're building a skill for data analysis, it should work harmoniously alongside a skill for creating reports, without the two conflicting or duplicating instructions.

### Portability — Build Once, Use Everywhere

Because skills are just files following an open standard, the same skill works identically across Claude.ai, Claude Code, and any other platform that supports the Agent Skills standard. The only exception: some skills rely on platform-specific capabilities (like running Python scripts), which the skill author can note in a `compatibility` field.

---

## 4. Skills and MCP — How They Work Together

MCP (Model Context Protocol) is a way of connecting an AI agent to external services — giving it access to your Notion workspace, your Linear board, your GitHub repositories, your internal databases. Think of MCP as the plumbing: it connects the agent to the kitchen.

Skills are the recipes: step-by-step instructions on how to actually cook something useful with those ingredients.

| MCP (Connectivity) | Skills (Knowledge) |
|---|---|
| Connects Claude to your service (Notion, Linear, Slack, etc.) | Teaches Claude how to use your service effectively |
| Provides real-time data access and tool invocation | Captures workflows and best practices |
| Answers: "What can Claude do?" | Answers: "How should Claude do it?" |

Without skills, MCP users often experience a frustrating gap: the connection works, but they don't know what to ask or how to ask it. They get inconsistent results. They write long prompts explaining their process every time. Skills fill that gap — pre-built workflows activate automatically based on what the user is asking for.

**When to build a Skill vs. an MCP**

The confusion usually comes from the fact that both feel like "extending what Claude can do." The distinction is simpler than it appears. Ask yourself two questions:

1. *Should Claude be able to call this anytime, across any context?* → Build an MCP. It's a capability that should always be available — like web search, or access to your database.

2. *Is this a repeatable multi-step workflow with defined steps?* → Build a skill. It's a procedure that should activate when a specific type of task comes up.

The signal that you need a skill: you notice yourself asking Claude the same multi-step sequence over and over. That repetition is exactly what a skill automates. The signal that you need an MCP: you need Claude to access an external system or service it currently can't reach.

A useful way to remember it: CLAUDE.md is your employee handbook (always-on context). Skills are training modules (activated for specific procedures). MCPs are the tools on the workbench (available capabilities to reach for).

---

## 5. Anatomy of a Skill

A skill is a folder. The folder name must be in `kebab-case` (all lowercase, words separated by hyphens, no spaces or underscores). Inside:

```
my-skill-name/
├── SKILL.md          ← Required. The heart of the skill.
├── scripts/          ← Optional. Python, Bash, JavaScript code.
│   └── validate.py
├── references/       ← Optional. Docs loaded on demand.
│   └── api-guide.md
└── assets/           ← Optional. Templates, icons, fonts.
    └── report-template.md
```

**Critical rules:**
- The file must be named exactly `SKILL.md` — case-sensitive. `skill.md` or `SKILL.MD` won't work.
- No `README.md` inside the skill folder. (Put that at the GitHub repo level if you're distributing publicly — it's for human visitors, not the agent.)
- No spaces or capitals in the folder name: `sprint-planner` ✅, `Sprint Planner` ✗, `sprint_planner` ✗
- Names containing "claude" or "anthropic" are reserved.

---

## 6. The YAML Frontmatter — The Most Important Part

Every `SKILL.md` starts with a block of structured metadata called YAML frontmatter — it's the section between the two `---` lines at the top of the file. This is Level 1 of the progressive disclosure system: it's always loaded, always visible to the agent, and it's how the agent decides whether to invoke the skill.

Getting this right is the single most important thing you can do.

**Minimal required format:**
```yaml
---
name: sprint-planner
description: Manages sprint planning workflows for engineering teams. Use when user says "plan a sprint", "create sprint tasks", "help with sprint planning", or asks about task prioritization and velocity.
---
```

The **`name`** field must match your folder name exactly: `kebab-case`, no spaces, no capitals.

The **`description`** field (maximum 1,024 characters) must answer two questions:
1. **What does the skill do?** (its capability)
2. **When should it be used?** (specific trigger phrases, scenarios, file types)

Agents tend to under-trigger — they err on the side of not loading skills unless they're clearly relevant. Write your description assertively, and include the actual phrases users would type.

**Good descriptions are specific and include triggers:**
```yaml
description: Analyzes Figma design files and generates developer handoff documentation.
Use when user uploads .fig files, asks for "design specs", "component documentation",
or "design-to-code handoff".
```

**Bad descriptions are vague or missing triggers:**
```yaml
description: Helps with projects.
# Or:
description: Creates sophisticated multi-page documentation systems.
# (No trigger phrases — agent won't know when to load it)
```

**Debugging tip:** Ask the agent directly: "When would you use the [skill-name] skill?" It will quote the description back. Adjust based on what's missing.

**Optional frontmatter fields:**
- `license`: Open source license (e.g., `MIT`, `Apache-2.0`)
- `compatibility`: Environment requirements (e.g., "Requires Python 3.10+, internet access")
- `allowed-tools`: Restricts which tools the skill can invoke (e.g., `"Bash(python:*) WebFetch"`)
- `metadata`: Custom key-value pairs — useful for `author`, `version`, `mcp-server`, `category`, `tags`

**Security restriction:** Never use XML angle brackets (`<` or `>`) in the frontmatter. The frontmatter appears in the agent's system prompt, so malicious content could theoretically inject instructions.

---

## 7. Writing Effective Instructions

After the frontmatter, write your instructions in plain Markdown. The body of `SKILL.md` is Level 2 of the progressive disclosure system — it loads when the agent decides the skill is relevant.

**Recommended structure:**
```markdown
# Skill Name

## Instructions

### Step 1: [First major step]
Clear explanation of what to do.

Example:
```bash
python scripts/validate.py --input {filename}
Expected output: validation summary with pass/fail for each field
```

### Step 2: [Next step]
...

## Examples

### Example 1: [Common scenario]
User says: "Set up a new project workspace"
Actions:
1. Fetch team structure via MCP
2. Create project with provided name
3. Create default tasks with labels
Result: Fully configured project workspace

## Troubleshooting

### Error: "Connection refused"
Cause: MCP server not running.
Solution: Check Settings > Extensions > [Service] > Reconnect
```

**Best practices for instructions:**

**Be specific and actionable.** Vague instructions produce inconsistent results. Tell the agent exactly what command to run, what output to expect, what constitutes success.

```
# Bad
Validate the data before proceeding.

# Good
Run `python scripts/validate.py --input {filename}`.
Expected output: a summary of pass/fail for each field.
If validation fails, common issues include:
- Missing required fields (add them to the CSV)
- Invalid date formats (use YYYY-MM-DD)
```

**Include error handling.** What should the agent do if an API call fails? If a required field is missing? Don't leave these as implicit — spell them out.

**Use progressive disclosure within the file.** Keep `SKILL.md` under 500 lines (ideally under 5,000 words). Move detailed reference docs, large examples, and API guides to `references/` and link to them: "Before writing queries, consult `references/api-guide.md` for rate limiting guidance and pagination patterns."

**For critical validations, write code — not prose.** Language instructions are interpreted; code is deterministic. If it's absolutely essential that something be checked (a compliance rule, a format validation), put it in a script in `scripts/`. The agent calls the script; the script either passes or fails. No ambiguity.

**Explain the why.** "Fetch the team roster before creating tasks" is better with the reason: "Fetch the team roster before creating tasks — this ensures assignees exist and prevents silent failures when tasks can't be assigned."

---

## 8. Three Categories of Skills

Anthropic has observed three primary use cases emerge from real-world skill adoption.

### Category 1: Document and Asset Creation

These skills produce consistent, high-quality output — documents, presentations, code, design artifacts — using the agent's built-in generation capabilities. No external tools required.

**What they contain:** Embedded style guides and brand standards, template structures, quality checklists before finalizing output.

**Examples:** A skill for generating legal briefs in a specific firm's format. A skill for writing technical documentation that always includes a "Quick Start" and "API Reference" section. Anthropic's own `frontend-design` skill that generates distinctive, production-grade UI code.

The power here is consistency: the same output format, the same quality bar, every time, for every user.

### Category 2: Workflow Automation

These skills orchestrate multi-step processes — often across multiple MCP-connected services — with explicit ordering, validation gates at each stage, and rollback instructions for failures.

**What they contain:** Step-by-step workflows with explicit dependencies, templates for common structures, iterative refinement loops, review checkpoints.

**Examples:** A customer onboarding workflow that creates an account, sets up payment, creates a subscription, and sends a welcome email — in that exact order, with verification at each step. A sprint planning workflow that fetches velocity data, analyzes capacity, suggests prioritization, and creates tasks.

The power here is reliability: complex processes complete consistently, without the user having to remember or specify each step.

### Category 3: MCP Enhancement

These skills layer workflow expertise on top of an MCP server's raw tool access. The MCP provides connectivity; the skill provides intelligence.

**What they contain:** Sequences of MCP tool calls, embedded domain knowledge (compliance rules, best practices), error handling for common API issues, context that users would otherwise need to specify every time.

**Examples:** Sentry's `sentry-code-review` skill, which automatically analyzes bugs detected in GitHub PRs using Sentry's error monitoring data. A Notion skill that knows your company's specific database schema and creates pages in the right format.

The power here is the gap between "Claude can use Notion" and "Claude uses Notion the way your team does."

---

## 9. Five Workflow Patterns

These patterns emerged from real skills built by early adopters. They're approaches, not templates — most skills blend more than one.

**A useful frame before choosing a pattern:** are you solving a problem-first or tool-first challenge? Problem-first means "I need to onboard a new customer" — the skill orchestrates tools to achieve the outcome. Tool-first means "I have the Linear MCP connected" — the skill teaches the optimal workflow for using that tool. Most skills lean one direction.

### Pattern 1: Sequential Workflow Orchestration

Use when tasks must happen in a specific order with dependencies between steps.

```
Step 1: Create account (MCP call: create_customer)
Step 2: Setup payment — wait for Step 1 to complete
Step 3: Create subscription using customer_id from Step 1
Step 4: Send welcome email
```

Key techniques: explicit step ordering, dependencies between steps, validation at each stage, rollback instructions if a step fails.

### Pattern 2: Multi-MCP Coordination

Use when a workflow spans multiple services and needs to pass data between them.

Example — design-to-development handoff:
```
Phase 1: Export assets from Figma (Figma MCP)
Phase 2: Upload assets to Drive, generate shareable links (Drive MCP)
Phase 3: Create development tasks with asset links attached (Linear MCP)
Phase 4: Post handoff summary to engineering channel (Slack MCP)
```

Key techniques: clear phase separation, explicit data passing between services, validate before advancing phases, centralized error handling.

### Pattern 3: Iterative Refinement

Use when output quality improves with iteration — the agent produces a draft, evaluates it against quality criteria, improves it, and repeats until meeting a threshold.

```
Draft → Quality Check (run validation script) → Identify Issues → Refine → Re-validate → Finalize
```

Key techniques: explicit quality criteria the agent can evaluate against, validation scripts for objective checks, clear stopping conditions to prevent infinite loops.

### Pattern 4: Context-Aware Tool Selection

Use when the same outcome should be achieved via different tools depending on context.

```
Decision tree:
- Large file (>10MB): Use cloud storage MCP
- Collaborative doc: Use Notion/Docs MCP
- Code file: Use GitHub MCP
- Temporary: Use local storage

Execute appropriate tool → Explain why that tool was chosen
```

Key techniques: clear decision criteria, defined fallback options, transparency with the user about which tool was selected and why.

### Pattern 5: Domain-Specific Intelligence

Use when the skill adds specialized knowledge — compliance rules, governance requirements, expert heuristics — beyond tool access.

```
Before processing: Run compliance checks (sanctions lists, jurisdiction rules, risk assessment)
If compliance passes: Process with fraud checks
If compliance fails: Flag for review, create compliance case
After processing: Log all decisions for audit trail
```

Key techniques: domain expertise embedded directly in the logic, compliance checks before any action, comprehensive documentation of decisions, clear governance rules.

---

## The Two-Skill Pattern: Agent Skills vs. Invoked Skills

This is a critical architectural decision in Claude Code that generalizes to any agentic system with preloaded context.

### Agent Skills (Preloaded in Context)

**What they are:** Skills that are loaded into an agent's context **at startup** and persist for the entire session. They become part of the agent's "knowledge base" before any task runs.

**Characteristics:**
- Always available, zero latency to invoke
- Consume tokens from the base context window
- Used for frequently-accessed knowledge or core procedures
- Example: A mining operations agent has "ore variability analysis" preloaded

**When to use:**
- Core domain knowledge the agent needs constantly
- Procedures that run on almost every invocation
- Operational constraints that must never be forgotten
- High-frequency tools or workflows

**Cost/Benefit:**
- **Cost:** Base context token consumption (you pay even if not used)
- **Benefit:** Instant access, no latency, guaranteed availability

### Invoked Skills (Called On-Demand)

**What they are:** Skills that are loaded **only when explicitly invoked** via `/skill-name` or through explicit instruction in the conversation.

**Characteristics:**
- Loaded when needed, discarded after use
- Lower base context cost
- Higher per-invocation cost (context switching overhead)
- Example: A mining operations agent invokes "emergency halt procedure" only in failure scenarios

**When to use:**
- Specialized knowledge needed infrequently
- Large reference materials (algorithms, lookup tables)
- Domain-specific workflows that don't run every invocation
- Specialized output formatters

**Cost/Benefit:**
- **Cost:** Per-invocation overhead, context switching
- **Benefit:** Lean base context, knowledge available when needed

### Design Pattern: Right-Sizing Your Agent

The question: **What should be preloaded vs. invoked?**

**Preload (agent skill):**
- Core RL reward function in a process control system
- Ore analysis framework in a mining operations system
- Safety constraints in an autonomous system
- Frequently-used validation rules

**Invoke (skill):**
- Failsafe/recovery procedures (used on error)
- Rare edge case handling
- Specialized output formats (SVG generation, LaTeX typesetting)
- Reference materials (lookup tables, encyclopedic knowledge)

**Real example — MineOS system with 1,000 control variables:**

```
Agent Skills (preloaded):
├── Core RL optimization algorithm
├── Ore variability model
├── Real-time safety constraints
└── Production target framework

Invoked Skills (on-demand):
├── Emergency halt procedure
├── Ore anomaly detection
├── Recovery and restart sequence
└── Historical performance analysis
```

The agent always has the core optimization logic. It invokes specialized procedures only when needed.

### Scope Precedence: Where Skills Live

Skills can be scoped at three levels:

| Level | Where | Visibility | Scope |
|-------|-------|-----------|-------|
| **Project** | `.claude/skills/` | Entire team | Shared across all agents and commands |
| **Agent** | Agent frontmatter `skills:` | Single agent | Only this agent can preload these agent skills |
| **User** | Personal skills folder | You only | Personal workflows and experiments |

**Design pattern for teams:**
```
.claude/skills/                        # Project-wide: mining operations framework
  ├── ore-analysis/
  ├── safety-constraints/
  └── rl-guidelines/

.claude/agents/mine-ops.md             # Agent-specific preload
  skills:
    - ore-analysis/framework
    - safety-constraints/core
```

Other agents get project skills but not necessarily the agent-specific preloads. This prevents knowledge collision.

### The Environment Diagnostic

If an agent consistently fails at a particular procedure:
- **Is the skill preloaded or invoked?** Preloaded skills guarantee availability; invoked skills depend on explicit invocation.
- **Is the skill's scope correct?** Agent-specific skills only load if the agent is assigned. Project skills load everywhere.
- **Is the skill's context lean?** Skills over 200 lines lose precision. Break into multiple smaller skills.

The fix is usually environment, not the agent's reasoning:
- Missing skill preload → add to agent frontmatter
- Skill never invoked → update agent's instructions to invoke it explicitly
- Skill too large → split into focused sub-skills

---

## 10. Testing and Iteration

### The Right Testing Philosophy

The most effective skill builders iterate on a single challenging task until the agent succeeds, then extract the winning approach into a skill. This is faster than writing a skill and then testing it broadly — you learn what actually works first.

Once you have a working foundation, expand to multiple test cases for coverage.

Skills can be tested at different levels of rigor:
- **Manual testing in Claude.ai** — Run queries directly, observe behavior. Fast, no setup.
- **Scripted testing in Claude Code** — Automate test cases for repeatable validation.
- **Programmatic testing via API** — Build evaluation suites that run systematically.

A skill used internally by five people needs different rigor than one deployed to thousands of enterprise users.

### Three Testing Areas

**1. Triggering tests** — Does the skill load at the right times?
- Run 10–20 test queries that should trigger the skill. Track how many load automatically vs. require explicit mention.
- Also test that it *doesn't* trigger on unrelated queries.

```
Should trigger:
- "Help me plan this sprint"
- "Create some tasks for the Q4 project"
- "Set up a sprint in Linear"

Should NOT trigger:
- "What's the weather today?"
- "Help me write a Python function"
- "Summarize this document"
```

**2. Functional tests** — Does the skill produce correct outputs?
- Valid output generated
- API/MCP calls succeed
- Error handling works as described
- Edge cases covered (empty inputs, missing fields, API failures)

**3. Performance comparison** — Does the skill improve results vs. baseline?

Compare the same task with and without the skill:

| Metric | Without Skill | With Skill |
|---|---|---|
| Messages needed | 15 back-and-forth | 2 clarifying questions |
| Failed API calls | 3 requiring retry | 0 |
| Tokens consumed | 12,000 | 6,000 |
| Time to completion | 20 minutes | 3 minutes |

### Recognizing When to Iterate

**Under-triggering** — the skill doesn't load when it should:
- Signals: Users manually enabling the skill, support questions about when to use it
- Fix: Add more trigger phrases and keywords to the description, especially technical terms users might actually say

**Over-triggering** — the skill loads for irrelevant queries:
- Signals: Users disabling the skill, confusion about its purpose
- Fix: Add negative triggers ("Do NOT use for simple data exploration"), narrow the scope statement

**Execution issues** — the skill triggers but doesn't follow instructions:
- Signals: Inconsistent outputs, user corrections needed, API failures
- Fix: Make instructions more specific, add error handling, script critical validations instead of describing them in prose

---

## 11. Distribution and Sharing

### How Users Install Skills (as of early 2026)

**Individual installation:**
1. Download or clone the skill folder
2. Zip the folder
3. Upload via Claude.ai → Settings → Capabilities → Skills, or place in Claude Code's skills directory

**Organization-level deployment:**
- Admins can deploy skills workspace-wide (launched December 2025)
- Enables automatic updates and centralized management across all users

### API Access for Programmatic Use

For applications, agents, and automated pipelines that use skills programmatically:
- `/v1/skills` API endpoint for listing and managing skills
- Add skills to Messages API requests via the `container.skills` parameter
- Works with the Claude Agent SDK for building custom agents
- Requires the Code Execution Tool beta (provides the secure environment skills run in)

| Use Case | Best Surface |
|---|---|
| End users interacting directly | Claude.ai / Claude Code |
| Manual testing during development | Claude.ai / Claude Code |
| Applications using skills programmatically | API |
| Production deployments at scale | API |
| Automated pipelines and agent systems | API |

### Publishing for Public Distribution

If you want others to use your skill:
1. Host on GitHub with a public repo and a `README.md` at the repo root (for human visitors — remember, no `README.md` inside the skill folder itself)
2. Document in your MCP server's docs: link to the skill, explain why using both together matters, provide a quick-start
3. Include installation instructions and example usage with screenshots

**Positioning principle — focus on outcomes, not technical features:**
```
Good: "Set up complete project workspaces in seconds instead of 30 minutes of manual setup."
Bad: "A folder containing YAML frontmatter and Markdown instructions that calls MCP server tools."
```

---

## 12. Troubleshooting Common Failures

### Skill Won't Upload

**"Could not find SKILL.md in uploaded folder"**
The file name is wrong. It must be exactly `SKILL.md` — case-sensitive. Rename it and retry.

**"Invalid frontmatter"**
YAML formatting error. Most common causes:
```yaml
# Wrong — missing --- delimiters
name: my-skill
description: Does things

# Wrong — unclosed quotes
description: "Does things

# Correct
---
name: my-skill
description: Does things.
---
```

**"Invalid skill name"**
The `name` field has spaces or capitals. Use `my-cool-skill`, not `My Cool Skill`.

### Skill Doesn't Trigger

The description is too vague. Run the debug check: ask the agent "When would you use the [skill-name] skill?" It will tell you what it understands. Add specific trigger phrases that match how users actually phrase requests.

### Skill Triggers Too Often

Add negative triggers and clarify scope:
```yaml
description: Advanced statistical modeling for CSV datasets. Use for regression,
clustering, and multivariate analysis. Do NOT use for simple data exploration or
chart creation (use data-viz skill instead).
```

### MCP Connection Issues

Symptom: Skill loads, but MCP calls fail.

Checklist:
1. Verify MCP server shows "Connected" in Settings → Extensions
2. Check authentication — API keys, OAuth tokens, permission scopes
3. Test MCP independently: ask the agent to call the MCP directly without the skill. If this fails, the issue is MCP configuration, not the skill.
4. Verify tool names — they're case-sensitive, and must match the MCP server's documentation exactly.

### Instructions Not Followed

Symptom: Skill loads, but agent ignores or inconsistently follows instructions.

Common causes:
- **Instructions too verbose** — Long paragraphs dilute attention. Use numbered steps and bullets. Move detail to `references/`.
- **Critical instructions buried** — Put the most important rules at the top. Use `## CRITICAL:` headers for non-negotiable steps.
- **Ambiguous language** — Replace vague phrases ("validate properly") with specific criteria ("Before calling create_project, verify: project name is non-empty, at least one team member assigned, start date is not in the past").
- **For high-stakes validations** — Write a script. Code is deterministic; language interpretation isn't. Put the script in `scripts/` and instruct the agent to run it.

### Performance Degradation

Symptom: Agent seems slow or response quality drops.

Causes: `SKILL.md` is too large, or too many skills are enabled simultaneously.

Solutions:
- Move detailed docs to `references/`, link from `SKILL.md`. Keep `SKILL.md` under 5,000 words.
- Avoid enabling more than 20–50 skills simultaneously. Use selective enablement.

---

## 13. Anti-Patterns

**Vague descriptions.** "Helps with projects." is not a description — it's noise. The agent won't know when to load this, and even if it does, users won't know what it's for.

**Missing trigger phrases.** Describing what a skill *does* without describing what a user *says* to trigger it results in permanent under-triggering.

**SKILL.md as a data dump.** The body of `SKILL.md` is loaded into the agent's active context. Dumping 10,000 words of API documentation into it wastes attention and degrades performance. Use `references/`.

**Over-relying on language for critical validations.** If a compliance check must always happen, a script is more reliable than an instruction. Language instructions can be misread, skipped, or interpreted loosely under novel conditions.

**Building a skill before finding the winning approach.** The fastest path is: work with the agent conversationally until you crack a difficult task, then encode *that specific winning approach* into a skill. Don't write skills speculatively.

**Not iterating.** Skills are living documents, not one-time deliverables. The signals for under-triggering, over-triggering, and execution failures are clear. Plan for at least one iteration cycle after real use.

---

*Sources: Anthropic's "The Complete Guide to Building Skills for Claude" (PDF, 2025); agentskills.io (Agent Skills open standard); github.com/clasen/Skills SKILL.md (2025)*

---

## 14. Continuous Learning via Instincts (v2 Architecture)

**Adapted from [everything-claude-code](https://github.com/affaan-m/everything-claude-code)**

Skills are powerful but heavy: each one is 300-500 lines, structured formally, with versioning overhead. For rapid knowledge capture, you need something lighter: **instincts**.

### What Are Instincts?

An **instinct** is a micro-skill: a single, atomic behavior pattern with a confidence score (0.3-0.9). Instead of building a full 500-line skill after every learning, you capture atomic insights immediately, then promote them to skills only after confidence reaches threshold.

**Instinct Example:**

```yaml
---
name: avoid-eval-for-internal-paths
confidence: 0.62
category: error-handling
trigger: ["error handling", "try-catch", "internal functions"]
---

# When to Avoid Error Handling

For internal, trusted code paths (functions you control, within your codebase),
avoid over-defensive error handling. Example:

❌ BAD (unnecessary):
```python
result = my_internal_function(safe_arg)  # You wrote this function
if result is None:  # But you check for None anyway
    result = fallback
```

✓ GOOD (trust internal contracts):
```python
result = my_internal_function(safe_arg)  # Trust it works
```

Only handle errors at **system boundaries** (external APIs, user input, filesystem).
```

**Key properties:**
- Atomic (one rule, not a procedure)
- Scored (confidence: 0.62 = "pretty sure")
- Lightweight (< 50 lines)
- Triggerable (keywords to activate)

### The Instinct Lifecycle

```
Stage 1: OBSERVATION (Confidence 0.3-0.4)
├─ You solve a problem in a session
├─ Agent catches the pattern
├─ Create instinct: "Here's what worked"
└─ Example: "Error handling inside custom code is waste"

Stage 2: VALIDATION (Confidence 0.5-0.7)
├─ Use instinct in 2-3 projects
├─ Works most of the time?
├─ Confidence increases: 0.5 → 0.7
└─ If it fails, debug why (narrow the rule)

Stage 3: PROMOTION (Confidence 0.8+)
├─ Instinct proved useful in 3+ projects
├─ Pattern stabilized
├─ Promote to full skill (formalize, document, version)
└─ Example: "Error Handling Patterns" skill

Stage 4: ABSORPTION (Confidence 0.95)
├─ Skill is so common it becomes implicit
├─ Merge into system prompt or CLAUDE.md
├─ Remove as separate skill (no longer needed)
└─ Example: Now part of default "best practices"
```

### Implementation: Instinct YAML Format

```yaml
---
name: pattern-identifier  # kebab-case, unique
confidence: 0.65          # 0.0-1.0, updated per cycle
category: coding | error-handling | performance | security | prompt-design
triggers: ["keyword1", "keyword2"]  # When to activate
phases: ["implementation", "review", "testing"]  # When in workflow
project_count: 2          # How many projects has this helped?
last_updated: 2026-03-08
---

# Human-Readable Pattern Name

Short description (2-3 sentences) of the pattern and when it applies.

## When to Use
- Situation 1
- Situation 2
- NOT when: counter-example

## Example
[Code or explanation showing the pattern]

## Why This Works
Brief explanation of the underlying principle.
```

### Confidence Scoring

How confidence evolves:

```
Instinct creation: confidence = 0.30 (guess)
├─ Used in 1 project successfully: +0.15 → 0.45
├─ Used in 2 projects, both succeed: +0.20 → 0.65
├─ Used in 3 projects, all succeed: +0.25 → 0.90
└─ Passed red-team / adversarial test: +0.10 → 1.00

If it fails:
├─ Narrow the rule: -0.10
├─ Add exception clause: no change (more specific)
└─ Abandon it: confidence stays but marked "under revision"
```

**Usage threshold:**
- < 0.50: Private (only you use it)
- 0.50-0.75: Project-scoped (share with team on this project)
- 0.75-0.90: Global (recommend to other projects)
- > 0.90: Promote to skill (formalize, version, document)

### Storage & Activation

**File structure:**

```
~/.claude/instincts/
├─ error-handling/
│  ├─ avoid-defensive-internals.yaml (0.65)
│  ├─ wrap-system-boundaries.yaml (0.82)
│  └─ use-custom-errors.yaml (0.71)
├─ performance/
│  ├─ lazy-load-large-contexts.yaml (0.78)
│  └─ precompute-expensive-values.yaml (0.55)
└─ prompt-design/
   └─ structure-with-xml.yaml (0.88)
```

**Activation (via hook or agent trigger):**

```
When user's request mentions "error handling":
├─ Scan instincts/ for matching `triggers`
├─ Load instincts with confidence > 0.50
├─ Inject into system prompt as "Known Patterns:"
└─ Agent can apply or ignore (confidence tells it the strength)

When agent finishes a task:
├─ Log which instincts were mentioned/used
├─ Update confidence based on success
└─ If confidence jumped, flag for promotion
```

### Promotion: From Instinct to Skill

When confidence reaches 0.85+:

```
OLD (Instinct):
---
name: use-custom-errors
confidence: 0.88
triggers: ["error", "exception", "catch"]
---
# Use Custom Error Classes
Always define custom error classes (ApplicationError, APIError) instead of generic Exception.

NEW (Skill):
SKILL.md - "Error Handling Best Practices"

## 1. Custom Error Classes
Define domain-specific exceptions...
[Full SKILL.md with references, examples, anti-patterns]

CLAUDE.md inclusion:
"When handling errors, always use custom classes from errors.py"
```

### Benefits Over Traditional Skills

| Aspect | Skills Only | Instincts + Skills |
|---|---|---|
| **Capture speed** | Days (write full skill) | Seconds (YAML) |
| **False positives** | Low (high bar to formalize) | Acceptable (0.3-0.7 OK) |
| **Learning curve** | Agent learns from instances | Agent learns incrementally |
| **Evolution** | Manual updates | Automatic confidence growth |
| **Overhead** | High (500+ lines per skill) | Low (20-50 lines per instinct) |

### Checklist: Instinct-Based Learning System

- [ ] Create ~/.claude/instincts/ directory
- [ ] Define instinct YAML format (confidence, triggers, category)
- [ ] Set up hook to load instincts by trigger keywords
- [ ] Log which instincts agent used in each session
- [ ] Implement promotion logic (confidence > 0.85 → flag for skill)
- [ ] Weekly review: promote mature instincts to skills
- [ ] Deprecate: remove instincts that regress (confidence drops)
- [ ] Document instinct evolution in session logs (learning history)

---
