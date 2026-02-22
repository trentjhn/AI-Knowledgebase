# Playbook: Writing Production Prompts

> **Use this when:** You're writing prompts that will run in a real application — not experimenting in a playground, but prompts that real users will interact with, that will run thousands of times, and that need to be reliable, maintainable, and debuggable.

---

## What Makes a Prompt "Production-Ready"

There's a big difference between a prompt that works in a demo and one that holds up in production. In a demo, you see the happy path. In production, you get:

- Users who phrase things in ways you never anticipated
- Edge cases that trigger unexpected model behavior
- Model updates that silently break previously working prompts
- Scale that makes per-response debugging impractical
- The need to iterate on the prompt without breaking what's already working

A production prompt is one that you've designed, tested, and documented with all of these in mind. The techniques below turn a prompt from something you wrote once into something you can maintain, improve, and trust.

---

## Core Technique Stack

### 1. Start with Zero-Shot, Then Add

A common mistake is reaching for complexity before you've established a baseline. Before adding examples, instructions, chain-of-thought, personas, or any other technique, write the simplest possible zero-shot prompt and test it.

Why? If the model already does what you need with minimal instruction, every layer you add is overhead — more tokens, more complexity, more surface area for things to go wrong. Zero-shot results also show you exactly what the model's defaults are, which tells you precisely what you need to change.

**The escalation path:**
1. Zero-shot first — does the model get the general idea?
2. Add a few-shot example if format or style is off
3. Add a system prompt if scope or persona needs defining
4. Add chain-of-thought if accuracy on reasoning tasks is insufficient
5. Add APE or OPRO if you need to find the optimal instruction automatically

See `prompt-engineering/prompt-engineering.md` for each of these techniques in detail.

### 2. Write Instructions, Not Constraints

This distinction matters more than it might seem. A constraint tells the model what *not* to do — "don't be too long," "don't use jargon," "don't mention competitors." An instruction tells the model what *to* do — "write in 2 sentences," "use plain language a high schooler would understand," "focus only on our product's features."

Constraints are vague — the model has to guess what's still allowed. Instructions are specific — the model knows exactly what to produce. In production, where you can't review every output, specificity is everything.

**Rewrite every constraint in your prompt as a positive instruction before shipping.**

### 3. Lock Down Output Format

If your application parses the model's output programmatically, the format must be consistent across every call. Even small variations — an extra sentence here, a slightly different JSON key there — break downstream code.

**Techniques for format enforcement:**
- **Specify format in the system prompt and provide an example.** "Return your answer as a JSON object with the following schema: `{result: string, confidence: "high"|"medium"|"low", sources: string[]}`"
- **Use the Template pattern.** Provide an explicit output template with named placeholders rather than describing the format in prose. The model fills in the blanks, and the structure is guaranteed.
- **Validate output programmatically.** Parse and validate every response in your application layer. Don't trust that the model will always comply — catch format violations and either retry or flag for review.
- **Use `json-repair` for JSON outputs.** If the model's response is truncated by a token limit mid-JSON, the `json-repair` library can automatically fix common malformation issues.

See `prompt-engineering/prompt-patterns.md` for the Template pattern.

### 4. Temperature for the Task Type

Production prompts that aren't matched to the right temperature setting are unreliable in predictable ways. This is one of the easiest fixes and one of the most commonly overlooked.

| Task type | Recommended temperature |
|---|---|
| Classification, extraction, parsing | 0 – 0.2 |
| Factual Q&A, summarization | 0.1 – 0.3 |
| Chain-of-thought reasoning | 0 |
| Balanced helpful responses | 0.2 – 0.5 |
| Creative writing, brainstorming | 0.7 – 1.0 |
| Self-consistency sampling | 0.7 – 0.9 |

If your task falls on the factual/structural side and you're using a high temperature, you will see inconsistent formatting, hallucinated details, and variable accuracy. Match the setting to the task.

### 5. Use Variables, Not Hardcoded Values

If your prompt will run on different inputs — different users, different documents, different contexts — never hardcode those values into the prompt text. Use placeholders.

```
You are a support assistant for {company_name}.
The user's current plan is: {user_plan}.
Their account was created on: {account_creation_date}.
Their question: {user_message}
```

This makes the prompt:
- **Maintainable** — update the template once, it applies everywhere
- **Testable** — you can run the same template against a matrix of input values
- **Debuggable** — when something goes wrong, you can see exactly what values were injected

### 6. APE for High-Value Prompts

For prompts that will run at high volume or that are critical to your product's quality, use Automatic Prompt Engineering rather than relying on your own first draft.

The process: give the model a handful of input-output examples of what you want, ask it to generate 5–10 candidate prompt instructions, evaluate each on a validation set, and take the best-performing one. This often surfaces phrasing that a human wouldn't write but that performs measurably better.

See `prompt-engineering/prompt-engineering.md` — APE section — for the full workflow.

### 7. Document Every Prompt Iteration

Every time you change a prompt, record what changed, why, what the before and after looked like, and what metric improved. This isn't optional record-keeping — it's the only way to:
- Understand why a previously working prompt broke after a model update
- Avoid re-trying approaches that already failed
- Safely roll back to a previous version when something goes wrong
- Share prompt context with teammates or future you

Use the tracking template in `prompt-engineering/prompt-engineering.md` (Section 7: Documentation).

---

## Recommended Workflow

**Phase 1: Define success before writing anything**
Write down: what does a correct output look like? What does an incorrect output look like? Collect 5–10 examples of each. These become your test cases. If you can't define correct and incorrect, your prompt will be impossible to evaluate.

**Phase 2: Write the minimal prompt**
Zero-shot first. Run it on all your test cases. Categorize failures: is the format wrong? Is the tone wrong? Is it answering the wrong question? Is it hallucinating? Each failure type points to a specific fix.

**Phase 3: Fix failures systematically**
Address one failure category at a time. If format is wrong, add a format specification. If tone is wrong, add examples that demonstrate the right tone. If it's answering the wrong question, clarify the task in the system prompt. Test after each change.

**Phase 4: Harden for edge cases**
Once happy-path cases work, run adversarial tests: strange inputs, empty inputs, very long inputs, inputs in different languages, inputs that try to change the prompt's behavior. Fix each failure.

**Phase 5: Optimize with APE (optional, high-value prompts)**
For prompts that justify the investment, run APE to find better instructions. Evaluate the APE-generated candidates against your test set. Use the winner.

**Phase 6: Set up regression testing**
Before deploying, save your test cases and their expected outputs. Add them to an automated test suite that re-runs whenever the prompt or the model changes. This catches regressions silently introduced by model updates.

**Phase 7: Monitor in production**
Log a sample of real inputs and outputs. Review them periodically. Real user inputs will surface failure modes that your test set didn't anticipate. Use these to update your test cases and refine the prompt.

---

## Common Pitfalls

**Shipping the first draft.** The first prompt is the starting point, not the final one. Always iterate on at least your known failure cases before deploying.

**Testing only happy-path cases.** Everything works on the clean examples. It breaks on the weird ones. Test with strange, malformed, adversarial, and edge-case inputs explicitly.

**Changing multiple things at once.** If you change the system prompt, the few-shot examples, and the temperature simultaneously and quality improves, you don't know what actually helped. Change one thing at a time, test, then change the next.

**Not accounting for model updates.** Your hosting provider updates models periodically. A prompt optimized for one version of a model may behave differently on a newer version. Run your test suite after any model change.

**Putting everything in one giant prompt.** Long prompts are harder to debug, slower, and more expensive. If a prompt is doing more than one conceptually distinct thing, consider splitting it into two sequential calls. Each call is simpler, faster, and easier to test independently.

**Not separating prompts from code.** Prompts stored as strings inside application code are harder to version, edit, and test. Store them in separate files with their own versioning. They change on a different cadence than business logic.

**Using the same temperature for everything.** Different tasks need different temperatures. This is a one-minute fix with a meaningful quality impact.

---

## Scaling Up

**Automated evaluation pipelines.** As your prompt library grows, manual testing becomes impractical. Build evaluation pipelines that score prompt performance on test cases automatically. Track metrics over time and get alerts when they degrade.

**Prompt registries.** Store all production prompts in a central registry with versioning, metadata, and performance history. This prevents prompt sprawl (the same prompt being maintained in three different places) and enables systematic improvement.

**A/B testing.** Run two versions of a prompt simultaneously in production, split across a portion of real traffic. Measure quality differences on real user interactions. This produces more reliable improvement data than offline test sets alone.

**Cost tracking per prompt.** Each prompt has a cost per call. As volume scales, prompt efficiency — measured in quality per token — becomes economically meaningful. Track token usage per prompt and optimize high-volume ones.

**Self-consistency for critical outputs.** For high-stakes outputs where a single wrong answer has significant consequences, run the prompt multiple times and take the majority vote. This is expensive but significantly more reliable. See `prompt-engineering/prompt-engineering.md` for the self-consistency technique.

---

*Draw from: `prompt-engineering/prompt-engineering.md` (all techniques, documentation template) · `prompt-engineering/prompt-patterns.md` (Template, Output Automater, Alternative Approaches)*
