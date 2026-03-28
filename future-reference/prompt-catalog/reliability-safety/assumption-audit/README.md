# Assumption Audit Prompt

## When to Use

This prompt is a crucial technique for preventing miscommunication and ensuring alignment before the AI undertakes a task. Use it when:
-   The task is complex, ambiguous, or highly context-dependent.
-   You want to avoid outputs that are technically correct but miss the mark due to unstated differences in understanding.
-   You need to proactively surface and correct hidden assumptions the AI might make about your knowledge, intent, or constraints.
-   You are collaborating on a project and need to ensure shared understanding with the AI partner.

## Why It Works

Many suboptimal AI outputs stem from implicit, incorrect assumptions made by the model that go uncorrected. The Assumption Audit forces the AI to explicitly state its foundational beliefs about the interaction *before* generating a response. By putting the onus on the AI to articulate its assumptions and then giving the user the opportunity to confirm or correct them, this prompt ensures a shared understanding, leading to significantly more relevant and accurate outputs.

## Architecture

This prompt works by enforcing a mandatory pre-computation phase focused on meta-cognition:

1.  **Pre-computation Instruction:** "Before answering my question, list every assumption you are making about:" clearly establishes the requirement to surface assumptions first.
2.  **Assumption Categories:** Specific categories ("What I already know," "What I want the output used for," "What constraints I'm operating under," "What counts as a good answer here") guide the AI to consider different facets of the interaction.
3.  **Confirmation/Correction Request:** "Then ask me to confirm or correct each assumption." transfers control to the user for validation.
4.  **Deferred Task Execution:** "Only start the actual task after I respond." ensures the core task is only addressed once assumptions are aligned.

## Trade-Offs

**What it does well:**
-   Significantly improves the relevance and accuracy of AI outputs by preventing misaligned assumptions.
-   Reduces wasted effort on outputs that would otherwise need extensive revision.
-   Fosters a more collaborative and communicative interaction style with the AI.
-   Helps both the user and the AI achieve a deeper, shared understanding of the task.

**What it sacrifices:**
-   Adds an extra turn (or more) to the conversation before the AI performs the main task.
-   Requires active engagement from the user to review and correct assumptions.
-   May feel unnecessary for very simple, unambiguous tasks.

## Related Techniques

-   **Meta-Cognitive Prompting:** Forces the AI to reflect on its own understanding and the context of the interaction.
-   **Clarification Dialogue:** Initiates a structured conversation to clarify expectations.
-   **Pre-computation Analysis:** Demands a phase of analysis *before* generating a solution.
-   **Constraint-Based Prompting:** The "Only start the actual task after I respond" acts as a strong constraint.

## Example Use Case

You're asking an AI to draft a marketing campaign for a new product, but you haven't explicitly told it your target audience, budget, or preferred tone. By using the Assumption Audit, the AI would first list its assumptions (e.g., "Target audience is tech-savvy millennials," "Budget is unlimited," "Tone should be informal"). You could then correct these assumptions, leading to a campaign draft that is much more aligned with your actual needs.

## Source

This prompt was provided by a user during a Gemini CLI interaction, citing its effectiveness in preventing bad outputs.