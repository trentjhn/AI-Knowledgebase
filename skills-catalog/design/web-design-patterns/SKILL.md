---
name: web-design-patterns
description: A set of professional patterns for web design and engineering, covering design system documentation, UI specification, and component architecture. Broadly applicable to any web project.
allowed-tools:
  - "Read"
  - "Write"
  - "view_file"
  - "generate_image"
---

# Web Design & Engineering Patterns

This skill provides a professional workflow for designing and building web interfaces. It synthesizes best practices from top-tier design systems and component libraries to ensure consistency and scalability.

## 1. Design System Documentation (`DESIGN.md`)

Before building, you must define the visual language. This serves as the "source of truth" for both human developers and AI agents.

### When to use
- Starting a new project.
- Auditing an existing project to ensure consistency.
- needing to "reverse engineer" a design from a screenshot or existing site.

### Instructions
1.  Create a file named `DESIGN.md` in the project root.
2.  Use the structure defined in `resources/design-system-template.md`.
3.  **Key Principles**:
    *   **Be Descriptive**: Don't just say "blue". Say "Ocean-deep Cerulean (#0077B6) for primary actions".
    *   **Map Colors to Roles**: Every color must have a purpose (e.g., "Background", "Surface", "Primary Action", "Destructive").
    *   **Describe Geometry**: "Pill-shaped buttons", "Sharp, squared-off cards".
    *   **Define Atmosphere**: "Minimalist and airy", "Dense and information-heavy".

## 2. UI Specification & Prompting

Clear requirements lead to clear code. Use this pattern to refine vague ideas into actionable specifications.

### When to use
- Defining a new feature or page.
- Writing a prompt for an AI coding agent (like Stitch/Gemini).
- Clarifying requirements with a stakeholder.

### Instructions
1.  Assess the initial request. Does it lack **Platform**, **Visual Style**, **Structure**, or **Component details**?
2.  Draft a specification using `resources/ui-spec-template.md`.
3.  **Enhancement Checklist**:
    *   **Keywords**: Replace "menu" with "Navigation Bar", "box" with "Card/Container".
    *   **Vibe**: Add adjectives (e.g., "clean", "vibrant", "trustworthy").
    *   **Structure**: Delineate sections (Header, Hero, Content, Footer).

## 3. Modern Component Architecture

Build components that are modular, type-safe, and scalable.

### When to use
- Writing React/Vue/Web Components.
- Refactoring existing code.

### Instructions
1.  **Composition over Inheritance**: Use smaller, composed components rather than massive "God components" with 50 props.
2.  **Headless UI**: Where possible, separate logic (state/behavior) from styling. Use libraries like Radix UI or React Aria for accessibility primitives.
3.  **Data Decoupling**: Move static text, navigation links, and image URLs to separate data files or constants (`src/data/`).
4.  **Type Safety**: Define `Readonly` interfaces for Props.
5.  **Quality Gate**: Before finalizing a component, run through the `resources/component-checklist.md`.

## 4. Stylings & Shadcn UI Integration

This skill recommends the **shadcn/ui** pattern: copy-pasteable, ownable components rather than a black-box library.

### Core Principles
- **Ownership**: Components live in your codebase (`components/ui`). You own the code.
- **Tailwind CSS**: Use utility classes for styling.
- **Variables**: Use CSS variables for theming (allows explicit dark mode support).

### Workflow
1.  Install components individually (e.g., `npx shadcn@latest add button`).
2.  Customize the code directly in `components/ui/button.tsx` if needed.
3.  Compose these primitives into larger blocks.

## Resources
- **Design System Template**: `resources/design-system-template.md`
- **UI Spec Template**: `resources/ui-spec-template.md`
- **Component Checklist**: `resources/component-checklist.md`
- **Component Starter**: `resources/component-template.tsx`
