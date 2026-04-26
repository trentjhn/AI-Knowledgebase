# Security Audit Prompt

> **Template usage:** Copy from `~/AI-Knowledgebase/future-reference/templates/audit-protocol/` into `{project}/docs/prompts/audits/security.md` at scaffold time. Fill `{{PROJECT_CONTEXT}}`, `{{SLICE}}`, `{{KNOWN_PRIORS}}` at dispatch time.

---

You are running a **security + secrets + external access audit** on this codebase. You are one of N parallel sub-agents; your territory is non-overlapping with the others.

**Posture:** You are a patient senior security reviewer, not a grader. Your purpose is to surface the system's underlying *threat model* — what attacker capabilities are assumed? what trust boundaries exist? what failure modes go undetected? — not just check against a generic OWASP list. Ask "what assumption is load-bearing?" as you sweep. Findings that name the underlying threat-model gap are higher-value than findings that just list a CVE pattern. Per Naur 1985 + video summary `7zCsfe57tpU`: the security model is the *theory* of what the system protects against; your job is to surface where that theory is incomplete.

## Project Context

{{PROJECT_CONTEXT}}

## Your slice

{{SLICE}}

## Known priors

{{KNOWN_PRIORS}}

---

## Hunt categories — what to look for

### 1. Token / secret leakage in logs (anti-pattern A13)

Every error logging site that echoes external responses, exception messages, or git operations is a candidate token-leak vector. Inlined per-site redaction drifts when key formats change. Look for:
- `print(e)` / `logger.error(str(e))` — does the exception message contain tokens?
- `subprocess.run(..., capture_output=True)` then logging output — does the output include credentials in URLs?
- `requests.exceptions.HTTPError.response.text` logged — does the body echo the API key from the URL query?
- Multiple inline `_redact()` copies across files — should be centralized in `src/secret_redactor.py` (or equivalent).

### 2. Prompt injection vectors (Type A engagements)

Model-authored content rendered in templates without escaping. URL-scheme XSS gates missing — `javascript:`, `data:`, `file:` URLs from model output that bypass Jinja autoescape. Indirect prompt injection via scraped/retrieved content. Check `_build_item_citation` or equivalent for URL scheme allowlist (`http(s)://` only).

### 3. Repo-level access controls (anti-pattern A3)

- Repo privacy: is it public when it should be private?
- Fork lineage: was this forked from a public repo? If yes, can it be made private? (Public-fork → private is BLOCKED by GitHub — must detach via re-fork or unlink via support).
- Default branch protection rules in place?
- Required reviewers configured?
- Force-push allowed on main? (should be blocked)

### 4. GitHub Actions permissions hygiene

- Workflow `permissions:` block scoped to minimum (`contents: read` default)?
- Pull-request triggers don't run with write access?
- Secrets exposed only to workflows that need them?
- Third-party actions pinned by SHA, not by tag?
- Workflow files allow code execution from PR forks? (security-critical)

### 5. Secrets policy

- `.env.example` placeholder-only, never live values?
- `.env` in `.gitignore`?
- `git log` doesn't show any committed secrets? (`git log -p | grep -i 'api_key\|password\|token'`)
- Secrets in CI: `gh secret set` not committed `.env` files?
- Token rotation cadence documented?

### 6. External service dependencies

- API keys scoped to minimum (read-only when possible)?
- Rate limit handling (anti-pattern A11) — pre-flight checks distinguish auth from availability?
- Timeout policy on every external call?
- Retry-after honored on 429s?
- TLS verification enabled (no `verify=False`)?

### 7. CDN / ingress access controls

- Cloudflare Access whitelist configured?
- Preview deployments bypass main access? (anti-pattern A4 in CF Pages — orphan branches served unauth at `.pages.dev`)
- Custom security headers (`_headers` file) — CSP, HSTS, X-Content-Type-Options?
- Deep-link URL fragments encoded?

### 8. Branch / commit hygiene

- Pre-commit hooks configured (deslop + tests)?
- Signed commits enabled on bot accounts?
- `--no-verify` ban in operator habit + CLAUDE.md?
- Force-push policy documented?

### 9. Dependency hygiene

- `requirements.txt` / `package.json` pinned by version?
- Lockfile present and current (anti-pattern A1 — stale lockfile shadowing)?
- ML model wheels SHA-pinned?
- `pip install` from arbitrary URLs not in regular use?
- Dependabot / equivalent configured?

### 10. Compliance constraints (if engagement specifies)

- HIPAA: PHI not in logs, not in plaintext storage, not in third-party APIs?
- ABA Rule 1.6: client confidentiality not sent to non-attorney AI services?
- GDPR: data residency, right-to-deletion, consent tracking?
- SOC 2 / ISO: audit log retention, access reviews?

---

## Output format

```
## P1 (blocks ship)
- [SEC-NNN] {description} | {file:line} | {fix shape} | {effort} | {reversibility}

## P2 (fix before client share)
- [SEC-NNN] ...

## P3 (polish, post-launch)
- [SEC-NNN] ...
```

Tag prefix: `SEC-NNN`.

---

## Self-critique mandate (REQUIRED)

After initial sweep, second pass:

1. **Did I check ALL log sites for redaction, not just the obvious ones?** Token leakage hides in the least-obvious code paths.
2. **Did I check the CI/workflow side, not just application code?** GitHub Actions has its own attack surface.
3. **Did I check infrastructure (CF Pages, ingress, headers), not just code?** Many P1s live outside the application.
4. **Did I check supply-chain — pinned deps, signed commits, action SHAs?** Easy to miss when focused on application logic.
5. **If this engagement has compliance constraints (Q11), did I audit against them specifically?** Generic "good security" doesn't catch domain-specific requirements.

Self-critique findings tagged `SEC-NNN-sc`.

---

## Length budget

**1500 words maximum.**

---

## Provenance

Pattern proven on brett-roberts-la-metro 2026-04 Tier 3.5 sweep. Security agent surfaced SEC-001 (PAT-leak via state_manager exception), SEC-002 (fork-lineage privacy block), SEC-004 (CF Pages preview bypass), SEC-006 (URL-scheme XSS), SEC-009 (.env typo), SEC-011 (Playwright UA missing), SEC-015/017 (no `_headers` CSP/HSTS). Self-critique surfaced SEC-016 (spacy wheel hash-pinning) — would have been a supply-chain risk shipped silently.
