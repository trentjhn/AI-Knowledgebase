# {PROJECT_NAME} — Threat Model

> **Template usage:** Scaffolded by `/cook` v1.8 Phase 5 into every new project's `docs/plans/threat-model.md`.
> Not a 50-page document — a 1-page structured artifact that answers Phase 0.6 + 0.9 questions formally.
> Update at every major architectural change; reviewed at every `/sweep` invocation.

**Created:** {YYYY-MM-DD}
**Last reviewed:** {YYYY-MM-DD}
**Project type:** Type A (AI deliverable) / Type B (AI-accelerated build) / Hybrid
**Exposure level:** Public / Auth-gated / Internal / Local-only

---

## Actors — Who could attack

[List specific actor categories from Phase 0.6 Q11.9 — pruned to realistic threats only]

| Actor | Motivation | Capability | Realistic? |
|---|---|---|---|
| Script kiddies | Opportunistic exploitation, defacement | Low-skill (use known tools) | yes/no |
| Competitors | Competitive intel, sabotage | Moderate (targeted reconnaissance) | yes/no |
| Insider threat | Disgruntled access, mistake | High (legitimate access) | yes/no |
| Nation-state | Espionage, supply chain | Very high (sophisticated) | yes/no |
| Legitimate-user-misuse | Confusion, accidental data exposure | Low (no malice, but can cause damage) | yes/no |

---

## Assets — What attackers want

[List from Phase 0.6 Q11.7 — what's actually in this system that has value]

| Asset | Value to attacker | Where stored | Access controls |
|---|---|---|---|
| User credentials | Account takeover, lateral movement | {db / vault / sessions} | {auth + encryption + ...} |
| PII (names/emails/etc.) | Resale, identity theft | {db / logs / backups} | {auth + access logging + ...} |
| Financial data | Direct theft, fraud | {db / payment processor / logs} | {auth + encryption + audit + ...} |
| Business logic / system prompts | IP theft, jailbreak vector | {code / config / prompts} | {repo privacy + secret management + ...} |
| Compute resources | Crypto mining, DDoS pivot | {servers / GPU / API quotas} | {rate limiting + monitoring + ...} |
| Reputation / brand trust | Reputational damage, defacement | {public surfaces} | {WAF + monitoring + incident response} |

---

## Threats — Specific attack vectors

[Map Phase 0.6 + 0.9 + ai-security.md OWASP LLM Top 10 to THIS project's actual surfaces]

### Threat 1: {e.g., Indirect prompt injection via scraped content}

- **Actor:** {Nation-state via compromised source / Legitimate-user-misuse via untrusted upload / etc.}
- **Surface:** {Where the attack enters — e.g., agent reads governance documents from third-party sites}
- **Impact if successful:** {Specific bad outcome — e.g., agent exfiltrates client PII to attacker-controlled server}
- **Likelihood:** Low / Medium / High (per Phase 0.6 worst-case)
- **Severity:** Low / Medium / High / Critical

### Threat 2: {e.g., Credential leakage via committed secrets}

- ...

### Threat 3: {e.g., Vector store poisoning}

- ...

[Add as many as the project's surfaces warrant — typically 3-8 for a focused threat model]

---

## Defenses — What we have

[Concrete defenses scaffolded or implemented; each defense should map to ≥1 threat above]

### Defense layer 1: Network / infrastructure

- [ ] HTTPS enforced everywhere
- [ ] Firewall configured (only 80/443 publicly)
- [ ] CORS scoped to specific origins (no wildcards)
- [ ] Cloudflare Access whitelist (if deployed via CF Pages)
- [ ] Default branch protection rules

### Defense layer 2: Application / auth

- [ ] Every route checks authentication
- [ ] Auth tokens have expiry; sessions invalidated on logout
- [ ] Passwords hashed with bcrypt/argon2
- [ ] Rate limiting on auth endpoints + sensitive operations
- [ ] Input validated server-side (not just client-side)
- [ ] Output sanitized (HTML escape, URL scheme allowlist for model-authored hrefs)

### Defense layer 3: Secrets / credentials

- [ ] No secrets in git history (`git log -p | grep` clean)
- [ ] `.env` in `.gitignore`
- [ ] `.env.example` placeholders only
- [ ] Production secrets via vault / `gh secret set` / equivalent
- [ ] Centralized secret redactor in error logs (anti-pattern A13)

### Defense layer 4: AI-specific (if Type A)

- [ ] Spotlighting / taint tracking on model input (per ai-security.md §4)
- [ ] Output validation gates (grounding check, NER gate, allow-list)
- [ ] Tool/permission scoping (least privilege per agent action)
- [ ] System prompt does not contain credentials or business secrets
- [ ] Eval framework with regression gate before prompt revisions ship
- [ ] Prompt versioning with changelog

### Defense layer 5: Data integrity

- [ ] Every persisted item has stable `content_hash` (or equivalent ID)
- [ ] Schema validation at ingestion + retrieval boundaries
- [ ] Defensive normalizers for upstream data quirks
- [ ] DB queries parameterized (no string concat in SQL)
- [ ] Backups configured AND TESTED (test restore, not just backup)

### Defense layer 6: Observability / response

- [ ] Error tracking (Sentry/Bugsnag/equivalent)
- [ ] Uptime monitoring with alerts
- [ ] Log aggregation
- [ ] PII redaction in logs (not just secrets)
- [ ] Alerting threshold configured (you find out before users do)

---

## Residual risks — Known gaps with rationale

[What we KNOW is not yet defended, why we accept the risk, what would change our mind]

| Gap | Why accepted | Trigger to revisit |
|---|---|---|
| {e.g., No WAF in front of public endpoint} | {Cost vs current threat level not justified for v1} | {Sustained scraping attempts OR attempted SQL injection in logs} |
| {e.g., Single-region backup only} | {RTO of 4 hrs acceptable for v1; multi-region adds cost without near-term value} | {SLA negotiation with client requires sub-hour RTO} |
| {e.g., No third-party penetration test yet} | {v1 budget; defer to post-launch quarter} | {Before any compliance audit OR public marketing push} |

---

## Defense-to-threat traceability

[For each major threat above, list the defenses that mitigate it. Surface gaps where threats have no defense]

- **Threat 1 (Indirect prompt injection):** Mitigated by Defense 4 (spotlighting + output validation). Gap: input source whitelist not enforced; could surface in /sweep.
- **Threat 2 (Credential leakage):** Mitigated by Defense 3 (full layer). No known gaps.
- **Threat 3 (Vector store poisoning):** Mitigated by Defense 4 (RAG-specific). Gap: no signing on ingested documents.

---

## Review cadence

- **Updated at:** every major architectural change (new external integration, new auth surface, new persistent store, model migration)
- **Reviewed at:** every `/sweep` invocation (security-attack-surface agent reads this file as part of context)
- **Audited at:** quarterly (operator manual review) OR whenever Phase 0.6 worst-case-impact answer changes

---

**Provenance:** Template scaffolded by `/cook` v1.8 Phase 5 (designed 2026-04-27). Format draws from Phase 0.6 + 0.9 questions, OWASP LLM Top 10, and consulting playbook security patterns.
