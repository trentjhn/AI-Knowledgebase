# Context Engineering

**Sources:** 12-Factor Agents (Factor 3), rlancemartin.github.io, simple.ai, LangChain Blog, dbreunig.com, LlamaIndex Blog *(2025)*

---

## Table of Contents

1. [Start Here: What Is a Context Window?](#start-here-what-is-a-context-window)
2. [From Prompt Engineering to Context Engineering](#from-prompt-engineering-to-context-engineering)
3. [Everything That Goes Into Context](#everything-that-goes-into-context)
4. [The Four Core Strategies](#the-four-core-strategies)
5. [How Contexts Fail — And Why It Matters](#how-contexts-fail--and-why-it-matters)
6. [Own Your Context Window](#own-your-context-window)
7. [Practical Principles](#practical-principles)
8. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
9. [Tools & Frameworks](#tools--frameworks)

---

## Start Here: What Is a Context Window?

Before anything else, you need to understand what a **context window** is — because everything in context engineering revolves around it.

Imagine you're hiring a consultant to help you with a complex project. Before they start, you give them a briefing packet: background documents, your company's history, the current problem, past attempts that didn't work, and instructions for what you need them to do. That briefing packet is the **only thing they know about your situation** — they walk in knowing nothing else.

That's exactly how a large language model (LLM) works. An LLM has no persistent memory. Every time you interact with it, it starts from a blank slate. The **context window** is the briefing packet you hand it — it's every piece of text the model can "see" at one time. The model reads everything in that window, processes it, and generates a response. Then the window is discarded.

> **Context Window:** The entire body of text (measured in tokens — roughly 3/4 of a word each) that an LLM can read and reason over at one time. It typically ranges from a few thousand tokens to over one million tokens in modern models. The model can only work with what's in this window.

Context windows have grown dramatically — from ~4,000 tokens a few years ago to over 1,000,000 tokens today. But a bigger window doesn't automatically mean better results. It means more responsibility: you now have to decide what goes in that space, in what order, and in what format.

**The core constraint:** LLMs only know two things — what they learned during training, and what you put in the context window. That's it. They cannot look things up, they cannot remember yesterday's conversation, and they cannot infer information you forgot to include. Context is everything.

---

## From Prompt Engineering to Context Engineering

You've probably heard of **prompt engineering** — the practice of carefully crafting the exact wording of your questions and instructions to get better answers from an AI. "Be specific. Add examples. Tell it what format you want." This became a popular skill around 2022-2023.

Prompt engineering is still useful, but it's become the baseline — everyone does it now. The real competitive edge has shifted to something deeper: **context engineering**.

> **The key distinction:**
> - **Prompt engineering** asks: *How should I phrase this question?*
> - **Context engineering** asks: *What information does the model need access to, when does it need it, and how should it be organized?*

Here's an analogy that makes this concrete. Prompt engineering is like coaching someone on how to answer a test question well — "read carefully, show your work, check your answer." Context engineering is like deciding *what textbooks they've studied, which notes they have on their desk, and which reference materials are available to them during the test.* The coaching matters, but the materials are what truly determine success.

| | Prompt Engineering | Context Engineering |
|---|---|---|
| **Focus** | How you phrase the request | What information the model can access |
| **Scope** | One interaction at a time | The whole system over time |
| **Nature** | Static — you write it once | Dynamic — adapts as the task progresses |
| **Skills needed** | Writing, clarity | Information architecture, data systems |

**Why this matters in practice:** Cognition (the company behind the Devin AI coding agent) stated that context engineering is "effectively the #1 job of engineers building AI agents." Most agent failures — situations where an AI assistant does the wrong thing or produces poor output — trace back to inadequate context, not model limitations. The model isn't dumb; it just didn't have the right information.

---

## Everything That Goes Into Context

When most people think about context, they imagine the prompt they wrote — the text they typed in the chat box. But for any real AI application, especially agents that take actions and run autonomously, context is far more complex. It has **eight components**:

---

### 1. System Prompt / Instructions

This is the foundational layer — the permanent instructions that define how the model should behave. Think of it as the job description you give a new employee on their first day. It might say: "You are a customer service agent for a software company. Always be polite. Never discuss competitors. If you don't know something, say so."

System prompts don't change between conversations. They establish the model's identity, tone, capabilities, and constraints.

---

### 2. User Input

The actual request or task from the user — the question they asked, the file they uploaded, the task they described. This is the immediate trigger for the current response.

---

### 3. Short-Term Memory (Conversation History)

When you have a multi-turn conversation with an AI, it remembers what was said earlier in the same conversation because the entire conversation history gets passed back into the context window on each new turn. The model doesn't actually "remember" anything — the application sends the full conversation transcript every time, so the model can read what was already said.

This is why very long conversations can sometimes make AI assistants behave strangely — you're filling up the context window with the conversation history, leaving less room for other important information.

---

### 4. Long-Term Memory

This is memory that persists *across* conversations — information saved from past sessions that gets retrieved and injected into the current context when relevant. You've seen this in tools like ChatGPT Memory ("Remember that I prefer Python"), or in coding tools like Cursor that load your project conventions.

Long-term memory doesn't happen automatically — it requires explicit systems to store, retrieve, and inject that information.

---

### 5. Retrieved Knowledge (RAG)

**RAG** stands for **Retrieval-Augmented Generation**. It's a technique where, instead of trying to make the model know everything, you retrieve relevant documents or data at the moment they're needed and inject them into the context window.

Example: A customer support AI doesn't have your entire product documentation memorized. Instead, when a user asks a question, the system searches the documentation for relevant sections and drops them into the context. The model then answers based on those retrieved passages — "just-in-time" knowledge.

This is how AI systems can answer questions about documents, databases, or knowledge bases they were never trained on.

#### The Scale-Dependency Problem

A critical insight from recent research: **retrieval effectiveness depends heavily on your model scale and task**. The common assumption — "bigger models always benefit more from RAG" — is misleading.

Empirical finding from OLMo-2 scaling studies (30M to 3B parameters across 100B pretraining tokens): The marginal utility of retrieval is *non-linear*. A small model (30M) may see 15% accuracy gains from retrieval, while a larger model (1B) sees 8% gains from the same retrieval setup on the same task. Meanwhile, on certain reasoning tasks, both see consistent improvement, but the saturation point (where adding more pretraining data beats adding retrieval) varies by 3-5x across task types.

**Practical implications for practitioners:**

1. **Don't assume RAG helps equally across model scales.** Benchmark RAG vs. scale-only baselines for your specific model size and task domain.

2. **Map your saturation point.** At what ratio of model parameters to pretraining data does adding retrieval become more cost-effective than adding more training tokens? This varies:
   - Reasoning tasks: saturation later (retrieval stays valuable at higher data budgets)
   - QA tasks: saturation earlier (parametric knowledge dominates sooner)
   - Scientific tasks: intermediate

3. **Use a three-dimensional scaling framework** — model size × pretraining budget × retrieval store size — to estimate optimal allocation. Don't treat pretraining and retrieval as independent decisions.

4. **Task-specific optimization matters.** A configuration optimized for open-domain QA may be suboptimal for reasoning-heavy tasks with the same model. Profile your actual workload.

The core principle: **Scale decisions are architecture decisions.** Before committing to a retrieval pipeline, understand whether your model size and task type will actually benefit from it relative to the cost.

---

### 6. Tool Definitions

When an AI agent has access to tools (web search, code execution, file reading, APIs), the model needs to know *what tools are available* and *how to use them*. These descriptions live in the context window. The model reads them, decides which tool is appropriate for the current task, and calls it.

An important and often overlooked point: if you give the model 50 tool descriptions, it has to wade through all 50 every time it makes a decision. Too many tool options in context causes confusion and errors — more on this in the failure modes section.

---

### 7. Tool Responses

When a tool gets called, its output gets added to the context window. If the model searched the web, the search results go in. If it ran code, the output goes in. The model then reads these results and decides what to do next.

In a long agentic workflow (where the model is taking many sequential actions), tool responses accumulate and can fill the context window quickly.

---

### 8. Structured Outputs / Global State

For complex multi-step tasks, there's often a shared "state" that tracks what's been decided and accomplished so far — a running scratchpad that different parts of the workflow can read from and write to. This structured state prevents the model from losing track of where it is in a complex process.

---

> **The big picture:** At any given moment in an AI agent's operation, the model's context window contains some combination of all eight of these components. Context engineering is the discipline of deciding *which* components appear, *when*, and *how they're organized* — because that directly determines the quality of the model's output.

---

## The Four Core Strategies

Once you understand what goes into context, the question becomes: *how do you manage it?* There are four fundamental strategies for context management.

---

### Strategy 1: Write — Save Information Outside the Window

The context window is finite and temporary. Information that isn't saved externally will be lost the moment the context window is cleared. The **Write** strategy means proactively saving important information to external storage so it can be retrieved later.

**Scratchpads during execution:** Long-running agents often write notes to themselves as they work. Anthropic's multi-agent research assistant, for example, saves its plan to an external file when the context window approaches 200,000 tokens — if it didn't, the plan would be truncated and lost. This is like a surgeon making notes during a long operation so they don't lose track of what they've done.

**Long-term memories across sessions:** There are two main approaches to building memories that persist between sessions:
- **Reflection** (from the Reflexion research framework): After completing a task, the agent reflects on what worked and what didn't, and saves those lessons for future use. Like a consultant writing a debrief after every project.
- **Periodic synthesis** (from Generative Agents research): Periodically compress recent memories into higher-level abstractions. Instead of saving every individual event, synthesize them into patterns and insights.

You see the Write strategy in production tools like ChatGPT memory, Cursor's project rules, and Windsurf's workspace memory — all of them persist information externally and inject it back into future contexts.

---

### Strategy 2: Select — Pull Only What's Needed

Having information available doesn't mean you should put all of it in the context window at once. The **Select** strategy means retrieving only the specific information relevant to the current task.

Think of it like a well-organized office. You don't spread every file you've ever created across your desk before you start working. You pull the specific files you need for today's task, work with them, and put them away.

**Types of information you might select:**
- **Episodic memories:** Examples of how similar tasks were handled before (for few-shot learning)
- **Procedural knowledge:** Step-by-step instructions for how to do something
- **Semantic facts:** Specific information relevant to the current task

**How selection works in practice:**

| Method | When to Use | How It Works |
|---|---|---|
| Always-included files | Small docs universally relevant | Load them every time (e.g., CLAUDE.md project rules) |
| Embedding-based retrieval | Large knowledge bases | Convert content to vector embeddings; find closest match to current query |
| Knowledge graphs | Structured relational data | Traverse entity relationships for multi-hop queries that embedding similarity can't answer |
| Temporal retrieval | Time-sensitive corpora | Date-weighted scoring + version-aware filtering so "current" means most recent, not highest embedding similarity |

> **The 2025 retrieval meta:** Semantic embedding-only retrieval is now considered inadequate for production RAG. The competitive baseline is **4-channel parallel retrieval** — BM25 keyword + semantic vector + knowledge graph traversal + temporal reasoning, fused via Reciprocal Rank Fusion (RRF). Each channel solves a fundamentally different class of query failure that the others can't compensate for. Full architecture and implementation in `future-reference/playbooks/building-rag-pipelines.md` → "The 4-Channel Parallel Retrieval Architecture."

**A counterintuitive insight on tool selection:** You can apply the same retrieval approach to *tool descriptions*, not just data. RAG-MCP research (arXiv 2505.03275) found that retrieving only the most relevant tool descriptions improved tool call accuracy **3×** over always loading all tools (43.1% vs. 13.6% baseline in large-toolset conditions) while cutting prompt tokens by over 50%. Note: the 13.6% baseline reflects a stressed scenario with many tools loaded simultaneously — production gains will vary, but the directional finding is robust. The model gets confused when it has to choose among dozens of tools; giving it only the relevant subset dramatically improves selection accuracy.

---

### Strategy 3: Compress — Trim the Fat

Even with good selection, context accumulates over a long task. Each tool call adds input and output. Each reasoning step adds text. Left unmanaged, this bloats the context window, increases cost, and — critically — degrades performance (the model gets distracted by old information).

The **Compress** strategy means actively reducing context size while preserving essential information.

**Summarization:** Instead of keeping the full transcript of a web search, post-process it down to the 3 most relevant sentences. Instead of keeping the full history of every tool call, summarize what was learned and what decisions were made.

**Trimming:** Hard-coded rules that remove older messages once a threshold is hit. Simpler than summarization, but loses information.

**The auto-compact example:** Claude Code (the coding assistant) automatically triggers "auto-compact" when the conversation reaches 95% of the context window's capacity. It summarizes the full interaction so far into a compact form and continues from there — the model essentially reads "here's what happened so far" in compressed form and picks up where it left off.

**The challenge:** Compression that's too aggressive loses critical decisions. A summarization system might compress "we decided not to use the database migration approach because it would break backwards compatibility" down to "we discussed database options" — losing the crucial reasoning. Getting compression right often requires specialized fine-tuned models for summarization.

---

### Strategy 4: Isolate — Split Across Separate Entities

Sometimes the best way to manage context is to keep separate concerns in separate context windows entirely.

**Multi-agent isolation:** Instead of one agent trying to do everything in one giant context window, spawn multiple agents each with a focused, contained context. Anthropic's research showed that their parallel multi-agent approach (several agents with isolated contexts working simultaneously) outperformed a single agent trying to handle everything in one context.

The trade-off: isolation is expensive. Multi-agent architectures use up to **15× more tokens** than a single-agent approach (Anthropic Engineering, 2025) because you're running multiple context windows in parallel. You pay more, but you get cleaner reasoning in each agent.

**Sandbox isolation:** For tasks involving large data objects — images, audio, video — keep those objects in a separate execution environment and only pass structured descriptions or results into the LLM's context. HuggingFace's CodeAgent does this: the LLM writes code to process an image, but the image itself never enters the LLM's context window.

**State isolation:** Complex workflows use schema-based state objects (similar to a Python `dataclass` or Pydantic model) that track the full workflow state, but only expose relevant fields to the LLM at each step.

---

## How Contexts Fail — And Why It Matters

Bigger context windows don't automatically mean better performance. More information in context can actually hurt an AI agent in predictable ways. There are four distinct failure modes — and knowing them helps you diagnose problems and design better systems.

---

### Failure Mode 1: Context Poisoning

**What it is:** A hallucination or error enters the context window and gets treated as fact in every subsequent step, compounding the mistake.

**Why it's dangerous:** LLMs don't flag their own previous mistakes. If the model made something up in step 3 of a 20-step workflow, that wrong information gets passed forward as ground truth and influences steps 4 through 20. The error doesn't just affect one step — it poisons the well.

**Real example:** A Gemini AI agent was playing Pokémon and hallucinated details about the game state (items in its inventory, where it had been). These hallucinated details were saved as the "goals section" of its ongoing context. From that point forward, the agent pursued impossible objectives based on its own fictional history — it was optimizing toward a state that didn't exist.

**How to protect against it:**
- Validate tool outputs before adding them to context — don't assume tools return accurate information
- Don't feed model-generated content directly back into context without checking it
- Build mechanisms to "quarantine" uncertain information rather than treating it as fact
- Monitor conversation history for early errors before they propagate forward

---

### Failure Mode 2: Context Distraction

**What it is:** An excessively large context causes the model to over-rely on past patterns instead of thinking freshly about the current situation.

**The intuition:** Imagine you're trying to solve a novel problem, but someone has plastered your office walls with records of every similar (but not identical) problem you've ever worked on. Instead of thinking creatively, you keep looking at the walls and saying "well last time we did X." The historical record distracts you from fresh thinking.

**Research evidence:**
- A study of a long-running AI agent found that as its context grew "significantly beyond 100,000 tokens," the agent "showed a tendency toward favoring repeating actions from its vast history rather than synthesizing novel plans"
- Databricks found that model accuracy starts to deteriorate around **32,000 tokens** for smaller models (like Llama 3.1 405B)
- Long context works well for *retrieval and summarization* (finding information that's already there) but degrades *multi-step reasoning* (synthesizing something new)

**How to protect against it:**
- Find your model's "distraction ceiling" empirically — test performance at different context sizes
- For multi-step reasoning tasks, keep context lean even if that means compressing more aggressively
- Reserve large context windows for tasks where you're mainly looking things up, not thinking through complex problems

---

### Failure Mode 3: Context Confusion

**What it is:** Irrelevant information in the context forces the model to process and weigh things that shouldn't matter, degrading response quality.

**The intuition:** The model doesn't know what to ignore. When you put something in the context, the model *has to* pay attention to it — it processes every token. This means irrelevant information actively competes with relevant information for the model's attention.

**Research evidence:** The Berkeley Function-Calling Leaderboard tested models across different numbers of available tools:
- Every model performed worse as the number of tool descriptions increased
- A Llama 3.1 8B model succeeded with 19 available tools but failed with all 46 tools in context
- The problem isn't that the model can't use the right tool — it's that too many wrong options confuse its decision

**How to protect against it:**
- Don't include all tools all the time — dynamically expose only the tools relevant to the current step
- Use RAG to select tool descriptions (not just data)
- Test with realistic tool counts before deploying — don't assume "more tools available = better"

---

### Failure Mode 4: Context Clash

**What it is:** Contradictory information across different parts of the context (or across different conversation turns) causes the model to make inconsistent decisions.

**How it happens:** Early in a conversation, the model makes assumptions and acts on them. Later, new information arrives that contradicts those early assumptions. The model now has two conflicting versions of reality in its context — and it tends to stick with the earlier one because it already built reasoning on top of it.

**Research evidence:** A Microsoft and Salesforce study tested "sharded prompts" — where critical information was spread across multiple conversation turns rather than given all at once. The result: a **39% average accuracy drop** across all models tested. OpenAI's o3 dropped from 98.1% to 64.1% accuracy on the same task. The root cause: "LLMs often make assumptions in early turns and prematurely attempt to generate final solutions, on which they overly rely."

**How to protect against it:**
- Provide complete, consistent information upfront rather than distributing it across turns
- Don't spread critical information across multiple messages if you can consolidate it
- When information changes, explicitly acknowledge and replace old information rather than just adding new information alongside it

---

### The Agent Vulnerability Problem

Agents are uniquely susceptible to all four failure modes *simultaneously*. In a single agentic session, an agent might:
- Gather information from multiple sources (risk: clash between sources)
- Make dozens of sequential tool calls (risk: context fills up → distraction)
- Have hallucinations in its early steps feed forward (risk: poisoning)
- Have a large library of tools available at all times (risk: confusion)

> **Core principle:** Prioritize context *quality* over context *quantity*. The right 10,000 tokens reliably outperform 100,000 unfocused tokens.

---

## Own Your Context Window

Most AI frameworks give you a default message format: `system`, `user`, `assistant`, `tool` — a structured conversation transcript. This works fine for simple applications. But for complex agents, you can and should take direct control of how your context is structured.

From the 12-Factor Agents framework (a set of principles for production-grade AI agents): context is the *programmable layer* of agent behavior. Treat it as an engineering artifact — design it deliberately, version it, and iterate on it.

### Why Custom Formats?

The default message-based format is generic. It's designed to be readable by humans and parseable by models — but it's not optimized for *your specific domain or workflow*.

Consider a deployment automation agent. At every step, it needs to know: who requested the deployment, what tags are available, what the deployment history looks like, and what succeeded or failed in the current attempt. That information could be scattered across 15 separate tool call messages in the default format — or it could be structured into a clean, readable XML block that the model can trace through at a glance.

**Custom context format options:**
- **XML tags** for semantic clarity — each piece of information is labeled with its meaning
- **YAML** for hierarchical data that has natural nesting
- **Custom serialization** for domain-specific data structures

**Example — default format vs. custom XML for a deployment workflow:**

Default format (lots of separate messages, hard to trace state):
```
[user]: deploy v2.3.1
[tool_call]: list_git_tags
[tool_result]: v2.3.1, v2.3.0, v2.2.9...
[tool_call]: deploy_backend
[tool_result]: {"status": "error", "message": "timeout"}
[user]: retry it
```

Custom XML format (explicit, structured, traceable):
```xml
<slack_message>
  From: @user | Channel: #deployments | Text: "deploy v2.3.1"
</slack_message>

<list_git_tags_result>
  tags: [v2.3.1 (2025-01-15), v2.3.0 (2025-01-10), v2.2.9 (2024-12-28)]
</list_git_tags_result>

<deploy_backend_attempt_1>
  version: "v2.3.1" | environment: "production" | result: TIMEOUT
</deploy_backend_attempt_1>

<human_feedback>
  instruction: "retry it"
</human_feedback>
```

The custom format makes the progression of state explicit. The model can read the history clearly, understand exactly what has been tried, and make a better decision about what to do next. Failed attempts are visible without being cluttered. The human instruction is clearly labeled as a human instruction.

### When to Use Custom Formats

Custom context formatting pays off when:
- You need maximum token efficiency (every token costs money and affects performance)
- You're running a complex multi-step workflow with state that needs to be tracked
- You want fine-grained control over what the model sees at each step
- You're iterating and want the flexibility to experiment with different structures

The core principle: don't accept your framework's default format as optimal. It's a starting point. The right format for your application is the one that makes your specific workflow's state clearest to the model.

---

## Practical Principles

### Ordering Matters

Where information appears in the context window affects how much "attention" the model pays to it. Research on transformer models (the architecture underlying LLMs) shows that:

- **Beginning:** Establishes the frame — good for system-level instructions, identity, and permanent constraints
- **Middle:** Working memory — good for task-specific background information and data
- **End:** Highest attention, most direct influence on the next output — put your specific instruction and desired format here

This is why system prompts go at the top and your specific question goes at the very end.

### Long-Term Memory Types

If you're building applications that need to remember across sessions, there are three distinct types of memory storage to consider:

| Memory Type | What It Stores | How It Works |
|---|---|---|
| **Vector memory** | Chat messages and documents | Converted to numeric embeddings; retrieves semantically similar content |
| **Fact extraction** | Discrete facts pulled from conversation | Parses "User's name is Sarah, prefers Python" into structured facts |
| **Static memory** | Fixed, always-relevant information | Loaded every time without any retrieval logic |

Most real applications need a combination of all three.

### Workflow Engineering

One of the most powerful context engineering techniques isn't about what you put in the context — it's about *breaking up the task* so each LLM call gets a focused, lean context.

Instead of one giant prompt asking the model to do everything at once, design a sequence of smaller LLM calls where each call has only the context it needs for its specific step. Then use deterministic code (not LLM calls) for the parts that don't require language understanding — validation, data transformation, routing.

**Benefits of explicit workflow design:**
- Each LLM call has a smaller, more focused context → better performance
- Deterministic logic handles mechanical steps → cheaper and more reliable
- Built-in validation at each step → catch errors early
- The workflow is debuggable — you can inspect what each step received and produced

---

## Anti-Patterns to Avoid

These are the most common mistakes people make with context management, along with why they cause problems and what to do instead:

| ❌ Anti-Pattern | 🔍 Why It's a Problem | ✅ Fix |
|---|---|---|
| **Dumping all available context** | Causes confusion and distraction — the model processes irrelevant tokens | Curate: include only what's needed for this specific step |
| **One giant LLM call for everything** | Monolithic context = no room for specific, focused reasoning | Break into a workflow with smaller, targeted calls |
| **Ignoring context window limits** | Performance degrades long before you hit the hard limit | Monitor token usage; compress proactively |
| **Assuming bigger context = smarter** | More context often causes distraction, not improvement | Test empirically; match context size to task type |
| **Static context in a dynamic workflow** | Information goes stale; the model reasons about outdated state | Rebuild context dynamically at each step |
| **Injecting unvalidated model output back into context** | Hallucinations get treated as facts and compound | Validate tool results before re-injecting |
| **Always showing all tools** | The model gets confused when 40+ options are available | Dynamically expose only the relevant tools per step |
| **Spreading critical info across many turns** | Creates context clash — early assumptions override later information | Consolidate related information; provide it all at once |

---

## Tools & Frameworks

The following tools are specifically designed to support context engineering:

**LangGraph** — A framework for building agentic workflows as explicit graphs. It gives you complete, fine-grained control over what information flows into each step of your workflow. Unlike higher-level frameworks that abstract this away, LangGraph lets you see and control exactly what's in the context at each node.

**LangSmith** — Observability for LangGraph and LangChain applications. It traces agent execution step by step, showing exactly what was in the context when each decision was made. Invaluable for debugging context-related failures.

**LlamaIndex** — A retrieval and data framework for AI applications. Provides infrastructure for RAG, long-term memory blocks (`VectorMemoryBlock`, `FactExtractionMemoryBlock`, `StaticMemoryBlock`), and a Workflows framework for multi-step agentic applications.

**LlamaParse** — Document processing tool for converting complex files (PDFs, spreadsheets, presentations) into clean, structured text for context injection.

**LlamaExtract** — Extracts specific structured data from complex documents. Rather than dumping a whole PDF into context, LlamaExtract pulls out only the relevant fields.

**CLAUDE.md / Cursor Rules** — The "always-included context" approach for coding assistants. A markdown file that gets injected into every context window for a given project, encoding the project's conventions, architecture, and patterns so the model doesn't have to rediscover them each time.

Effective CLAUDE.md design has a few non-obvious constraints worth knowing:

*Instruction budget.* Claude Code's system prompt already consumes roughly 50 instructions before your CLAUDE.md is even loaded. The practical ceiling before instruction overload degrades performance is around 150–200 total — leaving you 100–150 slots. Every instruction you add displaces attention from the others. This makes the **80% rule** the most important filter: only include instructions relevant to 80%+ of your sessions. Task-specific instructions belong in separate files that get loaded on demand, not in the always-on CLAUDE.md.

*Three-level hierarchy.* CLAUDE.md files load at three scopes: global (`~/.claude/CLAUDE.md`, applies to all projects), project root (`./CLAUDE.md`), and directory-specific (`./src/CLAUDE.md`, `./tests/CLAUDE.md`). Directory files only load when Claude accesses that part of the codebase — a natural form of progressive disclosure that keeps the active context lean. Use this to write conditional behavior: different conventions for `tests/` vs. `src/api/` without cluttering the root file.

*Context swapping.* For projects with very different operational modes (development vs. deployment vs. debugging), maintain separate CLAUDE.md variants and swap them in as needed. This is preferable to one bloated file with branching instructions for every possible situation.

*What not to include.* Code style rules enforced by linters (ESLint, Black, Ruff) don't belong in CLAUDE.md — use hooks and pre-commit automation to enforce those. Credentials and API keys never belong there. Anything inferrable directly from the codebase is better left out. CLAUDE.md should encode what the codebase can't tell Claude on its own.

---

## CLAUDE.md Loading Mechanisms in Practice

One of the most underrated aspects of context management is **how context actually gets loaded** when you're working with monorepos or complex project structures. This applies specifically to Claude Code, but the principles generalize to any agentic system with modular knowledge.

### The Ancestor/Descendant Model (Claude Code)

Claude Code loads CLAUDE.md files in a specific hierarchy:

**Ancestor Loading (Immediate):**
- Your root repository `/.claude/CLAUDE.md` always loads at startup
- Parent directory `CLAUDE.md` files load automatically
- This is "ancestor first" — constraints and rules from parents cascade down

**Descendant Loading (Lazy):**
- Subdirectory CLAUDE.md files only load when you access files in that directory
- Once loaded, they persist for the session
- This prevents context bloat in monorepos with 50+ subdirectories

**Sibling Isolation:**
- CLAUDE.md files in non-ancestor, non-descendant directories don't load
- Prevents cross-contamination in parallel development

### Why This Matters

In a monorepo with frontend, backend, and data services:

```
root/
├── .claude/CLAUDE.md                 # Loads immediately: core values, definitions
├── frontend/
│   └── .claude/CLAUDE.md             # Loads only when you touch frontend/*
├── backend/
│   └── .claude/CLAUDE.md             # Loads only when you touch backend/*
└── data-services/
    └── .claude/CLAUDE.md             # Loads only when you touch data-services/*
```

**Without lazy loading:** The agent would hold frontend + backend + data instructions in context simultaneously, even when working only on frontend. Wasted tokens and conflicting guidance.

**With lazy loading:** Only the relevant domain's CLAUDE.md loads. Context stays lean. The agent doesn't get confused by irrelevant constraints.

### Practical Design Pattern: <200 Lines Per File

The rule: **keep each CLAUDE.md under 200 lines** (60 lines in intensive domains like data science).

Why? Because:

1. **Determinism degrades with length** — instructions get ignored or reinterpreted at higher token counts (empirical: 80% adherence at 150 lines, 60% at 400 lines)
2. **Context bloat kills precision** — more instructions = lower fidelity to any single instruction
3. **Monorepo solution** — split domain-specific knowledge into separate files, load lazily

**Example structure for a complex project:**

```
root/.claude/CLAUDE.md (120 lines)
├── Core values, definitions, key decisions
├── Global constraints (security, data, compliance)

root/.claude/rules/safety.md (70 lines)
├── Never-execute rules (hard boundaries)

root/services/mining-ops/.claude/CLAUDE.md (150 lines)
├── Mine planning domain knowledge, operational constraints

root/services/plant-ops/.claude/CLAUDE.md (140 lines)
├── Process control domain knowledge, RL behavior guidelines
```

Each file stays under 200 lines. The agent loads only what's needed. Instructions stay crisp.

### The Diagnostic: Context vs. Instruction Quality

If an agentic system keeps failing at the same step, ask: **Is this a model failure or an environment failure?**

- **Model failure:** The model is given correct context but still reasons incorrectly (rare with modern models)
- **Environment failure:** The context is incomplete, contradictory, or poorly formatted (common)

Environment failures are permanent fixes:
- Undocumented setup steps → document them
- Missing type annotations → add them
- Vague success criteria → define metrics clearly
- Conflicting constraints → clarify or remove

Environment failures are 10x cheaper to fix than trying to prompt your way out of them.

---

## Key Takeaways

Context engineering is the practice of intentionally designing what an LLM can see, in what form, and at what moment. It's the primary lever for AI agent performance — more impactful than model selection for most real-world applications.

The core disciplines:

1. **Understand all 8 context components** — the context window is far more than just your prompt
2. **Apply the four strategies** — Write, Select, Compress, and Isolate based on the situation
3. **Design for the four failure modes** — poisoning, distraction, confusion, and clash each require different defenses
4. **Take ownership of your format** — custom serialization structures beat default message formats for complex workflows
5. **Build workflows, not prompts** — break complex tasks into steps, each with a focused, lean context
6. **Quality beats quantity** — the right 10,000 tokens consistently outperform 100,000 unfocused ones
---

## 10. Token Economics & Budget Management

**Adapted from [everything-claude-code](https://github.com/affaan-m/everything-claude-code)**

The context window is not unlimited. More importantly, **tokens have cost**. Context engineering must balance three competing demands: quality (enough information to succeed), speed (fast response), and cost (staying under budget).

### Token Budgeting by Layer

Every layer of context consumes tokens. Map your token allocation:

```
Model context window: 200,000 tokens (Opus)

Allocation:
├─ System prompt: 1,500 tokens (permanent)
├─ Agent instructions: 2,000 tokens (permanent)
├─ User request: 500 tokens (variable)
├─ Conversation history: 20,000 tokens (grows per turn)
├─ Retrieved knowledge (RAG): 50,000 tokens (pulled per query)
├─ Code context (codebase snippets): 40,000 tokens (task-specific)
├─ Reference docs: 20,000 tokens (static)
└─ Scratch space (for reasoning): 66,000 tokens (model working memory)
```

**Rule of thumb:** Reserve 30% for model reasoning. If your context fills >70% of window, compact before next request.

### Strategic vs. Automatic Compaction

**Automatic compaction** (happen at 95% context): Too late. Quality already degraded. Context gets corrupted during summarization.

**Strategic compaction** (at 50%): Proactive. Before quality suffers.

Decision tree:
```
Context usage > 50%?
├─ If YES and at phase boundary (research done, ready for implementation)
│  └─ Compact: Summarize session, save to file, start fresh
├─ If YES but mid-phase
│  └─ Don't compact yet; compress instead (summarize conversation history only)
└─ If NO: Continue
```

### MCP Context Budgeting

MCP (Model Context Protocol) servers expose tools. Each tool definition consumes tokens even when unused.

```
Naive: Load 20 MCPs at startup
├─ Cost: ~10,000 tokens just for tool definitions
├─ Result: 5% of 200k context window gone before task starts
└─ Quality: Poor (model distracted by irrelevant tools)

Smart: Load MCPs dynamically
├─ Startup: Load 3 core MCPs (~1,500 tokens)
├─ Task-specific: Load additional MCPs when task arrives
│  └─ "This task needs database access" → load DB MCP (500 tokens)
│  └─ "This task needs file ops" → load file MCP (300 tokens)
└─ Result: 2,300 tokens total (77% savings)
```

Best practice: Keep under 5-10 MCPs active at any time. Dynamic loading saves orders of magnitude in context overhead.

---

## 11. Iterative Retrieval for Multi-Agent Context

**Adapted from [everything-claude-code](https://github.com/affaan-m/everything-claude-code)**

When multiple agents work together (orchestrator → specialized sub-agents), the **sub-agent context problem** emerges: the sub-agent doesn't know what context it needs because it lacks the orchestrator's semantic understanding.

### The Problem

Orchestrator: "Find information on user retention factors"
Sub-agent: "What context do I need? I don't know if this is for B2B SaaS, mobile games, or social platforms."
Result: Sub-agent returns generic summary, orchestrator has to re-query.

### The Iterative Retrieval Pattern

Break context refinement into a loop:

```
Phase 1: DISPATCH
├─ Orchestrator sends query + broad objective to sub-agent
├─ Sub-agent: "Find user retention research"
└─ Cost: Initial request token budget

Phase 2: RETRIEVE & SUMMARIZE
├─ Sub-agent retrieves candidate materials
├─ Returns provisional summary (50% confidence)
└─ Cost: Retrieval + first summary pass

Phase 3: ORCHESTRATOR EVALUATES
├─ Ask: "Is this sufficient?"
├─ If YES → done
├─ If NO → identify gaps
└─ Cost: Zero (orchestrator evaluates existing content)

Phase 4: REFINE & LOOP
├─ If gaps found, ask targeted follow-ups
│  ├─ "You mentioned SaaS; what about mobile games?"
│  ├─ "That covers engagement; what about churn drivers?"
│  └─ "Focus on onboarding phase specifically"
├─ Sub-agent refetches, updates summary
└─ Loop max 3 cycles (prevents infinite loops)
```

### Max 3 Cycles Rule

Why stop at 3? Empirically:
- Cycle 1→2: 40% quality improvement (big jumps in understanding)
- Cycle 2→3: 15% quality improvement (diminishing returns)
- Cycle 3→4: 5% improvement (not worth the cost/delay)

### Cost Analysis

Three cycles vs. all-at-once *(illustrative metrics from everything-claude-code multi-agent context pattern):*
```
Naive (all context at once):
├─ Subagent sees 50K tokens of unfiltered information
├─ Returns 25K token summary
├─ Cost: 75K tokens for maybe 40% relevance

Iterative (3 cycles):
├─ Cycle 1: 5K tokens → 2K summary (80% relevance)
├─ Cycle 2: 8K tokens → 3K refined summary (92% relevance)
├─ Cycle 3: 10K tokens → 4K final summary (95% relevance)
├─ Total: 23K + 9K output = 32K tokens (57% savings)
└─ Quality: 95% vs. 40% (2.4× better)
```

The loop pays for itself through higher quality and lower total context usage. Real-world improvements depend on context complexity and orchestrator quality.

---
