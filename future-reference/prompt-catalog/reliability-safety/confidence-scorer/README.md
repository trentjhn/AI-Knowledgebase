# Confidence Scorer Prompt

## When to Use

This prompt is a valuable tool for critical evaluation and risk assessment of AI-generated content. Use it when:
-   Accuracy and factual correctness are essential, but the AI's response might contain a mix of high-confidence and speculative claims.
-   You need to quickly identify which parts of an AI's output require human verification.
-   You want to train yourself or the AI to be more aware of the reliability of its own statements.
-   You are dealing with sensitive information where even low-confidence errors can be costly.

## Why It Works

The Confidence Scorer forces the AI to perform a meta-cognitive task: auditing its own output for reliability *before* the user reviews it. By assigning a clear, three-tiered scale (HIGH, MEDIUM, LOW) and explicitly defining what each level means, it provides a structured way for the AI to signal the trustworthiness of its claims. This upfront self-assessment shifts the burden of initial vetting from the human to the AI, making human review more efficient and targeted.

## Architecture

This prompt works by embedding specific post-processing instructions within a larger task:

1.  **Core Task (Implicit):** The AI first completes its primary task (indicated by "After completing your response...").
2.  **Self-Audit Instruction:** "go back and score every factual claim on this scale:" directs the AI to review its own generated content.
3.  **Confidence Scale Definition:** "[HIGH] - You would stake your reputation on this, [MEDIUM] - You believe this but recommend verifying, [LOW] - This is your best guess, treat with caution" provides clear, actionable definitions for scoring.
4.  **Labeling Requirement:** "Label every claim before I read it." ensures the self-assessment is clearly presented to the user.
5.  **User Intent:** "I will verify the LOW ones myself." communicates the human's strategy, further reinforcing the value of the AI's scoring.

## Trade-Offs

**What it does well:**
-   Enhances the reliability and transparency of AI outputs.
-   Streamlines the human verification process by highlighting areas of uncertainty.
-   Helps prevent acting on low-confidence information as if it were highly reliable.
-   Encourages the AI to develop a more nuanced understanding of its own knowledge boundaries.

**What it sacrifices:**
-   May add a small amount of processing time as the AI performs the self-audit.
-   The accuracy of the AI's self-assigned confidence scores is still dependent on the model's internal calibration, though it tends to be more reliable when explicitly prompted.
-   The user still bears the ultimate responsibility for verifying claims, especially those marked MEDIUM or LOW.

## Related Techniques

-   **Meta-Cognitive Prompting:** Forces the AI to reflect on and evaluate its own output.
-   **Self-Auditing:** A form of self-correction where the AI reviews its own work.
-   **Confidence Scoring:** Explicitly requesting the AI to quantify its certainty.
-   **Risk Assessment:** Helps in quickly identifying claims with higher associated risk.

## Example Use Case

You're asking an AI to summarize a scientific paper on a novel topic, and you need to quickly understand which findings are well-established versus those that are more speculative. By using the Confidence Scorer, the AI will label each claim in its summary, allowing you to prioritize your own deeper dives into the source material for the "MEDIUM" and "LOW" confidence statements.

## Source

This prompt was provided by a user during a Gemini CLI interaction, citing its effectiveness in forcing the model to audit itself.