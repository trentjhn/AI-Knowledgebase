---
name: cloning-protocol
description: >
  Systematic website cloning and re-branding protocol. Use when the user says
  "clone this site", "re-skin this", "brand swap", "make this website for [X]",
  or asks to customise logo, copy, pricing, reviews, trusted brands, or colour
  scheme on a cloned template. Walks through six phases, collects all assets
  and copy from the user, then implements every change.
---

# Cloning Protocol

> **Purpose:** Take a cloned website template and systematically re-brand it for a new client by swapping six core elements: **Logo · Copy · Trusted Brands · Pricing · Reviews · Colour Scheme**.

---

## When to Use This Skill

- The user says "clone this website for [brand]"
- The user says "re-skin / rebrand / customise this template"
- The user references any of the six changeable elements below
- A repo has just been cloned and the user wants to make it their own

---

## Template Component Map

The cloned template is a **Vite + React + TypeScript** project. Below is a precise map of which files control which brandable element. Always verify paths by running `list_dir` first — the repo structure may have been reorganised.

| # | Element | Primary Files | What to Change |
|---|---------|--------------|----------------|
| 1 | **Logo** | `components/Navbar.tsx`, `components/Footer.tsx`, `index.html` (`<title>`) | Logo icon/image, brand name text (`VOLTFLOW`), favicon, `<title>` tag |
| 2 | **Copy** | `components/Hero.tsx`, `components/Features.tsx`, `components/Footer.tsx`, `components/CardScannerSection.tsx`, `components/AuditTool.tsx`, `index.html` | Headlines (multi-styled with gradients), sub-headlines, body paragraphs, CTA button labels, meta descriptions, badge text, section titles |
| 3 | **Trusted Brands** | `components/SocialProof.tsx` | Brand name strings in the `brands` array — replace with real client logos/names |
| 4 | **Pricing** | `components/Pricing.tsx` | Plan names, prices, feature lists, CTA labels, highlighted plan |
| 5 | **Reviews** | `components/Testimonials.tsx` | Reviewer names, roles, testimonial quotes, avatar images, ratings |
| 6 | **Colour Scheme** | **ALL components** + `components/ui/*` + `index.html` `<style>` block | Primary accent (`#BFF549`), gradient mid-points, background (`#02040a`), muted text (`#99A1AF`), button glows, shadow rgba values, volumetric effects, icon fills, border colors, selection color, scrollbar colors — **requires component-by-component audit** |

**Additional Components to Check:**
- `components/CardScannerSection.tsx` - headline gradients, section copy
- `components/AuditTool.tsx` - comprehensive color usage (backgrounds, buttons, text, badges, circles, icons), headline styling, CTA labels
- `components/StickyCTA.tsx` - floating CTA button colors and text
- `components/ui/gradient-menu.tsx` - any UI component colors
- `components/ui/gradient-menu-inline.tsx` - any UI component colors

---

## Workflow

Run through each phase **in order**. Do NOT skip ahead or begin implementing until all six phases of information gathering are complete.

### Phase 0 — Discovery

- [ ] **Confirm the repo is cloned** and identify the workspace root.
- [ ] **Run the site locally** (`npm install && npm run dev`) so changes can be previewed.
- [ ] Ask the user: *"What is the brand / company name for this new site?"*

### Phase 1 — Logo

Ask the user for the following:

- [ ] **Brand name** 
- [ ] **Logo image file** — request in these dimensions:
  - Navbar icon: **40 × 40 px** (PNG or SVG, transparent background)
  - Footer icon: **32 × 32 px** (PNG or SVG, transparent background)
  - Favicon: **32 × 32 px** (ICO or PNG)
- [ ] If the user does not have a logo image, offer to use a **Lucide icon** from the existing library and ask which icon they prefer.
- [ ] Confirm whether the icon background colour should match the new accent colour.

**Implementation targets:**
```
components/Navbar.tsx  →  logo icon + "VOLTFLOW" text
components/Footer.tsx  →  logo icon + "VOLTFLOW" text
index.html             →  <title> tag + favicon link
```

### Phase 2 — Copy Changes

Ask the user for the following:

**Hero Section (`components/Hero.tsx`):**
- [ ] **Hero headline** - May be multi-line with different styling per line
  - Main text (e.g., "WE BUILD GORGEOUS WEBSITES" or "TYPING IS DEAD")
  - Gradient/styled portions (identify which words get gradient treatment)
  - Accent portions (identify which words get accent color)
- [ ] **Hero sub-headline / tagline** (replaces "Elevating digital presence…")
- [ ] **Hero badge text** (replaces "Performance Optimized" or "TRUSTED BY 200+ BRANDS")
- [ ] **Primary CTA label** (replaces "Start Your Project")
- [ ] **Secondary CTA label** (replaces "View Our Work")

**Navigation (`components/Navbar.tsx`):**
- [ ] **Navbar CTA label** (replaces "Book Strategy")
- [ ] **Navigation link labels** (if customizing menu items)

**Sections with Gradient Headlines:**
- [ ] **CardScannerSection headline** (e.g., "Stop Burning Cash on" + gradient text "Bad Websites")
  - Plain text portion
  - Gradient text portion (note which part gets gradient styling)
- [ ] **AuditTool section headline** (e.g., "FREE AI CONVERSION CRITIQUE")
  - Identify which words get special styling (outline, gradient, accent color)
  - Sub-text below headline

**Other Sections:**
- [ ] **Features section headline** (replaces "SCIENTIFIC PRECISION.")
- [ ] **Features section sub-text**
- [ ] **Features card titles & descriptions** (there are 3 main cards + 3 bottom row items)
- [ ] **Pricing section headline** (replaces "INVEST IN ROI")
- [ ] **Pricing section sub-text** (e.g., "Clear, transparent pricing…")
- [ ] **Testimonials section headline**
- [ ] **Footer tagline** (replaces "We help elite businesses dominate…")
- [ ] **Footer copyright text**
- [ ] **Footer column titles & links** (3 columns: Expertise, Agency, Support)
- [ ] **Page `<title>` and meta description** in `index.html`

**Button Labels Throughout:**
- [ ] Review ALL button labels across components (CTAs, form submits, etc.)
- [ ] Check for: "Analyze Now", "Start Project", "View Work", "Get Started"

If the user provides partial copy, **confirm what should stay as-is** and what they want you to generate.

**IMPORTANT:** When implementing multi-styled headlines:
- Preserve the HTML structure (line breaks, spans)
- Apply gradients via: `className="bg-gradient-to-r from-[...] via-[...] to-[...] bg-clip-text text-transparent"`
- Apply accent colors directly: `className="text-[#7C3AED]"`
- Apply stroke/outline effects: `className="text-transparent [-webkit-text-stroke:1px_white]"`

### Phase 3 — Trusted Brands Logos

Ask the user for the following:

- [ ] **List of brand names** to display in the marquee (replaces TechVibe, NexusLabs, etc.)
- [ ] **Brand logo images** (optional) — request in these dimensions:
  - Marquee logos: **height 48–64 px**, width proportional, **SVG preferred** (PNG with transparent background also acceptable)
- [ ] If the user supplies logo images, the implementation will swap from text-based marquee to `<img>` tags.
- [ ] If the user supplies only names, keep the current text-based animated marquee.
- [ ] Confirm the label above the marquee (currently "Trusted by industry leaders").

**Implementation target:**
```
components/SocialProof.tsx  →  brands array / logo images + label text
```

### Phase 4 — Pricing

Ask the user for the following:

- [ ] **Number of pricing tiers** (currently 3: Starter, Growth, Enterprise)
- [ ] For **each tier**, collect:
  - Plan name
  - Subtitle / tagline
  - Price (with currency symbol)
  - Feature bullet points (list of strings)
  - Whether this tier is the "highlighted / recommended" plan
- [ ] **CTA button label format** (currently "Choose {plan.name}")
- [ ] **Pricing section headline** (if different from copy already provided in Phase 2)
- [ ] **Pricing section sub-text** (currently "Clear, transparent pricing. No hidden fees. Just results.")

**Implementation target:**
```
components/Pricing.tsx  →  pricingPlans array + section heading + CTA labels
```

### Phase 5 — Reviews / Testimonials

Ask the user for the following:

- [ ] **Number of testimonials** (currently 4)
- [ ] For **each testimonial**, collect:
  - Reviewer full name
  - Reviewer role / title & company
  - Testimonial quote text
  - Star rating (1–5)
  - Avatar image — request in these dimensions:
    - **100 × 100 px** (PNG or JPG, square, ideally circular crop)
- [ ] If the user does not have avatar images, offer to keep the randomised placeholder avatars or use `generate_image` to create stylised ones.

**Implementation target:**
```
components/Testimonials.tsx  →  testimonials array
```

### Phase 6 — Colour Scheme

Ask the user for the following:

- [ ] **Primary accent colour** (replaces `#BFF549` — the lime green used for CTAs, highlights, stars, badges)
- [ ] **Background colour** (replaces `#02040a` — the near-black base)
- [ ] **Muted text colour** (replaces `#99A1AF` — used for secondary / descriptive text)
- [ ] **Secondary accent** (optional — replaces the blue/purple accents in Features cards)
- [ ] **Gradient colors** (if using purple: `#7C3AED` base, `#A855F7` mid-point for gradients)
- [ ] **Selection highlight colours** (text selection `::selection`)
- [ ] If the user provides a single brand colour, **derive the full palette automatically**:
  - Primary accent → user colour
  - Mid-tone for gradients → lighten/shift hue 15%
  - Hover states → lighten 10%
  - Glow/blur overlays → same hue at 5–10% opacity
  - Selection → accent bg + black text

**CRITICAL — Color appears in many places beyond simple backgrounds:**
- Button backgrounds AND button glow effects (blur shadows)
- Text colors AND text gradients (`bg-gradient-to-r`, `bg-clip-text`)
- Icon fills, strokes, AND SVG gradient definitions
- Background orbs, glows, and volumetric effects
- Score circles, progress indicators, badges, pills
- Border colors, hover effects, and focus states
- Shadow colors in hover states (`hover:shadow-[0_0_40px_rgba(...)]`)

**Implementation targets (comprehensive find-and-replace):**
```
#BFF549   →  new primary accent     (ALL files - use replace_all: true)
#FACC15   →  new gradient mid       (if present - secondary yellow/gold)
#02040a   →  new background         (ALL files + index.html <style>)
#99A1AF   →  new muted text         (ALL files)
rgba(191,245,73,...)  →  new rgba   (shadow/glow effects)
index.html            →  ::selection, scrollbar, body background
```

---

## Implementation Protocol

Once **all six phases** of information have been collected and confirmed:

### Step 1 — Backup Verification
- [ ] Confirm the repo has git history so changes are recoverable (`git status`).

### Step 2 — Colour Scheme (do this FIRST)
- [ ] **IMPORTANT:** Use `replace_all: true` in Edit tool for efficient color replacement
- [ ] Perform a **global find-and-replace** across all files for each color token:
  - [ ] Replace `#BFF549` (or old primary) → new primary (hex uppercase)
  - [ ] Replace `#FACC15` (if present) → new gradient mid-point
  - [ ] Replace `rgba(191,245,73,X)` → new rgba with same alpha
  - [ ] Replace `#02040a` → new background
  - [ ] Replace `#99A1AF` → new muted text
- [ ] Update `index.html` `<style>` block (body bg, selection, scrollbar).
- [ ] **Audit each component individually** for missed colors:
  - [ ] `components/Hero.tsx` - button gradients, glow effects, orb backgrounds
  - [ ] `components/AuditTool.tsx` - ALL accent colors throughout (volumetric bg, score circles, badges, button, text highlights, icons)
  - [ ] `components/CardScannerSection.tsx` - gradient text in headlines
  - [ ] `components/Pricing.tsx` - highlighted plan accents, badges
  - [ ] `components/Features.tsx` - card accents, icon backgrounds
  - [ ] `components/SocialProof.tsx` - badge colors, accent text
  - [ ] `components/Testimonials.tsx` - star colors, accent elements
  - [ ] `components/Navbar.tsx` - CTA button, active states
  - [ ] `components/Footer.tsx` - link hover states, accent elements
  - [ ] `components/ui/` - check ALL UI component files for color usage
- [ ] Verify no hardcoded color values were missed:
  - [ ] Run `grep_search` for old hex codes (try both cases: `#BFF549` and `#bff549`)
  - [ ] Search for `rgba(191,245,73` or other RGB variants
  - [ ] Check for gradient definitions: `from-[#`, `via-[#`, `to-[#`

### Step 3 — Logo
- [ ] Save any uploaded logo files to `/public/` directory.
- [ ] Update `Navbar.tsx` — swap icon component / add `<img>` tag, update brand name text.
- [ ] Update `Footer.tsx` — same as above.
- [ ] Update `index.html` — `<title>` tag, add `<link rel="icon">` if favicon provided.

### Step 4 — Copy
- [ ] Update `Hero.tsx` — headline, sub-headline, badge, CTAs.
- [ ] Update `Navbar.tsx` — nav links, CTA button label.
- [ ] Update `Features.tsx` — section title, card titles, descriptions.
- [ ] Update `Pricing.tsx` — section headline, sub-text (if different from pricing data).
- [ ] Update `Footer.tsx` — tagline, copyright, column titles/links.
- [ ] Update `index.html` — `<title>`, meta description.

### Step 5 — Trusted Brands
- [ ] Update `SocialProof.tsx` — replace `brands` array with new names or `<img>` logos.
- [ ] If using images, save to `/public/brands/` and reference from component.

### Step 6 — Pricing
- [ ] Update `Pricing.tsx` — replace `pricingPlans` array with new data.

### Step 7 — Reviews
- [ ] Update `Testimonials.tsx` — replace `testimonials` array with new data.
- [ ] If avatar images provided, save to `/public/avatars/` and update `src` paths.

### Step 8 — Final Verification
- [ ] Run `npm run dev` and visually verify in browser.
- [ ] **Comprehensive color audit** using grep:
  - [ ] `grep_search "#BFF549"` (or old primary - try uppercase)
  - [ ] `grep_search "#bff549"` (try lowercase variant)
  - [ ] `grep_search "rgba(191,245,73"` (RGB variants in shadows/glows)
  - [ ] `grep_search "#FACC15"` (any secondary accent colors)
  - [ ] Manually review the output of each search to confirm all matches are intentional
- [ ] Check for any remaining references to old brand name:
  - [ ] `grep_search "VOLTFLOW"` (or old brand name)
  - [ ] `grep_search "voltflow"` (lowercase variant)
- [ ] **Visual verification checklist** in browser:
  - [ ] All gradients render with new colors (hero button, text gradients, badges)
  - [ ] Button hover glows use new color in shadow
  - [ ] Background orbs/volumetric effects show new accent
  - [ ] All icon colors updated (Sparkles, CheckCircle, stars, etc.)
  - [ ] Score circles, progress indicators use new color
  - [ ] Badge backgrounds and borders match new scheme
  - [ ] Text selection highlight uses new color (select text on page to verify)
- [ ] Confirm all links, CTA buttons, and images render correctly.
- [ ] Test responsive design on mobile viewport (some gradient text may need adjustment).
- [ ] If any colors look wrong, use the component-specific audit checklist in Step 2 to find missed instances.

---

## Asset Dimensions Summary

Provide this table to the user when requesting assets:

| Asset | Dimensions | Format | Notes |
|-------|-----------|--------|-------|
| Navbar logo icon | 40 × 40 px | SVG or PNG (transparent) | Square, used in rounded container |
| Footer logo icon | 32 × 32 px | SVG or PNG (transparent) | Matches navbar but smaller |
| Favicon | 32 × 32 px | ICO or PNG | Browser tab icon |
| Trusted brand logos | height 48–64 px | SVG preferred | Used in scrolling marquee |
| Testimonial avatars | 100 × 100 px | PNG or JPG | Square, displayed as circle |

---

## Gradient Handling Guide

Many modern sites use gradients instead of flat colors. Here's how to handle them:

### Types of Gradients You'll Encounter

1. **Button gradients:**
   ```tsx
   bg-gradient-to-r from-[#BFF549] via-[#FACC15] to-[#BFF549]
   ```
   Replace ALL three color values with your new palette.

2. **Text gradients (using bg-clip-text):**
   ```tsx
   className="bg-gradient-to-r from-[#7C3AED] via-[#A855F7] to-[#7C3AED] bg-clip-text text-transparent"
   ```
   Used for gradient headline text - update all hex values.

3. **SVG gradients (for icons):**
   ```tsx
   <svg width="0" height="0">
     <defs>
       <linearGradient id="purple-gradient">
         <stop offset="0%" style={{stopColor: '#7C3AED'}} />
         <stop offset="50%" style={{stopColor: '#A855F7'}} />
         <stop offset="100%" style={{stopColor: '#7C3AED'}} />
       </linearGradient>
     </defs>
   </svg>
   <Sparkles className="fill-[url(#purple-gradient)]" />
   ```
   Update `stopColor` values in the gradient definition.

4. **Shadow gradients (button glows):**
   ```tsx
   shadow-lg hover:shadow-[0_0_40px_rgba(124,58,237,0.5)]
   ```
   Convert your new hex to rgba and update the shadow color.

### Gradient Replacement Strategy

- **For 3-color gradients:** Use `from-[primary] via-[lighter] to-[primary]` for consistent look
- **Deriving the mid-point color:** Lighten primary by 15% or shift hue slightly
- **Common patterns:**
  - Purple gradient: `#7C3AED → #A855F7 → #7C3AED`
  - Blue gradient: `#3B82F6 → #60A5FA → #3B82F6`
  - Green gradient: `#10B981 → #34D399 → #10B981`

---

## Error Handling

- If `npm install` fails → check Node.js version (`node -v`, needs ≥ 18).
- If colors look wrong after replacement:
  - Run `grep_search` for hex codes with mixed case (`#bff549` vs `#BFF549`)
  - Check for rgba variants: `grep_search "rgba(191,245,73"`
  - Manually audit components listed in Step 2 - some components may have many instances
  - Look for gradient definitions: `from-[#old]`, `via-[#old]`, `to-[#old]`
  - Check SVG gradient definitions: `<stop ... stopColor='#old' />`
  - Verify shadow colors in hover states: `hover:shadow-[0_0_40px_rgba(old,0.5)]`
- If gradients don't appear:
  - Ensure ALL color stops in gradient are updated (from, via, to)
  - Check that `bg-clip-text text-transparent` is present for text gradients
  - For SVG gradients, verify the gradient `id` matches the `fill="url(#id)"`
- If logo images don't load → verify paths are relative to `/public/` and referenced from root (`/logo.svg`).
- If some elements still show old colors:
  - Use the component-specific audit checklist in Step 2
  - Components like `AuditTool.tsx` may have 10+ instances of the accent color
  - Check UI components in subdirectories (`components/ui/*`)
- If the user provides only some of the six elements → implement what's provided, leave the rest as template defaults, and note which items still need customization.
- If TypeScript errors appear after changes → these are often just type hint issues and won't prevent the site from running in dev mode. Focus on visual verification in the browser.

---

## Interaction Style

- Be **systematic** — work through phases 1–6 in order.
- Be **specific** — when asking for assets, always state the exact dimensions and preferred format.
- Be **efficient** — ask for all items within a phase in a single message, not one at a time.
- Be **confirmatory** — before implementing, summarise all collected information and get a final "go" from the user.
- **Never assume** — if the user hasn't provided something, ask. Don't invent brand names, pricing, or testimonials.
