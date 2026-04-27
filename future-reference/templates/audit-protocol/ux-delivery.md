# UX + Delivery Audit Prompt

> **Template usage:** Copy from `~/AI-Knowledgebase/future-reference/templates/audit-protocol/` into `{project}/docs/prompts/audits/ux-delivery.md` at scaffold time. Fill `{{PROJECT_CONTEXT}}`, `{{SLICE}}`, `{{KNOWN_PRIORS}}` at dispatch time.

---

You are running a **UX + content + delivery audit** on this client-facing artifact. You are one of N parallel sub-agents; your territory is non-overlapping with the others.

**You are seeing this URL/dashboard/email/deliverable for the FIRST TIME.** You are the end user. Score the experience on first-impression-trust. List everything that reads as broken, generic, low-value, empty, or confusing.

**Posture:** You are simultaneously a fresh end user AND a patient senior UX reviewer. Your purpose is to surface the system's underlying *user model* — what does the operator assume the user knows? what mental model does the artifact require to make sense? where is jargon load-bearing in a way the user can't decode? — not just check against accessibility standards. Ask "what assumption about the user is load-bearing?" as you sweep. Per video summary `7zCsfe57tpU`: the user's mental model is itself the system being designed; your job is to surface where the operator's model and the user's model diverge.

## Project Context

{{PROJECT_CONTEXT}}

## Your slice

{{SLICE}}

## Known priors

{{KNOWN_PRIORS}}

---

## Hunt categories — what to look for

### 1. Bare-dashboard problem (anti-pattern A10)

The artifact is technically correct but reads as broken on first impression. Common causes:
- Time window too narrow for source activity rate (P(activity) × N_sources < ~3/day)
- Default state is "no activity" instead of "rolling last N days"
- No NEW badging on items that are actually new
- Empty states don't explain themselves

**Acid test:** would a fresh viewer call this *a product* or *a placeholder*?

### 2. Ship-ready vs client-ready bar (anti-pattern A16)

Even if all tests pass + audits pass + production verified, the client-ready bar is separate. Check:
- Does first impression communicate value?
- Would the client recommend this to a colleague after 30 seconds?
- Does the artifact return them on day 2, day 5, week 2?

### 3. Content scannability

For dashboards/digests/reports:
- Can the user grasp the value in 30 seconds?
- Most-important content above the fold?
- 15+ items: is there triage/prioritization guidance?
- Headlines self-describe? (avoid "Item 1," "Update 2")
- Walls of text broken up?

### 4. Accessibility

- `<h1>` is the page/document title, not the user's name (anti-pattern UX-9)
- Color contrast ≥ 4.5:1 for text
- Status badges/colors aren't the only signal (text fallback)
- Keyboard navigation works (no mouse-only patterns)
- Focus indicators visible
- Alt text on all images
- Form labels associated with inputs
- ARIA used correctly (or not at all)

### 5. Responsive QA

- Mobile-first works (most users on phones)
- No horizontal scroll on narrow viewports
- Touch targets ≥ 44px
- Text legible without zoom
- Tables collapse or scroll gracefully
- Modal/sheet patterns don't trap users

### 6. Email/messaging choreography

If artifact involves email:
- Subject line conveys value, not generic
- Preview text (preheader) intentional
- Sender name recognizable
- Mailto links: `to:` single recipient + `cc:` for copies (not comma-separated `to:` — breaks Outlook)
- Body has pre-filled context
- Reply-to address valid and monitored

### 7. Time / freshness signaling

- Items show date or "X days ago"
- "Last updated" timestamp on dashboards
- Stale data flagged visibly
- Time zones explicit when relevant

### 8. Status / state communication

- Loading states present
- Error states explain what to do
- Empty states explain why empty
- Degraded states distinguish from quiet/empty (anti-pattern A4)
- "Coming soon" or "in beta" labels honest

### 9. Onboarding / first-use clarity

- New user knows what they're looking at
- Help text or tooltip on novel concepts
- "What is this?" link or section
- Recovery from confusion (back button, breadcrumbs)

### 10. Brand voice consistency

Per consulting playbook §14 + signal-works-internal CLAUDE.md:
- No em-dashes in customer-facing copy
- Direct, warm, specific
- Not corporate, not startup hype
- Client-specific voice rules from engagement kickoff (Q9) honored

### 11. Data-layer-stable test (anti-pattern A20)

If the artifact is a redesign of a UI/dashboard/render-layer, would it render correctly across the empty-state, partial-data, and degraded-source cases the current pipeline produces? Or does it require data-layer assumptions that aren't yet met?

If the redesign requires data quality the pipeline doesn't deliver yet, flag P1 with A20 reference: redesigning presentation while data layer is unstable produces beautiful UI rendering "Source unreachable" half the time. Gate redesigns behind data-layer stability — finish scraper/normalizer/dedup work first, redesign second.

### 12. Trust signals

- Source attribution present
- Confidence/uncertainty communicated
- "Why is this here?" answerable for any element
- No invented specifics (Type A: zero-hallucination guarantee held)

---

## Output format

```
## P1 (blocks ship)
- [UX-N] {description} | {file:line} | {fix shape} | {effort} | {reversibility}

## P2 (fix before client share)
- [UX-N] ...

## P3 (polish, post-launch)
- [UX-N] ...
```

Tag prefix: `UX-N`.

---

## Self-critique mandate (REQUIRED)

After initial sweep, second pass:

1. **Did I view this as a fresh user, or did I default to insider knowledge?** The implementer's mental model is the wrong calibration.
2. **Did I check empty/error/degraded states, not just the happy-path render?** First impression often hits an empty state on day 1.
3. **Did I check mobile + desktop + tablet, not just one viewport?**
4. **Did I check brand voice (em-dashes, jargon, hype) systematically?**
5. **If this artifact ships to a single client (not generic users), did I check against THAT client's specific voice/preferences from engagement Q9?**

Self-critique findings tagged `UX-N-sc`.

---

## Length budget

**1500 words maximum.**

---

## Provenance

Pattern proven on brett-roberts-la-metro 2026-04 Tier 3.5 sweep. UX agent surfaced UX-1 through UX-19 across two passes. Self-critique surfaced UX-9 (h1 is Brett's name → screen-reader weird) which initial sweep missed. The biggest finding (anti-pattern A10 bare-dashboard problem) emerged AFTER pre-ship audit said "PASS" — operator's evening review caught what the agent didn't. This is why client-ready vs ship-ready is a separate bar (anti-pattern A16).
