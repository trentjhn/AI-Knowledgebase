# /cook Skill Reference

The `/cook` skill is the executable companion to `magnum-opus.md`.
It lives at `~/.claude/skills/cook/SKILL.md` (system-level, available
in all sessions).

## What It Does

Traverses the three-layer architecture (workflow hub + knowledge layer
+ capability layer) and writes a complete project scaffold to disk.
Guides the user through 6 phases (0 through 5), asking targeted questions
grounded in KB best practices at each gate.

## When to Use

Starting any new project. Invoke with `/cook` or describe a new project
idea — the skill triggers on: "new project", "start building", "scaffold
a project for", "let's build", "I want to build".

## Output

See `docs/plans/2026-04-12-magnum-opus-design.md` for the complete
scaffold structure. Short version: CLAUDE.md + AGENTS.md + SOUL.md +
README.md + .claude/agents/ + .claude/skills/ + docs/kb-references.md
+ docs/plans/design.md + docs/plans/implementation.md.

## Architecture

The skill reads `magnum-opus.md` at runtime — it does not contain
workflow logic itself. Minor content changes to the hub doc do not
require skill updates. Skill updates are only needed when:
- Layer interfaces change (new phase added to magnum-opus.md)
- New scaffold output files are added to the done-gate checklist
- New catalog directories are added that the skill needs to traverse

## Maintenance

Update `~/.claude/skills/cook/SKILL.md` when the scaffold structure changes.
Update `magnum-opus.md` when phase logic or gate conditions change.
These are separate concerns in separate files by design.
