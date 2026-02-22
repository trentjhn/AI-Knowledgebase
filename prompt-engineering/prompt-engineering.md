# Prompt Engineering

**Table of Contents**
1. [What Prompt Engineering Is](#1-what-prompt-engineering-is)
2. [LLM Output Configuration — The Dials You Control](#2-llm-output-configuration--the-dials-you-control)
3. [Prompting Techniques](#3-prompting-techniques)
   - [Zero-Shot](#zero-shot)
   - [One-Shot and Few-Shot](#one-shot-and-few-shot)
   - [System, Role, and Contextual Prompting](#system-role-and-contextual-prompting)
   - [Step-Back Prompting](#step-back-prompting)
   - [Chain of Thought (CoT)](#chain-of-thought-cot)
   - [Self-Consistency](#self-consistency)
   - [Tree of Thoughts (ToT)](#tree-of-thoughts-tot)
   - [ReAct (Reason + Act)](#react-reason--act)
   - [Automatic Prompt Engineering (APE)](#automatic-prompt-engineering-ape)
4. [Code Prompting](#4-code-prompting)
5. [Best Practices](#5-best-practices)
6. [Documentation — The Practice Most People Skip](#6-documentation--the-practice-most-people-skip)
7. [Anti-Patterns](#7-anti-patterns)

---

## 1. What Prompt Engineering Is

A large language model is, at its core, a prediction engine. It takes text as input and predicts — token by token — what the most likely next word should be, based on patterns in the enormous amount of text it was trained on. Every word it generates becomes the new end of the sequence, and then it predicts the next word again, and so on.

When you write a prompt, you are setting up that prediction engine to head in a particular direction. A well-crafted prompt is like pointing a very powerful engine down a specific road. A poorly crafted prompt is like starting the engine and hoping it finds the right destination on its own.

**Prompt engineering** is the discipline of designing those prompts — iteratively, deliberately, and systematically — to get the outputs you actually want. It's not programming in the traditional sense; you're not writing logic. You're writing *inputs that steer probabilistic prediction*. That distinction matters because the same instruction phrased three different ways can yield meaningfully different results.

Anyone can write a prompt. The skill is in writing prompts that reliably produce good outputs, across different inputs, on the first or second try rather than the fifteenth.

The quality of your prompt depends on: the model you choose, the model's training data, the configuration settings (temperature, sampling), your word choice, tone, structure, and how much context you provide. Prompting is inherently iterative — you try, observe, adjust, and repeat.

---

## 2. LLM Output Configuration — The Dials You Control

Before writing a single word of prompt text, it helps to understand the configuration settings that shape how the model generates its response. These aren't minor tweaks — they fundamentally change what kind of output the model produces.

### Output Length

Every response has a token limit — the maximum number of tokens the model will generate. Setting this limit is important: more tokens mean more computation, higher cost, and slower responses. But a limit that's too tight will cut off the answer mid-thought.

Crucially, restricting the output length does *not* make the model more concise in its thinking — it just makes it stop writing sooner. If you want genuinely short output, you need to both set a low token limit *and* ask for brevity in the prompt itself.

### Temperature — How Creative vs. How Predictable

Temperature is the most widely discussed setting, and for good reason. It controls how "random" the model's word choices are.

Think of it this way: when the model is deciding what word comes next, it has a probability distribution across thousands of possible words. Temperature controls how peaked or flat that distribution becomes before sampling from it.

- **Low temperature (0–0.3)**: The distribution is very peaked. The highest-probability word dominates, so the model almost always picks the "safest" most predictable option. Good for factual tasks, classification, math, and anywhere there's a single right answer.
- **High temperature (0.7–1.0+)**: The distribution flattens. Lower-probability words become plausible options, so the model can surprise you — for better or worse. Good for creative writing, brainstorming, generating variety.
- **Temperature = 0**: Fully deterministic (greedy decoding) — always picks the single highest-probability token. Use this for CoT reasoning and tasks with one correct answer.

**The repetition loop bug**: At both extremes, temperature can cause the model to get stuck repeating the same words or phrase endlessly. At low temperature, the deterministic path loops back on itself. At high temperature, random chance eventually lands on words that lead back to the same place. The fix is usually careful tuning of temperature together with top-K and top-P.

**Good starting points:**
- Balanced creative/coherent: temperature 0.2, top-P 0.95, top-K 30
- Highly creative: temperature 0.9, top-P 0.99, top-K 40
- Conservative/factual: temperature 0.1, top-P 0.9, top-K 20
- Single correct answer: temperature 0

### Top-K and Top-P — Narrowing the Candidate Pool

While temperature reshapes the entire probability distribution, top-K and top-P add a filter *before* sampling occurs — they restrict which words are even eligible to be selected.

**Top-K** keeps only the K most probable next tokens. Setting K to 1 is equivalent to temperature 0 (always pick the top word). Setting K to the full vocabulary size effectively disables the filter.

**Top-P** (also called nucleus sampling) keeps tokens until their cumulative probability reaches the threshold P. If P is 0.9, the model picks from whichever tokens collectively account for 90% of the probability mass. This adapts automatically — if one word dominates, only that word might be included; if the distribution is spread out, more words are included.

**How they interact with temperature:** When all three are active, tokens must pass both the top-K and top-P filters *before* temperature is applied to sample among the survivors. At extreme settings, they cancel each other out — temperature 0 makes top-K and top-P irrelevant; top-K of 1 makes everything else irrelevant.

The key practical lesson: **experiment with settings together**, not in isolation. Changing one affects how the others behave.

---

## 3. Prompting Techniques

### Zero-Shot

The simplest possible prompt — no examples, just a task description. You're relying entirely on the model's general knowledge and training.

```
Classify movie reviews as POSITIVE, NEUTRAL, or NEGATIVE.

Review: "Her" is a disturbing study revealing the direction humanity is
headed if AI is allowed to keep evolving, unchecked. I wish there were
more movies like this masterpiece.

Sentiment:
```

Zero-shot works when the task is common enough that the model has seen many examples in training. It fails when the task is unusual, requires specific format conventions, or has edge cases the model can't anticipate on its own. When zero-shot fails, reach for few-shot.

### One-Shot and Few-Shot

You give the model one (one-shot) or several (few-shot) examples of the desired input-output pattern. The model then follows that pattern for the new input.

This works because of something remarkable in how LLMs are trained: they can recognize and generalize from patterns shown *within the prompt itself*, without any retraining. The examples act as a live teaching signal.

**Why it matters:** Even one good example can dramatically improve output format and quality. Multiple examples increase the chance the model learns the actual pattern rather than overfitting to surface features of a single example.

**How many examples?** Three to five is a good starting rule. Use more for complex tasks; you may need fewer if the model is very capable and the task is clear.

**Practical tips for few-shot:**
- Use examples that cover the range of variation you expect in real inputs
- Include edge cases if they're likely
- For classification tasks, mix up the classes across examples — don't put all the "positive" examples first, or the model may latch onto order rather than meaning
- Start with six examples and dial back if the context gets too long

```
Parse pizza orders into JSON:

EXAMPLE:
"I want a small pizza with cheese and pepperoni."
{"size": "small", "ingredients": ["cheese", "pepperoni"]}

EXAMPLE:
"Large pizza, tomato sauce and mozzarella please."
{"size": "large", "ingredients": ["tomato sauce", "mozzarella"]}

Now parse: "I'd like a large pizza, first half cheese and mozzarella,
other half ham and pineapple."
```

### System, Role, and Contextual Prompting

These three techniques all shape *how the model approaches a task*, but each from a different angle.

**System prompting** defines the overall task and output format. It's the "big picture" instruction — telling the model what it is fundamentally supposed to do. It's especially useful for enforcing output structure (return JSON, use only one word, be concise) and for safety/tone guidelines ("always be respectful in your answers").

**Role prompting** assigns a persona or identity to the model. This shapes the tone, vocabulary, level of detail, and perspective. "You are a kindergarten teacher" produces different explanations than "you are a PhD researcher." The role provides an implicit style guide. You can layer personality on top: "Act as a travel guide, but with a humorous tone."

Available styles worth experimenting with: Confrontational, Descriptive, Direct, Formal, Humorous, Influential, Informal, Inspirational, Persuasive.

**Contextual prompting** provides specific background information for the current task. Unlike a system prompt (which is relatively stable), context is dynamic — it changes per request. "You are writing for a blog about retro 80s arcade games" tells the model what to assume about the audience and subject matter without having to spell out every constraint explicitly.

These three overlap significantly in practice. A single prompt can include all three layers: a system instruction, a role assignment, and specific context for the current task. The value of keeping them conceptually distinct is that it gives you a framework for diagnosing when something goes wrong — was it the system setup, the role framing, or the missing context?

### Step-Back Prompting

Step-back prompting is a two-stage technique that activates broader knowledge before tackling a specific task.

The problem it solves: when you ask a model a narrow, specific question, it tends to pattern-match to similar specific questions in its training data. This can produce generic or templated answers. But if you first ask a more general question — one step removed from the specific task — the model activates richer background knowledge, which then improves the specific answer.

**The workflow:**
1. Identify the general principle behind your specific task
2. Ask the model about the general principle first
3. Feed the model's answer back in as context for the specific task

**Example:** Instead of directly asking "Write a storyline for a first-person shooter level," first ask "What are the five most engaging settings in first-person shooter games?" Then feed those settings back in as context: "Using these settings, write a storyline for one level."

The result is more specific, more grounded, and more creatively rich than if you'd asked directly. Step-back prompting is particularly useful for creative tasks, domain-specific problems, and any case where the model's default response feels generic or shallow.

### Chain of Thought (CoT)

LLMs are surprisingly bad at math. Ask a model a simple age-difference problem with no guidance, and it often gives the wrong answer. Ask it to "think step by step," and it suddenly gets it right. This is the core insight behind Chain of Thought prompting.

CoT prompting instructs the model to generate *intermediate reasoning steps* before arriving at a final answer. By making the model articulate its reasoning, you force it to slow down, catch errors, and build conclusions from a logical chain rather than pattern-matching directly to a guess.

```
# Without CoT:
When I was 3, my partner was 3 times my age. I'm now 20. How old is my partner?
→ Output: 63 (wrong)

# With CoT:
...How old is my partner? Let's think step by step.
→ Output: When I was 3, partner was 9. Difference is 6. Now I'm 20, so partner is 26. ✓
```

**Why this works:** The intermediate steps become part of the input for predicting the next token. When the model writes "the difference is 6," that fact is now *in the context* when it predicts the final answer. It's not magic — it's the model being forced to construct its own scaffolding.

**Advantages of CoT:**
- Low effort, high effectiveness — just add "Let's think step by step" or show an example with reasoning
- Works out of the box with any capable LLM without fine-tuning
- Makes the reasoning visible and debuggable — you can see where the logic went wrong
- More robust across different model versions — reasoning chains drift less than direct prompts when you upgrade models

**Disadvantage:** More output tokens = higher cost and latency. The reasoning appears in the response, which means you're paying for it.

**Zero-shot CoT** uses just the phrase "Let's think step by step." **Few-shot CoT** shows one or more complete examples including the reasoning chain — this is more powerful for complex tasks.

**Critical best practice:** For CoT, always set temperature to 0. You're looking for the single correct reasoning path, not creative variation.

### Self-Consistency

Self-consistency extends CoT by running the same prompt multiple times (with a higher temperature to generate variety) and then selecting the most commonly occurring final answer.

The intuition: if you ask ten people to independently work through a hard problem and eight of them arrive at the same answer, that answer is probably right. Self-consistency applies this voting logic to LLM responses.

**The process:**
1. Send the same CoT prompt multiple times with high temperature (so each run explores a different reasoning path)
2. Extract the final answer from each response
3. Select the most frequently occurring answer

This is expensive — you're paying for multiple completions — but it provides a pseudo-probability measure of how confident the model is. If 9 out of 10 runs agree, that's meaningful signal. If it's 5/10, you know the question is genuinely ambiguous or the prompt needs work.

Self-consistency is most valuable when a single wrong reasoning path could lead to confidently wrong answers — it catches those cases by making them statistically rare.

### Tree of Thoughts (ToT)

Where CoT follows a single reasoning chain (linear) and self-consistency runs multiple parallel chains independently, Tree of Thoughts lets the model explore a branching tree of reasoning paths — considering multiple approaches at each decision point and evaluating which branches are most promising.

Imagine solving a complex puzzle. CoT says "here's my one attempt." Self-consistency says "here are ten independent attempts." Tree of Thoughts says "let me explore three approaches, evaluate each, pick the most promising one to develop further, explore branches from there, and prune the ones that aren't working."

ToT is the most powerful of the three for tasks that require genuine exploration — puzzle solving, multi-step planning, creative problem-solving. It's also the most computationally expensive and requires more sophisticated implementation than just modifying a text prompt.

### ReAct (Reason + Act)

All the techniques above operate purely in language — the model thinks and generates text. ReAct is the bridge to the real world: it combines reasoning with action, allowing the model to use external tools (search engines, calculators, APIs, databases) mid-response.

ReAct mimics how humans actually solve hard problems. We don't just think — we look things up, check our work, gather data, then think again based on what we found.

**The thought-action loop:**
1. Model reasons about the problem and decides what action to take
2. Action is executed (e.g., a web search)
3. Observation (the result) is fed back in
4. Model reasons again based on what it learned
5. Repeat until a final answer is reached

**Example — "How many children do Metallica's band members have?"**
```
Thought: Metallica has 4 members. I need to look up each one.
Action: Search "How many kids does James Hetfield have?"
Observation: Three children
Thought: 1/4 members = 3 children total so far
Action: Search "How many kids does Lars Ulrich have?"
Observation: 3
...
Final Answer: 10
```

ReAct is the foundation for tool-using agents. It's what makes the difference between a model that knows things and a model that can *find out* things dynamically. When combined with skill prompts and MCP servers (see the Skills knowledge base doc), ReAct-style reasoning is how agents orchestrate complex multi-step workflows.

### Automatic Prompt Engineering (APE)

At a certain point, you might wonder: can you prompt the model to write better prompts? Yes — this is Automatic Prompt Engineering.

**The workflow:**
1. Write a meta-prompt asking the model to generate N variants of a prompt for your task
2. Evaluate each variant against a quality metric (accuracy, BLEU score, human rating)
3. Select the best-scoring variant; optionally tweak it and evaluate again
4. Repeat

APE is especially useful when you need to cover the full range of ways users might phrase a request (for chatbot training), or when you want to avoid the bias of your own prompt-writing instincts. Different people write prompts differently, and APE surfaces that variance systematically.

The limitation: APE is only as good as your evaluation metric. If you can't clearly measure what "better" means for your task, it's hard to know which generated prompt actually wins.

---

## 4. Code Prompting

LLMs trained on large amounts of code are remarkably effective at generating, explaining, translating, and debugging code. The same prompting principles apply, but with a few specific patterns worth knowing.

### Writing Code

Be specific about the language, the exact task, and any constraints. Vague prompts produce vague code.

```
Write a Bash script that asks for a folder name, checks if it exists,
then prepends "draft_" to every filename inside it.
```

**Always read and test the output.** LLMs reproduce patterns from training data; they don't reason about execution. They can produce code that looks correct but has subtle bugs. Think of them as a very fast first draft, not a trusted engineer.

### Explaining Code

Drop in unfamiliar code and ask the model to walk through what each part does. This is faster than reading documentation, especially for languages you don't use daily. Works well for understanding someone else's code or revisiting your own code after time away.

### Translating Code

LLMs can translate between programming languages with surprising fidelity — Bash to Python, JavaScript to TypeScript, SQL dialects. The prompt is simply: "Translate this [language A] code to [language B]" followed by the code block.

Review the output carefully. The model may use idioms from one language that don't map cleanly to the other, or miss library equivalents.

### Debugging and Reviewing Code

Paste the broken code and the error message together. Ask the model to explain what's wrong and how to fix it. LLMs are particularly good at this because they've seen thousands of variations of common bugs — they often recognize the pattern instantly.

Beyond fixing the immediate error, ask for a general code review: "Are there other issues with this code?" You'll often get suggestions for robustness, error handling, and readability improvements beyond the original bug.

---

## 5. Best Practices

### Provide Examples — The Single Most Effective Technique

If you do nothing else, add examples. One-shot or few-shot examples are the most reliable way to improve output quality, format, and accuracy. They act as live teaching — the model sees exactly what good output looks like and imitates it.

### Design with Simplicity

If a prompt is confusing to you, it's confusing to the model. Plain language outperforms complex language. Remove anything that isn't essential.

Before: "I am visiting New York right now, and I'd like to hear more about great locations. I am with two 3 year old kids. Where should we go during our vacation?"

After: "Act as a travel guide. Suggest great places to visit in New York Manhattan with a 3-year-old child."

Use action verbs to be precise: Act, Analyze, Categorize, Classify, Compare, Create, Describe, Evaluate, Extract, Generate, Identify, List, Parse, Rank, Recommend, Summarize, Translate, Write.

### Be Specific About the Output

Vague prompts produce vague outputs. Specify the format, length, tone, and structure you want.

- "Write a blog post about consoles" → too open
- "Write a 3-paragraph blog post about the top 5 video game consoles, in a conversational style, for a general audience" → clear

### Use Instructions Over Constraints

Tell the model what *to do*, not what *not to do*. Instructions communicate desired outcomes directly; constraints leave the model guessing about what's still allowed. A list of constraints can also conflict with each other.

- Constraint: "Don't mention specific game titles."
- Instruction: "Discuss only the console hardware, the company, the release year, and total sales."

The instruction is clearer, more actionable, and less likely to produce unexpected edge-case behavior. Use constraints only when you genuinely need to prevent specific harmful or off-topic content.

### Use Variables in Prompts

When you'll reuse a prompt template with different inputs, use placeholders:

```
You are a travel guide. Tell me one interesting fact about the city: {city}
```

Variables make prompts maintainable, reusable in applications, and easier to test systematically across different inputs.

### Control Length in the Prompt, Not Just the Config

Setting a max token limit tells the model when to stop — it doesn't make responses more concise. If you want a short response, say so: "Explain quantum physics in one sentence." or "Summarize this in 50 words."

### Experiment with Output Formats

For non-creative tasks — extraction, classification, parsing, summarization of structured data — requesting JSON output has meaningful advantages:

- Always returns in the same shape, making it easy to parse programmatically
- Forces the model to think in terms of structure, which reduces hallucinations
- Makes relationships between pieces of data explicit
- Enables sorting, filtering, and downstream use without reformatting

Provide a schema alongside the request for best results. The schema acts as a blueprint that keeps the model's output disciplined.

**JSON repair:** If the model hits the token limit mid-JSON, the output will be malformed. The `json-repair` Python library can automatically fix truncated JSON — useful in production pipelines.

### For CoT: Always Temperature 0

Chain of thought reasoning should be deterministic. You want the most probable reasoning chain, not creative variation. Set temperature to 0 for any CoT prompt.

Also: put the answer *after* the reasoning. The generation of the reasoning changes the token context that the model uses to predict the final answer. Reversing the order defeats the purpose.

### Experiment Together

Prompt engineering is partly subjective — what works best varies by model, task, and context. If you're working in a team, have multiple people write independent prompts for the same task and compare results. Different instincts surface different approaches; the best prompt often emerges from combining elements from several attempts.

---

## 6. Documentation — The Practice Most People Skip

Prompt outputs vary across models, across sampling settings, and even across identical prompts to the same model (when token probabilities are tied, tie-breaking is random). Without documentation, you lose track of what you tried, can't reproduce good results, and can't understand why a previously working prompt broke after a model update.

The recommended format for tracking every prompt attempt:

| Field | What to Record |
|---|---|
| Name & version | A unique identifier for this attempt |
| Goal | One sentence on what this prompt is trying to achieve |
| Model | Name and version |
| Temperature | Exact value |
| Token limit | Exact value |
| Top-K | Value or N/A |
| Top-P | Value or N/A |
| Full prompt | The entire prompt text, exactly as sent |
| Output | The actual output(s) received |
| Result | OK / NOT OK / SOMETIMES OK |
| Notes | What worked, what didn't, what to try next |

**Additional tips:**
- Save prompts in separate files from application code — they're maintained on a different cadence than logic
- When working with RAG systems (retrieval-augmented generation — where you inject retrieved documents into the prompt), also record the query, chunk settings, and what content was actually injected
- Once a prompt is production-ready, add it to automated evaluation pipelines so you catch regressions when models update

---

## 7. Anti-Patterns

**Assuming the first prompt is the final prompt.** Prompt engineering is explicitly iterative. Expecting a correct output from the first attempt is like expecting compiled code to work without testing. Budget for multiple rounds.

**Vague output specifications.** "Write something about AI" is not a prompt — it's a topic. Always specify length, format, tone, and what you actually want the output to do.

**Using constraints instead of instructions.** "Don't be too long" is harder for a model to act on than "Write exactly two paragraphs." Positive instructions are consistently more effective than negative constraints.

**Skipping examples because they take time.** The time spent writing two or three good examples is almost always recovered in reduced iteration time and better output quality.

**Ignoring temperature for the task type.** Using high temperature for math or classification tasks, or low temperature for creative brainstorming, often produces exactly the wrong result. Match the setting to the task.

**Not reading code outputs before running them.** LLMs produce plausible-looking code that can have real bugs. Always review before executing, especially for scripts that touch files, networks, or databases.

**Not documenting prompt iterations.** You will revisit your prompts. Models update, tasks evolve, edge cases surface. The documentation you skip now will cost you much more time later when you're trying to reconstruct what you did and why.

---

*Source: Lee Boonstra, "Prompt Engineering" (Google / Vertex AI whitepaper, February 2025)*
