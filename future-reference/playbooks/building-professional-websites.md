# Playbook: Building Professional Websites with AI

> **Use this when:** You're building a marketing site, business site, personal site, or any public-facing web presence using AI tools. The protocol is transferable across project types (gym, personal brand, small business, portfolio) — what changes is the content and aesthetic direction, not the process.

---

## The Core Problem This Solves

AI defaults to the statistical average of its training data. The result is what practitioners call "AI slop": Inter font, purple-to-blue gradients, cards nested in cards, centered layouts, glassmorphism decorations, and generic stock-photo heroism. These aren't bugs — they're the *modal output* of training on the web. Every LLM learned from the same templates.

This playbook fights that bias with three mechanisms:
1. **Context before generation** — the agent knows who this is for and what it should feel like before writing a single line of code
2. **A design contract (DESIGN.md)** — a plain-text file that encodes your visual system, readable by any agent
3. **Quality gates** — explicit review steps that catch AI fingerprints before they ship

---

## Tool Stack

These tools map to specific phases of the workflow. Install what you'll use:

| Tool | Phase | Install |
|------|-------|---------|
| **Impeccable** | Design + Quality | `/plugin marketplace add pbakaus/impeccable` |
| **interface-design** | Design memory | `/plugin marketplace add Dammyjay93/interface-design` |
| **ui-skills** | Quality gates | `npx skills add ibelick/ui-skills` |
| **Emil Kowalski skill** | Animation (selective) | `npx skills add emilkowalski/skill` |
| **spec-kit** | Project scaffolding | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` |
| **FontofWeb** | Font discovery | fontofweb.com (MCP available) |
| **Supahero / footer.design / navbar.gallery** | Reference inspiration | Web (no install) |

---

## Phase 0: Project Intelligence

**Before any design work begins.** The agent needs to know who this is for before it can make good decisions. Context you cannot derive from code.

Create a `PROJECT.md` in the project root with these fields filled out:

```markdown
# Project Intelligence

## What this is
[One sentence: "A marketing site for CrossFit Ironside, a functional fitness gym in East Oakland."]

## Target audience
[Who visits this site, what they want, what they already know]

## Primary goal
[The one action a visitor should take: Book a class / Contact for a quote / Buy a product]

## Brand personality
[3 adjectives that describe the feel: "Raw, honest, community-driven" / "Premium, minimal, confident"]

## What this is NOT
[Explicit anti-goals: "Not corporate, not intimidating, not stock-photo-gym"]

## Competitors / reference sites
[2-3 URLs of sites that get the vibe right — not necessarily same industry]

## Content inventory
[What pages exist: Home, About, Classes, Pricing, Contact]
[What media exists: Own photos? Logo? Video?]
```

**Why this matters:** The Impeccable SKILL.md is explicit — "You cannot infer this context by reading the codebase. Code tells you what was built, not who it's for or what it should feel like." Running `/teach-impeccable` generates this context from conversation. You can also write it directly.

---

## Phase 1: Design System (DESIGN.md)

**Output: a `DESIGN.md` file in the project root.**

DESIGN.md is the design counterpart to AGENTS.md — a plain-text design system that any agent reads before generating UI. It encodes colors, typography, spacing, component rules, and do's/don'ts. Every screen the agent generates afterward follows the same visual contract.

### Option A: Generate from vibe description (fastest)
Describe the aesthetic to the agent and have it produce DESIGN.md. In Stitch/Antigravity:
```
A minimal, confident site for a functional fitness gym. Dark background (#0D0D0D),
warm white text, single accent in amber/orange. Bold display type, raw photography.
No corporate energy, no stock photos. Think Notion docs meets CrossFit Journal.
```

### Option B: Extract from existing brand
Provide your logo URL or website. The agent extracts the palette, type choices, and style patterns.

### Option C: Write it directly
Use this template:

```markdown
# Design System: [Project Name]

## Overview
[1-2 sentences describing the site's visual personality and intent]

## Colors
- **Primary**: [hex + when to use it: CTAs, active states, key actions]
- **Background**: [hex — primary page background]
- **Surface**: [hex — card/panel background]
- **Text primary**: [hex]
- **Text secondary**: [hex]
- **Accent**: [hex — used sparingly, max 10% visual weight]
- **Error**: [hex]
- **Border**: [hex]

## Typography
- **Display / Headlines**: [Font name, weight, tracking]
- **Body**: [Font name, weight, size range, line-height]
- **Labels / UI**: [Font name, weight, size]
- **Measure**: max-width 65ch for body text

## Spacing
- Base unit: 4px
- Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128px
- Section padding: [value for desktop and mobile]

## Components
- **Buttons**: [border-radius, height, padding, primary style]
- **Cards**: [use only when content is genuinely distinct; no nested cards]
- **Inputs**: [border style, focus state]
- **Navigation**: [sticky or static, background treatment]

## Motion
- Default duration: 200-300ms for interactions, 400-600ms for transitions
- Easing: ease-out on entrance, ease-in-out for transitions
- Animate only: transform and opacity (never width/height/margin/padding)

## Do's
- [Specific things that reinforce the brand feel]
- Keep primary accent color to <10% visual weight
- Use whitespace as a design element, not filler

## Don'ts
- [Explicit anti-patterns for this specific project]
- No generic stock photography
- No Inter font (unless deliberately chosen with rationale)
- No card grids as default layout
```

### Committing to a Direction

Once DESIGN.md exists, run:
```
/interface-design:init
```

This reads the design system and saves persistent decisions to `.interface-design/system.md`. Spacing values, depth strategy, surface elevation — decided once, applied consistently across every session. Without this, decisions drift: buttons are 36px today, 38px tomorrow, 40px next week.

---

## Phase 2: Tech Stack Decision

Choose based on project requirements:

| Need | Stack |
|------|-------|
| Fast static marketing site, SEO critical | **Astro** + Tailwind + Motion |
| React-based, needs interactivity | **Next.js** + Tailwind + shadcn/ui + Motion |
| Fully custom, no framework preference | **Vite** + Vanilla JS/TS + Tailwind |
| Client wants CMS | Astro or Next.js + **Sanity** or **Contentful** |
| Needs 3D / immersive hero | Above + **Spline** or **Three.js** |

**For most marketing/business sites: Astro + Tailwind CSS + Motion is the right answer.** Astro ships zero JS by default, has near-perfect Lighthouse scores, and has excellent island architecture for interactive components.

**Animation libraries:**
- **Motion (framer-motion)** — the default for React component animations
- **GSAP** — for scroll-driven animations, timeline sequences, complex entrance effects; the professional choice for agencies
- **Lottie** — pre-built animations (use for illustration-style motion, not UI)

**3D:**
- **Spline** — no-code 3D scenes embeddable as iframes or via React component; production-ready
- **Three.js** — full control, much more complex; only if Spline can't do what you need

---

## Phase 3: Spec and Architecture

Using **spec-kit**:

```bash
specify init . --ai claude
```

This scaffolds the spec structure. Then create your feature specification:

```bash
specify feature "homepage"
```

The spec covers: user stories, technical approach, component inventory, page structure, API/data needs, edge cases.

**Page inventory for a standard marketing site:**
- `/` Home (hero, value prop, social proof, CTA)
- `/about` Brand story, team
- `/services` or `/[type]` What they offer
- `/contact` Form or booking link
- `404` Custom error page

For each page, specify:
- **Hero treatment**: What's above the fold? The hero is the only section that will definitely be seen.
- **Content priority**: What must a visitor know in 5 seconds?
- **CTA**: One per page, clear, specific
- **Scroll behavior**: Any animation or parallax intent?

---

## Phase 4: Build Protocol

### Order matters

Build in this sequence — don't jump to hero animations before the design system is applied everywhere:

1. **Design tokens** — CSS variables or Tailwind config with your DESIGN.md values before any components
2. **Typography** — set the type system globally; test with real content (not lorem ipsum)
3. **Navigation** — sticky or static, mobile hamburger, consistent across all pages
4. **Layout shells** — page containers, grid system, section spacing
5. **Above-the-fold content** — hero section without animation first
6. **Body content** — remaining page sections
7. **Footer**
8. **Micro-animations** — only after structure is right
9. **Scroll animations** — last, after content is finalized

### During build: activate design enforcement

```bash
# In Claude Code terminal:
/interface-design:status        # verify design system loaded
/baseline-ui src/               # catch baseline violations early
```

### Font selection

Use **FontofWeb** (fontofweb.com) to search for fonts used by specific sites or in specific visual styles. The MCP server connects directly to your agent session for in-context font discovery.

**Current non-default fonts worth knowing (2025):**

*For display/headlines (replace Inter):*
- **Neue Haas Grotesk** — premium, confident, used by serious brands
- **Geist** — clean, technical, Vercel's font, free
- **Cabinet Grotesk** — characterful grotesque, strong for brands
- **Clash Display** — bold, geometric, strong personality
- **Satoshi** — balanced, humanist, versatile

*For body text:*
- **Plus Jakarta Sans** — modern, readable, warm
- **Instrument Sans** — elegant, slightly condensed
- **DM Sans** — clean, functional

*For accent/personality:*
- **Instrument Serif** — pairs well with geometric sans for editorial feel
- **Fraunces** — optical size-aware, great for display at large sizes

*Serif for premium brands:*
- **Playfair Display** — classic editorial
- **Cormorant** — luxury, delicate at small sizes

---

## Phase 4.5: Content Strategy

**Copy slop is as real as design slop.** A professionally designed site with AI-generated filler copy still reads as low-effort. The copy brief goes into `PROJECT.md` before the agent writes a single headline.

### The Copy Brief (add to PROJECT.md)

```markdown
## Voice and Tone
[3 words: "Direct, warm, unfiltered" / "Premium, authoritative, concise"]
[What the brand sounds like: "A knowledgeable friend, not a salesperson"]
[What it does NOT sound like: "Corporate press release / startup hype / motivational poster"]

## Audience's internal monologue
[What they're thinking when they land on this page]
[e.g., "I want to get in shape but gyms feel intimidating and I don't know where to start"]

## The one thing they need to believe to take action
[e.g., "This place is for real people, not Instagram athletes"]

## Copy constraints
- Maximum headline length: [characters or words]
- Reading level target: [conversational / professional / technical]
- First person ("we") or third person ("[Brand] does X")
- UK or US English
```

### The Copy Fingerprint Test

Same logic as design fingerprints — these are the modal outputs of AI writing on marketing copy:

**Words and phrases that signal AI:**
- [ ] "Revolutionize," "transform," "unlock," "unleash"
- [ ] "Seamlessly," "effortlessly," "easily"
- [ ] "Cutting-edge," "state-of-the-art," "next-generation"
- [ ] "Empowering," "leveraging," "synergy"
- [ ] "Journey" used as a verb or pretentious noun
- [ ] "At [Brand], we believe..." as an opening
- [ ] Three-part parallel structure as the default rhythm for everything

**Structural signals of AI copy:**
- [ ] Headline is abstract claim; subhead is also abstract claim (no specificity at any level)
- [ ] Every section ends with a generic CTA ("Learn more," "Get started," "Contact us")
- [ ] Benefits list reads the same regardless of audience (no audience-specific framing)
- [ ] "Our mission is to..." as first sentence anywhere
- [ ] Social proof that's a round number ("Over 1,000 satisfied customers")

### Copy Protocol: How to Brief the Agent

Don't ask the agent to "write marketing copy for a gym." Give it the constraints first:

```
Write the homepage hero headline and subhead for [Project].

Context:
- Audience: [specific description from PROJECT.md]
- What they're thinking: [internal monologue]
- What they need to believe: [one thing]
- Voice: [3 words]
- This is NOT: [anti-goals]
- Reference tone (not reference content): [describe a comparable voice — e.g., "Patagonia, not Nike"]

Constraints:
- Headline: under 8 words, no buzzwords, specific not abstract
- Subhead: one sentence, answers "what exactly do you get"
- No "revolutionize," "transform," "seamlessly," or "unlock"
- Write 3 options, explain the strategic difference between each
```

Asking for 3 options with strategic reasoning forces the agent to explore the decision space rather than defaulting to its first modal output.

### Section-Specific Copy Rules

**Hero headline:** Specific beats clever. "Functional fitness classes for Oakland adults who've never felt at home in a gym" is better than "Redefine Your Limits." Specificity is also what differentiates you from every other gym on the web.

**Social proof:** Avoid round numbers and vague claims. "143 members" is more credible than "100+ members." Named testimonials with specific outcomes beat anonymous quotes. "I lost 22 lbs in 4 months" beats "This gym changed my life."

**CTAs:** Verb + specific outcome. "Book your first class" > "Get started." "See membership options" > "Learn more." "Send us a message" > "Contact us." The button should finish the sentence "I want to ___."

**Error and empty states:** These get written last and skipped most often. Write them intentionally — an error message is a brand moment. "Something went wrong" is a wasted opportunity. "We couldn't save your form — check your connection and try again" is both helpful and human.

---

## Phase 4.6: Image Protocol

Images are the fastest way to make or break a professional site — and the most common gap when working with small businesses and personal brands.

### The Image Situation Decision Tree

```
Does the client have professional photography?
├── Yes → Use it. Optimize for web (see below).
├── No → Do they have decent phone photos?
│         ├── Yes → Upscale with AI (Magnific, Topaz), remove backgrounds where needed
│         └── No → What's the subject matter?
│                   ├── People/places (gym, restaurant, person) → Photo shoot is the right call
│                   │   Photography budget is not optional for conversion-critical sites
│                   └── Abstract/product/concept → Illustration or typographic treatment
│                       Use Midjourney/Flux with specific art direction, not generic prompts
└── Stock photography → Last resort. If you must use stock:
    ├── Getty / Unsplash / Pexels — avoid the "smiling at laptop" category entirely
    ├── Use editorial-style photos, not "concept" photography
    └── Apply grain texture overlay to reduce stock-photo feel
```

### Image Optimization Checklist

- [ ] **Format**: WebP for all photos, AVIF where browser support allows (98%+ by 2025). Never ship JPEG or PNG without converting.
- [ ] **Size**: Hero images max 1920px wide / 300-500KB. Thumbnails under 100KB. Full-page backgrounds: 2500px, compressed aggressively.
- [ ] **Lazy loading**: `loading="lazy"` on all images below the fold. `loading="eager"` + `fetchpriority="high"` on the hero image only.
- [ ] **`srcset`**: Serve different sizes for different viewports. A 1920px image served to mobile is wasted bandwidth.
- [ ] **`alt` text**: Describe what's in the image, not what it represents. "Members training at CrossFit Ironside gym in East Oakland" not "community."
- [ ] **Dimensions declared**: Always set `width` and `height` attributes (even with CSS sizing) to prevent CLS.

### Tools for Image Work

- **Squoosh** (squoosh.app) — free, browser-based, best compression control
- **Sharp** (Node.js) — batch processing in build pipeline
- **Magnific / Topaz Photo AI** — AI upscaling for low-res photos
- **Remove.bg** — background removal for product/person shots
- **Unsplash Source API** — dynamic placeholder images during development

### Art Direction in AI Image Prompts

When generating images with Midjourney, Flux, or similar:

Don't: `"A gym with people working out"`
Do: `"Documentary-style photography, natural light, diverse adults in their 30s-40s doing functional fitness movements, warehouse-style gym, Oakland California, editorial feel, shot on 35mm film, desaturated warm tones, no poses, no smiling at camera —ar 16:9 --style raw"`

The specificity of the prompt is the difference between stock-feel and editorial-feel. Always specify: lighting style, demographic specificity, setting details, photographic style reference, aspect ratio.

---

## Phase 0.5: Agent Setup (CLAUDE.md for Web Projects)

**This file tells Claude Code how to behave on this project specifically.** Drop it in the project root before starting any build work. Without it, the agent makes judgment calls that may be inconsistent with your decisions.

```markdown
# CLAUDE.md

## Project Context
Read PROJECT.md and DESIGN.md before starting any work.
Read .interface-design/system.md if it exists for design decisions already made.

## Stack
- Framework: [Astro / Next.js / etc.]
- Styling: Tailwind CSS
- Animation: [Motion / GSAP]
- Component primitives: [shadcn/ui / Base UI / etc.]

## Code Standards
- TypeScript over JavaScript
- Tailwind classes only — no inline styles unless absolutely necessary
- CSS custom properties for design tokens (match DESIGN.md values exactly)
- No `any` types
- Component files: PascalCase. Utilities: camelCase. Constants: SCREAMING_SNAKE_CASE.

## Design Enforcement
- Never use Inter without explicit instruction
- No nested cards
- No glassmorphism unless explicitly requested
- No purple-to-blue gradients
- Animate only `transform` and `opacity`
- Respect `prefers-reduced-motion` — wrap all animations in the media query

## File Conventions
- Components: src/components/
- Pages: src/pages/ (Astro) or app/ (Next.js)
- Styles: src/styles/
- Assets: src/assets/

## Before Writing Code
1. State what you're building and why
2. If the design isn't in DESIGN.md, ask — don't invent
3. If spacing/sizing isn't on the 4px grid, flag it

## What NOT to Do
- Don't add features or pages not specified
- Don't use lorem ipsum — flag missing content
- Don't pick fonts not in DESIGN.md
- Don't add animations without confirmation
- Don't assume what "looks good" — follow the design system
```

---

## Phase 5: Quality Gates

Run these in sequence before considering a section complete:

### Gate 1: Design contract compliance
```bash
/audit                    # Technical quality: a11y, performance, responsive
/critique                 # UX: hierarchy, clarity, emotional resonance
/normalize                # Align with design system standards
```

### Gate 2: Baseline enforcement
```bash
/baseline-ui src/         # Catches animation violations, typography scale issues,
                          # accessibility failures, layout anti-patterns
```

### Gate 3: Accessibility
```bash
/fixing-accessibility src/   # Keyboard behavior, labels, focus states, semantics
```

### Gate 4: The AI fingerprint test

Manually check against each of these — if you see them, fix them before shipping:

**Typography fingerprints:**
- [ ] Inter, Roboto, Open Sans, Lato, or Montserrat used without a deliberate reason
- [ ] All text the same weight (no weight hierarchy)
- [ ] Body text smaller than 16px
- [ ] Letter-spacing modified on body text (only appropriate for uppercase labels)

**Color fingerprints:**
- [ ] Purple-to-blue gradient anywhere
- [ ] Cyan-on-dark as primary accent
- [ ] Pure black (#000000) for large areas
- [ ] Pure white (#FFFFFF) for backgrounds
- [ ] Gray text on colored backgrounds
- [ ] Glassmorphism (backdrop-blur + transparency as decoration, not function)

**Layout fingerprints:**
- [ ] Cards nested inside cards
- [ ] Everything centered (asymmetry creates visual interest)
- [ ] Identical spacing between all sections
- [ ] 3-column feature grid as default layout
- [ ] Hero metric template (large number + label repeated 3x)

**Motion fingerprints:**
- [ ] Animation on layout properties (width, height, margin, padding)
- [ ] Bounce or elastic easing on UI elements
- [ ] Animations over 500ms for interaction feedback
- [ ] Animation not respecting `prefers-reduced-motion`

**Copy fingerprints:**
- [ ] "Revolutionizing" or "seamlessly" anywhere
- [ ] "Click here" as link text
- [ ] Generic button text ("Submit", "OK", "Learn More")
- [ ] Lorem ipsum in any final deliverable

### Gate 5: Polish pass
```bash
/polish                   # Final review before shipping
```

### Gate 6: Optional depth passes (use selectively)
```bash
/typeset                  # Fix font choices, hierarchy, sizing
/arrange                  # Fix layout, spacing, visual rhythm
/animate                  # Add purposeful motion (only when motion is appropriate)
/colorize                 # Introduce or refine strategic color use
/harden                   # Error handling, i18n, edge cases
```

---

## Phase 6: Metadata and SEO

Don't skip this — it's invisible but affects how the site appears in search and social sharing:

```bash
/fixing-metadata src/     # Correct titles, meta descriptions, OG images, social cards
```

Checklist:
- [ ] Unique `<title>` per page (under 60 chars)
- [ ] Meta description (under 160 chars, includes primary keyword)
- [ ] `og:image` — 1200×630px, branded (not generic)
- [ ] `og:title` and `og:description` distinct from `<title>` and meta description
- [ ] `canonical` URL set
- [ ] Favicon in multiple sizes (16×16, 32×32, 180×180 for Apple touch)
- [ ] `robots.txt` exists
- [ ] `sitemap.xml` if multi-page
- [ ] Page load time under 3 seconds (Core Web Vitals)

---

## Section-Specific Guidance

### Hero Sections (the only section everyone sees)

Reference: supahero.io for 1000+ examples across styles.

The hero has one job: make the right person want to scroll. It should answer "who is this for, what do they get, why now?"

**What strong heroes have in common:**
- **One clear CTA** — not two equal-weight buttons
- **Real photography or distinctive illustration** — no stock imagery of smiling people at laptops
- **Type at scale** — headlines 60-120px+ on desktop; use `clamp()` for fluid scaling
- **Negative space** — content doesn't need to fill the viewport
- **Immediate specificity** — "Functional fitness for working adults in East Oakland" beats "Get Fit Today"

**Hero patterns worth using:**
- Split layout (text left, image right) — timeless, high conversion
- Full-bleed background image with text overlay — works when the image is strong
- Typographic hero — all text, no image; requires distinctive type treatment
- Editorial grid — multiple overlapping elements, borrowed from magazine layout

**Hero patterns that signal AI:**
- Gradient mesh background + floating UI cards
- "Trusted by 1000+ companies" + logo strip in hero
- Three value-prop cards in a row below the fold

### Navigation

Reference: navbar.gallery for inspiration.

**Sticky navs** work for longer pages. **Static navs** work for page-at-a-time sites.

Standard marketing nav: Logo (left) + Links (center or right) + CTA button (right). Mobile: hamburger triggers full-screen or slide-in menu.

**What professional navs do:**
- Clear visual separation from page content (border or subtle background)
- Active state on current page
- CTA button is visually distinct from navigation links (filled vs. text)
- Mobile menu closes on link click
- Announcement bar above nav only for genuinely time-sensitive info

### Footers

Reference: footer.design for inspiration.

The footer is a brand moment, not an afterthought. Strong footers have:
- Consistent with the site's visual system (not a different design language)
- Legal links (Privacy, Terms) clearly present but not dominant
- Social links if the brand has active presence (don't link dead profiles)
- Newsletter signup if there's genuine content to send
- Copyright with current year (auto-update with JS)

Footer don'ts:
- Repeating the full navigation
- Cluttering with every page link
- Mismatched typography or color from the rest of the site

---

## Reference: Current Design Meta (2025)

What professional studios and agencies are actually shipping for marketing sites:

**Visual language:**
- Dark-first designs (not just dark-mode option — designed dark)
- Off-black (#0A0A0A, #0D0D0D) not pure black
- Cream/warm white (#F8F5EE) not pure white for light sites
- Grain texture overlay (subtle CSS noise or SVG) adds depth to flat colors
- Mesh gradients as background texture, not as decoration
- Single strong accent color, used extremely sparingly

**Typography:**
- Oversized display type — 80-140px headlines are normal
- Tight tracking on headlines (-0.03em to -0.05em)
- Mixed weight in same heading (thin + black weight)
- Serif accent for editorial brands
- Variable fonts for weight transitions on hover

**Layout:**
- Intentional asymmetry — grid-breaking for key elements
- Editorial borrowing from print: overlapping text and image, cutout effects
- Scroll-driven reveals (GSAP ScrollTrigger or CSS `animation-timeline`)
- One full-bleed section that breaks the container pattern

**What's moving out:**
- Centered everything
- Glassmorphism (peaked 2022-2023)
- Purple as a default "tech" accent
- Three-card feature grids
- Gradient text (except for specific brand contexts)
- Animated counter numbers (extremely overdone)

---

## Handoff Checklist

Before considering a site "done":

- [ ] DESIGN.md committed to repo
- [ ] All pages pass `/audit` without violations
- [ ] All pages pass `/baseline-ui`
- [ ] Accessibility: keyboard-navigable, focus states visible, contrast passing
- [ ] Metadata complete (title, description, OG image) for all pages
- [ ] Core Web Vitals: LCP < 2.5s, CLS < 0.1, INP < 200ms
- [ ] Tested on mobile (real device, not just DevTools)
- [ ] Tested in Safari (it behaves differently from Chrome)
- [ ] 404 page exists and is branded
- [ ] All forms have validation and success/error states
- [ ] No lorem ipsum, placeholder content, or TODO comments
- [ ] Images have `alt` text
- [ ] Fonts are loaded efficiently (preload, swap, fallback metrics matched)
- [ ] `.interface-design/system.md` committed (preserves design decisions for future sessions)

---

## DESIGN.md Template (Copy-Paste Ready)

```markdown
# Design System: [Project Name]

## Overview
[1-2 sentences: visual personality, aesthetic intent, target feel]

## Colors
- **Background**: [hex] — primary page background
- **Surface**: [hex] — elevated surfaces (cards, panels, navs)
- **Border**: [hex] — dividers, component borders
- **Text primary**: [hex] — headlines and body
- **Text secondary**: [hex] — supporting text, labels, captions
- **Accent**: [hex] — CTAs, highlights, active states (use sparingly)
- **Error**: [hex]

## Typography
- **Display**: [Font], [weight], tracking: [value]
- **Headline**: [Font], [weight], tracking: [value]
- **Body**: [Font], [weight], 16-18px, line-height: 1.6
- **Label**: [Font], [weight], 12-14px, tracking: [value]
- Body measure: max-width: 65ch

## Spacing
- Base: 4px grid
- Section vertical padding: [value desktop] / [value mobile]

## Border Radius
- [e.g., Sharp (0px) / Soft (6-8px) / Rounded (12-16px) / Pill (999px) for buttons]

## Shadows / Depth
- [e.g., No shadows — depth via background color variation]
- [e.g., Subtle: 0 1px 3px rgba(0,0,0,0.12)]

## Motion
- Interaction feedback: 150-200ms, ease-out
- Page transitions: 300-400ms, ease-in-out
- Scroll-triggered reveals: 600ms, ease-out, staggered 80ms between items
- Animate: transform, opacity only

## Components
- **Button (primary)**: [height, padding, radius, background, text color]
- **Button (secondary/ghost)**: [style]
- **Input**: [border, radius, focus state]
- **Card**: [when to use, padding, radius, border vs shadow]
- **Navigation**: [sticky or static, background, separator]

## Do's
- [Specific to this project]

## Don'ts
- [Specific to this project]
- Never use Inter without a deliberate reason
- No nested cards
- No gradient-text
- Accent color max 10% visual weight
```

---

## Performance Budget

Performance is a design decision, not an afterthought. Set targets before building, not after.

### Hard Targets (non-negotiable)

| Metric | Target | What it affects |
|--------|--------|-----------------|
| LCP (Largest Contentful Paint) | < 2.5s | Hero image / headline render time |
| CLS (Cumulative Layout Shift) | < 0.1 | Images without dimensions, late-loading fonts |
| INP (Interaction to Next Paint) | < 200ms | Button clicks, form submissions |
| Page weight (initial load) | < 500KB | JS bundle + CSS + above-fold images |
| Lighthouse score | > 90 | Composite — aim for 95+ on Astro |

### Common causes of performance failures on marketing sites

**JavaScript bloat:**
- Animation libraries loaded when no animation is visible above fold
- Full shadcn/ui bundle imported when only 2 components are used (tree-shake)
- Google Analytics + GTM + HubSpot + Intercom all firing on load — defer everything except analytics

**Image weight:**
- Hero image is a 4MB JPEG (convert to WebP, compress to <300KB)
- LCP image is lazy-loaded (it shouldn't be — use `fetchpriority="high"`)
- No `srcset` — mobile gets the desktop image

**Font loading:**
- Multiple font weights loaded synchronously (only load what you use)
- No `font-display: swap` (causes invisible text during load)
- Fallback font metrics not matched (causes CLS when font swaps in)

### Quick Performance Audit

```bash
# In terminal after build:
npx lighthouse https://localhost:3000 --view

# Specific checks:
npx unlighthouse --site https://your-site.com   # full-site audit
```

---

## Project Kickoff Prompt (Copy-Paste Ready)

Use this as the first message to your agent (Claude Code or Antigravity) at the start of any new project. Fill in the brackets.

```
I'm building a [type of site] for [client/project name].

Before we write any code, read these files in order:
1. PROJECT.md — who this is for and what it needs to accomplish
2. DESIGN.md — the visual system to follow exactly
3. CLAUDE.md — how to work on this project
4. .interface-design/system.md — persistent design decisions (if it exists)

Stack: [Astro / Next.js] + Tailwind CSS + [Motion / GSAP]

First task: confirm you've read all context files, then list:
- The pages we're building
- The components we'll need
- Any questions about the design system or content before starting

Do not start writing code until I confirm the component inventory is right.
```

This front-loads alignment — the most common cause of wasted build time is agents making assumptions about scope, design, or stack that don't match what you actually want.

---

*Cross-references: `skills/skills.md` (how skills work, when to install) · `agentic-engineering/agentic-engineering.md` (agent patterns, CLAUDE.md as context layer) · `specification-clarity/specification-clarity.md` (spec-driven development principles)*
