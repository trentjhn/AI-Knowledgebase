#!/bin/bash
# UserPromptSubmit hook — Forced Skill Evaluation Template
#
# WHAT IT DOES:
#   Before every prompt, forces Claude to explicitly evaluate each installed
#   skill (YES/NO with reason) and invoke relevant ones before implementing.
#   Checks both user-level (~/.claude/skills/) and project-level (.claude/skills/).
#   Exits silently if no skills are found — zero overhead on bare projects.
#
# WHY:
#   Passive description matching achieves ~20% skill activation rate.
#   This hook raises it to ~84% via a commitment sequence that makes
#   skipping activation syntactically awkward before implementation.
#   Source: scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably
#
# GLOBAL INSTALLATION (recommended — fires on every project):
#   mkdir -p ~/.claude/hooks
#   cp skill-activation.sh ~/.claude/hooks/skill-activation.sh
#   chmod +x ~/.claude/hooks/skill-activation.sh
#   # Then merge settings-template.json into ~/.claude/settings.json
#
# PER-PROJECT INSTALLATION:
#   mkdir -p .claude/hooks
#   cp skill-activation.sh .claude/hooks/skill-activation.sh
#   chmod +x .claude/hooks/skill-activation.sh
#   # Then merge settings-template.json into .claude/settings.json
#
# SKILL SCOPES (both are checked, project takes precedence on name conflicts):
#   User-level:    ~/.claude/skills/        — always available, all projects
#   Project-level: <repo-root>/.claude/skills/ — this project only
#
# CUSTOMIZATION:
#   SKILL_HOOK_DESCRIPTIONS=true  — include trigger descriptions (verbose but helpful)
#   Default: false (skill names only)

SHOW_DESCRIPTIONS="${SKILL_HOOK_DESCRIPTIONS:-false}"

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
USER_SKILLS_DIR="$HOME/.claude/skills"
PROJECT_SKILLS_DIR="$REPO_ROOT/.claude/skills"

# Build deduplicated skill list — project-level takes precedence over user-level
# (bash 3.2 compatible: no associative arrays)
seen=""
SKILL_LINES=""

for skills_dir in "$PROJECT_SKILLS_DIR" "$USER_SKILLS_DIR"; do
    [ -d "$skills_dir" ] || continue
    for skill_dir in "$skills_dir"/*/; do
        [ -f "$skill_dir/SKILL.md" ] || continue
        skill_name=$(basename "$skill_dir")

        # Skip duplicates (project-level was processed first)
        echo "$seen" | grep -qx "$skill_name" && continue
        seen="$seen
$skill_name"

        if [ "$SHOW_DESCRIPTIONS" = "true" ]; then
            desc=$(grep -m1 "^description:" "$skill_dir/SKILL.md" 2>/dev/null \
                   | sed 's/^description:[[:space:]]*//' \
                   | cut -c1-70)
            if [ -n "$desc" ]; then
                SKILL_LINES="$SKILL_LINES\n  - $skill_name: $desc"
            else
                SKILL_LINES="$SKILL_LINES\n  - $skill_name"
            fi
        else
            SKILL_LINES="$SKILL_LINES\n  - $skill_name"
        fi
    done
done

# Exit silently if no skills found — no noise on bare projects
[ -z "$SKILL_LINES" ] && exit 0

cat <<EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MANDATORY SKILL EVALUATION — DO NOT SKIP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Installed skills:
$(echo -e "$SKILL_LINES")

STEP 1 — EVALUATE: For each skill above, state YES or NO with a one-line reason.
STEP 2 — ACTIVATE: For every YES, call Skill(skill-name) tool immediately.
STEP 3 — IMPLEMENT: Only after Steps 1 and 2 are complete.

CRITICAL: Evaluation is WORTHLESS without activation.
If a skill is YES → you MUST invoke Skill() before writing any code.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF
