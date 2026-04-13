---
name: pre-ship
description: Pre-deployment safety gate for web apps and software. Runs a structured checklist (security, database, infrastructure, code quality, monitoring) before any production deploy. Use when saying "ready to ship", "deploy to production", "going live", "launch", or "ready to deploy". Always checks intent first — never auto-runs.
origin: KB
---

# Pre-Ship

Production launch gate. Catches the things that cost 10x more to fix after launch.

## Check-In Gate

Before running any checklist, always ask:

"Looks like you're approaching a production deploy. Which mode?

**A) First production deploy** — full checklist (~20 min). Everything from auth to monitoring.
**B) Updating existing production** — abbreviated checklist (~5 min). Just the things that break on updates.
**C) Not deploying yet** — dismiss. Continue building.

Which is it?"

Wait for response before proceeding.

---

## Mode A: Full Checklist (First Production Deploy)

Work through each category. Check off as you go. Surface any unchecked items before proceeding.

---

### Security

- [ ] No API keys, secrets, or credentials in frontend code or committed to git
- [ ] `.env` files in `.gitignore` — verify with `git status`
- [ ] Every route checks authentication (audit ALL endpoints, not just the obvious ones)
- [ ] HTTPS enforced everywhere — HTTP redirects to HTTPS
- [ ] CORS locked to your domain — no wildcard (`*`) origins
- [ ] Input validated and sanitized server-side (not just client-side)
- [ ] Rate limiting on auth endpoints and sensitive operations
- [ ] Passwords hashed with bcrypt or argon2 (not MD5, SHA1, or plain)
- [ ] Auth tokens have expiry set
- [ ] Sessions invalidated server-side on logout
- [ ] Security headers set: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- [ ] Dependencies scanned: `npm audit` run, critical vulnerabilities resolved

---

### Database

- [ ] Backups configured AND tested — test the restore, not just the backup
- [ ] Parameterized queries everywhere — no string concatenation in SQL
- [ ] Separate development and production databases (never shared)
- [ ] Connection pooling configured
- [ ] Migrations in version control — no manual schema changes
- [ ] App connects as a non-root database user with minimum required permissions
- [ ] Production database credentials are not in the codebase

---

### Infrastructure & Deployment

- [ ] All environment variables set on the production server
- [ ] SSL certificate installed, valid, and auto-renewing
- [ ] Firewall configured — only ports 80 and 443 open publicly
- [ ] Process manager running: PM2, systemd, or platform equivalent
- [ ] Staging test passed before production deploy
- [ ] Rollback plan exists and has been tested (see `deployment-patterns` for rollback commands)
- [ ] Docker image uses pinned version tags (not `:latest`)
- [ ] Health check endpoint returns meaningful status at `/health`
- [ ] Resource limits set (CPU, memory) if containerized

---

### Code Quality

- [ ] No `console.log` statements in production build
- [ ] Error handling on all async operations
- [ ] Loading and error states visible in UI
- [ ] Pagination on all list endpoints (no unbounded queries)
- [ ] Structured logging — JSON format, no PII in logs

---

### Monitoring

Before going live, you need visibility into what's happening. Four non-negotiables:

- [ ] **Error tracking** — Sentry, Bugsnag, or equivalent. Captures uncaught exceptions with stack traces.
- [ ] **Uptime monitoring** — Better Uptime, UptimeRobot, or equivalent. Alerts when the app goes down.
- [ ] **Log aggregation** — Logtail, Datadog, or platform logs. Searchable, structured logs in one place.
- [ ] **Alerting** — Error rate threshold alert configured. You find out before users do.

Quick setup (no-cost options):
- Error tracking: Sentry free tier (5K errors/month)
- Uptime: UptimeRobot free tier (50 monitors, 5-min checks)
- Logs: Logtail free tier or Railway/Render/Vercel built-in logs
- Alerts: Slack webhook from any of the above

---

### Final Gate

Can't check every box? **You are not ready to ship.**

The post-launch patch costs 10x more than the pre-launch fix.

If items are intentionally deferred (e.g., monitoring for a private beta), document why and set a deadline. Don't silently skip.

---

## Mode B: Abbreviated Checklist (Updating Existing Production)

For routine updates — things that break on deploys even when the base setup is solid.

- [ ] No new secrets added to frontend code
- [ ] New routes have authentication checked
- [ ] Database migrations are backward-compatible (no destructive changes without a plan)
- [ ] Migration tested against production-sized data
- [ ] Rollback tested: can you revert if something breaks?
- [ ] Staging deploy passed before production
- [ ] `npm audit` if dependencies changed
- [ ] No `console.log` in new code

---

## Cross-References

- **How to set up deployments** (CI/CD pipelines, Docker, blue-green, canary strategies): see `deployment-patterns`
- **Rollback commands** (kubectl, Vercel, Railway): see `deployment-patterns` → Rollback Strategy
- **Environment configuration patterns** (12-factor, Zod validation): see `deployment-patterns` → Environment Configuration
- **Health check implementation**: see `deployment-patterns` → Health Checks
