# PRODUCTION — Quality, Security & Optimization (Advanced)

Shipping reliable, secure, well-measured AI systems. Prerequisites: Complete [FOUNDATIONS/](../FOUNDATIONS/) and [AGENTS_AND_SYSTEMS/](../AGENTS_AND_SYSTEMS/) first.

---

## Topics

### [**Evaluation**](evaluation/)
**1,000+ lines** — Measuring AI system quality in production

- Why evaluation is hard: probabilistic outputs, no ground truth, measurement bias
- 3-level eval stack: offline (before prod) / online (in prod) / human review
- What you're actually measuring: faithfulness, relevance, coherence, hallucination rate
- LLM-as-judge with bias mitigation (GPT-4 achieves >80% human agreement)
- RAG evaluation via Ragas framework (4 specific metrics)
- Agent evaluation: task completion, trajectory quality
- Benchmarks and contamination risk (39.4% accuracy drop on uncontaminated data)
- Framework comparison table: Ragas, DeepEval, Braintrust, Promptfoo, LangSmith
- Eval-Driven Development (EDD): write evals BEFORE implementation, costs pay for themselves on 2nd similar feature

**Start with:** "Why evaluation is hard" and 3-level eval stack sections

---

### [**AI Security**](ai-security/)
**1,100+ lines** — Threat models, defenses, and hardening for AI agents

- Why AI agents require different security thinking
- Governance framework for AI systems
- OWASP LLM Top 10 threat landscape
- Deep dives: prompt injection, data poisoning, model extraction, etc.
- Zero Trust architecture for AI
- Identity & Access Management for agents
- AI Firewall / Gateway pattern
- Sandboxing: 4 execution isolation tiers
- Monitoring and detection strategies
- Agent configuration security: transitive injection, tool allowlisting, credential scoping, MCP vetting

**Start with:** "Why AI agents require different security" and OWASP Top 10 sections

---

### [**Specification Clarity**](specification-clarity/)
**512 lines** — Writing unambiguous AI specs that implement correctly

- 7-property framework for clear specs
- Types of ambiguity: scope, definition, success, behavior, edge cases
- BDD (Behavior-Driven Development) acceptance criteria for AI
- Constraint architecture and decomposition
- Spec anti-patterns to avoid
- How clear specs prevent misimplementation

**Start with:** 7-property framework and ambiguity types

---

### [**Fine-tuning**](fine-tuning/)
**586 lines** — When and how to fine-tune, costs, failure modes

- Fine-tuning vs. prompting vs. RAG decision framework
- Fine-tuning spectrum: pre-training → instruction tuning → RLHF/DPO → task fine-tuning
- Instruction tuning (FLAN, InstructGPT)
- RLHF and DPO as alternatives
- PEFT/LoRA: 10,000× parameter reduction
- QLoRA: quantization tricks for efficient fine-tuning
- Data requirements (50-100k examples)
- Cost/infrastructure breakdown
- Alignment tax and catastrophic forgetting risks

**Start with:** Decision framework and fine-tuning spectrum sections

---

## Learning Path

1. **Prerequisites:** [FOUNDATIONS/](../FOUNDATIONS/) and [AGENTS_AND_SYSTEMS/](../AGENTS_AND_SYSTEMS/)
2. **Start:** Evaluation (measure quality before shipping)
3. **Then:** AI Security (protect against threats)
4. **Then:** Specification Clarity (communicate intent precisely)
5. **As needed:** Fine-tuning (optimize models for specific tasks)

---

## How These Connect

**Evaluation** answers: "How do I know if my system works?"
**AI Security** answers: "How do I protect my system from attacks?"
**Specification Clarity** answers: "How do I describe requirements without ambiguity?"
**Fine-tuning** answers: "When should I train vs. prompt vs. retrieve?"

Use them together when shipping production systems.

---

## Quick Reference

| Topic | Best For | Read Time |
|-------|----------|-----------|
| Evaluation | Measuring quality, Eval-Driven Development | 3-4 hours |
| AI Security | Threat modeling, hardening agents | 3-4 hours |
| Specification Clarity | Clear requirements, preventing bugs | 1-2 hours |
| Fine-tuning | Training decisions, cost analysis | 2 hours |

---

**You're now ready to build and ship production AI systems.** Use [FUTURE-REFERENCE/](../../future-reference/) for practical playbooks and templates.

Last updated: 2026-03-08
