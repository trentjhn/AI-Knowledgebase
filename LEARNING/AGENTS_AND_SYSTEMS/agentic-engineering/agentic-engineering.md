# Agentic Engineering

> Distilled from *Agentic Engineering* by Jaymin West (https://github.com/jayminwest/agentic-engineering-book), plus empirical studies on function-calling optimization (Brief Is Better: Non-Monotonic Chain-of-Thought Budget Effects, 2026)
> Guiding philosophy: **"One agent, one purpose, one prompt."**

---

## What Is an AI Agent?

Before diving into the details, it's worth establishing what we mean by an **AI agent**.

A standard AI interaction looks like this: you ask a question, the AI answers, and it's done. The AI isn't doing anything in the world — it's just responding to text with more text.

An **AI agent** is different. An agent can take *actions* — it can search the web, read and write files, execute code, call APIs, send messages, and interact with external systems. It's not just answering questions; it's actually doing things. Crucially, it can chain multiple actions together: read a file, then analyze it, then write a new file based on what it found, then run tests, then report back. It can operate autonomously through many steps toward a goal.

This makes agents dramatically more powerful than chatbots — but also dramatically more complex to build correctly. Agentic engineering is the discipline of building these systems well.

---

## Table of Contents

1. [Foundations — The Four Pillars](#1-foundations--the-four-pillars)
2. [The Twelve Leverage Points](#2-the-twelve-leverage-points)
3. [Prompt Engineering](#3-prompt-engineering)
4. [Models](#4-models)
5. [Context](#5-context)
6. [Tool Use](#6-tool-use)
7. [Patterns](#7-patterns)
8. [Practices](#8-practices)
9. [Mental Models](#9-mental-models)
10. [Agent Frameworks](#10-agent-frameworks)
11. [Development Methodologies](#11-development-methodologies)
12. [Dual-Instance Planning](#12-dual-instance-planning)
13. [Event-Driven Agents](#13-event-driven-agents)
14. [Team AI Coordination](#14-team-ai-coordination)
15. [Multi-Agent Shared Context & Query Routing](#15-multi-agent-shared-context--query-routing)

---

## 1. Foundations — The Four Pillars

### The Core Four Pillars

Every AI agent, no matter how complex, is built from four fundamental components. Understanding these pillars — and how they interact — is the entire foundation of agentic engineering.

**The Prompt** is the set of instructions you give the agent. It tells the agent who it is, what its job is, how to behave, and what constraints it must follow. Think of it as the job description and employee handbook combined.

**The Model** is the underlying AI — the actual language model that does the reasoning and decision-making. Different models have very different capabilities, costs, speeds, and behaviors. Choosing the right model for the right task is a significant skill in itself.

**The Context** is the agent's working memory — everything the model can "see" at once. It includes instructions, conversation history, retrieved documents, tool outputs, and any other information relevant to the current task. Context is finite and temporary: when the session ends, context is gone.

**Tool Use** refers to the external actions the agent can take. Without tools, an agent can only generate text. With tools — web search, file reading/writing, code execution, API calls — the agent can interact with the world.

These four pillars are deeply interconnected. You can't change one without affecting the others:

- Adding more tools fills up the context window with tool descriptions, leaving less room for actual task information
- Switching to a less capable model might mean your carefully written prompt stops being followed correctly
- Expanding your context with more background information affects how the model interprets your prompt
- Changing the prompt can override how the model interprets everything else in the context

> **Counter-intuitive finding:** "More" does not equal better — but the type of "more" matters. More *irrelevant* tools, *noisy* context, and *redundant* instructions degrade agent performance: a focused agent with the right tools and lean context consistently outperforms one drowning in options. However, more *structured, domain-relevant* context (comprehensive playbooks, well-organized knowledge) can improve performance for knowledge-intensive tasks. The rule is: cut noise ruthlessly, but don't strip structured domain knowledge. See ACE framework in Section 5 for when larger context helps.

**The 2025 landscape:** Until recently, model choice dominated everything — get the best model and most other things would work out. That's no longer true. The gap between frontier models has narrowed significantly. The other three pillars (prompt, context, tool use) now carry far more weight in determining whether your agent succeeds.

---

## 2. The Twelve Leverage Points

### A Framework for Knowing Where to Intervene

When an agent isn't working well, where do you fix it? When you want to improve an agent, what do you change? The **Twelve Leverage Points** framework gives you a structured answer.

The concept is adapted from systems thinking — specifically Donella Meadows' work on places to intervene in a complex system. The key insight: **not all interventions have equal impact**. Some changes ripple through the entire system; others just fix one local problem.

The twelve points are ordered from lowest to highest leverage. Changes at points 1-4 affect everything downstream. Changes at points 9-12 produce local, limited improvements.

---

### Low Leverage (Points 9-12): Local Fixes

These are the tools most people reach for first — and they often work, but only for isolated issues.

**Point 12 — Context: What does the agent actually know?**
Poor context: loading your entire documentation library (500K+ tokens, mostly irrelevant to the current task).
Good context: loading only the specific module docs relevant to this task (15K tokens, high relevance).
The same agent with better context will perform dramatically better without changing anything else.

**Point 11 — Model: What capability tier is appropriate?**
Using a frontier model (Opus) for a task that only needs basic pattern matching wastes 10× the cost. Using a cheap fast model (Haiku) for architectural reasoning produces unreliable results. Match the model tier to the task complexity.

**Point 10 — Prompt: Are instructions concrete and followable?**
Vague: *"Make this code better."*
Concrete: *"Refactor the authentication module to use dependency injection. Extract token validation into a separate class. Maintain existing test coverage."*
The second version leaves no ambiguity about what "better" means. The model can follow it literally.

**Point 9 — Tools: What actions can the agent take?**
Tools come in several varieties: internal functions you write yourself, MCP servers (standardized tool protocols), and CLI wrappers. The choice affects flexibility vs. reliability. Too many tools causes confusion (see the context section).

---

### Medium Leverage (Points 5-8): System Properties

These points affect how the agent operates, not just what it knows or can do.

**Point 8 — Standard Output: Can you see what's happening?**
An agent you can't observe is an agent you can't debug. Every log entry needs clear sources and descriptions. "Observable agent systems are manageable agent systems." If you don't have visibility, you're flying blind.

**Point 7 — Types: Is data typed consistently?**
Strong typing in your codebase helps agents write correct code — they can see what types functions expect and return. Surface type errors in actionable, readable formats so agents can fix them without guessing.

**Point 6 — Documentation: Can agents navigate and trust the docs?**
Documentation needs to be *agent-navigable* — easy to search, up to date, and ideally self-improving. An agent reading outdated documentation will confidently do the wrong thing. Stale docs are worse than no docs for agents.

**Point 5 — Tests: Are tests actually verifying real behavior?**
Watch for "testing theatre" — tests that pass but don't verify anything meaningful. Good tests give agents clear feedback: pass means success, fail means something specific is broken. Mock at system boundaries (external APIs, databases), not internally — internal mocks create false confidence.

---

### High Leverage (Points 1-4): System Architecture

These points shape the fundamental structure of how work flows through the system.

**Point 4 — Architecture: Is the codebase agentically intuitive?**
AI models were trained on vast amounts of code. They perform best on architectures that follow widely-known, historically-popular patterns. A conventional folder structure, standard naming conventions, and familiar design patterns help agents orient quickly. Exotic custom architectures that deviate from training distribution make agents slower and more error-prone.

**Point 3 — Plans: Can agents complete tasks without constant interruption?**
A good plan is a massive, detailed prompt that contains everything the agent needs to complete a well-scoped task with zero further input. Getting the scope right is the critical skill here — too broad and the plan can't anticipate every case; too narrow and you're back to constant back-and-forth.

**Point 2 — Templates: Do agents know what good output looks like?**
Reusable, consistently structured prompt templates prevent output drift across different invocations. Templates also make it easy to compare outputs and iterate on prompts systematically. Without templates, every prompt invocation is a new experiment.

**Point 1 — ADWs (AI Developer Workflows): How does work carry between agents?**
This is the highest leverage point in the entire framework. ADWs define how work flows between agents — how one agent's output becomes another agent's input. The choice between deterministic (code-based, predictable) and stochastic (LLM-based, flexible) handoffs shapes the entire system's reliability. Getting this architecture right is the difference between agents that compound each other's work effectively and agents that compound each other's errors.

---

### Common Beginner Mistakes

New practitioners tend to make the same mistakes when building their first agents:

1. **Poor information organization** — Dumping everything into unstructured context, causing the model to miss critical information buried in noise
2. **Excessive trust in model outputs** — Not verifying what the agent produced before using it in downstream steps; errors compound
3. **Too many tools** — Giving agents access to every tool available "for flexibility"; unfocused agents waste tokens evaluating irrelevant options
4. **Passive or vague language** — "Improve this code" instead of "Refactor X to achieve Y while maintaining Z"
5. **No structure** — Presenting information as free-form prose when structured formats (markdown, JSON, XML) work dramatically better
6. **No constraints** — Agents need boundaries; presenting an unbounded option space causes analysis paralysis and inconsistent outputs
7. **Insufficient detail** — Expecting agents to "figure out" the approach; relying on discovery instead of specification increases failure rates

---

## 3. Prompt Engineering

### What Makes a Good Prompt?

A prompt is more than just a question or instruction. For an AI agent, the prompt is the foundation of everything — it defines the agent's identity, scope, constraints, workflow, and expected outputs. Bad prompts produce bad agents regardless of how good the underlying model is.

Prompt engineering has matured from "how do I phrase this question" to a genuine engineering discipline with measurable quality dimensions, structured formats, and evolutionary patterns.

---

### The 7 Levels of Prompt Maturity

Prompts can be thought of as evolving through seven maturity levels, from the simplest possible form to sophisticated self-improving systems.

**Level 1 — Static:** A fixed instruction with no variation. "Summarize this document." Works for one-off tasks, but has no flexibility. Every invocation is identical.

**Level 2 — Parameterized:** Accepts variables as input. Instead of a fixed instruction, the prompt contains placeholders like `$ARGUMENTS` that get filled in at runtime. The same prompt template can now handle many different inputs. *When to evolve: "I need this to work with different inputs."*

**Level 3 — Conditional:** Branches based on input or state. Different inputs trigger different instructions within the same prompt. Like an `if/else` statement embedded in the prompt logic. *When to evolve: "I need different behavior for different types of input."*

**Level 4 — Contextual:** Incorporates external files, documents, or reference material. The prompt dynamically loads relevant context from outside itself — reading project files, documentation, or prior outputs. *When to evolve: "I need this to understand my specific codebase or domain."*

**Level 5 — Composed:** Invokes other prompts as subroutines. Rather than doing everything in one prompt, this level coordinates with other specialized prompts, passing outputs between them. *When to evolve: "I need coordination with other specialized agents."*

**Level 6 — Self-Modifying:** Updates itself based on execution outcomes. After running, the agent analyzes what worked and what didn't, and updates its own knowledge sections with new learnings. See below for how this works. *When to evolve: "I want this agent to get better over time."*

**Level 7 — Meta-Cognitive:** Analyzes and improves other prompts in the system. Instead of improving just itself, this level improves the whole ecosystem of prompts it oversees. *When to evolve: "I want to improve the entire system."*

> **Rule:** Start at the lowest level that meets your requirements. Let real usage drive evolution upward. Building a Level 5 prompt when you need a Level 2 is over-engineering — it adds complexity and failure modes without benefit.

**How Level 6 self-modification works:**

After each significant task, the agent:
1. Runs `git diff` to see uncommitted changes, and `git log` to see recent commits
2. Analyzes which patterns in the codebase changed and why
3. Updates its `## Expertise` section with new learnings, dated and referenced to the specific commit that revealed them
4. Leaves the `## Workflow` section (operational procedures) completely untouched

Conservative rules for self-updates: *preserve* existing patterns unless they're confirmed obsolete. *Append* new learnings with commit references. *Remove* only patterns contradicted by multiple recent implementations.

---

### The Canonical 7-Section Prompt Structure

Well-designed agent prompts follow a consistent structure. Here's the complete template with explanation of each section:

```markdown
---
name: agent-name              # Kebab-case identifier used for invocation
description: When to use this # Action-oriented; describes what triggers this agent
tools: Tool1, Tool2           # Minimal required tools — only what this agent needs
model: haiku | sonnet | opus  # Matched to the task's complexity
---

# Title

## Purpose
You are a [role]. Your sole focus is [single responsibility].
# This establishes identity — one role, not a committee of roles

## Variables
USER_PROMPT: $1
STATIC_CONFIG: value
# Named inputs make it clear what the agent receives and what's fixed

## Instructions
- IMPORTANT: Critical constraint here
- Positive instruction (do this)
- Negative instruction (never do this)
# Ordered by priority — most critical first

## Workflow
1. Parse Input
2. Gather Context
3. Execute Task
4. Verify Results
5. Report
# Deterministic steps the agent follows

## Report
### Summary
- **Status**: [success/failure]
### Details
[Exact markdown structure expected]
# Defined output format — prevents parsing failures downstream
```

**Design output-first:** Before writing any instructions, define the exact output format you expect. Use JSON schemas, markdown templates, or concrete examples. The output contract drives the design of everything else. An agent that produces inconsistently structured output breaks downstream systems.

---

### Language That Helps vs. Language That Hurts

**Forbidden meta-commentary** — these phrases signal that the agent is narrating its process rather than producing output. They break downstream parsing and add noise:
- "Based on the changes..."
- "I have created..."
- "Here is the..."
- "Let me..." / "I will..." / "Looking at..."

The agent should *produce* the output, not *announce* that it's producing it.

---

**Declarative vs. Imperative language:** The SatLM study (Ye et al., NeurIPS 2023) found declarative prompts outperform imperative ones by ~23% — but specifically on a challenging subset of grade-school arithmetic (GSM), not on complex reasoning tasks broadly. On the full GSM8K dataset, imperative program-aided LMs remain competitive. The principle (declarative for constraint satisfaction and reasoning, imperative for procedural tool-calling) is sound, but the 23% figure shouldn't be taken as a general benchmark.

- **Declarative** describes a desired state: *"The solution minimizes edge cases."* The model figures out how to achieve it.
- **Imperative** prescribes steps: *"Parse input, validate schema, return result."* The model executes the steps.

| Task Type | Preferred Style | Example |
|---|---|---|
| Complex reasoning | Declarative | "The solution handles all edge cases" |
| Sequential workflow | Imperative | "Parse input, validate, then return" |
| Tool calling | Imperative | "Search codebase for references" |
| Creative work | Declarative | "The narrative maintains consistent tone" |

The best pattern for complex workflows: declarative for the overall goal, imperative for the specific operational steps.

---

**The Pink Elephant Problem — Why Negative Instructions Backfire:**

When you tell someone "don't think about a pink elephant," they immediately think about a pink elephant. The same happens with LLMs. "Never use global variables" causes the model to activate the concept of global variables — increasing the probability it uses them.

Convert negative constraints to positive alternatives:

| ❌ Negative (backfires) | ✅ Positive (effective) |
|---|---|
| Never use global state | Use dependency injection |
| Don't expose internal errors | Return user-friendly error messages |
| Never modify files without reading | Read file contents before editing |

**Constraint ordering matters:** Put critical blocking constraints first. The model weights earlier content more heavily, so the most important rules go at the top.

```markdown
# CRITICAL — NEVER VIOLATE
- Zero data loss
- Pass all existing tests

# IMPORTANT GUIDELINES
- Follow existing code patterns

# STYLE PREFERENCES
- Keep functions under 50 lines
```

---

### Model-Invoked vs. User-Invoked Prompts

Not all prompts are triggered the same way. There are two fundamentally different activation modes:

**Model-invoked prompts (Skills)** are activated automatically when the model recognizes that a task semantically matches the skill's description. You don't have to remember to use them — the model figures out when they apply. The description field is critical: it must clearly define what triggers the skill *and* what doesn't.

```yaml
---
name: security-reviewer
description: >
  Security-focused code review. Use when analyzing code for vulnerabilities,
  authentication issues, injection attacks, or authorization flaws.
  NOT for general code quality or style review.
---
```

**User-invoked prompts (Slash Commands)** require the user to explicitly call them by name: `/review:security`, `/deploy`, `/test`. They're predictable and easy to debug because the user consciously chooses to invoke them. Good naming matters — `/capture` is better than `/knowledge:add-new-entry`.

| Use Model-Invoked When | Use User-Invoked When |
|---|---|
| The trigger is describable semantically | The user needs to consciously choose |
| Users benefit from not remembering the command | Multiple valid approaches could apply |
| The workflow repeats frequently | The task is rare or one-off |

---

### Measuring Prompt Quality

| Dimension | What It Measures |
|---|---|
| **Structure** | Is it well-organized and parseable by a machine? |
| **Reusability** | Can it be adapted for similar tasks without rewriting? |
| **Templating** | Are the variable parts clearly distinguished from the fixed parts? |
| **Breadth** | Does it handle the full scope of expected inputs? |
| **Depth** | Does it handle edge cases and unusual situations? |
| **Maintainability** | Could someone else understand and modify it six months later? |

---

### Model-Specific Formatting Preferences

Different AI models respond better to different formatting conventions. The same content structured differently can produce up to **40% accuracy variance** in smaller models.

- **Claude (Anthropic):** Prefers XML-style tags: `<instructions>`, `<context>`, `<constraints>`
- **GPT (OpenAI):** Works best with markdown headers (`###`), horizontal rules (`---`), and code fences
- **Gemini (Google):** Values precision; put key information at the *end* of the prompt (context-last ordering)

---

## 4. Models

### The Golden Rule: Default to Frontier

A **frontier model** is the current state-of-the-art — the most capable AI available. When in doubt, use the best model available.

This might feel counterintuitive if you're thinking about cost. But there's a reliable pattern: when things aren't working, the problem is almost never the model capability — it's almost always the prompt or the context. Debugging with a weaker model introduces a second variable and makes diagnosis much harder.

Here's the recommended decision process:

```
1. Start with the frontier model
2. Is the task working reliably?
   → NO:  Don't blame the model yet. Debug the prompt and context first.
   → YES: Is cost a real constraint for this specific use case?
          → NO:  Stay with frontier. Don't optimize prematurely.
          → YES: Test the task with a smaller model.
                 → Still reliable? Switch to smaller.
                 → Unreliable?    Stay with frontier.
```

The key insight: **only downgrade after you have a working solution**. Trying to build and debug with a weaker model simultaneously creates confusion about whether failures are model-related or prompt-related.

**The capabilities that matter most:** Reasoning quality and tool use reliability. Context length, speed, and cost are secondary considerations for most use cases.

**When smaller models are genuinely appropriate:**
- *Scouting/investigative tasks* — reading documents and summarizing findings. A smaller model (Haiku) is fast, cheap, and sufficient for "read and distill" work.
- *Simple retrieval or filtering* — finding things that match criteria, not reasoning about complex tradeoffs.

**Small models as specialized components:** Think of smaller models not as "worse versions" of frontier models, but as specialized retrieval systems. Keep their context minimal (base config + relevant tools + the specific query), let them retrieve and distill, and return results to a more capable orchestrator model for synthesis.

---

### The Three-Tier Spawn Strategy

In multi-agent systems — where multiple AI agents work together — you don't use one model for everything. You match model capability to the specific type of work each agent is doing.

| Model | Cost | Speed | What It's Good For | How Many to Run |
|---|---|---|---|---|
| **Haiku** | Lowest | Fastest | Information gathering, pattern finding, file discovery, search-style tasks | Many at once (5-10 parallel) |
| **Sonnet** | Medium | Medium | Well-defined implementation, established patterns, standard refactoring | A few at once (2-4 parallel) |
| **Opus** | Highest | Slowest | Architectural decisions, ambiguous problems, creative solutions, security review | Rarely, one at a time |

**The pipeline escalation pattern:**

```
Haiku (Research) → Opus (Design) → Sonnet (Implement) → Haiku (Verify)
```

This maps model tier to the type of thinking required at each phase:
- *Research* processes large volumes of text — cheap models handle this fine
- *Design* requires reasoning about tradeoffs under uncertainty — expensive models excel here
- *Implementation* follows patterns established in the design — mid-tier is sufficient
- *Verification* is pattern matching (does it pass tests?) — cheap models are adequate

**The economics in concrete numbers:**
- Running 10 Haiku agents in parallel: ~30 seconds, costs ~$0.10
- Running 1 Opus agent: ~30 seconds, costs ~$1.00
- Haiku delivers 10× the breadth of coverage for 1/10 the cost when the task is information gathering

**Orchestrators use Sonnet or Opus** — the agent managing and coordinating other agents needs to reason well. This cost is amortized across all the subagent work it coordinates.

---

### How Models Actually Behave

**Probabilistic, not deterministic:** LLMs don't compute answers the way code does — they sample from a probability distribution. This means the same prompt can produce different outputs on different runs. This variability compounds in multi-step workflows.

**Temperature** controls this randomness (0 = most consistent, 1 = most varied):

| Temperature | Single-Step Success | 10-Step Success |
|---|---|---|
| 0.0 | ~99% | ~90% |
| 0.5 | ~97% | ~74% |
| 1.0 | ~95% | ~60% |

**Use temperature 0 for multi-agent orchestration and long workflows.** The compounding effect makes higher temperatures increasingly costly over many steps. Reserve higher temperature only for isolated creative phases where variation is desirable.

**Instruction-following by tier:**
- Frontier models (Opus, GPT-4o): reliably follow complex multi-constraint instructions
- Mid-tier (Sonnet): handle structured instructions well, may skip subtle requirements
- Smaller models (Haiku): only work for simple, clearly constrained instructions

**Instruction fade in long contexts:** As the context window fills, instructions that appeared early in the conversation receive *less attention* than recent messages. This is called **recency bias** — the model gives more weight to what appeared recently. In long conversations (above ~50% context utilization), your initial instructions start to "fade." Fix: repeat critical constraints closer to the current task, or spawn a fresh agent for new tasks.

---

### The Compound Error Problem

This is one of the most important mathematical realities in agentic engineering.

In a multi-step workflow, if each individual step has a 95% success rate, a 10-step workflow succeeds only about 60% of the time. Here's why: success probability compounds — it's not 95%, it's 95% × 95% × 95% × ... ten times.

| Per-Step Accuracy | 10 Steps | 50 Steps | 100 Steps |
|---|---|---|---|
| 99% | 90.4% | 60.5% | 36.6% |
| 95% | 59.9% | 7.7% | 0.6% |
| 90% | 34.9% | 0.5% | 0.003% |

The implication is stark: **improving per-step accuracy from 95% to 99% more than doubles your success rate on 50-step tasks.** Chasing the last 4% of per-step reliability is often more valuable than any architectural change.

Practical responses to this reality:
- Optimize per-step reliability above all else
- Keep workflow lengths as short as possible (fewer steps = less compounding)
- Implement retry mechanisms for recoverable failures — retries catching 80% of errors dramatically improves the effective success rate

---

### Multi-Model Architectures

**When a single model is fine:**
- Low volume applications
- Tasks with homogeneous complexity (everything requires similar reasoning)
- Prototyping phase — keep it simple until you know what you're building
- Total API spend below ~$500-1000/month — multi-model complexity isn't worth the overhead

**The Orchestrator-Specialist Pattern:**

A strong, capable orchestrator model decomposes complex tasks and delegates to cheaper specialists:

```
Orchestrator (Opus)
├── Specialist A (Sonnet)  — handles Task A
├── Specialist B (Sonnet)  — handles Task B
└── Specialist C (Haiku)   — handles Task C (simpler)
        ↓
Orchestrator synthesizes all results
```

Research backing: NVIDIA's ToolOrchestra (arXiv 2511.21689) demonstrated this pattern with Nemotron-Orchestrator-8B routing to specialized domain models. On benchmark tasks (FRAMES: 76.3%, tau2-Bench: 80.2%), the orchestrator-specialist system outperformed larger monolithic models at lower compute cost. The key finding: a small orchestrator that routes intelligently beats a large model trying to do everything — routing intelligence matters more than raw model size.

**Model Cascades:**

Try the cheap model first. Only escalate to the expensive model when the quality gate fails.

If 70% of your queries are simple enough for the cheap model and 30% need the expensive one:
- All expensive: 100 queries × $0.010 = $1.00
- Cascade: (70 × $0.001) + (30 × $0.010) = $0.37 — a 62% cost reduction

Quality gate approaches: confidence thresholds, schema validation, classifier-based routing.

**Planning-Execution Separation:**

Let the expensive model plan; let the cheap model execute.

An expensive planning model produces a detailed structured plan (JSON task definitions, dependency graph). A cheap execution model reads the plan and follows it step by step.

The mechanism: the planning model's structured output converts an ambiguous goal into unambiguous steps that a cheaper execution model can follow reliably. The quality lift comes from the plan quality, not the executor. Specific benchmarks vary by task; measure against your own workload rather than expecting a universal accuracy gain.

---

### Known Model Limitations and How to Handle Them

| Limitation | What Happens | Fix |
|---|---|---|
| **Math** | Models are unreliable at arithmetic | Delegate numeric computation to code/external tools |
| **Hallucination** | Generates confident-sounding false information | RAG with mandatory citations reduces this 60-80% |
| **Context degradation** | Performance drops above ~60% context utilization | Compact proactively at 40-60%, not reactively at 95% |
| **Instruction drift** | Early instructions lose weight in long contexts | Repeat critical constraints near the task |
| **Tool use errors** | Wrong tool selected or parameters malformed | Provide concrete examples per tool (72% → 90% accuracy) |
| **Version instability** | Model upgrades change behavior unexpectedly | Pin versions; run staged regression tests before upgrading |

---

## 5. Context

### The Working Memory Analogy

The context window is the agent's working memory — and like human working memory, it's both the most powerful and most fragile part of the system.

Think of it this way: if you hire a new contractor and give them a detailed briefing package at the start of the day, they can work effectively all morning. But if you over-stuff that briefing with irrelevant documents, they'll spend time processing noise. If the briefing runs so long they can't hold it all in mind, they'll start losing track of early instructions. If you wait until the briefing package is completely full before organizing it, you'll find that you've buried the most important parts.

The same dynamics apply to agent context. Managing it well is one of the highest-leverage skills in agentic engineering.

**Five foundational beliefs about context:**

1. **Context is capability.** An agent with 20% context utilization has substantially more cognitive headroom than one at 80%. Treat context like a budget, not a dumping ground.
2. **Quality beats quantity.** What's in the context matters more than how much there is. 30K tokens of highly relevant content produces better results than 100K tokens of mixed signal and noise.
3. **Fresh starts are cheap.** When in doubt, boot a new agent. Salvaging degraded context is almost never worth the effort — it's cheaper to start clean.
4. **Inject vs. retrieve.** Inject what the agent *must* know upfront. Let it retrieve what it *might* need, on demand.
5. **One agent, one task.** If a task scope expands during execution, kill the current agent and rescope rather than pushing through with a cluttered context.

---

### Capability Degradation Thresholds

Agent performance doesn't degrade linearly as context fills — there are thresholds where behavior changes notably:

| Context Utilization | What to Do |
|---|---|
| 0–30% | Normal operation — no action needed |
| 30–60% | Good window for intentional compaction |
| 60–80% | Consider starting fresh at natural task boundaries |
| 80–95% | Begin wrapping up — don't start new sub-tasks |
| 95%+ | Boot a new agent immediately |

**Important nuance:** Context *type* matters more than context *volume*. An agent at 30% context filled with highly relevant domain examples is in better shape than one at 30% context filled with log output. The number tells you utilization; it doesn't tell you about quality.

---

### Context Strategies

**Proactive Compaction — Compress Early, Not Late**

The common failure pattern is "emergency compression" — waiting until the context is nearly full, then trying to summarize everything at the last minute. This produces what's called **brevity bias**: the rushed summarization collapses all the nuance and domain-specific detail into generic, vague summaries. You lose the good stuff.

Better approach: deliberately compress at 40-60% utilization. At that point you have time to summarize thoughtfully, preserve key decisions and reasoning, and discard genuine noise. Proactive compaction preserves quality. Reactive compaction destroys it.

**Structured Over Prose**

Markdown, JSON, and XML consistently outperform unstructured prose in context. Structured formats help agents:
- Quickly locate specific information without reading everything
- Parse expected data into clear categories
- Understand the relationship between pieces of information

Dumping paragraphs of prose into context forces the agent to process everything linearly. Structured formats let it jump directly to what's relevant.

---

### Advanced Context Patterns

**Progressive Disclosure — Loading Information in Tiers**

Instead of loading all available information at once, load metadata first, then full content only for what's actually needed.

*Tier 1 — Metadata:* Names, descriptions, summaries. ~50-200 characters per item. Load all of them upfront.
*Tier 2 — Full content:* Complete documentation for items that were selected. ~500-5,000 words each. Load only for selected items.
*Tier 3 — Detailed resources:* Supporting files, source code. Unbounded. Load only when specifically needed.

**The token economics make this compelling:**
- 10 knowledge items × 1,000 tokens each = 100,000 tokens (loading everything)
- Progressive disclosure: ~5,000 tokens (metadata + the one selected item)
- 20× reduction in token usage with full access to all 10 items

*Use when:* large knowledge bases, multi-domain expertise, tight context budgets.
*Skip when:* small static knowledge sets, all information is always needed.

---

**Context Loading vs. Context Accumulation**

There are two mental models for how context is built:

**Accumulation (the default):** Context grows over time as a log — everything that happened gets appended. The context is whatever has accumulated.

**Loading (the payload model):** For each agent invocation, deliberately construct exactly the right context for that specific call. Base config + project context + only the relevant tools + the query + retrieved facts. Nothing else.

| Accumulation | Payload Model |
|---|---|
| "What has accumulated?" | "What must I include to succeed?" |
| Context as an append-only log | Context built fresh for each call |
| Grows and degrades over time | Precise and purpose-built |
| Easy to implement | Requires deliberate design |

The payload model explains why small models can work well in orchestrator patterns: the orchestrator handles the complex accumulation; scouts and specialists receive clean, curated context loads with only what they need.

---

**The ACE Framework — When Bigger Context Is Better**

Conventional wisdom says "shorter is better." The ACE (Agentic Context Engineering) framework challenges this for knowledge-intensive domains.

The claim: for complex domains (medical, legal, scientific, large codebases), a comprehensive evolving playbook in context *outperforms* compressed prompts. The agent doesn't have to rediscover patterns — they're all there in the playbook.

The three-role structure:
- **Generator:** Executes tasks using the current playbook
- **Reflector:** Analyzes outcomes and extracts new learnings
- **Curator:** Evolves the playbook based on reflections

Playbook entries include usage metadata so the system knows what's working:
```markdown
## Authentication Patterns

- [AUTH-001] Use JWT tokens for stateless sessions
  Helpful: 12 | Harmful: 1

- [AUTH-002] Validate tokens on every API call
  Helpful: 15 | Harmful: 0
```

Results: +12.5% on the AppWorld benchmark, 82.3% latency reduction compared to an alternative approach. The paradox: larger, well-structured contexts execute *faster* because the agent doesn't waste time rediscovering patterns through trial and error.

---

### Multi-Agent Context Management

**Context Isolation — Why Each Agent Gets Its Own Window**

In multi-agent systems, each subagent operates with its own separate, independent context window. The orchestrator doesn't share its context with subagents, and subagents don't see each other's contexts.

Why this matters:
- **Prevents contamination:** One agent's hallucinations or errors can't spread directly to another agent's context
- **Enables true parallelism:** Agents can run simultaneously without interfering with each other
- **Natural compression boundary:** When subagents return results to the orchestrator, they summarize — creating an automatic compression point
- **Fresh starts at scale:** Each new subagent starts clean, not burdened by the history of previous work

**The cost:** Multi-agent context isolation uses approximately **15× more tokens** than a single-agent approach (Anthropic Engineering, "How we built our multi-agent research system," 2025 — token usage explained 80% of performance variance). You're paying for quality and reliability, not speed — both single-agent and multi-agent approaches achieve similar latency on complex tasks (~40 seconds). The value is deterministic quality and zero variance across runs.

**Explicit context forking in practice:**
```yaml
---
name: isolated-researcher
context: fork
tools: Read, Grep, Glob, WebFetch
---
```
This subagent starts with a completely fresh context — no parent history carries over. Results return as a synthesized summary, not raw data.

---

**Persistent State vs. Ephemeral Context**

Context is temporary — it disappears when the session ends. For information that needs to survive across sessions or be shared between agents, you need **persistent state** (external storage).

| Ephemeral Context | Persistent State |
|---|---|
| Lives for one session | Survives restarts |
| One agent's private working memory | Sharable across agents and sessions |
| Failure mode: context fills up, degrades | Failure mode: stale or incorrect data |

**What belongs where:**
- *Context:* Current task details, recent tool outputs, working hypotheses, intermediate reasoning steps
- *State:* User preferences, conversation history, accumulated learnings, corrections from past mistakes

**The memory contamination risk:** If one agent writes a hallucination to shared state, that false information becomes "ground truth" for every agent that reads it later. Defenses: write validation gates, source attribution, periodic audits of shared state.

---

## 6. Tool Use

### What Are Tools?

Tools are the mechanisms through which agents take actions in the world. Without tools, an LLM can only generate text. With tools, it can:
- Read and write files
- Execute code
- Search the web
- Query databases
- Call external APIs
- Spawn other agents

Every tool call works the same way: the model decides to use a tool, generates a structured tool call (the tool name + parameters), your application intercepts it, executes the actual action, and returns the result back to the model's context.

One architectural nuance worth internalizing: **the model never directly executes a tool.** It generates a structured request — essentially a JSON blob saying "call this tool with these parameters." A separate orchestration layer (your application code) receives that request, validates it against permissions and constraints, and then executes it. This separation is intentional. It means you can inspect, log, throttle, or reject any tool call before it happens — the model's intent and the actual execution are distinct steps with a control point between them.

---

### Designing Good Tools

The quality of your tool descriptions directly determines whether the model will use them correctly. A tool with a vague description will be misused — or ignored entirely.

**Include examples — they transform performance.** JSON schemas tell the model what structure a tool call should have, but they can't teach *when* or *how* to use it. Examples fill that gap. Research showed that adding concrete examples improved tool call accuracy from 72% to 90%.

The ideal example set has three levels:
1. *Minimal case* — the simplest valid usage (shows the floor)
2. *Partial case* — using some parameters but not all (shows selective usage)
3. *Full case* — using all features together (shows the ceiling)

Use realistic data in examples, not placeholder names like `"example_user"` or `"test_value"`. Focus examples on the ambiguous cases, not the obvious ones.

**Always include "When NOT to use" in descriptions:**

```markdown
### search_codebase
Use when: You need to find where something is defined or used across files
Do NOT use for: Reading the full contents of a specific file (use read_file instead)
```

Without this, models frequently call the wrong tool when multiple tools have overlapping-seeming names. The "Do NOT use for" section is the single most effective addition for preventing the most common misuse patterns.

**Self-documenting names:** Use domain-specific prefixes that make the action unambiguous: `git_commit`, `git_push`, `db_query`. Avoid versioned names that obscure purpose: `finder_v2`, `processor_new`. When two tools have similar functionality, include explicit comparison tables in their descriptions.

---

### Tool Selection — How the Model Chooses

Tool selection is reasoning, not keyword matching. The model reads your tool names and descriptions, understands the current task, and reasons about which tool serves that task. This means the quality of your descriptions directly controls selection accuracy.

**Reducing the tool pool for better accuracy:**

As the number of available tools grows, selection accuracy *declines*. This is Context Confusion (see the Context Engineering doc): too many options means the model has to process more irrelevant information.

Rule of thumb: **more than ~50 tools degrades selection performance.** When you're approaching this threshold, implement:

- **Role-based filtering:** Not every agent needs every tool. A research agent doesn't need deployment tools.
- **Dynamic discovery:** Only load tool definitions that are relevant to the current task
- **Skill-based activation:** Load specialized tool sets on demand when entering a specialized workflow phase

**The production pattern: decision trees first, model second.**

Not every decision should run through the LLM. In production agents, the right architecture is to handle routine, high-confidence cases with deterministic logic — simple if-else trees or rule-based lookups — and only invoke the model when genuine ambiguity exists. This avoids burning tokens and adding latency on decisions that don't actually require reasoning. Routing a support ticket to the billing team doesn't need an LLM; recognizing that a request is ambiguous between two departments does. Structure your agent so the model is a last resort for hard cases, not the default path for every case.

**A specific trap: extended reasoning in tool selection.** If you're using a reasoning-class model (o3, Claude Sonnet with extended thinking, etc.), resist the instinct to give it high thinking budgets for tool-calling loops. Empirical research shows that excessive reasoning tokens degrade function-calling accuracy: brief reasoning (8–32 tokens) improves selection reliability, while extended reasoning (128+ tokens) causes the model to second-guess itself, hallucinate nonexistent tools, and make worse choices. Keep reasoning budgets low in tight tool-selection loops and reserve extended thinking for the planning and validation layers, not the execution layer.

---

### The Meta-Cognitive Tool Arbitration Problem

Designing good tools is only half the battle. The other half is designing agents that *know when not to use them*.

A common pathology in agentic systems is "blind tool invocation" — the agent reflexively calls tools even when its internal knowledge is sufficient to answer the question. This looks like wasted computation on the surface, but it's actually a deeper reasoning failure: the agent lacks the meta-cognitive capability to compare internal knowledge against task requirements and recognize that external tool use is unnecessary.

**Why this is hard to solve with standard RL approaches:**

Standard reinforcement learning tries to address this with a scalar reward that penalizes tool invocations. But this creates an unsolvable optimization problem: an aggressive penalty suppresses essential tool use (the model becomes too conservative), while a mild penalty gets overwhelmed by variance in the accuracy reward signal during advantage normalization — rendering it ineffective at preventing overuse.

**The dual-channel solution:**

Rather than combining accuracy and efficiency into a single scalar objective, decouple them into two independent optimization channels:

1. **Accuracy channel:** Maximizes task correctness — standard RL objective, allows any behavior that produces correct answers
2. **Efficiency channel:** Enforces execution economy *exclusively within accurate trajectories* — only penalizes tool overuse when the answer is correct

This separation means the model can't trade accuracy for efficiency (aggressive tool reduction can't hurt correctness), but it can discover minimal-tool paths within the set of correct solutions. Empirical results: this approach reduces unnecessary tool invocations by orders of magnitude while simultaneously improving reasoning accuracy.

**Practical implication for your agent design:**

If you observe your agents calling tools gratuitously, the problem isn't usually the tool descriptions — it's the training signal. Standard RLHF won't capture the "know when not to use tools" objective. Consider whether your reward function explicitly incentivizes efficiency *only when accuracy is maintained*. If you're training agents that interact with external systems, this distinction becomes critical: unnecessary API calls are not just wasteful, they're a failure of agent reasoning.

---

### Tool Restrictions as Security Boundaries

This is a critical architectural principle: treat tool access permissions like production security — **deny all by default, explicitly allowlist only what each agent needs.**

Different agent roles should have different tool sets, by design:

| Agent Role | Tools | Why This Restriction |
|---|---|---|
| Reviewer/Analyzer | Read, Grep, Glob | Read-only — cannot introduce changes |
| Test Runner | Bash (tests only), Read, Grep | Can execute, cannot modify code |
| Builder/Implementer | Read, Edit, Write, Grep, Glob | Full modification for the task |
| Orchestrator | Task, Read, Glob | Routes work, has minimal direct access |
| Scout/Explorer | Read, Grep, Glob, WebFetch | Discovery only — cannot modify |

**Why this matters beyond security:** Restrictions enforce architectural intent. A scout agent that can't edit files is *architecturally forced* to report its findings back — it cannot "helpfully" modify things while investigating. Tool restrictions make the right behavior the only possible behavior.

**Common mistake:** Giving all agents full tool access "for flexibility." This creates permission sprawl, increases the blast radius of mistakes, and confuses the model (why does a reader have write access?). Start restrictive and expand only when you can demonstrate a specific need.

---

### Scaling Tool Use

**Dynamic tool discovery for large tool libraries:**

A typical MCP setup (MCP is a standardized protocol for connecting agents to external services) integrating GitHub, Slack, Sentry, Grafana, and Splunk consumes approximately **55,000 tokens just in tool schemas** — before you've added any task information. That's a massive context tax.

The solution: defer tool definition loading. Instead of loading all schemas upfront, load them only when a tool is discovered as relevant through a search mechanism.

*Result:* 85% reduction in tool-related token usage while maintaining access to the full tool library.
*When to use it:* 20+ tools or multiple MCP servers. Under 20 simple tools, eager loading is fine.

**Programmatic tool orchestration:**

For workflows requiring 3+ dependent tool calls, generate code that orchestrates those calls in a sandboxed environment. The results process in-place rather than each tool result re-entering the agent's context.

*Result:* 37% token reduction on multi-tool workflows.
*Use when:* parallel operations that need filtering/transformation, large datasets that would overwhelm the context.

---

### Building Efficient MCP Tools

Most MCP servers are built as transparent API pass-throughs: the tool calls the API, dumps the full response into context, and lets the model sort out what's relevant. This feels easiest to build, but it's expensive to run. API responses are designed for human consumption — they return every field, every nested object, every bit of metadata a developer might want. Most of it is irrelevant to what the agent needs right now, and it all burns context.

Three design principles that fix this at the source:

**1. Filter at the source — return only essential fields**

Strip irrelevant fields inside your tool code before returning the result to the model. Don't rely on prompt instructions like "ignore the extra fields" — the model still has to read them first.

Real example: a financial account tool returning 18 fields per account, reduced to 6 (id, name, type, on_budget, closed, balance). Token reduction: 65%. The model gets exactly what it needs for the task and nothing else.

Default to minimal fields. If edge cases need more detail, expose them through optional parameters rather than always returning the full payload.

**2. Pre-aggregate data — compute summaries server-side**

When the task involves analysis across many records, summarize before returning rather than returning raw records. The model can reason about a summary far better than it can reason about 500 individual rows — and the token cost is incomparably lower.

Real example: a 6-month spending analysis returning individual transactions vs. monthly summaries. Token count: 4,890 → 262 (94.6% reduction). The summary answered the user's actual question; the raw transactions would have answered a different one.

**3. Work within API constraints creatively**

When the API you're wrapping doesn't have a direct endpoint for what the user needs, build a multi-step workaround using the operations that do exist. Don't expose the limitation as a tool limitation — design the workflow around it.

**The hidden cost of tool definitions themselves**

This is easy to overlook: tool definitions — the schemas and descriptions you write so the model knows what each tool does — consume context even when the tools aren't being called. In a real production session with multiple MCP servers connected, tool definitions consumed **24% of the total context window** before a single task message was sent.

This reinforces the dynamic tool discovery approach: load tool schemas only when a tool has been identified as relevant, not all at once at session start.

---

### Tool Lifecycle — Revisit as Models Improve

Most tool design advice focuses on what to add. There's an equally important question that's easier to miss: **what should you remove or replace as model capabilities increase?**

Tools are built against the model you have at the time. A tool designed to scaffold a weaker model can become a constraint for a stronger one. The Claude Code team experienced this directly: early Claude needed a TodoWrite tool and periodic system reminders to stay on task. As the model improved, those reminders started working against it — Claude interpreted them as a signal that it couldn't modify the plan, limiting the adaptive behavior the newer model was actually capable of. The scaffolding had become a cage.

The lesson: periodically audit your existing tools against the model you're running now, not the model you designed for. Ask not just "are there gaps in what my agent can do?" but also "are there tools that are now constraining behavior that the current model handles better on its own?" What was scaffolding six months ago may be deadweight — or worse, an active constraint — today.

---

### Skills — Tools That Modify Behavior

**Skills** are a distinct category from regular tools. Regular tools *do things* (read a file, call an API). Skills *change how the agent reasons* — they inject specialized instructions and context that modify the agent's approach to a domain.

| Aspect | Regular Tools | Skills |
|---|---|---|
| What they do | Direct actions (read, write, call) | Inject instructions + change permissions |
| How they're activated | Algorithmic matching | LLM reasoning about descriptions |
| Token cost | ~100 tokens | ~1,500+ tokens |
| Purpose | Execute specific operations | Specialize agent behavior for a domain |

Skills trade higher token overhead for contextual specialization. The model discovers capabilities through skill metadata, then loads full skill instructions only when needed — a form of progressive disclosure applied to behavior.

**Choosing the right abstraction:**

| Feature Type | Token Cost | Use When |
|---|---|---|
| Tools | ~100 | One-time actions, simple retrieval |
| Skills | ~1,500+ | Weekly+ repeatable workflows, or when autonomous activation helps |
| Subagents | Full conversation | Parallel work streams, context isolation needed |
| MCP Servers | 10,000+ | Continuous data access, rich external integrations |

---

### Automated Harness Optimization: Systematic Discovery of Model Wrapping Patterns

The "harness" is the code wrapper that surrounds your model — how you structure prompts, format input, manage execution state, retrieve context, and present output. For agentic systems, the harness encodes critical decisions about (1) how you present goals and constraints to the agent, (2) how you represent tool schemas and execution traces, (3) how you structure multi-turn history, (4) what retrieval strategy you use, and (5) what feedback loops you implement.

In practice, harness design is almost always manual. You write a prompt, test it, tweak it based on failures, and ship it. This works, but it's suboptimal. The harness — the *structure* of how information is presented — profoundly affects model reasoning, yet optimization frameworks treat it as a black box or ignore it entirely.

Lee, Nair, Zhang, Lee, Khattab, and Finn (2026) demonstrate that systematic automated harness optimization outperforms manual baselines by significant margins. The method: use an agentic proposer that can access source code, prior evaluation scores, and execution traces to search over harness variations. The key insight that makes this work: **preserve implementation-level details across iterations**. Text-based feedback optimization fails because LLM outputs are compressed — you can't deduce from a failure message whether to modify prompt tone, reasoning structure, or retrieval strategy. Execution traces (where the model struggled) reveal the pattern directly.

#### The Harness Optimization Problem

Manual harness design is a lossy process. You observe that accuracy is 70% on a task, but the failure message (e.g., "incorrect answer") doesn't specify which harness component caused the failure. Is it:
- The instruction phrasing? (change wording)
- The step-by-step reasoning format? (modify CoT structure)
- The context being retrieved? (change retrieval strategy)
- The feedback loop design? (add self-correction)

Each of these requires a different structural change to the harness. A human designer guesses and iterates. A systematic approach analyzes *where in the reasoning process* the failure occurred (execution traces), then proposes targeted harness modifications.

**Why this matters for agentic systems:** Agents are sensitive to harness structure. An agent optimized for planning-heavy workflows (where you want extensive internal reasoning) may fail on action-heavy tasks (where you want rapid tool selection). A harness optimized for retrieval-augmented generation doesn't transfer to code generation. The harness isn't generic; it's task-family-specific.

#### The Meta-Harness Architecture

The system operates through a **filesystem-mediated iterative search** pattern. Unlike gradient-based optimization (which requires differentiable functions) or text-based feedback optimization (which loses implementation details), Meta-Harness preserves full harness code and execution history as observable state.

**Filesystem-Mediated Search Loop:**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Initialize: Sample diverse harness candidates          │
│    (baseline + mutations of prompt structure, CoT format, │
│     retrieval integration, feedback loops)                  │
├─────────────────────────────────────────────────────────────┤
│ 2. Execute: Run each harness variant on representative    │
│    benchmark tasks (100-500 examples per harness)         │
├─────────────────────────────────────────────────────────────┤
│ 3. Score: Collect performance metrics (accuracy, latency, │
│    token efficiency, failure patterns)                     │
├─────────────────────────────────────────────────────────────┤
│ 4. Analyze: Extract execution traces from failed cases     │
│    (where in the reasoning chain did it break?)            │
├─────────────────────────────────────────────────────────────┤
│ 5. Propose: Agentic proposer analyzes:                     │
│    - Source code of top-performing harnesses              │
│    - Historical scores (what worked before?)              │
│    - Execution traces (failure patterns)                  │
│    → Generate improved candidates via mutation            │
├─────────────────────────────────────────────────────────────┤
│ 6. Filter: Rank candidates by improvement potential        │
│    (score improvement vs. prior generation)                │
├─────────────────────────────────────────────────────────────┤
│ 7. Repeat: Cycle until convergence (or budget exhausted)   │
└─────────────────────────────────────────────────────────────┘
```

The critical decoupling: harness generation (proposer thinking about structure) is separate from execution (actually running the harness). This allows the proposer to analyze what worked without being constrained by execution time.

#### Harness Patterns Discovered

Systematic search reveals recurring structural patterns that maximize performance across task families:

**Pattern A: Explicit Step Structuring (Chain-of-Thought Variants)**

```python
# Structure matters as much as content
prompt_explicit = """Solve this step by step.
1. First, analyze the problem—what are the inputs, outputs, constraints?
2. Then, reason through the solution—apply relevant knowledge.
3. Finally, state your answer clearly."""

prompt_implicit = "Solve: " + problem
# Same problem, different accuracy: explicit 78%, implicit 62%
```

The structured format forces intermediate reasoning visibility. The model can't collapse to a final answer without articulating reasoning steps. This forces grounding.

**Pattern B: Self-Correction Scaffolding**

```python
prompt_with_feedback = """Solve the problem.
Check: Is this correct? Walk through the logic.
If not correct, revise.
Final answer: (after revision)"""
```

Builds in a verification step. Empirically: +5-8% accuracy on problems where the model's first attempt is often wrong but self-correctable.

**Pattern C: Retrieval-Augmented Reasoning**

```python
prompt_with_context = """Context from documents: {retrieved_docs}

Use this context to answer: {question}

If the context doesn't contain relevant information, 
state that explicitly before answering from your knowledge."""
```

The explicit instruction about when *not* to use context prevents context hallucination (using irrelevant documents as if they're authoritative).

**Pattern D: Tool Execution Traces in Context**

```python
# For agentic systems—include prior tool execution history
agent_prompt = """Past tool outputs:
{tool_trace}

Next step: Based on what you've learned from prior tools, 
decide what to do next."""
```

Execution traces (not summaries) preserve the full reasoning path. Agents can see exactly what prior tools returned, not a compressed summary.

**Pattern E: Constraint Reinforcement**

```python
prompt_with_constraints = """Task: {task}

Hard constraints:
- Never use tool X for tasks involving sensitive data
- Always validate outputs with tool Y before returning
- Maximum 3 tool calls (then return best-effort answer)

Soft preferences:
- Prefer tool A (faster, 95% accuracy)
- Only use tool B if A fails"""
```

Clear separation of hard constraints (non-negotiable) and preferences (optimize but don't violate). Models follow hard constraints; soft preferences are optimization targets.

These patterns aren't discovered through intuition — they emerge from systematic search. A harness optimized for one task family rarely transfers to another, suggesting patterns are task-specific. A harness optimized for retrieval-heavy tasks (accuracy-focused) differs from harnesses optimized for code generation (structure-focused).

#### Why Text-Based Optimization Fails

This is the core mechanism that makes Meta-Harness necessary. Standard text-based optimization (like TextGrad or other gradient-free methods) tries to improve prompts by:

1. Running the current harness
2. Observing failure message (e.g., "model produced wrong answer")
3. Using that feedback to propose text improvements

**The problem:** LLM outputs are compressed. A failure message like "incorrect" doesn't reveal which harness component caused the failure. Multiple distinct harness changes could produce the same failure for different reasons:

| Failure: "Incorrect Answer" | Possible Harness Causes | Fix |
|---|---|---|
| Model misunderstood the problem | Constraint phrasing unclear | Reword constraints |
| Model couldn't reason through steps | CoT structure too loose | Add explicit step numbering |
| Model used irrelevant context | Retrieval strategy wrong | Change which documents retrieved |
| Model computed wrong intermediate step | No verification step | Add self-correction loop |
| Model forgot early constraints | Constraint buried in context | Move constraint near task |

Text-based optimization can only improve *content* (word choice, examples), not *structure* (whether steps are numbered, where constraints appear, how context is integrated). Harness engineering is mostly structure.

**Meta-Harness solves this by using execution traces.** Instead of relying on final outputs, the system captures:
- Token-level probability distributions (where the model was uncertain)
- Attention patterns (which parts of context influenced decisions)
- Intermediate "thoughts" (if the harness includes reasoning steps)

From these traces, the proposer identifies the exact point where the model went astray: "Attention scattered across context when it should have focused on the constraint on line 12." That's actionable. It leads to moving the constraint earlier, using explicit bracketing `[CONSTRAINT: ...]`, or reducing context noise.

**The empirical finding:** Systems using text-based feedback achieve ~3-5% accuracy improvement. Systems using execution trace-based feedback achieve 8-18% improvement on the same tasks. Execution traces compress less; they preserve implementation-level detail.

#### Empirical Results

**Context Reduction:**
- Baseline harnesses developed manually: 2,000–5,000 tokens of instructions
- After optimization: 30–50% reduction while maintaining or improving accuracy
- Example: "Irrelevant chain-of-thought steps removed by identifying which steps the model never attended to. Latency improved 45%."

**Accuracy Gains by Task Family:**

| Task Family | Baseline → Optimized | Improvement | Typical Budget |
|---|---|---|---|
| Retrieval/RAG (T-Bench) | 71% → 83% | +12–18% | 1,500 evals |
| Code Generation (SWEBench-like) | 62% → 70% | +8–15% | 2,000 evals |
| Math Reasoning (IMO-level) | 45% → 52% | +7–15% | 1,200 evals |
| Long-horizon Planning (10+ steps) | 38% → 42% | +4–8% | 2,000 evals (diminishing) |

**Cross-Task Transfer:** Only 60–75% of gains transfer to unseen task families. A harness optimized for retrieval doesn't transfer to code generation despite architectural similarities. This suggests pattern discovery is task-family-specific, not universal.

**Cost-Benefit Threshold:** Harness optimization becomes cost-effective when the same harness is deployed to 100k+ inferences. For a single one-off task, manual tuning is faster. For production systems serving repeated task types, automated optimization ROI is clear.

**Efficiency Metrics:**
- Search budget to convergence: 500–2,000 harness evaluations
- Search cost: 10–20% of downstream inference cost on production workloads
- Practical implication: Invest in optimization for high-traffic task families; manual tuning for rare one-offs.

#### Implementation Workflow — Three Phases

**Phase 1: Baseline & Task Definition (Days 1–2)**

✓ *Validated by Meta-Harness empirical study on 8 task families (T-Bench, SWEBench, math, planning)*

1. Define the task family and success metric
   - "Code generation task, evaluated by pass@1 on SWEBench-like benchmarks"
   - Not: "Make code generation better"
   - **Why:** Optimization target must be concrete and measurable.

2. Establish a baseline harness
   - Start with a reasonable manual harness (what a human engineer would write)
   - Document its performance: accuracy, latency, token usage
   - This becomes the control. Optimization is only valuable if it beats this baseline.
   - **Why:** Prevents "optimizing into local optima" — you know what baseline behavior is.

3. Prepare evaluation data
   - 100–500 representative examples from the task family
   - Split: 80% for optimization search, 20% held-out for final validation
   - **Why:** Held-out set prevents overfitting to the optimization data.

4. Set optimization budget
   - Small: 500 harness evaluations (fast iteration, ~6 hours)
   - Medium: 1,500 evals (~18 hours, typical production choice)
   - Large: 2,000+ evals (~24 hours, worth it for high-traffic services)
   - **Why:** More evals = better optimization, but with diminishing returns. Paper shows 80% of gains by 1,000 evals.

**Phase 2: Automated Search (Days 3–5)**

✓ *Validated by Meta-Harness: Proposer mechanism, mutation strategies, ranking*

1. Initialize harness pool
   ```python
   base_harness = load_baseline()
   pool = [base_harness]  # Always keep baseline
   
   # Generate mutations: prompt variations, structure changes
   for _ in range(100):
       # Mutation strategies:
       # - Reorder steps in CoT
       # - Add/remove context sections
       # - Change constraint phrasing
       # - Adjust retrieval integration
       mutant = apply_random_mutation(base_harness)
       pool.append(mutant)
   ```
   **Why:** Diversity in initial pool prevents settling into local optima.

2. Run evaluation loop
   ```python
   for iteration in range(budget // batch_size):
       # Evaluate all candidates
       scores = {h: evaluate(h, task_examples) for h in pool}
       
       # Keep top performers
       top_harnesses = sorted(scores.items(), 
                              key=lambda x: x[1])[:10]
       
       # Extract patterns from top performers
       patterns = extract_patterns_from_code(top_harnesses)
       # (e.g., "top harnesses all move constraints to start")
       
       # Generate new candidates by combining patterns
       candidates = []
       for pattern in patterns:
           for harness in top_harnesses:
               mutant = apply_pattern(harness, pattern)
               candidates.append(mutant)
       
       # Keep diverse set: top performers + new candidates
       pool = top_harnesses + sample(candidates, 100)
   ```
   **Why:** Iterative refinement + pattern extraction prevents brute-force search.

3. Monitor observable signals during search
   - **Convergence:** If top score doesn't improve for 3 consecutive iterations, search is stalled. Stop or increase mutation radius.
   - **Diversity:** Track how many *unique* harness structures are in the top-10. Low diversity (everyone's using the same structure) suggests premature convergence.
   - **Accuracy plateau:** If accuracy improvement < 1% per 100 evals, stop. Diminishing returns set in.

**Phase 3: Validation & Deployment (Day 6–7)**

✓ *Validated by Meta-Harness: Held-out test performance, transfer testing, deployment gates*

1. Evaluate final harness on held-out test set
   ```
   final_harness = pool.best()
   final_accuracy = evaluate(final_harness, test_examples)
   baseline_accuracy = evaluate(baseline_harness, test_examples)
   
   improvement = (final - baseline) / baseline
   ```
   **Gate:** Require > 2% improvement on held-out set. If not met, optimization didn't generalize; use baseline instead.
   **Why:** Prevents overfitting to the optimization data.

2. Test transfer to related task families
   - If you have related tasks (e.g., retrieval tasks A and B), test if harness optimized on task A performs well on task B
   - Expected: 60–75% transfer
   - **Gate:** If transfer < 50%, harness is over-specialized. Consider rerunning search with mixed task examples.

3. Measure production impact
   - Deploy to 5% traffic for 24 hours
   - Monitor: accuracy drop threshold (> 2% = rollback), latency (> 10% increase = investigate), cost per inference
   - **Why:** Production data distribution may differ from benchmark data.

4. Gradual rollout
   ```
   Day 1: 5% traffic
   Day 2: 25% traffic (if no degradation)
   Day 3: 50% traffic
   Day 4: 100% traffic
   ```
   **Why:** Catches tail cases and distribution shifts before full rollout.

#### Observable Signals for Production Monitoring

Once deployed, monitor these signals continuously. They reveal when harness performance is degrading or when re-optimization is needed.

**Real-Time Signals (checked every hour):**

- **Accuracy trend:** Track rolling 24-hour accuracy. Threshold: > 2% drop triggers alert. If persistent (> 48 hours), prepare rollback.
- **Token efficiency:** Measure tokens per inference. Threshold: > 10% increase indicates potential harness drift or task distribution change.
- **Latency tail:** Monitor 95th percentile latency. Threshold: > 15% increase suggests the harness is causing longer reasoning chains than expected.

**Daily Signals (aggregated, checked daily):**

- **Failure pattern clustering:** Analyze which types of inputs cause failures. If a new failure pattern emerges (e.g., previously unseen input type), task distribution may have shifted. Threshold: > 5% of failures in a new category.
- **Model confidence variance:** Track whether the model's self-reported confidence (if included in harness) matches actual accuracy. High variance (confident but wrong, or uncertain but right) suggests harness is miscalibrating the model.

**Weekly Signals (trend analysis):**

- **Accuracy drift:** Acceptable range: ±1% weekly. If accuracy drops > 1% weekly, re-optimize candidate harnesses are queued.
- **Cost per accuracy point:** Divide weekly cost by accuracy percentage. If this increases > 10%, either accuracy is declining or the harness is less efficient.

**Quarterly Decision Points:**

- **Re-optimize on new data:** If you've accumulated new task examples in a quarter, consider re-running the optimization loop with 1,000 evaluations.
- **Test on new model version:** When Claude or other models release new versions, test the optimized harness. If performance drops > 5%, re-optimize for the new model.
- **Expand to new task families:** If you've added new related tasks, test whether the harness transfers. If transfer < 50%, run targeted optimization for the new family.

#### Failure Modes & Practical Limits

**1. Cross-Task Transfer Ceiling (60–75%)**

Harnesses optimized on one task family show limited transfer to others:
- Harness optimized for T-Bench (retrieval): transfers at 73% effectiveness to retrieval-like tasks
- Same harness on code generation tasks: 45% effectiveness (significant gap)

**Implication:** You can't optimize once and ship everywhere. Either: (a) optimize per task family, or (b) optimize on a mixture and accept ~15% quality degradation on specialized tasks.

**2. Model Overfitting**

Harnesses sometimes become tightly coupled to specific model architectures:
- Harness optimized on Claude 3.5: achieves stated performance
- Same harness on GPT-4: 8–12% accuracy loss
- Same harness on DeepSeek: 5–10% accuracy loss

**Implication:** If you plan to support multiple models, either: (a) optimize separately per model, or (b) include model version in optimization objective (optimize across 2–3 models jointly, accepting some loss for each).

**3. Instruction Sensitivity**

Even in "optimized" harnesses, minor wording changes cause variance:
- "Solve step by step" vs. "Solve the problem step by step" → 5–10% accuracy variance
- Order of constraints ("Never use tool X" at top vs. buried) → 3–8% variance

**Implication:** Optimized harnesses aren't robust to small changes. Treat them as fixed once deployed. If you need to modify (add a new tool, update a constraint), re-run optimization.

**4. Long-Horizon Reasoning Bottleneck**

Harnesses for tasks requiring > 10 reasoning steps show diminishing optimization returns:
- 5-step tasks: +15–18% improvement typical
- 10-step tasks: +8–12% improvement
- 20+ step tasks: +4–8% improvement

**Implication:** For complex multi-step agent workflows, harness optimization has limits. Other levers (better models, stronger tool design, explicit planning structure) may provide more value.

**5. Computational Cost**

Optimization budget (500–2,000 evaluations) is only economical for:
- High-traffic tasks (100k+ inferences per month)
- Repeated task families (not one-off analysis)

For bespoke or infrequent tasks, manual tuning is faster.

#### Practical Application to Agentic Systems

How does harness optimization apply to agents specifically?

**For Agent Planning:** Agents that require extensive reasoning benefit from CoT structure optimization. A planning agent optimized with explicit step numbering and intermediate reasoning capture can achieve +8–15% improvement in multi-step task completion.

**For Tool-Using Agents:** Tool invocation is sensitive to how tool descriptions and prior execution traces are presented. Optimization can discover the right balance: how much trace history to include (too much causes confusion; too little causes tool misuse), how to format tool schemas (structured vs. prose), when to include tool usage examples.

**For Retrieval-Augmented Agents:** RAG agents are highly sensitive to how context is integrated. Optimization can discover: (a) the optimal retrieval strategy (keyword vs. semantic; how many documents), (b) how to format context to prevent hallucination (explicit demarcation, source attribution), (c) when to use context vs. agent's training knowledge.

**For Multi-Turn Agents:** Agents that maintain state across turns can benefit from harness optimization on how conversation history is integrated, when to compress history, how to handle contradictions between history and new information.

**Integration with Planning:** Use harness optimization as the final phase of agent development. Follow this sequence:

1. **Baseline agent** — implement with reasonable harness (manual design)
2. **Test on benchmarks** — measure baseline accuracy
3. **Optimize harness** — run 1,000–2,000 evaluations on representative tasks
4. **Deploy** — ship optimized harness with gradual rollout
5. **Monitor & re-optimize quarterly** — as task distribution shifts, re-run optimization

This approach treats harness as a tunable dimension alongside model selection and tool design — a first-class part of the system optimization surface.

---

## 7. Patterns

### Research-Perspective: The Four-Module Agent Architecture

Academic research on LLM agents has converged on a four-module conceptual model that complements the practitioner Four Pillars framework. Where the Four Pillars (prompt, model, context, tools) describe the engineering components you build and configure, this four-module model describes the cognitive functions an agent must perform:

**Profiling Module** establishes the agent's identity and operational role. In engineering terms, this is what you define in the system prompt — but framed functionally, it answers: who is this agent and how does it approach problems? Profiles can be handcrafted for precise control, generated by the LLM for scalability, or derived from dataset alignment for domain authenticity. The profiling module explains why a research agent and a support agent exhibit completely different reasoning styles even when using the same underlying model.

**Memory Module** mirrors human memory architecture across three tiers: **sensory memory** (the current context window — immediate inputs the agent is actively processing), **short-term memory** (working state within a session, retained in-context), and **long-term memory** (persistent external storage that survives across sessions). This framing is useful because it maps directly to the engineering distinction between context (sensory + short-term) and persistent state (long-term). An agent without long-term memory resets completely after each session; one with it accumulates experience, corrects past mistakes, and evolves its understanding across interactions.

**Planning Module** handles task decomposition — breaking complex goals into achievable sub-tasks and sequencing them appropriately. Single-path reasoning (sequential steps from goal to execution) and Chain-of-Thought are both planning mechanisms. The planning module is what makes the difference between an agent that attempts a complex task as one monolithic action and one that decomposes it into a dependency graph of smaller actions, each more reliable than the whole.

**Action Module** translates the decisions from all three other modules into concrete world-affecting outputs. It integrates profiling (what kind of agent is this?), memory (what do I know from past experience?), and planning (what am I supposed to do next?) to select and execute the right action — whether that's a tool call, a generated response, or spawning a sub-agent.

This four-module framing is most useful for diagnosing where a specific agent failure originates. An agent that behaves inconsistently across task types likely has a weak profiling module. One that makes good decisions in early steps but degrades after long sessions has inadequate memory management. One that attempts complex tasks without decomposition has an immature planning module. One that selects the wrong tools despite understanding the task has an action module failure.

---

### How to Choose a Pattern

Agentic patterns are recurring solutions to common agent architecture problems. Choosing the right pattern for the right situation is a skill in itself.

**When in doubt, start with Plan-Build-Review.** It handles the majority of software engineering tasks well, and it's understandable enough to debug when something goes wrong.

| Task Characteristics | Best Pattern |
|---|---|
| Standard feature implementation | Plan-Build-Review |
| Production coding with mandatory process steps (lint, CI, compliance) | Blueprints |
| Complex analysis requiring multiple expert perspectives | Orchestrator |
| Information-gathering with unknown scope | ReAct |
| High-stakes irreversible operations | Human-in-the-Loop |
| Multiple independent tasks in one domain at scale | Expert Swarm |
| Complex design decisions with real tradeoffs | Multi-Agent Collaboration |
| Long-running projects requiring knowledge persistence across sessions | Persistent Agent Memory |

Patterns can be combined: an Orchestrator can coordinate parallel Plan-Build-Review workers. Human-in-the-Loop gates fit naturally at phase transitions in any pattern.

---

### Command → Agent → Skill Orchestration Pattern (Claude Code)

This is the architectural pattern for composing agentic systems in Claude Code and similar tools where you have explicit concepts for user-facing commands, autonomous agents, and reusable knowledge artifacts (skills).

**The three-layer abstraction:**

```
Command Layer (UX/Orchestration)
    ↓ routes request to
Agent Layer (Execution with memory/context)
    ↓ deploys
Skill Layer (Specialized knowledge/tools)
```

**What each layer does:**

- **Commands** handle user interaction, request routing, and result formatting. They're the "entry point" interface. Typically use lighter models (Haiku) because they're not doing reasoning work — they're coordinating.
- **Agents** execute with persistent memory, learning across sessions, and adaptive behavior. They have preloaded context (agent skills) that give them domain expertise upfront. Typically use more capable models (Sonnet, Opus).
- **Skills** are modular knowledge artifacts — domain algorithms, procedures, reference materials. They exist in two forms: preloaded (part of agent context at startup) or invoked (loaded on-demand).

**Why this beats a flat architecture:**

In a flat system, you have one agent that handles everything: user interface, decision-making, and domain knowledge all mixed together. This causes:
- Context bloat (the agent is always holding UI logic + domain knowledge)
- Scaling friction (adding a new capability requires editing the big agent)
- Determinism problems (the agent gets confused by competing instructions)

In the Command→Agent→Skill pattern:
- Commands stay small and focused on UX
- Agents stay focused on reasoning
- Skills encode knowledge independently

**Real example — Weather System (from claude-code-best-practice repo):**

```
Command: /weather-orchestrator (Haiku)
  → Routes to Agent: weather-agent (Sonnet)
    → Loads Agent Skill: weather-fetcher (preloaded instructions)
    → Invokes Skill: weather-svg-creator (on-demand SVG generation)
  → Returns formatted result to user
```

The user runs one command. That command invokes a specialized agent. The agent uses its preloaded skill + specialized tools. The SVG is generated by a separate skill. Clean separation of concerns.

**When to use this pattern:**

- Multi-step workflows requiring different levels of reasoning
- Systems where you need distinct user interfaces and autonomous behaviors
- When domain knowledge is large (use preloaded agent skills to load it once)
- Scaling scenarios where multiple agents need the same domain knowledge

**Design decision: preloaded vs. invoked skills**

For each skill, ask: *Does this agent need it on every invocation?*

- **Yes** → preloaded agent skill (part of agent context at startup, always available)
- **No** → invoked skill (loaded on-demand, lower base cost)

Example: A mining operations agent preloads "ore variability analysis" (needed constantly) but invokes "emergency halt procedure" (used only on errors).

---

### Plan-Build-Review

The default starting pattern. Most software engineering agent work fits this structure:

**Phase 1 — Research:** Investigate the codebase, gather context, understand the existing system.
**Phase 2 — Plan:** Create a concrete specification based on the research. This becomes the shared artifact.
**Phase 3 — Build:** Implement against the spec.
**Phase 4 — Improve:** Review outcomes and update expertise for the next run.

**Why research always comes first:** "Bad research compounds exponentially." If your understanding of the existing system is wrong at step 1, every subsequent decision builds on that wrong foundation. Thousands of lines of correctly-written code for the wrong system is a catastrophic outcome.

Research outputs must be concrete, specific artifacts:
- ✅ "Module X uses pattern Y — see lines 45-67 in `auth.py`"
- ❌ "The code probably does something with databases"

The first is actionable; the second is useless for planning.

**Adapting scale to task size:**

| Flow | When to Use | Phases |
|---|---|---|
| Quick Flow | Bug fixes, small prototypes | Skip research and plan; go straight to build |
| Standard Flow | Typical feature implementations | All 4 phases |
| Full Planning | New products, systems | Extended research, multiple planning rounds |
| Enterprise | Compliance-critical, regulated systems | Full flow + audit checkpoints |

---

### Orchestrator Pattern

An orchestrator is a central coordinator that invokes specialized sub-agents, synthesizes their outputs, and manages workflow transitions. Think of it as a manager who directs a team of specialists — each specialist does focused work in their area; the manager integrates the results.

```
Orchestrator (Main Coordinator)
├── Phase 1: Scout Agent (read-only exploration — learns the territory)
├── Phase 2: Planning Council (parallel domain experts)
│   ├── Architecture Expert
│   ├── Testing Expert
│   └── Security Expert
├── Phase 3: Build Agents (parallel, dependency-aware)
├── Phase 4: Review Panel (parallel experts — cannot modify what they review)
└── Phase 5: Validation Agent (runs tests, confirms correctness)
```

**The most critical implementation detail — Single-Message Parallelism:**

All agents you want to run in parallel *must* be invoked in a single message. If you invoke them in separate sequential messages, they run one after another — not simultaneously. A 10-agent swarm invoked simultaneously takes ~4 minutes. Invoked sequentially, it takes ~40 minutes. This is a 10× performance difference from one architectural decision.

**The Spec File as Shared Context:**

A single artifact flows through all phases like a baton:
- The Scout discovers the current state and documents findings
- The Planning Council creates a spec based on those findings
- Builders reference the spec while implementing
- Reviewers check compliance against the spec
- Validators verify the implementation matches the spec

This shared artifact keeps everyone on the same page without requiring agents to share contexts.

**Phase Gating — Don't Proceed on Failure:**

Before each phase transition, verify that the previous phase produced acceptable outputs. If prerequisites fail — if the spec is incomplete, if the build has critical errors — halt and provide specific remediation instructions rather than pushing forward.

**Communication principles:** The orchestrator should "absorb complexity, radiate simplicity." The user shouldn't see internal orchestration mechanics. Don't say "spawning subagents" or "executing task graph analysis" — say "breaking this into parallel tracks" and "pulling it all together now."

**When to delegate vs. read directly:**
- Orchestrator reads 1-2 files directly: quick lookups, small configs
- Delegate to sub-agents: 3+ files, codebase exploration, pattern searching

**Fundamental Limits on Delegation: The Information-Theoretic Constraint**

A deceptively simple question: when does delegating a decision to a specialist subagent actually improve outcomes compared to a centralized coordinator? The answer is: only when the specialist has access to information the coordinator doesn't.

Ao, Gao, and Simchi-Levi's 2026 formal analysis of multi-agent planning establishes a hard theoretical boundary: any delegated multi-agent system operating under finite communication capacity is *decision-theoretically dominated* by a centralized Bayes decision-maker—unless the delegated agents access new external information sources (separate sensors, local real-time data, asymmetric context).

**The mechanism is communication bottleneck.** Delegation forces agents to communicate decisions back through language, which has finite bandwidth. Every communication step introduces information loss, measurable as posterior divergence or conditional mutual information. If all agents reason over the same training data and shared context, the cost of communication loss exceeds the benefit of distribution. Empirically, LLM experiments (2026) confirm this bound holds in practice.

**Practical implication:** When architecting multi-agent systems, ask: "Do the delegated agents have access to information the orchestrator doesn't?" If no—if they operate on shared context, same training data, no special sensors or local expertise—centralization often beats distribution. Your agents pay the communication cost without gaining information advantage. Delegation wins when agents have **asymmetric information**: local expertise, different sensors, real-time data flows unavailable to the center, or specialized datasets.

**This changes how you evaluate orchestrator vs. multi-agent trade-offs.** Before distributing work across agents, establish what novel information each agent will contribute. If the answer is "just compute the same thing in parallel," you're paying for communication without information gain.

---

### ReAct Pattern (Reasoning + Acting)

ReAct (Reasoning + Acting) is an interleaved approach where the agent alternates between reasoning about the current situation and taking an action based on that reasoning:

```
Thought: "I need to understand how authentication works. Let me search for it."
Action: search_codebase("authentication")
Observation: [results]
Thought: "I found the main auth module. Now I need to see how tokens are validated."
Action: read_file("auth/token_validator.py")
Observation: [file contents]
Thought: "Now I understand the system. The bug is on line 47 where..."
Final Answer: [diagnosis and fix]
```

**Three properties that make this pattern valuable:**

1. **Grounded decisions:** Every action follows explicit reasoning about what was actually observed. The agent cannot claim to know something it hasn't retrieved — the thought step forces articulation of *why* the action is needed.

2. **Observable trace:** The thought-action-observation chain is a complete audit trail. When something goes wrong, you can read exactly what the agent was thinking when it made each decision.

3. **Adaptive:** Each observation can change the plan. Unlike a fixed multi-step plan that must be executed even if early steps reveal the plan is wrong, ReAct adjusts continuously based on what it actually discovers.

**When to use ReAct:**
- Information-gathering tasks where the scope is unknown (you don't know how many steps it will take)
- Each step depends heavily on what previous steps revealed
- Hallucination is high-risk (medical, legal, financial contexts) — grounded decisions reduce this
- Explainability matters — you need to show why each step was taken

**When not to use ReAct:**
- Well-defined procedures with a known set of steps
- High-throughput scenarios where the reasoning overhead is too expensive
- Single-tool tasks (no interleaving needed)

**Synthesis — combining ReAct and Plan-Build-Review:** Use the ReAct pattern *within* the Research phase of Plan-Build-Review. ReAct's exploratory nature is ideal for open-ended investigation; Plan-Build-Review's structured approach is ideal for execution.

**Anti-patterns:**
- *Thought-free actions:* Always generate a Thought before every Action. Skipping thoughts collapses ReAct back into ungrounded sequential tool calling.
- *Observation overload:* Tool outputs can be enormous. Summarize or truncate observations before they fill the context.
- *Infinite loops:* Set a maximum iteration count (10-20 steps). Detect when the same action is being repeated. Require an explicit "Final Answer" action to terminate.

---

### Human-in-the-Loop

Human-in-the-Loop (HITL) means strategically inserting human approval checkpoints at high-risk moments in an automated workflow. The agent can do most work autonomously; humans intervene only where judgment, risk tolerance, or authorization matters.

**Risk-Based Gate Criteria**

Not every operation needs human approval — gate fatigue happens when agents ask permission for everything, and humans start approving without reading. Reserve gates for genuinely risky operations:

| Risk Factor | Auto-proceed | Require Human Approval |
|---|---|---|
| Reversibility | Git commit (easily undone) | Database schema migration (painful to reverse) |
| Blast radius | Single file edit | Production deployment |
| Cost | Under $0.10 | Over $100 |
| Sensitivity | Internal code | Credentials, payments |
| Precedent | Routine operation | First time doing this type of operation |

**Always require approval:** Production deployments, database schema changes, external API calls with side effects, credential changes, deleting data.

**Safe to auto-proceed:** Reading files, running tests in isolated environments, creating branches, generating documentation drafts.

---

**Gate Placement Strategies**

*Pre-Action Gates:* The agent presents a plan and waits for approval before doing anything. Best for irreversible operations — you want the human to approve before the point of no return.

*Post-Action Review Gates:* The agent executes a phase and pauses for review before proceeding to the next phase. Best for complex multi-step workflows where the intermediate work is valuable regardless of what happens next.

*Checkpoint Gates at Phase Transitions (recommended default):* Gates between major phases of the workflow. The spec file serves as the approval artifact — humans review the plan, not raw code changes.

```
Research → [GATE: review and approve research findings]
Plan → [GATE: review and approve spec before implementation]
Build → [GATE: review before deployment or merge]
```

**What makes a good approval request:** Every approval request must include: (1) a clear statement of what action will be taken, (2) sufficient context to evaluate it, (3) a risk assessment with a specific rollback plan if things go wrong, and (4) explicit options — not just "approve or reject" but actual choices.

Rule: No rollback plan = not ready for approval. If you can't tell the human how to recover from this action going wrong, you haven't thought it through enough.

---

### Expert Swarm Pattern

The Expert Swarm pattern is for scaling a well-defined task across many parallel workers, while maintaining consistency through a shared knowledge file.

The structure:
```
Expert Lead (has the domain expertise)
│
├── expertise.yaml (shared knowledge file — max ~750 lines)
│
├── Worker 1 (reads expertise.yaml, handles Section A)
├── Worker 2 (reads expertise.yaml, handles Section B)
├── Worker 3 (reads expertise.yaml, handles Section C)
│   ...
└── Worker N
       ↓
Join/Synthesis Phase (verify consistency, update indexes)
       ↓
Improve Agent (updates expertise.yaml based on all worker outputs)
```

**Why pass the expertise file path, not copy the content:**

Option A — Copy expertise into each worker's context: pollutes every worker's context with 500-750 lines of knowledge they partially share. Creates synchronization problems if workers need to update it.

Option B — Pass the file path: each worker reads the file when needed. The context stays clean. All workers reference the same single source of truth. When the expertise file updates, all future workers automatically benefit.

**The Learning Separation Rule:** Workers execute tasks. An improve agent analyzes results afterward. Never let workers update the expertise file during parallel execution — that creates race conditions where two workers overwrite each other's updates.

```
Workers 1-10 run in parallel (read-only access to expertise.yaml)
        ↓
All workers complete → commit their outputs
        ↓
Improve agent analyzes all 10 worker outputs
        ↓
Improve agent updates expertise.yaml once, atomically
        ↓
Next swarm benefits from all learnings
```

**Scale evidence:** A real 10-agent swarm added 3,082 lines of code across 7 new files and 15 modified files in approximately 4 minutes wall-clock time. Sequential estimate: ~40 minutes. **10× speedup, zero consistency drift** — every output followed the same standards because all workers read the same expertise file.

**Token economics constraint:** Keep expertise.yaml under ~750 lines (~3,000 tokens). At 10 workers, that's 30,000 tokens in coordination overhead — still manageable. An unbounded expertise file breaks the pattern economically.

**Workers return summaries, not full artifacts.** The orchestrator needs confirmation of completion and a high-level summary. Returning the full output would pollute the orchestrator's context and defeat the purpose of isolation.

**When to use:** Multiple independent tasks within a single domain, consistency across outputs is critical, domain expertise is well-documented, scale justifies the coordination overhead.

**When not to use:** Simple single-file changes, tasks with sequential dependencies on each other, domain expertise not yet codified into an expertise file.

**The honest cost math — swarms are not always worth it.** Real-world data from Overstory (a production multi-agent orchestration system built by Jaymin West, the author of the agentic engineering book this doc draws from):

> 20-agent swarm: 8M tokens, $60, 6 hours
> Single agent sequential: 1.2M tokens, $9, 8 hours
> Same result. 6.6× more expensive for 25% faster.

The failure modes that drive this: errors compound multiplicatively at integration boundaries, coordination overhead consumes tokens without producing code, and independent agents produce architectural drift — inconsistent naming, duplicated utilities, conflicting assumptions. Jaymin's own conclusion: *"Most day-to-day engineering work is deeply interconnected, benefits from coherent reasoning, and is better served by a single focused agent."* Swarms genuinely win for embarrassingly parallel tasks (test generation, large-scale exploration, experiments with zero shared state). For everything else, lean toward a single focused agent first.

**Inter-agent communication — the SQLite mail pattern.** When you do need agents to coordinate, one production-tested approach is a persistent message queue backed by SQLite rather than direct process communication or shared state. Each agent sends and receives typed protocol messages (`worker_done`, `merge_ready`, `dispatch`, `escalation`) through a central database. Benefits: agents don't need to know about each other's process IDs or execution state, messages persist across restarts, and the mail log becomes a built-in audit trail of what each agent did and why. WAL (Write-Ahead Logging) mode enables concurrent reads at ~1-5ms per query without locking conflicts.

---

### Multi-Agent Collaboration

Multi-Agent Collaboration puts specialized agent personas in a shared conversation space where they respond to each other's ideas. Unlike most patterns where agents work in isolation, here agents actively build on and push back against each other's proposals.

**An example of how this plays out:**

```
User: "How should we handle authentication?"

Orchestrator selects 3 relevant personas:

  Security Expert: "Use OAuth2 with PKCE flow — it prevents authorization
                   code interception attacks."

  Architect: "Agree on OAuth2, but I'd store tokens in Redis rather than
             localStorage to prevent XSS exposure."

  Developer: "Redis adds a dependency and operational complexity. Could
             we use httpOnly cookies instead? Same XSS protection,
             simpler infrastructure."

User: "What about mobile apps? We have both web and mobile clients."

Orchestrator selects different personas...
```

Notice what's happening: agents are genuinely disagreeing, referencing each other's arguments, and the user's question steered the conversation in a new direction.

**What makes this pattern work:**

1. **Selective participation:** The orchestrator picks 2-3 relevant personas per message, not all of them. Calling all agents every time creates noise and exhausts the context.
2. **Role authenticity:** The security expert worries about security threats, not code elegance. The developer worries about implementation complexity. Authentic perspective matters.
3. **Genuine disagreement:** Forced consensus hides real tradeoffs. Let agents disagree when their perspectives genuinely conflict.
4. **Human steering:** The user isn't a passive observer — they ask follow-up questions and guide the direction at each turn.

**When this pattern helps:** Complex decisions with real tradeoffs, brainstorming, design reviews, situations where there's no single objectively correct answer.

**When it adds noise:** Execution tasks (just implement it), well-defined problems (just solve it), simple enough situations where one perspective is sufficient.

**Synthesis — when to stop exploring:** After 5-10 rounds of dialogue, the orchestrator should synthesize: (1) what all agents agree on, (2) what remains genuinely unresolved and why, (3) a recommended path forward, and (4) concrete next steps. Exploration without synthesis wastes effort.

---

### Self-Organizing Multi-Agent Systems: The Endogeneity Paradox

The dominant assumption in multi-agent design is that you should assign roles upfront: agent A handles security, agent B handles architecture, agent C implements. This assumption is wrong. A 25,000-task empirical study (Dochkina 2026) testing coordination across 8 LLM models, 4–256 agents, and 8 protocols reveals a counterintuitive finding: **systems where agents autonomously select their roles—without role pre-assignment—outperform designed hierarchies by 14% (p < 0.001), and outperform fully autonomous systems by 44% (p < 0.0001).**

This is the **endogeneity paradox**: optimal coordination emerges not from maximal external control nor maximal autonomy, but from a hybrid that provides minimal structural scaffolding (fixed ordering) while enabling full role autonomy (emergent specialization). The practical recipe is startlingly simple: give agents a **mission, a communication protocol, and a capable model**—not role assignments. The rest emerges.

#### What the Study Tested

To establish this finding rigorously, the research compared four coordination protocols:

1. **Coordinator (centralized, exogenous):** Agent 0 analyzes the task, assigns roles to all other agents, who execute in parallel. Single point of control. N+1 LLM calls.
   - Quality: 0.767 (N=16, L3 tasks)
   - Reasoning: Bottlenecked by one agent's judgment; other agents execute role instructions rather than adapting.

2. **Sequential (hybrid):** Agents process the task in fixed order. Each agent observes **completed outputs of all predecessors**, autonomously selects its role, decides whether to participate or abstain, and contributes accordingly. The ordering is fixed (exogenous), but role selection and participation are fully endogenous. N sequential LLM calls.
   - Quality: 0.875 (N=16, L3 tasks) — **+14% vs. Coordinator, +44% vs. Shared**
   - Reasoning: Provides optimal information type—factual, task-specific, accumulated results, not intentions/history/one-agent plans.

3. **Broadcast (signal-based, endogenous):** Two rounds. Agents broadcast role intentions simultaneously, then decide informed by all intentions. 2N LLM calls.
   - Quality: 0.510 (pilot data)
   - Reasoning: Agents work with incomplete information (intentions may change before execution).

4. **Shared (fully autonomous, endogenous):** Agents access shared organizational memory from previous tasks, make all decisions simultaneously and independently. N parallel calls.
   - Quality: 0.503 (pilot data) — **44% worse than Sequential**
   - Reasoning: Role duplication due to lack of real-time visibility into what others are doing.

**Why Sequential Wins: The Information Argument**

The superiority of Sequential can be understood through information theory. Each agent must decide what role to play. Sequential provides each agent with:
- **Factual results** of predecessors' work on *this specific task*
- Not intentions (may change between rounds)
- Not historical patterns (may not apply to current task)
- Not someone else's plan (limited by one agent's judgment)

This is informationally superior to all alternatives. The sports draft analogy illuminates it: each team selects knowing all previous picks, naturally filling complementary positions without central planning. The paradox is that minimal structure enables maximal emergence—one simple constraint (fixed ordering) unlocks spontaneous role differentiation, voluntary abstention, and mission alignment that no amount of explicit design achieves.

#### System Architecture: How to Build It

The system follows a discrete-time architecture:

```
At each timestep t:
  1. Receive task τt
  2. State xt encodes: agent roles, interaction topology, organizational memory
  3. Dynamics: xt+1 = F(xt, ut, τt, wt, εt)
     where:
       ut = coordination decisions (protocol, routing)
       wt = external shocks (model changes, agent failures)
       εt = LLM stochasticity
  
  4. Measure five metrics at each step:
     • Qt ∈ [0.25, 1.0]: solution quality (multi-criteria LLM-as-judge)
     • Tt: execution time in minutes
     • Ct: cost in tokens
     • Rt: risk (compliance failures, errors)
     • Mt ∈ [0.25, 1.0]: mission relevance

  5. Optimization objective:
     max J = E[Σ(αQ·Qt + αM·Mt − αT·Tt − αC·Ct − αR·Rt)]
     with αi > 0 and constraints on acceptable risk/cost
```

**Quality Evaluation: Multi-Criteria LLM-as-Judge**

Don't use binary "correct/incorrect" scoring. Use a separate judge model (different from agent models to avoid self-evaluation bias) that evaluates each solution across five dimensions on a 4-point scale with verbal anchors:

| Dimension | What It Measures |
|-----------|---|
| **Accuracy** | Factual correctness of claims |
| **Completeness** | Coverage of all task requirements |
| **Coherence** | Logical consistency and structure |
| **Actionability** | Readiness for practical application |
| **Mission Relevance** | Contribution to organizational mission |

Aggregate as: Qt = (accuracy + completeness + coherence + actionability) / 16, where minimum is 0.25 (floor = each sub-score of 1 on 4-point scale).

#### Protocol Selection: Decision Tree

Choose your coordination protocol based on model capability and task characteristics:

| Characteristic | Protocol Choice | Why |
|---|---|---|
| Strong model + complex task (L3–L4) | **Sequential** | Enables autonomy that strong models leverage effectively |
| Weak model + simple task (L1–L2) | **Coordinator** | Weak models need explicit routing; simple tasks tolerate centralization |
| Time-sensitive, parallel-friendly | **Broadcast** (use cautiously) | 2 rounds permit some parallelism, but quality suffers (~30% vs Sequential) |
| Organizational memory available | **Shared** (with caveats) | Only if agents have low-redundancy roles; role duplication tanks quality |
| Uncertainty about optimal roles | **Sequential** | Always a safe default—emerges roles rather than guessing them |

**Implementation Detail: The Sequential Protocol as Code**

```python
def sequential_protocol(task, agents, models):
    """
    Agents process task in fixed order.
    Each agent observes predecessors' outputs before deciding its role.
    """
    outputs = []
    
    for i, agent in enumerate(agents):
        # Agent i sees what all predecessors (0...i-1) contributed
        predecessor_context = "\n".join(f"Agent {j} output: {output}" 
                                       for j, output in enumerate(outputs))
        
        # Agent decides: What is my role? Should I participate?
        agent_prompt = f"""
        Task: {task}
        
        Work completed so far:
        {predecessor_context}
        
        Your turn. What role should you play? Analyze what's missing.
        If you have no value to add, respond: ABSTAIN
        If you will contribute, state your role and output.
        """
        
        response = agent.generate(agent_prompt)
        
        if response != "ABSTAIN":
            outputs.append(response)
        # else: agent self-abstained (voluntary, endogenous)
    
    return outputs  # Final solution is aggregate of all contributions
```

The key: each agent has factual, accumulated information (predecessor outputs) to make an informed decision. No guessing, no re-planning, no communication overhead.

#### Model Selection & Capability Threshold

Not all models benefit from autonomy. The research identified a **capability threshold** below which autonomy hurts performance—rigid structure becomes beneficial for weak models.

**Threshold Requirements (Three Capabilities):**

1. **Self-reflection:** Ability to assess one's own competence. Claude Sonnet 4.6 shows 8.6% voluntary abstention rate (appropriate—most tasks don't need every agent). GLM-5 shows 0.8% (inappropriate—no self-awareness).

2. **Deep reasoning:** Multi-step logical chains. Required to understand task complexity and decide whether participation adds value. Adversarial (L4) tasks expose this: models without deep reasoning collapse.

3. **Instruction following:** Precise adherence to the sequential protocol. Agents must follow a fixed order and interpret the "observe predecessors" instruction correctly.

**Model Rankings & Strategy:**

| Model | Capability | L3 Quality | L4 Quality | Cost Efficiency | Strategy |
|---|---|---|---|---|---|
| Claude Sonnet 4.6 | Very High | 0.875 | 0.594 | Baseline | Use for L3–L4; high-stakes decisions |
| DeepSeek v3.2 | Very High | 0.829 | 0.629 (!) | 24× cheaper | Use for L3–L4; cost-sensitive deployments |
| GLM-5 | High | 0.800 | 0.579 | Moderate | Use for L2–L3 when DeepSeek unavailable |
| Gemini-3-flash | Moderate | 0.357 | — | Cheapest | Use only for L1 (simple tasks); expect 70%+ quality drop on L3 |

**Critical Finding: Multi-Model Strategy Beats Single Model**

No single model dominates all dimensions. A hybrid approach:
- Use strong models (Claude, DeepSeek) for L3–L4 (adversarial, multi-stakeholder tasks)
- Use efficient models (DeepSeek if cost-sensitive, GLM-5, Gemini-3 for cost) for L1–L2 (simple, single-domain tasks)
- Result: ~95% quality of all-Claude at 24× lower average cost

**The Reversal Effect: When to Abandon Autonomy**

Below the capability threshold, autonomy becomes *harmful*. When comparing free-form (self-organized) vs. fixed-role operation:
- Claude Sonnet 4.6: free-form Q = 0.594 > fixed Q = 0.574 (autonomy helps +3.5%)
- GLM-5: free-form Q = 0.519 < fixed Q = 0.574 (autonomy hurts −9.6%)

**Rule:** If a model scores < 0.65 on L3 tasks, use Coordinator protocol with fixed roles instead of Sequential autonomy.

#### Scaling from 4 to 256 Agents: Sub-Linear Cost Growth

One of the most surprising findings: scaling to 256 agents produces **no quality degradation** while cost grows only ~11.8%. This enables very large systems without diminishing returns.

**Scaling Data (Fixed Roles, GPT-4.1-mini, 8,020 tasks):**

| Agents | Quality | Tokens | Cost Increase |
|---|---|---|---|
| 8 | 0.954 | 3,164 | — |
| 16 | 0.952 | 3,200 | +1.1% |
| 32 | 0.955 | 3,270 | +3.4% |
| 64 | 0.949 | 3,537 | +11.8% |

Scaling to 256 agents (self-organization, L1 tasks):

| Agents | Quality ± σ | Coordination Overhead | Time |
|---|---|---|---|
| 64 | 0.964 ± 0.039 | 0.180 | 10.9 min |
| 128 | 0.958 ± 0.038 | 0.180 | 11.5 min |
| 256 | 0.967 ± 0.032 | 0.179 | 13.0 min |

Kruskal-Wallis test: H = 1.84, p = 0.61 (no statistically significant difference).

**Why Scaling Works Without Degradation:**

1. **Fixed ordering (Sequential) is O(N) in latency but O(1) in quality degradation.** Each agent adds one inference step, not one re-planning cycle.

2. **Voluntary self-abstention becomes a cost-optimization mechanism at scale.** At N = 256, ~45% of agents self-abstain, effectively creating an adaptive team size. The system does cost reduction automatically.

3. **Emergent properties intensify with scale:**
   - Unique role specialization: 75% at N=4 → 91% at N=64 (fewer agents doing the same thing)
   - Hierarchy depth: 1.0 (trivial) at N=4 → 2.0 at N=64 (naturally forms 2-layer structure)
   - Adaptation speed: 0.7 → 3.0 (larger systems respond faster to external changes)

**Scaling Strategy:**

1. Test your system at N=8–16 with your target protocol.
2. Run a scaling campaign: 8 → 16 → 32 → 64 agents on representative tasks.
3. If quality remains stable at 64, you can safely deploy to 128–256.
4. Monitor coordination overhead (stays ~0.18 even at 256); if it rises above 0.25, switch to batched Sequential (groups of K agents in parallel, next group sees all previous).

#### Task Complexity Levels: Your Quality Ceiling

Task complexity is the primary predictor of what's achievable. The four levels map to organizational problem types:

| Level | Type | Example | Complexity | Typical Quality |
|---|---|---|---|---|
| **L1** | Single-domain, simple steps | API security review | 1 domain, 3–5 steps, no dependencies | 0.986 ± 0.011 |
| **L2** | Cross-domain, integration | Architecture decision with 2 domains | 2 domains, 5–10 steps, knowledge fusion | 0.992 ± 0.008 |
| **L3** | Multi-phase, sequential deps | Zero-trust migration plan | 3+ domains, 10–20 steps, phase ordering | 0.948 ± 0.019 |
| **L4** | Adversarial, conflicting stakes | CEO vs. Legal vs. CFO resource allocation | 3+ domains, conflicting interests, incomplete info | 0.614 ± 0.020 (current frontier) |

**Hierarchy Depth as a Stability Signal:**

Self-organized systems spontaneously deepen hierarchy as task complexity increases:

| Task Level | Hierarchy Depth | Meaning |
|---|---|---|
| L1 | 1.22 | Flat—all agents peers |
| L2 | 1.06 | Still flat—minimal dependencies |
| L3 | 1.30 | Slight hierarchy—some agents specialize in synthesis |
| L4 | 1.56 | Deeper structure—system organizes into management layers |

This is emergent, not designed. Don't force hierarchy depth; let it emerge based on task needs.

#### Practical Deployment Workflow

**AI Agent Implementation Context:** The following workflow is derived directly from Dochkina's empirical findings and is the proper deployment sequence to replicate the paper's results when building multi-agent agentic systems. This is not theoretical—if you follow these phases in order, your system should achieve the quality and cost metrics reported in the 25,000-task study.

Here's how to actually build and deploy a self-organizing system:

**Phase 1: Design (Days 1–2)**

✓ *Validated by Dochkina: Section V.E ("Practical Recipe") + empirical protocol/model comparisons*

1. Define mission and values (NOT role assignments)
   - Example: "Analyze this architectural decision for security, cost, and maintainability trade-offs."
   - Don't specify: "Agent A checks security, Agent B checks cost, Agent C checks maintainability"
   - **Why:** Paper shows agents spontaneously invent specialized roles; pre-assignment constrains performance.

2. Select coordination protocol
   - Default to **Sequential** for unknown scenarios (0.875 L3 quality, +14% vs Coordinator)
   - Switch to Coordinator only if models score < 0.65 on L3 tasks (capability threshold reversal)
   - Avoid Shared/Broadcast (quality 0.503–0.510, both ~44% worse than Sequential)
   - **Why:** Paper tested all 4; Sequential consistently wins across models and task levels.

3. Choose model tier based on task complexity
   - L1–L2: Efficient model (Gemini-3-flash ~0.36, GLM-5 ~0.80, or DeepSeek v3.2 for cost)
   - L3: Strong model (Claude Sonnet 4.6 ~0.88 or DeepSeek v3.2 ~0.83, 24× cheaper)
   - L4: Your strongest model (Claude Sonnet 4.6 ~0.59, DeepSeek shows trend toward superiority at +6% but not yet proven)
   - **Why:** Paper ranked models by capability threshold; below ~0.65 on L3, autonomy reverses.

**Phase 2: Implementation (Days 3–5)**

✓ *Validated by Dochkina: Section III (Methodology) + Figure 4 role assignment heatmap*

1. Initialize agents with minimal role scaffolding
   ```python
   agents = [
       Agent(model=claude, instruction="You are a member of an analysis team."),
       Agent(model=claude, instruction="You are a member of an analysis team."),
       Agent(model=claude, instruction="You are a member of an analysis team."),
       # ... N agents, identical instructions
   ]
   ```
   Note: No role pre-assignment. Agents are identical at init time.
   **Why:** Paper shows RSI→0 (agents reinvent roles per task); identical init enables emergence.

2. Implement Sequential protocol loop (see code example above)
   ```
   For each agent in order:
     - Agent sees: completed outputs of all predecessors
     - Agent decides: What is my role? Should I participate?
     - If value-add: contribute output
     - Else: ABSTAIN (voluntary)
   ```
   **Why:** Paper proves Sequential (factual outputs) beats Broadcast (intentions) and Shared (history).

3. Set up multi-criteria LLM-as-judge evaluation
   - Separate judge model (GPT-5.4 in paper's Series 3; different from agent models)
   - Fixed judge across all evaluation runs (preserves internal validity)
   - Evaluate on all 5 dimensions: accuracy, completeness, coherence, actionability, mission relevance
   - Aggregate: Qt = (acc + comp + coh + act) / 16 ∈ [0.25, 1.0]
   - **Why:** Paper uses this exact methodology to avoid self-evaluation bias.

4. Test on representative tasks at N=8
   - L1 task: Should achieve ~0.98 quality (paper: 0.986 ± 0.011)
   - L3 task: Should achieve ~0.85–0.90 quality (paper: 0.948 ± 0.019 at N=32/64)
   - If below these ranges: revisit model tier or protocol choice.

**Phase 3: Scaling (Days 6–7)**

✓ *Validated by Dochkina: Series 2 (8,020 tasks, N=8–64) + Series 3 (6,000 tasks, N=64–256)*

1. Run scaling campaign
   - N = 8, 16, 32, 64 on same task set (same task complexity level, same judge model)
   - Measure: quality Qt, cost Ct (tokens), time Tt
   - Expected: Quality remains stable (paper: 0.949–0.955 across 8×), cost grows ~12%
   - Statistical test: Kruskal-Wallis or t-test; if p > 0.05, quality not significantly degraded, safe to continue scaling
   - **Why:** Paper explicitly tested this progression; sub-linear scaling proven to 256 agents.

2. Monitor self-abstention rate
   - Target: 8–15% at N=8–16; 20–45% at N=64–256
   - Low (< 2%): agents can't self-assess; likely model below capability threshold
   - High (> 70%): task is too simple; reduce agent count or increase complexity
   - **Why:** Paper shows Claude abstains 8.6% (healthy), GLM-5 abstains 0.8% (unhealthy), emerges 45% at N=256.

3. Measure emergent role diversity (Role Specialization Index, RSI)
   - Count unique role names invoked across tasks at N=8, N=16, N=32, N=64
   - Target: RSI→0 (approaches zero), meaning agents create new roles per task
   - With 8 agents: expect ~5,000 unique roles across sample tasks
   - With 64 agents: expect ~5,000 (no increase—agents don't consolidate)
   - If RSI stays high (agents use same role repeatedly): mission/prompt unclear
   - **Why:** Paper: Figure 4 shows RSI→0; agents at N=4 create 5,006 roles, N=64 create 5,010 (+0.1%).

**Phase 4: Production (Day 8+)**

✓ *Validated by Dochkina: Section IV.D (closed vs. open-source) + Section IV.H (resilience to external shocks)*

1. Deploy to live workload
   - Start with N=16–32 (confirmed sweet spot: quality stable, cost ~3200 tokens at N=16)
   - Monitor: cost, latency (Sequential is O(N), expect ~15 min at N=16), quality per task type
   - Expected latency: N=8 ~14.5 min, N=16 ~14.4 min, N=64 ~14.8 min (varies by model speed, not strongly with N)
   - **Why:** Paper Series 2 shows stable execution times across 8× agent increase.

2. Implement multi-model strategy
   - Route L1–L2 tasks to efficient model (Gemini-3-flash, GLM-5)
   - Route L3–L4 to strong model (Claude Sonnet 4.6 or DeepSeek v3.2)
   - Expected cost savings: 40–50% vs. all-Claude deployment, 92–97% quality retention
   - **Why:** Paper shows DeepSeek 0.829 (95% of Claude 0.875) at 24× lower cost; optimal for L3.

3. Set up resilience testing
   - Introduce perturbations in controlled test set:
     - Random agent removal (remove 1–2 agents mid-execution)
     - Hub agent removal (if hierarchical, remove highest-degree agent)
     - Model substitution (25% of agents switch to weaker model)
   - Expected: Quality recovers within 1 iteration (no latency increase)
   - Paper tested on N=32, achieved Resilience Index RI = 0.959 (Spectral Hierarchy model), zero variance
   - Adaptation speed improves with scale: 0.7→1.5→3.0 as N increases 4→16→64
   - **Why:** Paper shows self-organizing systems heal faster than designed systems when perturbed.

#### Emergent Properties to Monitor

As your system scales, watch for these signatures of healthy self-organization:

**1. Dynamic Role Specialization (RSI → 0)**

Agents should *not* settle into fixed roles. Instead, RSI (Role Stability Index) converges to zero, meaning agents reinvent their specialization for each task.

Observable: With 8 agents, system invents 5,006 unique role names across tasks. With 64 agents, 5,010 (+0.1%). About 54% of roles used exactly once—agents aren't recycling roles; they're creating new ones per task.

Action: If you see role consolidation (same agents doing the same role repeatedly), your mission statement is unclear or your task set is too narrow.

**2. Voluntary Self-Abstention**

Healthy systems show high voluntary abstention rates:
- Claude: 8.6% abstain (agents recognize incompetence)
- DeepSeek: 4–5% abstain
- Weak models: 0.2–0.8% abstain (unable to self-assess)

Observable: In Sequential protocol, agents announce "ABSTAIN" without coordinator pressure. Compare to Coordinator (100% of non-contributing agents directed to abstain by coordinator).

Action: If abstention < 2%, your model may lack self-reflection; consider switching to Coordinator or a stronger model.

**3. Shallow Spontaneous Hierarchy**

The system should form 1–2 management layers naturally, not 3+ (which suggests unnecessary coordination overhead).

Observable: Hierarchy Depth stable around 1.0–2.0 even as N scales from 4 to 256.

Action: If HD > 2.5, your mission may be ambiguous or your task genuinely requires deep sequencing. Re-examine the problem structure.

#### Failure Modes & Guardrails

**1. The Capability Cliff**

Below model threshold, autonomy reverses:
- Claude Sonnet 4.6 + Sequential: Q = 0.594 ✓
- GLM-5 + Sequential: Q = 0.519 ✗ (switch to Coordinator)

Mitigation: Always run a 10-task L3 pilot to measure model performance. If Q < 0.65, use Coordinator protocol instead.

**2. Role Duplication (Shared Protocol Failure)**

Fully autonomous agents without real-time visibility duplicate roles:
- Broadcast quality: 0.510 (38% worse than Sequential)
- Shared quality: 0.503 (44% worse than Sequential)

Reason: Agents can't see what others are doing in real time; multiple agents tackle the same subtask.

Mitigation: Default to Sequential. Use Shared only if you have persistent organizational memory from previous runs and verified low-redundancy role sets.

**3. L4 Adversarial Task Collapse**

Adversarial tasks (conflicting stakeholders, incomplete info) show 37% quality drop from L1:
- L1 quality: 0.986
- L4 quality: 0.614

Current frontier: System struggles when stakeholders have genuinely conflicting interests and no single correct answer exists.

Mitigation: For L4 tasks, expect lower absolute quality. Use strong models + Sequential + human-in-the-loop for final decision-making.

**4. Sequential Latency at Very Large N**

Sequential is O(N) in latency. At N = 256, execution time is 13 minutes; at N = 1,024 (future), could be 50+ minutes.

Mitigation: Implement **batched Sequential** variant—groups of K agents work in parallel, next group observes all previous. O(N/K) latency while preserving Sequential's informational advantage.

#### Cost Optimization & Multi-Model Strategy

Token consumption scales sub-linearly despite agent count increase. Average token cost per agent drops as N grows (from ~400 tokens per agent at N=8 to ~55 at N=64). Leverage this with multi-model strategy:

**Cost Comparison (N=16, L3 tasks, 120 tasks per model):**

| Model | L3 Quality | L4 Quality | Tokens | Cost/1K Tokens | Strategy |
|---|---|---|---|---|---|
| Claude Sonnet 4.6 | 0.875 | 0.594 | 37K | 0.0236 | Strong; use for L3–L4 |
| DeepSeek v3.2 | 0.829 | 0.629 | 47K | 0.0177 | 95% Claude quality, 24× cheaper |
| GLM-5 | 0.800 | 0.579 | 57K | 0.0140 | Efficient; L2–L3 only |

**Deployment Strategy:**

1. **Task Router:** Classify incoming task complexity (L1–L4)
2. **Model Selection:**
   - L1 → Gemini-3-flash ($0.08/MTok)
   - L2 → GLM-5 ($0.15/MTok) or DeepSeek ($0.20/MTok)
   - L3 → DeepSeek ($0.20/MTok) or Claude ($4.50/MTok for high-stakes)
   - L4 → Claude (only option currently for adversarial)
3. **Cost Savings:** ~40–50% vs. all-Claude deployment, with 92–97% quality retention.

---

### Real-World Orchestration Patterns

The patterns above describe collaboration architectures. This section covers the production-grade mechanisms for making orchestration actually work at scale — based on the ECC system, an open-source agent harness built from 10+ months of intensive daily use.

**The Chief-of-Staff Pattern**

For complex multi-step projects, a dedicated coordinator agent — separate from all specialist agents — manages cross-agent work. The chief-of-staff doesn't implement anything. Its job is decomposition, delegation, and synthesis.

```
Chief-of-Staff (opus):
  → Receives high-level goal from human
  → Decomposes into atomic subtasks
  → Dispatches to appropriate specialist agents
  → Monitors progress, resolves blockers
  → Synthesizes outputs into coherent deliverable
  → Reports back to human with unified result
```

Why a separate coordinator matters: specialist agents optimized for their domain make poor project managers. A security reviewer shouldn't also be tracking whether the database migration is blocking the API tests. Separation of concerns applies to agents just as it does to code.

**The Loop-Operator Pattern**

For tasks with machine-verifiable success criteria, a loop-operator agent manages continuous execution rather than delegating to a one-shot agent. The pattern:

1. Loop-operator receives task + success criteria
2. Dispatches implementation agent with bounded scope
3. Runs verification step (tests, lint, type-check)
4. If criteria not met: analyzes failure, updates instructions, dispatches again
5. Caps at `max_iterations` (typically 5-10) to prevent runaway loops
6. Escalates to human if cap hit without success

The key design insight is that the loop-operator doesn't know *how* to implement the task — it knows *whether* it's done. These are different skills, and mixing them in one agent produces confused behavior.

**Harness Construction Principles**

The quality of an agent harness determines the ceiling of what your agents can achieve. Four factors dominate:

- **Action space quality:** Tools should be schema-first, narrow, and deterministic in output shape. Broad tools that do many things produce ambiguous action choices. Micro-tools for sensitive operations (file deletion, database writes), macro-tools only when latency genuinely dominates.

- **Observation quality:** What the agent perceives after taking an action should be rich enough to enable course correction. Thin observations (just "success" or "error") force the agent to retry blindly. Rich observations include the changed state, any warnings, and enough context to understand why the action succeeded or failed.

- **Recovery quality:** Can the agent get back on track after a failed action? Good recovery requires: idempotent operations where possible, rollback mechanisms for destructive steps, and explicit error messages that describe what went wrong at a level the agent can reason about.

- **Context budget:** Token cost is an architectural constraint, not an afterthought. MCP tool schemas cost ~500 tokens each at load time. Agent descriptions load universally regardless of whether the agent is invoked. Prose runs at ~words × 1.3 tokens; code at ~chars ÷ 4. Design your harness with these costs in mind from the start.

**The /multi-* Command Pattern**

For large projects where parallel execution genuinely helps, the multi-execute pattern spawns independent agent instances for non-overlapping subtasks:

```
/multi-plan   → Multiple planning agents produce competing plans
              → Human selects or synthesizes the best approach

/multi-execute → Parallel implementation agents work on independent modules
              → Chief-of-staff monitors and integrates outputs

/multi-backend → Backend-only parallel agents (API + database + auth simultaneously)
/multi-frontend → Frontend-only parallel agents (components + state + routing simultaneously)
```

The key constraint: tasks must have zero shared state during execution. Agents writing to the same files in parallel produce merge conflicts and architectural drift. Partition work by module or layer, never by feature (features cut across layers).

**A Practical Agent Taxonomy**

Production agent harnesses tend to converge on a similar set of specialist roles. The following taxonomy — drawn from the ECC harness — serves as a reference for what to build:

| Tier | Agents | Model | Responsibility |
|---|---|---|---|
| Orchestration | chief-of-staff, loop-operator, harness-optimizer | opus | Planning, coordination, harness self-improvement |
| Architecture | planner, architect | opus | Decomposition, system design |
| Implementation | language reviewers (Python, TS, Go, etc.) | sonnet | Domain-specific implementation review |
| Quality | code-reviewer, tdd-guide, security-reviewer | sonnet | Standards enforcement |
| Operations | build-error-resolver, doc-updater, refactor-cleaner | haiku/sonnet | Maintenance tasks |

The model assignments aren't arbitrary: orchestration and architecture require the reasoning depth of Opus; maintenance tasks are well-defined enough for Haiku; implementation review sits in between.

---

### Autonomous Loops

An iteration-based pattern where the agent repeatedly attempts a task, using git history as external memory, with a fresh context window for each attempt. The agent looks at what previous iterations committed, understands what worked and what didn't, and improves on the next attempt.

Success criteria must be machine-verifiable — tests passing, lint clean, schemas validated. The agent iterates until the criteria are met or a maximum iteration count is reached.

**Use when:** Machine-verifiable success criteria, reversible operations (git makes recovery easy), failure is acceptable learning data.

**Contrast with Human-in-the-Loop:** Use autonomous loops when mistakes are cheap and recoverable. Use HITL when operations are irreversible or when human judgment about *whether* the result is good cannot be automated.

---

### Self-Improving Experts

Agents that update their own expertise based on execution outcomes. This is the production implementation of Level 6 prompt maturity.

**The four-agent cycle:**
1. *Plan agent* creates a plan for the task
2. *Human approves* the plan (HITL gate)
3. *Build agent* implements the plan
4. *Review agent* validates the implementation
5. *Improve/Learn agent* runs after completion — analyzes git history, extracts new patterns, updates the expertise file

The improve agent always runs *after* execution, never during. It's an analysis pass, not an intervention in the current task.

---

### Persistent Agent Memory

Most agent patterns discussed so far are session-bound — the agent starts fresh each time, with no recollection of previous work. For long-running projects, this is a significant limitation: a coding agent that forgets your conventions after every session, a research agent that re-discovers the same sources it already processed, a personal assistant that can't remember your preferences. This pattern addresses that problem.

The core idea is to give agents *external memory that survives session boundaries* — stored as plain files, tracked by git, and selectively loaded into context depending on how relevant a piece of memory is right now.

**What to store: three types of memory**

Before thinking about how to store memory, it helps to think about what kind of information you're storing. Google's memory framework (from their "Context Engineering: Sessions & Memory" whitepaper) identifies three distinct types — and they behave differently enough to warrant treating them separately:

- **Semantic memory** — stable facts and preferences. Things that are true about the world or about the person/project and change rarely. *"User prefers TypeScript. No semicolons. Tabs over spaces."* This is your most durable memory — once it's written, it should only change when a preference actually shifts.

- **Episodic memory** — events and history. What happened in past sessions. *"On Feb 17 we debugged the auth module and found a race condition in token refresh."* This is always new — each session adds to it. It's the running log of what's been done.

- **Procedural memory** — workflows and learned routines. How to do things. *"When deploying, run tests, then build, then push to staging, then get approval before prod."* This evolves slowly as you refine how you work.

Most memory files end up containing all three mixed together, which works fine. But if you organize your files by type, you'll find naming and updating them becomes much more intuitive — and the agent has a clearer sense of which files are likely relevant for a given task.

---

**Why files over a database?**

The natural instinct is to store memory in a database — structured, queryable, persistent. But files have a counterintuitive advantage: they're already a tool agents know how to use. An agent can edit a markdown file with the same bash and text-editing tools it uses for any other task. There's no specialized memory API to learn, no schema to design, no migration when structure needs to change. Standard tools are more composable, more debuggable, and less fragile than custom memory APIs.

---

**The Two-Tier Architecture: Core vs. Extended**

Not all memory should be treated equally. The two-tier approach makes an explicit distinction:

- **Core memory** — facts relevant in *every* session, regardless of what you're working on. Preferred coding style, project folder structure, conventions the team has adopted. Core memory lives in a designated folder (commonly `system/`) and is automatically injected into the system prompt every time the agent runs. It's always in context.

- **Extended memory** — knowledge that might be relevant but isn't always needed. Module-specific notes, research from previous sessions, user preferences not needed every day. Extended memory lives in the directory structure but isn't auto-loaded. The agent can see it exists and choose to read it, but it doesn't pre-fill the context window on every run.

This separation matters because context is finite. Loading everything into the system prompt quickly crowds out room for the actual task. The two-tier design keeps core knowledge permanently available while letting extended knowledge stay on disk until needed.

```
memory/
├── system/                ← always injected into system prompt
│   ├── identity.md        "You are an expert in TypeScript..."
│   ├── conventions.md     "We use conventional commits..."
│   └── project-map.md     "Main entry point: src/index.ts"
└── extended/              ← visible to agent, loaded on demand
    ├── projects/
    │   └── auth-module.md
    └── preferences/
        └── human-interests.md
```

---

**Git as the Memory Backend**

This is the genuinely novel element of this pattern. By storing memory as a git-tracked folder, you get several capabilities for free:

- **Version control:** Every change to agent memory is a commit. You can see exactly what the agent learned and when — and roll back if a memory turns out to be wrong or misleading.
- **Audit trail:** Commit messages can record which agent made a change and why. "Reflection agent added project convention about error handling based on session 2025-11-15."
- **Parallel agent isolation:** Multiple agents working simultaneously on memory can use git worktrees to isolate their changes before merging. This prevents race conditions where two agents overwrite each other's work — the same risk the Expert Swarm pattern manages through its Learning Separation Rule.

The memory contamination risk (a hallucinated fact written to shared memory becoming "ground truth" for all future agents) is meaningfully reduced when you have full git history. A bad memory is just a commit you can inspect and revert, not permanent corruption.

---

**Reflection Agents (Sleeptime Agents)**

Memory doesn't curate itself. You need a mechanism to take what happened during a session and decide what's worth persisting. This is the job of a **reflection agent** — sometimes called a sleeptime agent because it typically runs in the background after the main work is done.

A reflection agent is a lightweight LLM call triggered at the end of a session or on a schedule. It receives recent conversation or action history and answers: *What here is worth remembering for future sessions?* It then writes or updates the appropriate memory files and commits the changes.

The critical design principle: reflection agents run *after* the main agent finishes, never during. This prevents them from blocking the main workflow. The main agent does its work, completes, and memory consolidation happens asynchronously.

A minimal reflection agent prompt looks like:

```
Here is a summary of what happened in the last session:
[session summary]

The current memory folder contains:
[directory listing]

Please identify any new facts, preferences, or conventions that would be
useful in future sessions, and write them to the appropriate files.
Commit your changes with a message describing what you added and why.
```

---

**When to consolidate: session compaction triggers**

A reflection agent needs something to trigger it. There are three main strategies, each with different tradeoffs:

- **Count-based** — consolidate after a certain number of tokens or conversation turns. Simple to implement, but blunt: it fires on a schedule regardless of whether anything meaningful happened. Good enough for most setups.

- **Time-based** — consolidate after a period of user inactivity. Useful for long-running async projects where sessions don't have a clean end. Less predictable than count-based.

- **Event-based** — consolidate when a task is detected as complete. The most intelligent approach: memory gets updated at the natural boundary between one piece of work and the next. The tradeoff is that detecting task completion reliably is harder — you need the agent to recognize when it's done, not just when it's been a while.

In practice, many setups use a hybrid: count-based as a safety net (consolidate if the context gets too long), plus event-based when the user signals completion manually — like a `/new` command, or a "that's done, let's move on" message. The manual signal is essentially event-based compaction with a human doing the detection.

---

**When this pattern makes sense:**
- Long-running projects where context accumulates across many sessions
- Personalized assistants that need to learn user preferences over time
- Coding agents working on a codebase they should know deeply
- Any scenario where re-discovering the same context every session is expensive

**When it's overkill:**
- One-off tasks with no meaningful carry-forward state
- Pipelines where freshness matters more than continuity (you want the agent to re-evaluate from scratch)
- Short-lived workflows where persistent memory adds overhead without benefit

**You don't need a third-party service to implement this.** The complete pattern — three memory types organized into files, git-tracked folder, two-tier loading convention, reflection agent triggered by count or event — is buildable with any LLM and standard file tools. Managed platforms (like Letta) add conveniences such as server-side backup, visual memory interfaces, and bootstrapping from historical sessions, but the core architecture is entirely self-hostable.

---

### Blueprints Pattern (Hybrid Deterministic/Agentic State Machine)

This pattern addresses a core reliability problem in production agentic systems: pure agent loops are unpredictable and expensive, but pure deterministic workflows can't handle ambiguity. The solution is a single workflow graph with two explicitly typed nodes — deterministic and agentic — and a design discipline that determines which tasks belong in each.

**Named by Stripe** as "Blueprints" in their Minions coding agent system (1,300+ agent-written PRs per week, 2025). The underlying concept is converging as a standard production pattern across the industry under various names: "hybrid state machines" (Tomasz Tunguz), "compound AI systems" (deepset), "workflow agents" (Google Cloud, Oracle). The name varies; the pattern is the same.

**How common is this in production?** An analysis of 14 production agentic workflows found that ~65% of all nodes run as pure deterministic code on average — only 14% of workflows are fully agentic. The implication: most real production "AI" systems are mostly code, with LLMs used surgically at the steps that genuinely need judgment. As Tunguz put it: *"Is AI doing less? Yes. Is the system doing more? Also yes."*

**The two node types:**

- **Deterministic nodes** — fixed execution with no LLM involvement. Linting, formatting, git operations, running tests, pushing code. These always behave identically, cost zero tokens, and are fully predictable. Hard-code anything with a known, correct procedure.
- **Agentic nodes** — free-form LLM reasoning with tool access. "Implement this task," "diagnose these CI failures," "write tests for this function." Use LLMs only where the task genuinely requires judgment.

```
Blueprint: Implement Feature
─────────────────────────────────────────────
[Deterministic] Pre-hydrate context (run MCP tools, load relevant docs)
      ↓
[Agentic]       Implement task (LLM with full tool access)
      ↓
[Deterministic] Lint + format (run linter, auto-fix, push)
      ↓
[Deterministic] Submit to CI
      ↓
[Agentic]       Fix CI failures (LLM diagnoses failures, patches code)
      ↓
[Deterministic] Final push → PR creation
─────────────────────────────────────────────
Hard limit: 2 CI iterations maximum
```

**Why this beats a pure agent loop:**

A pure agent loop uses LLM reasoning for every step — including things like "run the linter" that have exactly one correct answer. This wastes tokens, introduces unnecessary variance, and makes the system harder to debug. Blueprints hard-code every deterministic step so the LLM only spends context and compute on decisions that actually require judgment.

**Context pre-hydration.** The first deterministic node runs relevant tools *before* the agentic phase begins — fetching documentation, loading ticket context, pulling code search results. The LLM starts reasoning with a full picture rather than spending its first actions collecting what it needs. Pre-hydration is what makes one-shot completion rates practical at Stripe's scale.

**The two-iteration CI cap.** Hard limit: two CI runs per task. If the agent can't fix failures in two rounds, it escalates to a human. The reasoning: diminishing returns — additional iterations rarely succeed and burn compute. Hard caps prevent infinite loops and make failure escalation a *designed feature*, not a fallback.

**"What's good for humans is good for agents."** Run agents on the same machines and tooling human engineers already use. Agents inherit all the existing optimizations, compliance controls, and debugging infrastructure without requiring agent-specific builds.

**The prerequisite: establish the deterministic harness first.** Blueprints don't create the deterministic infrastructure — they assume it exists. CI, linting, and a test suite must be in place before Blueprint-style agent workflows can run. This has an important sequencing implication for greenfield projects: build the deterministic harness first (test framework, CI pipeline, linter config), then use Blueprint-pattern agents to build features against it. Once the harness exists, agents can run in parallel against the same infrastructure — which is how systems like Stripe scale to hundreds of concurrent tasks. The larger and more complex the codebase, the more valuable the pattern becomes, because the agentic reasoning burden grows while the deterministic steps stay constant.

**What the deterministic harness actually looks like — Agent Readiness.** Factory.ai formalized this as an "Agent Readiness" framework: when AI coding agents underperform, teams blame the model, but the real bottleneck is usually the codebase environment. Missing pre-commit hooks force agents into slow CI feedback loops. Undocumented environment variables cause repeated guessing. Build processes requiring tribal knowledge prevent agents from verifying their own work. These deficiencies compound. Factory evaluates codebases across eight pillars:

| Pillar | What it covers |
|---|---|
| Style & Validation | Linters, type checkers, formatters — agents get immediate feedback on code quality |
| Build System | Reproducible, documented builds agents can run without tribal knowledge |
| Testing | Unit, integration, and E2E tests agents can execute to verify their own changes |
| Documentation | Inline docs, READMEs, architecture notes — reduces agent guessing |
| Dev Environment | Containerized or scripted setup with no manual steps |
| Code Quality | Consistent patterns agents can learn from and extend |
| Observability | Logging, tracing, metrics — agents can diagnose failures |
| Security & Governance | Secrets management, access controls, dependency scanning |

**Five maturity levels, target is Level 3 (Standardized):** production-ready with E2E tests, maintained docs, security scanning, and observability. Level 3 is where agents become reliably effective. Levels 4-5 enable increasingly sophisticated autonomous contributions but require significant investment. The practical implication: you don't need a perfect codebase before running agents, you need a Level 3 codebase.

A useful diagnostic: if an agent keeps failing at the same step, ask whether the failure is the model or the environment. Undocumented setup steps, missing type annotations, and absent test coverage are environment failures — fixing them improves every agent that runs against that codebase, permanently. (Source: Factory.ai, "Agent Readiness," 2025)

**When to use Blueprints:**
- Production coding agents with high-reliability or compliance requirements
- Any workflow mixing creative implementation with mandatory process steps (linting, CI, compliance checks)
- Greenfield projects after the test/CI harness is established
- When you want to reduce token cost and variance without sacrificing agent flexibility on the hard parts

**How it relates to LangGraph:** Blueprints and LangGraph implement the same graph execution model (nodes + edges). The distinction: Blueprints makes the deterministic/agentic split a named, first-class design decision rather than an implementation detail. In LangGraph terms, some nodes call the LLM, others are pure Python — Blueprints says you should be *intentional* about which is which and why.

---

### Agent Orchestration Patterns

When you move from single agents to multi-agent systems, you need explicit patterns for how agents communicate, pass work between each other, and handle failures. This is called **agent orchestration** — the discipline of coordinating multiple specialized agents toward a shared goal.

**The Sub-Agent Context Problem**

Multi-agent systems face a fundamental architectural challenge: each sub-agent exists in isolation, with limited context about why it was invoked. The orchestrator has semantic understanding (the "why"), but sub-agents only get the literal query (the "what"). This mismatch causes sub-agents to produce summaries that miss key details the orchestrator needed.

Example: An orchestrator asks a research sub-agent, "Find information on user retention factors." The sub-agent doesn't know the full context — is this for a B2B SaaS company? A social platform? A games studio? Each would need different research, but the sub-agent receives no hint. It returns a generic summary that the orchestrator then has to iterate on.

**The Iterative Retrieval Pattern**

The solution is to treat sub-agent returns as *provisional summaries that might need follow-up questions*, not final answers:

```
1. Orchestrator dispatches query + objective to sub-agent
2. Sub-agent returns summary
3. Orchestrator evaluates: "Is this sufficient?"
4. If no: ask targeted follow-up questions
5. Sub-agent refetches data, returns clarified summary
6. Loop until sufficient (max 3 cycles to prevent infinite loops)
```

This transforms the architecture from "one-shot delegation" to "iterative refinement." The cost is higher (more back-and-forth), but the quality is dramatically better because the sub-agent eventually understands what the orchestrator actually needs.

**Sequential Phase Orchestration**

The most robust multi-agent pattern structures work as sequential phases, with a shared artifact flowing between them:

```
Phase 1: RESEARCH (Explore Agent)
├─ Gather context from codebase
├─ Identify patterns
└─ Output: research-summary.md

Phase 2: PLAN (Planning Agent)
├─ Read research-summary.md
├─ Create implementation spec
└─ Output: plan.md

Phase 3: IMPLEMENT (Build Agent)
├─ Read plan.md
├─ Write tests first (TDD)
├─ Implement code
└─ Output: code changes + test results

Phase 4: REVIEW (Review Agent)
├─ Read plan.md and code changes
├─ Evaluate against spec
└─ Output: review comments

Phase 5: VERIFY (Verification Agent)
├─ Run test suite
├─ Fix failures or escalate
└─ Output: test results (pass/fail)
```

Each agent receives one clear input and produces one clear output. The outputs become inputs for the next phase. This prevents context contamination where multiple agents are trying to work from partially-understood shared state.

**Design discipline for orchestration:**

1. **One clear input per agent** — The agent knows exactly what is being asked. Include both the specific query AND the broader objective context.
2. **One clear output per agent** — Define the exact format (markdown, JSON, code file). Parsing failures downstream multiply quickly.
3. **Shared artifact progression** — Files (like a `plan.md` or `research-summary.md`) become the "source of truth" that flows through phases. All agents reference the same artifact, preventing divergence.
4. **Phase gates** — Before transitioning to the next phase, verify the previous phase's output is acceptable. If not, loop within that phase rather than pushing forward with bad data.
5. **Max iterations** — Set hard limits on how many times you'll loop (usually 3). If a phase can't succeed in 3 iterations, escalate rather than retrying infinitely.

---

### Agent Abstraction Tierlist

Not all agent patterns are equally accessible or necessary. Some agent architectures have high skill floors — they require deep understanding of orchestration, context management, and failure modes. Others are straightforward wins with minimal complexity.

This tierlist helps you choose: **start in Tier 1, only graduate to Tier 2 when you have mastery and a genuine need.**

**Tier 1: Easy Wins (Pick These First)**

These patterns have low skill floors and deliver high value-to-complexity ratio. Most teams should start here.

- **Subagents** — Delegate specialized tasks to focused agents (2-3 independent tasks max). "Use one agent for research, one for coding, one for review." High value because it isolates context and reduces failure surface. Low complexity because each agent is simple and independent. *Start here* if moving from single-agent to multi-agent.

- **Metaprompting** — Use a cheap prompt to "pre-think" what a more expensive prompt should do. "Before running the code-writing prompt, spend a cheap prompt thinking through the design." High value because it improves the main agent's reasoning without adding agents. Low complexity because it's just better prompt discipline.

- **Better scoping questions** — Ask the user more at the beginning instead of iterating. "Before I start, tell me: Is this for internal use or customer-facing? What's the context?" Eliminates mid-task pivots. No code complexity; pure communication improvement.

- **Plan documents as shared state** — Agents read from a shared plan file rather than from oral instructions. Reduces ambiguity, enables parallelism, makes failures debuggable. Very low code complexity; big leverage from better structure.

**Tier 2: High Skill Floor (Graduate Only When Ready)**

These patterns unlock powerful capabilities but require deep understanding of agent failure modes, orchestration, and state management. The cost of getting them wrong is high.

- **Long-running agents** — Agents that execute over hours or days, accumulating context and recovering from failures. Requires careful memory management, session lifecycle understanding, and ability to diagnose failures from limited logs. *When to use:* Long-running projects, overnight batch jobs, agents that need to learn from previous runs. *When NOT to use:* Simple one-shot tasks (Tier 1 subagents are better).

- **Parallel multi-agent systems** — Multiple agents working simultaneously on the same codebase or shared state. Requires isolation via git worktrees, careful merging strategy, and ability to debug race conditions where two agents write conflicting changes. High variance in outcomes. *When to use:* Large, well-segmented tasks where agents can work independently. *When NOT to use:* Highly interdependent tasks (agents need to constantly sync state).

- **Role-based multi-agent systems** — Agents that take on personas ("you are the security expert," "you are the performance specialist") and collaborate. Requires careful prompt engineering to prevent agents from contradicting each other or inventing false consensus. Fails badly when assumptions about role expertise are wrong. *When to use:* Design reviews, architecture decisions where multiple perspectives matter. *When NOT to use:* Most feature implementation (simpler patterns work better).

- **Computer-use agents** — Agents that control the mouse and keyboard, navigate GUIs, interact with web apps, manage terminals. Very early paradigm (as of 2025), requires wrangling. Low success rates on complex tasks. *When to use:* GUI automation, testing against unfamiliar systems where API access isn't available. *When NOT to use:* As a replacement for APIs or programmatic interfaces (subagents are more reliable).

**The Graduation Rule**

You're ready to graduate to Tier 2 when:
1. You have successfully deployed a Tier 1 pattern in production
2. You've debugged at least one non-trivial failure
3. The current pattern is genuinely the bottleneck (not just "wouldn't it be cool to...")
4. You can articulate why the specific Tier 2 pattern solves the problem better than Tier 1

If you answer "I don't know" to any of those, stay in Tier 1. The patterns there scale further than most teams realize, and mastering them is worth more than superficially trying advanced patterns.

---

## 8. Practices

### Debugging Agents

Debugging an agent is fundamentally different from debugging regular code. In regular code, you can step through execution and see exactly what happened. In agent debugging, the model's internal reasoning is opaque — you can only observe inputs and outputs, and work backward to infer what went wrong.

**Diagnostic framework — match symptom to root cause:**

```
Wrong output         → Problem is the prompt or context
Looping behavior     → Problem is the termination conditions
Premature stopping   → Problem is the stopping criteria
Wrong tool selected  → Problem is the tool descriptions
Hallucination        → Problem is context, missing grounding
Crashes/errors       → Problem is tool errors or context overflow
```

**Common failure modes and their fixes:**

| Failure Mode | Likely Cause | Fix |
|---|---|---|
| Context overflow | Agent approaching context limit, behavior gets erratic | Proactive compaction, spawn fresh agent |
| Tool selection errors | Tool descriptions unclear or overlapping | Add examples, add "Do NOT use for" sections |
| Hallucination | Model inventing information not in context | Add grounding via RAG with citations |
| Instruction drift | Long context causes early instructions to fade | Repeat critical instructions near the task |
| Tool selection confusion | Multiple tools look similar | Clearer differentiation, comparison tables |
| Premature termination | No clear signal for when the task is done | Define explicit stopping criteria |
| Multi-agent state corruption | Agents working from stale or wrong shared state | Context isolation, fresh agent instances |

**Debugging techniques, in order of usefulness:**

1. **Structured logging** — Record every tool call with full parameters and results. Debugging without logs is guessing.
2. **Minimal reproduction** — Isolate the failing case to the smallest possible input. Can you reproduce the failure with a 10-line input?
3. **A/B prompt testing** — Run working prompt and failing prompt side-by-side to find the exact difference causing the problem.
4. **Context inspection** — Audit what's actually in the agent's context at the moment of the bad decision. Print the full context if needed.
5. **Model comparison** — Run the same prompt on multiple models. If some work and some don't, it's a model capability issue. If all fail the same way, it's a prompt/context issue.

**Debugging anti-patterns:**
- *Debugging without logs:* Truly impossible to diagnose. Always log.
- *Changing multiple variables simultaneously:* If you fix the prompt and the context at the same time, you can't know which fix actually worked.
- *Blaming the model first:* The culprit is almost always the prompt or context, not model capability. Check those first.

---

### Cost and Latency

**The right mental model for AI API costs:** Don't ask "is this expensive?" Ask "what's the cost of NOT using it?"

**Real-world ROI example (3-person engineering team):**
- $12,000/month in total API costs (~$4,000 per engineer)
- Each engineer ships roughly a week's worth of work every single day
- 10× productivity multiplier on feature delivery

For a team where each engineer has a loaded cost of ~$150K/year ($12,500/month), spending an additional $4,000/month to 10× their output means the effective cost per unit of shipped work drops by 90%. The $4K/month cost is trivially small against that backdrop.

**When cost genuinely constrains you:**
- Batch processing millions of documents at scale
- Consumer products with thin margins and cost-per-request economics

**When cost is rarely the constraint:**
- Internal tooling (developer time cost >> API cost)
- Customer-facing features (revenue impact >> API cost)
- Prototyping (speed to learning >> API cost)

**Better metrics to track:**

| ❌ Poor Metric | ✅ Better Metric |
|---|---|
| Total API spend | Cost per feature shipped |
| Cost per token | API cost as % of engineer loaded cost |
| Agent invocations | Time-to-delivery vs. baseline |

**The multi-agent token paradox:**

Multi-agent architectures use ~15× more tokens than single-agent approaches. What do you get for that 15× overhead?
- 80× improvement in action specificity
- 100% actionable recommendation rate (vs. 1.7% for single-agent)
- Zero quality variance across trials

The surprising finding: this isn't primarily about speed — both single-agent and multi-agent achieve similar latency (~40 seconds for complex tasks). You're paying 15× more tokens for *deterministic quality*, not speed.

---

### Production Concerns

**Lifecycle Hooks — Real-Time Control and Observability**

Hooks are event handlers that fire at critical moments in agent execution. They enable real-time visibility and enforcement rather than after-the-fact analysis. Think of them as middleware for your agent: each hook intercepts a specific event in the execution lifecycle and can inspect, modify, block, or log what happens at that moment.

There are six hook types, each covering a different point in the lifecycle:

| Hook | When It Fires | Blocking? | Primary Use |
|---|---|---|---|
| `SessionStart` | When a new Claude session begins | No | Load context, inject conventions, restore session state |
| `PreToolUse` | Before any tool executes | **Yes** — exit code 2 blocks the tool | Validate commands, block dangerous operations, enforce git safety |
| `PostToolUse` | After a tool completes | No | Audit logging, cost tracking, PR notifications, quality gates |
| `Stop` | When a response completes | No | Batch formatting (Biome/Prettier), session state persistence, pattern extraction |
| `SessionEnd` | When the session closes | No | Final state persistence, cost metrics, cleanup |
| `PreCompact` | Before context compaction | No | Save critical state before context is compressed |

The blocking distinction matters enormously. `PreToolUse` is the only hook that can *prevent* an action. All others observe and react. This is by design — you want broad observability but surgical blocking authority.

**Hook matchers** — hooks can target specific tools or all tools:

```json
{ "matcher": "Bash" }          // fires only before Bash commands
{ "matcher": "Write" }         // fires only before file writes
{ "matcher": "Edit" }          // fires only before file edits
{ "matcher": "*" }             // fires before any tool
```

**The custom hook contract** — hooks are shell commands that receive tool metadata via stdin (JSON) and respond via stdout (JSON). Exit code 0 = success, exit code 2 = block (PreToolUse only), any other non-zero = error. This makes hooks composable with any language or tool: bash scripts, Python, Node.js, or compiled binaries.

**Hook profiles** — rather than maintaining separate hook configs per environment, profile-based configuration lets you toggle behavior via environment variables:

- **minimal** — only session state persistence + critical safety checks
- **standard** (default) — full suite: safety checks, quality gates, audit logging, pattern extraction
- **strict** — adds security scanning, enforces coverage minimums, blocks non-compliant commits

**Time budgets** — hooks block execution while running, so speed matters:

| Hook | Time Budget | If Exceeded |
|---|---|---|
| `SessionStart` | 3-5 seconds | Proceed with defaults |
| `PreToolUse` | 5-10 seconds | Log warning, proceed anyway |
| `PostToolUse` | 2-3 seconds (target) | Non-blocking, but slow hooks create backpressure |
| `Stop` | Up to 30 seconds | Acceptable — runs after response, user doesn't wait |

**Production hook patterns** — the most valuable hooks observed in production:

*Dev server blocker:* A `PreToolUse` hook on Bash that checks whether a dev server is already running (via tmux pane check) before allowing another `npm run dev`. Prevents the most common multi-session footgun: two servers on the same port.

*Git safety enforcer:* A `PreToolUse` hook on Bash that blocks `--no-verify` and `--no-gpg-sign` flag patterns. Prevents accidental bypass of pre-commit hooks and signing requirements.

*Compaction threshold counter:* A `PreToolUse` hook that increments a counter per tool call. At a configurable threshold (default: 50), triggers a strategic compact at a safe point (after planning, after research, never mid-implementation). This is more reliable than manual `/compact` discipline.

*Session state persistence:* A `Stop` hook that writes the current session's key facts, decisions, and progress to a markdown file. When the next session starts, `SessionStart` loads this file. Together they implement memory that survives context boundaries without external infrastructure.

*Pattern extractor:* A `Stop` hook that analyzes the session for recurring correction patterns and user preferences, writes them to `~/.claude/skills/learned/`, and builds up a personalized micro-skill library over time.

**Pre-edit dependency injection:** Before an agent edits a file, inject dynamic context — current imports, type definitions, available exports from the TypeScript language server. This prevents the most common implementation errors: missing imports, type mismatches, using functions that don't exist.

**Philosophy:** Permissive tools + strict prompts + hook enforcement. The agent has broad access; the prompt guides what it should do; hooks enforce the hard limits that must never be violated. This three-layer model means you can give agents wide tool access (needed for real autonomy) without losing safety guarantees (needed for production trust).

---

**Production Lessons from Large Codebases:**

*Boot new agents, don't salvage degraded ones.* Context confusion causes compounding errors. The cost of starting fresh is always less than the cost of debugging a degraded agent.

*CLAUDE.md as convention encoding.* A project conventions file that gets injected into every agent context. Agents can't infer all conventions by reading code — they need explicit documentation of architectural decisions, naming patterns, and team preferences.

*Test-first discipline.* One subagent writes failing tests. Another subagent makes them pass. A third reviews without any sunk-cost bias in the implementation. This separation prevents the reviewer from rationalizing bad code because they wrote it.

*Dedicated review gate.* The reviewing agent didn't write the code it's reviewing. No sunk-cost bias, no rationalization — just honest assessment.

*Opus 4.5 for orchestration.* Practitioner consensus from the field: Opus is notably better at managing teams of subagents and producing coherent multi-agent workflows.

---

### Evaluation — Measuring Whether Your Agent Actually Works

**Start immediately with 3-5 test cases.** Don't wait for a comprehensive test suite before evaluating. Three carefully chosen test cases reveal far more than zero:
- Happy path — the most common, expected use case
- Most likely failure mode — whatever you expect to break first
- Full end-to-end — the complete workflow from start to finish

**The evaluation progression:**

1. *Manual tracing* — run test cases by hand and read the full logs and outputs carefully
2. *Online user feedback* — deploy to a limited set of users with explicit feedback mechanisms
3. *Offline automated datasets* — build regression test suites from real production failures

**Turning failures into tests:** Every production failure should immediately become a test case: capture the exact input and context, define the expected output, add it to the regression suite, verify the fix prevents recurrence, run the test on every subsequent change. Production failures are the highest-signal test cases you'll ever get.

**The Compound Error Reality — Why Per-Step Accuracy Matters So Much:**

| Per-Step Accuracy | 10-Step Task Success |
|---|---|
| 99% | 90.4% |
| 95% | 59.9% |
| 90% | 34.9% |

Improving per-step accuracy from 95% to 99% more than doubles success on 50-step tasks. This is why optimizing the reliability of individual steps is the most leveraged investment in agent quality.

**Evaluation anti-patterns:**
- *Waiting for large eval suites before starting* — your requirements will change; start with 3-5 cases now
- *Testing only final outputs* — check intermediate reasoning, tool calls, and decision logic too
- *Relying solely on LLM judges* — LLMs have systematic biases (they prefer longer answers, certain positions in lists, well-written prose regardless of correctness). Always calibrate against human evaluation on a representative sample.
- *Ignoring cost and latency* — a 95%-accurate agent that takes 45 seconds and costs $2 per success may not be viable even if the accuracy is acceptable

---

### Long-Horizon Planning Under Compounding Consequences

When agents must maintain strategic coherence over extended periods (weeks, months), new failure modes emerge that don't surface in short-horizon tasks. YC-Bench (He et al., 2026) benchmarked agents on a simulated year-long startup operation with hundreds of decision points, revealing three critical insights for real-world systems that must manage long-term state and adapt to unfolding circumstances.

**Scratchpad Usage Predicts Success.** Agents that consistently maintained internal notes—tracking assumptions, past decisions, and implications—significantly outperformed those relying purely on prompt context. This is context management at the agent's own layer: when task length exceeds context windows, the agent must externalize its reasoning to persist information across turns. Unlike tool-use patterns that can be scripted, note-taking is a learned discipline. Agents that performed well explicitly created decision logs ("We chose vendor X because Y; if Z changes, reconsider this"), tracked financial state across turns, and maintained a running list of assumptions about client behavior. This mirrors human practice: domain experts maintain personal rubrics and decision journals. Absence of scratchpad forced agents to re-derive context from previous outputs on every turn, leading to inconsistent decisions and forgotten constraints.

**Adversarial Reasoning is the Primary Failure Mode.** 47% of agent bankruptcies in YC-Bench stemmed from agents failing to detect or respond appropriately to adversarial clients—a reasoning gap distinct from planning execution. The environment included clients who would deliberately mislead agents about contract terms, demand unfavorable renegotiations, or claim disputes to avoid payment. Agents trained on benign interactions lacked mental models for adversarial actors. When faced with a suspicious client, successful agents explicitly asked: "Is this actor trying to exploit us? What incentives do they have? How do we verify their claims?" Unsuccessful agents treated all interactions as honest information exchange. This reveals a gap in agent-level threat modeling: systems that lack explicit reasoning about adversarial scenarios default to assuming good faith, which is often false in competitive environments.

**Compounding Consequences Require Explicit Modeling.** Early mistakes (hiring the wrong employee, accepting a bad contract, over-committing runway) cascade into late-game constraints (payroll spirals, lost customer relationships, inability to pivot). Agents that succeeded explicitly modeled these compound effects rather than treating each decision independently. Successful agents maintained projections: "If we hire this team member, payroll becomes $X/month; we have Y months of runway; that leaves Z for marketing." They could trace how early mistakes constrained later options. Unsuccessful agents optimized each decision locally (take the contract, hire the person) without modeling the accumulating constraints. By month 6, they found themselves in untenable positions (high payroll, low revenue, no path forward) because no one was reasoning backward from the end state.

**Practical implications for deployment:**

For long-horizon agent applications (research assistants managing multi-month projects, business operations agents, supply-chain planners), three practices make a measurable difference:

1. **Mandatory scratchpad checkpoints.** At each turn or decision, require the agent to write a decision summary: what changed, what was decided, and what assumptions underpin the decision. Periodically (every 10 steps or when context nears capacity), have the agent review and synthesize its scratchpad to consolidate implicit learnings into explicit rubrics.

2. **Adversarial stress-testing.** Before deploying a long-horizon agent, test it against scenarios where information sources are unreliable, actors are incentive-misaligned, or explicit deception is involved. Add this to the evaluation suite. Agents that score well on benign test suites often fail dramatically when stakes create incentives for lying.

3. **Consequence-chain prompting.** When the agent makes a major decision (hiring, spending, committing to a strategy), insert a step that forces backward reasoning: "Assume this decision goes wrong; what would that look like? How would it constrain us later? Is that acceptable?" This simple frame dramatically improves detection of compound-consequence traps.

Scratchpad availability is not optional for long-horizon tasks — it's the agent's external memory for multi-turn coherence. Without it, agents lose information and repeat mistakes. The adversarial reasoning gap is often invisible until deployment, making pre-deployment stress-testing essential. And modeling compounding consequences is not sophisticated reasoning; it's basic second-order thinking that improves measurably when explicitly prompted.

---

### Intent Engineering

Prompt engineering tells an agent *what to do*. Context engineering tells it *what to know*. Intent engineering tells it *what to want* — and it operates at a level above both.

The core problem it addresses: organizations have largely solved "can AI do this task?" and mostly failed to solve "can AI do this task in a way that serves our actual goals?" These are very different questions, and the gap between them is where production AI systems most often break down.

**The Klarna case study — the canonical example**

Klarna deployed an AI customer support agent that handled 2.3 million conversations monthly, cut resolution times from eleven minutes to two minutes, and saved $60 million. By every metric it was given, it succeeded. The CEO later publicly acknowledged the strategy had backfired and began rehiring humans.

What went wrong: the agent optimized for speed and cost reduction — measurable, legible metrics — while quietly destroying the customer relationships and trust that actually drove retention. It succeeded at the wrong thing. Nobody told it that "resolve quickly" and "preserve customer loyalty" were in tension, or which one to prioritize when they conflicted.

This is the intent gap. The agent did exactly what it was measured on. The organization failed to encode what it actually needed.

**What intent engineering involves**

Intent is what determines how an agent acts when explicit instructions run out — when it hits an ambiguous case, a tradeoff not covered in the spec, a situation the prompt didn't anticipate. Without encoded intent, agents default to optimizing for whatever is most legible: speed, task completion, literal instruction-following. With it, they can reason about edge cases in alignment with what the organization actually values.

A complete intent specification for an agent covers seven components:

1. **Objective** — the problem being solved and its business value
2. **Desired outcomes** — observable state changes that indicate success (not just task completion)
3. **Health metrics** — non-regression constraints that must be maintained even while optimizing (e.g., CSAT must not drop below 4.2)
4. **Strategic context** — the broader system the agent operates within
5. **Constraints** — steering rules (soft guidance) and hard enforced limits
6. **Decision authority** — which decisions the agent can make independently vs. must escalate
7. **Stop rules** — when to halt, escalate, or declare completion

The customer support example properly specified: *objective* = resolve issues without creating frustration; *desired outcome* = customer confirms resolution, no repeat ticket within 24 hours; *health metric* = CSAT stays above 4.2. An agent with these constraints cannot optimize resolution speed at the expense of satisfaction — the health metric makes that tradeoff explicit and bounded.

**Intent engineering vs. the other disciplines**

| Discipline | Tells the agent... | Time horizon |
|---|---|---|
| Prompt craft | What to do right now | Per-request |
| Context engineering | What to know | Per-session |
| Intent engineering | What to want / optimize for | Persistent infrastructure |

Intent engineering sits closest to organizational strategy. It's less about any individual prompt or agent and more about what gets encoded into the infrastructure that agents run on — the standing values, tradeoffs, and decision hierarchies that should govern autonomous behavior across all tasks.

Gartner predicts 40% of agentic AI projects will be cancelled by 2027. The most common reason won't be that the agents couldn't do the task — it'll be that they did the task while failing to preserve what the organization actually cared about.

---

### Specification Engineering Primitives

As agents become capable of running autonomously for hours or days, the bottleneck shifts from real-time prompt iteration to upfront specification quality. You can't course-correct a long-running agent mid-task the way you'd refine a chat prompt. Everything the agent needs to succeed must be encoded before it starts.

Specification engineering is the practice of writing agent-readable documents complete enough for autonomous execution. Five primitives define what a good specification contains:

**1. Self-contained problem statement**

All context the agent needs is in the spec. The agent should never have to guess about project conventions, user preferences, or background state. If the agent has to ask a clarifying question before it can start, the problem statement failed.

*Practice:* Write the request as if the recipient has zero prior knowledge. If you find yourself thinking "they'll know what I mean," that assumption is the gap.

**2. Clear acceptance criteria**

Three or fewer verifiable sentences that define what "done" looks like. Not "build a good dashboard" — "the dashboard displays daily active users, 30-day retention, and revenue by segment; all three charts update when the date filter changes; page load time is under two seconds."

Acceptance criteria serve two purposes: they tell the agent what to aim for, and they give you a way to evaluate whether the output is actually done rather than just reasonable-looking.

*Practice:* Before handing any task to an agent, write three sentences that would let a stranger verify completion without asking you.

**3. Constraint architecture**

Four layers of constraint, each serving a different function:
- *Must do* — required behaviors with no exceptions
- *Must not do* — hard limits that should trigger escalation if approached
- *Prefer* — soft guidance for ambiguous cases (when in doubt, choose X over Y)
- *Escalate when* — conditions that should pause execution and request human input

Without explicit constraints, agents default to whatever behavior minimizes task friction — which is not always the right behavior.

**4. Decomposition**

Break large tasks into independently executable subtasks, each under roughly two hours of agent work. Tasks that are too large create compounding error risk (see the per-step accuracy table above) and make debugging nearly impossible when something goes wrong.

The test for good decomposition: could you hand each subtask to a different agent, with no shared context, and have it produce a useful artifact? If not, the task is still too coupled.

**5. Evaluation design**

For any task you'll run repeatedly, define how you'll verify the output is actually good — not just plausible-looking. Three to five test cases with known good outputs let you catch regressions when models update, prompts change, or edge cases appear in production.

*Practice:* After completing a recurring AI task successfully, capture that input/output pair as a test case. Over time, this builds institutional knowledge about what "good" looks like for your specific use case — knowledge that doesn't exist anywhere else.

**The cumulative stack**

These four disciplines build on each other:

```
Specification engineering (what to build, fully specified)
  requires →  Intent engineering (what to optimize for)
    requires →  Context engineering (what to know)
      requires →  Prompt craft (how to express it)
```

Failures at higher levels are increasingly severe — a great prompt in service of the wrong intent causes more damage than a poorly phrased prompt for the right one. Getting the stack right, from bottom to top, is the compounding investment.

---

## 9. Mental Models

### The Pit of Success

> Design systems where the easiest path is also the correct path.

This concept comes from Rico Mariani's work on .NET Framework design. Traditional system design erects guardrails and checks to prevent developers from making mistakes — you have to work to avoid the pitfalls. The Pit of Success inverts this: instead of building guardrails, design the system so the natural, easy, obvious path leads directly to the right outcome. Success is the path of least resistance.

```
Traditional approach:           Pit of Success:

  ┌─────────┐                       ╲         ╱
  │ SUCCESS │                        ╲       ╱
  └────▲────┘                         ╲     ╱
       │ climb                         ╲   ╱
       │ against gravity                ╲ ╱
  ─────┴─────                         SUCCESS
  (you must work upward)          (you fall naturally into it)
```

**Applied to the context window:** The context window is the most powerful Pit of Success lever in agentic engineering. LLMs are next-token prediction machines — every token in the context window influences the probability distribution over output tokens. The context window isn't just "information for the model" — it's a gravitational field that pulls outputs toward certain regions of possibility space.

Good context (relevant examples, clear instructions, structure) makes the correct output the statistically dominant continuation. Poor context (vague, irrelevant, contradictory) splits the probability mass across many competing outputs — some correct, some not.

**Three mechanisms that make context a Pit of Success:**

1. **Attention flows to what matters:** Information near the *end* of the context gets more attention (recency bias). Related information grouped together creates coherent attention patterns. Structural clarity helps attention form correctly. These aren't bugs — they're how transformer attention works. Design with them, not against them.

2. **Examples shift the distribution:** Few-shot examples don't just "show the model what to do" — they literally shift the probability distribution over output tokens. Including an example of your desired output format at inference time is training data. Choose examples that pull output distribution toward what you want.

3. **Context primes token sequences:** "Let me think step by step" primes chain-of-thought output. A code block primes more code. Technical vocabulary primes technical output. You're not convincing a mind — you're setting up the probability environment so that the desired continuation is statistically dominant.

**Designing for the Pit of Success:**

Make the correct output the only sensible continuation of the context:

```
# Weak — many valid continuations, none clearly correct
"Handle this user request appropriately."

# Strong — the correct output is the obvious next thing
"Respond to this user request with a JSON object containing:
- 'action': one of ['approve', 'deny', 'escalate']
- 'reason': a single sentence explanation

User request: {request}

Response:"
```

The second version doesn't leave room for the model to invent a different format. The JSON structure has been primed; "Response:" creates an immediate gap that must be filled.

**Eliminate competing attractors:** Don't include examples of things you *don't* want. Don't hedge instructions. Remove irrelevant context that could prime wrong directions. Every element in the context is either pulling output toward the right answer or competing with that pull.

---

### Specs as Source Code

> Throwing away prompts after generating code is like checking in compiled binaries while discarding the source code.

Articulated by Sean Grove. This mental model fundamentally reframes what's primary and what's secondary in AI-assisted development.

In traditional software development:
- **Source code** is the primary artifact — what you maintain, review, and version control
- **Compiled binary** is the derivative artifact — you throw it away and regenerate it from source

In agentic programming:
- **Specifications** are the primary artifact — what you maintain, review, and version control
- **Generated code** is the derivative artifact — you can always regenerate it from the spec

```
Traditional:               Agentic:

┌──────────────┐           ┌──────────────┐
│ Source Code  │           │ Specification│  ← Primary, maintain this
└──────┬───────┘           └──────┬───────┘
       │ compile                  │ agent reads
       ↓                          ↓
┌──────────────┐           ┌──────────────┐
│   Binary     │           │ Generated    │
│ (throwaway)  │           │ Code         │  ← Derivative, regeneratable
└──────────────┘           └──────────────┘
```

**What this changes in practice:**

*Version control:* Check in specs, research documents, and planning artifacts — they're the source. The diff to a spec file is more important than the diff to the code it produces. If you delete the spec after generating code, you've lost the source.

*Code review:* Review the spec for correctness, completeness, and testability. If the spec is right, the code can always be regenerated. A wrong spec generates a lot of wrong code very efficiently.

*Project structure:*
```
specs/                   ← Primary (version controlled, reviewed)
  architecture.md
  requirements.md
  plan.md
src/                     ← Derivative (regeneratable from specs)
  main.py
```

**The BMAD Pattern — Living Artifacts Through Four Phases:**

1. *Analysis Phase* → Product Brief, Research Summary
2. *Planning Phase* → PRD (Product Requirements Document), UX Design
3. *Solutioning Phase* → Architecture Document, Epics/Stories
4. *Implementation Phase* → Working Code (generated from the above docs)

Phases 1-3 produce documents. Phase 4 produces code *from* those documents. The documents are the truth; the code is a consequence of the truth.

**Adversarial review gates between phases:** Before moving from one phase to the next, an orchestrator critically examines each artifact. This prevents: incomplete PRD → flawed architecture → thousands of lines of correctly-implemented wrong behavior.

**When to apply:**
- Multi-agent systems (specs become the shared interface between agents)
- Long-lived projects (future agents understand the system by reading specs)
- Complex domains where *why* something was decided matters as much as *what* was decided
- Regulated industries (compliance becomes inherent to the process, not post-hoc documentation)

**When it's overkill:**
- One-off scripts or throwaway automation
- Exploratory prototypes where you're still figuring out what to build
- Stable finished systems that won't change

**Common pitfalls:**
- *Spec drift:* Specs and implementation diverge over time. Fix: make spec updates part of the change workflow; test that implementation matches specs.
- *Over-specification:* Specs become harder to maintain than the code they describe. Fix: capture intent and constraints, not line-by-line implementation decisions.
- *Vague specs:* Too high-level to be executable. Fix: think "testable" — if you can't verify whether the spec was followed, it's too vague.

---

### Execution Topologies

When building multi-agent systems, you have to choose how agents are connected and how work flows between them. These are the five fundamental topologies:

| Topology | Structure | Best For |
|---|---|---|
| **Parallel** | All agents start simultaneously, results gathered at end | Independent tasks, maximum throughput |
| **Sequential** | Agent A → Agent B → Agent C (each feeds the next) | Dependent phases where each step requires the previous step's output |
| **Synthesis** | Multiple independent agents → one agent synthesizes all outputs | Research aggregation, multi-perspective review |
| **Nested** | Agents that spawn their own sub-agents | Complex hierarchical task decomposition |
| **Persistent** | One long-running agent with continuously evolving state | Continuous workflows, growing knowledge bases |

**How to know if your system is improving over time — Four Improvement Vectors:**

1. **Wider** — handles more diverse types of tasks than before
2. **Deeper** — makes progress further into complex multi-step tasks
3. **Thicker** — produces higher-quality outputs at the same task difficulty
4. **Less Friction** — requires less human intervention to complete the same tasks

**The Autonomy Spectrum:**

| Level | Name | Human Role |
|---|---|---|
| 1 | Augmentation | Human does the work; AI assists at specific moments |
| 2 | Copilot | Human leads; AI suggests next steps |
| 3 | Supervised Autonomy | AI acts; human reviews each output |
| 4 | Delegated Autonomy | AI acts autonomously; human approves at phase gates |
| 5 | Full Autonomy | AI acts end-to-end without human intervention |

**What's achievable today (2025):** Well-scoped coding tasks, document processing, data transformation — these can reliably reach Level 4-5.

**Not yet reliable:** Novel problem-solving requiring genuine judgment in ambiguous situations, tasks with unclear success criteria, high-stakes irreversible operations where the cost of error is catastrophic.

---

### Context as Code

Context is not just "background information." Context is an executable specification for agent behavior.

A well-designed context that defines the agent's identity, its domain knowledge, the success criteria for the task, and available tool patterns is functionally a program. The agent executes against the context the same way a traditional computer program executes against instructions.

**The implication:** Context deserves the same engineering rigor as code. It should be:
- **Version controlled:** Track changes, understand history, revert if needed
- **Reviewed:** Someone other than the author checks it for correctness
- **Tested:** Verify that specific context produces specific outputs reliably
- **Iterated:** Improve it systematically based on observed performance

Treating context as a casual prose document leads to unreliable agents. Treating it as code leads to reliable, improvable, maintainable agents.

---

### Externalization: The Cognitive Architecture Lens

> Modern agent progress is increasingly driven by reorganizing infrastructure, not upgrading model weights.

This framing, from Zhou et al. 2026, offers a useful architectural lens: the history of LLM agents is a story of **externalization** — progressively moving cognitive functions that used to live inside model parameters into dedicated external systems. When you add a vector database for memory, a skill library for procedures, or a harness that enforces approval gates, you're externalizing cognition.

This matters because it shifts how you diagnose agent failures. Rather than asking "does my model understand the task?" you ask: "which cognitive function is inadequately externalized?"

**The three-layer evolution:**

```
Weights layer:  Knowledge, behavior, and skills are baked into model parameters.
                Durable but static — changing them requires retraining.

Context layer:  Dynamic information flows in via the context window.
                Flexible but ephemeral — gone when the session ends.

Harness layer:  Runtime infrastructure (memory stores, skill libraries, protocols,
                orchestration) persists beyond any single model call.
                The emerging design frontier.
```

Modern agent development operates primarily at the harness layer. Models haven't changed as fast as the infrastructure wrapping them.

**The four externalization types:**

| Dimension | What's Externalized | Why It Matters |
|---|---|---|
| **Memory** | State across time — working context, episodic experience, semantic knowledge | Without memory externalization, agents reset with every session |
| **Skills** | Procedural expertise — reusable procedures, decision heuristics, normative constraints | Without skill externalization, behavior must be re-specified in every prompt |
| **Protocols** | Interaction structure — agent-tool, agent-agent, agent-user contracts (MCP is the canonical example) | Without protocol externalization, each integration is bespoke |
| **Harness** | Runtime coordination — orchestration, sandboxing, human oversight, observability, context budget management | The unifying layer; coordinates Memory, Skills, and Protocols |

The Harness is architecturally distinct: it's not a fourth *type* of externalization — it's the runtime environment within which the other three operate.

**Failure modes through this lens:**

The externalization model reframes common agent failures as representational mismatches — a cognitive function that should be externalized still lives (poorly) in the prompt or the model:

- *Stale memories:* The memory store misrepresents current state (externalized, but not maintained)
- *Context flooding:* Memory retrieves too much (externalization without relevance filtering)
- *Prompt bloat:* Procedural knowledge lives in the system prompt instead of a skill library (not yet externalized)
- *Bespoke integrations:* Tool interfaces are hand-coded per agent instead of protocol-governed (not yet externalized)
- *Unsafe skill composition:* Combining externalized skills creates boundary conditions neither skill anticipated

**Relationship to the Four Pillars:**

This mental model doesn't replace the Four Pillars (Prompt, Model, Context, Tool Use) — it sits above them as a *why*. The Pillars describe what you're configuring; externalization explains the architectural trend of where those configurations are moving. Tools become protocols; context becomes memory stores; prompts become skill libraries.

(Source: Zhou et al. 2026, "Externalization in LLM Agents," arXiv:2604.08224)

---

## 10. Agent Frameworks

Four major frameworks for building agentic systems, each with a distinct philosophy:

**LangGraph** — Workflows as stateful graphs. You define your workflow as a directed graph with explicit nodes (steps) and edges (transitions). Gives you complete control over every step and handles state checkpointing (the ability to pause and resume workflows). Best for: complex branching workflows with conditional logic, enterprise applications requiring durability and auditability.

**CrewAI** — Agents as role-playing teams. You define agents with roles ("researcher," "writer," "critic"), and they collaborate on tasks using those roles. Very intuitive to set up quickly. Best for: rapid prototyping, workflows with clear role separation.

**Microsoft Agent Framework** — Conversation-based collaboration. Agents interact primarily through conversation protocols. Built for Azure-native deployment. Best for: Microsoft/Azure ecosystem integration, dynamic multi-agent collaboration.

**Claude Agent SDK** — Deep tool integration with Anthropic models. A harness for building autonomous agents with sophisticated tool use. Best for: applications building deeply on Anthropic models, rich tool integration.

| Framework | Choose When |
|---|---|
| LangGraph | Complex stateful workflows with checkpoints, enterprise reliability requirements |
| CrewAI | Rapid prototyping, team-based collaboration with clear roles |
| Microsoft Agent Framework | Azure-native deployment, dynamic agent collaboration |
| Claude Agent SDK | Deep tool integration, Anthropic models, sophisticated autonomy |

**Hybrid strategy:** Prototype in CrewAI (fastest to get running), productionize in LangGraph (most control and durability). Use MCP (Model Context Protocol) as an integration layer to connect agents across different frameworks when needed.

---

### LangChain vs LangGraph

These two come from the same ecosystem but are typically chosen as **alternatives for workflow orchestration** — you pick one based on how complex your workflow is. The common mental model in practice: LangChain for simple, LangGraph for complex.

#### The Core Architectural Difference: DAG vs Cyclic Graph

This is the root of everything:

**LangChain chains (LCEL)** execute as a **DAG — Directed Acyclic Graph**. Data flows in one direction, step by step, with no loops. Input → A → B → C → Output. That's it. Great when your workflow is predictable and sequential. Awkward or impossible when it needs to branch conditionally or retry.

**LangGraph** executes as a **cyclic graph**. Nodes connect via edges that can loop back. This is what enables: retrieve → grade → if bad, rewrite and retrieve again → if good, generate. The cycle is native to the model, not bolted on.

The loop capability is the primary reason people reach for LangGraph.

#### LangChain — Simple, Linear Workflows

LangChain (2022) is a **component library + chain runner** for building LLM applications:

- **LCEL chains** — compose components into sequential pipelines: prompt → LLM → parser
- **Retrievers** — standardized interface over 50+ vector stores and search engines
- **Tools** — wrappers for APIs, code execution, web search
- **Memory** — conversation history (buffer, summary, vector-based)
- **Integrations** — connectors to every major LLM provider and data source

Ideal for: chatbots, summarization, single-pass Q&A, simple RAG, content generation — any workflow that takes an input, processes it linearly, and returns an output.

**The ceiling:** When your workflow needs to make a decision mid-run and loop back (query rewriting, retries, multi-step reasoning), LangChain chains hit a wall. The DAG structure prevents it.

#### LangGraph — Complex, Stateful Workflows

LangGraph (2024) is a **stateful graph runtime** for workflows that need control flow:

- **Explicit state** — a typed `State` object flows through every node; every node can read and modify it
- **Nodes** — Python functions: receive state, return updated state
- **Edges** — direct (always go to B) or conditional (go to B or C based on state)
- **Cycles** — loops are first-class. Retrieve → grade → rewrite → retrieve again is trivial to model
- **Checkpointing** — pause mid-graph, persist state, resume later (essential for human-in-the-loop)
- **Streaming** — emit partial state at each step

Ideal for: agentic RAG with grading and rewriting, multi-agent systems, long-running workflows with human approval gates, anything that adapts based on intermediate results.

#### The "Together" Nuance

LangGraph was built on top of LangChain's primitives, so technically they can coexist — a LangGraph node can call `ChatAnthropic` or use a LangChain retriever internally. But in practice, **you pick one as your orchestration layer** and use it consistently. You don't usually run both chain orchestration and graph orchestration in the same pipeline.

**LangSmith** (observability) works with both regardless of which you choose.

#### When to Use Each

| Scenario | Use |
|---|---|
| Chatbot, Q&A bot, summarization tool | LangChain — linear chain is sufficient |
| Simple RAG (retrieve → prompt → answer) | LangChain — no looping needed |
| RAG with query rewriting and relevance grading | LangGraph — requires cycles |
| Multi-agent system with handoffs and state | LangGraph — explicit node/edge model |
| Workflow that needs to pause for human review | LangGraph — checkpointing |
| Rapid prototype needing many integrations fast | LangChain — breadth of connectors |
| Production agent with conditional retry logic | LangGraph — cycles + explicit state |
| Debugging a 6-step pipeline with state visibility | LangGraph — every transition is inspectable |

#### Decision Rule

**Start with the question: does your workflow need to loop?**

- No loops, no branching → LangChain chains are simpler and faster to build
- Loops, conditional paths, or stateful persistence → LangGraph

Most real agents eventually need loops. That's usually when teams migrate from LangChain to LangGraph.

---

## 11. Development Methodologies

> **Adapted from:** Claude Code Ultimate Guide by Florian Bruniaux (CC BY-SA 4.0)

Building reliable agents requires choosing the right development methodology — the process you follow when writing and testing code. There is no single "best" methodology, but there are worse and better choices depending on what you're building.

### Fifteen Methodologies Arranged by Tier

The methodologies form a pyramid. The base (Tier 1) represents foundational practices every team should follow. The upper tiers add discipline and structure as the stakes increase.

**Tier 1: Foundational (Essential)**
- **BMAD** (Build-Measure-Analyze-Decide) — The product development cycle: build a feature, measure how it performs, analyze results, decide next steps
- **GSD** (Get Stuff Done) — Pragmatism over process; useful for early prototypes and discovery phases
- **SDD** (Specification-Driven Development) — Specs are written before code; the spec is the contract

**Tier 2: Quality-Focused**
- **TDD** (Test-Driven Development) — Write tests first, implement to pass tests
- **BDD** (Behavior-Driven Development) — Tests express business behavior in human-readable language (Given/When/Then)
- **DDD** (Domain-Driven Development) — Code is organized around domain concepts; developers deeply understand the business domain

**Tier 3: Architecture & Scale**
- **CQRS** (Command Query Responsibility Segregation) — Read and write operations use different data models; useful when read and write patterns diverge dramatically
- **Event Sourcing** — All changes are recorded as immutable events; current state is derived from the event stream
- **Saga Pattern** — Long-running distributed transactions are coordinated as a series of local transactions with compensating actions

**Tier 4: Resilience & Safety**
- **LOSA** (Layers of Observation, Simulation, Adaptation) — Multi-layer safety: observe system behavior, simulate failures, adapt based on observations
- **Chaos Engineering** — Deliberately break things in production to understand failure modes before they cause customer impact
- **Circuit Breaker Pattern** — Monitoring + automatic degradation: detect failure patterns and fail fast rather than waiting for timeout

**Tier 5-6: Advanced**
- **Declarative Infrastructure** — Infrastructure is code; immutable and version controlled
- **Observability Engineering** — Metrics, logs, traces are first-class concerns built into architecture from the start

### How to Choose the Right Methodology

The decision tree is simple:

**Step 1: What's the stakes?**
- Low (prototype, internal tool) → GSD + BMAD
- Medium (production service, moderate risk) → SDD + TDD + BDD
- High (financial system, healthcare, irreversible actions) → Add DDD, CQRS, Chaos Engineering

**Step 2: How fast does it need to evolve?**
- Very fast (startup MVP) → Minimize process, maximize iteration
- Moderate (steady-state product) → SDD + TDD for predictability
- Stable (mature system) → Maximize observability and resilience; accept slower iteration

**Step 3: How critical is correctness?**
- Correctness doesn't matter much (entertainment, content generation) → GSD works
- Correctness matters (data consistency, financial accuracy) → Require tests and specs
- Correctness is non-negotiable (life-safety, regulatory) → DDD, CQRS, Chaos Engineering, full observability

### Plan-First Methodology

From Boris Cherny's observations on production code: **"Once the plan is good, the code is good."** This is the single highest-leverage principle across all tiers.

The pattern:
1. **Write the specification** — What are we building? What are the success criteria? What are the constraints?
2. **Design the interface** — What does the code expose? What are the inputs and outputs?
3. **Plan the implementation** — Break it into small, verifiable steps (TDD calls these "tests," but the structure is the same)
4. **Implement** — Execute the plan; each step produces code that passes the corresponding test
5. **Refactor** — Now that it works, make it clean

The cognitive science: Writing the plan forces you to think deeply about the problem before you start coding. This eliminates rework. Coders who skip the plan spend more time debugging than coders who plan thoroughly.

**Implementation:** Use specs-first workflows (Section 9 of *Mental Models* covers this). Spec first, then tests, then code. The spec is the contract; the tests verify the contract is met; the code implements it.

---

## 12. Dual-Instance Planning

> **Adapted from:** Claude Code Ultimate Guide by Florian Bruniaux (CC BY-SA 4.0)

When building complex agents or features, splitting the work into a **Planner** and an **Implementer** significantly improves quality. The Planner's job is pure strategic thinking; the Implementer's job is execution.

### The Pattern

**Planner instance:**
- Writes the specification, design document, and implementation plan
- Designs the system architecture and component interactions
- Reviews the implementer's work against the spec
- Never implements code; only reviews it

**Implementer instance:**
- Reads the plan and builds exactly what the plan says
- Can suggest refinements to the plan, but the planner approves
- Tests extensively; writes code that passes tests
- Never diverges from the plan without planner approval

### When It Pays Off

The overhead is ~$100–200/month in token costs (running two instances instead of one). It pays off when:

- **Complexity is high** — More than 2,000 lines of code, multiple components interacting
- **Correctness is critical** — Financial code, security-sensitive code, complex business logic
- **You want better code reviews** — The planner catches architectural issues; the implementer catches implementation bugs

**Cost-benefit:** Dual-instance planning breaks even after 2–3 correction cycles. If you would normally need to fix architectural mistakes by hand, the planner catches them at the design stage and saves more time than it costs.

### Quality-Over-Speed Decision Matrix

| Scenario | Single Instance | Dual Instance |
|----------|---|---|
| Prototype, low risk | ✓ Faster | ✗ Overkill |
| Feature, medium risk | Mixed | ✓ Recommended |
| Complex feature, high risk | ✗ Error-prone | ✓ Strongly recommended |
| Critical system, regulatory | ✗ Insufficient | ✓ Essential |

**Implementation:**
- Start with a single instance writing the spec
- Once the spec is solid, switch to dual instance (planner reviews, implementer builds)
- If reviews reveal major architectural issues, the planner revises the spec
- The implementer tests and iterates until the code passes the plan

---

## 13. Event-Driven Agents

> **Adapted from:** Claude Code Ultimate Guide by Florian Bruniaux (CC BY-SA 4.0)

Most agents are **pull-based**: they wake up when a user asks a question, retrieve information, and respond. Event-driven agents are **push-based**: they listen to external events (Linear cards being created, PRs being opened, CI/CD pipelines finishing, database changes) and act on those events autonomously.

### The Pattern

External event sources (Linear, GitHub, Slack, databases) emit events. An agent subscribes to those events, decides whether to act, and executes actions. The cycle is:

1. **Event arrives** — A card is assigned, a PR is created, a test fails, a database query completes
2. **Agent detects event** — Via webhook, polling, or event stream subscription
3. **Agent evaluates** — Does this event require my action? Is it aligned with my constraints?
4. **Agent acts** — Execute the appropriate action (create a task, leave a comment, run a cleanup, post to Slack)
5. **Cycle repeats**

### Key Guardrails

**Idempotency:** An agent must be safe to run multiple times on the same event without producing duplicate actions. Use idempotency keys: every action is tagged with a unique identifier. Before acting, check if the action was already taken.

**Concurrency limits:** If multiple events arrive simultaneously, the agent shouldn't spawn a thousand parallel operations. Implement a queue with bounded concurrency (e.g., "process at most 5 events in parallel").

**Circuit breaker:** If the agent fails repeatedly on the same event, it should stop trying and escalate. Don't let it retry infinitely; that's how runaway costs happen.

**Self-reinforcing loops:** An agent's action can trigger another event, which triggers the agent again. This is useful for iterative refinement, but implement a depth limit: "after 3 rounds of refinement, stop and ask for human input."

### Real Examples

**Continuous document generation:** A webhook fires when a KB doc is updated. The agent regenerates related diagrams, cheatsheets, and Q&A. Users always see consistent, up-to-date artifacts.

**Auto-remediation:** Monitoring system detects a spike in error rate. The agent automatically checks logs, identifies the issue, rolls back the most recent deployment, and posts a summary to Slack. Human reviews and approves the action.

**PR review bot:** When a PR is created, the agent analyzes the code, runs linters, checks for security issues, and leaves comments. No human needed until the PR is ready for merge.

---

## 14. Team AI Coordination

> **Adapted from:** Claude Code Ultimate Guide by Florian Bruniaux (CC BY-SA 4.0)

As teams grow beyond 3–5 developers, using a single shared agent configuration becomes unwieldy. Different developers have different needs: Alice needs security-focused guidance, Bob needs infrastructure expertise, Charlie needs to understand data pipelines. Team AI Coordination uses **profile-based module assembly** to give each developer a customized agent.

### The Pattern

A **profile** is a YAML file that describes a developer's role and tools. The profile assembles reusable modules:
- Shared modules (everyone uses these: basic Python linting, git helpers)
- Role-specific modules (security modules for Alice, infrastructure modules for Bob)
- Skill modules (optional domain knowledge: "ML systems" module, "payment processing" module)

When a developer starts their session, a script reads their profile and assembles a customized agent configuration.

### Four Components

**1. Shared modules** — Reusable instruction sets: Python best practices, git workflow, testing patterns, code review checklists.

**2. YAML profiles** — Role definitions:
```yaml
developer:
  name: alice
  role: security-engineer
  modules:
    - shared/python
    - shared/git
    - security/threat-modeling
    - security/owasp
    - database/access-control
```

**3. Skeleton template** — A base prompt that every agent gets, regardless of profile. It establishes tone and fundamental constraints.

**4. Assembler script** — Reads the profile, loads the modules in the right order, and constructs the final system prompt.

### Why This Works

**Scalability:** With centralized management, you update a module once and every developer using that module benefits.

**Consistency:** All developers follow the same patterns; no silos where one team has better processes than another.

**Specialization:** Security engineers get security-focused guidance; infrastructure engineers get infrastructure-focused guidance. The same underlying system, customized to context.

**Maintenance:** 59% token reduction compared to a single bloated agent configuration that tries to handle everything. Only load the knowledge needed for the current role.

**Zero drift:** The YAML files are the source of truth. Developers can't accidentally diverge because they're executing a shared assembly, not managing individual configs.

### When to Adopt

**Scaling threshold:** Teams with 5+ developers or multi-tool scenarios (some developers use Claude Code, others use GitHub Copilot, others use custom tools).

**Before threshold:** A single shared configuration with optional toggles is simpler.

---

## 15. Multi-Agent Shared Context & Query Routing

> **Status:** Frontier problem. Not fully solved. Industry consensus emerging but no silver bullet yet.

When you have multiple agents working on the same task, they need access to shared knowledge. But dumping your entire knowledge base into context is expensive (token bloat) and inefficient (noise). The alternative — **selective retrieval** — creates a harder problem: how do you know what to retrieve, and when?

This is one of the most under-discussed challenges in multi-agent systems. Most teams encounter it in production and have to improvise solutions. Understanding the problem and tradeoffs is more valuable than pretending a magic solution exists.

### The Core Problem: Query Routing Under Uncertainty

Agent A is working on a task. It needs context. But:

- **Query under-specification** — The agent doesn't know exactly what to ask for ("I need info about X" — but X is underspecified)
- **Relevance uncertainty** — Even if the agent formulates a query, it doesn't know if the results will actually help
- **Timing uncertainty** — Should it query now, or wait? Query early and you might retrieve docs that become stale. Query late and you might have already made a wrong decision.
- **False negatives** — The agent doesn't think to query for something it needs (unknown unknowns)

**Concrete failure:**
```
Agent A is designing a payment API.
It thinks: "I need API design patterns"
It queries KB: "API design"
KB returns generic docs on REST, CRUD, etc.

Agent A misses: "For payment systems, you must also check fraud flags before processing"
That doc exists in KB but under "fraud detection" or "compliance" not "API design"
Agent A never thought to query for fraud, so it didn't find it.

Result: Agent ships incomplete design. You catch it in code review. Wasted time.
```

### Why This Is Hard: Four Fundamental Reasons

**1. Query formulation is itself reasoning**

To ask the right question, you need to already understand the problem deeply. But the point of querying is to *fill gaps* in understanding. This is circular.

Example:
```
Junior engineer: "I need help with performance"
Senior engineer: "Performance of what? Queries? Network? Rendering?"
Junior engineer doesn't know, because they don't understand the problem deeply yet.

Same thing happens with agent queries. The agent doesn't know what it doesn't know.
```

**2. Semantic matching is probabilistic, not deterministic**

Vector databases use embedding similarity. But:
```
Agent queries: "How do we handle async operations?"
KB has docs titled:
- "Concurrency patterns" (0.87 similarity)
- "Non-blocking I/O" (0.79 similarity)
- "Task queues" (0.71 similarity)
- "Threading best practices" (0.65 similarity)

At what similarity threshold do you return results?
If you set it at 0.80, you miss "Task queues."
If you set it at 0.70, you get "Threading" which might not be relevant.
```

This is a signal/noise tradeoff. There's no universally correct threshold.

**3. Timing creates a trilemma**

You must choose one:

| Approach | Pros | Cons |
|---|---|---|
| **Retrieve early** | All context available; no latency hits during reasoning | Docs might become stale; context bloat; you retrieve 50 docs to avoid missing 1 |
| **Retrieve just-in-time** | Minimal context; up-to-date information | Latency hit every query; if KB is slow, agent is blocked; context keeps changing |
| **Retrieve continuously** | Always current | Token explosion; unstable context (always changing); expensive |

There's no solution that wins on all three dimensions.

**4. Agents hallucinate queries (ask for docs that don't exist)**

```
Agent: "I need the 2024 security audit report"
KB: No results found

Agent then:
Option A: Proceeds without the doc (incomplete reasoning)
Option B: Hallucinates what was in the doc (confident false answer)
Option C: Escalates to human

Most agents do A or B. Neither is good.
```

---

### What Actually Works Today (Honest Tradeoffs)

**Option 1: Explicit Routing (Most Reliable)**

You engineer the orchestration yourself:

```python
# Pseudo-code
task = "Refactor authentication module"

# Step 1: Agent thinks about the task
agent_a = spawn_agent("architect", prompt=base_prompt)

# Step 2: YOU decide what context is needed
context = retrieve_from_kb(["auth-patterns", "security-best-practices"])

# Step 3: Agent gets context, proceeds
result = agent_a.work_on(task, context=context)

# Step 4: At specific checkpoints, retrieve more context
if step == "implementation":
    context += retrieve_from_kb(["testing-patterns", "error-handling"])
```

**Pros:**
- Predictable; no surprises
- Debuggable; you see exactly what context each agent gets
- Efficient; only retrieve what you know is needed

**Cons:**
- Not scalable; requires manual engineering per workflow
- Brittle; if task changes, you need to update routing rules
- Inflexible; agents can't ask for unexpected info

**When to use:** Small number of well-defined workflows. High stakes (compliance, security). Teams with time to engineer orchestration.

---

**Option 2: LLM-Driven Routing (Most Flexible)**

Let the agent decide when and what to retrieve:

```python
system_prompt = """
You have access to a documentation KB.
When you need information, use this format:
QUERY_KB: <describe what you need>

Example:
"I need to understand rate-limiting strategies for APIs"
QUERY_KB: rate limiting patterns for high-traffic APIs

Then I will retrieve docs and feed them back.
"""

# Agent operates normally, occasionally emitting QUERY_KB requests
# Orchestrator intercepts QUERY_KB, retrieves, feeds results back
# Agent continues reasoning with new context
```

**Pros:**
- Flexible; agents adapt to unexpected situations
- Scalable; same approach works for many workflows
- Reactive; agents ask for help when they realize they need it

**Cons:**
- Unreliable; agents often don't query when they should (confidence bias)
- Costly; extra API calls for query decisions
- Timing uncertainty; agent might proceed without context before realizing it needed it
- Over-querying; agents sometimes query for things they can reason about themselves

**Real-world problem:**
```
Agent A thinks: "I can figure this out based on my general knowledge"
Agent A proceeds without querying
Agent A makes a suboptimal decision
Only at evaluation do you realize it needed context

Versus:

Agent B over-queries
Agent B wastes tokens
But Agent B gets the right answer

Most teams find they can't tell which is happening until too late.
```

**When to use:** Exploratory workflows. Agents need autonomy. You have budget for extra queries. Evaluation is strong enough to catch errors.

---

**Option 3: Pre-Retrieval (Brute Force)**

Retrieve all potentially relevant context upfront:

```python
task = "Design a payment system"

# Retrieve everything that might be relevant
all_relevant_docs = retrieve_from_kb([
    "payment*",        # All payment-related docs
    "compliance*",     # All compliance docs
    "error-handling*", # All error handling docs
    "security*"        # All security docs
])

# Dump into context
context = f"Reference Documentation:\n{format_docs(all_relevant_docs)}"

# Agent works with full context
result = agent.work_on(task, context=context)
```

**Pros:**
- Simple; no coordination logic
- No timing issues; all info available upfront
- No risk of missing context; agent has everything

**Cons:**
- Token explosion; you lose efficiency gains of retrieval
- Noisy context; lots of irrelevant docs distract the agent
- No scalability; this breaks with large knowledge bases

**When to use:** Small knowledge bases. Agents are token-constrained anyway. Simplicity matters more than efficiency.

---

### How to Evaluate If It's Working

You don't know until you measure:

**1. Query quality** — Sample 20 agent queries and manually rate: was the query well-formed and relevant?
```
Good query: "What are the transaction rollback strategies for distributed payments?"
Bad query: "Tell me about databases"
```

**2. Coverage** — Trace failures back to missing context. Did the agent miss relevant docs?
```
Agent designed payment system without checking compliance requirements.
Was there a compliance doc the agent should have queried for?
If yes, routing failed.
```

**3. Latency** — Measure wall-clock time for task completion. Did retrieval add significant overhead?
```
Task with explicit routing: 2.3 seconds
Task with LLM-driven routing: 3.8 seconds (retrieval overhead)
```

**4. Token efficiency** — Compare token usage across approaches.
```
Pre-retrieval: 45K tokens (all docs upfront)
Just-in-time: 28K tokens (selective retrieval)
But just-in-time had 3 query misfires (agent asked for wrong things)
```

---

### Real-World Failure Modes

**Hallucinated queries:**
```
Agent: "QUERY_KB: how to implement JWT with RSA-4096 keys"
KB: No docs on RSA-4096 specifically (only RSA-2048)
Agent: Proceeds without results, hallucinates implementation
Result: Security vulnerability
```

**Redundant retrieval:**
```
Agent A queries: "rate limiting patterns"
Agent B (same task) queries: "rate limiting patterns"
Same docs retrieved twice; wasted tokens
```

**Over-retrieval:**
```
Agent queries: "API design"
KB returns: 47 docs
Agent has to filter through signal/noise
Likely missed relevant doc in the haystack
```

**Stale context:**
```
Agent retrieves docs at 10:00 AM
Docs are updated at 10:15 AM
Agent proceeds with stale info at 10:20 AM
```

---

### Where the Industry Is

**As of 2026:**

1. **Most teams default to pre-retrieval** (Option 3) — It's simple and works, even if inefficient.

2. **LLM-driven routing** (Option 2) is being researched but reliability is still unclear. Early results suggest agents under-query (~40% miss context they should have retrieved).

3. **Explicit routing** (Option 1) is used by teams with high stakes and engineering resources (financial systems, healthcare).

4. **Active research areas:**
   - **Query prediction models** — Train classifiers to predict "does this agent need context on X?" But this requires labeled training data.
   - **Adaptive retrieval** — Retrospectively retrieve context if agent makes mistakes, learn for next time.
   - **Confidence-based retrieval** — Retrieve context when agent confidence is low. Problem: agent confidence is often uncalibrated.
   - **Hierarchical routing** — Multi-level filtering (category → subcategory → docs) to reduce search space.

---

### Recommendation for Multi-Agent Systems

**Start with explicit routing.** Build the orchestration manually for your specific workflows. You'll learn what context matters. Once you have patterns, you can generalize.

**Then consider LLM-driven routing** only if:
- Your workflows are too diverse for manual orchestration
- You have strong evaluation to catch retrieval misses
- Token budget is high enough to absorb over-querying

**Avoid pre-retrieval** unless your knowledge base is small or context budget is already huge.

---

★ **Insight ─────────────────────────────────────**
The multi-agent context problem is fundamentally a **prediction under uncertainty** problem. You're asking agents to predict what they'll need before they've fully reasoned through the problem. This is hard the same way predicting which test case will catch a bug is hard — you don't know until you need it. This is why the most reliable systems today either (a) have humans make routing decisions, or (b) dump everything and accept inefficiency. Neither is satisfying. This is a frontier problem where better solutions are emerging but no silver bullet exists yet. Acknowledging this in conversations with companies signals you understand the actual constraints of production agent systems, not the idealized version in papers.
`─────────────────────────────────────────────────`

---

---

## 16. Claude Code Agent Teams

> **Source:** Anthropic Claude Code documentation (April 2026). Experimental feature.
> **Full reference:** See `agent-teams.md` in this folder.

Most multi-agent architectures — including the patterns in Sections 7–13 of this doc — assume a hub-and-spoke communication model: one orchestrator has full context, workers complete delegated tasks and report results. The orchestrator holds the intelligence; workers are execution engines.

Claude Code Agent Teams inverts this assumption. Rather than spawning disposable workers that report back, it coordinates *peer sessions*: each teammate is a full Claude Code instance with its own context window, its own conversation history, and direct messaging access to all other teammates. The team lead sets direction and synthesizes findings, but it doesn't mediate every communication. Teammates talk to each other.

This matters because the hub-and-spoke model creates a specific failure pattern: the orchestrator's context window becomes a bottleneck. Everything passes through one agent's reasoning, which means anchoring is endemic — once the orchestrator forms a hypothesis, subsequent information gets filtered through it. In an agent team, multiple agents explore in parallel with genuinely independent contexts, then compare findings. Contradictions surface because different agents reached different conclusions from the same evidence.

### The Core Infrastructure

Agent teams run on three coordination primitives:

**Shared task list** (`~/.claude/tasks/{team-name}/`) — Tasks have three states (pending → in progress → completed) and can depend on each other. File locking prevents race conditions when multiple teammates try to claim the same task simultaneously. The task list is the coordination backbone; agents don't need to track what others are doing — they just look at what's available and claim it.

**Mailbox (push-based messaging)** — Messages deliver automatically without polling. A teammate notifies the lead when it goes idle. Any teammate can message any other by name. Broadcast reaches all teammates simultaneously (expensive — scales token cost with team size).

**Subagent definitions as blueprints** — Existing subagent definitions (tools allowlist, model, system prompt instructions) can be reused as teammate types. Define a role once; deploy it as either a disposable subagent or a peer teammate depending on the coordination pattern needed.

### When Teams Solve a Different Problem than Subagents

The decision is structural, not just about parallelism:

| | Subagents | Agent Teams |
|:--|:--|:--|
| **Communication** | Results return to lead only | Teammates message each other directly |
| **Context** | Isolated; results summarized | Isolated; findings communicated explicitly |
| **Best for** | Parallel work where only result matters | Parallel work where peer discussion improves outcome |
| **Token cost** | Lower | Higher (~7x in plan mode; see `agent-teams.md`) |

Use subagents when you need execution in parallel. Use agent teams when you need *reasoning* in parallel — when the most valuable output is what happens when multiple independent conclusions meet.

### Connection to Section 15: The Shared Context Problem

Section 15 describes query routing under uncertainty as "a frontier problem — not fully solved." Agent Teams doesn't resolve the retrieval problem (each teammate still has isolated context and doesn't automatically know what other teammates know). What it provides is a communication layer so agents can push relevant findings to each other deliberately, rather than trying to retrieve context they might not know to ask for.

The partial solution: a `TeammateIdle` hook can force a teammate to broadcast findings before going idle. A `TaskCompleted` hook can require a summary artifact be written to a shared file before marking work done. These patterns approximate shared context through explicit communication discipline.

### Quality Gates via Hooks

Three hook events are specific to Agent Teams:

- **`TeammateIdle`** — fires before a teammate stops. Exit code 2 keeps the teammate working.
- **`TaskCreated`** — fires before a task is created. Exit code 2 blocks creation.
- **`TaskCompleted`** — fires before a task is marked done. Exit code 2 prevents completion.

Together, these let you enforce a programmable definition of "done" at the task level — before code reaches review or CI.

### Best Use Cases

The strongest uses are tasks with **natural decomposition boundaries** where parallel work is genuinely independent, but where **cross-pollination of findings** improves the final result:

- **Parallel research and synthesis** — multiple investigators on different angles, actively challenging each other's findings
- **Multi-layer technical work** — frontend/backend/database/tests each owned by a different teammate, coupling points well-defined
- **Debugging with competing hypotheses** — each teammate tests a different theory, actively trying to disprove the others
- **Multi-domain analysis** — technical, legal, financial, UX perspectives applied simultaneously
- **Security audits** — separate reviewers for different attack surfaces (injection, authentication, authorization, data exposure)

### Key Limitations to Architect Around

- No session resumption for in-process teammates (`/resume`/`/rewind` don't restore them)
- Task status can lag — dependent tasks may appear blocked even when work is complete
- One team per session; no nested teams; lead is fixed for team lifetime
- Split-pane display requires tmux or iTerm2 (not VS Code terminal, Windows Terminal, Ghostty)
- Permissions set at spawn time from the lead's permission mode

**For the full reference** — architecture, setup, display modes, hook implementations, token cost controls, troubleshooting — see `agent-teams.md` in this folder.

**For deployment patterns** — broad use cases, operational workflows, quality gate configurations — see the multi-agent-orchestration playbook.

---

## References (Section 15)

- **Reliability limits of multi-agent planning:** Ao, Gao, Simchi-Levi, "On the Reliability Limits of LLM-Based Multi-Agent Planning" (arXiv 2603.26993, 2026) — Establishes decision-theoretic bounds on delegation: delegated agents dominated by centralized decision-maker unless they access new external information. Information loss in communication measured via posterior divergence.
- **In-context learning limits:** Lim et al., "In-Context Learning Unlocked for Transformers" (2024) — Shows that more context doesn't always improve performance; threshold effects exist.
- **RAG pitfalls:** Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (FAIR, 2020) — Original RAG paper; identifies relevance matching challenges.
- **Multi-agent coordination:** Mirkovic & Virani, "Multi-Agent Reinforcement Learning" (2024) — Surveys coordination problems; context sharing is discussed but not fully solved.
- **Query formulation in IR:** Navigli et al., "Word Sense Disambiguation: A Unified Evaluation Framework and Empirical Comparison" (JMLR, 2015) — Foundational work on how query formulation affects retrieval; applies to agent queries.
- **Hallucination in RAG:** Bang et al., "A Multitask, Multilingual, Multimodal Evaluation of ChatGPT on Reasoning, Hallucination, and Interactivity" (ICLR, 2024) — Agents over-confident in hallucinated information when retrieval fails silently.
