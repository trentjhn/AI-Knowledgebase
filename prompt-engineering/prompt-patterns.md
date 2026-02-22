# Prompt Patterns: A Catalog of Reusable Prompting Solutions

> Source: "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT" — White et al., Vanderbilt University, 2023

---

## What Are Prompt Patterns?

If you've ever written code, you've probably heard of *design patterns* — reusable solutions to common programming problems like "how do I handle multiple objects that need to do the same thing?" or "how do I decouple the parts of my system so they don't depend on each other?" These patterns don't tell you exactly what code to write; they give you a *template for thinking* that you adapt to your specific situation.

Prompt patterns work the same way for conversations with AI. When you interact with an LLM repeatedly, you start to notice that certain types of problems come up over and over: you want more accurate outputs, you want the model to ask you questions instead of guessing, you want it to generate structured output in a specific format, or you want to get better answers without having to become an expert in the topic first. Each of these recurring problems has a prompt pattern — a reusable approach that applies across hundreds of different topics and tasks.

The catalog below was developed by researchers at Vanderbilt University who studied hundreds of real interactions with ChatGPT. They identified 16 distinct patterns and organized them into 6 categories based on what problem each one solves. Think of this as your toolkit: you don't use every tool on every job, but knowing what tools exist means you're never stuck.

---

## How to Use This Catalog

Each pattern is described with:
- **What it does** — the problem it solves, in plain English
- **The core structure** — the key phrases that activate the pattern
- **A concrete example** — so you can see it in action
- **When and how to combine it** — patterns work together, and the combinations are often more powerful than any single pattern

You'll notice that patterns from different categories can be combined freely. The Vanderbilt researchers found that mixing 2–3 patterns in a single prompt creates capabilities that feel surprisingly sophisticated — like turning an LLM into a cybersecurity training game simply by combining Persona + Game Play + Visualization Generator.

---

## Category 1: Input Semantics — Teaching the LLM Your Language

These patterns deal with *how input is interpreted*. The fundamental challenge they address: natural language is ambiguous, and typing out full instructions every time is tedious. What if the LLM could learn your shorthand?

---

### Meta Language Creation

**What it does:** You define a custom shorthand or symbolic language, teach the LLM what it means once, and then use that shorthand for the rest of the conversation. Instead of typing "please generate Python code that handles authentication," you type something like `CODEGEN:auth:python` and the model knows exactly what you mean.

This pattern is most useful when you're doing repetitive, specialized work — like generating code for many different functions, or building a structured dataset — and you want a compact input format that maps unambiguously to your intent. Unlike natural language, a well-designed meta language eliminates the ambiguity that causes LLMs to misinterpret your requests.

**Core structure:**
```
When I type X, I want you to do Y.
When I type Z, I want you to do W.
[Continue defining your language...]
From now on, respond to these codes accordingly.
```

**Example:**
```
I'm going to define some shortcodes for code generation. When I type:
  CRUD [entity] [language] — generate complete Create, Read, Update, Delete operations for [entity] in [language]
  TESTS [function] — generate unit tests for [function]
  DOCS [module] — generate API documentation for [module]
From now on, respond to these codes with the corresponding output.

CRUD User python
```

**When to use it:** You're doing a high-volume, repetitive task where the same pattern of request recurs many times. The upfront investment of defining the language pays off quickly.

**Caution:** The meta language can drift — if you use a natural language question later that conflicts with a code you defined, the LLM may misinterpret it. Keep meta languages scoped to distinct tasks or start fresh conversations when switching contexts.

---

## Category 2: Output Customization — Controlling What You Get Back

These patterns shape *what form the output takes* — its structure, style, level of detail, and format. Use them when the LLM's default response style doesn't match your needs.

---

### Output Automater

**What it does:** Instead of describing a series of steps and then manually executing them, you ask the LLM to write a script that will execute those steps for you automatically. The LLM becomes not just an advisor but a code generator that turns its own suggestions into runnable automation.

This pattern is particularly valuable for multi-step technical tasks. If an LLM tells you "first do A, then B, then C, then D," there are many opportunities for human error. An automatically generated script eliminates that risk.

**Core structure:**
```
Whenever you suggest a sequence of steps that I should perform,
also create a [bash/Python/etc.] script that performs those steps automatically.
```

**Example:**
```
Whenever you suggest a sequence of terminal commands I should run,
also provide a bash script I can run directly to execute them.

How do I set up a fresh Ubuntu server for a Node.js web application?
```

The LLM will both explain the setup and give you a deployable script.

**When to use it:** Any time the output consists of a sequence of executable steps rather than just information. Particularly powerful for DevOps, system administration, and deployment tasks.

---

### Persona

**What it does:** You ask the LLM to adopt a specific character, role, or domain identity. This goes well beyond just telling it "act like an expert" — a persona gives the model a named, scoped identity that consistently shapes its vocabulary, perspective, and what it includes or excludes from its answers.

The key insight is that the persona constrains output in useful ways. A "skeptical senior engineer reviewing a pull request" will give different (and often more useful) feedback than just asking for "feedback on this code."

**Core structure:**
```
Act as [persona]. When acting as [persona], your responses should reflect [key traits].
```

**Examples:**
```
Act as a Linux terminal for a computer running Ubuntu 22.04.
When I type a command, respond with the terminal output that command would produce.
Do not provide explanations — only terminal output.
```

```
Act as a skeptical security researcher reviewing my code.
Flag any potential vulnerabilities, assume adversarial users, and don't let me off easy.
```

**When to use it:** When you want a consistent perspective maintained across a long conversation, or when you want output that reflects a specific expertise domain or communication style.

**Combine with:** Game Play (to run simulations), Reflection (to explain the persona's reasoning), Visualization Generator (to add visual outputs to the persona's responses).

---

### Visualization Generator

**What it does:** LLMs can't generate images — but they can generate *inputs for tools that do*. This pattern asks the LLM to produce text-based specifications (like Graphviz DOT code, Mermaid diagrams, or DALL-E prompts) that you then feed into a visualization tool to produce the actual image.

This bridges the gap between LLM text generation and visual communication. Concepts like system architecture, process flows, and data relationships are much easier to understand visually, but writing the DOT or Mermaid syntax yourself is tedious.

**Core structure:**
```
Whenever I ask you to visualize something, generate [format] that I can provide to [tool] to create the visualization.
```

**Example:**
```
Whenever I ask you to visualize something, generate either a Graphviz DOT file
or a Mermaid diagram — choose whichever is more appropriate for what needs to be shown.

Visualize the relationships between the components of a microservices authentication system.
```

The LLM will select the right format (probably Mermaid for a flow/relationship diagram) and generate the code.

**When to use it:** Explaining architectures, process flows, decision trees, entity relationships — anywhere a diagram would be clearer than prose.

---

### Template

**What it does:** You provide an exact output structure with named placeholders, and the LLM fills in those placeholders while preserving the rest of the format exactly. This is essential when you need output in a format that the LLM wouldn't produce on its own — a specific URL structure, a precise JSON schema, a fill-in-the-blank form letter.

**Core structure:**
```
I am going to provide a template for your output.
[PLACEHOLDER] marks where you should insert content.
Preserve the formatting and overall template exactly.
Template: [your template with PLACEHOLDERS]
```

**Example:**
```
I am going to provide a template for your output.
Everything in all caps is a placeholder.
Fit your output into one or more placeholders.
Preserve the formatting exactly.

Template: https://api.myapp.com/users/NAME/posts/POST_SLUG/tags/TAG_LIST
```

User: "Generate an entry for a user named Sarah Chen who wrote a post called 'Getting Started with Docker' tagged with devops and containers."

LLM: `https://api.myapp.com/users/sarah-chen/posts/getting-started-with-docker/tags/devops,containers`

**When to use it:** When you need output embedded in a specific structure — URLs, JSON objects, form letters, code templates — that the LLM wouldn't naturally produce in the right format.

**Caution:** The Template pattern can conflict with other Output Customization patterns since it tightly constrains format. Hard to combine with Recipe, for example.

---

### Infinite Generation

**What it does:** You establish a generation rule once, then the LLM produces output repeatedly (potentially indefinitely) without you having to retype the prompt each time. You control the rate of generation and optionally provide refinements between each output.

This is valuable for batch content generation — creating many variations of something, generating a dataset, or repeatedly applying the same transformation to different inputs.

**Core structure:**
```
I would like you to generate [output type] forever, [N] at a time.
[Optional: instructions for how to use my input between outputs]
[Optional: stop when I say STOP]
```

**Example:**
```
From now on, generate a product name and tagline for a SaaS company, 2 at a time.
After each pair, wait for me to tell you a theme or adjective, and incorporate it into the next pair.
Stop when I say DONE.
```

**When to use it:** Batch content creation, dataset generation, repetitive transformations. Particularly powerful when combined with Template (to format each output consistently).

**Caution:** As the conversation grows long, the LLM's context window fills with previous outputs. The original prompt instructions can "fade" and the model may drift from the intended behavior. Monitor outputs and restate instructions if needed.

---

## Category 3: Error Identification — Catching What Goes Wrong

LLMs make mistakes. These patterns help surface errors, false facts, and flawed reasoning before they cause problems — especially useful when you're not an expert in the topic you're discussing.

---

### Fact Check List

**What it does:** You instruct the LLM to append a list of factual claims to its answer — claims that you (or another source) should verify. The LLM flags its own potentially incorrect statements rather than presenting them as settled fact.

This is subtle but powerful: the LLM knows what kinds of things it tends to get wrong (specific version numbers, dates, statistics, API details). Asking it to explicitly surface those claims gives you a quality-control checklist without requiring you to be an expert.

**Core structure:**
```
When you provide an answer, generate a set of facts that the answer depends on that should be fact-checked.
List these facts at the end of your response.
[Optional: only include facts related to X domain]
```

**Example:**
```
When you provide answers about setting up cloud infrastructure,
generate a list of specific facts I should verify — especially version numbers,
pricing, and service names — since these change frequently.

How do I set up a PostgreSQL database on AWS RDS?
```

The response will end with: *"Facts to verify: RDS PostgreSQL currently supports up to version X.X. The db.t3.micro instance type is free-tier eligible. The maximum storage is Y GB for this tier..."*

**When to use it:** When you're learning a new domain and can't easily spot errors yourself. Particularly valuable for technical setups, medical/legal information, and anything involving specific numbers or dates.

**Combine with:** Question Refinement (refine your question, then fact-check the answer). Works well as a standing instruction at the start of a long conversation about an unfamiliar topic.

---

### Reflection

**What it does:** After answering a question, the LLM explains its reasoning and the assumptions it made. This makes the "thinking" visible, which lets you catch errors in logic, spot assumptions you disagree with, and understand *why* the LLM gave the answer it did.

Without this pattern, LLMs present conclusions confidently without showing their work. The Reflection pattern is essentially asking the model to "show your work" — which is how you catch mistakes before acting on them.

**Core structure:**
```
Whenever you generate an answer, explain the reasoning and assumptions behind it.
[Optional: ...so that I can improve my question]
[Optional: ...tailored to [domain]-specific concerns]
```

**Example:**
```
When you provide answers about software architecture decisions,
explain the reasoning and assumptions behind your recommendations,
include specific evidence or examples where possible,
and address any ambiguities or limitations in your answer.
```

**When to use it:** Architecture decisions, debugging help, strategic recommendations — anywhere the *why* matters as much as the *what*, and where you want to validate the logic, not just accept the conclusion.

**Combine with:** Fact Check List (reasoning + facts = full transparency). Combine with Alternative Approaches to see both the reasoning for the recommended approach and the trade-offs of alternatives.

---

## Category 4: Prompt Improvement — Getting Better Answers

These patterns help you ask better questions — either by having the LLM help you rephrase, by forcing more careful reasoning, or by exploring the problem from multiple angles before committing to an approach.

---

### Question Refinement

**What it does:** Before answering your question, the LLM suggests a better version of your question. This is enormously useful when you're new to a topic — you often don't know enough to ask the *right* question, which means you get answers to the wrong question.

This pattern essentially uses the LLM's domain expertise to compensate for your inexperience in framing the problem.

**Core structure:**
```
Whenever I ask you a question, suggest a better version of my question that I should ask instead.
[Optional: ask me if I want to use the refined version or the original]
```

**Example:**
```
Whenever I ask a question about database design,
suggest a more precise and complete version of my question before answering it.

How do I make my queries faster?
```

LLM: *"A more complete version of your question might be: 'Given a PostgreSQL database with [table structure], what indexing strategies, query optimizations, and schema changes would reduce query latency for [specific access pattern]?' Would you like me to answer your original question or this refined version?"*

**When to use it:** When exploring unfamiliar topics, when you know what you want but not how to ask for it, or when you've been getting answers that feel slightly off from what you needed.

---

### Alternative Approaches

**What it does:** For every solution the LLM suggests, it also presents alternative ways to accomplish the same goal. This prevents premature lock-in to the first reasonable-sounding approach and exposes trade-offs you might not have considered.

Software developers intuitively know this: there are always at least three ways to solve any problem, and the "obvious" one isn't always the best for your specific constraints.

**Core structure:**
```
Whenever you suggest a solution to a problem,
also provide N alternative approaches that could also solve the problem.
Compare the trade-offs of each approach.
```

**Example:**
```
Whenever you recommend how to implement a feature,
also describe 2 alternative implementation approaches
and briefly compare the trade-offs of all three.

How should I implement user authentication in my Express.js app?
```

**When to use it:** Any design or architectural decision where you're committing to an approach. Prevents tunnel vision on the first suggestion.

**Combine with:** Reflection (understand the reasoning behind each alternative) and Cognitive Verifier (decompose the trade-off analysis into sub-questions).

---

### Cognitive Verifier

**What it does:** You ask the LLM to break your question into smaller sub-questions, answer each independently, and then synthesize those answers into a final response. This forces more careful, structured reasoning than asking for an answer directly — particularly for complex questions where the right answer depends on correctly reasoning through multiple sub-problems.

The name comes from cognitive science: breaking complex problems into sub-problems and synthesizing them leads to more accurate reasoning than attempting to answer holistically.

**Core structure:**
```
When you are asked a question, generate a set of sub-questions that help answer the original question.
Answer each sub-question individually.
Use the sub-answers to answer the original question.
```

**Example:**
```
When I ask you a question, break it into 3-5 sub-questions,
answer each one, then synthesize them into a final answer.

Should I use microservices or a monolith for my new startup's backend?
```

The LLM will then reason through: What is the team size and expertise? What's the expected traffic pattern? How rapidly will requirements change? What's the operational complexity tolerance? — before synthesizing a recommendation.

**When to use it:** Complex, multi-factor decisions where getting the answer right requires carefully reasoning through several components. Architecture decisions, business strategy questions, debugging complex problems.

---

### Refusal Breaker

**What it does:** When the LLM refuses to answer a question, it explains why and suggests alternative phrasings that it *would* answer. This helps users who got a refusal because the question was ambiguously phrased (or touched a false positive in content filters) to find a legitimate path forward.

**Important caveat:** This pattern has dual-use potential and should be applied thoughtfully. It exists to help users rephrase poorly-worded legitimate questions — not to circumvent appropriate content restrictions.

**Core structure:**
```
Whenever you can't answer a question, explain why you can't answer it
and provide one or more alternative wordings of the question that you could answer.
```

**Example application:** If you ask about security vulnerabilities in a way that triggers a refusal, the LLM can explain "I can't describe how to exploit this vulnerability, but I can explain how to detect it and how to write defensive code against it" — and rephrase your question accordingly.

**When to use it:** When you've received a refusal that seems like a false positive — your intent is legitimate but your phrasing triggered a content filter.

---

## Category 5: Interaction — Changing Who Asks the Questions

These patterns flip or restructure the fundamental dynamics of the conversation. Instead of you always asking and the LLM always answering, these patterns create richer, more dynamic interactions.

---

### Flipped Interaction

**What it does:** Instead of you asking questions and the LLM answering, the LLM asks *you* questions and uses your answers to build understanding before responding. This is particularly valuable when the LLM needs information from you to give a good answer — but you don't know what information it needs.

Think of it like the difference between going to a doctor who just prescribes based on your self-diagnosis versus one who asks you questions to properly diagnose. The latter is almost always better, but requires an interaction pattern where the expert asks the questions.

**Core structure:**
```
I want you to ask me questions to achieve X.
Ask one question at a time (or N questions at a time).
When you have enough information, [tell me / provide the output / etc.]
```

**Example:**
```
I want you to help me design a database schema for my application.
Ask me questions one at a time to gather everything you need to know.
When you've gathered enough information, generate the schema.
```

The LLM will ask: What entities need to be stored? What are the relationships between them? What access patterns will be most common? What scale are you expecting? — and build the schema based on your actual answers rather than assumptions.

**When to use it:** Any time the quality of the LLM's output depends heavily on information you have but haven't provided yet. System design, personalized recommendations, debugging sessions where context matters.

---

### Game Play

**What it does:** You establish a game with specific rules, and the LLM generates the content and manages the game flow indefinitely. The key insight is that you provide the rules (which are simple) and the LLM provides the content (which is complex). This inverts the usual workload.

Games created this way can be used for education, training, entertainment, or exploration. Because the LLM understands the topic deeply, it generates realistic and appropriate content for the game.

**Core structure:**
```
We are going to play a game about [topic].
[Describe the setup or scenario]
[Rules — each rule as a separate statement]
[How the game starts]
```

**Example:**
```
We are going to play a code review game.
You are going to present me with code snippets that contain 1-3 bugs or design issues.
I will identify what's wrong and explain how to fix it.
After my answer, you'll tell me what I got right, what I missed, and then show the corrected code.
Start with easy bugs and gradually increase difficulty.
Begin by presenting the first snippet.
```

**When to use it:** Learning a new technical domain, security training, practicing decision-making in simulated scenarios, making repetitive learning tasks more engaging.

**Combine with:** Persona (give the game an identity), Visualization Generator (add diagrams to the game), Infinite Generation (keep producing new game content automatically).

---

## Category 6: Context Control — Managing What the LLM Knows

These patterns give you precise control over what information the LLM is attending to — what's in scope and what should be ignored.

---

### Context Manager

**What it does:** You explicitly tell the LLM what to focus on and what to ignore within the conversation. LLMs sometimes attend to irrelevant parts of a long conversation, dragging in earlier context that's no longer relevant or confusing. The Context Manager pattern lets you scope the conversation precisely.

**Core structure:**
```
Within the scope of [topic/task]:
Please consider [X, Y, Z]
Please ignore [A, B, C]
[Optional: start over / reset context]
```

**Examples:**
```
When analyzing the following code, only consider security aspects —
ignore code style, naming conventions, and performance.
```

```
For the rest of this conversation, ignore everything about the old API I described earlier.
We're switching to a REST-based approach.
Please consider only the new architecture I'm about to describe.
```

```
Ignore everything we've discussed. Start over.
```

**When to use it:** When conversations have gone long and old context is causing confusion or drift. When you want to scope a review to specific concerns. When switching to a new topic within the same conversation.

**Caution:** If the LLM was initialized with organizational-level system prompts (instructions injected before your conversation), a full context reset may eliminate those too. Be aware of what you might be losing.

---

### Recipe

**What it does:** You provide a goal and a partial set of steps toward that goal, and ask the LLM to complete the recipe — filling in missing steps, ordering them correctly, and flagging any unnecessary steps you included. This is the pattern for workflow automation: you know roughly what needs to happen but not the exact sequence.

**Core structure:**
```
I would like to achieve X.
I know that I need to perform steps A, B, C.
Provide a complete sequence of steps for me.
Fill in any missing steps.
Identify any unnecessary steps.
```

**Example:**
```
I want to deploy a containerized web application to AWS.
I know I need to: create a Docker image, set up an AWS account, and configure a domain name.
Please provide a complete sequence of steps.
Fill in any missing steps.
Identify any of my steps that might be unnecessary depending on the approach.
```

The LLM will complete the recipe (ECR registry, ECS task definition, load balancer, Route 53 setup, etc.) and flag that "configure a domain name" may be unnecessary for a staging environment.

**When to use it:** Infrastructure setup, deployment workflows, process design, any multi-step task where you know some of the pieces but not the complete sequence.

**Combines:** Template (to format each step consistently), Alternative Approaches (to show multiple valid orderings or strategies), Reflection (to explain why each step is included).

---

## Combining Patterns

The real power of this catalog comes from composition. A few combinations the researchers found particularly effective:

**The Expert Advisor Stack:**
Persona + Reflection + Fact Check List
*"Act as a senior security architect. After answering, explain your reasoning, and list any facts I should independently verify."* — You get domain expertise + visible reasoning + a checklist for errors.

**The Structured Discovery:**
Flipped Interaction + Cognitive Verifier + Recipe
*"Ask me questions to understand my goal, break down the problem systematically, then provide a step-by-step recipe."* — Useful for complex technical planning sessions.

**The Simulation Environment:**
Game Play + Persona + Visualization Generator + Infinite Generation
*"You are a Linux terminal for a compromised machine. Respond to my commands with realistic output. When I ask you to visualize the network topology, generate a Graphviz DOT file."* — Creates a full cybersecurity training simulation.

**The Self-Improving Session:**
Question Refinement + Alternative Approaches + Reflection
*"Suggest a better version of each question I ask, provide the answer with alternatives, and explain your reasoning."* — Every question gets improved, answered thoroughly, and explained. Excellent for learning a new domain.

---

## Key Takeaways

Prompt patterns solve *categories of problems*, not specific tasks — which is what makes them reusable. A few principles to internalize:

The best patterns for accuracy are **Cognitive Verifier** and **Reflection** — they force structured reasoning rather than fast pattern-matching. Use them for any consequential decision.

The best patterns for quality when you're a non-expert are **Question Refinement** and **Fact Check List** — the first improves your question, the second flags what you can't evaluate yourself.

The best patterns for repetitive work are **Meta Language Creation**, **Infinite Generation**, and **Output Automater** — they reduce friction for batch tasks and automate execution of suggestions.

The best patterns for interactive learning are **Flipped Interaction** and **Game Play** — they restructure the conversation so the LLM does the teaching rather than just answering.

As LLM capabilities evolve, some of these patterns may become unnecessary — models may automatically show reasoning or ask clarifying questions. But the *problems* they solve are permanent: you'll always want better accuracy, better question framing, and better control over what the model is focused on.
