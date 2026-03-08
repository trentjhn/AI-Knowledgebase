# AGENTS & SYSTEMS — Building with AI (Mid-Level)

How to architect and build AI agents and systems. Prerequisites: Complete [FOUNDATIONS/](../FOUNDATIONS/) first.

---

## Topics

### [**Agentic Engineering**](agentic-engineering/)
**2,000+ lines** — The most comprehensive reference on building AI agents

- Core Four Pillars of agentic systems
- Twelve Leverage Points framework for agent design
- 7-level prompt maturity model for agents
- Model selection and multi-model architectures
- Context management for agents, degradation strategies
- Tool design, restrictions, scaling, MCP integration
- 6 major patterns: Plan-Build-Review, Orchestrator, ReAct, HITL, Expert Swarm, Multi-Agent
- Practices: debugging, cost optimization, production deployment, evaluation
- Mental models: Pit of Success, Specs as Source Code, Context as Code
- Agent orchestration patterns and abstraction tiers

**Start with:** Four Pillars, then Twelve Leverage Points

---

### [**AI System Design**](ai-system-design/)
**1,200+ lines** — Architecture patterns for production AI systems at scale

- 11 core design patterns (agents, RAG, classification, content generation, etc.)
- Data pipelines: ingestion, processing, retrieval, monitoring
- Observability: logging, tracing, alerting, metrics
- Scalability: caching, batching, parallel processing
- Trade-offs: cost vs. quality, latency vs. accuracy, consistency vs. availability
- Lessons from Uber, Netflix, Meta on building at scale

**Start with:** Core design patterns, then trade-offs section

---

### [**Skills**](skills/)
**850+ lines** — Building reusable Agent Skills for consistent behavior

- What skills are and why they solve the "re-explaining problem"
- YAML frontmatter (CRITICAL for skill design)
- 3 skill categories: document creation, workflow automation, MCP enhancement
- 5 workflow patterns for skill design
- Testing: trigger-based, functional, performance
- Distribution, versioning, troubleshooting
- Instincts v2: continuous learning via micro-skills with confidence scoring

**Start with:** "What are skills?" and YAML frontmatter sections

---

## Learning Path

1. **Start:** [FOUNDATIONS/](../FOUNDATIONS/) (prerequisite)
2. **Then:** Agentic Engineering (understand agent architecture)
3. **Parallel:** AI System Design (understand larger system design)
4. **Then:** Skills (learn how to make agent behavior reusable)
5. **Next:** Move to [PRODUCTION/](../PRODUCTION/) for quality, security, and optimization

---

## How These Connect

**Agentic Engineering** teaches you how to build a single agent well.
**AI System Design** teaches you how to build systems of multiple agents/components.
**Skills** teaches you how to make agent behavior reusable and consistent across projects.

Read them in order, but they reinforce each other.

---

## Quick Reference

| Topic | Best For | Read Time |
|-------|----------|-----------|
| Agentic Engineering | Building agents, prompting, model choice | 4-6 hours |
| AI System Design | System architecture, scalability, trade-offs | 3-4 hours |
| Skills | Reusable agent knowledge, testing skills | 2-3 hours |

---

**Next step:** Once you understand building, move to [PRODUCTION/](../PRODUCTION/) to learn how to ship reliable, secure, well-evaluated systems.

Last updated: 2026-03-08
