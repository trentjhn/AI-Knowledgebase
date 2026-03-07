# Level 4 Prompt Engineering — The Professional Brief

## When to Use

When you need **consistent, high-quality outputs** from an LLM and you're willing to invest 5 minutes in structuring the request properly. This is the standard for production work, client deliverables, and any output that goes beyond your personal use.

## Why It Works

Most prompts fail because they skip steps. You ask a question, the model answers, but you didn't tell it to verify its work or check for errors. A **Level 4 prompt** separates instruction from data and forces the model to process your instructions *before* touching your data.

The XML structure (`<instruction>`, `<context>`, `<expected_output_format>`) isn't decoration—it's a forcing function that prevents the most common source of LLM errors: the model skipping to a conclusion before fully understanding the task.

## Architecture

A Level 4 prompt has **five required elements**:

1. **Intent** — What are you asking for? Start with a command verb: Analyse, Extract, Synthesise, Draft, Evaluate.
2. **Persona** — Who should the model be? "Senior business analyst," "experienced software architect," "academic reviewer."
3. **Process** — What steps must happen in order? "First, identify the risks. Then, evaluate mitigation strategies. Only after both, recommend a course of action."
4. **Constraints** — What should it avoid? "Do not exceed 200 words," "Do not use jargon," "Cite sources for every claim."
5. **Format** — What does the output look like? "Markdown table with three columns: Risk | Likelihood | Mitigation." Not "whatever format seems reasonable."

## Trade-Offs

**What it does well:**
- Reduces hallucination by forcing step-by-step reasoning
- Eliminates ambiguity (model knows exactly what you want)
- Consistent outputs across multiple runs (same structure every time)
- Scalable (works with teams using the same brief structure)

**What it sacrifices:**
- Speed — takes longer to write than a one-liner
- Creativity — highly structured outputs are less novel (this is usually what you want)
- Flexibility — if you need the model to decide the format, this won't work

## What to Adjust

**For different scenarios:**

- **High-stakes, low-tolerance-for-error** (legal review, financial analysis): Add explicit quality gates. "If confidence < 80%, state uncertainty instead of guessing."
- **Creative work** (copywriting, design ideation): Loosen the format constraints. "Suggest three conceptually different approaches" vs. "Follow this exact template."
- **Speed-critical** (quick research, brainstorming): Use Level 3 (persona + few examples) instead. Level 4 is overkill for exploratory work.
- **Technical work with domain jargon**: Add an "explain in simple terms" constraint to catch where the model is hand-waving.

## Example Input & Output

### Example: Analyzing a competitive product

**Your Level 4 Prompt:**

```
<instruction>
Act as a senior product strategist.
First, identify the three core value propositions of this product.
Then, evaluate which are defensible vs. easily copied.
Only after both steps, recommend the strategic vulnerabilities Trenton should exploit.
Do not make claims without evidence from the product documentation. If something is unclear, state "Insufficient data to evaluate: [specific claim]."
</instruction>

<context>
Product: Cursor IDE
Value Props from their website:
- "AI that understands your codebase"
- "Code generation that's 10x faster than competitors"
- "Works in VS Code environment"

Trenton's context: Building a competing IDE, shipping Q3 2026.
</context>

<expected_output_format>
Markdown with three sections:
1. Core Value Props (bullet list)
2. Defensibility Analysis (table: Prop | Defensible? | Why)
3. Strategic Vulnerabilities (3-5 bullet points, ranked by exploitability)
</expected_output_format>
```

**Expected Output Structure:**

```
# Cursor IDE — Strategic Analysis

## Core Value Props
- AI understands codebase (via embeddings + fine-tuning on user code)
- Generates code faster than human typing (claimed 10x productivity)
- Integrates with existing VS Code environment (no new tooling)

## Defensibility Analysis
| Prop | Defensible? | Why |
|---|---|---|
| AI understands codebase | Partially | Multiple vendors claim this; defensibility comes from execution quality, not exclusivity |
| 10x faster generation | Difficult | Speed improvements fade quickly; benchmarks don't hold as models improve |
| VS Code integration | Weak | VS Code is open-source; integration is a commodity feature by 2026 |

## Strategic Vulnerabilities
1. **Overreliance on VS Code ecosystem** — If Microsoft ships competitive AI features directly into VS Code, Cursor's distribution moat vanishes
2. **Benchmark volatility** — Speed claims become obsolete as underlying models improve; need defensibility beyond "currently fastest"
3. **Codebase understanding is learned, not built-in** — Requires per-user fine-tuning; high latency for new users or projects
```

Notice: The prompt forced the model to complete the analysis (step 1) *before* making recommendations (step 2). This prevents premature conclusions.

## Related Techniques

- **Chain-of-Thought (CoT)** — Similar forcing of step-by-step reasoning, but less structured. Use when you want reasoning visible but don't care about exact format.
- **Few-Shot Prompting** — Pair with Level 4 prompts to show examples of "good output." Boosts accuracy 10-20%.
- **Persona Priming** — The "Act as X" component. Stronger effect when combined with explicit instructions.
- **Discernment Loop** — Use after getting a Level 4 output to interrogate it (check for hallucinations, missed steps, persona drift).

## Common Mistakes

1. **Mixing instruction and data** — Don't: "Analyze this sales report: [data]". Do: put data in `<context>` block.
2. **Vague constraints** — Don't: "Be concise". Do: "Maximum 150 words, bullet list format."
3. **Forgetting the format** — Don't: assume the model will choose good output format. Do: specify exact structure.
4. **Over-specifying steps for simple tasks** — Level 4 is overkill for "write a poem" or "brainstorm startup ideas." Use Level 2-3 instead.

## Source

Adapted from "AI Fluency Framework" (Anthropic, 2025) and "Prompt Engineering Guide" (Google, 2025). Detailed in `prompt-engineering.md` (KB section 2).

---

## Quick Reference: When to Use Level 4 vs. Other Levels

| Level | Use When | Trade-Off |
|-------|----------|-----------|
| **Level 1** | "Just asking a question" | No consistency, highly variable output |
| **Level 2** | Quick research, brainstorming | Some structure, but still loose |
| **Level 3** | Good output needed, but don't care about format | Solid results, but output varies |
| **Level 4** | Production work, client deliverables, at-scale operations | Best results, but requires 5 min upfront investment |
