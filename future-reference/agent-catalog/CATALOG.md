# Agent Catalog — Flat Index

Read this before selecting a role. You are not assigned a role — you
self-select based on what the task needs and what predecessors have
already produced.

**How to use:** Read the full table. Identify what's missing from
prior outputs. Select the role that fills the most critical gap.

---

## Core — Every Project

| Agent | Self-select when | Produces |
|---|---|---|
| [architect](core/architect.md) | No structure exists; system design decisions needed; scaling or component decisions pending | Architecture doc, component map, ADRs |
| [planner](core/planner.md) | Task needs decomposition before execution; scope is clear but steps are not | Ordered implementation plan with dependencies |
| [code-reviewer](core/code-reviewer.md) | Code exists and needs quality, pattern, and correctness review | Annotated review with specific issues and fixes |
| [doc-updater](core/doc-updater.md) | Implementation changed and documentation is now out of sync | Updated docs matching current implementation |

## Quality — Hardening

| Agent | Self-select when | Produces |
|---|---|---|
| [security-reviewer](quality/security-reviewer.md) | Code handles user input, auth, APIs, payments, or sensitive data | OWASP audit, severity-ranked issues, specific fixes |
| [tdd-guide](quality/tdd-guide.md) | Tests are missing, coverage is low, or TDD discipline is needed | Test suite, coverage report, TDD workflow |
| [performance-optimizer](quality/performance-optimizer.md) | Latency, throughput, or resource usage is a concern | Performance analysis, bottleneck identification, fixes |
| [harness-optimizer](quality/harness-optimizer.md) | AI system accuracy needs improvement; prompt/context patterns need optimization | Optimized harness patterns, accuracy benchmarks |
| [refactor-cleaner](quality/refactor-cleaner.md) | Code is working but messy, duplicated, or violates patterns | Refactored code with same behavior, cleaner structure |
| [build-error-resolver](quality/build-error-resolver.md) | Build is failing and the error needs systematic diagnosis | Root cause analysis, specific fix |
| [go-reviewer](quality/go-reviewer.md) | Go code needs idiomatic review | Go-specific review: error handling, concurrency, patterns |
| [python-reviewer](quality/python-reviewer.md) | Python code needs idiomatic review | Python-specific review: types, patterns, Pythonic style |
| [typescript-reviewer](quality/typescript-reviewer.md) | TypeScript code needs type safety and pattern review | TS-specific review: type correctness, safety, patterns |
| [evaluator](quality/evaluator.md) | Output quality needs structured assessment; evaluator-optimizer loop needed; pass/fail criteria must be enforced | Structured evaluation with PASS/NEEDS_IMPROVEMENT/FAIL signal and specific improvement guidance |

## Design — First-Class (not optional for UI projects)

| Agent | Self-select when | Produces |
|---|---|---|
| [ux-researcher](design/ux-researcher.md) | User needs unclear; journey mapping needed; design decisions require user grounding | User journey map, segment definitions, design requirements |
| [ui-designer](design/ui-designer.md) | Screens or components need visual design; existing UI needs polish | Component specs, screen designs, design decisions |
| [design-system-architect](design/design-system-architect.md) | New project needs visual foundation; token system needs definition | Token system, DESIGN.md, component composition rules |
| [accessibility-reviewer](design/accessibility-reviewer.md) | UI is complete or nearly complete; WCAG compliance needed | WCAG audit, severity-ranked issues, specific fixes |
| [product-designer](design/product-designer.md) | Complex feature needs design thinking from problem to solution | Problem statement, solution exploration, design spec |

## Product — PM Layer

| Agent | Self-select when | Produces |
|---|---|---|
| [product-strategist](product/product-strategist.md) | Project vision or success metrics are unclear; product direction needed | Vision statement, success metrics, user stories, assumption map |
| [spec-writer](product/spec-writer.md) | Requirements exist but are ambiguous; developers need an implementable contract | 7-property spec with BDD acceptance criteria |
| [technical-writer](product/technical-writer.md) | Feature complete; documentation needed; README outdated | Documentation humans actually want to read |

## AI Specialist — AI/Agentic Projects Only

| Agent | Self-select when | Produces |
|---|---|---|
| [context-architect](ai-specialist/context-architect.md) | System prompt or context window design needed; token costs high; memory strategy unclear | Context architecture spec, system prompt, token budget |
| [eval-designer](ai-specialist/eval-designer.md) | AI feature about to be implemented (required pre-condition); quality needs measuring | Eval spec, test set, automated eval harness, baseline |
| [prompt-engineer](ai-specialist/prompt-engineer.md) | System prompt needs construction; outputs inconsistent; technique selection needed | System prompt, few-shot examples, test results |
| [kb-navigator](ai-specialist/kb-navigator.md) | Task requires KB knowledge; pattern recognition fired; best practices needed | Relevant KB sections with synthesis and decision recommendation |
| [data-analyst](ai-specialist/data-analyst.md) | Data analysis needed; code execution + tool use required; structured insights from datasets | Analysis report with findings, visualizations spec, and actionable conclusions |

## Meta — Coordination

| Agent | Self-select when | Produces |
|---|---|---|
| [chief-of-staff](meta/chief-of-staff.md) | Multi-agent coordination is breaking down; task routing needs oversight | Coordination plan, task assignments, escalation handling |
| [loop-operator](meta/loop-operator.md) | Agent is in a loop pattern; loop execution needs monitoring and quality gates | Loop execution with checkpoint validation |
| [scout](meta/scout.md) | Brownfield or unfamiliar codebase needs mapping before builders start; architecture, patterns, and constraints are unknown | Codebase map, architecture assessment, constraint list, pattern inventory — strictly read-only |
| [merger](meta/merger.md) | Parallel agent branches completed on separate worktrees and need reconciliation into a target branch | Clean merge with tiered conflict resolution, test-verified integration, conflict resolution log |
