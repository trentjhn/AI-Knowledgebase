# Boundary Setter Prompt

## When to Use

This prompt is a critical safety and control mechanism, especially when interacting with AI models in sensitive contexts. Use it when:
-   You need to prevent the AI from generating specific types of undesirable, harmful, or inaccurate content.
-   The task involves sensitive information, potential for misinformation, or actions that could lead to negative consequences.
-   You want to enforce strict adherence to ethical guidelines, factual accuracy, or content policies.
-   You have experienced the AI overstepping boundaries or making inappropriate suggestions in previous interactions.

## Why It Works

The Boundary Setter prompt leverages the power of explicit, negative constraints to control AI behavior. By defining "hard stops" – actions the AI *must never* perform – it creates robust guardrails that outperform vague or positive instructions. This approach reduces the model's degrees of freedom in undesirable directions, making its output more predictable, safer, and aligned with user expectations. It addresses the challenge that AI models, by default, may prioritize task completion over adherence to implicit ethical or factual boundaries.

## Architecture

This prompt works by establishing a set of non-negotiable rules for the AI's output:

1.  **Context Setting:** "You are helping me with: [task]" establishes the general purpose of the interaction.
2.  **Hard Stop Declaration:** "Here is what you must never do in this response:" introduces the list of explicit negative constraints.
3.  **Specific Prohibitions:** Each bullet point (e.g., "Never invent statistics without flagging them," "Never suggest actions that could cause [specific harm]") details an action or type of content that is strictly forbidden.
4.  **Enforcement Statement:** "These are hard stops. Not guidelines." unequivocally communicates the non-negotiable nature of the constraints.

## Trade-Offs

**What it does well:**
-   Significantly enhances the safety and ethical alignment of AI outputs.
-   Reduces the generation of misinformation, harmful content, or inappropriate suggestions.
-   Increases the predictability and controllability of AI behavior in sensitive tasks.
-   Provides a clear framework for defining acceptable and unacceptable content.

**What it sacrifices:**
-   May reduce the AI's creativity or spontaneity in areas close to the defined boundaries.
-   Requires careful thought from the user to define comprehensive and unambiguous "hard stops."
-   Over-constraining the AI with too many boundaries might make it difficult to complete legitimate tasks, though for critical safety, this is often an acceptable trade-off.

## Related Techniques

-   **Constraint-Based Prompting:** A primary example of using explicit constraints (especially negative ones) to control AI behavior.
-   **Safety Protocols:** Aims to embed safety mechanisms directly into the AI's operational guidelines.
-   **Ethical AI Design:** Directly supports the implementation of ethical principles within AI interactions.
-   **Guardrails:** Establishes explicit boundaries to prevent the AI from veering into undesirable territory.

## Example Use Case

You are using an AI to generate medical information for educational purposes, and it's critical that the AI does not provide diagnostic advice or invent statistics. By using the Boundary Setter, you would explicitly instruct the AI: "Never offer medical diagnoses," and "Never invent statistics without flagging them as hypothetical." This ensures the AI remains within its defined safe operating parameters.

## Source

This prompt was provided by a user during a Gemini CLI interaction, citing its effectiveness in outperforming soft instructions.