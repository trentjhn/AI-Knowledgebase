# PromptArena — Design System & Aesthetic Guide

**Aesthetic Direction:** Educational brutalism — rigorous, honest, no decoration without purpose. Raw feedback loops. Function visible.

---

## Color Palette

**Primary:**
- Black: `#000000`
- White: `#FFFFFF`
- Accent Blue: `#2563EB` (electric, not soft)

**Semantic:**
- Success: `#16A34A` (dark green, minimal use)
- Error: `#DC2626` (dark red, minimal use)
- Neutral: `#6B7280` (for secondary text only)

**Why:** High contrast, brutalist simplicity. Single accent color (blue) for all interactive states. No gradient pastels, no "friendly" colors.

---

## Typography

**Display Font (Headings):** Playfair Display, serif, 700 weight
- H1: 48px, line-height 1.1, letter-spacing -1px
- H2: 32px, line-height 1.2, letter-spacing -0.5px
- H3: 24px, line-height 1.3

**Body Font (UI, scenario text):** IBM Plex Mono, monospace, 400 weight
- Body: 14px, line-height 1.6
- Labels: 12px, uppercase, letter-spacing 0.5px
- Code blocks: 12px, line-height 1.8

**Why:** Monospace = "code-forward aesthetic." Playfair = editorial elegance for contrast. Brutalism respects hierarchy through size and weight, not sweetness.

---

## Spacing System

```
Base unit: 4px (multiples of 4)

Token scale:
2 (8px), 3 (12px), 4 (16px), 6 (24px), 8 (32px), 12 (48px), 16 (64px)

Applied:
- Card padding: 24px
- Between sections: 32px
- Form input padding: 12px (top/bottom) 16px (left/right)
- Button padding: 12px 16px
```

---

## Component Aesthetics

### Buttons

**Primary (Submit, Action):**
```css
background: #2563EB;
color: white;
padding: 12px 16px;
border: none;
font-family: IBM Plex Mono;
font-size: 14px;
font-weight: 600;
cursor: pointer;
text-transform: uppercase;
letter-spacing: 0.5px;
transition: all 0.2s;
```

On hover: `background: #1D4ED8` (10% darker)
On disabled: `background: #D1D5DB; cursor: not-allowed; opacity: 0.6`

Why: Monospace buttons feel technical. Uppercase feels authoritative. No rounded corners = brutalism.

### Text Inputs & Textarea

```css
background: white;
border: 2px solid #000;
padding: 12px 16px;
font-family: IBM Plex Mono;
font-size: 14px;
color: #000;
resize: vertical;
```

On focus: `border: 2px solid #2563EB; outline: none;`

Why: Stark black border, no shadow. Monospace inside and out = consistency.

### Cards

```css
background: white;
border: 1px solid #000;
padding: 24px;
margin-bottom: 32px;
```

Why: Minimal border. No shadow = flat, honest. Generous padding = breathing room.

### Rubric Items

```css
border-left: 4px solid #2563EB;
padding-left: 16px;
margin-bottom: 16px;
```

Buttons inside rubric:
- Pass button: `background: white; border: 2px solid #16A34A; color: #16A34A;`
- Fail button: `background: white; border: 2px solid #DC2626; color: #DC2626;`

Why: Left border accent (not full box) = minimal. Outline buttons for non-primary actions.

### Solution Modal

```css
position: fixed;
inset: 0;
background: rgba(0, 0, 0, 0.8);
display: flex;
align-items: center;
justify-content: center;
```

Modal content:
```css
background: white;
max-width: 800px;
width: 90%;
max-height: 80vh;
overflow-y: auto;
padding: 32px;
border: 2px solid #000;
animation: slideUp 0.3s ease-out;
```

```css
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(32px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Why: Stark black overlay. Modal enters from bottom with fade. Purposeful animation, not decorative.

---

## Layout

### Main Arena Layout

```
[Left Sidebar 25%] | [Right Content Area 75%]
```

**Left sidebar:**
- Fixed height, scrollable
- Scenario cards stack vertically
- Selected scenario has blue left border

**Right content area:**
- Scenario description (top, 120px)
- Prompt editor (scrollable textarea, flex-grow)
- Response display (if submitted)
- Rubric (if submitted)

Why: Asymmetric layout. Unequal columns = intentional visual hierarchy.

### Responsive (Mobile)

At breakpoint 768px:
- Switch to single column
- Sidebar becomes horizontal tabs
- Full-width editor

---

## Motion & Micro-interactions

### Page Load (Scenario Details)

```css
/* Staggered entrance */
.scenario-title { animation: fadeInDown 0.4s ease-out; }
.scenario-description { animation: fadeInDown 0.5s ease-out; animation-delay: 0.1s; }
.task-block { animation: fadeInDown 0.6s ease-out; animation-delay: 0.2s; }

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Button Hover

```css
button:hover {
  background-color: #1D4ED8;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}

button:active {
  transform: translateY(0);
  box-shadow: none;
}
```

Why: Button rises on hover, presses on click = tactile feedback.

### Token Counter

```css
.token-count {
  animation: countUp 0.6s ease-out;
  font-weight: 700;
  color: #2563EB;
}

@keyframes countUp {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

Why: Tokens are a core feedback signal — animate them to draw attention.

---

## Visual Details

### Background

- Default: Pure white (`#FFFFFF`)
- Sidebar: Off-white (`#F9FAFB`)
- Code/Pre blocks: `#F3F4F6` with monospace font

### Borders & Dividers

- All borders: 1-2px solid black (no gray, no softness)
- No box shadows (except on hover for depth)
- No rounded corners (exception: modal has 4px if necessary for focus visibility)

### Code Block Styling

```css
pre, code {
  font-family: IBM Plex Mono;
  font-size: 12px;
  background: #F3F4F6;
  border: 1px solid #D1D5DB;
  padding: 12px;
  overflow-x: auto;
}
```

Why: Monospace rendering for clarity. Minimal background contrast (not white, but very light).

### Hover States

- Interactive elements: 2px color change (usually to blue) + 2px vertical shift (up)
- Text links (if any): underline appears on hover (no color change)
- Cards: border color shifts to blue on hover

Why: Consistent, minimal feedback. No complexity.

---

## Accessibility

- All text has minimum 4.5:1 contrast ratio (black on white = passes)
- Focus states visible (blue border on inputs)
- All buttons have text labels (not icons alone)
- Semantic HTML: `<button>` for buttons, `<label>` for form inputs
- Font size never below 12px (readability)

---

## Example Component: PromptEditor

```jsx
export function PromptEditor({ value, onChange, onSubmit, isLoading }) {
  return (
    <div className="prompt-editor-container">
      <label className="editor-label">Your Prompt</label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Write your prompt here. Use Level 4 structure if possible..."
        className="prompt-textarea"
      />
      <button
        onClick={onSubmit}
        disabled={isLoading || !value.trim()}
        className="btn-primary btn-submit"
      >
        {isLoading ? "Submitting..." : "Submit Prompt to Claude"}
      </button>
    </div>
  );
}
```

```css
.prompt-editor-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
  border: 1px solid #000;
  background: white;
  margin-bottom: 32px;
}

.editor-label {
  font-family: IBM Plex Mono;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #000;
}

.prompt-textarea {
  font-family: IBM Plex Mono;
  font-size: 14px;
  line-height: 1.6;
  padding: 12px 16px;
  border: 2px solid #000;
  min-height: 200px;
  resize: vertical;
  background: white;
  color: #000;
}

.prompt-textarea:focus {
  outline: none;
  border-color: #2563EB;
  box-shadow: inset 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.btn-primary {
  background: #2563EB;
  color: white;
  padding: 12px 16px;
  border: none;
  font-family: IBM Plex Mono;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  background: #1D4ED8;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: none;
}

.btn-primary:disabled {
  background: #D1D5DB;
  cursor: not-allowed;
  opacity: 0.6;
}
```

---

## Implementation Notes for Developer

1. **Font Loading:** Import Playfair Display and IBM Plex Mono from Google Fonts in `globals.css`
2. **CSS Variables:** Define color and spacing tokens in `:root` for consistency
3. **No UI Library:** Build components from scratch with plain CSS (no shadcn/ui or tailwind utilities). This ensures aesthetic control.
4. **Motion:** Use CSS animations + `animation-delay` for staggered reveals. No JavaScript animation libraries.
5. **Responsive:** Mobile breakpoint at 768px. Test on phone.
6. **Dark Mode:** Not required for MVP. If added later, invert colors (white text on black background, same brutalist aesthetic).

---

## Design Rationale

**Why Brutalism?**
- Prompt engineering is technical work. The interface should feel technical, not cozy.
- Monospace everywhere signals "code-forward."
- High contrast = no ambiguity about what's interactive.
- No decoration = all visual attention goes to content (the prompts and responses).

**Why No Rounded Corners?**
- Brutalism is geometric. Right angles feel honest.

**Why Stark Colors?**
- Black/white/blue only. No pastels, no gradients, no "friendly" colors.
- Reduces cognitive load. You focus on your prompt and Claude's response, not the interface.

**Why This Motion Strategy?**
- Staggered entry on page load creates a sense of "emergence" — information revealing itself.
- Button hover feedback (shift + shadow) is tactile without being distracting.
- Token counter animates because it's a live feedback signal — worth highlighting.
- Modal slides up from bottom (not fade-in) because it's a significant context shift.

---

## What This Design Prevents

- Generic "AI UI" aesthetics (no purple gradients, no Inter font, no 8-color pastel palette)
- Cute, handholding tone (this is rigorous learning, not a game)
- Visual noise (every element has a job; nothing decorative)
- Unclear affordances (interactive elements are obvious)
- Slow feedback (animations are quick; responses appear immediately)

---

## Files to Reference During Implementation

When the coding assistant builds PromptArena, they should:

1. Reference this design system for all styling decisions
2. Build components from scratch (no shadcn/ui or pre-built component libraries)
3. Use CSS custom properties for colors/spacing (consistency)
4. Test responsive behavior at 768px breakpoint
5. Verify all motion is CSS-only (no JavaScript animation)
6. Ensure accessibility (contrast, focus states, semantic HTML)

This design system is **non-negotiable**. The aesthetic direction is intentional and should be preserved in implementation.
