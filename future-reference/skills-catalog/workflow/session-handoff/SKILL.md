---
name: session-handoff
description: Generate a structured handoff document capturing current progress, open tasks, key decisions, and context needed to resume work. Use when ending a session, saying "continue later", "save progress", "session summary", or "pick up where I left off".
---

# Session Handoff

Different from wrap-up. Wrap-up is a checklist for *you*. Handoff is a document written for the *next session*.

## Trigger

Use when saying "handoff", "continue later", "pass to next session", "session transfer", or ending a session and wanting to resume smoothly.

## Workflow

1. Gather current state from git.
2. List completed, in-progress, and pending work.
3. Note key decisions made and their reasoning.
4. Capture any learnings from this session.
5. Use the Glob tool with pattern `.claude/agents/*` to discover the active agent fleet. List every file found in the Active Agent Fleet output section.
6. To fill **Next Session Invocations**: read the `## Development Workflow` section of `CLAUDE.md`, identify the current phase, and list the remaining skills in sequence. Use exact skill names (e.g., `superpowers:executing-plans`, not "execute"). If mid-task, specify the sub-step (e.g., "task 4 of 9").
7. Generate a resume command for the next session.

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

## Current Phase
- **Workflow phase**: [brainstorm / plan / execute / review / done]
- **Sub-step**: [e.g., "executing-plans — task 4 of 9 complete" or "plan written, not yet executing"]
- **Last verified checkpoint**: [last artifact confirmed correct against acceptance criteria]

## Active Agent Fleet
[Use Glob tool: `.claude/agents/*` — list every file found with one-line purpose]
- `[agent-filename].md` — [what it does / when to use it]
[If new files appeared since last handoff, note them here.]

## Next Session Invocations
[Read CLAUDE.md Development Workflow. Based on current phase, list skills to invoke first, in order:]
1. [exact skill name, e.g., superpowers:executing-plans] — [one-line context, e.g., "resume from task 4, auth module"]
2. [next skill if applicable]
[If session is complete: "No pending invocations — project is at [phase]."]

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

## Guardrails

- Write for the reader (next session), not the writer.
- Include specific file paths and line numbers where relevant.
- The resume command should be copy-pasteable into the next session.
- Keep it factual — describe changes functionally, don't infer motivation.
