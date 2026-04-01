#!/bin/bash
# UserPromptSubmit hook — Forced Skill Evaluation Template
#
# WHAT IT DOES:
#   Before every prompt, forces Claude to explicitly evaluate each installed
#   skill (YES/NO with reason) and invoke relevant ones before implementing.
#   Dynamically reads .claude/skills/ — no hardcoded skill names.
#
# WHY:
#   Passive description matching achieves ~20% skill activation rate.
#   This hook raises it to ~84% by creating a commitment sequence that
#   makes skipping activation syntactically awkward before implementation.
#   Source: scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably
#
# INSTALLATION:
#   1. Copy this file to your project: .claude/hooks/skill-activation.sh
#   2. Make it executable: chmod +x .claude/hooks/skill-activation.sh
#   3. Add to .claude/settings.json (see settings-template.json):
#      "hooks": {
#        "UserPromptSubmit": [{ "hooks": [{ "type": "command",
#          "command": ".claude/hooks/skill-activation.sh" }] }]
#      }
#
# CUSTOMIZATION:
#   Set SKILL_HOOK_DESCRIPTIONS=true in your environment to include skill
#   trigger descriptions in the evaluation list (more verbose, more useful).
#   Default: false (skill names only — less noise per prompt)
#
# NOTES:
#   - Exits silently (exit 0) if no skills are installed — no overhead
#   - Works with both project-level and user-level skill directories
#   - The forced 3-step sequence is what produces reliable activation;
#     rephrasing it as softer guidance will degrade performance

SHOW_DESCRIPTIONS="${SKILL_HOOK_DESCRIPTIONS:-false}"

# Find repo root, fall back to current directory
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SKILLS_DIR="$REPO_ROOT/.claude/skills"

# Exit silently if no skills installed — zero overhead on bare projects
if [ ! -d "$SKILLS_DIR" ] || [ -z "$(ls -A "$SKILLS_DIR" 2>/dev/null)" ]; then
    exit 0
fi

# Build skill list, optionally with descriptions parsed from YAML frontmatter
SKILL_LINES=""
for skill_dir in "$SKILLS_DIR"/*/; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    skill_name=$(basename "$skill_dir")
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

# Exit silently if directory exists but contains no valid SKILL.md files
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
