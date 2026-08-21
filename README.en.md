# Data Agent Radar

[中文](README.md) | **English**

*A living research map of agents that perform end-to-end data work: understanding data, planning analyses, executing queries and code, transforming data, verifying results, recovering from errors, and delivering artifacts.*

**Research Radar family:** [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) · [Agent Memory](https://github.com/H20Zhang/Agent-Memory-Radar) · [Agentic RAG](https://github.com/H20Zhang/Agentic-RAG-Radar) · **Data Agent**

[30 sec: Timeline](#timeline) · [3 min: 7/30-day changes](#periods) · [5 min: Field Map](#field-map) · [15 min: Reading Paths](#reading-paths) · [Browse all](#library)

> **Beginner mental model.** `intent → discover/ground data → plan → query/code/transform → inspect/verify → revise/recover → learn/reuse → deliver`
>
> **Current thesis.** A Data Agent is not merely an SQL generator. The difficult systems problem is connecting **business semantics, heterogeneous data, tool execution, intermediate state, verification, and recovery** into a reliable loop.

Last updated: **2026-08-21**

<a id="timeline"></a><a id="latest"></a>
## Latest Timeline

> **Time note.** Native-v2 records are ordered by full `radar_published_at`. The six older records that follow have no reliable first-discovery or first-publication times; their source dates remain contextual and are not Radar acceptance chronology. Open any row for the question, evidence, caveat, map judgment, and deep-reading links.

<a id="entry-2608-17007"></a>
<details><summary>2026-08-21 · SkillEffect · Execution & Transformation <!-- timefirst:area=execution-transformation --> — Check bounded lowering before execution <!-- timefirst:delta=checked-bounded-tool-lowering --></summary>

**Question.** Before an agent-generated data program receives tool authority, can it be lowered into a checked implementation that obeys a hard memory cap? Full title: *SkillEffect: Checked Lowering for Memory-Bounded Agent Tools*. <!-- timefirst:question=memory-bounded-tool-dispatch -->

**Evidence.** Across 24 task–Skill pairs, the `hard cap bounded completion` comparison is 0 / 0 / 4 / 20 / 20 / 24 for direct execution and 12 / 24 / 24 / 24 / 24 / 24 for bounded execution; median peak memory falls 8.45×. <!-- timefirst:evidence=cap-sweep-completion~hard-cap-bounded-completion -->

**Caveat.** Each computation still needs a manually audited relation plugin; XLSX onboarding uses about `476 lines relation-specific code`, and certification scans the input again, so this is not automatic optimization of arbitrary code. <!-- timefirst:caveat=relation-plugin-coverage~476-lines-relation-specific-code -->

**Map.** `early_signal`; place it in Execution & Transformation as a resource check between code generation and execution authority, without changing the stable map.

**Links.** [Primary](https://arxiv.org/abs/2608.17007) · [中文深读](papers/2608.17007.md) · [English note](papers/2608.17007.en.md)

</details>

<a id="entry-2608-18050"></a>
<details><summary>2026-08-21 · StagedWorkspace · Execution & Transformation <!-- timefirst:area=execution-transformation --> — Put dual views on shared workspace state <!-- timefirst:delta=dual-view-workspace-state --></summary>

**Question.** How can parsed retrieval, native files, review diffs, and final delivery avoid referring to different versions of a work product? Full title: *StagedWorkspace: A Versioned Workspace for Knowledge-Work Agents*. <!-- timefirst:question=versioned-workspace-state -->

**Evidence.** The fixed-harness read ablation covers `OfficeQA 133 APEX 452 tasks`; dual view has a higher point estimate than the more limiting single-view arm for every tested model. <!-- timefirst:evidence=fixed-read-ablation~officeqa-133-apex-452-tasks -->

**Caveat.** The experiment isolates dual-view access, not content-hash synchronization: there is no `synced versus unsynced control`, and ingestion, background parsing, and sandbox costs are excluded. <!-- timefirst:caveat=versioning-attribution-gap~synced-versus-unsynced-control -->

**Map.** `early_signal`; place it in Execution & Transformation as a workspace contract across intermediate state, edits, and delivered artifacts, without changing the stable map.

**Links.** [Primary](https://arxiv.org/abs/2608.18050) · [中文深读](papers/2608.18050.md) · [English note](papers/2608.18050.en.md)

</details>

<a id="entry-2608-14246"></a>
<details><summary>2026-08-14 · Polaris · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — Dynamic specialist assignment <!-- timefirst:delta=dynamic-specialist-assignment --></summary>

**Question.** Can specialized agents and online task assignment reliably organize multi-stage enterprise analytics? Full title: *Polaris: Multi Agentic System for Conversational Enterprise Analytics*. <!-- timefirst:question=multi-stage-enterprise-analytics -->

**Evidence.** Tables 1–2 contain forty synthetic Airbnb cases; retrieved-context semantic similarity is 0.85, `context precision 0.99`, and final-response answer relevancy is 0.90, with threshold pass rates of 100% / 100% / 92.5%. <!-- timefirst:evidence=synthetic-case-results~context-precision-0.99 -->

**Caveat.** The paper provides no cost-matched single-agent comparison and no `DTC-off component ablation`, so it does not establish multi-agent superiority over a simpler controller. <!-- timefirst:caveat=coordination-attribution-gap~dtc-off-component-ablation -->

**Map.** `early_signal`; place it in Planning & Semantic Interaction without rewriting the stable map; Execution is a downstream boundary for later isolation.

**Links.** [Primary](https://arxiv.org/abs/2608.14246) · [中文深读](papers/2608.14246.md) · [English note](papers/2608.14246.en.md)

</details>

<a id="entry-2608-09254"></a>
<details><summary>2026-08-10 · Business Truth / QueryProof · Verification & Recovery <!-- timefirst:area=verification-recovery --> — Make safe-to-answer part of correctness <!-- timefirst:delta=safe-to-answer-contract --></summary>

**Question.** After SQL executes, how should a system decide whether the business meaning is correct and whether to clarify, abstain, or return a result? Full title: *Business Truth, not SQL Accuracy: A Rule-Gated 7B Analytics Agent Outperforms a Direct-Prompted 32B Baseline*. <!-- timefirst:question=business-semantic-correctness -->

**Evidence.** The paper explicitly uses **business truth rate targets**, separating clarification/abstention and false success from execution match. <!-- timefirst:evidence=business-truth-evaluation~business-truth-rate-targets -->

**Caveat.** The headline baseline has **unmatched system scaffolding**, and no component ablation isolates the deterministic verification layer. <!-- timefirst:caveat=component-attribution-gap~unmatched-system-scaffolding -->

**Map.** `early_signal`; support Verification & Recovery as a distinct success boundary.

**Links.** [Primary](https://arxiv.org/abs/2608.09254) · [中文深读](papers/2608.09254.md) · [English note](papers/2608.09254.en.md)

</details>

<a id="entry-2607-14386"></a>
<details><summary>2026-07-15 · CIPHER · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — Separate exploration, selection, and execution <!-- timefirst:delta=decoupled-plan-search --></summary>

**Question.** How can a data-science agent avoid locking its trajectory to the first low-evidence hypothesis? Full title: *CIPHER: A Decoupled Exploration-Selection Framework for Test-Time Scaling of Data Science Agents*. <!-- timefirst:question=test-time-plan-diversity -->

**Evidence.** The system performs **diverse initial plan search**, generating multiple initial states before selection and parallel candidate execution. <!-- timefirst:evidence=plan-diversity-mechanism~diverse-initial-plan-search -->

**Caveat.** Gains include **added parallel selection cost**; a clean result needs the same model, tools, and total budget against a single-trajectory control. <!-- timefirst:caveat=cost-matching-gap~added-parallel-selection-cost -->

**Map.** `early_signal`; expose planning as generation × diversity × selection × allocation.

**Links.** [Primary](https://arxiv.org/abs/2607.14386) · [中文深读](papers/2607.14386.md) · [English note](papers/2607.14386.en.md)

</details>

<a id="entry-2606-31041"></a>
<details><summary>2026-06-30 · Semantic-Layer-Mediated Agent · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — Separate business concepts from physical SQL <!-- timefirst:delta=semantic-ir-factorization --></summary>

**Question.** How can enterprise NL→SQL separate business-semantic grounding from dialect-specific execution into inspectable responsibility boundaries? Full title: *A Semantic-Layer-Mediated Agent for Natural Language to SQL over Heterogeneous Enterprise Databases*. <!-- timefirst:question=semantic-physical-factorization -->

**Evidence.** The **Semantic Model Query compilation** path lets the agent emit a business-level intermediate representation before a deterministic compiler realizes physical SQL. <!-- timefirst:evidence=semantic-ir-mechanism~semantic-model-query-compilation -->

**Caveat.** The design transfers quality and maintenance burden to **semantic layer curation cost**; coverage gaps and definition drift remain unresolved. <!-- timefirst:caveat=curation-coverage-dependence~semantic-layer-curation-cost -->

**Map.** `early_signal`; mark the boundary between semantic/intermediate plans and physical execution without changing the stable map.

**Links.** [Primary](https://arxiv.org/abs/2606.31041) · [中文深读](papers/2606.31041.md) · [English note](papers/2606.31041.en.md)

</details>

<a id="entry-2602-16720"></a>
<details><summary>2026-02-11 · APEX-SQL · Data Discovery & Grounding <!-- timefirst:area=data-discovery-grounding --> — Test schema hypotheses against real data <!-- timefirst:delta=active-grounding-probes --></summary>

**Question.** When metadata is insufficient, can an agent actively test column, join, and value hypotheses before generating SQL? Full title: *APEX-SQL: Talking to the data via Agentic Exploration for Text-to-SQL*. <!-- timefirst:question=active-schema-grounding -->

**Evidence.** The method creates an **active data profiling loop**: hypothesis → profiling → verification, followed by SQL generation. <!-- timefirst:evidence=profiling-grounding-loop~active-data-profiling-loop -->

**Caveat.** Active probing adds **online database access cost**, latency, load, and possible data exposure, requiring a cost-matched strong static control. <!-- timefirst:caveat=profiling-resource-cost~online-database-access-cost -->

**Map.** `early_signal`; treat the source as a probeable database environment, not read-only metadata.

**Links.** [Primary](https://arxiv.org/abs/2602.16720) · [中文深读](papers/2602.16720.md) · [English note](papers/2602.16720.en.md)

</details>

<a id="entry-2601-15709"></a>
<details><summary>2026-01-22 · AgentSM · Learning & Reuse <!-- timefirst:area=learning-reuse --> — Persist database-specific execution knowledge <!-- timefirst:delta=semantic-program-memory --></summary>

**Question.** How can execution experience become reusable, interpretable, and maintainable database-specific memory for future queries? Full title: *AgentSM: Semantic Memory for Agentic Text-to-SQL*. <!-- timefirst:question=database-experience-reuse -->

**Evidence.** Prior trajectories become **interpretable semantic programs** that let later queries reuse reasoning paths. <!-- timefirst:evidence=semantic-program-reuse~interpretable-semantic-programs -->

**Caveat.** Persistent experience has **schema workload drift risk**; conflicts, versions, utility attribution, and deletion policy remain open. <!-- timefirst:caveat=persistent-memory-drift~schema-workload-drift-risk -->

**Map.** `early_signal`; separate Learning & Reuse from per-query prompting.

**Links.** [Primary](https://arxiv.org/abs/2601.15709) · [中文深读](papers/2601.15709.md) · [English note](papers/2601.15709.en.md)

</details>

<a id="periods"></a><a id="changes"></a>
## 7 / 30-Day Changes

The current windows aggregate native `radar_published_at` and use the last synthesis time as their exact cutoff. Legacy records remain in the Timeline and reading paths but do not enter Radar-acceptance windows. One work can be a signal, but cannot establish a trend by itself.

<a id="last-7-days"></a>
### Last 7 days · 2026-08-15—2026-08-21

*The time basis is native Radar acceptance; both endpoints are inclusive.*

- **`new_signal` · Execution & Transformation · Put a checked resource boundary before execution authority.** <!-- timefirst:direction key="checked-bounded-tool-lowering" state="new_signal" supports="2608.17007" confidence="medium" implication="separate-resource-safety-from-delivery~resource-safe-execution-not-artifact-correctness" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-21T03:38:26Z" prior="none" --> Support: [SkillEffect](#entry-2608-17007); confidence: **medium**. Implication: measure resource-safe execution separately from final artifact correctness: `resource safe execution not artifact correctness`. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-08-21T03:38:26Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Execution & Transformation · Let localization, editing, and delivery share a workspace boundary.** <!-- timefirst:direction key="dual-view-versioned-workspace" state="new_signal" supports="2608.18050" confidence="medium" implication="test-version-binding-separately~synced-versus-unsynced-control-needed" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-21T03:38:26Z" prior="none" --> Support: [StagedWorkspace](#entry-2608-18050); confidence: **medium**. Implication: a `synced versus unsynced control needed` comparison must isolate version binding. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-08-21T03:38:26Z (UTC)**. Prior map evidence: **none**.

<a id="last-30-days"></a>
### Last 30 days · 2026-07-23—2026-08-21

*The time basis is native Radar acceptance; both endpoints are inclusive.*

- **`new_signal` · Execution & Transformation · Put a checked resource boundary before execution authority.** <!-- timefirst:direction key="checked-bounded-tool-lowering" state="new_signal" supports="2608.17007" confidence="medium" implication="separate-resource-safety-from-delivery~resource-safe-execution-not-artifact-correctness" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-21T03:38:26Z" prior="none" --> Support: [SkillEffect](#entry-2608-17007); confidence: **medium**. Implication: measure resource-safe execution separately from final artifact correctness: `resource safe execution not artifact correctness`. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-08-21T03:38:26Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Execution & Transformation · Let localization, editing, and delivery share a workspace boundary.** <!-- timefirst:direction key="dual-view-versioned-workspace" state="new_signal" supports="2608.18050" confidence="medium" implication="test-version-binding-separately~synced-versus-unsynced-control-needed" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-21T03:38:26Z" prior="none" --> Support: [StagedWorkspace](#entry-2608-18050); confidence: **medium**. Implication: a `synced versus unsynced control needed` comparison must isolate version binding. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-08-21T03:38:26Z (UTC)**. Prior map evidence: **none**.

Both works sit in Execution & Transformation, but their direction keys differ, so neither `reinforces` the other. The evidence adds early signals and leaves the Field Map unchanged.

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

[Evaluation view →](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)

<a id="reading-paths"></a>
## Reading Paths

| Question | Suggested path | What to learn |
|---|---|---|
| **How should an agent ground itself in an enterprise database?** | APEX-SQL → Semantic-Layer-Mediated Agent → AgentSM | Active profiling, semantic abstraction, and reusable database-specific knowledge solve different parts of grounding. |
| **How can resource-bounded execution preserve inspectable artifact state?** | SkillEffect → StagedWorkspace | The first checks resource relations before execution authority; the second puts retrieval views, native edits, diffs, and delivery on one workspace boundary. Neither replaces final-artifact validation. |
| **How should data work become reliable rather than merely executable?** | SkillEffect → StagedWorkspace → Business Truth / QueryProof → Data Agent evaluation in Benchmark Radar | Resource safety, workspace state, business meaning, and artifact verification are distinct success boundaries and should be measured separately. |
| **When does more agentic planning help?** | CIPHER → Polaris | Test-time plan search and multi-agent orchestration add control capacity, but need a simpler matched control and total-cost accounting to isolate value. |

<a id="library"></a>
## Research Library

- **[Browse by problem / research line / year](library/README.en.md)**
- [Data Agent evaluation genealogy](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)

## Scope

High-priority work should change a meaningful control boundary in real data work: data discovery/grounding, semantic planning, multi-tool execution, verification/recovery, workflow learning/reuse, or enterprise analytics orchestration. Plain Text-to-SQL leaderboard papers without a substantive agent-control, data-interaction, or verification contribution are usually not high priority.

## About

This repo covers methods, systems, and research tensions. Benchmark genealogy, protocol validity, and evaluation gaps live in [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data) so the family does not maintain two competing benchmark maps.
