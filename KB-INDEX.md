# KB-INDEX — Complete Concept Navigation Map

**Purpose:** Find a concept quickly without reading entire files. KB is organized by learning path: Foundations → Agents & Systems → Production.

**Total KB:** ~9,300 lines across 13 learning docs + 7 playbooks + prompt catalog + PM context. Use this index to find exact sections.

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
| **104–140** | **Scale-Dependency in RAG: Empirical findings that retrieval effectiveness varies by model size & task; 3D scaling framework for pretraining/retrieval allocation** |
| **NEW:** 10. | Token Economics & MCP Budgeting: strategic compaction (50% threshold), dynamic MCP loading (77% savings) |
| **NEW:** 11. | Iterative Retrieval for Multi-Agent: 4-phase loop, max-3-cycles rule, 57% token savings vs. 2.4× quality improvement |

---

### LEARNING/FOUNDATIONS/reasoning-llms/reasoning-llms.md (268+ lines)

**When and how to use reasoning LLMs (o3, Claude 3.7, Gemini 2.5)**

| Lines | Section |
|---|---|
| 19–67 | What reasoning models are, when to use vs. standard models |
| 68–130 | Design patterns: planning layer, LLM-as-judge, agentic RAG |
| 131–197 | Prompting rules: no manual CoT, thinking effort tiers (low/medium/high) |
| 198–256 | Limitations, failure modes, when NOT to use reasoning |
| 257–268 | Decision workflow + key takeaways |
| **NEW:** | **Function-Calling CoT Budget Constraints: Non-monotonic relationship between CoT tokens and tool-use accuracy; practical implications for agentic reasoning** |

---

### LEARNING/FOUNDATIONS/multimodal/multimodal.md (~500 lines)

**Vision-language models, document understanding, multimodal RAG, audio, video, and agentic vision**

| Section | Topic |
|---|---|
| 1. | What "multimodal" actually means — modalities, early vs. late fusion, images as token representations |
| 2. | VLM architecture deep dive — vision encoder (ViT/CLIP/DINOv2), projection layer (linear vs. Q-Former), LM backbone, resolution tradeoff, training paradigm |
| 3. | Major architectures — CLIP (contrastive pre-training, zero-shot), LLaVA (linear projection lesson), BLIP-2 (Q-Former), GPT-4V/4o (native multimodal), Claude vision (tile-based, 5MB/20 img limits, ~1,700 tokens at high detail), Gemini (1M context for long video) |
| 4. | Document understanding — OCR-then-LLM vs. vision-native vs. hybrid vs. specialized (Textract, Azure); decision table by document type |
| 5. | Multimodal RAG — 4 approaches: text-only, CLIP embedding, VLM-generated summaries, ColPali late interaction (patch-level SOTA) |
| 6. | Audio and speech — Whisper architecture, model size table (tiny to large-v3), faster-whisper (3x speedup), ASR options, TTS options, native audio models vs. ASR pipeline |
| 7. | Video understanding — frame sampling strategies, Gemini 1.5 long-video, production architecture |
| 8. | Multimodal in agentic systems — computer use loop, UI grounding challenge, vision as tool use |
| 9. | Evaluation and benchmarks — VQA/DocVQA/ChartQA/TextVQA/video benchmarks; contamination warning (39% inflation) |
| 10. | Practical guide — decision tree (when to use VLM vs. OCR), image preprocessing checklist, token cost math, VLM prompt engineering, 5 error modes unique to VLMs, production checklist |

---

### LEARNING/FOUNDATIONS/emerging-architectures/emerging-architectures.md (~500 lines)

**Frontier monitoring: architectural research challenging the transformer + BPE paradigm (early 2026)**

Type: Informed observer tracking a fast-moving frontier — not a practitioner how-to. Re-read every 6-12 months.

| Lines | Section |
|---|---|
| 1–35 | Purpose and framing — what this doc is for and how to use it |
| 36–115 | Section 1: Current dominant paradigm — transformer + BPE foundations, 4 known bottlenecks (autoregressive latency, O(n²) attention, tokenization artifacts, KV cache growth), why transformers resist displacement |
| 116–205 | Section 2: State Space Models / Mamba — SSM core idea (fixed-size hidden state, O(n) scaling), Mamba selective state transitions, Mamba-2 SSD theory, retrieval weakness, hybrid SSM/Transformer (Jamba 52B) as practical near-term bet |
| 206–295 | Section 3: Mixture of Experts (MoE) — already in production (Mixtral, GPT-4, DeepSeek-V3), routing mechanics, expert collapse + auxiliary loss fix, DeepSeek-V3 innovation (671B total / 37B active per token), fine-grained MoE frontier |
| 296–390 | Section 4: Byte-level and tokenization-free models — BPE problem, MegaByte (hierarchical byte-level), BLT (entropy-based dynamic patching, 50% FLOPs at equivalent quality), infrastructure gap |
| 391–475 | Section 5: Continuous / latent space models — CALM (K-token chunk vectors, 1.82B scale, custom BrierLM metric), diffusion LMs (MDLM/SEDD, parallel generation, infilling strength), flow matching, discrete vs. continuous tension |
| 476–555 | Section 6: Linear attention variants — Performer, RetNet, RWKV-6 (O(1) inference memory), retrieval precision tradeoff, GQA/MQA already in production (4-8x KV cache reduction) |
| 556–635 | Section 7: Signal vs. noise framework — 5 green flags, 5 red flags, current status table for all 7 architectures |
| 636–end | Section 8: Practical implications for builders — 1-2yr / 2-4yr / 4yr+ horizons, PM procurement questions, uncertainty framing |

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

### LEARNING/AGENTS_AND_SYSTEMS/mcp/mcp.md (~500 lines)

**Model Context Protocol — universal interface between AI models and external systems**

| Lines | Section |
|---|---|
| 1–50 | What MCP is, the N×M problem, HTTP analogy, what it enables |
| 51–110 | Architecture: hosts, clients, servers — three-tier diagram, session lifecycle |
| 111–210 | Three primitives: Tools (model-controlled), Resources (app-controlled), Prompts (user-controlled) |
| 211–270 | Transport: stdio vs. HTTP+SSE — comparison table, Claude Desktop config example |
| 271–360 | MCP vs. function calling — key differences table, when to use each |
| 361–460 | Building an MCP server — Python SDK + TypeScript SDK minimal examples, design principles |
| 461–520 | Security model — trust hierarchy, consent requirement, 4 MCP-specific attack types + defenses |
| 521–560 | Ecosystem — host apps, server categories table, official + community servers, SDKs |
| 561–590 | Decision framework — MCP vs. direct integration decision table, portfolio approach |
| 591–640 | MCP in agentic systems — shared tool layer diagram, context budget (82% savings), memory pattern, MCP+RAG pattern |

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

### LEARNING/PRODUCTION/rl-alignment/rl-alignment.md (~550 lines)

**Full landscape of RL techniques for aligning and improving language models — from RLHF to RLVR**

Prerequisites: fine-tuning.md, evaluation.md

| Lines | Section |
|---|---|
| 1–70 | RL alignment landscape: why RL is needed, core loop, technique spectrum + comparison table |
| 71–200 | RLHF: 3-stage pipeline (SFT → RM → PPO), InstructGPT result (1.3B beats 175B), KL penalty mechanics, reward hacking |
| 201–310 | DPO: eliminates RM + PPO, closed-form derivation (conceptual), variants (IPO, KTO, SimPO), when to use |
| 311–420 | PRMs vs. ORMs: step-level vs. outcome labels, PRM800K, Lightman et al. 2023 SOTA on MATH, Monte Carlo rollout training |
| 421–500 | GRPO: eliminates value function, group-relative advantage formula, key params (G=8–16), DeepSeek-R1 result |
| 501–590 | RLVR: verifiable reward paradigm, verifiable domains table, DeepSeek-R1 architecture, "aha moment" emergence, code+unit-tests recipe |
| 591–660 | Constitutional AI + RLAIF: 2-phase CAI process, AI labeling scaling argument, laundering failure mode |
| 661–720 | RFT / STaR: rejection sampling loop, iterative bootstrapping, limitations (can't start from 0%) |
| 721–800 | Reward hacking + alignment tax: concrete examples (verbosity, sycophancy, formatting), mitigations, managing the tax |
| 801–end | Practical stack for builders: base model alignment comparison table, fine-tuning safety risks, evaluation signals, technique decision framework |

---

### LEARNING/PRODUCTION/inference-optimization/inference-optimization.md (~500 lines)

**How LLMs actually run in production — latency, throughput, cost, and the full optimization toolkit**

| Lines | Section |
|---|---|
| 1–60 | What inference optimization is: training vs. inference compute, why inference bottlenecks, 5 key metrics (TPS, TTFT, TPOT, p95/p99, GPU utilization) |
| 61–190 | Quantization: FP32/FP16/BF16/INT8/INT4 tradeoffs; GPTQ vs. AWQ; accuracy cliff; VRAM table (7B→405B at each precision) |
| 191–270 | Speculative decoding: autoregressive bottleneck, draft+verify mechanism, 2–3× latency gains, Medusa heads |
| 271–380 | KV cache: memory formula, PagedAttention (24× throughput), prefix caching, sliding window, GQA (4–8× cache reduction) |
| 381–440 | Continuous batching: static vs. dynamic scheduling, 5–30× throughput improvement, framework support |
| 441–540 | Serving frameworks: vLLM, TGI, Triton+TensorRT, SGLang, Ollama — comparison table + selection guide |
| 541–620 | Parallelism: tensor (within-node, NVLink), pipeline (cross-node), data, expert (MoE) — decision guide |
| 621–660 | Flash Attention: O(n²) → O(n) memory, 3–7× speedup, FA2/FA3, practitioner notes |
| 661–740 | Production optimization workflow: 9-step sequence from profiling to continuous monitoring |
| 741–780 | Cost mental model: API vs. self-host break-even, 10M tokens/day threshold, GPU reference table |
| 781–end | Quick reference: technique selection table (problem → technique → expected gain) |

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

### future-reference/playbooks/ (11 playbooks)

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
| [building-professional-websites.md](future-reference/playbooks/building-professional-websites.md) | Website builds | Professional website architecture and patterns |
| [project-example-support-classifier.md](future-reference/playbooks/project-example-support-classifier.md) | Worked example | End-to-end support ticket classifier build |
| [project-template.md](future-reference/playbooks/project-template.md) | New projects | General AI project template structure |

---

---

## 🛠️ SKILLS-CATALOG — Pull-Ready Skills & Agents

### skills-catalog/ (35 skills + 15 agents)

**Functional Claude Code skills and agent definitions. Copy into `.claude/skills/` or `.claude/agents/` for any project.**

See [skills-catalog/README.md](skills-catalog/README.md) for the full index, descriptions, and quick-setup recipes.

| Category | Count | Source | Examples |
|---|---|---|---|
| `workflow/` | 11 skills | Skills Master | brainstorming, planning, smart-commit, deslop, session-handoff |
| `design/` | 6 skills | Skills Master | frontend-taste, ui-ux-pro-max, web-design-patterns |
| `engineering/` | 11 skills | Skills Master + ECC | tdd-workflow, verification-loop, api-design, security-review |
| `production/` | 6 skills + reference | ECC | context-budget, strategic-compact, deployment-patterns, hooks-reference |
| `agents/` | 15 agents | ECC | planner, architect, chief-of-staff, code-reviewer, loop-operator |
| `meta/` | 1 skill | Skills Master | antigravity_skill_creator |

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
| **FOUNDATIONS** | Prompt Eng, Context Eng, Reasoning, Multimodal, Emerging Architectures | ~2,400 | 7-8h |
| **AGENTS_AND_SYSTEMS** | Agentic Eng, System Design, Skills, MCP | ~4,500 | 10-11h |
| **PRODUCTION** | Evaluation, Security, Specs, Fine-tuning, Inference Optimization, RL Alignment | ~3,450 | 12-13h |
| **CAREER** | PM preparation (4 docs) | ~800 | As needed |
| **FUTURE-REFERENCE** | 11 playbooks + catalog + specs | ~3,500 | As needed |
| **SKILLS-CATALOG** | 35 skills + 15 agents | ~15,000 | Per project |
| **Total** | **14 learning topics + skills catalog + extras** | **~26,000+** | **28-31h learning** |

Last updated: 2026-04-01 (added skills-catalog with 35 skills + 15 agents; deepened multi-agent orchestration + hooks sections in agentic-engineering.md; fixed playbook index count)
