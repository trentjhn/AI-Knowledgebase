# KB-INDEX — Complete Concept Navigation Map

**Purpose:** Find a concept quickly without reading entire files. KB is organized by learning path: Foundations → Agents & Systems → Production.

**Total KB:** ~9,300 lines across 14 learning docs + 9 playbooks + 24 agents + prompt catalog + PM context. Use this index to find exact sections.

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

### LEARNING/FOUNDATIONS/context-engineering/context-engineering.md (870+ lines)

**Context as a first-class engineering discipline**

| Lines | Section |
|---|---|
| 21–59 | Context window explained, prompt vs. context engineering distinction |
| 60–131 | 8 context components: system prompt, user input, memory, RAG, tools, tool responses, state |
| 132–204 | 4 core strategies: Write / Select / Compress / Isolate with examples |
| 205–289 | 4 failure modes: Poisoning / Distraction / Confusion / Clash (with empirical evidence) |
| **302–340** | **Failure Mode 5: Knowledge Integration Bottleneck in RAG — resolving conflicts between parametric knowledge & retrieved documents; joint decoding solution; 12.1% accuracy gain, 16.3% hallucination reduction** |
| **219–233** | **Multi-agent isolation cost-benefit: DACS mechanism (Dynamic Attentional Context Scoping), empirical validation (90–98.4% steering accuracy, 3.53× context efficiency, 0–14% contamination vs. 28–57% baseline)** |
| 341–420 | Custom context formats, ordering rules, long-term memory, workflow engineering |
| 410–466 | Anti-patterns, tools, integration checklist |
| **104–140** | **Scale-Dependency in RAG: Empirical findings that retrieval effectiveness varies by model size & task; 3D scaling framework for pretraining/retrieval allocation** |
| **NEW:** 10. | Token Economics & MCP Budgeting: strategic compaction (50% threshold), dynamic MCP loading (77% savings) |
| **NEW:** 11. | Iterative Retrieval for Multi-Agent: 4-phase loop, max-3-cycles rule, 57% token savings vs. 2.4× quality improvement |
| **NEW:** 12. | Context Compaction — threshold guidance (5K–150K), 58.6% token reduction on sequential workflows, tool result clearing (96.3% bloat reduction), automatic summarization pattern |
| **NEW:** 13. | Speculative Prompt Caching — 90.7% TTFT improvement (20.87s → 1.94s), parallel cache warming during user input, requirements for cache hit |

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

### LEARNING/AGENTS_AND_SYSTEMS/agent-sdk/agent-sdk.md (~450 lines) *(NEW)*

**Claude Agent SDK implementation patterns — the how-to layer above agentic concepts**

| Lines | Section |
|---|---|
| 1–60 | SDK vs. base API — what's different; core abstractions (query, sessions, Task tool, vaults) |
| 61–120 | Pattern 1: Research Agent — stateless query, allowed_tools, specialization |
| 121–200 | Pattern 2: Chief-of-Staff — Task tool delegation, context isolation, orchestrator-only rule |
| 201–260 | Pattern 3: Parallel Subagents — model tiering (Opus orchestrates, Haiku workers), ThreadPoolExecutor, cost math |
| 261–320 | Pattern 4: Programmatic Tool Calling (PTC) — code execution vs. round trips, filtering at code level |
| 321–370 | Pattern 5: Semantic Tool Routing — embedding-based discovery, 90%+ context reduction, deferred loading |
| 371–410 | Pattern 6: Evaluator-Optimizer Loop — PASS/NEEDS_IMPROVEMENT/FAIL signals, iteration caps |
| 411–435 | Decision framework — choosing between patterns |
| 436–460 | Cost optimization — model tiering table, context isolation, parallel execution economics |
| 461–480 | Anti-patterns — orchestrators doing domain work, shared context, no exit conditions |

---

### LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md (4,200+ lines)

**The most comprehensive agentic engineering reference—everything about building AI agents**

| Lines | Section |
|---|---|
| 9–62 | What an agent is, Four Pillars |
| 63–146 | Twelve Leverage Points framework |
| 147–343 | Prompt engineering for agents: 7-level maturity, 7-section structure |
| 344–506 | Model selection, behavior, multi-model architectures |
| 507–670 | Context management, degradation thresholds, advanced patterns |
| 671–891 | Tool design, selection, restrictions, scaling, MCP, tool lifecycle (including meta-cognitive tool arbitration & dual-channel optimization) |
| **740–790** | **Meta-Cognitive Tool Arbitration: "blind tool invocation" pathology. Why scalar RL rewards fail. Dual-channel framework separating accuracy from efficiency. Orders-of-magnitude tool reduction while improving reasoning accuracy** |
| **842–1746** | **AUTOMATED HARNESS OPTIMIZATION (NEW — Meta-Harness, Lee et al. 2026): Systematic discovery of model wrapping patterns via filesystem-mediated search. The harness problem (manual prompt/tool/context structure design). Why text-based optimization fails (output compression loses implementation detail). The Meta-Harness architecture with agentic proposer + execution trace analysis. Harness patterns discovered (CoT structuring, self-correction, RAG integration, tool trace management, constraint reinforcement). Empirical results (12–18% accuracy gains on retrieval tasks, 8–15% on code generation, 75% context reduction). Three-phase implementation workflow (baseline → automated search → validation & deployment). Observable signals for production monitoring (accuracy drift, token efficiency, failure pattern clustering). Failure modes & practical limits (60–75% cross-task transfer ceiling, model overfitting, instruction sensitivity, long-horizon bottleneck). Practical application to agentic systems (planning agents, tool-using agents, RAG agents, multi-turn agents).** |
| 1747–2074 | Patterns: Plan-Build-Review, Orchestrator, ReAct, HITL, Expert Swarm, Multi-Agent, Persistent Memory |
| **1018–1055** | **Fundamental Limits on Delegation: Information-theoretic bounds on multi-agent planning (Ao et al. 2026). Delegated agents improve outcomes only with asymmetric information. Communication bottleneck creates information loss (posterior divergence). Practical architecture guidance for when to centralize vs. distribute** |
| 2075–2330 | Practices: debugging, cost, production, evaluation, intent engineering, spec engineering |
| 2331–2531 | Mental models: Pit of Success, Specs as Source Code, Topologies, Context as Code |
| **~2973–3030** | **Externalization: Cognitive Architecture Lens (Zhou et al. 2026) — Weights→Context→Harness evolution; 4-element taxonomy (Memory/Skills/Protocols/Harness); failure modes as representational mismatches; relationship to Four Pillars** |
| 2772–2863 | Agent Frameworks: LangChain, LangGraph, CrewAI, Claude Agent SDK, decision framework |
| 2865–2935 | Development Methodologies: 15 methodologies in 6-tier pyramid, plan-first principle |
| 2936–2990 | Dual-Instance Planning: planner↔implementer pattern, cost-benefit analysis, decision matrix |
| 2991–3030 | Event-Driven Agents: push-based agent pattern, guardrails (idempotency, concurrency, circuit breaker) |
| 3031–3075 | Team AI Coordination: profile-based module assembly, 4 components, scaling threshold |
| 3078–3408 | Multi-Agent Shared Context & Query Routing: frontier problem, 3 approaches (explicit/LLM-driven/pre-retrieval), real failure modes, evaluation framework |
| **~3410–3580** | **Claude Code Agent Teams (Section 16): Native multi-agent primitive. Peer sessions vs. hub-and-spoke. Shared task list + mailbox architecture. Subagent definitions as blueprints. Quality gates via TeammateIdle/TaskCreated/TaskCompleted hooks. Connection to Section 15 shared context problem. Decision matrix vs. subagents. Key limitations.** |
| **1805–1890** | **Long-Horizon Planning Under Compounding Consequences: Scratchpad usage as context persistence, adversarial reasoning gap (47% failure rate), modeling compound effects. Practical deployment strategies for multi-month tasks** |
| **1222–1616** | **Self-Organizing Multi-Agent Systems: The Endogeneity Paradox (Dochkina 2026). 25,000-task study proving Sequential protocol (fixed ordering + autonomous role selection) outperforms centralized coordination by 14% and fully autonomous by 44%. Complete system architecture, deployment workflow, model selection with capability thresholds, scaling to 256 agents without quality degradation, cost optimization via multi-model strategy, emergent properties (role specialization, voluntary self-abstention, spontaneous hierarchy), failure modes & guardrails.** |

---

### LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/context.md (~115 lines)

**Context management within agentic systems**

| Lines | Section |
|---|---|
| 1–15 | Core mental model: context as capability, five key beliefs |
| 16–69 | Context vs. Memory distinction, storage options (in-memory, file, SQLite, vector DB, Redis) |
| 70–77 | Memory consistency in multi-agent systems, write conflict patterns |
| **78–92** | **Context Contamination During Concurrent Steering: DACS mechanism (lightweight per-agent registries + asymmetric focus isolation), empirical results (90–98.4% steering accuracy, 3.53× context efficiency, 0–14% contamination vs. 28–57% baseline), N-scaling advantage (+20.4 pts at N=5)** |
| 93–115 | Capability degradation thresholds, advanced patterns (progressive disclosure, payload model, context loading) |

---

### LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agent-teams.md (~380 lines)

**Complete reference for Claude Code Agent Teams — the native multi-agent peer coordination primitive**

| Lines | Section |
|---|---|
| 1–35 | What it is and why it matters: peer sessions vs. hub-and-spoke, the problem it solves |
| 36–90 | Architecture: team lead, teammates, shared task list, mailbox, storage paths |
| 91–145 | When to use: vs. single session, vs. subagents, decision matrix by scenario |
| 146–185 | Setup: enable flag, version requirement, display modes (in-process vs. split panes) |
| 186–240 | Controlling the team: creating teams, assigning tasks, direct messaging, plan approval, shutdown |
| 241–320 | Quality gates via hooks: TeammateIdle, TaskCreated, TaskCompleted — exit codes, shell examples |
| 321–360 | Context and communication: what teammates receive, spawn prompt design, what they don't inherit |
| 361–380 | Subagent definitions as blueprints, token costs, limitations, troubleshooting |

---

### LEARNING/AGENTS_AND_SYSTEMS/ai-system-design/ai-system-design.md (919 lines)

**Architectural patterns for AI systems at scale**

| Lines | Section |
|---|---|
| 1–145 | Design thinking for AI systems |
| 146–412 | 11 core design patterns (agents, RAG, classification, content generation, etc.) |
| **253–267** | **Reliability boundary on multi-agent architectures: When delegation fails (Ao et al. 2026). Information loss in agent-to-orchestrator handoffs. Asymmetric information as prerequisite for distributed coordination** |
| 413–678 | Data pipelines: ingestion, processing, retrieval, monitoring |
| 679–834 | Observability: logging, tracing, alerting, metrics |
| 835–1000 | Scalability: caching, batching, parallel processing, resource management |
| 776–799 | MLOps Engineering Patterns: reproducibility, hyperparameter optimization |
| 800–919 | Production Safety Rules: 6 non-negotiable rules (port stability, database safety, feature completeness, infrastructure lock, dependency safety, pattern following) + Verification Paradox |

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
| **NEW:** 14 (ext.) | **Collective Skill Evolution (SkillClaw, Ma et al. 2026): trajectory aggregation across users → autonomous evolver → shared repository; failure modes (domain mismatch, skill bloat, degradation); relationship to individual instincts** |

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

### LEARNING/PRODUCTION/evaluation/evaluation.md (1,050+ lines)

**Evaluating AI systems in production—metrics, frameworks, best practices**

| Lines | Section |
|---|---|
| 1–145 | Why evaluation is hard: probabilistic outputs, no ground truth, measurement bias |
| 146–289 | 3-level eval stack: offline / online / human |
| 290–412 | What you're actually measuring: faithfulness, relevance, coherence, hallucination rate |
| 413–598 | LLM-as-judge with all 4 bias types and mitigations (GPT-4 >80% human agreement) |
| 599–756 | **External Metrics Over LLM Judgment**: Empirical fit / parsimony / accuracy as independent evaluators; pattern from AutoTheory research automation system |
| 757–914 | RAG evaluation via Ragas framework (4 metrics: retrieval, relevance, etc.) |
| 915–1047 | Agent evaluation (task completion, trajectory quality) |
| 1048–1203 | Benchmarks + contamination risk (39.4% drop on uncontaminated) |
| 1204–1362 | Framework comparison table (Ragas, DeepEval, Braintrust, etc.) |
| **NEW:** 14. | Evaluation Patterns: checkpoint-based vs. continuous evals, pass@k vs. pass^k metrics |
| **NEW:** 15. | Eval-Driven Development (EDD): evals BEFORE implementation, cost-benefit analysis (pays for itself on 2nd similar feature) |
| **NEW:** 16. | **External Metrics Anchoring**: Replace LLM self-assessment with domain-specific numerical criteria (empirical fit, prediction accuracy, parsimony) for discovery and generation tasks |

---

### LEARNING/PRODUCTION/ai-security/ai-security.md (1,260+ lines)

**Complete AI security threat model and defense strategies**

| Lines | Section |
|---|---|
| 1–62 | Why AI agents require different security mindset |
| 63–145 | Governance framework for AI agents |
| 146–289 | OWASP LLM Top 10 threat landscape |
| 290–262 | Deep dives: key attack vectors (injection, poisoning, model theft, agent-specific, RAG-specific) |
| **201–262** | **RAG-Specific Attack Surfaces: 4 primary surfaces (pre-retrieval corruption, retrieval-time manipulation, downstream context exploitation, knowledge exfiltration) with defense strategies; distinction between RAG risks vs. inherent LLM vulnerabilities** |
| 321–576 | Core security principles: Zero Trust, least privilege, defense in depth |
| 577–755 | Identity & Access Management for agents |
| 756–903 | AI Firewall / Gateway pattern |
| 904–1058 | Sandboxing: execution isolation (4 tiers) |
| 1059–1208 | Monitoring, detection, DevSecOps |
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

**New Structure (as of 2026-04-03):** Playbooks follow a consistent pattern:
1. **Decision tree** routes you to the right primary playbook (agent, RAG, chatbot, or prompting)
2. **"Add Optional Capabilities"** section cross-references other playbooks for secondary features
3. **Phases** contain **3–5 granular steps** (10–30 min each)
4. **Every step** includes: KB reference (file + exact lines) + action + validation checklist
5. **No time estimates** (redundant with AI assistance)

See [playbooks/README.md](future-reference/playbooks/README.md) for the complete structure explanation.

---

**Primary Pattern Playbooks** (Follow new structure)

| Playbook | Primary Pattern | When to Use | Structure |
|----------|---|---|---|
| [**building-ai-agents.md**](future-reference/playbooks/building-ai-agents.md) | Multi-step autonomous task | Research agent, workflow automation, data processing | Decision tree → 5 phases → Step-by-step with KB citations |
| [**building-rag-pipelines.md**](future-reference/playbooks/building-rag-pipelines.md) | Document retrieval & ranking | Search internal docs, extract structured info, question-answering | (To be enhanced with new structure) |
| [**building-chatbots.md**](future-reference/playbooks/building-chatbots.md) | Real-time conversation | User interaction, multi-turn state, conversational UI | (To be enhanced with new structure) |
| [**writing-production-prompts.md**](future-reference/playbooks/writing-production-prompts.md) | Single LLM call | Classification, generation, summarization, one-shot tasks | (To be enhanced with new structure) |

---

**Specialized & Meta Playbooks** (Existing structure)

| Playbook | Best for | Key Topics |
|----------|----------|-----------|
| [**magnum-opus.md**](future-reference/playbooks/magnum-opus.md) | **All projects (master workflow)** | **9-phase scaffold workflow: intake → domain research → classification → spec + pre-flight → harness design → methodology → capability selection → scaffold output → eval baseline. Used by `/cook` skill. Routes to KB, never contains KB content.** |
| [**meta-workflow.md**](future-reference/playbooks/meta-workflow.md) | **All projects (meta-layer)** | **6 phases (ideation → spec → design → build → harden → deploy → operate), decision matrices, failure taxonomy, playbook selector** |
| [autonomous-agent-loops.md](future-reference/playbooks/autonomous-agent-loops.md) | Choosing loop patterns | Sequential, iterative, infinite, RFC-DAG, REPL, cleanup with quality gates |
| [multi-agent-orchestration.md](future-reference/playbooks/multi-agent-orchestration.md) | Building multi-agent systems | 13-agent model, parallel execution, context isolation (DACS contamination prevention), failure recovery, Claude Code Agent Teams deployment patterns |
| [cost-optimized-llm-workflows.md](future-reference/playbooks/cost-optimized-llm-workflows.md) | Cost control | Model routing (Haiku/Sonnet/Opus), budget enforcement, retry strategies |
| [building-professional-websites.md](future-reference/playbooks/building-professional-websites.md) | Website builds | Professional website architecture and patterns |
| [building-ai-saas.md](future-reference/playbooks/building-ai-saas.md) | AI-powered SaaS products | Pre-flight framework, 4 failure modes, Phase 0–3 build sequence, patterns worth repeating |
| [production-agent-patterns.md](future-reference/playbooks/production-agent-patterns.md) | Production agent deployment | HITL approval workflows (sync dev + async webhook), stateful orchestration, credential vaults, prompt versioning, event-driven integration |
| [project-example-support-classifier.md](future-reference/playbooks/project-example-support-classifier.md) | Worked example | End-to-end support ticket classifier build |
| [project-template.md](future-reference/playbooks/project-template.md) | New projects | General AI project template structure |

---

---

### future-reference/agent-catalog/ (24 agents)

**Role definitions for the Sequential protocol agent pool**

See [agent-catalog/CATALOG.md](future-reference/agent-catalog/CATALOG.md) for the flat index (name | self-select when | what it produces).

| Category | Agents |
|---|---|
| `core/` | architect, planner, code-reviewer, doc-updater |
| `quality/` | security-reviewer, tdd-guide, performance-optimizer, harness-optimizer, refactor-cleaner, build-error-resolver, go-reviewer, python-reviewer, typescript-reviewer |
| `design/` | ux-researcher, ui-designer, design-system-architect, accessibility-reviewer, product-designer |
| `product/` | product-strategist, spec-writer, technical-writer |
| `ai-specialist/` | context-architect, eval-designer, prompt-engineer, kb-navigator |
| `meta/` | chief-of-staff, loop-operator |

Agents self-select roles via the Sequential protocol — not pre-assigned. See `agent-catalog/README.md` for the self-selection process and `agent-catalog/SOUL-TEMPLATE.md` for the functional personality template.

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

Last updated: 2026-04-03 (enhanced playbooks with decision trees, step-by-step structure, KB citations; added playbooks/README.md explaining new format; building-ai-agents.md now has complete Phase 1 with validation)
