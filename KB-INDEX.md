# KB-INDEX — Concept Navigation Map

> Use this before reading any KB file. Find the concept → read only the relevant lines.
> Total KB: ~5,800 lines across 9 primary docs + 4 playbooks. Don't read whole files.

---

## prompt-engineering/prompt-engineering.md (518 lines)
| Lines | Section |
|---|---|
| 29–42 | What prompt engineering is |
| 43–86 | Output config: temperature, top-K, top-P, length |
| 87–102 | Zero-shot prompting |
| 103–133 | Few-shot / one-shot prompting |
| 134–162 | System, role, contextual prompting |
| 148–162 | Step-back prompting |
| 163–221 | Chain of Thought (CoT) — includes empirical results |
| 201–229 | Self-consistency |
| 222–256 | Tree of Thoughts (ToT) |
| 230–277 | ReAct (Reason + Act) |
| 257–280 | APE — Automatic Prompt Engineering |
| 278–368 | Advanced techniques: Auto-CoT, Reprompting, Chain of Draft, RaR, OPRO |
| 369–401 | Code prompting |
| 402–499 | Best practices |
| 500–518 | Anti-patterns |

## prompt-engineering/prompt-patterns.md (544 lines)
| Lines | Section |
|---|---|
| 7–28 | What patterns are, how to use the catalog |
| 35–65 | Meta Language Creation |
| 72–209 | Output customization: Output Automater, Persona, Visualization, Template, Infinite Generation |
| 216–272 | Error identification: Fact Check List, Reflection |
| 279–439 | Prompt improvement: Question Refinement, Alternative Approaches, Cognitive Verifier, Refusal Breaker |
| 384–439 | Interaction: Flipped Interaction, Game Play |
| 446–531 | Context control: Context Manager, Recipe |
| 510–544 | Combining patterns + key takeaways |

## context-engineering/context-engineering.md (446 lines)
| Lines | Section |
|---|---|
| 21–59 | Context window explained, prompt vs. context engineering |
| 60–131 | 8 context components (system prompt, user input, memory, RAG, tools, tool responses, state) |
| 132–204 | 4 strategies: Write / Select / Compress / Isolate |
| 205–289 | 4 failure modes: Poisoning / Distraction / Confusion / Clash |
| 290–406 | Custom formats, ordering, long-term memory, workflow engineering |
| 390–446 | Anti-patterns, tools, key takeaways |

## reasoning-llms/reasoning-llms.md (268 lines)
| Lines | Section |
|---|---|
| 19–67 | What reasoning models are, when to use vs. standard models |
| 68–130 | Design patterns: planning layer, LLM-as-judge, agentic RAG |
| 131–197 | Prompting rules: no manual CoT, thinking effort tiers |
| 198–256 | Limitations and failure modes |
| 257–268 | Decision workflow + key takeaways |

## skills/skills.md (543 lines)
| Lines | Section |
|---|---|
| 20–69 | What skills are, the re-explaining problem, core principles |
| 70–120 | Skills + MCP relationship, decision framework |
| 121–234 | Skill anatomy: YAML frontmatter (critical), instruction writing |
| 235–344 | 3 categories + 5 workflow patterns |
| 345–527 | Testing, iteration, distribution, troubleshooting |
| 527–543 | Anti-patterns |

## agentic-engineering/agentic-engineering.md (1,726 lines)
| Lines | Section |
|---|---|
| 9–62 | What an agent is, Four Pillars |
| 63–146 | Twelve Leverage Points framework |
| 147–343 | Prompt engineering for agents: 7-level maturity, 7-section structure |
| 344–506 | Model selection, behavior, multi-model architectures |
| 507–670 | Context management, degradation thresholds, advanced patterns |
| 671–841 | Tool design, selection, restrictions, scaling, MCP, tool lifecycle |
| 842–1269 | Patterns: Plan-Build-Review, Orchestrator, ReAct, HITL, Expert Swarm, Multi-Agent, Persistent Memory |
| 1270–1525 | Practices: debugging, cost, production, evaluation, intent engineering, spec engineering |
| 1526–1726 | Mental models: Pit of Success, Specs as Source Code, Topologies, Context as Code |

## ai-security/ai-security.md (461 lines)
| Lines | Section |
|---|---|
| 23–62 | Why AI security is different — paradigm shifts |
| 63–130 | Governance framework |
| 131–177 | OWASP LLM Top 10 (all 10 vulnerabilities) |
| 133–177 | Prompt injection (direct + indirect) + spotlighting defense |
| 178–288 | Privilege escalation, least privilege, Zero Trust |
| 224–327 | Identity management, credential vaults, MCP gateway |
| 329–395 | AI firewall/gateway pattern, sandboxing options |
| 396–461 | Monitoring, DevSecOps, emerging threats, anti-patterns |

## ai-system-design/ai-system-design.md (595 lines)
| Lines | Section |
|---|---|
| 23–92 | AI vs. deterministic decision framework |
| 93–237 | 11 architectural patterns (RAG, cascade, guardrails, caching, event-driven, multi-agent) |
| 238–339 | System design trade-offs: latency/cost/reliability/nondeterminism |
| 296–382 | Data architecture: databases, embedding pipelines, RAG at scale |
| 383–435 | Observability, metrics, tooling landscape |
| 436–517 | Scalability lessons from Uber/Netflix/Meta/Airbnb/LinkedIn |
| 518–573 | 12-Factor Agents standard |
| 438–573 | 8 anti-patterns |

## specification-clarity/specification-clarity.md (713 lines)
| Lines | Section |
|---|---|
| 22–81 | 7-property executable spec framework |
| 82–187 | Requirements engineering: Wiegers, IEEE 830, use cases |
| 131–187 | Acceptance criteria: Given/When/Then, INVEST, spec-driven evaluation |
| 191–277 | Constraint architecture — specifying what you don't want |
| 223–311 | Problem statement structure, CATWOE, Shape Up methodology |
| 313–428 | Decomposition: when to split tasks, granularity decisions |
| 354–428 | Failure mode catalog (8 failure modes incl. CMU findings) |
| 432–531 | 10 writing techniques for clearer specs |
| 533–685 | Decision frameworks, PRD structure, evaluation design |
| 653–713 | Anti-patterns |

## playbooks/ (4 files, ~500 lines total)
| File | When to Use | Key Sections |
|---|---|---|
| building-rag-pipelines.md | Building any RAG system | Chunking (L34), query understanding (L44), context injection (L53), hallucination prevention (L63), scaling (L121) |
| building-ai-agents.md | Building autonomous agents | ReAct (L23), tool design (L47), HITL (L69), scaling (L118) |
| building-chatbots.md | Building conversational AI | System prompt (L25), persona (L38), context across turns (L50), pitfalls (L118) |
| writing-production-prompts.md | Shipping prompts to prod | Zero-shot first (L23), output format (L46), APE (L89), documentation (L97) |

---

## Cross-Reference: Find a Concept Across Files

| Concept | Primary Location | Also In |
|---|---|---|
| RAG | ai-system-design.md L106, playbooks/building-rag-pipelines.md | context-engineering.md L96, agentic-engineering.md L113 |
| Prompt injection | ai-security.md L133 | agentic-engineering.md L736 |
| Context window management | context-engineering.md L21 | agentic-engineering.md L507 |
| Tool design | agentic-engineering.md L671 | playbooks/building-ai-agents.md L47 |
| Spaced repetition / eval | agentic-engineering.md L1393 | specification-clarity.md L590 |
| Multi-agent patterns | agentic-engineering.md L1083 | ai-system-design.md L226 |
| Cost optimization | agentic-engineering.md L1313 | ai-system-design.md L251 |
| Specification writing | specification-clarity.md | agentic-engineering.md L1470 |
| Chain of Thought | prompt-engineering.md L163 | agentic-engineering.md L147 |
| Memory (long-term) | context-engineering.md L88 | agentic-engineering.md L1153 |
| Security / Zero Trust | ai-security.md L198 | ai-system-design.md L508 |
| Model selection | agentic-engineering.md L344 | reasoning-llms.md L38 |
