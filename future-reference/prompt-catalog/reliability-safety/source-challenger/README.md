# Source Challenger Prompt

## When to Use

This prompt is invaluable for tasks where factual accuracy and verifiable information are paramount. Use it when:
-   You need to minimize fabricated citations or "hallucinations" of sources.
-   You require transparency regarding the origin and reliability of information provided by the AI.
-   You are performing research, data gathering, or factual analysis where claims must be traceable.
-   You want to build a habit of critical assessment regarding AI outputs, even if you don't explicitly verify every source.

## Why It Works

The Source Challenger directly addresses the AI's tendency to generate plausible but false citations or make claims without clear provenance. By explicitly stating that the user *will* ask for sources and then instructing the AI to provide them upfront, it forces the model to engage in a more rigorous internal search for factual grounding. This pre-emptive sourcing significantly reduces the likelihood of fabricated content, as the AI "knows" it will be challenged.

## Architecture

This prompt works by embedding a conditional, post-processing instruction that inverts the typical user-AI interaction:

1.  **Core Task Instruction:** "Complete this task: [task]" sets the primary objective.
2.  **Pre-emptive Question:** "After your response, I will ask you one question: 'Where does each key claim in this response come from?' Answer that question now, before I ask it." This is the core mechanism, forcing the AI to self-source.
3.  **Sourcing Format:** "For every claim: cite the type of source, the approximate time period, and your confidence level." provides a structured format for the required sourcing information.
4.  **Flagging Mechanism:** "If you can't source it, flag it." ensures transparency about unsourced claims.

## Trade-Offs

**What it does well:**
-   Dramatically reduces fabricated citations and unsourced claims (reported 67% reduction in NVIDIA's workflows).
-   Increases the verifiability and trustworthiness of AI outputs.
-   Promotes a higher standard of factual rigor in AI interactions.
-   Helps users quickly identify which claims are strongly supported versus those that are not.

**What it sacrifices:**
-   Adds to the length of the AI's response, as sourcing information is appended.
-   May increase processing time slightly as the AI performs the self-sourcing task.
-   Requires the AI to have access to and be able to recall/search relevant sources, which might vary depending on the model's capabilities and context window.

## Related Techniques

-   **Meta-Cognitive Prompting:** Forces the AI to reflect on the origin of its own knowledge.
-   **Verifiability Protocols:** Aims to make AI outputs more easily verifiable by human users.
-   **Honesty Protocols:** By flagging unsourced claims, it promotes transparency and honesty.
-   **Constraint-Based Prompting:** Uses the requirement to source as a strong constraint on output quality.

## Example Use Case

You are using an AI to gather information for a business report that requires all claims to be substantiated. By using the Source Challenger, the AI will provide its answer and then immediately follow up with citations for each key piece of information, including an assessment of the source type and its confidence in that source. This allows you to quickly assess the reliability of the information and know where to dig deeper if needed.

## Source

This prompt was provided by a user during a Gemini CLI interaction, citing its effectiveness in NVIDIA's workflows.