---
name: session-handoff
description: Generate a structured handoff document capturing current progress, open tasks, key decisions, and context needed to resume work. Handoffs are PAIRED BRACKETS — write one at every phase boundary (milestone completion, substantive batch of decisions, mid-session pivot) AND at session end. If you read a handoff at session start, you owe one back before transitioning.
---

# Session Handoff

Different from wrap-up. Wrap-up is a checklist for *you*. Handoff is a document written for the *next session*.

## Bracket pattern (primary framing)

**Handoffs are paired brackets, not session-end events.** Every phase opens with a handoff read-in and closes with a handoff write-out. The reciprocity is the discipline:

- **Read-in trigger** (always): At session start, read the most recent non-superseded handoff in `.sessions/handoffs/` to load phase state.
- **Write-out trigger** (newly load-bearing): Before transitioning to the next phase OR ending the session — whichever comes first — write a handoff. The handoff closes the bracket of the just-completed phase and opens the bracket of the next.

**Why this framing matters:** "Session-end handoff" is too narrow — phase boundaries happen *within* sessions too. Long sessions accumulate context that auto-compaction silently degrades; mid-session handoffs crystallize phase findings before they're lost. The bracket pattern also makes the norm self-perpetuating: if a session opens by reading a handoff, it inherits the contract to write one when the next phase boundary arrives.

### What counts as a phase boundary

Substantive enough to warrant a handoff:
- Milestone or build phase completion (M0 done, M1 starts)
- A batch of decisions that future-Claude would benefit from inheriting (4+ ecosystem migrations discovered, architectural pivot, scope correction)
- An audit/sweep finding that surfaces unexpected work
- End of session (always, even mid-phase)

Skip the handoff when:
- The "phase" was a single config tweak or trivial edit
- A handoff was written within the last hour and no substantive work occurred since
- The work is genuinely throwaway (sandbox experiment, scratch script)

The rule of thumb: *if a fresh Claude session would benefit from this state being captured, write the handoff.*

## Trigger

Use when:
- Phase or milestone completes (write-out side of bracket)
- Substantive batch of decisions/findings has accumulated
- About to start a new session and want to resume smoothly
- Operator says "handoff", "continue later", "pass to next session", "save progress", "wrap this phase"
- Mid-session pivot or architectural correction (so the next phase inherits the corrected state)

## Workflow

1. Gather current state from git.
2. List completed, in-progress, and pending work.
3. Note key decisions made and their reasoning.
4. Capture any learnings from this session.
5. Generate a resume command for the next session.

## Commands

```bash
git status
git diff --stat
git log --oneline -5
git branch --show-current
```

## Output

```markdown
# Session Handoff — [date] [time]

## Status
- **Branch**: feature/xyz
- **Commits this session**: 3
- **Uncommitted changes**: 2 files modified
- **Tests**: passing / failing / not run

## What's Done
- [completed task 1]
- [completed task 2]

## What's In Progress
- [current task with context on where you stopped]
- [file:line that needs attention next]

## What's Pending
- [next task that hasn't been started]
- [blocked items with reason]

## Key Decisions Made
- [decision 1 and why]
- [decision 2 and why]

## Learnings Captured
- [Category] Rule (from this session)

## Files Touched
- `path/to/file1.ts` — [what changed]
- `path/to/file2.ts` — [what changed]

## Gotchas for Next Session
- [thing that tripped you up]
- [non-obvious behavior discovered]

## Resume Command
> Continue working on [branch]. [1-2 sentence context]. Next step: [specific action].
```

## File Location

**Always write handoffs to `.sessions/` inside the current project directory** —
NOT to `~/AI-Knowledgebase/.sessions/` or any external location. The handoff
belongs with the repo it describes so it appears in the project's VS Code
explorer and travels with the repo.

- Create `.sessions/` at the repo root if it doesn't exist.
- Name the file `handoff-YYYY-MM-DD.md` (append `-evening`, `-2`, etc. for
  multiple handoffs on the same day).
- If a `CLAUDE.md` or similar config references a "latest handoff" path,
  update that reference to point to the new file.
- Plans, execution docs, and spike notes also belong in the project (e.g.
  `docs/plans/`), not in external knowledgebases.

## Guardrails

- Write for the reader (next session), not the writer.
- Include specific file paths and line numbers where relevant.
- The resume command should be copy-pasteable into the next session.
- Keep it factual — describe changes functionally, don't infer motivation.
- All file references in the handoff should use project-relative paths
  (e.g. `.sessions/handoff-2026-04-15.md`) or absolute paths to the
  project directory — never to external directories.

---

## SignalWorks Takeaways Extension

After producing the handoff doc (above), run this extension. It auto-captures
workflow takeaways for SignalWorks consulting engagements without manual prompting.

### Step 1: Detect SignalWorks project

Read the project's `CLAUDE.md` (path: `<project-root>/CLAUDE.md`).
Look for a line matching this exact pattern:

```
signalworks_takeaways_target: <absolute-path>
```

If the line is absent, **skip the rest of this extension** — non-SignalWorks
project, no impact, normal handoff flow continues.

If the line is present, extract the absolute path (the value after the colon).
This is the canonical takeaways target file in `signal-works-internal/takeaways/`.

### Step 2: In-session extraction

Identify transferable workflow patterns from the current session. Use the
already-loaded session context — no API call, no extra cost.

For each pattern, format as:

```markdown
### Pattern: {one-line summary}

**Evidence (this session):** {what happened that surfaced the pattern}

**Transfer rule:** {generalized statement applicable to future engagements}

**Provenance:** {project-slug}, {YYYY-MM-DD}
```

### Step 3: Apply gate — "must have transferable rule"

Only emit entries that have a clear, generalized transfer rule. If a pattern
is one-time-only or too specific to be portable, skip it.

If NO entries qualify after the gate, **write nothing** — avoid file pollution
with low-signal noise. Continue with normal handoff completion.

### Step 4: Dual-write — project-local + canonical

If at least one entry qualifies, write to BOTH:

**4a. Project-local target (always).** Every SignalWorks project (scaffolded by `/cook` v1.5+ or pre-existing like brett-gove-intell) has `docs/workflow-notes/session-takeaways.md`. Append qualified entries here under `## Session: {YYYY-MM-DD}` heading. This file is committed with the project's normal commit cycle — no separate git operations from session-handoff.

```bash
TODAY=$(date +%Y-%m-%d)
PROJECT_ROOT=$(git rev-parse --show-toplevel)
PROJECT_TAKEAWAYS="$PROJECT_ROOT/docs/workflow-notes/session-takeaways.md"

if [ -f "$PROJECT_TAKEAWAYS" ]; then
  printf "\n## Session: %s\n\n%s\n" "$TODAY" "$ENTRIES" >> "$PROJECT_TAKEAWAYS"
fi
```

**4b. Canonical target (always — same content).** Append the same entries to the canonical signal-works-internal path AND auto-commit + push there:

```bash
TARGET_PATH="<absolute path from step 1>"
TARGET_REPO=$(git -C "$(dirname "$TARGET_PATH")" rev-parse --show-toplevel)
TARGET_RELPATH=$(realpath --relative-to="$TARGET_REPO" "$TARGET_PATH")
SLUG=$(basename "$TARGET_PATH" .md)

# Mandatory pull-rebase first (signal-works-internal is co-owned, see its CLAUDE.md)
cd "$TARGET_REPO" && git pull --rebase

printf "\n## Session: %s\n\n%s\n" "$TODAY" "$ENTRIES" >> "$TARGET_PATH"

git add "$TARGET_RELPATH"
git commit -m "takeaways(${SLUG}): N entries from ${TODAY} session"
git push
```

Both files receive identical content. Project-local serves in-project visibility + travels with project archive. Canonical serves cross-engagement aggregation + survives project archival + harvest scanning.

### Step 5: Failure fallback for canonical-write

If pull-rebase, commit, or push to signal-works-internal fails (network error, merge conflict that can't be auto-resolved, push rejected):

1. Write the same content to `${TARGET_PATH}.pending` (sibling file with `.pending` suffix)
2. **Do NOT block the handoff** — handoff doc completion is the priority
3. Project-local write (4a) is unaffected by canonical-write failure
4. Surface the failure in the handoff's "Gotchas for Next Session" section:

```markdown
- ⚠️ Takeaways canonical-write to `<TARGET_PATH>` failed at git layer.
  Pending content at `<TARGET_PATH>.pending` — resolve manually:
  `cd <TARGET_REPO> && git pull --rebase && cat <pending> >> <target> && rm <pending> && git add . && git commit && git push`
  Project-local copy at `<PROJECT_TAKEAWAYS>` succeeded.
```

### Behavior on non-SignalWorks projects

Step 1's detection short-circuits cleanly. No SignalWorks-specific impact on
personal experiments, sandboxes, or any project without the
`signalworks_takeaways_target:` line in its CLAUDE.md.
