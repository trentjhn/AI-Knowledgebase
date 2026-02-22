# Playbook: Building AI Agents

> **Use this when:** You're building a system where an AI needs to take sequences of actions, use external tools, make decisions across multiple steps, or operate with some degree of autonomy — rather than just answering a single question.

---

## What an AI Agent Actually Is

Before getting into techniques, it's worth being precise about what distinguishes an agent from a regular LLM call. A standard LLM interaction is stateless and single-turn: you send a prompt, you get a response, done. An agent is different in three ways:

1. **It takes actions, not just text.** Agents call tools — search engines, databases, APIs, code executors — and incorporate the results into their next decision.
2. **It operates across multiple steps.** The output of one step becomes the input for the next. The agent is navigating a process, not answering a question.
3. **It has some degree of goal-directedness.** Given a high-level objective, it figures out the intermediate steps required rather than waiting to be told each one.

This power comes with new failure modes that don't exist in simple prompting. Agents can get stuck in loops, take wrong turns they can't recover from, drift from the original goal, or fail silently in ways that are hard to detect. The techniques below address these specifically.

---

## Core Technique Stack

These are the building blocks you'll draw on for almost every agent build. Think of this as your default toolkit — you might not use all of them, but you should consciously decide which ones to include.

### 1. ReAct (Reason + Act) — The Foundation

ReAct is the fundamental pattern for tool-using agents. At each step, the agent alternates between *thinking* (reasoning about what to do next) and *acting* (calling a tool). The tool's output becomes new context, and the cycle repeats.

The key insight: forcing the model to reason *before* acting dramatically reduces errors. An agent that jumps straight to action without reasoning tends to pick the wrong tool, use the wrong parameters, or miss a simpler path. The "thought" step is not overhead — it's error prevention.

**The loop:**
```
Thought: [What do I need to do next? What information am I missing?]
Action: [tool_name with parameters]
Observation: [result from the tool]
Thought: [What does this tell me? What's next?]
...
Final Answer: [synthesized result]
```

See `prompt-engineering/prompt-engineering.md` for the full ReAct breakdown.

### 2. Chain of Thought for Planning

Before an agent starts acting, it should plan. A CoT planning step — "Think through the steps needed to accomplish this goal before taking any action" — forces the agent to map out the path before walking it. This catches logical errors early, before the agent has already taken five wrong steps.

**How to implement:** Add an explicit planning phase to your system prompt. Before any tool calls, require the agent to output a numbered list of steps it intends to take. This plan becomes the anchor — you can reference it to detect when the agent has drifted.

### 3. Tool Design and Restriction

The quality of an agent is largely determined by the quality of its tools. Poorly designed tools are the most common source of agent failure. Key principles:

- **Each tool does exactly one thing.** A tool that "searches for information and summarizes it" creates ambiguity. Make them `search()` and `summarize()` separately.
- **Return rich, structured information.** A tool that returns raw text is harder to reason about than one that returns structured data. The cleaner the output, the better the agent's next reasoning step.
- **Don't give the agent tools it doesn't need.** Every tool is an opportunity for the agent to go off-track. Only expose what's required for the task.
- **Validate inputs before execution.** Agents sometimes hallucinate tool parameters. Build validation into your tool layer, not into the prompt.

See `agentic-engineering/agentic-engineering.md` for detailed tool design principles.

### 4. Context Management Across Steps

As an agent works through multiple steps, its context window fills up. This causes a subtle failure: the original instructions — the goal, the constraints, the format requirements — get pushed far back in context and start to fade. The agent begins to drift.

Strategies to manage this:
- **Keep the goal visible.** Re-state the original objective at the end of each reasoning step, not just at the beginning.
- **Summarize as you go.** Rather than accumulating all tool outputs verbatim, have the agent summarize what it's learned at each step. This compresses context while preserving meaning.
- **Use a scratchpad.** Give the agent a persistent working memory structure (a structured dict or running summary) that it explicitly maintains and updates rather than relying on the full conversation history.

See `context-engineering/context-engineering.md` for the full context strategy framework.

### 5. Human-in-the-Loop (HITL) Checkpoints

Full autonomy is rarely the right default. For most real-world agents, you want checkpoints where the system pauses and asks for human confirmation before taking high-stakes, irreversible, or expensive actions.

Design your agent with explicit decision points:
- **Classify actions by reversibility.** Reading data is safe; deleting it is not. Writing a draft is safe; sending an email is not. The agent should treat these differently.
- **Surface uncertainty explicitly.** When the agent's confidence is low or the path forward is ambiguous, it should ask rather than guess. "I'm not sure whether you want X or Y — which should I do?" is better than a confident wrong choice.
- **Set clear stop conditions.** Define what constitutes task completion. Agents without clear stopping criteria sometimes keep taking actions after they've already solved the problem.

---

## Recommended Workflow

When starting a new agent build, work through these stages in order:

**Stage 1: Define the task boundary clearly**
Write out in plain English: what does success look like? What information will the agent start with? What tools will it have? What are the things it should never do? This becomes the foundation of your system prompt.

**Stage 2: Design your tools before your prompts**
The tools determine what the agent can actually do. Get them working correctly in isolation first — test each tool independently before the agent ever touches it.

**Stage 3: Build the simplest possible version first**
Start with a single-step agent: one tool, one decision, one output. Confirm it works correctly. Add complexity incrementally. Adding multiple tools, multi-step reasoning, and memory management all at once makes failures impossible to diagnose.

**Stage 4: Add the planning step**
Once the basic tool-use works, add an explicit planning phase before action. Observe whether the plans are sensible. Bad plans at this stage reveal gaps in the system prompt or tool descriptions.

**Stage 5: Add context management**
Once multi-step workflows are working, identify where context starts to degrade. Add summarization, scratchpad patterns, or explicit goal reinforcement where needed.

**Stage 6: Add guardrails and HITL**
Identify the highest-risk actions in your workflow. Add human confirmation requirements, validation layers, and fallback behaviors for those specifically.

---

## Common Pitfalls

**The agent loops.** It keeps calling the same tool with the same parameters because it's not making progress but also not recognizing it's stuck. Fix: add a step counter and explicit loop detection. "If I have called the same tool with the same parameters more than twice, I should stop and report that I'm stuck."

**The agent drifts from the goal.** It gets absorbed in a sub-task and forgets the original objective. Fix: anchor the original goal in every reasoning step. Keep it visible at the bottom of the context, not just at the top.

**The agent hallucinates tool outputs.** Instead of actually calling a tool, it generates what the output "would probably be." Fix: enforce strict separation between reasoning and tool calls in your prompt format. Never let the model generate observations — those must come from actual tool execution.

**The agent is over-confident.** It proceeds past a point of genuine uncertainty rather than asking. Fix: explicitly prompt for uncertainty expression: "If you're not sure which path to take, say so and describe what information would help you decide."

**Context window overflow.** After many steps, the agent loses track of earlier instructions. Fix: implement rolling summarization and keep the goal statement pinned at a consistent location in context.

---

## Scaling Up

As your agent handles more complex tasks, these patterns become increasingly important:

**Multi-agent architecture.** For complex tasks, break work into specialized sub-agents (a planner, a researcher, a writer, a reviewer) rather than one general agent doing everything. Each agent is simpler, more reliable, and easier to debug. See `agentic-engineering/agentic-engineering.md` for the Orchestrator, Expert Swarm, and Multi-Agent Collaboration patterns.

**Persistent memory.** Add external memory (a database, a vector store) so the agent can recall information from previous sessions and past tasks. This is what enables agents that get better over time rather than starting fresh every run.

**Evaluation pipelines.** Once an agent is in production, set up automated tests that run it on known tasks and check the outcomes. Model updates and prompt drift can quietly break agents that were working fine.

**Cost monitoring.** Multi-step agents can make many LLM calls per task. Track cost per task from the start, and set budget limits that trigger early termination if something goes wrong.

---

*Draw from: `agentic-engineering/agentic-engineering.md` (architecture patterns, tool design, orchestration) · `context-engineering/context-engineering.md` (context strategies, window management) · `prompt-engineering/prompt-engineering.md` (ReAct, CoT, system prompting)*
