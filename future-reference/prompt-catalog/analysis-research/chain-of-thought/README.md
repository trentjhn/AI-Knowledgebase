# Chain-of-Thought (CoT) — Visible Reasoning

## When to Use

When you need the model to **show its work** — especially for complex reasoning, multi-step problems, or situations where you need to verify the logic before trusting the answer. CoT works best when the final answer matters less than understanding *how* you got there.

## Why It Works

Without CoT, LLMs often skip intermediate reasoning and jump to conclusions. Chain-of-Thought forces the model to narrate each step, which:
1. **Improves accuracy** — The model is less likely to contradict itself if it has to show its reasoning
2. **Makes errors visible** — You can spot where the logic breaks down
3. **Enables verification** — You can fact-check each step independently

**Empirical results** (from research):
- Zero-shot CoT on MultiArith: 17.7% → 78.7% accuracy
- Zero-shot CoT on GSM8K: 10.4% → 40.7% accuracy
- Works across reasoning tasks (math, logic, reading comprehension)

## Trade-Offs

**What it does well:**
- Dramatically improves reasoning accuracy
- Makes errors discoverable
- Works even without examples (zero-shot CoT)
- Parallelizable with Self-Consistency (run multiple chains, vote on best answer)

**What it sacrifices:**
- Length — outputs are much longer (you get the full reasoning chain)
- Speed — takes longer to read and validate all the steps
- Determinism — different reasoning paths can reach the same answer (sometimes desirable, sometimes not)

## What to Adjust

**For different scenarios:**

- **Math/Logic problems**: Use the basic form above. Longer reasoning chains actually improve accuracy here.
- **Ambiguous or subjective questions**: Add "What are the strongest counter-arguments?" to your thinking steps.
- **High-stakes decisions**: Combine with Self-Consistency (run 5-10 independent chains, take majority vote).
- **Speed-critical work**: Use Tree-of-Thoughts (branching paths) to explore key decision points without exploring dead ends.
- **Team communication**: Add "Explain in simple terms for someone without this background" as a final step.

## Example Input & Output

### Example: Evaluating a startup acquisition decision

**Your CoT Prompt:**

```
Let's work through this step-by-step.

Should Trenton recommend that Mariana Minerals acquire the copper mining asset in Moab (cost: $50M, expected NPV: $120M over 10 years)?

Think through:
1. What do we know for certain?
2. What assumptions are we making?
3. What are the key unknowns?
4. What steps need to happen in sequence?
5. What could go wrong at each step?

Only after documenting all of the above, provide your recommendation.
```

**Example Output (partial):**

```
1. What we know for certain:
   - Upfront cost: $50M
   - Expected NPV projection: $120M over 10 years
   - Asset location: Moab, Utah
   - Mariana currently has one project (Lithium One) under construction
   - Market: copper prices are historically volatile

2. What assumptions we're making:
   - The NPV projection is accurate (key assumption to validate)
   - Copper prices don't collapse below X price point
   - Mariana can successfully execute on ore extraction + process control
   - Environmental permitting won't face major delays (based on Lithium One experience)

3. Key unknowns:
   - What copper price assumptions are embedded in the $120M NPV?
   - How much execution risk is Mariana taking on? (They're still ramping Lithium One)
   - What's the project timeline? (5 years to cash positive? 10 years?)
   - How does this asset's risk profile compare to Lithium One?

4. Sequence needed:
   - Validate the NPV model and price assumptions
   - Assess Mariana's operational bandwidth (are they stretched?)
   - Evaluate permitting and timeline risk
   - Stress-test under downside copper price scenarios
   - Determine if this strains Mariana's capital position

5. What could go wrong:
   - Copper prices crater (happened 2022-2023); projected NPV becomes negative
   - Permitting delays push 5-year timeline to 8+ years
   - Mariana is operationally stretched and Lithium One + Copper project fail in parallel
   - Equipment/RL optimization doesn't translate from lithium to copper extraction processes

Recommendation: **Conditional Yes** — but validate the NPV model first, specifically copper price assumptions. If the model assumes sustained prices above $4/lb and that seems optimistic, discount the recommendation.
```

Notice: The reasoning is visible, challengeable, and step-by-step. You can argue with each assumption.

## Related Techniques

- **Tree-of-Thoughts (ToT)** — Explores multiple reasoning branches in parallel. Better for complex decisions with many unknowns.
- **Self-Consistency** — Run multiple independent CoT chains, take the majority answer. Improves accuracy 10-20% more.
- **Reflection/Critique** — After CoT, add a step: "What are the weakest parts of this reasoning?" to surface your own errors.
- **Level 4 Prompt Engineering** — Pair with CoT to structure the output. "Show your work in the thinking section, then provide final recommendation in a one-line summary."

## Common Mistakes

1. **Not checking the reasoning** — CoT is useless if you just read the final answer and ignore the chain. The value is in validating each step.
2. **Using it for simple questions** — Don't use CoT for "What's the weather tomorrow?" or "Define X." The overhead isn't worth it.
3. **Assuming one chain is enough** — For important decisions, run Self-Consistency (multiple chains) to see if the model contradicts itself.
4. **Expecting perfect reasoning** — CoT reduces errors but doesn't eliminate them. It makes errors visible so you can catch them.

## When NOT to Use

- **Simple factual questions** ("What year was X founded?") — CoT adds noise
- **Creative brainstorming** ("Generate startup ideas") — You want divergence, not detailed reasoning
- **Summarization** ("Summarize this article") — CoT makes outputs longer without improving quality

## Source

Research: Wei et al. (2022) "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (NeurIPS). Detailed in `prompt-engineering.md` KB section (Core Techniques, #3).

---

## Quick Cheat: When to Combine CoT With Other Techniques

| Situation | Combine With | Why |
|-----------|---|---|
| Important decision, time to verify | Self-Consistency | Run 5 chains, take majority vote |
| Decision tree with many branches | Tree-of-Thoughts | Explore key decision points systematically |
| Need both reasoning + structured output | Level 4 Prompting | CoT in the thinking section, structured format in output |
| Feedback loop with user | Reflection | After CoT, add "What are the weakest assumptions?" |
| Need to teach someone | Persona (Explainer) + CoT | "Explain your reasoning as if teaching a smart 15-year-old" |
