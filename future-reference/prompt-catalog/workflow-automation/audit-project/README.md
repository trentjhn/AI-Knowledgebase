# Audit Your Entire Project Prompt

## When to Use

This prompt is designed for leveraging an AI model as a senior software architect to perform a comprehensive audit of a project. Use it when you need to:
- Identify architectural flaws and areas for improvement.
- Surface technical debt and prioritize its resolution.
- Detect security vulnerabilities and performance bottlenecks.
- Get a prioritized, actionable plan for project enhancement and risk mitigation.

## Why It Works

This prompt works by clearly defining a highly specialized persona for the AI, assigning a complex multi-faceted task, and providing explicit steps and rules for execution. The `<rules>` section forces the AI to be actionable, impactful, and clear, delivering specific fixes rather than vague warnings. The structured output further ensures that the audit is easily digestible and actionable, prioritizing high-impact issues.

## Architecture

This prompt uses a structured format to guide the AI's analysis and output:

1.  **Role (`<role>`):** Defines the AI's persona as a senior software architect, setting the expectation for expertise and strategic thinking.
2.  **Task (`<task>`):** Clearly states the objective: a full project analysis for flaws, risks, and performance issues.
3.  **Steps (`<steps>`):** Breaks down the audit process into sequential actions, guiding the AI's workflow.
4.  **Rules (`<rules>`):** Imposes strict constraints on the AI's findings and recommendations, ensuring they are specific, prioritized, and executable.
5.  **Output (`<output>`):** Specifies the desired structure for the final deliverable, making the audit results easy to interpret.

## Trade-Offs

**What it does well:**
- Provides a structured, expert-level project audit.
- Delivers actionable, prioritized recommendations.
- Focuses on high-impact fixes and critical issues like security.
- Standardizes the audit process for consistency.

**What it sacrifices:**
- Requires the user to provide comprehensive project files (which is outside the AI's direct capability, requiring user interaction).
- The depth of the audit is dependent on the completeness and quality of the provided project context.
- May require iteration or clarification if the AI's initial findings are not perfectly aligned with specific project nuances.

## Related Techniques

-   **Persona Priming:** Emphasizes giving the AI a specific role to enhance the quality of its analysis.
-   **Step-by-Step Reasoning:** The `<steps>` section encourages a methodical, structured approach to analysis.
-   **Constraint-Based Prompting:** The `<rules>` section imposes strict output and content requirements.

## Example Use Case

Imagine you've inherited an existing codebase and need a quick, high-level but actionable assessment of its health. You would provide this prompt to an AI and then follow its instruction to upload relevant project documentation, code snippets, dependency lists, etc., to receive a prioritized action plan for improvement.

## Source

This prompt was provided by a user during a Gemini CLI interaction.