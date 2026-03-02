# Agentic Engineering

> Distilled from *Agentic Engineering* by Jaymin West
> Source: https://github.com/jayminwest/agentic-engineering-book
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
| Complex analysis requiring multiple expert perspectives | Orchestrator |
| Information-gathering with unknown scope | ReAct |
| High-stakes irreversible operations | Human-in-the-Loop |
| Multiple independent tasks in one domain at scale | Expert Swarm |
| Complex design decisions with real tradeoffs | Multi-Agent Collaboration |
| Long-running projects requiring knowledge persistence across sessions | Persistent Agent Memory |

Patterns can be combined: an Orchestrator can coordinate parallel Plan-Build-Review workers. Human-in-the-Loop gates fit naturally at phase transitions in any pattern.

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

Hooks are event handlers that fire at critical moments in agent execution. They enable real-time visibility and enforcement rather than after-the-fact analysis.

| Hook | Primary Use |
|---|---|
| `PreToolUse` | Validate commands before execution — catch dangerous operations before they happen |
| `PostToolUse` | Log actions, update metrics, track per-tool token costs |
| `SubagentStop` | Record subagent outputs, promote artifacts to persistent storage |
| `ErrorEscalation` | Notify human overseers when agents fail or behave unexpectedly |

Hooks run synchronously and block agent execution — use them for real enforcement, not just logging. But keep them fast (see time budgets below) or they become a bottleneck.

| Hook | Time Budget | If Exceeded |
|---|---|---|
| SessionStart | 3-5 seconds | Proceed with defaults |
| PreEdit | 10-15 seconds | Skip optional context injection |
| PreToolUse | 5-10 seconds | Log warning, proceed anyway |

**Pre-edit dependency injection:** Before an agent edits a file, inject dynamic context — current imports, type definitions, available exports from the TypeScript language server. This prevents the most common implementation errors: missing imports, type mismatches, using functions that don't exist.

**Philosophy:** Permissive tools + strict prompts + hook enforcement. The agent has broad access; the prompt guides what it should do; hooks enforce the hard limits that must never be violated.

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
