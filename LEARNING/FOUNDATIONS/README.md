# FOUNDATIONS — Core Concepts (Start Here)

Understanding how LLMs work, how to prompt them, and how they reason.

**Read this first.** These three topics are prerequisites for everything else in the KB.

---

## Topics

### [**Prompt Engineering**](prompt-engineering/)
**518 lines** — Everything about prompting techniques with research backing

- 9 core techniques: zero-shot, few-shot, CoT (Chain of Thought), self-consistency, APE, ReAct, ToT, and more
- Empirical results: Zero-shot CoT increases accuracy 17.7% → 78.7% on math problems
- Output configuration: temperature, top-K, top-P interactions
- Code prompting, best practices, anti-patterns

**Start with:** Sections on zero-shot CoT and few-shot if new to prompting

---

### [**Context Engineering**](context-engineering/)
**600+ lines** — How LLMs use context, strategies for managing it, failure modes

- What is a context window and why it matters
- 8 context components: system prompt, user input, memory, RAG, tools, etc.
- 4 core strategies: Write (create context), Select (retrieve), Compress (summarize), Isolate (separate trusted/untrusted)
- 4 failure modes: Poisoning, Distraction, Confusion, Clash
- Token budgeting, MCP overhead, iterative retrieval for multi-agent systems

**Start with:** "What is a context window?" section, then 4 strategies

---

### [**Reasoning LLMs**](reasoning-llms/)
**268 lines** — When and how to use reasoning models (o3, Claude 3.7, Gemini 2.5)

- What reasoning models are and when they're worth the cost
- Design patterns: planning layer, LLM-as-judge, agentic RAG
- Thinking effort tiers: low (fast) vs. medium (balanced) vs. high (expensive but thorough)
- Limitations and when NOT to use reasoning

**Start with:** "What reasoning models are" section, decision workflow at end

---

## Learning Path

1. **Start:** Prompt Engineering (understand how to talk to LLMs)
2. **Then:** Context Engineering (understand what they can see)
3. **Then:** Reasoning LLMs (understand when to use advanced models)
4. **Next:** Move to [AGENTS_AND_SYSTEMS/](../AGENTS_AND_SYSTEMS/) to start building

---

## Quick Reference

| Topic | Best For | Read Time |
|-------|----------|-----------|
| Prompt Engineering | Learning prompting techniques | 2-3 hours |
| Context Engineering | Understanding LLM blindspots | 2 hours |
| Reasoning LLMs | Knowing when to splurge on reasoning | 45 min |

---

**Next step:** Once you understand these three, move to [AGENTS_AND_SYSTEMS/](../AGENTS_AND_SYSTEMS/) to learn how to build with them.

Last updated: 2026-03-08
