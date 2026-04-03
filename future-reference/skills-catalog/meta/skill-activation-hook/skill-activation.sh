#!/bin/bash
# UserPromptSubmit hook — Filtered Skill Evaluation
#
# WHAT IT DOES:
#   Reads the user's prompt from stdin, keyword-matches it against each
#   installed skill's description, and only outputs the evaluation block
#   for skills that actually overlap with the current task.
#   Completely silent if no skills match — zero output, zero tokens.
#
# WHY:
#   Passive description matching achieves ~20% skill activation rate.
#   A forced-eval hook with no filtering fires on every message and wastes
#   tokens. This version stays silent on irrelevant prompts and outputs a
#   compact evaluation block only when skills are plausibly relevant.
#   Source: scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably
#
# GLOBAL INSTALLATION (fires on every project):
#   mkdir -p ~/.claude/hooks
#   cp skill-activation.sh ~/.claude/hooks/skill-activation.sh
#   chmod +x ~/.claude/hooks/skill-activation.sh
#   # Add to ~/.claude/settings.json (see settings-template.json)
#
# SKILL SCOPES (both checked, project takes precedence on name conflicts):
#   User-level:    ~/.claude/skills/
#   Project-level: <repo-root>/.claude/skills/
#
# ENV:
#   SKILL_HOOK_DESCRIPTIONS=true  — show trigger descriptions in output
#   SKILL_HOOK_MIN_KEYWORD_LEN=4  — minimum keyword length for matching (default: 5)

SHOW_DESCRIPTIONS="${SKILL_HOOK_DESCRIPTIONS:-false}"
MIN_KEYWORD_LEN="${SKILL_HOOK_MIN_KEYWORD_LEN:-5}"

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
USER_SKILLS_DIR="$HOME/.claude/skills"
PROJECT_SKILLS_DIR="$REPO_ROOT/.claude/skills"

# Read prompt from stdin — UserPromptSubmit sends JSON with user's message
INPUT=$(cat)

# Extract prompt text via python3 (available on macOS/Linux by default)
# Tries multiple field names Claude Code may use; falls back to raw input
PROMPT_TEXT=$(echo "$INPUT" | python3 -c "
import sys, json, re
try:
    d = json.load(sys.stdin)
    text = d.get('prompt') or d.get('message') or d.get('userPrompt') or ''
    if not text:
        # Last resort: concatenate all string values in the JSON
        text = ' '.join(str(v) for v in d.values() if isinstance(v, str))
    print(re.sub(r'[^\w\s]', ' ', text).lower())
except Exception:
    # If JSON parse fails, treat the raw input as text
    print(re.sub(r'[^\w\s]', ' ', sys.stdin.read()).lower())
" 2>/dev/null)

# If prompt extraction completely failed, fall through with empty string
# (all skills will be included as a safe default — same as old behavior)
PROMPT_UNREADABLE=false
[ -z "$PROMPT_TEXT" ] && PROMPT_UNREADABLE=true

# Build deduplicated, filtered skill list
seen=""
MATCHED_LINES=""

for skills_dir in "$PROJECT_SKILLS_DIR" "$USER_SKILLS_DIR"; do
    [ -d "$skills_dir" ] || continue
    for skill_dir in "$skills_dir"/*/; do
        [ -f "$skill_dir/SKILL.md" ] || continue
        skill_name=$(basename "$skill_dir")

        # Deduplicate — project-level already processed first
        echo "$seen" | grep -qx "$skill_name" && continue
        seen="$seen
$skill_name"

        # Extract description from YAML frontmatter
        desc=$(grep -m1 "^description:" "$skill_dir/SKILL.md" 2>/dev/null \
               | sed 's/^description:[[:space:]]*//')

        # Keyword match: extract words >= MIN_KEYWORD_LEN chars from description,
        # check if any appear in the user's prompt
        MATCHES=false
        if [ "$PROMPT_UNREADABLE" = "true" ]; then
            # Can't read prompt → include all skills (safe fallback)
            MATCHES=true
        elif [ -n "$desc" ]; then
            # Build pipe-delimited keyword pattern from description
            keywords=$(echo "$desc $skill_name" \
                       | tr '[:upper:]' '[:lower:]' \
                       | grep -oE "[a-z]{${MIN_KEYWORD_LEN},}" \
                       | grep -vE "^(with|this|that|from|have|will|when|your|their|each|about|which|these|those|using|where|other|skill|tool|code|file|task|work|make|used|use|call|need|only|also|into|then|than|should|would|could|after|before|while|being|doing|built|based)$" \
                       | head -10 \
                       | tr '\n' '|' \
                       | sed 's/|$//')
            [ -n "$keywords" ] && echo "$PROMPT_TEXT" | grep -qE "$keywords" && MATCHES=true
        fi

        [ "$MATCHES" = "false" ] && continue

        if [ "$SHOW_DESCRIPTIONS" = "true" ] && [ -n "$desc" ]; then
            MATCHED_LINES="$MATCHED_LINES\n  - $skill_name: $(echo "$desc" | cut -c1-70)"
        else
            MATCHED_LINES="$MATCHED_LINES\n  - $skill_name"
        fi
    done
done

# Completely silent if nothing matched — no tokens, no noise
[ -z "$MATCHED_LINES" ] && exit 0

cat <<EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RELEVANT SKILLS DETECTED — EVALUATE BEFORE IMPLEMENTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$(echo -e "$MATCHED_LINES")

For each: YES or NO with one-line reason.
Every YES → call Skill(skill-name) immediately, before any implementation.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF
