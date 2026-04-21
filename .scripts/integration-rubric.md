# KB Integration Rubric — CI Version

Used by the automated deep-dive pipeline. Distilled from kb-paper-integration skill.

## TRIAGE — Quality Gate and Routing (Call 1)

Run these gates in order. Each sets a confidence ceiling. Use the lowest ceiling that applies.

1. **Is this a mechanism, not an application?**
   - MECHANISM: generalizable pattern, insight into WHY something works or fails across systems
   - APPLICATION: domain-specific deployment, infrastructure tuning, benchmark chasing
   - If application with no extractable mechanism: confidence ≤ 0.50, skip integration

2. **Does it generalize?**
   - Would this pattern apply to other agents/prompts/systems beyond this paper's specific domain?
   - Yes → proceed. No → confidence ≤ 0.55

3. **Does it fill a gap or contradict existing KB content?**
   - Carefully read what the KB-INDEX says the target section already covers.
   - **Confirmatory** (agrees with, extends, or confirms what the KB already says): confidence ≤ 0.72
   - **Gap-filling** (topic genuinely not covered in KB): confidence ≥ 0.85
   - **Contradictory** (overturns or challenges a specific KB assumption): confidence ≥ 0.88
   - Mentions the topic without new insight: confidence ≤ 0.55

4. **Deployment relevance — would this change how a practitioner builds or deploys AI this week?**
   - "Would an engineer or PM building an AI agent, RAG pipeline, or evaluation system make a different decision after reading this?"
   - YES — directly changes prompting strategy, agent design, evaluation approach, or deployment pattern: add +0.03 to confidence (subject to ceiling)
   - NO — primarily of academic interest, no near-term action: no change; if high novelty but low deployment relevance, cap confidence at 0.82

**Scoring discipline:** Most papers are confirmatory (gate 3). Force yourself to honestly check KB-INDEX before scoring. If you are not sure whether a topic is covered, treat it as confirmatory (≤ 0.72). Reserve ≥ 0.85 strictly for papers where you can name a specific KB gap or assumption this paper changes.

**All gates pass:** 0.80–0.88 for strong mechanism with deployment relevance; 0.88–0.95 for genuine gap-filling or contradiction with direct practitioner implications.

**No-match fallback:** If the paper doesn't fit any routing row below, set confidence ≤ 0.50 and leave kb_routing.primary_file as an empty string.

## Triage Output Schema (Call 1 — no draft text)

Return ONLY valid JSON:
```
{
  "paper_id": "string",
  "title": "string",
  "html_available": boolean,
  "quality_gate": {
    "is_mechanism": boolean,
    "generalizes": boolean,
    "fills_gap": boolean,
    "deployment_relevant": boolean,
    "confidence": float,
    "reasoning": "string (1-2 sentences: which gate drove the score and why)"
  },
  "kb_routing": {
    "primary_file": "string (relative path from repo root)",
    "section_anchor": "string (exact section heading text from KB file)",
    "secondary_file": null or "string",
    "secondary_section_anchor": null or "string"
  },
  "playbook_routing": {
    "applies": boolean,
    "playbook_file": null or "string",
    "section_anchor": null or "string"
  },
  "magnum_opus_flag": null or "string",
  "key_findings": "string (2-3 sentences, empirical numbers where available)",
  "highlights_blurb": "string (2 sentences — what it found and why a practitioner should care)"
}
```

## KB Section Routing (primary destination)

| Paper focus | Primary KB file |
|---|---|
| Prompting technique, few-shot, output control | LEARNING/FOUNDATIONS/prompt-engineering/prompt-engineering.md |
| RAG, retrieval, context selection, context window | LEARNING/FOUNDATIONS/context-engineering/context-engineering.md |
| Reasoning, CoT, planning, thinking effort | LEARNING/FOUNDATIONS/reasoning-llms/reasoning-llms.md |
| Multimodal, vision-language, audio, video | LEARNING/FOUNDATIONS/multimodal/multimodal.md |
| Emerging architectures, SSM, MoE, tokenization | LEARNING/FOUNDATIONS/emerging-architectures/emerging-architectures.md |
| Agent architecture, tool use, orchestration, HITL | LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md |
| Multi-agent systems, coordination, self-organizing | LEARNING/AGENTS_AND_SYSTEMS/agentic-engineering/agentic-engineering.md |
| Claude Agent SDK patterns, Task tool, subagents | LEARNING/AGENTS_AND_SYSTEMS/agent-sdk/agent-sdk.md |
| MCP, external tools, API integration | LEARNING/AGENTS_AND_SYSTEMS/mcp/mcp.md |
| Skills, reusable instruction patterns | LEARNING/AGENTS_AND_SYSTEMS/skills/skills.md |
| Evaluation, benchmarking, LLM-as-judge | LEARNING/PRODUCTION/evaluation/evaluation.md |
| Security, jailbreak, adversarial, prompt injection | LEARNING/PRODUCTION/ai-security/ai-security.md |
| Fine-tuning, LoRA, RLHF, DPO | LEARNING/PRODUCTION/fine-tuning/fine-tuning.md |
| RL alignment, GRPO, reward hacking, RLVR | LEARNING/PRODUCTION/rl-alignment/rl-alignment.md |
| Inference, latency, quantization, serving | LEARNING/PRODUCTION/inference-optimization/inference-optimization.md |
| Specification, requirements, acceptance criteria | LEARNING/PRODUCTION/specification-clarity/specification-clarity.md |

## Secondary Section Rules

Only add a secondary section if:
- The finding is DIRECTLY actionable there (not just "mentioned")
- You can write 2-3 distinct, non-redundant sentences for the secondary
- The two insights are genuinely different angles (not the same point restated)

## Section Anchor Format

The `section_anchor` field must be an EXACT QUOTE of a section heading from the target KB file — the text after `## ` or `### `. Examples:
- "Special Case: Function-Calling Agents and the Reasoning Paradox"
- "LLM-as-a-Judge"
- "Reward Hacking and the Alignment Tax"

Use KB-INDEX section descriptions to identify which heading is relevant, then quote the heading text exactly as it appears in the file.

## Playbook Routing

Update a playbook ONLY when the paper has PRACTICAL, IMPLEMENTABLE methodology:
- Code patterns, deployment checklists, validation metrics, step-by-step procedures
- NOT: theoretical findings alone (those go in KB docs only)

Relevant playbooks:
- `future-reference/playbooks/building-ai-agents.md` — agent build patterns
- `future-reference/playbooks/building-rag-pipelines.md` — RAG methodology
- `future-reference/playbooks/multi-agent-orchestration.md` — multi-agent deployment
- `future-reference/playbooks/cost-optimized-llm-workflows.md` — cost/efficiency
- `future-reference/playbooks/production-agent-patterns.md` — HITL, stateful agents

## Magnum Opus Flag

Flag for magnum-opus update if the paper introduces a pattern that should inform project-level decisions (not just KB reference). Phrase as: "Phase N ([phase name]) — [one sentence on what should be added/updated]"

## DRAFT — KB Text Generation (Call 2)

Called only for papers with confidence ≥ 0.75. You will receive:
- The triage result (routing, key_findings, highlights_blurb)
- The existing content of the target KB section (what's already there)
- The paper content

Your job: write draft_kb_text that adds genuinely new insight without restating what's already in the section.

KB writing standards:
- Plain English first, define jargon on first use
- Narrative prose before bullets or tables
- Concrete examples with real numbers from the paper
- No placeholder text, no hedge phrases ("this suggests that...")
- 200–500 words for primary, 100–200 for secondary

Draft output schema (Call 2):
```
{
  "draft_kb_text": "string",
  "draft_kb_text_secondary": null or "string",
  "draft_playbook_text": null or "string"
}
```
