# Data Agent Radar

[中文](README.md) | **English**

*A living research map of agents that perform end-to-end data work: understanding data, planning analyses, executing queries and code, transforming data, verifying results, recovering from errors, and delivering artifacts.*

**Research Radar family:** [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) · [Agent Memory](https://github.com/H20Zhang/Agent-Memory-Radar) · [Agentic RAG](https://github.com/H20Zhang/Agentic-RAG-Radar) · **Data Agent**

[30 sec: Timeline](#timeline) · [3 min: 7/30-day changes](#periods) · [5 min: Field Map](#field-map) · [15 min: Reading Paths](#reading-paths) · [Browse all](#library)

> **Beginner mental model.** `intent → discover/ground data → plan → query/code/transform → inspect/verify → revise/recover → learn/reuse → deliver`
>
> **Current thesis.** A Data Agent is not merely an SQL generator. The difficult systems problem is connecting **business semantics, heterogeneous data, tool execution, intermediate state, verification, and recovery** into a reliable loop.

Last updated: **2026-09-02**

<a id="timeline"></a><a id="latest"></a>
## Latest Timeline

> **Time note.** Native-v2 records are ordered by full `radar_published_at`. The six older records that follow have no reliable first-discovery or first-publication times; their source dates remain contextual and are not Radar acceptance chronology. Open any row for the question, evidence, caveat, map judgment, and deep-reading links.

<a id="entry-2608-31082"></a>
<details><summary>2026-09-02 · Agentic Data Cracking · Learning & Reuse <!-- timefirst:area=learning-reuse --> — Materialize already-read documents into cross-query structure <!-- timefirst:delta=workload-adaptive-structured-reuse --></summary>

**Question.** Once a data-reasoning query has already paid the prefill cost to open a long document, can the system persist part of that evidence as structure so a later, different query touching the same document avoids paying the raw-document read again? Full title: *Token-Efficient Data Reasoning Agents via Adaptive Structuring of Unstructured Data*. <!-- timefirst:question=cross-query-structured-reuse -->

**Evidence.** After adding one human-verified related preceding question for every FanOutQA test question, the paper reports `FanOutQA cost cut 53 percent`: mean prefill falls 189K→87K tokens and mean cost $0.26→$0.12; the 4K cracking decode/cache-read overhead is included, with LLM-judge accuracy 42% vs. 43% (p=.39). <!-- timefirst:evidence=matched-cost-result~fanoutqa-cost-cut-53-percent -->

**Caveat.** The key boundary is `synthetic locality demand cache control absent`: cross-query locality is deliberately constructed, while the matched baseline jointly changes the shared store, catalog, structured reads/writes, and speculative extraction. A same-budget demand-only persistent cache is missing, and dynamic-corpus invalidation/stale-state maintenance is unmeasured. <!-- timefirst:caveat=locality-and-control-confound~synthetic-locality-demand-cache-control-absent -->

**Map.** `early_signal`; enter Learning & Reuse and connect to Data Discovery & Grounding. It expands the reusable object into a workload-materialized shared data substrate, but one paper does not change the stable map.

**Links.** [Primary](https://arxiv.org/abs/2608.31082) · [中文深读](papers/2608.31082.md) · [English note](papers/2608.31082.en.md)

</details>

<a id="entry-2608-25210"></a>
<details><summary>2026-08-28 · BLIP · Verification & Recovery <!-- timefirst:area=verification-recovery --> — Turn provenance into an executable answer-reproduction witness <!-- timefirst:delta=verifiable-answer-provenance --></summary>

**Question.** For LLM-powered data processing, can a plausible citation be upgraded into an executable input subset on which the same model reproduces the same or an equivalent answer? Full title: *Bolt-on, Verifiable Provenance for LLM-Powered Data Processing*. <!-- timefirst:question=answer-reproduction-provenance -->

**Evidence.** Across `seven datasets over thirty percent`, BLIP satisfies the answer-reproduction constraint and reports more than 30% higher provenance accuracy than the best baseline at comparable provenance size, while keeping total inference cost on the same order as the original full-input query. <!-- timefirst:evidence=answer-preservation-guarantee~seven-datasets-over-thirty-percent -->

**Caveat.** The key boundary is `single invocation not business truth`: BLIP verifies reproducibility of the model's current answer. A wrong or ambiguous full-input answer can still be reproduced reliably, and the current definition does not cover a multi-tool, multi-step agent workflow. <!-- timefirst:caveat=reproducibility-truth-boundary~single-invocation-not-business-truth -->

**Map.** `early_signal`; enter Verification & Recovery and separate source relevance, answer-reproduction provenance, and answer/business correctness. One paper does not change the stable map.

**Links.** [Primary](https://arxiv.org/abs/2608.25210) · [中文深读](papers/2608.25210.md) · [English note](papers/2608.25210.en.md)

</details>

<a id="entry-2608-22651"></a>
<details><summary>2026-08-27 · ReAct-SQL · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — Separate grounding and composition controls <!-- timefirst:delta=adaptive-probing-typed-relational-control --></summary>

**Question.** With backbone, hints, and judge fixed, can simple database probing and a typed relational action space separately expose the grounding and composition bottlenecks in Text-to-SQL? Full title: *Iteration Without Elaboration: A Simple ReAct Architecture Suffices for Text-to-SQL Generation*. <!-- timefirst:question=grounding-composition-factorization -->

**Evidence.** In the matched three-stage ablation, `EHR iteration gain 26.23 points` (95% CI [+22.91,+29.66], p≈10^-47), while BIRD iteration adds only +0.60 points; the DSL then adds +5.42 points on BIRD (p=.006) but only +1.71 on EHR. <!-- timefirst:evidence=matched-component-ablation~ehr-iteration-gain-26.23-points -->

**Caveat.** `BIRD iteration and EHR DSL nonsignificant`; EHR-SQL excludes the unanswerable subset, scoring uses a fixed LLM judge, and the cross-system baselines differ in retrieval assets, schema descriptions, and backbone implementation. <!-- timefirst:caveat=benchmark-dependent-attribution~bird-iteration-and-ehr-dsl-nonsignificant -->

**Map.** `early_signal`; enter Planning & Semantic Interaction and connect to Execution & Transformation. It makes probe policy and typed execution representation testable controls without changing the stable map.

**Links.** [Primary](https://arxiv.org/abs/2608.22651) · [中文深读](papers/2608.22651.md) · [English note](papers/2608.22651.en.md)

</details>

<a id="entry-2608-23395"></a>
<details><summary>2026-08-25 · VAT decomposition · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — Test agent granularity with falsification criteria <!-- timefirst:delta=dependency-layer-decomposition-control --></summary>

**Question.** After fixing business subtasks, tools, schemas, validation, and the orchestrator, can worker partitioning identify the real benefit and failure boundary of multi-agent decomposition? Full title: *Right-Sizing LLM-Agent Decomposition in VAT Determination: A Pilot Controlled Sweep*. <!-- timefirst:question=controlled-agent-decomposition -->

**Evidence.** In a 4,400-run synthetic VAT pilot, C2/C3 both have point accuracy of 0.830, but `no headline test survived Holm` and the intermediate-optimum criterion was unmet; one schema-conforming wrong record sharply degrades every condition. <!-- timefirst:evidence=precommitted-controlled-sweep~no-headline-test-survived-holm -->

**Caveat.** Token-matched sensitivity cannot distinguish budget from architecture; `content injection timing confounded`, and a 40-case synthetic rule oracle is not real VAT or legal truth. <!-- timefirst:caveat=decomposition-attribution-gap~content-injection-timing-confounded -->

**Map.** `early_signal`; enter Planning & Semantic Interaction and connect to Verification & Recovery. The negative result defines a testable control boundary but does not change the stable map.

**Links.** [Primary](https://arxiv.org/abs/2608.23395) · [Code, data, and traces](https://github.com/pedro-santos-eng/Right-sizing-LLM-agent-decomposition-in-VAT-determination) · [中文深读](papers/2608.23395.md) · [English note](papers/2608.23395.en.md)

</details>

<a id="entry-2608-19625"></a>
<details><summary>2026-08-24 · Scientific Data Skills · Data Discovery & Grounding <!-- timefirst:area=data-discovery-grounding --> — Package a dataset snapshot as an agent interface <!-- timefirst:delta=dataset-snapshot-skill --></summary>

**Question.** How can scientific context, file organization, operating procedures, quality checks, and snapshot provenance become a reusable dataset interface? Full title: *Scientific Data Skills: Enabling Agent-Ready Scientific Data Services at Scale*. <!-- timefirst:question=dataset-snapshot-interface -->

**Evidence.** The registered, discipline-routed workflow reaches **Hit at one 80.77 percent**, versus 70.19% when the complete skill is retrieved as ordinary text. <!-- timefirst:evidence=registered-workflow-result~hit-at-one-80.77-percent -->

**Caveat.** The winner jointly changes routing, registration, and curated information; a **matched routed raw control absent**, and no dataset invocation or quality check is executed. <!-- timefirst:caveat=routing-content-confound~matched-routed-raw-control-absent -->

**Map.** `early_signal`; enter Data Discovery & Grounding and connect Learning & Reuse. One system paper does not change the stable map.

**Links.** [Primary](https://arxiv.org/abs/2608.19625) · [中文深读](papers/2608.19625.md) · [English note](papers/2608.19625.en.md)

</details>

<a id="entry-2608-19902"></a>
<details><summary>2026-08-24 · Brain Researcher · Verification & Recovery <!-- timefirst:area=verification-recovery --> — Put executable analyses through claim-scope review <!-- timefirst:delta=governed-claim-workflow --></summary>

**Question.** After analysis code runs, how can a system preserve negative results, bound claims, and prevent unreviewed conclusions from entering memory? Full title: *Bringing analytic rigor to agentic AI for science: The Brain Researcher platform for neuroimaging data analysis*. <!-- timefirst:question=scientific-claim-governance -->

**Evidence.** Tool routing rises from 23.3% to 93.6%, but **verified groundedness only 22 percent**; several research episodes explicitly retain blocked, rejected, and conflicting results. <!-- timefirst:evidence=routing-claim-boundary~verified-groundedness-only-22-percent -->

**Caveat.** The headline removes registry, KG, and constraints together; automated review also has a **sign blind review error missed**, so human scientific inspection remains necessary. <!-- timefirst:caveat=automated-review-boundary~sign-blind-review-error-missed -->

**Map.** `early_signal`; enter Verification & Recovery and separate execution artifacts from defensible scientific claims without changing the stable map.

**Links.** [Primary](https://arxiv.org/abs/2608.19902) · [中文深读](papers/2608.19902.md) · [English note](papers/2608.19902.en.md)

</details>

<a id="entry-2608-20434"></a>
<details><summary>2026-08-24 · MAESTRO · Execution & Transformation <!-- timefirst:area=execution-transformation --> — Connect a scientific-data campaign into a traced loop <!-- timefirst:delta=traced-computational-campaign --></summary>

**Question.** Can literature, structure cleaning, multi-fidelity simulation, and candidate delivery share provenance, state, review, and recovery boundaries? Full title: *An LLM agent for end-to-end computational materials discovery*. <!-- timefirst:question=traceable-scientific-campaign -->

**Evidence.** The computational funnel completes **sixty four thousand to eleven candidates** and full process simulation corrects simple proxy rankings; candidates still require experiments. <!-- timefirst:evidence=campaign-funnel-result~sixty-four-thousand-to-eleven-candidates -->

**Caveat.** A **matched single agent pipeline absent**; deterministic scientific tools perform the main computation, leaving multi-agent and LLM orchestration causality unresolved. <!-- timefirst:caveat=orchestration-attribution-gap~matched-single-agent-pipeline-absent -->

**Map.** `early_signal`; enter Execution & Transformation and connect grounding with scientific verification, leaving the stable map unchanged.

**Links.** [Primary](https://arxiv.org/abs/2608.20434) · [中文深读](papers/2608.20434.md) · [English note](papers/2608.20434.en.md)

</details>

<a id="entry-2608-20525"></a>
<details><summary>2026-08-24 · Bolo · Verification & Recovery <!-- timefirst:area=verification-recovery --> — Check runtime and dataflow before pipeline publication <!-- timefirst:delta=runtime-dataflow-admission --></summary>

**Question.** How can an automatically repaired inference template avoid false success that runs without using the target model or input? Full title: *Bolo: Verified Model Hub for Next-Generation AI Databases*. <!-- timefirst:question=inference-pipeline-admission -->

**Evidence.** On selected Type III repositories, **type three runnable 86.08 percent** beats mini-swe's 73.12%, but at about 2.5 times the API cost. <!-- timefirst:evidence=selected-repository-repair~type-three-runnable-86.08-percent -->

**Caveat.** HalluVer checks only static target-model/input/output dataflow; **task specific output verification future**, so the result is not behaviorally verified. <!-- timefirst:caveat=semantic-verification-gap~task-specific-output-verification-future -->

**Map.** `early_signal`; separate runtime success from minimal artifact dataflow without rewriting the stable map.

**Links.** [Primary](https://arxiv.org/abs/2608.20525) · [中文深读](papers/2608.20525.md) · [English note](papers/2608.20525.en.md)

</details>

<a id="entry-2608-20661"></a>
<details><summary>2026-08-24 · KDAF · Verification & Recovery <!-- timefirst:area=verification-recovery --> — Separate answer correctness from evidence replay <!-- timefirst:delta=provenance-vs-answer-correctness --></summary>

**Question.** How can enterprise-finance answers constrain company, period, and provenance without treating a citation as a correct answer? Full title: *Auditable by Construction: An Ontology-Driven Framework for Trustworthy LLM Analytics in Enterprise Finance*. <!-- timefirst:question=enterprise-evidence-replay -->

**Evidence.** KDAF reaches **traceability F1 0.515**, above BM25's 0.463, and eliminates cross-company evidence in the test pool; answer correctness does not improve. <!-- timefirst:evidence=traceability-entity-discipline~traceability-f1-0.515 -->

**Caveat.** The pool is gold-derived and the **matched company filter control absent**; zero leakage may come from a simple metadata filter rather than ontology / CARP. <!-- timefirst:caveat=ontology-attribution-gap~matched-company-filter-control-absent -->

**Map.** `early_signal`; separate provenance replay from business truth and leave the stable map unchanged.

**Links.** [Primary](https://arxiv.org/abs/2608.20661) · [中文深读](papers/2608.20661.md) · [English note](papers/2608.20661.en.md)

</details>

<a id="entry-2608-20844"></a>
<details><summary>2026-08-24 · TRACE · Verification & Recovery <!-- timefirst:area=verification-recovery --> — Separate proposal and review before catalog writes <!-- timefirst:delta=evidence-gated-catalog-write --></summary>

**Question.** When does a multi-source attribute candidate have enough product-identity and evidence support to enter a production catalog? Full title: *TRACE: Agentic Catalog Enrichment with Multi-source Evidence Grounding*. <!-- timefirst:question=catalog-evidence-publication -->

**Evidence.** The package produced a **thirty one million SKUs randomized outcome**: a five-week A/B test increased checkout conversion by 0.48% relative, supporting the end-to-end product result. <!-- timefirst:evidence=production-package-result~thirty-one-million-skus-randomized-outcome -->

**Caveat.** The current four-verdict policy writes UNVERIFIED values, but the **unverified write policy not validated**; there is no Scout-only or matched single-agent control. <!-- timefirst:caveat=judge-attribution-gap~unverified-write-policy-not-validated -->

**Map.** `early_signal`; separate discovery, transformation, and publication authority without treating the Judge or multi-agent package as isolated mechanisms.

**Links.** [Primary](https://arxiv.org/abs/2608.20844) · [中文深读](papers/2608.20844.md) · [English note](papers/2608.20844.en.md)

</details>

<a id="entry-2608-21341"></a>
<details><summary>2026-08-24 · Artic · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — Compile workflow dependencies into explicit artifacts <!-- timefirst:delta=artifact-driven-workflow-compilation --></summary>

**Question.** How can every step in a long workflow declare its reads, writes, and control transfers instead of making the agent infer dependencies from context? Full title: *Natural-Language Workflows Are Not Software Yet: Artifact-Driven Compilation for Reliable Agent Execution*. <!-- timefirst:question=explicit-artifact-control-flow -->

**Evidence.** Against the closest Code control, Artic gains **code control nine thirteen points** across three executors, a more defensible package result than the 28-point Text headline. <!-- timefirst:evidence=matched-code-control~code-control-nine-thirteen-points -->

**Caveat.** The compiler jointly changes decomposition, routing, gates, and retries; a **same calls prompts without artifacts** control is absent, and semantic equivalence remains model-judged. <!-- timefirst:caveat=bundled-harness-attribution~same-calls-prompts-without-artifacts -->

**Map.** `early_signal`; enter Planning & Semantic Interaction and connect execution, verification, and recovery without changing the stable map.

**Links.** [Primary](https://arxiv.org/abs/2608.21341) · [中文深读](papers/2608.21341.md) · [English note](papers/2608.21341.en.md)

</details>

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
<details><summary>2026-08-14 · Polaris · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — Assign specialized analytic roles dynamically <!-- timefirst:delta=dynamic-specialist-assignment --></summary>

**Question.** Can specialized agents plus online task assignment reliably organize multi-stage enterprise analysis? Full title: *Polaris: Multi Agentic System for Conversational Enterprise Analytics*. <!-- timefirst:question=multi-stage-enterprise-analytics -->

**Evidence.** Tables 1–2 evaluate 40 synthetic Airbnb cases; retrieval-context semantic similarity is 0.85, **context precision 0.99**, and final-answer relevance 0.90, with threshold pass rates of 100% / 100% / 92.5%. <!-- timefirst:evidence=synthetic-case-results~context-precision-0.99 -->

**Caveat.** The paper has no condition-matched single-agent control and lacks a **DTC-off component ablation**; it therefore cannot establish multi-agent superiority over a simpler controller. <!-- timefirst:caveat=coordination-attribution-gap~dtc-off-component-ablation -->

**Map.** `early_signal`; place it in Planning & Semantic Interaction without rewriting the stable map. Execution is a downstream boundary that still needs to be isolated.

**Links.** [Primary](https://arxiv.org/abs/2608.14246) · [中文深读](papers/2608.14246.md) · [English note](papers/2608.14246.en.md)

</details>

<a id="entry-2608-09254"></a>
<details><summary>2026-08-10 · Business Truth / QueryProof · Verification & Recovery <!-- timefirst:area=verification-recovery --> — Make safe-to-answer part of correctness <!-- timefirst:delta=safe-to-answer-contract --></summary>

**Question.** After SQL executes successfully, how should a system decide whether the business meaning is correct and whether to clarify, abstain, or answer? Full title: *Business Truth, not SQL Accuracy: A Rule-Gated 7B Analytics Agent Outperforms a Direct-Prompted 32B Baseline*. <!-- timefirst:question=business-semantic-correctness -->

**Evidence.** The work exposes **business truth rate targets** and separates clarification, abstention, and false success from execution matching. <!-- timefirst:evidence=business-truth-evaluation~business-truth-rate-targets -->

**Caveat.** The headline baseline has **unmatched system scaffolding**, and no component ablation isolates the deterministic verification layer. <!-- timefirst:caveat=component-attribution-gap~unmatched-system-scaffolding -->

**Map.** `early_signal`; treat Verification & Recovery as a distinct success boundary.

**Links.** [Primary](https://arxiv.org/abs/2608.09254) · [中文深读](papers/2608.09254.md) · [English note](papers/2608.09254.en.md)

</details>

<a id="entry-2607-14386"></a>
<details><summary>2026-07-15 · CIPHER · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — Decouple exploration, selection, and execution <!-- timefirst:delta=decoupled-plan-search --></summary>

**Question.** How can a data-science agent avoid locking an entire trajectory onto its first weak hypothesis? Full title: *CIPHER: A Decoupled Exploration-Selection Framework for Test-Time Scaling of Data Science Agents*. <!-- timefirst:question=test-time-plan-diversity -->

**Evidence.** The system performs a **diverse initial plan search**, then selects candidate paths for parallel execution. <!-- timefirst:evidence=plan-diversity-mechanism~diverse-initial-plan-search -->

**Caveat.** Gains include **added parallel selection cost**; the needed control fixes model, tools, and total inference budget. <!-- timefirst:caveat=cost-matching-gap~added-parallel-selection-cost -->

**Map.** `early_signal`; decompose planning into plan generation × diversity × selection × resource allocation.

**Links.** [Primary](https://arxiv.org/abs/2607.14386) · [中文深读](papers/2607.14386.md) · [English note](papers/2607.14386.en.md)

</details>

<a id="entry-2606-31041"></a>
<details><summary>2026-06-30 · Semantic-Layer-Mediated Agent · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — Separate business concepts from physical SQL <!-- timefirst:delta=semantic-ir-factorization --></summary>

**Question.** How should enterprise NL→SQL separate business-semantic grounding from dialect-specific execution into inspectable responsibility boundaries? Full title: *A Semantic-Layer-Mediated Agent for Natural Language to SQL over Heterogeneous Enterprise Databases*. <!-- timefirst:question=semantic-physical-factorization -->

**Evidence.** **Semantic Model Query compilation** has the agent produce a business-layer intermediate representation that a deterministic compiler converts into physical SQL. <!-- timefirst:evidence=semantic-ir-mechanism~semantic-model-query-compilation -->

**Caveat.** The system transfers quality and maintenance burden to the **semantic layer curation cost**; coverage gaps and definition drift remain unresolved. <!-- timefirst:caveat=curation-coverage-dependence~semantic-layer-curation-cost -->

**Map.** `early_signal`; mark the boundary between semantic/intermediate planning and physical execution without rewriting the stable map.

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
### Last 7 days · 2026-08-27—2026-09-02

*The time basis is native Radar acceptance; both endpoints are inclusive.*

- **`new_signal` · Learning & Reuse · Already-read unstructured data can become cross-query shared structure.** <!-- timefirst:direction key="workload-adaptive-structured-reuse" state="new_signal" supports="2608.31082" confidence="medium" implication="test-speculation-against-demand-cache~matched-demand-cache-locality-and-invalidation-accounting" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [Agentic Data Cracking](#entry-2608-31082); confidence: **medium**. Implication: before crediting speculative cracking, require `matched demand cache locality and invalidation accounting` to separate persistence, speculation, real locality, and maintenance cost. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Verification & Recovery · Provenance can become a replayable answer-reproduction witness.** <!-- timefirst:direction key="verifiable-answer-provenance" state="new_signal" supports="2608.25210" confidence="medium" implication="separate-reproduction-from-truth~answer-reproduction-not-business-truth" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [BLIP](#entry-2608-25210); confidence: **medium**. Implication: treat `answer reproduction not business truth` as a distinct verification layer before claims about source or business correctness. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Planning & Semantic Interaction · Test database probing separately from typed query control.** <!-- timefirst:direction key="adaptive-probing-typed-relational-control" state="new_signal" supports="2608.22651" confidence="medium" implication="separate-grounding-from-composition~match-probing-and-typed-controls-before-more-orchestration" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [ReAct-SQL](#entry-2608-22651); confidence: **medium**. Implication: `match probing and typed controls before more orchestration` before attributing gains to an elaborate pipeline. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.

<a id="last-30-days"></a>
### Last 30 days · 2026-08-04—2026-09-02

*The time basis is native Radar acceptance; both endpoints are inclusive.*

- **`new_signal` · Learning & Reuse · Already-read unstructured data can become cross-query shared structure.** <!-- timefirst:direction key="workload-adaptive-structured-reuse" state="new_signal" supports="2608.31082" confidence="medium" implication="test-speculation-against-demand-cache~matched-demand-cache-locality-and-invalidation-accounting" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [Agentic Data Cracking](#entry-2608-31082); confidence: **medium**. Implication: before crediting speculative cracking, require `matched demand cache locality and invalidation accounting` to separate persistence, speculation, real locality, and maintenance cost. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Verification & Recovery · Provenance can become a replayable answer-reproduction witness.** <!-- timefirst:direction key="verifiable-answer-provenance" state="new_signal" supports="2608.25210" confidence="medium" implication="separate-reproduction-from-truth~answer-reproduction-not-business-truth" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [BLIP](#entry-2608-25210); confidence: **medium**. Implication: treat `answer reproduction not business truth` as a distinct verification layer before claims about source or business correctness. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Planning & Semantic Interaction · Test database probing separately from typed query control.** <!-- timefirst:direction key="adaptive-probing-typed-relational-control" state="new_signal" supports="2608.22651" confidence="medium" implication="separate-grounding-from-composition~match-probing-and-typed-controls-before-more-orchestration" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [ReAct-SQL](#entry-2608-22651); confidence: **medium**. Implication: `match probing and typed controls before more orchestration` before attributing gains to an elaborate pipeline. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Planning & Semantic Interaction · Test decomposition granularity with budget and fault controls.** <!-- timefirst:direction key="dependency-layer-decomposition-control" state="new_signal" supports="2608.23395" confidence="medium" implication="treat-partition-as-hypothesis~holm-token-and-fault-controls-required" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [VAT decomposition](#entry-2608-23395); confidence: **medium**. Implication: treat partitioning as a hypothesis and require `Holm token and fault controls required`. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Data Discovery & Grounding · Dataset knowledge can become a versioned agent interface.** <!-- timefirst:direction key="dataset-snapshot-skill-interface" state="new_signal" supports="2608.19625" confidence="medium" implication="isolate-routing-registration-content~matched-routed-raw-control-needed" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [Scientific Data Skills](#entry-2608-19625); confidence: **medium**. Implication: a `matched routed raw control needed` to separate routing, registration, and content. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Verification & Recovery · Scientific claims can be bounded or blocked after execution.** <!-- timefirst:direction key="governed-scientific-claim-workflow" state="new_signal" supports="2608.19902" confidence="medium" implication="retain-human-claim-review~automated-review-missed-directionality" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [Brain Researcher](#entry-2608-19902); confidence: **medium**. Implication: retain human review because `automated review missed directionality`. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Execution & Transformation · Traceable state can span a complete computational campaign.** <!-- timefirst:direction key="auditable-computational-campaign" state="new_signal" supports="2608.20434" confidence="medium" implication="compare-orchestration-to-script~same-tools-thresholds-compute-control" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [MAESTRO](#entry-2608-20434); confidence: **medium**. Implication: compare agents with a script using the `same tools thresholds compute control`. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Verification & Recovery · Model-pipeline admission needs more than one successful run.** <!-- timefirst:direction key="verified-inference-pipeline-admission" state="new_signal" supports="2608.20525" confidence="medium" implication="require-output-level-oracles~runnable-dataflow-not-task-correctness" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [Bolo](#entry-2608-20525); confidence: **medium**. Implication: report `runnable dataflow not task correctness` and add output-level oracles. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Verification & Recovery · Replayable provenance does not replace answer correctness.** <!-- timefirst:direction key="ontology-traceable-enterprise-evidence" state="new_signal" supports="2608.20661" confidence="medium" implication="separate-provenance-from-truth~provenance-complete-answer-still-wrong" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [KDAF](#entry-2608-20661); confidence: **medium**. Implication: evaluation must admit that a `provenance complete answer still wrong`. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Verification & Recovery · Catalog writes can follow evidence proposals.** <!-- timefirst:direction key="evidence-gated-catalog-enrichment" state="new_signal" supports="2608.20844" confidence="medium" implication="validate-current-write-policy~human-validate-unverified-writes" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [TRACE](#entry-2608-20844); confidence: **medium**. Implication: **human validate UNVERIFIED writes** before treating the current publication gate as evidence. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Planning & Semantic Interaction · Intermediate artifacts can become workflow-control interfaces.** <!-- timefirst:direction key="artifact-driven-workflow-compilation" state="new_signal" supports="2608.21341" confidence="medium" implication="match-total-inference-budget~same-calls-prompts-gates-budget" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [Artic](#entry-2608-21341); confidence: **medium**. Implication: use the `same calls prompts gates budget` to isolate artifact materialization. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Execution & Transformation · Put a checked resource boundary before execution authority.** <!-- timefirst:direction key="checked-bounded-tool-lowering" state="new_signal" supports="2608.17007" confidence="medium" implication="separate-resource-safety-from-delivery~resource-safe-execution-not-artifact-correctness" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [SkillEffect](#entry-2608-17007); confidence: **medium**. Implication: measure resource-safe execution separately from final artifact correctness: `resource safe execution not artifact correctness`. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Execution & Transformation · Let localization, editing, and delivery share a workspace boundary.** <!-- timefirst:direction key="dual-view-versioned-workspace" state="new_signal" supports="2608.18050" confidence="medium" implication="test-version-binding-separately~synced-versus-unsynced-control-needed" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-09-02T03:29:25Z" prior="none" --> Support: [StagedWorkspace](#entry-2608-18050); confidence: **medium**. Implication: a `synced versus unsynced control needed` comparison must isolate version binding. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **2026-09-02T03:29:25Z (UTC)**. Prior map evidence: **none**.

The thirteen native supports bind to thirteen distinct direction keys. Each remains an independent `new_signal`; none `reinforces` another. The evidence adds early signals and leaves the Field Map unchanged.

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
| **When does more agentic planning help?** | CIPHER → Polaris → VAT decomposition | Test-time search, dynamic orchestration, and fixed dependency partitions are distinct controls. The VAT pilot shows that point-estimate rankings need Holm, budget, and fault-timing checks before they become architecture claims. |
| **How much structure should database interaction add?** | APEX-SQL → ReAct-SQL → Semantic-Layer-Mediated Agent | Separate grounding probe policy from query representation: active probing can resolve value uncertainty, typed IR can reduce composition errors, and a heavier semantic layer additionally carries business definitions and cross-database governance. |
| **When should structure accumulate across queries that repeatedly touch the same documents?** | Agentic Data Cracking → AgentSM | The first materializes document reads already paid for by the workload into a shared data substrate; the second reuses database-specific execution knowledge. Evaluate locality/invalidation separately from schema/workload drift. |
| **How should scientific data move from discovery to a defensible claim?** | Scientific Data Skills → MAESTRO → Brain Researcher | Dataset semantics, computational campaigns, and claim review need separate provenance and failure boundaries; reproducible execution is still not scientific truth. |
| **When are artifacts and evidence ready for publication?** | Bolo → Artic → KDAF → BLIP → TRACE | Runtime, artifact dataflow, provenance replay, answer-reproduction provenance, and write policy are distinct gates; reproducing the model's current answer still does not replace business truth. |

<a id="library"></a>
## Research Library

- **[Browse by problem / research line / year](library/README.en.md)**
- [Data Agent evaluation genealogy](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)

## Scope

High-priority work should change a meaningful control boundary in real data work: data discovery/grounding, semantic planning, multi-tool execution, verification/recovery, workflow learning/reuse, or enterprise analytics orchestration. Plain Text-to-SQL leaderboard papers without a substantive agent-control, data-interaction, or verification contribution are usually not high priority.

## About

This repo covers methods, systems, and research tensions. Benchmark genealogy, protocol validity, and evaluation gaps live in [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data) so the family does not maintain two competing benchmark maps.
