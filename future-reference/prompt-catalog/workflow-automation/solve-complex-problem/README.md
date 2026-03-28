# Solve Any Complex Problem Prompt

## When to Use

This prompt is designed to engage an AI model in a structured, adaptive problem-solving process. Use it when you face a complex issue and need the AI to:
- Deeply understand the problem before proposing solutions.
- Identify and fill information gaps.
- Challenge underlying assumptions that might lead to incorrect solutions.
- Deliver solutions calibrated to the appropriate level of detail (quick, medium, or deep).

## Why It Works

This prompt enforces a critical pre-computation phase, preventing the AI from "jumping to conclusions" or hallucinating solutions for an incompletely understood problem. By explicitly demanding an assessment of reasoning depth, identification of missing information, and challenging of assumptions, it guides the AI toward more robust and accurate problem-solving. It prioritizes methodical understanding over immediate (and potentially incorrect) answers.

## Architecture

This prompt uses a structured format to guide the AI's analytical and problem-solving process:

1.  **Role (`<role>`):** Defines the AI's persona as an adaptive problem solver, emphasizing a thoughtful, calibrated approach.
2.  **Task (`<task>`):** States the objective: analyzing a complex problem, assessing missing information, challenging assumptions, and solving at the correct depth.
3.  **Steps (`<steps>`):** Breaks down the problem-solving process into explicit actions, ensuring a methodical approach.
4.  **Rules (`<rules>`):** Imposes strict constraints on the AI's behavior, forcing it to assess before solving, flag missing information, challenge assumptions directly, and state its depth assessment.

## Trade-Offs

**What it does well:**
- Significantly reduces the risk of incorrect or irrelevant solutions due to premature conclusions.
- Encourages a deeper, more robust understanding of complex problems.
- Improves the quality and relevance of the AI's solutions by challenging assumptions and filling information gaps.
- Calibrates the solution's depth, avoiding both over-simplification and unnecessary complexity.

**What it sacrifices:**
- Requires more initial interaction and setup time as the AI will ask clarifying questions and challenge assumptions.
- May not be suitable for very simple, straightforward problems where an immediate answer is preferred.
- The effectiveness depends on the user's willingness to engage in the pre-solution assessment phase.

## Related Techniques

-   **Persona Priming:** Assigns a specific role (adaptive problem solver) to guide the AI's approach.
-   **Step-by-Step Reasoning:** The `<steps>` section encourages a methodical, analytical process.
-   **Assumption Mapping:** Explicitly includes a step for identifying and challenging assumptions, a critical thinking skill.
-   **Contextual Awareness:** The emphasis on assessing reasoning depth and identifying missing information makes the AI highly context-aware.

## Example Use Case

You're facing a tricky bug in a distributed system, and previous attempts to fix it have failed. You would use this prompt to guide the AI in a systematic diagnosis, challenging your own beliefs about the bug's cause and ensuring all relevant factors are considered before a solution is proposed. The AI might ask clarifying questions, suggest tests to confirm assumptions, or outline different architectural layers to investigate.

## Source

This prompt was provided by a user during a Gemini CLI interaction.