# ArXiv Automated KB Integration Pipeline — Design

**Date:** 2026-04-19
**Status:** Approved, ready for implementation

---

## Problem

The existing ArXiv scraper deposits weekly digests in `raw/arxiv-papers/` but integration into the KB is fully manual. Each paper requires a human to fetch the full paper HTML, apply the integration rubric, write KB text, update KB-INDEX, and commit. This doesn't scale — the KB risks falling behind or becoming stale relative to the research it's meant to track.

---

## Goals

1. **Full automation:** Pipeline runs Friday after the scraper, no human approval gate for high-confidence papers
2. **Deep content analysis:** Fetch full arXiv HTML (methods + results + ablation + conclusion), not abstract-only
3. **Proper KB maintenance:** Every integration updates KB-INDEX, checks playbook routing, marks digest entries
4. **Human-readable weekly summary:** What was added, why it matters, what needs your attention — for learning and to surface skills/workflow integration opportunities
5. **Surgical revertability:** Per-paper commits so any bad integration can be `git revert`ed without touching others

## Non-Goals

- Updating `CLAUDE.md` pattern recognition rubric (too high-risk for automation)
- Updating `future-reference/playbooks/magnum-opus.md` (flagged in summary only — user decides)
- Touching `.sessions/` (local-only, never in CI)

---

## Architecture

```
Friday 8:00am UTC
├── Job 1: arxiv-scraper.py          (exists)
│   └── → raw/arxiv-papers/YYYY-MM-DD.md
│
Friday 8:10am UTC
├── Job 2: arxiv-deep-dive.py        (new)
│   ├── ThreadPoolExecutor: 1 thread per paper
│   │   ├── Fetch arxiv.org/html/{id}
│   │   ├── Extract: methods + results + ablation + conclusion
│   │   ├── Claude API quality gate + routing analysis
│   │   └── Structured proposal per paper
│   └── → raw/arxiv-proposals/YYYY-MM-DD.json
│
Friday 8:20am UTC
└── Job 3: arxiv-integrate.py        (new)
    ├── Read proposals JSON
    ├── Group papers by target KB file
    ├── For each paper (sequential):
    │   ├── Re-read target file (fresh state)
    │   ├── Insert at semantic anchor
    │   ├── Update KB-INDEX
    │   ├── Update playbook if warranted
    │   ├── Mark digest entry as integrated
    │   └── git commit (per paper)
    └── Write weekly summary → git commit
```

---

## New Files

```
.scripts/
├── arxiv-scraper.py         (exists — unchanged)
├── arxiv-deep-dive.py       (new)
├── arxiv-integrate.py       (new)
└── integration-rubric.md    (new — KB routing rubric for CI access)

raw/
├── arxiv-papers/            (exists)
├── arxiv-proposals/         (new directory)
└── arxiv-weekly-summary/    (new directory)

.github/workflows/
└── arxiv-digest.yml         (modified — add 2 new jobs)
```

---

## Job 2: arxiv-deep-dive.py

### Per-paper analysis output (proposals JSON schema)

```json
{
  "paper_id": "2604.15224v1",
  "title": "Context Over Content: Exposing Evaluation Faking in Automated Judges",
  "html_available": true,
  "quality_gate": {
    "is_mechanism": true,
    "generalizes": true,
    "fills_gap": true,
    "confidence": 0.91
  },
  "kb_routing": {
    "primary_file": "LEARNING/PRODUCTION/evaluation/evaluation.md",
    "section_anchor": "after the LLM-as-judge bias types section",
    "secondary_file": null
  },
  "playbook_routing": {
    "applies": false,
    "playbook_file": null,
    "section_anchor": null
  },
  "magnum_opus_flag": "Phase 5 eval baseline — LLM judge assumption may need stakes-neutral framing note",
  "key_findings": "LLM judges inflate scores when detecting high-stakes contextual framing. Stakes signaling overrides content-based evaluation. Contradicts foundational LLM-as-judge assumption.",
  "draft_kb_text": "[Full prose ready to insert, KB writing standards applied]",
  "draft_playbook_text": null,
  "highlights_blurb": "LLM judges inflate scores when they detect high-stakes framing — the mechanism contradicts the foundational assumption of automated eval pipelines."
}
```

### Confidence thresholds

| Confidence | HTML Available | Action |
|---|---|---|
| ≥ 0.80 | Yes | Direct KB integration in Job 3 |
| 0.60–0.79 | Yes | Proposals JSON only, flagged in summary |
| Any | No (abstract only) | Proposals JSON only, capped at 0.60 |
| < 0.60 | — | Skipped, noted in summary as "filtered post deep-dive" |

### HTML section extraction

Target sections: `abstract`, `introduction`, `method`/`methodology`, `experiment`/`results`, `ablation`, `conclusion`, `limitation`

Fallback when HTML unavailable: use abstract from digest. Flag in proposals JSON. Confidence auto-capped at 0.60 (ineligible for direct integration).

### System prompt inputs

The Claude API call receives:
1. `integration-rubric.md` — KB routing decision tree (mechanism vs. application, section mapping, multi-section rules)
2. `KB-INDEX.md` — current KB structure for routing decisions
3. Extracted paper sections — full content of key sections

---

## Job 3: arxiv-integrate.py

### Sequential integration with semantic anchoring

```python
def insert_at_anchor(content: str, anchor: str, new_text: str) -> str:
    """
    Find anchor section heading, locate end of that section
    (next ## heading or end of file), insert new_text before it.
    Fallback: if anchor not found, raise AnchorNotFoundError
    → paper goes to proposals-only, flagged in summary.
    """
```

**Critical constraint:** File is re-read from disk before every insertion. Never insert against a stale in-memory copy — a previous paper's integration may have shifted content.

### KB-INDEX update

After each KB write, the integration agent:
1. Re-reads `KB-INDEX.md`
2. Finds the section entry for the modified file
3. Updates line count and adds new subsection entry with semantic description
4. Writes KB-INDEX back
5. Stages both files together in the same per-paper commit

### Playbook routing

Only triggers when `playbook_routing.applies = true` in proposals JSON. Follows the same semantic anchor + re-read pattern. Playbook writes are included in the same per-paper commit as the KB write.

### Commit format

```
docs(evaluation): Add stakes-signaling bias from "Context Over Content" [2604.15224]

LLM judges inflate scores when detecting high-stakes framing — contradicts
foundational LLM-as-judge assumption. Extends bias types section with new
mechanism and mitigation guidance.
```

### Error handling

| Failure | Behavior |
|---|---|
| Anchor not found in KB file | Skip KB write, add to proposals-only, flag in summary |
| Claude API error on integration | Retry once, then skip + flag |
| Git conflict on push | Fail job, log error — next week's run picks up proposals JSON |
| Playbook write fails | Skip playbook, complete KB write, flag in summary |

---

## Weekly Summary Format

```markdown
# KB Weekly Integration Summary — April 18, 2026

## What was added (3 integrated | 2 proposals only | 1 filtered)

### [Paper Title] [arxiv-id] → kb-file-short.md
**Why it matters:** [2-3 sentences — mechanism insight, what it contradicts or extends]
**Where it lives:** file.md → section (~line N)
**Practical signal:** [1 sentence — how this affects skills, workflows, or decisions]

---

## Proposals only (your review needed)
- [id] [title] — confidence 0.72, HTML unavailable. Review: raw/arxiv-proposals/

## Filtered post deep-dive
- [id] [title] — [reason: domain-specific, no mechanism, etc.]

## Magnum Opus flags (your action needed)
- [Paper] may warrant updating Phase N — [brief reason]

## Playbook updates made
- [playbook-file]: [what was added]
```

---

## GitHub Actions Changes

Extend `.github/workflows/arxiv-digest.yml` with two new jobs:

```yaml
deep-dive-analysis:
  needs: generate-digest
  runs-on: ubuntu-latest
  permissions:
    contents: write
  steps:
    - uses: actions/checkout@v4
      with: { fetch-depth: 0, token: "${{ secrets.GITHUB_TOKEN }}" }
    - uses: actions/setup-python@v5
      with: { python-version: '3.11' }
    - run: pip install requests anthropic beautifulsoup4
    - name: Run deep-dive analysis
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: python .scripts/arxiv-deep-dive.py
    - name: Commit proposals
      run: |
        git config user.email "arxiv-bot@github.com"
        git config user.name "ArXiv Bot"
        git add raw/arxiv-proposals/
        git diff --cached --quiet || (git commit -m "docs(arxiv): add deep-dive proposals $(date +%Y-%m-%d)" && git push origin main)

kb-integration:
  needs: deep-dive-analysis
  runs-on: ubuntu-latest
  permissions:
    contents: write
  steps:
    - uses: actions/checkout@v4
      with: { fetch-depth: 0, token: "${{ secrets.GITHUB_TOKEN }}" }
    - uses: actions/setup-python@v5
      with: { python-version: '3.11' }
    - run: pip install requests anthropic
    - name: Run KB integration
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: python .scripts/arxiv-integrate.py
    # Per-paper commits + final summary commit happen inside the script
```

No new secrets required. New dependency: `beautifulsoup4` (Job 2 only).

---

## Constraints and Deliberate Decisions

- **Semantic anchors, never line numbers** — line numbers drift as files are modified; anchors are intent
- **Per-paper commits** — surgical `git revert` without touching other integrations
- **Magnum-opus: flag only** — too high-risk to automate; surfaces in summary for human action
- **CLAUDE.md: never touched** — meta-layer, automation boundary
- **Abstract-only fallback capped at 0.60** — ensures HTML-unavailable papers never auto-integrate
- **Sequential writes in Job 3** — prevents line-drift and concurrent write conflicts
