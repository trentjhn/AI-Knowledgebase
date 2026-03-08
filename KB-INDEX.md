# KB-INDEX — Complete Concept Navigation Map

**Purpose:** Find a concept quickly without reading entire files. KB is organized in three sections: LEARNING (study), CAREER (professional), FUTURE-REFERENCE (practice).

**Total KB:** ~6,500+ lines across 10 learning docs + 7 playbooks + prompt catalog + PM context. Use this index to find exact sections.

---

## 📚 LEARNING SECTION

### LEARNING/prompt-engineering/prompt-engineering.md (518 lines)

**Core prompting techniques and research findings**

| Lines | Section |
|---|---|
| 29–42 | What prompt engineering is |
| 43–86 | Output config: temperature, top-K, top-P, length, interaction effects |
| 87–102 | Zero-shot prompting |
| 103–133 | Few-shot / one-shot prompting |
| 134–162 | System, role, contextual prompting |
| 148–162 | Step-back prompting |
| 163–221 | Chain of Thought (CoT) — empirical results: MultiArith +61, GSM8K +30.3 |
| 201–229 | Self-consistency — GSM8K +17.9%, SVAMP +11.0% |
| 222–256 | Tree of Thoughts (ToT) |
| 230–277 | ReAct (Reason + Act) |
| 257–280 | APE — Automatic Prompt Engineering (beats humans 24/24) |
| 278–368 | Advanced techniques: Auto-CoT, Reprompting (+9.4 pts), Chain of Draft, RaR, OPRO |
| 369–401 | Code prompting techniques |
| 402–499 | Best practices |
| 500–518 | Anti-patterns to avoid |

---

### LEARNING/prompt-engineering/future-reference/prompt-catalog/ (Prompt Patterns Reference)

**16 prompt patterns organized by category—use these templates when building**

| Lines | Section |
|---|---|
| 7–28 | What patterns are, how to use |
| 35–65 | Input Semantics: Meta Language Creation |
| 72–209 | Output Customization: Automater, Persona, Visualization, Template, Infinite Generation |
| 216–272 | Error Identification: Fact Check List, Reflection |
| 279–439 | Prompt Improvement: Question Refinement, Alternative Approaches, Cognitive Verifier, Refusal Breaker |
| 384–439 | Interaction: Flipped Interaction, Game Play |
| 446–531 | Context Control: Context Manager, Recipe |
| 510–544 | Combining patterns + key takeaways |

---

### LEARNING/context-engineering/context-engineering.md (600+ lines)

**Context as a first-class engineering discipline**

| Lines | Section |
|---|---|
| 21–59 | Context window explained, prompt vs. context engineering distinction |
| 60–131 | 8 context components: system prompt, user input, memory, RAG, tools, tool responses, state |
| 132–204 | 4 core strategies: Write / Select / Compress / Isolate with examples |
| 205–289 | 4 failure modes: Poisoning / Distraction / Confusion / Clash (with empirical evidence) |
| 290–406 | Custom context formats, ordering rules, long-term memory, workflow engineering |
| 390–446 | Anti-patterns, tools, integration checklist |
| **NEW:** 10. | Token Economics & MCP Budgeting: strategic compaction (50% threshold), dynamic MCP loading (77% savings) |
| **NEW:** 11. | Iterative Retrieval for Multi-Agent: 4-phase loop, max-3-cycles rule, 57% token savings vs. 2.4× quality improvement |

---

### LEARNING/reasoning-llms/reasoning-llms.md (268 lines)

**When and how to use reasoning LLMs (o3, Claude 3.7, Gemini 2.5)**

| Lines | Section |
|---|---|
| 19–67 | What reasoning models are, when to use vs. standard models |
| 68–130 | Design patterns: planning layer, LLM-as-judge, agentic RAG |
| 131–197 | Prompting rules: no manual CoT, thinking effort tiers (low/medium/high) |
| 198–256 | Limitations, failure modes, when NOT to use reasoning |
| 257–268 | Decision workflow + key takeaways |

---

### LEARNING/skills/skills.md (850+ lines)

**Agent Skills standard—building, testing, distributing reusable agent knowledge**

| Lines | Section |
|---|---|
| 20–69 | What skills are, the re-explaining problem, core principles |
| 70–120 | Skills vs. MCP: decision framework, when to use each |
| 121–234 | Skill anatomy: SKILL.md, YAML frontmatter (CRITICAL), instruction writing |
| 235–344 | 3 categories (document creation, workflow automation, MCP enhancement) + 5 workflow patterns |
| 345–527 | Testing (trigger/functional/performance), iteration signals, distribution |
| 527–543 | Anti-patterns |
| **NEW:** 14. | Continuous Learning via Instincts v2: micro-skills with confidence scoring (0.3-0.9), lifecycle stages, YAML format, promotion logic |

---

### LEARNING/agentic-engineering/agentic-engineering.md (2,000+ lines)

**The most comprehensive agentic engineering reference—everything about building AI agents**

| Lines | Section |
|---|---|
| 9–62 | What an agent is, Four Pillars |
| 63–146 | Twelve Leverage Points framework |
| 147–343 | Prompt engineering for agents: 7-level maturity, 7-section structure |
| 344–506 | Model selection, behavior, multi-model architectures |
| 507–670 | Context management, degradation thresholds, advanced patterns |
| 671–841 | Tool design, selection, restrictions, scaling, MCP, tool lifecycle |
| 842–1269 | Patterns: Plan-Build-Review, Orchestrator, ReAct, HITL, Expert Swarm, Multi-Agent, Persistent Memory |
| 1270–1525 | Practices: debugging, cost, production, evaluation, intent engineering, spec engineering |
| 1526–1726 | Mental models: Pit of Success, Specs as Source Code, Topologies, Context as Code |
| **NEW:** | Agent Orchestration Patterns: sub-agent context problem, iterative retrieval, sequential phase orchestration |
| **NEW:** | Agent Abstraction Tierlist: Tier 1 (easy wins) vs. Tier 2 (high skill floor) |

---

### LEARNING/ai-security/ai-security.md (1,100+ lines)

**Complete AI security threat model and defense strategies**

| Lines | Section |
|---|---|
| 1–62 | Why AI agents require different security mindset |
| 63–145 | Governance framework for AI agents |
| 146–289 | OWASP LLM Top 10 threat landscape |
| 290–512 | Deep dives: key attack vectors (injection, poisoning, model theft, etc.) |
| 513–718 | Core security principles: Zero Trust, least privilege, defense in depth |
| 719–897 | Identity & Access Management for agents |
| 898–1045 | AI Firewall / Gateway pattern |
| 1046–1200 | Sandboxing: execution isolation (4 tiers) |
| 1201–1350 | Monitoring, detection, DevSecOps |
| **NEW:** 11. | Agent Configuration Security: transitive injection threats, defense matrix, tool allowlisting, context layering, credential scoping, 4-tier sandboxing, MCP vetting |

---

### LEARNING/evaluation/evaluation.md (1,000+ lines)

**Evaluating AI systems in production—metrics, frameworks, best practices**

| Lines | Section |
|---|---|
| 1–145 | Why evaluation is hard: probabilistic outputs, no ground truth, measurement bias |
| 146–289 | 3-level eval stack: offline / online / human |
| 290–412 | What you're actually measuring: faithfulness, relevance, coherence, hallucination rate |
| 413–598 | LLM-as-judge with all 4 bias types and mitigations (GPT-4 >80% human agreement) |
| 599–756 | RAG evaluation via Ragas framework (4 metrics: retrieval, relevance, etc.) |
| 757–889 | Agent evaluation (task completion, trajectory quality) |
| 890–1045 | Benchmarks + contamination risk (39.4% drop on uncontaminated) |
| 1046–1200 | Framework comparison table (Ragas, DeepEval, Braintrust, etc.) |
| **NEW:** 14. | Evaluation Patterns: checkpoint-based vs. continuous evals, pass@k vs. pass^k metrics |
| **NEW:** 15. | Eval-Driven Development (EDD): evals BEFORE implementation, cost-benefit analysis (pays for itself on 2nd similar feature) |

---

### LEARNING/fine-tuning/fine-tuning.md (586 lines)

**Fine-tuning as a strategy—when to use, methods, costs, failure modes**

| Lines | Section |
|---|---|
| 1–89 | What fine-tuning is, fine-tuning vs. prompting vs. RAG decision framework |
| 90–234 | Fine-tuning spectrum: pre-training → instruction tuning → RLHF/DPO → task fine-tuning |
| 235–389 | Instruction tuning (FLAN, InstructGPT), RLHF 3-stage process |
| 390–512 | DPO as simpler RLHF alternative (preferred vs. rejected pairs) |
| 513–556 | PEFT/LoRA (10,000× fewer params), QLoRA (quantization tricks) |
| 557–650 | Data requirements, synthetic data, Alpaca problem |
| **NEW:** | Model Selection & Cost Trade-offs: Opus/Sonnet/Haiku routing, subagent optimization, 75% cost reduction examples |

---

### LEARNING/ai-system-design/ai-system-design.md (1,200+ lines)

**Architectural patterns for AI systems at scale**

| Lines | Section |
|---|---|
| 1–145 | Design thinking for AI systems |
| 146–412 | 11 core design patterns (agents, RAG, classification, content generation, etc.) |
| 413–678 | Data pipelines: ingestion, processing, retrieval, monitoring |
| 679–834 | Observability: logging, tracing, alerting, metrics |
| 835–1000 | Scalability: caching, batching, parallel processing, resource management |
| 1001–1200 | Trade-offs: cost vs. quality, latency vs. accuracy, consistency vs. availability |

---

### LEARNING/specification-clarity/specification-clarity.md (512 lines)

**Writing AI specs that are unambiguous and implementable**

| Lines | Section |
|---|---|
| 1–89 | Why specs matter, 7-property framework |
| 90–234 | Types of ambiguity (scope, definition, success, behavior, edge case) |
| 235–389 | BDD acceptance criteria pattern for AI systems |
| 390–512 | Constraint architecture, decomposition strategies, spec anti-patterns |

---

## 🎯 CAREER SECTION

### CAREER/pm-context/ (PM Role, Fundamentals, Scenarios, Applications)

**AI PM interview & career preparation**

- **ai-pm-role.md** — What AI PM means, what companies value, responsibilities
- **pm-fundamentals.md** — PM frameworks, decision-making models, mental models
- **interview-scenarios.md** — Real interview questions, case studies, how to approach
- **ai-pm-applications.md** — How each KB concept (agents, RAG, prompting, etc.) maps to PM decisions

---

## 🔧 FUTURE-REFERENCE SECTION

### future-reference/playbooks/

**Practical, ready-to-use guides for building AI systems**

| Playbook | Best for |
|----------|----------|
| [autonomous-agent-loops.md](future-reference/playbooks/autonomous-agent-loops.md) | Choosing the right loop pattern (sequential, iterative, infinite, RFC-DAG, REPL persistence, cleanup) with quality gates |
| [multi-agent-orchestration.md](future-reference/playbooks/multi-agent-orchestration.md) | Building 13-agent systems with parallel execution, context isolation, failure recovery |
| [cost-optimized-llm-workflows.md](future-reference/playbooks/cost-optimized-llm-workflows.md) | Model routing (Haiku/Sonnet/Opus), budget enforcement, cost tracking patterns |
| [building-ai-agents.md](future-reference/playbooks/building-ai-agents.md) | Step-by-step agent implementation |
| [building-chatbots.md](future-reference/playbooks/building-chatbots.md) | Conversational AI systems |
| [building-rag-pipelines.md](future-reference/playbooks/building-rag-pipelines.md) | Retrieval-augmented generation workflows |
| [writing-production-prompts.md](future-reference/playbooks/writing-production-prompts.md) | Production-grade prompt engineering |

---

### future-reference/prompt-catalog/

**Template prompts organized by domain**

- **prompt-patterns.md** — 16 reusable prompt pattern templates
- **analysis-research/** — Chain of Thought, research analysis prompts
- **design-product/** — Product design, requirements writing prompts

---

### future-reference/specs/

**Project specifications and implementation plans**

- PromptArena design system & implementation plan
- Future: Zenkai spec (personalized learning system)

---

## 🔍 How to Use This Index

1. **Find your topic:** Search for a concept or task above
2. **Read the relevant lines only:** Don't read the whole file—jump to the section you need
3. **Consult LEARNING for understanding:** If you need to learn a concept
4. **Consult FUTURE-REFERENCE for building:** If you're implementing something
5. **Consult CAREER for interview/PM work:** If preparing professionally

---

## Summary Statistics

| Category | Folders | Docs | Lines |
|----------|---------|------|-------|
| LEARNING | 10 | 10 | ~6,200 |
| CAREER | 1 | 4 | ~800 |
| FUTURE-REFERENCE | 3 | 7+catalog | ~2,500 |
| **Total** | **14** | **21+** | **~9,500** |

Last updated: 2026-03-08
