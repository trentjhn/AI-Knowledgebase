# KB-INDEX — Complete Concept Navigation Map

**Purpose:** Find a concept quickly without reading entire files. KB is organized by learning path: Foundations → Agents & Systems → Production.

**Total KB:** ~7,800 lines across 10 learning docs + 7 playbooks + prompt catalog + PM context. Use this index to find exact sections.

---

## 📚 LEARNING / FOUNDATIONS — Core Concepts (Start Here)

---

### LEARNING/FOUNDATIONS/prompt-engineering/prompt-engineering.md (518 lines)

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

### LEARNING/FOUNDATIONS/context-engineering/context-engineering.md (600+ lines)

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

### LEARNING/FOUNDATIONS/reasoning-llms/reasoning-llms.md (268 lines)

**When and how to use reasoning LLMs (o3, Claude 3.7, Gemini 2.5)**

| Lines | Section |
|---|---|
| 19–67 | What reasoning models are, when to use vs. standard models |
| 68–130 | Design patterns: planning layer, LLM-as-judge, agentic RAG |
| 131–197 | Prompting rules: no manual CoT, thinking effort tiers (low/medium/high) |
| 198–256 | Limitations, failure modes, when NOT to use reasoning |
| 257–268 | Decision workflow + key takeaways |

---

## 📚 LEARNING / AGENTS & SYSTEMS — Building (Mid-Level)

Prerequisites: Complete FOUNDATIONS first.

---

### LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md (2,603 lines)

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
| 1967–2058 | Agent Frameworks: LangChain, LangGraph, CrewAI, Claude Agent SDK, decision framework |
| 2060–2130 | Development Methodologies: 15 methodologies in 6-tier pyramid, plan-first principle |
| 2131–2185 | Dual-Instance Planning: planner↔implementer pattern, cost-benefit analysis, decision matrix |
| 2186–2225 | Event-Driven Agents: push-based agent pattern, guardrails (idempotency, concurrency, circuit breaker) |
| 2226–2270 | Team AI Coordination: profile-based module assembly, 4 components, scaling threshold |
| 2273–2603 | Multi-Agent Shared Context & Query Routing: frontier problem, 3 approaches (explicit/LLM-driven/pre-retrieval), real failure modes, evaluation framework |

---

### LEARNING/AGENTS_AND_SYSTEMS/ai-system-design/ai-system-design.md (897 lines)

**Architectural patterns for AI systems at scale**

| Lines | Section |
|---|---|
| 1–145 | Design thinking for AI systems |
| 146–412 | 11 core design patterns (agents, RAG, classification, content generation, etc.) |
| 413–678 | Data pipelines: ingestion, processing, retrieval, monitoring |
| 679–834 | Observability: logging, tracing, alerting, metrics |
| 835–1000 | Scalability: caching, batching, parallel processing, resource management |
| 776–799 | MLOps Engineering Patterns: reproducibility, hyperparameter optimization |
| 800–897 | Production Safety Rules: 6 non-negotiable rules (port stability, database safety, feature completeness, infrastructure lock, dependency safety, pattern following) + Verification Paradox |

---

### LEARNING/AGENTS_AND_SYSTEMS/skills/skills.md (850+ lines)

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

## 📚 LEARNING / PRODUCTION — Ship (Advanced)

Prerequisites: Complete AGENTS_AND_SYSTEMS first.

---

### LEARNING/PRODUCTION/evaluation/evaluation.md (1,000+ lines)

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

### LEARNING/PRODUCTION/ai-security/ai-security.md (1,100+ lines)

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

### LEARNING/PRODUCTION/specification-clarity/specification-clarity.md (512 lines)

**Writing AI specs that are unambiguous and implementable**

| Lines | Section |
|---|---|
| 1–89 | Why specs matter, 7-property framework |
| 90–234 | Types of ambiguity (scope, definition, success, behavior, edge case) |
| 235–389 | BDD acceptance criteria pattern for AI systems |
| 390–512 | Constraint architecture, decomposition strategies, spec anti-patterns |

---

### LEARNING/PRODUCTION/fine-tuning/fine-tuning.md (586 lines)

**Fine-tuning as a strategy—when to use, methods, costs, failure modes**

| Lines | Section |
|---|---|
| 1–89 | What fine-tuning is, fine-tuning vs. prompting vs. RAG decision framework |
| 90–234 | Fine-tuning spectrum: pre-training → instruction tuning → RLHF/DPO → task fine-tuning |
| 235–389 | Instruction tuning (FLAN, InstructGPT), RLHF 3-stage process |
| 390–512 | DPO as simpler RLHF alternative (preferred vs. rejected pairs) |
| 513–556 | PEFT/LoRA (10,000× fewer params), QLoRA (quantization tricks) |
| 557–650 | Data requirements, synthetic data, Alpaca problem |

---

## 🎯 CAREER — PM & Professional Development

---

### CAREER/pm-context/ (4 documents)

**AI PM interview & career preparation**

- **ai-pm-role.md** — What AI PM is, what companies value, responsibilities
- **pm-fundamentals.md** — PM frameworks, decision-making models, mental models
- **interview-scenarios.md** — Real interview questions, case studies, how to approach
- **ai-pm-applications.md** — How each KB concept (agents, RAG, prompting, etc.) maps to PM decisions

---

## 🔧 FUTURE-REFERENCE — Practical Tools

---

### future-reference/playbooks/ (8 playbooks)

**Practical, ready-to-use guides for building AI systems**

| Playbook | Best for | Key Topics |
|----------|----------|-----------|
| [**meta-workflow.md**](future-reference/playbooks/meta-workflow.md) | **All projects (meta-layer)** | **6 phases (ideation → spec → design → build → harden → deploy → operate), decision matrices, failure taxonomy, playbook selector** |
| [autonomous-agent-loops.md](future-reference/playbooks/autonomous-agent-loops.md) | Choosing loop patterns | Sequential, iterative, infinite, RFC-DAG, REPL, cleanup with quality gates |
| [multi-agent-orchestration.md](future-reference/playbooks/multi-agent-orchestration.md) | Building multi-agent systems | 13-agent model, parallel execution, context isolation, failure recovery |
| [cost-optimized-llm-workflows.md](future-reference/playbooks/cost-optimized-llm-workflows.md) | Cost control | Model routing (Haiku/Sonnet/Opus), budget enforcement, retry strategies |
| [building-ai-agents.md](future-reference/playbooks/building-ai-agents.md) | Agent implementation | Step-by-step from scratch |
| [building-chatbots.md](future-reference/playbooks/building-chatbots.md) | Conversational systems | Chatbot architecture and patterns |
| [building-rag-pipelines.md](future-reference/playbooks/building-rag-pipelines.md) | RAG workflows | Retrieval-augmented generation patterns |
| [writing-production-prompts.md](future-reference/playbooks/writing-production-prompts.md) | Production prompts | Crafting reliable prompts for deployment |

---

### future-reference/prompt-catalog/

**Template prompts organized by domain**

- **prompt-patterns.md** — 16 reusable prompt pattern templates (Output Automater, Persona, Visualization, etc.)
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

## Learning Path Quick Reference

| Phase | Topics | Lines | Time |
|-------|--------|-------|------|
| **FOUNDATIONS** | Prompt Eng, Context Eng, Reasoning | ~1,400 | 5h |
| **AGENTS_AND_SYSTEMS** | Agentic Eng, System Design, Skills | ~4,000 | 9-10h |
| **PRODUCTION** | Evaluation, Security, Specs, Fine-tuning | ~2,400 | 8-9h |
| **CAREER** | PM preparation (4 docs) | ~800 | As needed |
| **FUTURE-REFERENCE** | 7 playbooks + catalog + specs | ~2,500 | As needed |
| **Total** | **10 learning topics + extras** | **~9,500** | **22-24h** |

Last updated: 2026-03-08
