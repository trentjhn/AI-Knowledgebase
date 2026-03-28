# Red Team Pass Prompt

## When to Use

This prompt is an advanced technique for self-correction and quality assurance of AI-generated content. Use it when:
-   The AI has just completed a complex task or generated a significant output.
-   You need to rigorously audit the AI's response for factual errors, unsupported claims, exaggerations, or logical inconsistencies.
-   You want the AI to "debug" its own output before human review, saving time and improving final quality.
-   The stakes are high, and the output needs to be exceptionally clean and accurate.

## Why It Works

The Red Team Pass leverages the AI's own analytical capabilities by instructing it to adopt an adversarial persona. By switching roles and asking the AI to be a "hostile critic" of its *own previous output*, it forces a self-review from a completely different perspective. This technique is highly effective because it makes the AI actively search for flaws that it might have overlooked in its initial generation phase. The explicit instruction to "Mark every problem with [FLAG]" and then "produce a clean version" ensures a structured and actionable self-correction process.

## Architecture

This prompt works by creating a multi-turn, role-switching interaction:

1.  **Context Setting:** "You just completed this task: [paste AI's previous output]" establishes the target for the critique.
2.  **Role Switch Instruction:** "Now switch roles. You are now a hostile critic whose job is to find every hallucination, exaggeration, and unsupported claim in that response. Be ruthless." This is the core mechanism, changing the AI's operative persona.
3.  **Critique Mechanism:** "Mark every problem with [FLAG]." provides a clear signal for identified issues.
4.  **Correction Instruction:** "After the critique, produce a clean version with every flagged section fixed or removed." guides the AI to self-correct and deliver a refined output.

## Trade-Offs

**What it does well:**
-   Significantly improves the accuracy, factual basis, and overall quality of AI outputs.
-   Reduces hallucinations, exaggerations, and unsupported claims through rigorous self-auditing.
-   Leverages the AI's processing power to "debug itself" before human review.
-   Effective for complex, high-stakes tasks where errors are costly.

**What it sacrifices:**
-   Requires an additional turn of interaction after the initial output, adding to total processing time.
-   The quality of the critique and subsequent correction depends on the AI's ability to effectively switch roles and be genuinely "hostile" in its self-assessment.
-   The process might still benefit from human oversight to ensure the "fixed" version truly addresses all issues.

## Related Techniques

-   **Role-Play Prompting:** Explicitly instructs the AI to adopt a different persona.
-   **Self-Correction Protocols:** A form of iterative refinement where the AI reviews and improves its own work.
-   **Adversarial Prompting:** Uses an adversarial approach (critiquing) to enhance output quality.
-   **Meta-Cognitive Prompting:** Forces the AI to reflect on and evaluate its own output from a critical perspective.

## Example Use Case

You've asked an AI to generate a detailed competitive analysis report for a new market. After receiving the initial report, you would apply the Red Team Pass prompt. The AI would then re-read its own report, flagging any claims it couldn't fully support, any exaggerations, or any logical leaps. Following this critique, it would provide a revised, cleaner version of the report, ensuring a higher level of factual integrity before you present it.

## Source

This prompt was provided by a user during a Gemini CLI interaction, citing its effectiveness in debugging outputs before human review.