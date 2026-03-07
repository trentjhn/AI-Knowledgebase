# PromptArena — Skills Integration Guide

When building PromptArena with a coding assistant, invoke these skills **in sequence** for maximum quality.

---

## Skill Execution Sequence

### Phase 1: Planning & Setup

**Invoke: `superpowers:writing-plans`**
- Already done (see `/docs/plans/2026-03-07-promptarena.md`)
- Plan covers all 10 tasks with TDD discipline

---

### Phase 2: Implementation (Tasks 1-7)

**Invoke per-task: `superpowers:test-driven-development`**
- Write failing test first
- Implement minimal code to pass
- Commit after each step

**Invoke per-component: `frontend-taste` (design engineering)**

When building React components (Task 4), use frontend-taste to enforce design quality:

```
DESIGN_VARIANCE: 8 (asymmetric, artistic brutalism)
MOTION_INTENSITY: 6 (meaningful animations, not decorative)
VISUAL_DENSITY: 4 (breathing room, not packed)
```

Key frontend-taste directives for PromptArena:

1. **Typography Engineering** ✓ ALREADY SPECIFIED
   - Display: Playfair Display 700, `text-4xl tracking-tighter leading-none`
   - Body: IBM Plex Mono 400, `text-sm leading-relaxed`
   - See `/docs/promptarena-design-system.md` for exact specs

2. **No Tailwind** — Use custom CSS only
   - frontend-taste expects Tailwind, but PromptArena uses custom CSS for brutal aesthetic
   - Override: "Using custom CSS to enforce brutalist design system. No Tailwind utilities."

3. **Responsiveness** ✓ REQUIRED
   - Use CSS Grid (`grid grid-cols-1 md:grid-cols-2`) when available, else custom
   - Breakpoint at 768px for mobile
   - **CRITICAL:** Use `min-h-[100dvh]` (not `h-screen`) for full-height sections

4. **Icons** — Use Phosphor or SVG
   - No emojis (anti-emoji policy)
   - If needed, import from `@phosphor-icons/react` (check package.json)
   - Or use custom SVG primitives

---

### Phase 3: Testing (Task 8)

**Invoke: `superpowers:test-driven-development`**
- Write and run API client tests (Vitest)
- Write and run progress tracking tests
- All tests must pass before moving to Phase 4

---

### Phase 4: Code Quality (Task 9)

**Invoke: `pr-review-toolkit:code-reviewer`**
- Review all TypeScript source code
- Check against project standards (type safety, error handling, component design)
- Return to implementation if issues found

**Invoke: `pr-review-toolkit:code-simplifier`**
- Remove boilerplate and over-engineering
- Simplify abstractions

**Then invoke: `deslop`**
- Remove AI-generated code slop
- Check for:
  - Extra comments that state the obvious
  - Over-engineered abstractions for one-time operations
  - Unnecessary type casts
  - Defensive code that isn't needed for internal paths
  - Features beyond what was requested

All tests must pass after simplification.

---

### Phase 5: Error Handling (Throughout, emphasis Task 4-6)

**Invoke: `error-handling-patterns`**

When implementing API client and form submissions:

```typescript
// From error-handling-patterns: Custom error classes
class ApplicationError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

class APIError extends ApplicationError {
  constructor(message: string, statusCode: number, details?: any) {
    super(message, "API_ERROR", statusCode, details);
  }
}

// Usage in submitPromptToApi
async function submitPromptToApi(userPrompt: string, scenarioTask: string) {
  try {
    const response = await fetch("/api/submit-prompt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userPrompt, scenarioTask }),
    });

    if (!response.ok) {
      throw new APIError(
        `API error: ${response.statusText}`,
        response.status,
        { url: "/api/submit-prompt" }
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error; // Re-throw known errors
    }
    // Wrap unknown errors
    throw new ApplicationError(
      "Failed to submit prompt",
      "SUBMISSION_ERROR"
    );
  }
}
```

Key error-handling patterns for PromptArena:

1. **Custom Error Classes** (TypeScript)
   - `ApplicationError` base class
   - `APIError` for API failures
   - `ValidationError` for input validation

2. **Error Context** — Include details for debugging
   - What failed
   - Why it failed
   - Recoverable or fatal

3. **User-Friendly Messages** — Don't expose stack traces
   - "Failed to submit prompt" (user-facing)
   - Log full error internally

4. **Retry Logic** — For transient failures
   - Network timeout? Retry with exponential backoff
   - API rate limit? Queue and retry

---

### Phase 6: Deployment (Task 10)

**Invoke: `pro-workflow`** (if available)
- Final deployment checklist
- Environment variable verification
- Production readiness

---

## Skill-Specific Guidelines for PromptArena

### `deslop` — What to Watch For

PromptArena is deliberately brutalist and minimal. `deslop` should NOT remove:
- Necessary error handling (API failures are real)
- Comments on non-obvious logic (monospace typography, animation timing)
- Border and color definitions (they're the visual language)

`deslop` SHOULD remove:
- Comments like "// Set button to blue" (obvious from code)
- Try-catch blocks for scenarios that can't happen
- Over-engineered utilities (e.g., factory pattern for single-use component)
- Backwards-compatibility hacks

### `error-handling-patterns` — What's Required

All async operations (API calls, file access, external services) MUST have:
1. Try-catch wrapper
2. Specific error type (APIError, ValidationError, etc.)
3. User-friendly error message
4. Log with full context (for debugging)
5. Graceful fallback or clear error UI

Do NOT add error handling for:
- Scenarios that can't happen (e.g., "what if Array.map() fails")
- Internal trusted code paths
- Defensive checks for parameters you control

### `frontend-taste` — Adaptation for Custom CSS

`frontend-taste` is Tailwind-focused. For PromptArena (custom CSS):

**DO use frontend-taste's rules:**
- Typography engineering (scale, weight, tracking)
- Responsiveness (breakpoints, mobile-first)
- Icon choice (Phosphor, no emojis)
- Viewport stability (min-h-[100dvh] logic applies even with custom CSS)

**DO NOT use frontend-taste's rules:**
- Tailwind class recommendations (we use custom CSS)
- Tailwind-specific syntax (we use CSS variables)

**OVERRIDE with:**
- "Using custom CSS design system. All styling follows `/docs/promptarena-design-system.md`."

---

## Workflow Discipline

When coding assistant builds PromptArena:

1. **Task 1-3: Setup**
   - No skill invocations yet, just follow plan

2. **Task 4-7: Implementation + TDD**
   - `superpowers:test-driven-development` per task
   - `frontend-taste` when building components (with CSS override)
   - `error-handling-patterns` when handling API/form errors

3. **Task 8: Testing**
   - `superpowers:test-driven-development` for test writing
   - Ensure all tests pass

4. **Task 9: Code Quality**
   - `pr-review-toolkit:code-reviewer`
   - `pr-review-toolkit:code-simplifier`
   - `deslop`
   - All tests pass after each step

5. **Task 10: Deploy**
   - Verify environment setup
   - Run final tests
   - Deploy to Vercel

---

## Checklist for Coding Assistant

Before marking PromptArena as complete:

- [ ] All TDD cycles completed (tests pass)
- [ ] All API errors have custom error classes
- [ ] All async operations wrapped in try-catch
- [ ] Code review passed (no type issues, proper error handling)
- [ ] Simplification completed (no slop)
- [ ] Design system followed (fonts, colors, spacing, motion)
- [ ] Responsive at 768px breakpoint
- [ ] No Tailwind utilities (custom CSS only)
- [ ] No emojis (Phosphor icons or SVG if needed)
- [ ] All tests pass locally
- [ ] Environment variables verified
- [ ] Deployment checklist complete

---

## References

- Design System: `/docs/promptarena-design-system.md`
- Implementation Plan: `/docs/plans/2026-03-07-promptarena.md`
- Frontend Taste Skill: `/Users/t-rawww/zenkai/.claude/skills/frontend-taste/SKILL.md`
- Error Handling Patterns: `/Users/t-rawww/zenkai/.claude/skills/error-handling-patterns/SKILL.md`
- Deslop Skill: `/Users/t-rawww/zenkai/.claude/skills/deslop/SKILL.md`

---

**This is a complete, integrated spec. No improvisation. Follow exactly.**
