# AI Knowledgebase

A unified reference for AI teachings, findings, experiments, and research—organized by learning path and practical use.

*Started: 2026-02-20*

---

## 📚 LEARNING (Core Reference Topics)

Organized by **learning path**: Foundations → Building → Production. Total ~7,800 lines across 10 topics.

### [**FOUNDATIONS**](LEARNING/FOUNDATIONS/) — Start Here
**Understand how LLMs work: prompting, context, reasoning**

~1,400 lines | ~5 hours | Prerequisites: none

- [**Prompt Engineering**](LEARNING/FOUNDATIONS/prompt-engineering/) — 9 core techniques (CoT, self-consistency, APE, ReAct) with research results
- [**Context Engineering**](LEARNING/FOUNDATIONS/context-engineering/) — 4 strategies (Write/Select/Compress/Isolate), 4 failure modes, token budgeting
- [**Reasoning LLMs**](LEARNING/FOUNDATIONS/reasoning-llms/) — When to use reasoning models (o3, Claude 3.7), thinking tiers, design patterns

**→ Next:** Move to [AGENTS_AND_SYSTEMS](LEARNING/AGENTS_AND_SYSTEMS/)

---

### [**AGENTS & SYSTEMS**](LEARNING/AGENTS_AND_SYSTEMS/) — Build (Mid-Level)
**Design and build AI agents and systems**

~4,000 lines | ~9-10 hours | Prerequisites: complete FOUNDATIONS

- [**Agentic Engineering**](LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/) — Four Pillars, Twelve Leverage Points, 6 patterns, tool design, context management
- [**AI System Design**](LEARNING/AGENTS_AND_SYSTEMS/ai-system-design/) — 11 design patterns, data pipelines, observability, scalability
- [**Skills**](LEARNING/AGENTS_AND_SYSTEMS/skills/) — Agent Skills standard, testing, Instincts v2 continuous learning

**→ Next:** Move to [PRODUCTION](LEARNING/PRODUCTION/)

---

### [**PRODUCTION**](LEARNING/PRODUCTION/) — Ship (Advanced)
**Quality, security, optimization: shipping reliable systems**

~2,400 lines | ~8-9 hours | Prerequisites: complete AGENTS_AND_SYSTEMS

- [**Evaluation**](LEARNING/PRODUCTION/evaluation/) — 3-level eval stack, LLM-as-judge, Eval-Driven Development, frameworks
- [**AI Security**](LEARNING/PRODUCTION/ai-security/) — OWASP Top 10, Zero Trust, sandboxing, agent configuration security
- [**Specification Clarity**](LEARNING/PRODUCTION/specification-clarity/) — 7-property framework, BDD acceptance criteria
- [**Fine-tuning**](LEARNING/PRODUCTION/fine-tuning/) — LoRA/QLoRA, RLHF vs DPO, data requirements, costs

**→ Next:** Use [FUTURE-REFERENCE playbooks](future-reference/playbooks/) for practical application

---

## 🎯 CAREER (PM, Interview, Professional Development)

Resources for AI PM roles, interview preparation, and career navigation.

| Section | What's in it |
|---------|-------------|
| [**PM Context**](CAREER/pm-context/) | AI PM role fundamentals, PM frameworks, interview scenarios, AI concepts→PM decision mapping |

---

## 🔧 FUTURE-REFERENCE (Practical Tools & Applied Work)

Ready-to-use guides, templates, and specifications for building AI systems.

| Section | Contents |
|---------|----------|
| [**Playbooks**](future-reference/playbooks/) | 7 practical guides: building agents, chatbots, RAG pipelines, cost optimization, multi-agent orchestration, autonomous loops |
| [**Prompt Catalog**](future-reference/prompt-catalog/) | 16 reusable prompt patterns, example prompts by domain (design, analysis, research) |
| [**Specs**](future-reference/specs/) | Project specifications: PromptArena design system & plan, Zenkai learning system spec |

---

## Quick Navigation

**I'm new to AI and want to learn:**
→ Start with [LEARNING/FOUNDATIONS/prompt-engineering](LEARNING/FOUNDATIONS/prompt-engineering/)

**I understand prompting and want to build agents:**
→ Jump to [LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering](LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/)

**I'm building systems and need production guidance:**
→ Read [LEARNING/PRODUCTION/](LEARNING/PRODUCTION/)

**I want to build something right now:**
→ Browse [FUTURE-REFERENCE/playbooks/](future-reference/playbooks/)

**I need prompt templates:**
→ Check [FUTURE-REFERENCE/prompt-catalog/](future-reference/prompt-catalog/)

**I want the full index:**
→ See [KB-INDEX.md](KB-INDEX.md)

---

## Learning Timeline

| Phase | Content | Time | Outcome |
|-------|---------|------|---------|
| **Phase 1** | [LEARNING/FOUNDATIONS/](LEARNING/FOUNDATIONS/) | 5 hours | Understand LLM prompting, context, reasoning |
| **Phase 2** | [LEARNING/AGENTS_AND_SYSTEMS/](LEARNING/AGENTS_AND_SYSTEMS/) | 9-10 hours | Build functioning AI agents and systems |
| **Phase 3** | [LEARNING/PRODUCTION/](LEARNING/PRODUCTION/) | 8-9 hours | Ship production systems: measurable, secure, reliable |
| **Ongoing** | [FUTURE-REFERENCE/](future-reference/) | As needed | Apply knowledge to real projects |

**Total learning time:** ~22-24 hours (recommend 2-3 hours/week over 8-12 weeks)

---

**Last updated:** 2026-03-08
