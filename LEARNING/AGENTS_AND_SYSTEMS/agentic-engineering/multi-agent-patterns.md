# Multi-Agent Patterns (Sequential, Parallel, Loop)

This document explores fundamental architectural patterns for designing and implementing multi-agent systems, often facilitated by Agent Development Kits (ADKs) or robust agent frameworks. These patterns define how individual agents collaborate and exchange information to achieve complex goals, moving beyond monolithic agent designs.

These patterns integrate deeply with concepts like the Model Context Protocol (MCP) for tool use and the broader principles of Agentic Engineering for system design.

## 1. Sequential Agent Pattern

In a sequential pattern, agents execute tasks one after another in a predefined order. The output of one agent typically serves as the input for the subsequent agent, forming a pipeline or a chain of operations. This pattern is ideal for tasks that require a step-by-step approach or where dependencies between tasks are linear.

### Characteristics:
- **Linear Flow:** Tasks proceed in a strict order.
- **Dependency:** Each agent's operation is dependent on the successful completion and output of the previous agent.
- **Clarity:** Easy to understand and debug due to its predictable flow.
- **Use Cases:** Data processing pipelines, multi-stage problem-solving, structured report generation.

### Example Workflow:
A classic example involves a "Research & Reporting" workflow:
1.  **Planning Agent:** Receives a user query and generates a detailed plan.
2.  **Research Agent:** Takes the plan, executes research (e.g., using MCP-enabled search tools), and summarizes findings.
3.  **Report Agent:** Receives the research summary and compiles a final report.

### Code Example Reference:
See `sequential_agents.py` for a basic Python implementation demonstrating this pattern.

## 2. Parallel Agent Pattern

The parallel pattern allows multiple agents to execute tasks concurrently and often independently. This pattern is particularly useful for speeding up workflows by distributing workload or by having different agents work on distinct sub-problems simultaneously. The results from these parallel executions are typically aggregated or merged at a later stage.

### Characteristics:
- **Concurrency:** Multiple tasks run at the same time.
- **Independence:** Agents often operate with minimal or no direct dependency on each other during their execution phase.
- **Efficiency:** Significantly reduces overall execution time for decomposable tasks.
- **Use Cases:** Distributed data collection, concurrent analysis of different data streams, fan-out/fan-in processing.

### Example Workflow:
A "Multi-Source Data Analysis" workflow:
1.  **Orchestrator/Fan-out:** Receives a request to analyze a broad topic.
2.  **Data Collection Agent (Source A):** Collects data from one source (e.g., database via MCP).
3.  **Data Collection Agent (Source B):** Concurrently collects data from another source (e.g., external API via MCP).
4.  **Analysis Agent (for A):** Analyzes data from Source A.
5.  **Analysis Agent (for B):** Concurrently analyzes data from Source B.
6.  **Merger/Fan-in:** Aggregates and synthesizes the analysis results from both sources.

### Code Example Reference:
See `parallel_agents.py` for a basic Python implementation demonstrating this pattern using `concurrent.futures`.

## 3. Loop Agent Pattern

A loop agent pattern involves an agent or a group of agents repeatedly performing actions or interactions until a specific termination condition is met, or a maximum iteration count is reached. This pattern is essential for iterative refinement, optimization, monitoring, or goal-seeking behaviors.

### Characteristics:
- **Iteration:** Repeated execution of a set of actions.
- **Condition-Driven:** Execution continues as long as a specified condition is false (or true), or for a fixed number of iterations.
- **Adaptation:** Agents can adapt their behavior based on intermediate results within the loop.
- **Use Cases:** Optimization algorithms, continuous monitoring, iterative problem-solving (e.g., refining an answer until confidence thresholds are met), energy accumulation.

### Example Workflow:
An "Iterative Optimization" workflow:
1.  **Optimizer Agent:** Starts with an initial state or value.
2.  **Adjustment Agent:** Proposes an adjustment based on the current state.
3.  **Application Agent:** Applies the adjustment to update the state.
4.  **Check Agent:** Evaluates the new state against a termination condition (e.g., "is target value reached within tolerance?"). If not, the loop continues.

### Code Example Reference:
See `loop_agent.py` for a basic Python implementation demonstrating this pattern.

## Integration with MCP and Agentic Engineering

These multi-agent patterns are profoundly enhanced by MCP. Agents within these workflows can leverage MCP servers to access tools (e.g., for research, data collection, or executing actions) and resources (e.g., configuration, memory). MCP provides the standardized, decoupled interface, allowing agents to focus on their core logic while relying on robust, externalized tool execution.

**Cross-referencing:**
- **Model Context Protocol (MCP):** For understanding how agents access external capabilities (tools, resources, prompts). See `mcp.md`.
- **Agentic Engineering:** For broader principles of agent design, context management, and complex system architectures. See `agentic-engineering.md`.

## Further Research Considerations:
- **Orchestration Strategies:** How a "Summoner" or orchestrator agent intelligently selects and routes requests to specific sequential, parallel, or loop workflows.
- **Error Handling and Resilience:** Implementing robust error detection, fallback mechanisms, and graceful degradation across these multi-agent patterns.
- **Dynamic Workflow Generation:** How LLMs can dynamically construct or adapt these patterns based on complex user requests or environmental changes.
