---
name: pre-flight-verify
description: Use BEFORE writing any code that integrates with an external service, package, model, or third-party UI. Fetches current docs and verifies the integration shape against your assumption. Prevents drift on package versions, model names, API endpoints, UI flows, pricing, and tool schemas. Trigger reflexively whenever new external integration code is about to be written.
---

# Pre-Flight Verify

## Why this exists

Training-data memory of fast-moving external services drifts. Package versions move, models get deprecated, dashboard UIs redesign, pricing changes, tool/permission schemas evolve. Code written from memory often hits one of these drifts at runtime — at which point you've already paid the scaffolding cost.

**A 5-minute doc-fetch BEFORE writing the integration is cheaper than a 30-minute debug AFTER it fails.**

This is the highest-leverage behavior change available. Skipping it is the single most common cause of "scaffold compiles but breaks at first run."

## When to invoke (reflexive triggers)

Run this BEFORE writing or modifying code that touches:

- **npm package versions** — especially in fast-moving ecosystems (AI SDKs, ORMs, frameworks). Verify against npmjs.com or `npm view <pkg> version`.
- **Model names** — LLM providers deprecate models on 6-week cycles. Verify the exact model string against the provider's current docs.
- **API endpoints / method signatures** — REST endpoints get renamed; SDK methods get added/removed.
- **Third-party UI flows** — Supabase dashboard, OAuth provider pages, OpenAI console. Click-by-click instructions go stale fast.
- **Pricing / rate-limit assumptions** — free tiers shrink, prepaid minimums get added, request fees change.
- **Tool / permission schemas** — web_search tool factory names, MCP tool definitions, OAuth scope strings.
- **External library imports** — when an SDK has a v2→v3 jump, the import paths often change.

## Workflow

1. **Identify the assumption.** Name what you're about to write — exact package version, model name, endpoint, UI step, pricing claim.

2. **Fetch current source.** In priority order:
   - Official docs page (most authoritative for API shape)
   - Package registry page (npmjs.com — most authoritative for versions)
   - Recent changelog (catches breaking changes since memory)
   - GitHub repo for the SDK/library (source of truth when docs lag)

3. **Compare and decide.** Three outcomes:
   - **Match.** Your assumption is current. Proceed and note "verified against [source] on [date]" in code comment or commit message.
   - **Drift.** Assumption is stale. Update before writing. Note both old and new in your verification report.
   - **Abort.** The integration shape changed materially. Pause and re-plan with the operator.

4. **Document the verification.** Surface a short verification block in the conversation:

```
## Pre-flight: [service/package/model]
- Source: [URL]
- Assumption: [what I was about to write]
- Reality: [what's actually current — quote exact field/version/path]
- Action: [proceed / update / abort]
```

## Skip when

- Fully vendored code (no external network call at runtime, no external API)
- The doc was fetched within the last hour and nothing has changed
- Trivial config tweak that doesn't change integration shape
- Operator explicitly says "skip — I'll verify by running it"

## Cost

5 minutes per integration. Pays back the moment one verification catches a drift.

## What this prevents (failure mode catalog)

When skipped, these are the common failures:

- `npm install` errors because a package's major version doesn't match what was specified
- API returns 404 or 401 because a model/endpoint name was deprecated
- UI walkthrough doesn't match because the dashboard redesigned (Supabase 2024→2026, OpenAI console post-Responses-API)
- Pricing assumption blows past free tier or burns budget unexpectedly (Perplexity $5 free credit was deprecated; minimum is $50 prepaid)
- Tool factory name changed (`anthropic.tools.webSearch_20250305` instead of older variants)
- Citation field changed location (`result.sources` in Vercel AI SDK v3, vs. older `providerMetadata.*.citations`)

## Integration with other skills

- **`last30days`** — broader, surfaces what practitioners discovered. Use when the question is "what's recent in this space" (research mode).
- **`pre-flight-verify`** — narrower, verifies a specific assumption. Use when the question is "is this exact claim still true right now" (build mode).

Both can fire on the same task: `last30days` first to surface the landscape, `pre-flight-verify` per-integration before code.
