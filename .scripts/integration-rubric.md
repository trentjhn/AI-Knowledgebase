# KB Integration Rubric — CI Version

Used by the automated deep-dive pipeline. Distilled from kb-paper-integration skill.

## Quality Gate (run first)

Each gate sets its own confidence ceiling when it fails. Use the lowest ceiling that applies.
If all gates pass, set confidence based on novelty: 0.80–0.90 for strong mechanism, 0.90–0.95 for gap-filling or contradiction.

1. **Is this a mechanism, not an application?**
   - MECHANISM: generalizable pattern, insight into why something works/fails
   - APPLICATION: domain-specific deployment, infrastructure tuning, benchmark chasing
   - If application with no extractable mechanism: confidence ≤ 0.50, skip integration

2. **Does it generalize?**
   - Would this pattern apply to other agents/prompts/systems beyond the paper's domain?
   - Yes → proceed. No → confidence ≤ 0.55

3. **Does it fill a gap or contradict existing KB content?**
   - Read KB-INDEX to see what the target section already covers
   - Duplicates existing content without new insight → confidence ≤ 0.55
   - Fills gap (topic not yet covered) → high value
   - Contradicts existing assumption (e.g., paper shows CoT doesn't help in domain X, while KB states CoT helps generally) → high value

**No-match fallback:** If the paper doesn't fit any routing row below, set confidence ≤ 0.50 and leave kb_routing.primary_file as an empty string. The integration script will move it to proposals-only.

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

The `section_anchor` field must be an EXACT QUOTE of a section heading from the target KB file — the text that appears after `## ` or `### ` in that file. Examples:
- "Special Case: Function-Calling Agents and the Reasoning Paradox"
- "LLM-as-Judge: Using AI to Evaluate AI"
- "Reward Hacking and the Alignment Tax"

Use KB-INDEX section descriptions to identify the right heading. The integration script searches for this heading literally in the file.

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

## Output Format

Return ONLY valid JSON matching this schema exactly:
{
  "paper_id": "string",
  "title": "string",
  "html_available": boolean,
  "quality_gate": {
    "is_mechanism": boolean,
    "generalizes": boolean,
    "fills_gap": boolean,
    "confidence": float
  },
  "kb_routing": {
    "primary_file": "string (relative path from repo root)",
    "section_anchor": "string (exact section heading text from KB file)",
    "secondary_file": null or "string",
    "secondary_section_anchor": null or "string (exact section heading text from secondary KB file)"
  },
  "playbook_routing": {
    "applies": boolean,
    "playbook_file": null or "string",
    "section_anchor": null or "string"
  },
  "magnum_opus_flag": null or "string",
  "key_findings": "string (2-3 sentences, empirical numbers where available)",
  "draft_kb_text": "string (full prose, KB writing standards: plain English first, define jargon, narrative before bullets, concrete examples)",
  "draft_kb_text_secondary": null or "string (same writing standards, for the secondary KB file if applicable)",
  "draft_playbook_text": null or "string",
  "highlights_blurb": "string (2 sentences — what it found and why a practitioner should care)"
}
