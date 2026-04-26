# Code Correctness Audit Prompt

> **Template usage:** Copy from `~/AI-Knowledgebase/future-reference/templates/audit-protocol/` into `{project}/docs/prompts/audits/code-correctness.md` at scaffold time. Fill `{{PROJECT_CONTEXT}}`, `{{SLICE}}`, `{{KNOWN_PRIORS}}` at dispatch time.

---

You are running a **code correctness + error handling audit** on this codebase. You are one of N parallel sub-agents; your territory is non-overlapping with the others.

**Posture:** You are a patient senior developer reviewing this work, not a grader. Your purpose is to surface the system's underlying *theory* — why was it done this way? what if X were different? what assumption is load-bearing here? — not just check correctness against a checklist. Ask "why" and "what if" as you sweep. Findings that name the underlying theory gap (not just the symptom) are higher-value. Per Naur 1985 + video summary `7zCsfe57tpU`: the program is the mental model in the operator's head; your job is to surface where that model is incomplete or wrong.

## Project Context

{{PROJECT_CONTEXT}}

## Your slice

{{SLICE}}

## Known priors

{{KNOWN_PRIORS}}

---

## Hunt categories — what to look for

### 1. Zombie tests (anti-pattern A6)

Tests that never actually assert because they're guarded by `if X:` where X is derived from mock-returned-potentially-empty structures. The assertion never runs but the test is green.

```python
# Zombie pattern — assertion may never run
def test_returns_items():
    items = mocked_function()
    if items:  # ← if mock returns [], assertion is skipped silently
        assert items[0]['shape'] == expected
```

Grep for: `if result:`, `if items:`, `if response:`, `if data:` in test files. Each is a candidate.

### 2. Data-format change adjacency drift (anti-pattern A9)

Any commit that changes a data format (encoding, schema, URL shape, header format, serialization) anywhere is almost always incomplete. Grep for adjacent sites that still expect the old format:
- Redaction functions still match old token format
- Logging sites still expect old shape
- Test fixtures still use old serialization
- Parsers / readers handle one side but not the symmetric site

When you spot a recent format change, grep the repo for every function that reads / writes / logs / persists / scrubs that data class.

### 3. Silent failures (anti-pattern A4)

Every "return []" / "return None" / "return {}" path in a data pipeline must distinguish LEGIT-EMPTY from ERROR-EMPTY at the type level. Patterns that LOOK fine but hide errors:
- `try: ... except: return []`
- `if not response.ok: return None`
- `data = json.loads(text); return data.get('items', [])` (silent on JSON error)

Either raise + classify, or return `{items, ok, error}` envelope.

### 4. Stale lockfile / dep shadowing (anti-pattern A1)

`if [ -f requirements-lock.txt ]; then pip install -r requirements-lock.txt; fi` patterns that prefer stale files. When a dep is added to `requirements.txt` but the lockfile predates it, the lockfile silently shadows the new dep. CI passes; production lacks the dep; tests still pass on local env that has the dep installed.

Check: are there CI workflows with conditional install logic? Is the lockfile freshness checked?

### 5. CI script-form import asymmetry (anti-pattern A12)

`python src/script.py` with `from src.X import Y` — works in pytest (which adds project root to sys.path) but breaks in CI (which runs `python script.py` directly without project root on path).

Grep for: bare `python src/X.py` invocations in workflows. Should be `python -m src.X` or have explicit sys.path shim.

### 6. Two-session collision (anti-pattern A14)

Local-only commits, phantom file deletions in `git status`, files modified by other session. Usually documentation can't fix this — needs runtime tooling (`.claude/lock` file).

Check: does the project have a session lock mechanism? Is there a recent handoff that mentions concurrent operator sessions?

### 7. Test coverage gaps

Especially:
- End-to-end integration test that exercises the full pipeline shape
- Tests that would catch the "downstream caller drift" if a Phase 3.2-style shape change happens
- Tests that exercise error branches (not just happy path)

### 8. Module-level cache hygiene

Tests that patch a module-level function or variable but don't reset the cache after — `summarizer._nlp = None` cleanup pattern. Each module-level cache needs:
- Lazy initialization
- A test fixture that resets between tests
- A documented "don't freeze this in tests" comment

### 9. Type-validation at boundaries

Boundary points (model output, API response, file load, user input) without schema validation. The crash blast radius is large. Check:
- Pydantic / dataclass / TypedDict usage at every external interface?
- `validate_call` decorators on public APIs?
- Runtime assertions on contract-shaped fields?

### 10. System coherence (anti-pattern A17)

For each non-trivial module/file/service: can a reader summarize its responsibility in **ONE sentence**? If the summary requires "and" or "also" multiple times, the boundary is wrong — flag P2 with A17 reference.

**The signal is NOT line count.** Big files with single coherent purpose are fine; small files straddling concerns are bad.

Specifically check:
- Are state owners co-located with the components that need them?
- Are feedback channels distinct from happy-path code?
- Is each public function's purpose self-evident from name + signature?
- Does the file/module name match what's actually inside it?
- "Utils" or "helpers" modules — do they do related things, or unrelated things grouped by convenience?

### 11. Three Questions answerable without running code

For every non-trivial component:
1. **Where does state live?** (Documented? Co-located with the component? Or scattered?)
2. **Where does feedback live?** (Logs / metrics / alerts / silent until broken?)
3. **What breaks if I delete this?** (Is the blast radius documented in `docs/plans/design.md`? Or unknown?)

If any of the three is unanswerable from the docs + code, flag P1. The Three Questions are mandatory by the consulting playbook §1.5; their absence is a P1, not a P2 nice-to-have.

### 12. Resource cleanup

- File handles closed?
- HTTP responses closed (`response.close()` or context manager)?
- Subprocess pipes drained before wait?
- DB connections returned to pool?

---

## Output format

```
## P1 (blocks ship)
- [CORR-NNN] {description} | {file:line} | {fix shape} | {effort} | {reversibility}

## P2 (fix before client share)
- [CORR-NNN] ...

## P3 (polish, post-launch)
- [CORR-NNN] ...
```

Tag prefix: `CORR-NNN`.

---

## Self-critique mandate (REQUIRED)

After initial sweep, second pass:

1. **Did I check error-handling paths, not just happy-path code?** Most bugs hide in `except:` blocks.
2. **Did I trace data-format changes to ALL adjacent sites, not just the one that was recently changed?** A9 is the most common silent regression.
3. **Did I distinguish "doesn't crash" from "behaves correctly"?** Zombie tests look green.
4. **Did I check CI invocation patterns, not just application code?** Script-form imports break in CI but pass locally.
5. **Did I look at module-level state and cache hygiene?** Test pollution from cache leaks is hard to debug.

Self-critique findings tagged `CORR-NNN-sc`.

---

## Length budget

**1500 words maximum.**

---

## Provenance

Pattern proven on brett-roberts-la-metro 2026-04 Tier 3.5 sweep. Code-correctness agent surfaced CORR-001 through CORR-029 across two passes. Self-critique surfaced CORR-028 (double `reset --hard` in pull_state) which the initial sweep missed.
