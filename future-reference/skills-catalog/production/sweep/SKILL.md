---
name: sweep
description: Multi-agent deployment-readiness gate for any project going public or shipping to clients. Dispatches 9-11 specialized sub-agents in 2 waves + verification round across security/code/infra/data/UX/docs territories with heavy KB context loaded. Hard pass-gate (GO/HOLD/NO-GO) — blocks deploy on critical security/data-integrity findings. Use when saying "ready to ship", "deploy to production", "going public", "client delivery", "/sweep", or before any deploy declaration. Catches in one sweep what manual ad-hoc sub-agent dispatches miss across multiple cycles.
origin: KB
---

# /sweep — Multi-Agent Deployment Gate

Production launch gate. Multi-agent successor to single-checklist `pre-ship`. **The standard is: public-deploy-ready and attack-safe across the board** — same bar for consulting work and personal projects.

## Configuration

```
KB_ROOT default: ~/AI-Knowledgebase (override with `export KB_ROOT=/your/kb/path`)
```

If installing on a new machine: ensure the AI Knowledgebase is cloned to `$KB_ROOT/` OR set `KB_ROOT` environment variable. The skill resolves ALL KB references relative to `$KB_ROOT` and falls back to a hard error if `$KB_ROOT` doesn't exist (don't silently load wrong context).

Required local skills: `pre-ship` (referenced by security-deployment + infrastructure-deployment agents). Install via copy from `$KB_ROOT/future-reference/skills-catalog/production/pre-ship/` if not present at `$HOME/.claude/skills/pre-ship/`.

## When to invoke

- Before any production deploy
- Before any client-facing artifact share (URL, dashboard, email)
- Before declaring an engagement scaffold "deploy-ready"
- After a major refactor that touches security boundaries / state architecture / external interfaces
- When a CLAUDE.md mandate fires (per /cook v1.8 scaffold convention)

**This is NOT a routine check.** For quick solo deploys with no public exposure, use `pre-ship` (single checklist, ~5-20 min). `/sweep` is the heavy gate for going-public moments. Use it when wrong-answer would cost client trust, money, security, or reputation.

## Why multi-agent + heavy context

The failure mode this prevents: **operator dispatches sub-agents → agents find bugs → operator fixes → dispatches again → MORE bugs surface → continuous cycles.** Root cause: each manual sweep has limited slice context (each agent sees only its territory; cross-territory bugs require a verification round; missed-territory bugs require re-dispatch).

`/sweep` solves this with three discipline shifts:
1. **Comprehensive territory coverage in one dispatch** (7+ specialized agents, not 4 generic ones)
2. **Heavy KB context loaded into every brief** (OWASP LLM Top 10, pre-ship checklist, A1-A20 anti-patterns, AI security §3-§4) — agents work from real attack/failure-mode catalogs, not generic instructions
3. **Cross-pollination verification round** (Wave 2 agent receives ALL Wave 1 findings; hunts cross-territory bugs that single-territory agents miss)

**Honest framing:** zero-bug detection in one sweep is impossible. The bar is **all P1 (deploy-blocking) issues caught in one sweep**, so subsequent fix cycles surface only P2/P3 polish — not new "this would have been a critical bug in production" findings.

---

## Step 1: Auto-detect project context

Before dispatching agents, gather:

```bash
# Resolve KB_ROOT (must exist or sweep aborts — don't silently load wrong context)
KB_ROOT="${KB_ROOT:-$HOME/AI-Knowledgebase}"
if [ ! -d "$KB_ROOT" ]; then
  echo "ERROR: KB_ROOT not found at $KB_ROOT"
  echo "Set 'export KB_ROOT=/your/kb/path' or clone AI-Knowledgebase to ~/AI-Knowledgebase/"
  exit 1
fi

# Project root
PROJECT_ROOT=$(git rev-parse --show-toplevel)
COMMIT_SHA=$(git rev-parse --short HEAD)
TODAY=$(date +%Y-%m-%d)

# Language stack
LANG_HINT=""
[ -f "$PROJECT_ROOT/package.json" ] && LANG_HINT="JS/TS"
[ -f "$PROJECT_ROOT/pyproject.toml" ] || [ -f "$PROJECT_ROOT/requirements.txt" ] && LANG_HINT="Python"
[ -f "$PROJECT_ROOT/Cargo.toml" ] && LANG_HINT="Rust"
[ -f "$PROJECT_ROOT/go.mod" ] && LANG_HINT="Go"

# Project shape
HAS_WEB="false"
[ -d "$PROJECT_ROOT/src" ] && [ -f "$PROJECT_ROOT/index.html" ] && HAS_WEB="true"
[ -d "$PROJECT_ROOT/public" ] && HAS_WEB="true"

# SignalWorks engagement check
IS_SIGNALWORKS="false"
grep -q "signalworks_takeaways_target:" "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null && IS_SIGNALWORKS="true"

# AI deliverable check (Type A)
IS_AI_DELIVERABLE="false"
[ -d "$PROJECT_ROOT/docs/prompts" ] && IS_AI_DELIVERABLE="true"
grep -qi "anthropic\|openai\|gemini\|llm" "$PROJECT_ROOT/requirements.txt" "$PROJECT_ROOT/package.json" 2>/dev/null && IS_AI_DELIVERABLE="true"

# RAG check
HAS_RAG="false"
grep -qi "embedding\|vector\|chroma\|pinecone\|weaviate\|qdrant" "$PROJECT_ROOT/requirements.txt" "$PROJECT_ROOT/package.json" 2>/dev/null && HAS_RAG="true"

# Threat-model artifact (from /cook v1.8 scaffold)
THREAT_MODEL=""
[ -f "$PROJECT_ROOT/docs/plans/threat-model.md" ] && THREAT_MODEL="$PROJECT_ROOT/docs/plans/threat-model.md"

# Live URL — from operator argument or CLAUDE.md / design.md
# v1.9.1 calibration fix: also match scheme-less domain patterns (gov.signalworks.live, foo.pages.dev, etc.)
LIVE_URL="${1:-}"  # First argument
if [ -z "$LIVE_URL" ]; then
  LIVE_URL=$(grep -oE 'https?://[^ )`]+' "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null | head -1)
fi
if [ -z "$LIVE_URL" ]; then
  # Scheme-less domain patterns (e.g., `gov.signalworks.live`, `foo.pages.dev`, `bar.vercel.app`)
  LIVE_URL=$(grep -oE '[a-z0-9-]+\.(signalworks\.live|pages\.dev|vercel\.app|netlify\.app|fly\.dev)' "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null | head -1)
  [ -n "$LIVE_URL" ] && LIVE_URL="https://$LIVE_URL"
fi
```

Read into context:
- `$PROJECT_ROOT/docs/plans/design.md` — problem statement, deliverable, success criteria, AI Decision Points
- `$PROJECT_ROOT/docs/plans/threat-model.md` — actors / assets / threats / defenses / residual risks
- `$PROJECT_ROOT/SOUL.md` — engagement character, voice rules, definition of done
- `$PROJECT_ROOT/.sessions/handoffs/` — most recent handoff's "Audit Directions for Next Session" slot (priors for this sweep)
- If live URL: fetch HTML/JSON via `curl` or appropriate tool

**Surface the auto-detected context to operator before dispatching:**

```
Sweep target: {PROJECT_ROOT}
  Stack: {LANG_HINT}
  Web app: {HAS_WEB}
  SignalWorks engagement: {IS_SIGNALWORKS}
  AI deliverable (Type A): {IS_AI_DELIVERABLE}
  RAG: {HAS_RAG}
  Live URL: {LIVE_URL or "(none — will sweep code only)"}
  Threat model: {THREAT_MODEL or "(missing — will flag in docs-operability)"}

Dispatching {N} agents in 2 waves + verification round.
Estimated wall clock: ~25-30 min.
```

If operator wants to abort or adjust scope, do so before dispatch. Otherwise proceed.

---

## Step 2: Wave 1 — 7 universal agents in parallel

All 7 agents dispatched in a single message with parallel `Task` tool calls (per the conversation system prompt rule: "If you intend to call multiple tools and there are no dependencies between the calls, make all of the independent calls in the same message").

**Each agent's brief follows this structure** (do NOT skip sections):

```
You are running [TERRITORY] audit on this codebase as part of /sweep — a deployment-readiness gate.

## STAKES
This is a DEPLOYMENT GATE, not a code review. Findings you miss become production bugs the operator/client/end-user will hit. The operator has explicitly said "no playing around — this needs to be extremely effective." Treat this as the FINAL pass before going live.

## PROJECT CONTEXT
{Project description from design.md problem statement}
{Engagement type: SignalWorks / personal}
{Exposure level: public / auth-gated / internal / local-only}
{Sensitive data: PII / money / credentials / health / legal / none}
{Worst-case if compromised: from threat-model.md}

## YOUR TERRITORY
{Specific files / surfaces / concerns this agent owns — non-overlapping with sibling agents}

## KB CONTEXT (load and apply)
{Inline excerpt of relevant KB sections — see per-agent specifics below}

## KNOWN PRIORS (from prior sweep + handoff Audit Directions slot)
{Whatever the latest handoff's Audit Directions section contains, plus any prior sweep findings still open}

## HUNT CATEGORIES
{Numbered list specific to territory — see per-agent below}

## ADVERSARIAL FRAMING
Don't review. Try to BREAK this. What would an attacker / hostile user / stress-test do? Where would a real-world failure mode hit?

## OUTPUT FORMAT
## P1 (BLOCKS DEPLOY)
- [{TAG}-NNN] description | file:line | fix shape | effort | reversibility | evidence

## P2 (fix before client share)
- [{TAG}-NNN] ...

## P3 (polish, post-deploy)
- [{TAG}-NNN] ...

Each finding includes EVIDENCE (specific file:line, command output, HTML snippet, log string). No abstract findings.

## SELF-CRITIQUE MANDATE (REQUIRED)
After your initial sweep, second pass: {4-5 territory-specific meta-questions}. Don't assume your first pass is complete.

## LENGTH BUDGET
{1500 words for code/security/UX/data/infra; 900 for docs}
```

### Agent 1: security-attack-surface

**Territory:** OWASP LLM Top 10, 6 attack classes, prompt injection (direct + indirect), agent-specific attack vectors, RAG poisoning if applicable, supply-chain risks.

**KB context to load inline:** `$KB_ROOT/LEARNING/PRODUCTION/ai-security/ai-security.md` lines 67-200 (OWASP LLM Top 10 + Deep Dives). Anti-patterns A13 (centralized log-safety), A18 (recovery handler exception class).

**Hunt categories:**
1. Prompt injection vectors (direct + indirect — does the agent read external content? web pages? emails? retrieved docs?)
2. URL-scheme XSS in model-authored hrefs (`javascript:`, `data:`, `file:` — must be allowlist `http(s)://` only)
3. Token/secret leakage in error logs (anti-pattern A13 — centralized redactor required)
4. RAG attack surfaces (vector poisoning, retrieval manipulation, indirect injection via retrieved docs) — if RAG present
5. Tool/permission scoping (least-privilege per agent action; can the agent be tricked into elevated operations?)
6. System prompt leakage (prompt injection extracting business logic / credentials)
7. Excessive agency (does the agent have tools it shouldn't, given its trust boundary?)
8. Spotlighting / taint tracking applied? (Microsoft's >50% → <2% defense for indirect injection)

**Self-critique meta-questions:**
1. Did I check ALL inputs the model touches (user input, retrieved docs, external API responses, file reads), not just user-typed input?
2. Did I check ALL tool/action sinks (network calls, file writes, credential fields, logs), not just the obvious ones?
3. If RAG, did I check the vector store ingestion pipeline for poisoning vectors, not just retrieval?
4. Did I assume the threat model from `docs/plans/threat-model.md`, or default to "no threat model documented = treat as untrusted public exposure"?
5. Did I check supply-chain (deps, model wheels, plugins) for unsigned/unpinned items?

### Agent 2: security-deployment

**Territory:** pre-ship Security checklist + secrets/credentials/auth/CORS/HTTPS/headers/dep-audit.

**KB context to load inline:** `$HOME/.claude/skills/pre-ship/SKILL.md` Security section (lines 33-47). Anti-pattern A3 (fork lineage / repo privacy).

**Hunt categories:**
1. No API keys, secrets, or credentials in frontend code or git history (`git log -p | grep -iE 'api_key|password|token|secret'`)
2. `.env` in `.gitignore` — verify with `git status`
3. Every route checks authentication (audit ALL endpoints, not just obvious)
4. HTTPS enforced everywhere — HTTP redirects to HTTPS
5. CORS locked to specific origins (no wildcard `*`)
6. Input validated and sanitized server-side (not just client-side)
7. Rate limiting on auth endpoints and sensitive operations
8. Passwords hashed with bcrypt/argon2 (not MD5/SHA1/plain)
9. Auth tokens have expiry; sessions invalidated on logout
10. Security headers set: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
11. Dependencies scanned: `npm audit` / `pip-audit` / equivalent run; critical vulns resolved
12. Repo privacy + fork lineage (anti-pattern A3) — public-fork-of-public can't go private
13. GitHub Actions workflow permissions = `contents: read` minimum
14. Default branch protection rules in place

**Self-critique meta-questions:**
1. Did I `git log -p | grep` for committed secrets, not just check current files?
2. Did I check pre-ship's full checklist OR just the items I remember?
3. For auth: did I check EVERY endpoint, or just the obvious-public ones?
4. For headers/CSP: are they actually set in production response, or just in config?
5. If this is a fork, did I verify the privacy lineage doesn't lock visibility?

### Agent 3: code-correctness

**Territory:** A6 (zombie tests), A9 (data-format adjacency drift), A17 (system incoherence), A18 (recovery handler exception class), A19 (parallel branches drift), Three Questions answerable, silent failures (A4).

**KB context to load inline:** `$KB_ROOT/future-reference/templates/audit-protocol/code-correctness.md` (full file). Consulting playbook anti-patterns table A1-A20.

**Hunt categories:** (full list from code-correctness audit prompt — 14 categories including Three Questions answerable, system coherence, recovery handler exception classes, parallel branches drift)

**Self-critique meta-questions:** (per code-correctness audit prompt — error-handling paths, data-format adjacency, zombie vs real tests, CI script-form imports, module-level state)

### Agent 4: infrastructure-deployment

**Territory:** pre-ship Infrastructure/Database/Monitoring + 4 SaaS failure modes (infra-not-validated, external API fragility, silent failures, cross-cutting scope leakage).

**KB context to load inline:** `$HOME/.claude/skills/pre-ship/SKILL.md` Infrastructure/Database/Monitoring sections (lines 50-99). `$KB_ROOT/future-reference/playbooks/building-ai-saas.md` 4 failure modes section.

**Hunt categories:**
1. All env vars set on production server
2. SSL cert installed, valid, auto-renewing
3. Firewall configured (only 80/443 open publicly)
4. Process manager running (PM2/systemd/equivalent)
5. Staging test passed before production
6. Rollback plan exists AND tested (anti-pattern: untested rollback)
7. Docker image uses pinned version tags (not `:latest`)
8. Health check endpoint at `/health`
9. Resource limits set (CPU/memory) if containerized
10. DB backups configured AND TESTED (test the restore, not just the backup)
11. Parameterized queries everywhere (no string concat in SQL)
12. App connects as non-root DB user with min permissions
13. Error tracking (Sentry/Bugsnag/equivalent)
14. Uptime monitoring
15. Log aggregation
16. Alerting (error-rate threshold)
17. Pre-flight checks distinguish auth from availability (anti-pattern A11)

**Self-critique meta-questions:**
1. Did I verify backups are tested by restoring, not just configured?
2. Did I check the rollback plan can actually be executed under pressure?
3. Are monitoring alerts wired to a channel someone actually reads?
4. Are env vars set in production — did I verify, or just check the README?
5. For containerized: are resource limits set, or could this OOM under load?

### Agent 5: data-integrity

**Territory:** content_hash contract (every persisted item has stable identifier), silent failures (A4), zombie tests (A6), upstream-data normalizers, ingestion contract enforcement.

**KB context to load inline:** Consulting playbook §7 + ingestion contract. `$KB_ROOT/future-reference/playbooks/signalworks-consulting.md` A4/A6 anti-pattern descriptions.

**Hunt categories:**
1. Every persisted item has non-null `content_hash` (or stable ID) — anti-pattern from brett harvest
2. Silent failures: every `return []` / `return None` / `try-except` distinguishes LEGIT-EMPTY from ERROR-EMPTY at type level (anti-pattern A4)
3. Zombie tests: branches guarded by `if X:` where X is mock-returned-potentially-empty (anti-pattern A6)
4. Defensive normalizers in place for upstream data quirks (per /cook v1.7 scaffold)
5. Idempotency: can ingestion run be re-executed safely?
6. Dedup strategy: is content_hash actually used for dedup, or are there fallthrough paths?
7. Audit trail: can every persisted item trace back to its source?
8. Schema validation at boundaries (Pydantic / Zod / TypedDict)

**Self-critique meta-questions:**
1. Did I check EVERY persistence boundary, or just the main one?
2. Did I check error-empty vs legit-empty distinction at the TYPE level, not just docstrings?
3. For dedup: did I check what happens when content_hash is null OR collides?
4. Did I check upstream sources for data quirks the normalizer doesn't cover?
5. If schema validation is at one boundary, are there other boundaries that bypass it?

### Agent 6: ux-client-ready

**Territory:** A10 (bare-dashboard / first-share architectural test), A16 (ship-ready vs client-ready), A20 (data-layer-stable redesign test), accessibility, responsive QA, content scannability, brand voice.

**KB context to load inline:** `$KB_ROOT/future-reference/templates/audit-protocol/ux-delivery.md` (full file).

**Hunt categories:** (full list from ux-delivery audit prompt — 12 categories including bare-dashboard test, ship-ready-vs-client-ready, data-layer-stable test, accessibility, responsive QA, brand voice, trust signals)

**Self-critique meta-questions:** (per ux-delivery audit prompt — fresh-user posture, empty/error/degraded states, mobile+desktop+tablet, brand voice systematic, client-specific voice rules)

### Agent 7: docs-operability

**Territory:** runbook completeness, decision-log freshness, operator-commands cheatsheet, invariants doc, handoff chain integrity, missing artifacts.

**KB context to load inline:** `$KB_ROOT/future-reference/templates/audit-protocol/docs-operations.md` (full file). Reference to consulting playbook §11 (handoff discipline).

**Hunt categories:** (full list from docs-operations audit prompt — 10 categories including doc rot, README failures, runbook gaps, onboarding gaps, decision log hygiene, handoff chain integrity, invariants doc, prompts versioning, repo-organizational debt, CI/build doc)

**Self-critique meta-questions:** (per docs-operations audit prompt)

---

## Step 3: Conditional Wave 1 agents (classification-gated)

Dispatch each conditional agent IF its trigger condition fires. Multiple may fire on the same project (e.g., a Type A AI deliverable handling PII over public exposure dispatches all of: ai-eval-integrity, ai-rag-security if RAG, compliance-specific, cost-controls, performance-load).

### Agent 8 (conditional): ai-eval-integrity

Fires when `IS_AI_DELIVERABLE=true`.

**Territory:** Eval framework setup, hallucination prevention architecture, model selection rationale, prompt rigor, AI Decision Points + Verification Mechanisms.

**KB context to load inline:** `$KB_ROOT/LEARNING/PRODUCTION/evaluation/evaluation.md` lines 1-200. Consulting playbook §16.1-16.4. AI Decision Points section in design.md.

**Hunt categories:**
1. Eval framework exists (3-level stack: offline / online / human)?
2. Eval gate runs before prompt revisions ship?
3. Hallucination prevention architecture: verbatim-selection / grounding check / NER gate / allow-list — appropriate to project?
4. Model selection documented (cost / latency / fallback)?
5. Prompt versioning in `docs/prompts/{name}-vN.md` with changelog?
6. Loader actually reads what's in the file (not inlined string)?
7. Examples inside the loader's regex-captured fence (not orphaned)?
8. AI Decision Points + Verification Mechanisms documented in `docs/plans/design.md`?
9. Validation predicate's mechanism exposed to LLM in system prompt (per magnum-opus universal pattern)?

**Self-critique meta-questions:**
1. Did I check EVERY AI decision point, or just the headline one?
2. For each decision point, is the verification mechanism actually wired up in code?
3. Are eval gates enforcing quality, or are they advisory and skipped under pressure?
4. Did I verify the prompt loader sees what humans see in the prompt file?

### Agent 9 (conditional): ai-rag-security

Fires when `HAS_RAG=true`.

**Territory:** RAG-specific attack surfaces — vector poisoning, retrieval manipulation, indirect injection via retrieved content, knowledge base extraction.

**KB context to load inline:** `$KB_ROOT/LEARNING/PRODUCTION/ai-security/ai-security.md` Section 4 RAG-Specific Attack Surfaces (search "RAG-Specific Attack Surfaces").

**Hunt categories:**
1. Knowledge base poisoning vectors (who can write to the vector store? validated?)
2. Retrieval manipulation (can ranking algorithm be exploited? are retrieved doc IDs verifiable?)
3. Indirect prompt injection via retrieved docs (spotlighting / taint tracking on retrieved content?)
4. Knowledge base extraction (can crafted queries exfiltrate sensitive docs?)
5. Embedding model security (signed? hash-pinned?)
6. Document ingestion pipeline (validation? content scanning?)

**Self-critique meta-questions:**
1. Did I check ingestion-time AND retrieval-time attack vectors?
2. Are retrieved docs treated as untrusted input (taint tracking)?
3. Did I check who has write access to the vector store?
4. For extraction: can the model surface document content directly, or only synthesized answers?

### Agent 9b (conditional): compliance-specific

Fires when Phase 0.6 Q11.7 flags PII / money / credentials / health / legal data, OR Phase 0.6 Q11 flagged compliance scope (HIPAA / GDPR / ABA Rule 1.6 / SOC 2 / PCI-DSS).

**Territory:** Specific regulatory requirements that generic security audits miss. Not "good security in general" — the compliance regime's actual technical requirements.

**KB context to load inline:** `$KB_ROOT/LEARNING/PRODUCTION/ai-security/ai-security.md` compliance-relevant sections. Plus engagement-specific compliance requirements documented in `docs/plans/threat-model.md` constraints section.

**Hunt categories (load only the regimes that apply):**

**HIPAA (if health data):**
1. PHI encryption at rest AND in transit (AES-256 at rest; TLS 1.2+ in transit)
2. Audit trail captures every PHI access (user / time / record / action)
3. Minimum-necessary access enforced (no all-records access by default)
4. BAA in place with every vendor handling PHI (model providers, vector stores, log services)
5. Right-to-access / right-to-amend workflows defined
6. Breach notification process documented (60-day window)
7. PHI excluded from logs by default

**GDPR (if EU PII):**
1. Lawful basis for processing documented per data category
2. Consent flows for non-contractual data uses
3. Right-to-deletion implementation (actual removal, not soft-delete with audit log)
4. Data minimization (collecting only what's needed)
5. Data residency (EU data in EU regions if required by client)
6. Data Processing Agreement with every sub-processor
7. Privacy policy reflects actual data flows (not template boilerplate)

**ABA Rule 1.6 (if legal data — attorney-client privilege):**
1. Client confidentiality not sent to non-attorney AI services
2. Privilege not waived by sending to third-party AI providers without client consent
3. Conflict-of-interest checks before processing matter-related data
4. Document destruction policies aligned with retention requirements
5. Output review by attorney before client-facing delivery

**SOC 2 (if claiming compliance):**
1. Audit log retention meets policy (typically 1+ year)
2. Access reviews scheduled (typically quarterly)
3. Change management documented (every prod change has approval trail)
4. Vendor security assessments on file
5. Incident response procedures tested (not just documented)

**PCI-DSS (if money / cards):**
1. PAN never logged in plaintext (truncated or tokenized)
2. CVV never stored
3. PCI-scope minimization (avoid touching card data when possible)
4. Network segmentation if storing card data
5. Vulnerability scans quarterly

**Self-critique meta-questions:**
1. Did I check the SPECIFIC compliance regime requirements, or default to "good security in general"?
2. For each compliance requirement: is it implemented in code, or just documented in the threat model?
3. Did I verify vendor compliance certifications are current (not expired)?
4. Is the audit trail tamper-evident (append-only, not just append)?
5. For breach notification: does the operator know the timeline for THIS regime, and is there a procedure?

### Agent 9c (conditional): cost-controls

Fires when Phase 0.6 Q5 = Type A (AI deliverable). Token-bomb attacks and runaway costs are real and underaudited.

**Territory:** AI cost-bounding — token budgets per request, rate limits preventing runaway spend, cost monitoring/alerting, model fallback strategies.

**KB context to load inline:** Consulting playbook §16.3 (Model Selection Rationale). `$KB_ROOT/future-reference/playbooks/cost-optimized-llm-workflows.md` (model routing, budget enforcement).

**Hunt categories:**
1. Per-request token cap (input + output) configured in code, not just hoped for
2. Per-user rate limit on AI-touching endpoints (prevents one user from burning quota)
3. Per-day / per-month spend cap with hard stop AND alert
4. Model selection routes by task complexity (Haiku/Sonnet/Opus tiering — not Opus for everything)
5. Streaming used where appropriate (reduces cost on early-termination scenarios)
6. Prompt caching enabled if applicable (Anthropic prompt caching: 90% cost reduction on repeated context)
7. Cost monitoring dashboard exists (operator can see daily/weekly spend trend, not just monthly bill surprise)
8. Budget alert at 50% / 80% / 100% thresholds
9. Fallback to smaller/cheaper model on budget hit (degradation > total stop)
10. Token-bomb attack defenses: request validation rejects payloads that would generate disproportionate compute (extremely long retrieval chains, recursive tool calls, mega-prompts)
11. OWASP LLM10 (Unbounded Consumption) checks: rate limiting, token caps per request, circuit breakers on expensive operations

**Self-critique meta-questions:**
1. Did I check that token caps are CODE-ENFORCED, not just policy-documented?
2. Is there an actual circuit breaker on cost, or just a "we hope it doesn't run away" assumption?
3. For token-bomb: did I check input validation that would reject pathological payloads?
4. Is the fallback model actually wired up, or just listed in design.md?
5. For monitoring: would the operator notice within 24 hours if costs 10x'd, or would they find out at month-end billing?

### Agent 9d (conditional): performance-load

Fires when Phase 0.6 Q11.6 = public AND project is expected to handle non-trivial traffic (>~100 req/min, OR client deliverable with stated SLA).

**Territory:** "Will this break under realistic load?" — not Lighthouse perf scoring (that's ux-client-ready), but actual stress / load resilience.

**KB context to load inline:** `$KB_ROOT/future-reference/playbooks/building-ai-saas.md` (4 failure modes — especially infrastructure-not-validated). `$HOME/.claude/skills/pre-ship/SKILL.md` Infrastructure section.

**Hunt categories:**
1. Load test exists for expected peak traffic (k6 / locust / wrk / artillery — actual stress test, not assumption)
2. P95 latency target documented + tested under load
3. P99 latency target documented + tested under load
4. Database connection pool sized for peak concurrent connections
5. Per-endpoint resource limits (CPU/memory) configured if containerized
6. Pagination on every list endpoint (no unbounded queries that degrade under load)
7. Background job queue sized for peak burst (no synchronous processing of long-running tasks in request path)
8. Cache layer where hot data exists (Redis/Memcached/CDN) — NOT just "we'll add caching later"
9. Graceful degradation under load: what fails first, and is failure visible vs silent?
10. Auto-scaling configured (or explicit decision why not)
11. Database query plans for hot queries reviewed (no N+1, no full-table scans on big tables)
12. External API timeout + retry strategy under burst conditions (don't pile up retries)

**Self-critique meta-questions:**
1. Did I check that a load test was ACTUALLY RUN, or just configured?
2. For latency targets: tested at peak load, or only under happy-path solo-user conditions?
3. Did I check the slowest 1% of queries, not just the average?
4. For auto-scaling: tested by inducing load, or just configured and prayed?
5. Did I check the failure mode of every external dependency under burst (model API rate limits, DB connection pool exhaustion, downstream service slowness)?

---

## Step 4: Wave 2 — cross-pollination verifier (sequential after Wave 1)

After all Wave 1 agents return, dispatch ONE additional agent with ALL Wave 1 findings as input.

### Agent 10: cross-pollination-verifier

**Brief:**

```
You are the cross-pollination verifier for /sweep. Wave 1 dispatched 7-9 specialized
agents on non-overlapping territories. Each agent has limited context for its slice.

Your job: hunt for bugs that REQUIRE cross-territory reasoning to spot.

## INPUTS
{All Wave 1 findings, organized by agent / territory}

## HUNT CATEGORIES

1. **Compounding risks** — does Agent A's finding compound Agent B's finding?
   Example: security-attack-surface flagged a prompt-injection vector. Does code-correctness's
   finding about lax input validation make that vector trivially exploitable?

2. **Same root cause across territories** — do findings from multiple agents trace to a single
   bug?
   Example: data-integrity flagged content_hash=null. Does ux-client-ready's pin-collision
   finding trace to the same root cause?

3. **Defenses that depend on each other** — does Agent X's defense rely on Agent Y's defense
   being in place?
   Example: security-deployment requires CSP headers; if Agent Y (ux) flagged that the
   render layer is bypassing headers, the security defense is undermined.

4. **Findings that reveal architectural gaps** — do multiple findings point to a missing
   abstraction or layer?
   Example: 3 different agents flagging "no centralized X" in different territories =
   architectural finding that none of them alone could see.

5. **Trust-but-verify on each agent's P1 claims** — pick the 3-5 highest-impact P1 findings
   and run a one-liner verification (`grep`/`curl`/`jq`/test execution) before treating
   as confirmed P1. Per consulting playbook §7.

## OUTPUT FORMAT

## CROSS-TERRITORY P1 (NEW findings only — do not duplicate Wave 1)
- [XPOL-NNN] description | sources (Agent X + Agent Y) | fix shape | evidence

## VERIFICATION OF WAVE 1 P1s
- {Wave 1 P1 ID}: VERIFIED via {check} | OR FALSE POSITIVE via {check} | OR UNVERIFIED ({reason})

## ARCHITECTURAL FINDINGS (gaps revealed by pattern across multiple agents)
- {description} | evidence (which findings reveal it) | recommended architectural change

## LENGTH BUDGET
1500 words.

## SELF-CRITIQUE MANDATE
After initial cross-pollination pass, second pass: did I just synthesize Wave 1 findings,
or did I genuinely find bugs that require cross-territory reasoning? If I just summarized,
go deeper.
```

---

## Step 5: Verification round — deletion-test agent (sequential after Wave 2)

### Agent 11: deletion-test-agent

**Brief:**

```
You are the deletion-test agent for /sweep. Your job: for EVERY P1 finding (from Wave 1
+ cross-pollination), apply the Three Questions framework to the proposed fix.

## INPUTS
{All confirmed P1 findings with their fix shapes}

## FOR EACH P1, ANSWER:

1. **Where does state live after this fix?** (Does the fix introduce new state? Where?
   Is it isolated, or does it leak across boundaries?)

2. **Where does feedback live after this fix?** (Will the fix be observable in logs/
   metrics/alerts? Or is it a silent change we'll never know shipped correctly?)

3. **What breaks if we revert this fix?** (Blast radius of the fix itself.
   Is the revert clean, or does the fix entangle with other components?)

Plus the fix-introduces-new-bug check:
4. **Does the fix introduce NEW dependencies?** (Calls to new external services? New
   libraries? New code paths that weren't tested before?)

5. **Does the fix change a public API or contract?** (If yes, what depends on the old
   contract? Will the fix break callers?)

## OUTPUT FORMAT

## FIX VALIDATION TABLE
| P1 ID | State location | Feedback location | Revert blast radius | New dependencies | API change |
|-------|---------------|-------------------|---------------------|------------------|------------|
| ... | ... | ... | ... | ... | ... |

## FIXES FLAGGED FOR ADDITIONAL REVIEW
- {P1 ID}: {reason — e.g., "introduces silent failure mode"}

## SELF-CRITIQUE
1. Did I treat each fix's blast radius independently, or assume "small fix = small radius"?
2. Did I check whether the fix re-introduces a previously fixed anti-pattern?
3. For state-introducing fixes, did I verify the new state is testable?

## LENGTH BUDGET
800 words.
```

---

## Step 6: Consolidate and emit verdict

After all agents return:

1. **Dedupe** across Wave 1 + Wave 2 findings (cross-pollination verifier should mark dupes; verify).

2. **Triage by cohort** before severity (per consulting playbook §8):
   - Cohort 1 (no re-run needed): type fixes, redaction, test additions, doc refresh
   - Cohort 2 (re-run needed): prompt revisions, model migrations, schema changes
   - Severity sorts WITHIN each cohort

3. **Apply hard-fail conditions:**

```
HARD FAIL (verdict = NO-GO) if ANY of:
  - P1 from security-attack-surface (after verification)
  - P1 from security-deployment (after verification)
  - P1 from data-integrity (after verification)
  - P1 from cross-pollination-verifier (architectural risks)
  - deletion-test agent flagged a fix as "introduces new failure mode"

SOFT FAIL (verdict = HOLD — operator decides) if:
  - P2 findings exist
  - Any agent self-critique flagged an unverifiable claim

PASS (verdict = GO) if:
  - All P1s verified clean OR explicitly waived with documented justification
  - No deletion-test red flags
```

4. **Write report** to `.sessions/sweeps/sweep-{TODAY}-{COMMIT_SHA}.md`:

```markdown
# /sweep — {project} — {TODAY}

**Verdict:** GO / HOLD / NO-GO
**Project:** {PROJECT_ROOT}
**Commit:** {COMMIT_SHA}
**Live URL:** {LIVE_URL or "(none — code-only sweep)"}
**Agents dispatched:** {N} ({list})
**Wall clock:** {duration}

## TL;DR
{One paragraph: what's deploy-ready, what's blocking, what to do next}

## P1 — Blocks Deploy (Cohort 1: no re-run needed)
- ...

## P1 — Blocks Deploy (Cohort 2: re-run needed)
- ...

## P2 — Fix Before Client Share
- ...

## P3 — Polish, Post-Deploy
- ...

## Cross-Pollination Findings (architectural patterns)
- ...

## Deletion-Test Flags (fixes requiring additional review)
- ...

## Verification Records
- {P1 IDs verified vs flagged false-positive}

## Recommended Action Order
1. ...
2. ...

## Next Sweep Priors (auto-inserted into next handoff's Audit Directions slot)
- {What to focus on in next sweep based on this sweep's findings}
```

5. **Auto-update next handoff's Audit Directions slot** if a current handoff exists at `.sessions/handoffs/`.

6. **Surface verdict to operator:**

```
/sweep complete: {verdict}

{If GO:}     ✓ Deploy-ready. {N} P2 + {M} P3 findings logged for next iteration.
{If HOLD:}   ⚠ Decision required. {N} P2 findings; review report and decide go/no-go.
{If NO-GO:}  ✗ DO NOT DEPLOY. {N} P1 findings block deploy. Report at {report path}.

Manual eyes-on still required (consulting playbook §13: manual + automated catch
different bug classes). Do not treat /sweep PASS as sufficient by itself.
```

---

## Important behaviors

**Trust-but-verify discipline.** Per consulting playbook §7 v1.7 update: every agent claim about production state ("X is broken", "Y is missing") gets a one-liner verification (`grep`/`curl`/`jq`) before being treated as confirmed P1. The cross-pollination verifier handles this.

**Manual + automated parity.** /sweep automates the AUTOMATED half of the manual+automated discipline (consulting playbook §13). It does NOT replace the operator's manual walkthrough. Surface this in the verdict output every time.

**Wait-one-natural-cadence-run discipline.** If the operator invokes /sweep right after multiple force-runs / backfills / manual cycles, the live state may reflect dev churn. Recommend deferring deploy declaration until at least one natural scheduled run has produced clean state. (Per consulting playbook §13.5, integrated v1.7.)

**Adversarial framing per agent.** Every brief includes "Don't review. Try to BREAK this." Agents that posture as graders rather than adversaries miss critical findings.

**Self-critique mandate per agent.** Already proven on brett (consulting playbook §7) — the second pass catches what the first pass misses. Non-negotiable.

**No automated fixing.** /sweep produces findings + verdict. Operator approves each fix. (Per design doc non-goal.)

---

## Cross-references

- **Single-checklist alternative for non-public deploys:** `pre-ship` skill (`$HOME/.claude/skills/pre-ship/SKILL.md`)
- **Audit prompt templates** (per-territory, used by agents): `$KB_ROOT/future-reference/templates/audit-protocol/`
- **AI Security knowledge** (OWASP LLM Top 10, attack vectors): `$KB_ROOT/LEARNING/PRODUCTION/ai-security/ai-security.md`
- **Anti-pattern catalog A1-A20:** `$KB_ROOT/future-reference/playbooks/signalworks-consulting.md` Anti-Patterns Library
- **Multi-agent orchestration patterns:** `$KB_ROOT/future-reference/playbooks/multi-agent-orchestration.md`
- **Pre-deploy SaaS failure modes:** `$KB_ROOT/future-reference/playbooks/building-ai-saas.md`

---

**Provenance:** Designed 2026-04-27 (v1.8 patch). Source: brett-roberts-la-metro engagement experience (manual sub-agent dispatch failure mode), consulting playbook §13 (multi-agent audit discipline), pre-ship skill (deployment safety taxonomy), AI Security KB (OWASP LLM Top 10 + 6 attack classes).

---

## v1.9.1 Calibration Notes (2026-04-27 dogfood on brett-gove-intell)

First /sweep dogfood (2026-04-27, brett-gove-intell HEAD `51ca9fd`) ran 3 of the 9-12 agents (security-attack-surface, code-correctness, docs-operability) and surfaced calibration findings worth integrating into every dispatch:

**1. Path portability (FIXED in v1.9.1):** All KB references now use `$KB_ROOT` env var with `~/AI-Knowledgebase` default. Configuration section at top of skill explains. Hard-fails if `$KB_ROOT` is missing rather than silently loading wrong context.

**2. Live URL detection (FIXED in v1.9.1):** Step 1 regex now matches scheme-less domain patterns (`gov.signalworks.live`, `*.pages.dev`, `*.vercel.app`, `*.netlify.app`, `*.fly.dev`) in addition to fully-qualified `https?://` URLs.

**3. A18 vs A4 distinction (apply to code-correctness brief):** A18 is **narrow-catch** — recovery handler exists but exception class is too narrow, so recovery NEVER FIRES (e.g., `except RuntimeError` when production hits `TimeoutError`). A4 is **silent-fail** — recovery EXISTS and fires but suppresses the error (e.g., `except Exception: return []` instead of raising). When dispatching code-correctness agent, ensure both are listed as distinct hunt categories with this clarification — they're often confused.

**4. Lockfile hash coverage check (apply to security-attack-surface brief):** When `requirements-lock.txt` exists, verify ALL packages have `--hash=sha256:...` lines, not just spot-check the obvious ones (e.g., spacy model wheel). `grep -c "sha256" requirements-lock.txt` should ≈ count of `==` pinned versions. Partial hash coverage = supply-chain typosquat / registry-compromise gap.

**5. Sibling-repo findings marker:** When a finding depends on a sibling repo (e.g., security headers in dashboard repo separate from app repo), mark as `requires-sibling-repo-verification` rather than asserting fix shape blindly. The sweep operator may not have visibility into the sibling repo from the current sweep context.

**6. `page.evaluate()` JS injection (apply to security-attack-surface brief):** When project uses Playwright with `page.evaluate(js_string)`, audit whether `js_string` is a static literal or could be tainted by scraped content. Static = clean; dynamic = JS-template-injection risk.

**7. Always emit threat-model.md absence finding:** If `$PROJECT_ROOT/docs/plans/threat-model.md` is missing (project pre-dates /cook v1.8 OR was scaffolded without v1.8), emit standing finding [SEC-NNN-sc]: "No threat model documented — defaulted audit posture to 'untrusted public exposure'. Recommend scaffolding from `$KB_ROOT/future-reference/templates/threat-model-template.md`."

**8. Doc-vs-doc contradictions (apply to docs-operability brief):** Add to hunt category 1 (Doc rot): check for cross-doc contradictions, not just doc-vs-code. Example surfaced on brett: README says SMTP is configured, completion handoff says "skipped Zoho alerter setup", `.env.example` shows Gmail not Zoho — three docs, three different stories.

**9. Docs agent length budget bump:** For projects with >10 handoff files OR >5 architectural docs, raise docs-operability budget from 900 → 1100 words. Brett project hit this.

**10. Pytest invocation portability:** When projects work-around path issues via `PYTHONPATH=. pytest`, brief should specify the canonical invocation rather than assuming `pytest` works bare. Otherwise agent reports "tests pass" or "tests fail" based on stale environment.

**Status:** items 1+2 fixed in v1.9.1 SKILL.md. Items 3-10 documented here for agent dispatch context — operator should reference these notes when filling agent briefs (until v1.10 integrates them as automatic brief enrichment).

**Real production bug caught on first dogfood:** CORR-001 — three brett-gove-intell scrapers (la_metro, inglewood, lacoe_trustees) silently swallowed exceptions and returned `[]` instead of raising, classifying real outages as "quiet day" instead of "degraded source." Fixed in brett commit `d544c84`. Validates the /sweep design.
