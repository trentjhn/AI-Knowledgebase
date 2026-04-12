# Agent Catalog

A curated library of agent role definitions for Claude Code projects. Agents self-select roles via the Sequential protocol — they are not pre-assigned. This catalog is the available pool.

## Structure

```
agent-catalog/
├── CATALOG.md          ← START HERE — flat index for agent self-selection
├── README.md           ← this file
├── SOUL-TEMPLATE.md    ← functional personality template
├── core/               ← every project (architect, planner, code-reviewer)
├── quality/            ← hardening (security, testing, performance)
├── design/             ← UX/UI — first-class, not optional
├── product/            ← PM layer (strategy, spec, writing)
├── ai-specialist/      ← AI/agentic projects only
└── meta/               ← coordination agents
```

## How Agents Use This Catalog

1. Read `CATALOG.md` in full — see all available roles
2. Review what predecessor agents have already produced
3. Self-select the most complementary role not yet covered
4. Load that agent's definition file for full instructions
5. Announce role selection before beginning work

## The soul.md Convention

Every project scaffolded with `/cook` includes a `SOUL.md` at its root. This file defines the agent's functional personality — character traits that improve performance.

**CLAUDE.md must explicitly reference it:**
```markdown
## Identity
Read SOUL.md before anything else. It defines this agent's character
and values. These are non-negotiable and override default behavior.
```

**SOUL.md is not:**
- Aesthetic decoration ("I love a challenge! 🚀")
- Catchphrases
- Emoji usage
- Over-enthusiasm

**SOUL.md is:**
- Behavioral constraints that reduce variance
- Values that persist regardless of role or task
- Decision principles for ambiguous situations
- The agent's consistent character under pressure

See `SOUL-TEMPLATE.md` for the template.

## Index-First Convention

When adding a new agent to this catalog:
1. Write the `CATALOG.md` entry FIRST (catalog-first convention)
2. Then create the agent definition file
3. Never create a file without a corresponding CATALOG.md entry

This ensures the catalog is never stale and agents can always discover new roles.
