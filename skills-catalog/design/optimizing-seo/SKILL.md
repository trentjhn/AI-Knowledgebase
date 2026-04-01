---
name: optimizing-seo
description: >
  Systematic protocol for implementing modern SEO best practices (2025 standards).
  Use when the user mentions "SEO", "ranking", "Google search", "meta tags",
  "OpenGraph", "sitemap", or "robots.txt". Covers technical SEO, metadata,
  structured data (JSON-LD), and social sharing optimization.
---

# SEO Optimization Protocol (2025 Standards)

> **Purpose:** Systematically optimize a web application for search engines and social media sharing using modern 2025 standards (Core Web Vitals, JSON-LD, OpenGraph).

---

## When to Use This Skill

- The user asks to "make this site rank" or "improve SEO".
- The user mentions adding "meta tags", "social preview images", or "sitemaps".
- A new website is being prepared for launch (pre-flight check).
- The user is asking about "Next.js SEO" or "React Helmet".

---

## Workflow

Follow this 4-phase optimization checklist.

### Phase 1: Technical Foundation (The "Must-Haves")
- [ ] **Viewport & Charset**: Ensure `<meta name="viewport" content="width=device-width, initial-scale=1" />` and `<meta charset="utf-8" />` exist.
- [ ] **Canonical URL**: Every page must have a `rel="canonical"` link to prevent duplicate content issues.
- [ ] **Robots.txt**: Create a `public/robots.txt` allowing bots (unless sensitive).
- [ ] **Sitemap.xml**: Generate a dynamic or static `sitemap.xml`.
- [ ] **HTTPS**: Verify all assets are served via HTTPS.

### Phase 2: Metadata & Content (The "Click-Getters")
- [ ] **Title Tags**: Unique per page, 50-60 chars. Format: `[Page Title] | [Brand Name]`.
- [ ] **Meta Descriptions**: Unique per page, 150-160 chars. Action-oriented summary.
- [ ] **Heading Hierarchy**: One `<h1>` per page. Logical `<h2>` -> `<h3>` flow.
- [ ] **Alt Text**: All `<img>` tags must have descriptive `alt` attributes.

### Phase 3: Social & Rich Media (The "Share-Winners")
- [ ] **OpenGraph (OG)**: `og:title`, `og:description`, `og:image`, `og:url`, `og:type`, `og:site_name`.
- [ ] **Twitter Cards**: `twitter:card` (summary_large_image), `twitter:title`, `twitter:description`, `twitter:image`.
- [ ] **OG Image Spec**: 1200x630px, png/jpg, < 5MB. Centralized branding.
- [ ] **Favicons**: standard `.ico`, `.svg` (modern), and `apple-touch-icon`.

### Phase 4: Structured Data (The "AI-Preppers")
- [ ] **JSON-LD**: Implement `application/ld+json` script tags.
- [ ] **Organization Schema**: Logo, social profiles, contact info.
- [ ] **WebSite Schema**: Search box integration.
- [ ] **Page-Specific Schema**: `Article`, `Product`, `FAQPage`, `BreadcrumbList`.

---

## Implementation Guide

### 1. Next.js App Router (`layout.tsx` / `page.tsx`)

Use the built-in Metadata API.

```tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  metadataBase: new URL('https://www.example.com'),
  title: {
    default: 'Acme Corp | Building the Future',
    template: '%s | Acme Corp', // dynamic titles: "About | Acme Corp"
  },
  description: 'Acme Corp builds the future with AI-driven widgets. Start for free today.',
  keywords: ['AI', 'widgets', 'future', 'SaaS'],
  openGraph: {
    title: 'Acme Corp | Building the Future',
    description: 'Acme Corp builds the future with AI-driven widgets.',
    url: 'https://www.example.com',
    siteName: 'Acme Corp',
    images: [
      {
        url: 'https://www.example.com/og-image.jpg', // Must be absolute URL
        width: 1200,
        height: 630,
        alt: 'Acme Corp Dashboard Preview',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Acme Corp | Building the Future',
    description: 'Acme Corp builds the future with AI-driven widgets.',
    images: ['https://www.example.com/twitter-image.jpg'], // Must be absolute URL
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  alternates: {
    canonical: 'https://www.example.com',
  },
}
```

### 2. Standard HTML (`index.html`)

For Vanilla JS or Static Sites.

```html
<!-- Essentials -->
<title>Page Title | Brand Name</title>
<meta name="description" content="Detailed description of the page content, 150-160 chars.">
<link rel="canonical" href="https://www.example.com/current-page">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.example.com/current-page">
<meta property="og:title" content="Page Title | Brand Name">
<meta property="og:description" content="Detailed description of the page content.">
<meta property="og:image" content="https://www.example.com/images/og-image.jpg">
<meta property="og:site_name" content="Brand Name">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:url" content="https://www.example.com/current-page">
<meta name="twitter:title" content="Page Title | Brand Name">
<meta name="twitter:description" content="Detailed description.">
<meta name="twitter:image" content="https://www.example.com/images/twitter-image.jpg">
```

### 3. JSON-LD (Structured Data)

Place inside `<head>` or body. Use standard schemas.

**Organization (Global):**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Acme Corp",
  "url": "https://www.example.com",
  "logo": "https://www.example.com/logo.png",
  "sameAs": [
    "https://facebook.com/acmecorp",
    "https://twitter.com/acmecorp",
    "https://linkedin.com/company/acmecorp"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "Customer Service"
  }
}
</script>
```

**Article (Blog Post):**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Headline",
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg",
    "https://example.com/photos/16x9/photo.jpg"
   ],
  "datePublished": "2025-01-05T08:00:00+08:00",
  "dateModified": "2025-02-05T09:20:00+08:00",
  "author": [{
      "@type": "Person",
      "name": "Jane Doe",
      "url": "https://example.com/profile/janedoe123"
    }]
}
</script>
```

---

## 2025 Verification Tools

Before finishing, instructions MUST specify validation using these tools:

1.  **Headless UI / Meta Checking**:
    -   Inspect Element `<head>` to verify tags are present.
    -   Use **React DevTools** to check if meta tags are being hydrated correctly.

2.  **Public Validators**:
    -   **Rich Results Test (Google)**: `search.google.com/test/rich-results` (Validates JSON-LD).
    -   **Schema Validator**: `validator.schema.org`.
    -   **OpenGraph.xyz**: Previews how the link looks on Socials (Discord, Twitter, LinkedIn).
    -   **PageSpeed Insights**: Checks Core Web Vitals (LCP, CLS, INP).

---

## Common Pitfalls

-   **Missing Absolute URLs**: OG images and Canonical links MUST be absolute (`https://...`), not relative (`/img.jpg`).
-   **Blocked Robots**: Ensure `robots.txt` does not block `_next/static` or plain CSS/JS files.
-   **Duplicate H1s**: Never use more than one `<h1>` per page.
-   **Thin Content**: Pages with <300 words often get marked as "soft 404s" or "crawled - currently not indexed".
-   **Hydration Errors**: In React/Next.js, ensure `<title>` and `<meta>` tags are not causing server/client mismatch errors.
