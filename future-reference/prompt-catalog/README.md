# Prompt Catalog

A structured collection of production-grade prompts organized by use case. Each prompt includes the raw template, context on when/why to use it, trade-offs, examples, and related techniques.

## Structure

```
prompt-catalog/
├── README.md (this file)
├── use-case-1/
│   ├── prompt-name-1/
│   │   ├── prompt.md          # Raw prompt template (copy-paste ready)
│   │   └── README.md          # Context, trade-offs, examples, related techniques
│   └── prompt-name-2/
│       ├── prompt.md
│       └── README.md
└── use-case-2/
    └── prompt-name-3/
        ├── prompt.md
        └── README.md
```

## Use Cases

Use cases are organized by **operational context**, not by technique:

- **Analysis & Research** — prompts for understanding problems, analyzing data, literature reviews
- **Code & Technical** — code generation, review, debugging, architecture
- **Writing & Content** — blogs, documentation, emails, specifications
- **Design & Product** — PRDs, specs, UX research, decision frameworks
- **Strategy & Planning** — roadmaps, OKRs, competitive analysis, scenarios
- **Learning & Teaching** — explanations, tutorials, self-testing
- **Brainstorming & Ideation** — exploration, divergent thinking, problem-solving

## Adding New Prompts

When you send me a new prompt to catalog, I'll:
1. Determine the best-fit use case (or create a new one if needed)
2. Create `use-case/prompt-name/` folder
3. Save the raw prompt to `prompt.md`
4. Write `README.md` with context, trade-offs, examples, related techniques
5. Link related prompts bidirectionally

## Metadata (in each README)

Each prompt's README includes:

```
# [Prompt Name]

## When to Use
[Context: what problem does this solve?]

## Why It Works
[The mechanism: why is this approach effective?]

## Trade-Offs
[What does this do well? What does it sacrifice?]

## What to Adjust
[Customization guidance for different scenarios]

## Example Input & Output
[Concrete example showing the prompt in action]

## Related Techniques
[Links to other prompts that pair well with this one]

## Source
[Where this came from: KB section, external source, etc.]
```

## Quick Links

- **Most Versatile**: [coming soon]
- **Best for Brainstorming**: [coming soon]
- **Best for Code**: [coming soon]
- **Best for Analysis**: [coming soon]

---

Last updated: March 2026
