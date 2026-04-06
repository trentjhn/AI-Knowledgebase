# Playbook: Building AI Agents

> **Use this when:** You're building a system where an AI needs to take sequences of actions, use external tools, make decisions across multiple steps, or operate with some degree of autonomy — rather than just answering a single question.

---

## Decision Tree: What's Your Primary Pattern?

**Use this flowchart to find the right PRIMARY playbook. After building your primary pattern, you can add optional capabilities (retrieval, actions, etc.) — see "Add Optional Capabilities" section below.**

```
What's the core interaction pattern?
│
├─ Real-time conversation with users
│  └─ PRIMARY PLAYBOOK: building-chatbots.md
│     (User interruption, multi-turn state, response streaming)
│
├─ Process/search through documents I have
│  └─ PRIMARY PLAYBOOK: building-rag-pipelines.md
│     (Retrieval quality, ranking, chunking, indexing)
│
├─ Execute multi-step tasks autonomously
│  └─ PRIMARY PLAYBOOK: building-ai-agents.md (THIS ONE)
│     (ReAct loops, planning, tool orchestration, error recovery)
│
└─ Single LLM call (classify, generate, summarize)
   └─ PRIMARY PLAYBOOK: writing-production-prompts.md
      (Prompt engineering, output format, reliability)
```

**Quick Reference: Which Playbook?**

| Your Task | Primary Playbook | File |
|---|---|---|
| "Customer support chatbot that answers questions" | Chatbot | building-chatbots.md |
| "Search my internal documents for answers" | RAG | building-rag-pipelines.md |
| "Autonomous research agent that gathers data and writes reports" | **Agent** | **building-ai-agents.md** |
| "Monitor data, detect anomalies, trigger alerts" | **Agent** | **building-ai-agents.md** |
| "Extract info from PDFs, structure it, save to DB" | **Agent** | **building-ai-agents.md** |
| "Classify emails or categorize content" | Prompt | writing-production-prompts.md |

---

## Add Optional Capabilities

You've picked the agent playbook. Before starting, check if you need any of these optional capabilities. If yes, see the linked playbook for that specific section, then return here.

**Does your agent need to retrieve documents?**
- Example: Agent searches internal docs to answer questions before planning actions
- See: [building-rag-pipelines.md](building-rag-pipelines.md) Phase 1–2 (retrieval setup + ranking)
- Then: Return here for Phase 2.3 (Tool Design) to integrate retrieval as a tool

**Does your agent need to handle real-time user interruption?**
- Example: Agent is running a multi-step task, user can pause/modify mid-way
- See: [building-chatbots.md](building-chatbots.md) section "Multi-Turn State Management"
- Then: Return here for Phase 4 (Adding Human-in-the-Loop)

**Is this agent running for weeks/months with many decisions?**
- Example: Business operations agent, research agent with long-running tasks
- See: [agentic-engineering.md](../LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md) lines 1806–1829 (Long-Horizon Planning)
- Pattern: Add scratchpad for decision persistence

**Starting with just basic agent? → Skip this section, go to Phase 1 below.**

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

## Phase 1: Spec, Tools & Basic Agent

**Goal:** Define what your agent does, build & test its tools independently, write a working Level 1 prompt, and validate on 3 scenarios.

**Outcome:** A working agent on a simple task, git repo initialized, first phase complete.

---

### Step 1.1: Write Your Agent Specification

**What you're doing:** Define the agent's purpose, scope, constraints, and success criteria before writing any code.

**KB Reference:** [Seven Properties of Executable Spec](../LEARNING/PRODUCTION/specification-clarity/specification-clarity.md lines 52–83)

**Action:**

1. Create a file: `AGENT-SPEC.md` in your project root
2. Fill in these sections:
   ```markdown
   # Agent Specification
   
   ## Purpose
   [One sentence: What does this agent do?]
   
   ## Scope
   [What is the agent responsible for?]
   
   ## What it CAN do (autonomous decisions)
   - [Decision 1]
   - [Decision 2]
   
   ## What it CANNOT do (require human approval)
   - [Action 1]
   - [Action 2]
   
   ## Success Criteria
   - [Measurable outcome 1]
   - [Measurable outcome 2]
   - [Measurable outcome 3]
   
   ## Constraints (what it should never do)
   - Never [constraint 1]
   - Never [constraint 2]
   
   ## Starting Input
   [What information does the agent receive at the start?]
   
   ## Expected Output Format
   [What should the agent return? Structure it clearly]
   ```

3. Read what you wrote. Are there any ambiguities? (Could someone else misunderstand your intent?) If yes, clarify.

**Validation:**
- [ ] Spec has all 8 sections filled in
- [ ] Success criteria are measurable (not just "works well")
- [ ] At least 2 constraints defined (what it should never do)
- [ ] You can point to this spec and say "yes, my agent does this"

---

### Step 1.2: Design & Test Tools in Isolation

**What you're doing:** Build each tool your agent will use independently. Test them before the agent ever touches them.

**KB Reference:** [Tool Use: Design, Selection, Restrictions](../LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md lines 675–847)

**Action:**

1. List the tools your agent needs (from AGENT-SPEC.md "What it CAN do")
   ```python
   # tools.py
   
   def tool_one(input_param: str) -> dict:
       """Tool does one specific thing."""
       # implementation
       return {"status": "success", "result": result}
   
   def tool_two(input_param: str) -> dict:
       """Tool does one specific thing."""
       # implementation
       return {"status": "success", "result": result}
   ```

2. Write a test for each tool:
   ```python
   # test_tools.py
   
   def test_tool_one_happy_path():
       result = tool_one("valid_input")
       assert result["status"] == "success"
       assert "result" in result
   
   def test_tool_one_invalid_input():
       result = tool_one("invalid_input")
       assert result["status"] == "error"
   ```

3. Run tests: `pytest test_tools.py -v`
4. Confirm all tests pass before moving on

**Validation:**
- [ ] Each tool is a single, focused function (does one thing)
- [ ] Each tool returns a dict with `{"status": "success|error", "result": ...}`
- [ ] Each tool has at least 2 tests (happy path + error case)
- [ ] All tests pass

**Why this matters:** If a tool is broken, your agent will fail. Find tool bugs before the agent touches them.

---

### Step 1.3: Write System Prompt (Level 1 — Minimal)

**What you're doing:** Create a system prompt that defines the agent's role, goal, tools, and reasoning structure.

**KB Reference:** [Prompt Maturity Levels](../LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md lines 161–192)

**Action:**

1. Create a file: `src/prompts/agent-system.txt`
2. Start at **Level 1** (simplest possible):
   ```
   You are a [agent-name].
   
   Your job is to [purpose from AGENT-SPEC].
   
   You have access to these tools:
   - tool_one(param: str): [what it does]
   - tool_two(param: str): [what it does]
   
   CONSTRAINTS:
   - Never [constraint 1 from spec]
   - Never [constraint 2 from spec]
   
   When given a task:
   1. Understand what's being asked
   2. Think about which tools you need
   3. Use them to complete the task
   4. Return your result
   ```

3. Save this file. Don't optimize yet — keep it under 200 tokens.

**Validation:**
- [ ] Prompt is under 200 tokens
- [ ] It clearly states the agent's purpose
- [ ] All tools are listed
- [ ] Constraints are explicit

---

### Step 1.4: Test on 3 Scenarios

**What you're doing:** Run your agent on 3 test cases: happy path, edge case, failure mode. Confirm it works.

**KB Reference:** [Evaluation: Starting with 3–5 Test Cases](../LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md lines 1773–1805)

**Action:**

1. Write 3 test scenarios (in a file or as comments):
   ```python
   # test_agent.py
   
   # Scenario 1: Happy path (expected case)
   def test_agent_happy_path():
       agent = Agent(system_prompt=SYSTEM_PROMPT, tools=[tool_one, tool_two])
       result = agent.run("typical task description")
       assert result["status"] == "success"
   
   # Scenario 2: Edge case
   def test_agent_edge_case():
       agent = Agent(system_prompt=SYSTEM_PROMPT, tools=[tool_one, tool_two])
       result = agent.run("edge case task")
       assert "result" in result or result["status"] == "error"
   
   # Scenario 3: Failure mode
   def test_agent_failure():
       agent = Agent(system_prompt=SYSTEM_PROMPT, tools=[tool_one, tool_two])
       result = agent.run("task that should fail gracefully")
       assert result["status"] in ["error", "success"]  # Either is ok, should not crash
   ```

2. Run each scenario: `pytest test_agent.py -v`
3. Read the output carefully. Does the agent reason sensibly? Does it use the right tools?

**If all tests pass:** Go to Step 1.5  
**If any test fails:** Adjust the prompt slightly and re-run. (Stay at Level 1, don't add complexity yet)

**Validation:**
- [ ] 3 scenarios defined and executable
- [ ] All tests run without crashing
- [ ] Agent's reasoning is visible in outputs (you can see its thought process)
- [ ] At least 2 of 3 scenarios work correctly

---

### Step 1.5: Commit Phase 1

**What you're doing:** Save your work to git with a clean commit message.

**Action:**

```bash
git add AGENT-SPEC.md src/prompts/agent-system.txt src/tools.py tests/test_tools.py tests/test_agent.py
git commit -m "feat: phase 1 — agent spec, tools, level 1 prompt, passing 3 scenarios

- Spec defines purpose, scope, constraints, success criteria
- Tools tested independently before agent integration
- Level 1 system prompt (minimal, 150 tokens)
- 3 scenario tests: happy path, edge case, failure recovery
- All tests passing"
```

**Validation:**
- [ ] `git log` shows your commit with the message above
- [ ] All files are tracked (nothing untracked in `git status`)

---

### Next: Phase 2

Once Phase 1 is working and committed, you're ready for Phase 2: **Planning & ReAct Loop**

In Phase 2, you'll:
- Add explicit planning before tool use
- Implement the Thought → Action → Observation loop
- Test on more complex scenarios

See Phase 2 below ↓

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

**Persistent memory.** Add external memory so the agent can recall information from previous sessions and past tasks — this is what enables agents that improve over time rather than starting fresh every run. The retrieval strategy for that memory is a meaningful architectural decision, not just a vector store choice:

- **Semantic (embedding) retrieval** — for factual lookup ("what did we decide about X last week?"). The default and correct starting point.
- **BM25 + semantic hybrid** — the production baseline; adds exact-match retrieval for entity names, codes, and terminology that embeddings miss.
- **Knowledge graph retrieval** — for relational or planning queries ("what tasks depend on this component?", "what decisions touch this system?"). Agents doing multi-step planning often need to traverse relationships between entities, not just find similar documents. Add this when your agent's planning domain has meaningful entity relationships.
- **Temporal retrieval** — for history-aware agents that need to distinguish what is *currently* true from what was *previously* true ("what is the current state of this decision?" not "show me everything ever written about this decision").

Most agents start with semantic-only or 2-channel hybrid and that covers the majority of use cases. Add knowledge graph and temporal channels when your agent's queries demonstrate systematic failures they can't compensate for — relational failures and recency failures are the two signals to watch.

**Evaluation pipelines.** Once an agent is in production, set up automated tests that run it on known tasks and check the outcomes. Model updates and prompt drift can quietly break agents that were working fine.

**Cost monitoring.** Multi-step agents can make many LLM calls per task. Track cost per task from the start, and set budget limits that trigger early termination if something goes wrong.

---

## Phase 5: Production Optimization — Harness Tuning (Optional, High-Impact)

**Goal:** After your agent is stable in production with sufficient traffic, systematically optimize the agent's harness (prompt structure, tool presentation, context formatting) to improve accuracy and reduce cost.

**When to do this:** Once you have 100+ executions of the agent on real tasks and baseline metrics are stable. Optimization has diminishing returns on low-traffic agents; it pays for itself when the agent handles 100k+ inferences per month.

**Outcome:** 8–18% accuracy improvement and 30–50% token reduction through systematic discovery of better harness patterns.

---

### Step 5.1: Define Optimization Baseline

Before tuning, establish what you're optimizing for:

1. **Collect representative tasks:** 100–500 real-world examples from your agent's logs. These are your optimization dataset.
2. **Split the data:** 80% for optimization search, 20% held-out for final validation.
3. **Measure current performance:** Accuracy, latency, token usage per interaction on the held-out set. This is your baseline.
4. **Set an optimization budget:** 
   - Small: 500 evaluations (~6 hours, ~1% improvement)
   - Medium: 1,500 evaluations (~18 hours, typical choice, 8–12% improvement)
   - Large: 2,000+ evaluations (~24 hours, for high-traffic services, 12–18% improvement)

---

### Step 5.2: Run Harness Optimization Search

See: [`agentic-engineering/agentic-engineering.md` lines 842–1076](../LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md) (Automated Harness Optimization section — full technical details)

**In brief:** Use the Meta-Harness approach:

1. **Initialize a harness pool:** Your baseline agent + 100 mutations (reordered steps, modified context structure, different tool presentation, varied reasoning scaffolding).
2. **Iterative search:** For each iteration, evaluate all candidates on your 80% optimization set, identify top performers, extract patterns from their source code (e.g., "top performers all move constraints to the top"), generate new candidates by applying patterns, keep diverse set.
3. **Convergence signal:** Stop when top score doesn't improve for 3 consecutive iterations or budget exhausted.

**Observable signals during search:**
- Convergence rate (if accuracy improvement < 1% per 100 evals, diminishing returns)
- Diversity (if all top-10 harnesses use identical structure, you've found a local optimum)
- Pattern extraction (what structure patterns emerge from top performers?)

---

### Step 5.3: Validate on Held-Out Set

Once search converges:

1. **Evaluate final harness on held-out 20% data**
2. **Compare to baseline:** Require > 2% improvement on held-out set. If not met, optimization didn't generalize; use baseline instead.
3. **Test on related agent tasks:** If you have similar agents, test if this harness transfers to them (expect 60–75% transfer effectiveness).

---

### Step 5.4: Production Rollout & Monitoring

1. **Canary deployment:** Deploy to 5% traffic for 24 hours. Monitor for accuracy drop (> 2% triggers rollback).
2. **Gradual expansion:** 5% → 25% → 50% → 100% over 3–4 days.
3. **Ongoing monitoring:**
   - Accuracy trend (rolling 24h)
   - Token efficiency (tokens per inference)
   - New failure patterns (emerging once in production)

---

**When to re-optimize:**
- Quarterly: if new data shows task distribution shift
- Whenever a new model version releases (test harness transfer)
- Whenever you add new tools to the agent

---

*Draw from: `agentic-engineering/agentic-engineering.md` (architecture patterns, tool design, orchestration, **automated harness optimization**) · `context-engineering/context-engineering.md` (context strategies, window management) · `prompt-engineering/prompt-engineering.md` (ReAct, CoT, system prompting)*
