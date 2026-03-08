# Foundations of Agentic Engineering

## The Core Four Pillars

Everything in agentic engineering flows from four interconnected pillars:

| Pillar | Core Question |
|--------|---------------|
| **Prompt** | How to instruct the agent? |
| **Model** | What capabilities does the system provide? |
| **Context** | What information does the agent access? |
| **Tool Use** | What actions can the agent take? |

### How the Pillars Interact

The pillars are deeply interdependent:
- **Context fills as tools grow** — tool outputs consume context window space
- **Context is treated differently by different models** — each model has strengths and quirks
- **Certain models are better at tool calling** — capability varies significantly
- **Prompting impacts how models react to context and tools** — a prompt can disregard sections of context or available tools

When one pillar changes, it ripples to the others:
- **Downgrade the model** → massive performance impacts across the board
- **Add more tools** → risk flooding the context window
- **Alter context** → changes model behavior for the entire session
- **Change the prompt** → can steer or override how the model interprets everything else

### Hierarchy as of 2025

Until mid-2025, **model** sat at the top — the gap between frontier and everything else was large enough that model choice dominated outcomes. That gap has narrowed. The other pillars now carry more weight:
- **Tool use** is essential for any workflow that needs to take action
- **Context** alters entire session behavior
- **Prompting** determines direction of context window and model behavior

**Counter-intuitive finding:** "more" does not equal better capability. More tools, more context, more steering prompts degrade performance.

---

## The Twelve Leverage Points

A hierarchy of intervention points from lowest to highest leverage. Adapted from Donella Meadows' "Places to Intervene in a System."

> **Changes at the top (#1-#4) cascade throughout the system. Changes at the bottom (#9-#12) produce local fixes.**

| # | Leverage Point | Core Question |
|---|----------------|---------------|
| 12 | **Context** | What does the agent actually know? |
| 11 | **Model** | What tradeoffs exist: cost, speed, intelligence? |
| 10 | **Prompt** | Are instructions concrete and followable? |
| 9 | **Tools** | What actions can agents take, and in what form? |
| 8 | **Standard Out** | Can agents and operators see what's happening? |
| 7 | **Types** | Is typing consistent and enforced? |
| 6 | **Documentation** | Can agents navigate and trust the docs? |
| 5 | **Tests** | Are tests helping agents or just theatre? |
| 4 | **Architecture** | Is the codebase agentically intuitive? |
| 3 | **Plans** | Can agents complete tasks without further input? |
| 2 | **Templates** | Do agents know what good output looks like? |
| 1 | **ADWs** | How does work flow between agents? |

### Low Leverage (Local Fixes) — #12 to #9

**Context (#12):** Irrelevant context increases costs and dilutes signal. Loading entire documentation suites for every task (500k+ tokens, mostly irrelevant) is poor. Loading only relevant module documentation based on task requirements (15k tokens, high signal-to-noise) is good.

**Model (#11):** Match task complexity to model tier. Using GPT-4o for simple text extraction wastes 10x the cost. Use Claude 3.5 Sonnet for complex code generation, GPT-3.5 for text classification.

**Prompt (#10):** Vague → "Make this code better". Concrete → "Refactor the authentication module to use dependency injection. Extract token validation into a separate class. Maintain existing test coverage."

**Tools (#9):** Decide between internal tools, MCP servers, and CLI wrappers. The tradeoff is between flexibility and reliability.

### Medium Leverage (System Properties) — #8 to #5

**Standard Out (#8):** Observable agent systems are manageable. Logs should have clear sources, descriptions, and be self-documenting. Balance verbose logging with signal-to-noise ratio.

**Types (#7):** Strong typing helps agents write correct code. Surface type errors to agents in actionable ways. Type coverage correlates with agent success rate.

**Documentation (#6):** Documentation must be "agent-navigable" — easy to search, current, and self-improving. Agents look for documentation in predictable places; it should live there.

**Tests (#5):** Detect "testing theatre" (tests that pass but don't verify anything real). Mock implementations at the boundary, not internally. Test failures should guide agent behavior, not confuse it.

### High Leverage (Structural Changes) — #4 to #1

**Architecture (#4):** Codebases should be "agentically intuitive" — following historically-popular structures with higher likelihood of existing in training data. Familiar patterns → higher agent success.

**Plans (#3):** Plans are massive prompts passed to an agent with the expectation that no more user interaction is needed to finish the task. What makes a plan complete enough? How do you scope a plan? What happens if it fails partway through?

**Templates (#2):** Reusable, consistently structured prompts/plans. Agents need to know what good docs, code, and prompts look like. Templates prevent output drift.

**ADWs (#1):** AI Developer Workflows — how work carries between agents. Deterministic (code-based) vs. stochastic (agentic orchestration). The highest leverage point in the entire framework.

---

## Common Mistakes for New Practitioners

1. **Poor organization of information** — unstructured context causes models to miss critical information
2. **Excessive trust in model outputs** — skipping verification leads to compounding errors in multi-step workflows
3. **Flooding context with unrelated tools** — unfocused agents waste tokens evaluating irrelevant options
4. **Ad-hoc prompts with passive language** — vague instructions produce vague results
5. **Neglecting structure** in prompts, context, and tool responses
6. **Allowing too much freedom** — agents need constraints. Unbounded option spaces lead to analysis paralysis
7. **Insufficient instruction detail** — relying too heavily on agent discovery increases failure rates
8. **Failing to adhere to the Pit of Success mindset** — making correct actions harder than incorrect ones
