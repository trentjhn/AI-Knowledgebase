# Write Every Slide's Content Prompt

## When to Use

This prompt is invaluable for generating clear, concise, and impactful content for your presentation slides. Use it when you need to:
- Translate your slide structure (titles and purposes) into presentation-ready bullet points.
- Ensure that each slide communicates a single, clear idea without overwhelming the audience.
- Match the language complexity to your target audience.
- Achieve a consistent, headline-style language suitable for spoken presentations.

## Why It Works

This prompt acts as a specialized content writer, applying best practices for presentation content directly. By setting strict rules like "Maximum 5 bullets per slide" and "No full sentences," it forces conciseness and clarity, making the content easy to consume during a live presentation. It prevents slides from becoming text-heavy documents and ensures that each bullet point serves a precise communication goal. The focus on one idea per slide is crucial for audience comprehension and retention.

## Architecture

This prompt uses a structured format to guide the AI's content generation process:

1.  **Role:** Defines the AI's persona as a slide content writer, emphasizing clarity and conciseness.
2.  **Task:** Clearly states the goal: writing complete, presentation-ready content for every slide.
3.  **Steps:** Outlines a logical sequence for generating bullet points, ensuring clear ideas, matching language to audience, and flagging overloaded slides.
4.  **Rules:** Imposes strict quality constraints, such as limiting bullet points, enforcing headline-style language, and ensuring one idea per slide.
5.  **Output:** Specifies the desired structure for the content, including bullet points and flags for issues.

## Trade-Offs

**What it does well:**
- Produces highly effective and audience-friendly presentation content.
- Enforces conciseness and clarity, making slides impactful.
- Saves time by generating content that adheres to presentation best practices.
- Helps avoid the common pitfall of text-heavy, difficult-to-read slides.

**What it sacrifices:**
- Requires initial input of the slide structure (titles, purposes) and target audience.
- The AI's content generation is based on its training data; fine-tuning for very specific domain knowledge might require additional input or human review.
- While concise, human review is still needed to ensure the tone and nuance perfectly match the presenter's style.

## Related Techniques

-   **Persona Priming:** Assigns an expert role to guide the AI's content creation process.
-   **Constraint-Based Prompting:** Uses strict rules (e.g., max bullets, no full sentences) to shape the output format and style.
-   **Content Generation:** Directly guides the AI in generating specific content types.
-   **Clarity & Conciseness Principles:** Guides the AI to apply best practices for effective presentation communication.

## Example Use Case

After designing the structure of your presentation (e.g., using the "Design Every Slide Before You Write" prompt), you would use this prompt. You'd feed it the title and purpose for each slide, and the AI would generate 3-5 concise, headline-style bullet points per slide, ensuring each bullet conveys a single idea, all tailored to your specific audience. For example, for a "Problem Statement" slide, it might generate bullet points highlighting key challenges and their impact.

## Source

This prompt was provided by a user during a Gemini CLI interaction.