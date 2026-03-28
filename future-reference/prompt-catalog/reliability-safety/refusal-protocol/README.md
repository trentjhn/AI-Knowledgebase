# Refusal Protocol Prompt

## When to Use

This prompt is a foundational tool for enhancing the reliability and honesty of AI model outputs. Use it when:
-   Accuracy is paramount and hallucination must be minimized.
-   You need to clearly identify gaps in the AI's knowledge.
-   You want to avoid the AI making assumptions to fill missing information.
-   You prefer incomplete but honest answers over complete but potentially incorrect ones.

## Why It Works

The Refusal Protocol directly addresses the AI's tendency to "confidently guess" or hallucinate when faced with uncertainty. By explicitly instructing the AI to declare uncertainty or inability to complete a task, it creates a clear framework for honest reporting. The rule "Incomplete and honest beats complete and wrong" realigns the AI's objective towards truthfulness, significantly reducing the generation of fabricated information.

## Architecture

This prompt works by embedding specific conditional instructions within a larger task:

1.  **Core Task Instruction:** "Complete this task: [task]" sets the primary objective.
2.  **Uncertainty Clause:** "If at any point you are uncertain about a fact, stop and write: UNCERTAIN: [what you don't know]" creates a specific reporting mechanism for factual gaps.
3.  **Inability Clause:** "If you cannot complete any part of the request accurately, write: CANNOT COMPLETE: [specific reason]" provides a mechanism for the AI to gracefully decline or partially fulfill a request if it lacks sufficient capability or information.
4.  **Anti-Assumption Rule:** "Never fill gaps with assumptions. Incomplete and honest beats complete and wrong." reinforces the core principle of honesty and prevents implicit fabrication.

## Trade-Offs

**What it does well:**
-   Significantly reduces hallucination and fabricated content (reported 41% reduction in internal tests).
-   Increases the trustworthiness and reliability of AI outputs.
-   Helps in identifying the limits of the AI's knowledge and capabilities.
-   Promotes transparency in AI interactions.

**What it sacrifices:**
-   May lead to more "incomplete" answers, requiring further human intervention or clarification.
-   The AI might be overly cautious, refusing to answer even when it could provide a reasonably good guess (though this is often the desired behavior for critical tasks).
-   Requires careful framing of the initial `[task]` to ensure the AI understands the scope of what it needs to complete.

## Related Techniques

-   **Constraint-Based Prompting:** Uses negative constraints ("Never fill gaps with assumptions") and positive constraints ("write: UNCERTAIN...") to guide behavior.
-   **Honesty Protocols:** Aims to improve the truthfulness of AI outputs.
-   **Meta-Cognitive Prompting:** Forces the AI to reflect on its own knowledge state and capabilities.

## Example Use Case

You are using an AI to extract specific, verifiable data from a large legal document. You would use the Refusal Protocol to ensure that if the AI cannot find a piece of information or is uncertain about a legal interpretation, it explicitly flags this rather than inferring or fabricating an answer. This prevents potentially critical errors in legal analysis.

## Source

This prompt was provided by a user during a Gemini CLI interaction, citing its effectiveness in internal tests.