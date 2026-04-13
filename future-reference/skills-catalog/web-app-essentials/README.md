# Web App Essentials — Skill Manifest

Curated skill set for building and shipping high-quality web apps and software with AI. Not a minimal set — a powerful set. These are guardrails and force multipliers, not overhead.

**What this is:** A manifest of which skills to install, and from where. No skill files live here — they stay at their canonical paths in the catalog. Copy from there, not from here.

---

## Install (new machine or new project)

```bash
# From AI-Knowledgebase root — copy all essentials to global Claude skills
CATALOG=future-reference/skills-catalog
DEST=~/.claude/skills

cp -r $CATALOG/workflow/brainstorming/      $DEST/
cp -r $CATALOG/workflow/planning/           $DEST/
cp -r $CATALOG/workflow/smart-commit/       $DEST/
cp -r $CATALOG/workflow/deslop/             $DEST/
cp -r $CATALOG/workflow/session-handoff/    $DEST/
cp -r $CATALOG/production/pre-ship/         $DEST/
cp -r $CATALOG/production/deployment-patterns/ $DEST/
cp -r $CATALOG/design/frontend-design/      $DEST/
cp -r $CATALOG/design/ui-ux-pro-max/        $DEST/
cp -r $CATALOG/engineering/security-review/ $DEST/
```

---

## The Skills

### Tier A — Guardrails (every project, no exceptions)

| Skill | What it does | When it fires |
|---|---|---|
| `brainstorming` | Explores intent before implementation | "let's build", "add feature", any creative work |
| `planning` | Spec before code — the biggest quality lever | After design, before writing code |
| `smart-commit` | Quality gates + conventional commits | "commit", "save changes", ready to commit |
| `deslop` | Removes AI-generated bloat and over-engineering | "clean up", "simplify", before PR |
| `pre-ship` | Security + database + infrastructure + monitoring gate | "ship", "deploy", "going live", "ready to launch" |

### Tier B — Web/App Power Tools

| Skill | What it does | When it fires |
|---|---|---|
| `deployment-patterns` | CI/CD setup, Docker, blue-green/canary, health checks, rollback | "deploy", "CI/CD", "Dockerize", "production setup" |
| `frontend-design` | Distinctive, production-grade UI — avoids generic AI aesthetics | "build UI", "component", "page", "frontend" |
| `ui-ux-pro-max` | Full design system generation: Tailwind config, globals.css, components | "design system", "component library", "UI setup" |
| `security-review` | Security audit before production exposure | "security", "auth", "before PR", "production" |
| `session-handoff` | Structured handoff for complex multi-session builds | "continue later", "save progress", "pick up" |

---

## For cook

When `/cook` runs and project type = web app, Phase 6 should select all Tier A guardrails plus the Tier B skills relevant to the project scope. This manifest is the reference for what "web app" means in that context.

---

## Keeping This Current

When a new skill earns a spot here:
1. Add it to the table above with path and trigger description
2. Add the `cp` command to the install block
3. Add a CATALOG.md entry for the skill first (catalog-first convention)

When a skill is removed or superseded: update both the table and the install block together.
