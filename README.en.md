# Data Agent Radar

[中文](README.md) | **English**

This list tracks agents that perform end-to-end data work: understanding data, planning analyses, executing queries and code, transforming data, verifying results, recovering from errors, and delivering artifacts.

Related radars: [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) · [Agent Memory](https://github.com/H20Zhang/Agent-Memory-Radar) · [Agentic RAG](https://github.com/H20Zhang/Agentic-RAG-Radar) · **Data Agent**

[Latest](#latest) · [Field Map](#field-map) · [Reading Paths](#reading-paths) · [Library](#library)

Last updated: **2026-08-20**

<a id="latest"></a>
## Latest Research Signals

### [Polaris: Multi Agentic System for Conversational Enterprise Analytics](https://arxiv.org/abs/2608.14246)
`Planning & Orchestration` · **2026-08-14**

Polaris decomposes enterprise analytics across specialized querying, visualization, and reasoning agents, with Dynamic Task Coordination assigning work online. The causal question is whether multi-agent coordination still wins against a simpler single-agent + tool-routing control.

### [Business Truth, not SQL Accuracy: A Rule-Gated 7B Analytics Agent Outperforms a Direct-Prompted 32B Baseline](https://arxiv.org/abs/2608.09254)
`Verification & Reliability` · **2026-08-10**

The work separates “SQL executes” from “the business meaning is correct,” making clarification, abstention, schema drift, and deterministic post-execution checks part of analytics-agent correctness.

<details><summary><strong>The gap between SQL execution and Business Truth</strong></summary>

Production analytics failures often come from ambiguous business definitions, unanswerable warehouse questions, deprecated columns, or queries that execute successfully but return the wrong business number. QueryProof uses semantic-layer/catalog rules and deterministic post-execution checks before returning an answer.

The paper reports a higher Business Truth Rate than a direct-prompted larger-model baseline, but the systems are not scaffold-matched and no component ablation isolates the deterministic layer. The stronger research point is that **business-semantic correctness, clarification, abstention, and false-success rate are separate targets from execution match**.

</details>

### [CIPHER: A Decoupled Exploration-Selection Framework for Test-Time Scaling of Data Science Agents](https://arxiv.org/abs/2607.14386)
`Planning & Search` · **2026-07-15**

CIPHER avoids committing the entire data-science trajectory to one initial hypothesis: it generates multiple candidate initial states, selects among them, and executes several paths in parallel.

### [A Semantic-Layer-Mediated Agent for Natural Language to SQL over Heterogeneous Enterprise Databases](https://arxiv.org/abs/2606.31041)
`Semantic Grounding & Execution` · **2026-06-30**

The agent reasons over a curated semantic layer and emits a compact Semantic Model Query, while a deterministic compiler handles physical-schema and SQL-dialect execution.

<details><summary><strong>Why introduce a Semantic Model Query</strong></summary>

Direct NL→SQL over hundreds of physical tables asks the model to solve semantic grounding and dialect-specific execution at the same time. This design inserts a semantic intermediate representation so the model composes verified business concepts while deterministic code handles SQL realization.

That improves grounding but moves a large part of system quality into the semantic layer. The decisive comparison is therefore not “semantic layer vs raw schema” in the abstract; it is how much curation cost and coverage are required, and how the system behaves when the semantic layer is incomplete or wrong.

</details>

### [APEX-SQL: Talking to the data via Agentic Exploration for Text-to-SQL](https://arxiv.org/abs/2602.16720)
`Data Discovery & Grounding` · **2026-02-11**

Schema linking becomes hypothesis → data profiling → verification: the agent actively inspects real values/distributions to validate column and join assumptions before generating SQL.

### [AgentSM: Semantic Memory for Agentic Text-to-SQL](https://arxiv.org/abs/2601.15709)
`Learning & Reuse` · **2026-01-22**

Prior execution traces become interpretable semantic programs that persist as database-specific memory, allowing future queries to reuse reasoning paths rather than rediscover them from scratch.

<a id="changes"></a>
## Research Shifts

| Shift | Evidence | Research implication |
|---|---|---|
| **Semantic grounding is moving upstream of code generation.** | APEX-SQL actively profiles data; semantic-layer agents reason over business concepts before physical SQL. | Evaluate whether better grounding pays for exploration/curation cost, not only execution accuracy. |
| **Verification is becoming a first-class stage.** | QueryProof-style designs distinguish business truth, clarification, abstention, and post-execution checks from “query executed.” | A Data Agent needs a contract for when not to return a number. |
| **Data work is becoming a long-horizon control problem.** | CIPHER explores multiple initial states; Polaris coordinates specialized agents; AgentSM reuses prior execution knowledge. | Planning, intermediate state, recovery, and reusable experience should be measured separately from final artifacts. |

<a id="field-map"></a>
## Field Map

`intent → discover/ground → plan → execute/transform → inspect/verify → recover → learn/reuse → deliver`

| Research problem | Core question | Current tension |
|---|---|---|
| **Data Discovery & Grounding** | How does the agent find the right schema, table, file, document, metric, and business definition? | `static metadata ↔ active profiling` |
| **Planning & Semantic Interaction** | How should user intent become an executable, inspectable analytic plan? | `direct NL→SQL/code ↔ semantic/intermediate plan` |
| **Execution & Transformation** | How should SQL, Python, notebooks, DB/API tools, and real-computer actions compose? | `single-shot generation ↔ grounded multi-tool execution` |
| **Verification & Recovery** | When can a successful execution still be wrong, and how should the agent recover? | `execution success ↔ business truth / artifact verification` |
| **Learning & Reuse** | Which prior analyses, workflows, skills, and memories should persist? | `restart from scratch ↔ reusable experience` |

[Evaluation view →](https://github.com/H20Zhang/Agent-Benchmark-Radar#data-agents)

<a id="reading-paths"></a>
## Reading Paths

| Question | Suggested path | What to learn |
|---|---|---|
| **How should an agent ground itself in an enterprise database?** | APEX-SQL → Semantic-Layer-Mediated Agent → AgentSM | Active profiling, semantic abstraction, and reusable database-specific knowledge solve different parts of grounding. |
| **How should data work become reliable rather than merely executable?** | QueryProof / Business Truth → DataSpace / DSAgentBench in Benchmark Radar | Business semantics, clarification/abstention, artifact verification, and real-computer execution expand the success contract. |
| **When does more agentic planning help?** | CIPHER → Polaris | Test-time search over plans and multi-agent orchestration add control capacity, but need simpler matched controls to isolate value. |

<a id="library"></a>
## Research Library

- [Browse by problem / research line / year](library/README.en.md)
- [Data Agent evaluation genealogy](https://github.com/H20Zhang/Agent-Benchmark-Radar)

## Scope and ownership

High-priority work should change a meaningful control boundary in real data work: data discovery/grounding, semantic planning, multi-tool execution, verification/recovery, workflow learning/reuse, or enterprise analytics orchestration.

Plain Text-to-SQL leaderboard papers without a substantive agent-control, data-interaction, or verification contribution are usually not high priority.

This repo covers methods, systems, and research tensions. Benchmark genealogy, protocol validity, and evaluation gaps live in [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) so the family does not maintain two competing benchmark maps.
