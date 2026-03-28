# Find Every Mistake Before It Costs You Prompt

## When to Use

This prompt is designed to act as a critical "pre-commit" auditor for your work, particularly within an ongoing conversation or project. Use it when you need to:
- Get a thorough, unbiased review of your reasoning, assumptions, and proposed actions.
- Proactively identify logical errors, blind spots, and unconsidered risks.
- Challenge your own overconfidence or unexamined beliefs before making commitments.
- Ensure the quality and robustness of your plans or decisions before moving forward.

## Why It Works

This prompt works by assigning the AI a highly critical persona with the explicit task of finding flaws. The `<rules>` section is crucial, forcing the AI to be direct, provide specific corrections, explicitly flag overconfidence, and conduct this review *before* you commit to your next step. This leverages the AI's analytical capabilities to act as a rigorous quality assurance step, minimizing costly mistakes.

## Architecture

This prompt uses a structured format to guide the AI's audit and feedback process:

1.  **Role (`<role>`):** Defines the AI's persona as a critical thinking auditor, setting the expectation for rigorous, no-holds-barred review.
2.  **Task (`<task>`):** Clearly states the objective: reviewing the conversation history to find mistakes, risks, and challenge thinking.
3.  **Steps (`<steps>`):** Breaks down the audit into explicit actions, guiding the AI through logical error identification, assumption flagging, overconfidence detection, and risk surfacing.
4.  **Rules (`<rules>`):** Imposes strict constraints on the AI's feedback, demanding direct challenges, specific corrections, explicit flags for overconfidence, and timely review before commitment.
5.  **Output (`<output>`):** Specifies a structured format for the audit results, making it easy to digest and act upon.

## Trade-Offs

**What it does well:**
- Significantly reduces errors, unexamined assumptions, and risks in ongoing work.
- Provides an objective, critical perspective that human biases might miss.
- Acts as a powerful quality gate, improving the robustness of decisions and plans.
- Encourages self-reflection and more thorough consideration of alternatives.

**What it sacrifices:**
- Requires patience and an open mind from the user to receive potentially challenging feedback.
- May add a slight delay to the workflow as the audit is conducted before proceeding.
- The depth and accuracy of the audit depend on the completeness and clarity of the conversation history provided.

## Related Techniques

-   **Persona Priming:** Assigns a specific role (critical thinking auditor) to direct the AI's analytical approach.
-   **Step-by-Step Reasoning:** The `<steps>` section guides the AI through a methodical review process.
-   **Constraint-Based Prompting:** The `<rules>` section enforces specific feedback characteristics (e.g., direct, specific corrections).
-   **Meta-Cognitive Prompting:** Forces the AI to perform a "review of a review" or a "critique of a critique," simulating a meta-cognitive process.

## Example Use Case

You've spent hours planning a complex feature, outlining technical designs and potential solutions. Before you commit to the implementation, you'd use this prompt to have the AI scrutinize your entire thought process, identify any logical leaps, question your assumptions about user behavior or system performance, and surface any risks you might have overlooked in your detailed plan. The AI would then present its findings, allowing you to refine your approach.

## Source

This prompt was provided by a user during a Gemini CLI interaction.