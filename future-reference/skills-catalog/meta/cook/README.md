# /cook Skill — Install Guide

The `/cook` skill runs the magnum-opus workflow to scaffold any new project.

## Install

```bash
# 1. Copy the skill to your Claude Code skills directory
cp -r /path/to/AI-Knowledgebase/future-reference/skills-catalog/meta/cook ~/.claude/skills/

# 2. Open the skill and update KB_ROOT
# Find every instance of /path/to/your/AI-Knowledgebase
# Replace with your actual KB clone path (e.g. /Users/yourname/AI-Knowledgebase)
```

One path change unlocks the whole skill.

## Dependencies

| Dependency | Install |
|---|---|
| AI Knowledgebase | Clone `trentjhn/AI-Knowledgebase` |
| `last30days` skill | `https://github.com/mvanhorn/last30days-skill` — install from ClawHub |

## What It Does

Runs the 9-phase magnum-opus workflow interactively:

```
Phase 0    → Intake (problem capture + KB routing)
Phase 0.5  → Domain research (last30days)
Phase 1    → Project classification + topology decision
Phase 1.5  → Spec writing + pre-flight failure mode check
Phase 2    → Harness design (Four Pillars + context + memory + topology)
Phase 2.5  → Build methodology selection
Phase 3    → Agent + skill + prompt catalog traversal
Phase 4    → Scaffold written to disk
Phase 5    → Eval criteria + threat model baseline
```

Output: a complete project directory with CLAUDE.md, SOUL.md, AGENTS.md,
docs/plans/design.md, docs/plans/implementation.md, and pre-selected
agents and skills from the catalog.

## The Hub Document

The skill reads `magnum-opus.md` at runtime for its decision logic.
Minor updates to the hub don't require skill updates.
Only update this skill when the scaffold output structure changes.
