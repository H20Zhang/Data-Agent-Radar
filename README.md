# Data Agent Radar

**中文** | [English](README.en.md)

*追踪 Agent 如何完成端到端数据工作：理解数据、规划分析、执行查询与代码、转换数据、验证结果、从错误中恢复，并交付产物。*

**Radar Family：** [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) · [Agent Memory](https://github.com/H20Zhang/Agent-Memory-Radar) · [Agentic RAG](https://github.com/H20Zhang/Agentic-RAG-Radar) · **Data Agent**

[30 秒：最新时间线](#timeline) · [3 分钟：7/30 天变化](#periods) · [5 分钟：领域地图](#field-map) · [15 分钟：阅读路径](#reading-paths) · [浏览全部](#library)

> **先建立一个简单模型：** `意图 → 数据发现 / 对齐 → 规划 → 查询 / 编码 / 转换 → 检查 / 验证 → 修正 / 恢复 → 学习 / 复用 → 交付`
>
> **当前判断：** Data Agent 不应被缩成“会生成 SQL 的 Agent”。真正困难的是把**业务语义、异构数据、工具执行、中间状态、验证与恢复**连接成一个可靠闭环。

最后更新：**2026-08-25**

<a id="timeline"></a><a id="latest"></a>
## 最新时间线

> **时间说明。** 原生 v2 记录按完整 `radar_published_at` 排列；其后 6 条旧记录没有可靠的首次发现或首次收录时间，只保留来源发布日期作为上下文，不能解释成 Radar 接受时间。展开任一行即可查看问题、证据、限制、地图判断和深读链接。

<a id="entry-2608-23395"></a>
<details><summary>2026-08-25 · VAT decomposition · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — 用否证标准检验 Agent 分工粒度 <!-- timefirst:delta=dependency-layer-decomposition-control --></summary>

**问题。** 在固定业务子任务、工具、schema、验证与 orchestrator 后，只改变 worker partition，能否识别多 Agent 分工的真实收益与失败边界？完整标题：*Right-Sizing LLM-Agent Decomposition in VAT Determination: A Pilot Controlled Sweep*。<!-- timefirst:question=controlled-agent-decomposition -->

**证据。** 这项 4,400-run 合成 VAT pilot 中，C2/C3 点估计均为 0.830，但 `no headline test survived Holm`，作者的 intermediate-optimum 标准未满足；schema-conforming 错误记录让所有配置显著下降。<!-- timefirst:evidence=precommitted-controlled-sweep~no-headline-test-survived-holm -->

**限制。** 现有 token-matched sensitivity 仍无法区分预算与架构；`content injection timing confounded`，且 40 个合成案例的规则 oracle 不等于真实 VAT / legal truth。<!-- timefirst:caveat=decomposition-attribution-gap~content-injection-timing-confounded -->

**地图。** `early_signal`；进入规划与语义交互，并连接验证与恢复；负面结果形成可测试控制边界，但不修改稳定地图。

**链接。** [论文](https://arxiv.org/abs/2608.23395) · [代码、数据与 traces](https://github.com/pedro-santos-eng/Right-sizing-LLM-agent-decomposition-in-VAT-determination) · [中文深读](papers/2608.23395.md) · [英文深读](papers/2608.23395.en.md)

</details>

<a id="entry-2608-19625"></a>
<details><summary>2026-08-24 · Scientific Data Skills · Data Discovery & Grounding <!-- timefirst:area=data-discovery-grounding --> — 把数据集快照封装为 Agent 接口 <!-- timefirst:delta=dataset-snapshot-skill --></summary>

**问题。** 数据集的科学语境、文件结构、使用步骤、质量检查与快照来源如何成为可复用接口？完整标题：*Scientific Data Skills: Enabling Agent-Ready Scientific Data Services at Scale*。<!-- timefirst:question=dataset-snapshot-interface -->

**证据。** 注册并按学科路由的工作流达到 `Hit at one 80.77 percent`，高于把完整 skill 当普通文本检索的 70.19%。<!-- timefirst:evidence=registered-workflow-result~hit-at-one-80.77-percent -->

**限制。** 获胜条件同时改变路由、注册与人工整理的信息；`matched routed raw control absent`，也没有执行数据调用和质量检查。<!-- timefirst:caveat=routing-content-confound~matched-routed-raw-control-absent -->

**地图。** `early_signal`；进入数据发现与对齐，并连接学习与复用；单篇系统证据不修改稳定地图。

**链接。** [论文](https://arxiv.org/abs/2608.19625) · [中文深读](papers/2608.19625.md) · [英文深读](papers/2608.19625.en.md)

</details>

<a id="entry-2608-19902"></a>
<details><summary>2026-08-24 · Brain Researcher · Verification & Recovery <!-- timefirst:area=verification-recovery --> — 让可执行分析接受主张范围审查 <!-- timefirst:delta=governed-claim-workflow --></summary>

**问题。** 分析代码运行后，系统如何保留负结果、限制主张，并阻止未通过科学审查的结论写入记忆？完整标题：*Bringing analytic rigor to agentic AI for science: The Brain Researcher platform for neuroimaging data analysis*。<!-- timefirst:question=scientific-claim-governance -->

**证据。** 工具路由从 23.3% 升至 93.6%，但 `verified groundedness only 22 percent`；多组研究过程明确保留被阻断、拒绝与相互冲突的结果。<!-- timefirst:evidence=routing-claim-boundary~verified-groundedness-only-22-percent -->

**限制。** 主要对照同时移除工具注册表、知识图谱与约束层；自动审查还出现 `sign blind review error missed`，说明人类科学检查仍不可替代。<!-- timefirst:caveat=automated-review-boundary~sign-blind-review-error-missed -->

**地图。** `early_signal`；进入验证与恢复，把执行产物与可辩护科学主张分开；不修改稳定地图。

**链接。** [论文](https://arxiv.org/abs/2608.19902) · [中文深读](papers/2608.19902.md) · [英文深读](papers/2608.19902.en.md)

</details>

<a id="entry-2608-20434"></a>
<details><summary>2026-08-24 · MAESTRO · Execution & Transformation <!-- timefirst:area=execution-transformation --> — 把科学数据 campaign 连接成可追踪闭环 <!-- timefirst:delta=traced-computational-campaign --></summary>

**问题。** 文献、结构清洗、多保真模拟和候选交付能否共享来源、状态、审查与恢复边界？完整标题：*An LLM agent for end-to-end computational materials discovery*。<!-- timefirst:question=traceable-scientific-campaign -->

**证据。** 计算漏斗完成了 `sixty four thousand to eleven candidates`，并用完整过程模拟纠正简单 proxy 排名；候选仍待实验验证。<!-- timefirst:evidence=campaign-funnel-result~sixty-four-thousand-to-eleven-candidates -->

**限制。** 论文没有 `matched single agent pipeline absent` 所指的匹配对照；确定性科学工具完成主要计算，无法隔离多 Agent 或模型编排的因果贡献。<!-- timefirst:caveat=orchestration-attribution-gap~matched-single-agent-pipeline-absent -->

**地图。** `early_signal`；进入执行与转换，并连接数据对齐和科学验证；稳定地图不变。

**链接。** [论文](https://arxiv.org/abs/2608.20434) · [中文深读](papers/2608.20434.md) · [英文深读](papers/2608.20434.en.md)

</details>

<a id="entry-2608-20525"></a>
<details><summary>2026-08-24 · Bolo · Verification & Recovery <!-- timefirst:area=verification-recovery --> — 在发布模型 pipeline 前检查运行与数据流 <!-- timefirst:delta=runtime-dataflow-admission --></summary>

**问题。** 自动修复的 inference template 如何避免“能运行却没真正使用目标模型或输入”的虚假成功？完整标题：*Bolo: Verified Model Hub for Next-Generation AI Databases*。<!-- timefirst:question=inference-pipeline-admission -->

**证据。** 在筛选后的 Type III 仓库上，`type three runnable 86.08 percent`，高于 mini-swe 的 73.12%，但 API 成本约为 2.5 倍。<!-- timefirst:evidence=selected-repository-repair~type-three-runnable-86.08-percent -->

**限制。** 静态检查只覆盖目标模型、输入与输出的数据流；`task specific output verification future`，因此不能称为行为已验证。<!-- timefirst:caveat=semantic-verification-gap~task-specific-output-verification-future -->

**地图。** `early_signal`；把 runtime success 与最小 artifact dataflow 分开，不改写稳定地图。

**链接。** [论文](https://arxiv.org/abs/2608.20525) · [中文深读](papers/2608.20525.md) · [英文深读](papers/2608.20525.en.md)

</details>

<a id="entry-2608-20661"></a>
<details><summary>2026-08-24 · KDAF · Verification & Recovery <!-- timefirst:area=verification-recovery --> — 分开答案正确性与证据可回放性 <!-- timefirst:delta=provenance-vs-answer-correctness --></summary>

**问题。** 企业财务回答如何同时约束公司实体、期间和来源链，而不把 citation 当成正确答案？完整标题：*Auditable by Construction: An Ontology-Driven Framework for Trustworthy LLM Analytics in Enterprise Finance*。<!-- timefirst:question=enterprise-evidence-replay -->

**证据。** 实验中的 `traceability F1 0.515` 高于 BM25 的 0.463，并消除测试池里的跨公司证据；回答正确率没有提升。<!-- timefirst:evidence=traceability-entity-discipline~traceability-f1-0.515 -->

**限制。** 候选池来自 gold evidence，且 `matched company filter control absent`；零泄漏可能来自简单 metadata filter，而非 ontology / CARP。<!-- timefirst:caveat=ontology-attribution-gap~matched-company-filter-control-absent -->

**地图。** `early_signal`；把 provenance replay 与 business truth 分开，稳定地图不变。

**链接。** [论文](https://arxiv.org/abs/2608.20661) · [中文深读](papers/2608.20661.md) · [英文深读](papers/2608.20661.en.md)

</details>

<a id="entry-2608-20844"></a>
<details><summary>2026-08-24 · TRACE · Verification & Recovery <!-- timefirst:area=verification-recovery --> — 在目录写入前分离提议与审查 <!-- timefirst:delta=evidence-gated-catalog-write --></summary>

**问题。** 多源属性候选何时有足够的商品身份与证据支撑，可以写入生产目录？完整标题：*TRACE: Agentic Catalog Enrichment with Multi-source Evidence Grounding*。<!-- timefirst:question=catalog-evidence-publication -->

**证据。** 这套系统形成了 `thirty one million SKUs randomized outcome`：部署覆盖 3,100 万个商品，五周 A/B 的结账转化率相对提升 0.48%。<!-- timefirst:evidence=production-package-result~thirty-one-million-skus-randomized-outcome -->

**限制。** 当前四类 verdict 允许 UNVERIFIED 写入，但 `unverified write policy not validated`；没有 Scout-only 或匹配单 Agent 对照。<!-- timefirst:caveat=judge-attribution-gap~unverified-write-policy-not-validated -->

**地图。** `early_signal`；把发现、转换与发布授权拆开，不把 Judge 或多 Agent package 视为已隔离机制。

**链接。** [论文](https://arxiv.org/abs/2608.20844) · [中文深读](papers/2608.20844.md) · [英文深读](papers/2608.20844.en.md)

</details>

<a id="entry-2608-21341"></a>
<details><summary>2026-08-24 · Artic · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — 把流程依赖编译为显式产物 <!-- timefirst:delta=artifact-driven-workflow-compilation --></summary>

**问题。** 长流程如何让每一步声明读取、写入与控制转移，而不是依靠 Agent 在上下文中猜测依赖？完整标题：*Natural-Language Workflows Are Not Software Yet: Artifact-Driven Compilation for Reliable Agent Execution*。<!-- timefirst:question=explicit-artifact-control-flow -->

**证据。** 最接近的 Code 对照下，Artic 在三个 executor 上高出 `code control nine thirteen points`，比相对 Text 的 28 点 headline 更能代表 package 增益。<!-- timefirst:evidence=matched-code-control~code-control-nine-thirteen-points -->

**限制。** 编译器同时改变分解、路由、检查门与重试；缺少 `same calls prompts without artifacts` 对照，语义等价仍由模型判断。<!-- timefirst:caveat=bundled-harness-attribution~same-calls-prompts-without-artifacts -->

**地图。** `early_signal`；进入规划与语义交互，并连接执行、验证和恢复；不修改稳定地图。

**链接。** [论文](https://arxiv.org/abs/2608.21341) · [中文深读](papers/2608.21341.md) · [英文深读](papers/2608.21341.en.md)

</details>

<a id="entry-2608-17007"></a>
<details><summary>2026-08-21 · SkillEffect · Execution & Transformation <!-- timefirst:area=execution-transformation --> — 执行前检查有界工具降级 <!-- timefirst:delta=checked-bounded-tool-lowering --></summary>

**问题。** 模型生成的数据程序在取得工具执行权前，能否被降为满足硬内存上限的受检实现？完整标题：*SkillEffect: Checked Lowering for Memory-Bounded Agent Tools*。<!-- timefirst:question=memory-bounded-tool-dispatch -->

**证据。** 这 24 个 task–Skill 组合给出 `hard cap bounded completion` 对比：direct 为 0 / 0 / 4 / 20 / 20 / 24，bounded 为 12 / 24 / 24 / 24 / 24 / 24；峰值内存中位数降低 8.45×。<!-- timefirst:evidence=cap-sweep-completion~hard-cap-bounded-completion -->

**限制。** 每类计算仍需人工审计的 relation plugin；XLSX onboarding 约含 `476 lines relation-specific code`，认证还会重复扫描输入，不能解释成任意代码的自动优化。<!-- timefirst:caveat=relation-plugin-coverage~476-lines-relation-specific-code -->

**地图。** `early_signal`；放入执行与转换，在代码生成与执行授权之间增加资源检查边界；不修改稳定地图。

**链接。** [论文](https://arxiv.org/abs/2608.17007) · [中文深读](papers/2608.17007.md) · [英文深读](papers/2608.17007.en.md)

</details>

<a id="entry-2608-18050"></a>
<details><summary>2026-08-21 · StagedWorkspace · Execution & Transformation <!-- timefirst:area=execution-transformation --> — 让双视图共享工作区状态 <!-- timefirst:delta=dual-view-workspace-state --></summary>

**问题。** 解析后的检索视图、原生文件、review diff 与最终交付如何避免引用不同版本的工作产物？完整标题：*StagedWorkspace: A Versioned Workspace for Knowledge-Work Agents*。<!-- timefirst:question=versioned-workspace-state -->

**证据。** 固定 harness 的 read ablation 覆盖 `OfficeQA 133 APEX 452 tasks`；dual view 相对更受限的 single-view arm 在三种模型上均取得更高点估计。<!-- timefirst:evidence=fixed-read-ablation~officeqa-133-apex-452-tasks -->

**限制。** 实验隔离的是双视图访问，而不是内容哈希同步；没有 `synced versus unsynced control`，且 ingestion、后台 parsing 与 sandbox 成本未计入。<!-- timefirst:caveat=versioning-attribution-gap~synced-versus-unsynced-control -->

**地图。** `early_signal`；放入执行与转换，把中间状态、编辑与交付产物连成工作区契约；不修改稳定地图。

**链接。** [论文](https://arxiv.org/abs/2608.18050) · [中文深读](papers/2608.18050.md) · [英文深读](papers/2608.18050.en.md)

</details>

<a id="entry-2608-14246"></a>
<details><summary>2026-08-14 · Polaris · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — 动态分派专门分析角色 <!-- timefirst:delta=dynamic-specialist-assignment --></summary>

**问题。** 专门分工的 Agent 与在线任务分派，能否可靠组织多阶段企业分析？完整标题：*Polaris: Multi Agentic System for Conversational Enterprise Analytics*。<!-- timefirst:question=multi-stage-enterprise-analytics -->

**证据。** 表 1–2 共评测 40 个合成的 Airbnb 案例；检索上下文语义相似度为 0.85、`context precision 0.99`、最终回答相关性为 0.90，阈值通过率分别为 100% / 100% / 92.5%。<!-- timefirst:evidence=synthetic-case-results~context-precision-0.99 -->

**限制。** 论文没有与单 Agent 对照条件匹配的实验，也缺少 `DTC-off component ablation`；因此不能声称多 Agent 系统优于更简单的控制器。<!-- timefirst:caveat=coordination-attribution-gap~dtc-off-component-ablation -->

**地图。** `early_signal`；先放在规划与语义交互，不改写稳定地图；执行是后续需要拆分验证的下游边界。

**链接。** [论文](https://arxiv.org/abs/2608.14246) · [中文深读](papers/2608.14246.md) · [英文深读](papers/2608.14246.en.md)

</details>

<a id="entry-2608-09254"></a>
<details><summary>2026-08-10 · Business Truth / QueryProof · Verification & Recovery <!-- timefirst:area=verification-recovery --> — 把 safe-to-answer 纳入正确性 <!-- timefirst:delta=safe-to-answer-contract --></summary>

**问题。** 一条 SQL 成功执行后，系统如何判断业务含义是否正确，以及应该澄清、拒答还是返回结果？完整标题：*Business Truth, not SQL Accuracy: A Rule-Gated 7B Analytics Agent Outperforms a Direct-Prompted 32B Baseline*。<!-- timefirst:question=business-semantic-correctness -->

**证据。** 论文把 `business truth rate targets` 作为明确指标，并将澄清、拒答和虚假成功从执行匹配中拆开。<!-- timefirst:evidence=business-truth-evaluation~business-truth-rate-targets -->

**限制。** 标题中的基线比较没有匹配整套系统脚手架（`unmatched system scaffolding`），也没有组件消融来隔离确定性验证层。<!-- timefirst:caveat=component-attribution-gap~unmatched-system-scaffolding -->

**地图。** `early_signal`；支持把验证与恢复作为独立的成功边界。

**链接。** [论文](https://arxiv.org/abs/2608.09254) · [中文深读](papers/2608.09254.md) · [英文深读](papers/2608.09254.en.md)

</details>

<a id="entry-2607-14386"></a>
<details><summary>2026-07-15 · CIPHER · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — 分离探索、选择与执行 <!-- timefirst:delta=decoupled-plan-search --></summary>

**问题。** 数据科学 Agent 如何避免整条任务轨迹被第一个低证据假设锁死？完整标题：*CIPHER: A Decoupled Exploration-Selection Framework for Test-Time Scaling of Data Science Agents*。<!-- timefirst:question=test-time-plan-diversity -->

**证据。** 系统先搜索多套初始方案（`diverse initial plan search`），再选择候选路径并行执行。<!-- timefirst:evidence=plan-diversity-mechanism~diverse-initial-plan-search -->

**限制。** 收益同时包含额外的并行选择成本（`added parallel selection cost`）；需要模型、工具和总预算均相同的单轨迹对照。<!-- timefirst:caveat=cost-matching-gap~added-parallel-selection-cost -->

**地图。** `early_signal`；把规划拆成方案生成 × 多样性 × 选择 × 资源分配。

**链接。** [论文](https://arxiv.org/abs/2607.14386) · [中文深读](papers/2607.14386.md) · [英文深读](papers/2607.14386.en.md)

</details>

<a id="entry-2606-31041"></a>
<details><summary>2026-06-30 · Semantic-Layer-Mediated Agent · Planning & Semantic Interaction <!-- timefirst:area=planning-semantic-interaction --> — 分离业务概念与 physical SQL <!-- timefirst:delta=semantic-ir-factorization --></summary>

**问题。** 企业场景中的 NL→SQL 如何把业务语义对齐与特定方言执行拆成可检查的责任边界？完整标题：*A Semantic-Layer-Mediated Agent for Natural Language to SQL over Heterogeneous Enterprise Databases*。<!-- timefirst:question=semantic-physical-factorization -->

**证据。** `Semantic Model Query compilation` 让 Agent 先生成业务层中间表示，再由确定性编译器转换为物理 SQL。<!-- timefirst:evidence=semantic-ir-mechanism~semantic-model-query-compilation -->

**限制。** 系统把大量质量和维护负担转移给语义层整理（`semantic layer curation cost`）；覆盖缺口和定义漂移仍未解决。<!-- timefirst:caveat=curation-coverage-dependence~semantic-layer-curation-cost -->

**地图。** `early_signal`；标记语义 / 中间计划与物理执行之间的边界，不改写稳定地图。

**链接。** [论文](https://arxiv.org/abs/2606.31041) · [中文深读](papers/2606.31041.md) · [英文深读](papers/2606.31041.en.md)

</details>

<a id="entry-2602-16720"></a>
<details><summary>2026-02-11 · APEX-SQL · Data Discovery & Grounding <!-- timefirst:area=data-discovery-grounding --> — 用真实数据验证 schema 假设 <!-- timefirst:delta=active-grounding-probes --></summary>

**问题。** 元数据不足时，Agent 能否在生成 SQL 前主动验证字段、连接关系和值域假设？完整标题：*APEX-SQL: Talking to the data via Agentic Exploration for Text-to-SQL*。<!-- timefirst:question=active-schema-grounding -->

**证据。** 方法建立 `active data profiling loop`：先提出假设，再分析数据并验证，最后生成 SQL。<!-- timefirst:evidence=profiling-grounding-loop~active-data-profiling-loop -->

**限制。** 主动探查会增加在线数据库访问成本（`online database access cost`）、延迟、负载和潜在数据暴露风险，需要与强静态对照做成本匹配。<!-- timefirst:caveat=profiling-resource-cost~online-database-access-cost -->

**地图。** `early_signal`；把信息来源从只读元数据扩展为可主动探查的数据库环境。

**链接。** [论文](https://arxiv.org/abs/2602.16720) · [中文深读](papers/2602.16720.md) · [英文深读](papers/2602.16720.en.md)

</details>

<a id="entry-2601-15709"></a>
<details><summary>2026-01-22 · AgentSM · Learning & Reuse <!-- timefirst:area=learning-reuse --> — 持久化 database-specific execution knowledge <!-- timefirst:delta=semantic-program-memory --></summary>

**问题。** 历史执行经验如何变成可供后续查询复用、可解释且可维护的数据库专属记忆？完整标题：*AgentSM: Semantic Memory for Agentic Text-to-SQL*。<!-- timefirst:question=database-experience-reuse -->

**证据。** 历史轨迹被整理为可解释的语义程序（`interpretable semantic programs`），使后续查询可以复用推理路径。<!-- timefirst:evidence=semantic-program-reuse~interpretable-semantic-programs -->

**限制。** 持久经验面临数据库模式和工作负载漂移（`schema workload drift risk`）；冲突、版本、效用归因和删除策略仍是开放问题。<!-- timefirst:caveat=persistent-memory-drift~schema-workload-drift-risk -->

**地图。** `early_signal`；把学习与复用从逐次查询提示中单独划出。

**链接。** [论文](https://arxiv.org/abs/2601.15709) · [中文深读](papers/2601.15709.md) · [英文深读](papers/2601.15709.en.md)

</details>

<a id="periods"></a><a id="changes"></a>
## 7 / 30 天变化

当前窗口按原生 `radar_published_at` 聚合，并以最后合成时刻作为精确截止。旧记录仍保留在时间线与阅读路径中，但不进入 Radar 接受时间窗。一项工作可以提供新信号，不能单独证明趋势。

<a id="last-7-days"></a>
### 过去 7 天 · 2026-08-19—2026-08-25

*时间基准是原生 Radar 接受时间；窗口含首尾两日。*

- **`new_signal` · 规划与语义交互 · 分工粒度需要用预算与故障对照检验。** <!-- timefirst:direction key="dependency-layer-decomposition-control" state="new_signal" supports="2608.23395" confidence="medium" implication="treat-partition-as-hypothesis~holm-token-and-fault-controls-required" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[VAT decomposition](#entry-2608-23395)；置信度：**中**。含义：将 partition 视为待检验假设，并要求 `Holm token and fault controls required`。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 数据发现与对齐 · 数据集知识可以成为版本化 Agent 接口。** <!-- timefirst:direction key="dataset-snapshot-skill-interface" state="new_signal" supports="2608.19625" confidence="medium" implication="isolate-routing-registration-content~matched-routed-raw-control-needed" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[Scientific Data Skills](#entry-2608-19625)；置信度：**中**。含义：需要 `matched routed raw control needed`，分别检验路由、注册与内容。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 验证与恢复 · 科学主张可以在执行后被限定或阻断。** <!-- timefirst:direction key="governed-scientific-claim-workflow" state="new_signal" supports="2608.19902" confidence="medium" implication="retain-human-claim-review~automated-review-missed-directionality" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[Brain Researcher](#entry-2608-19902)；置信度：**中**。含义：必须保留人类审查，因为 `automated review missed directionality`。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 执行与转换 · 可追踪状态可以贯穿完整计算 campaign。** <!-- timefirst:direction key="auditable-computational-campaign" state="new_signal" supports="2608.20434" confidence="medium" implication="compare-orchestration-to-script~same-tools-thresholds-compute-control" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[MAESTRO](#entry-2608-20434)；置信度：**中**。含义：需要 `same tools thresholds compute control` 比较 Agent 与静态 pipeline。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 验证与恢复 · 模型 pipeline 准入需要超过一次成功运行。** <!-- timefirst:direction key="verified-inference-pipeline-admission" state="new_signal" supports="2608.20525" confidence="medium" implication="require-output-level-oracles~runnable-dataflow-not-task-correctness" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[Bolo](#entry-2608-20525)；置信度：**中**。含义：应分别报告 `runnable dataflow not task correctness`，并增加 output-level oracle。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 验证与恢复 · 来源可回放性不能替代答案正确性。** <!-- timefirst:direction key="ontology-traceable-enterprise-evidence" state="new_signal" supports="2608.20661" confidence="medium" implication="separate-provenance-from-truth~provenance-complete-answer-still-wrong" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[KDAF](#entry-2608-20661)；置信度：**中**。含义：评价必须承认 `provenance complete answer still wrong`。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 验证与恢复 · 目录写入可以晚于证据提议。** <!-- timefirst:direction key="evidence-gated-catalog-enrichment" state="new_signal" supports="2608.20844" confidence="medium" implication="validate-current-write-policy~human-validate-unverified-writes" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[TRACE](#entry-2608-20844)；置信度：**中**。含义：必须 `human validate unverified writes`，才能评价当前发布门槛。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 规划与语义交互 · 中间产物可以成为流程控制接口。** <!-- timefirst:direction key="artifact-driven-workflow-compilation" state="new_signal" supports="2608.21341" confidence="medium" implication="match-total-inference-budget~same-calls-prompts-gates-budget" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[Artic](#entry-2608-21341)；置信度：**中**。含义：下一步需要 `same calls prompts gates budget`，才能隔离 artifact materialization。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 执行与转换 · 执行授权前可以加入可检查的资源边界。** <!-- timefirst:direction key="checked-bounded-tool-lowering" state="new_signal" supports="2608.17007" confidence="medium" implication="separate-resource-safety-from-delivery~resource-safe-execution-not-artifact-correctness" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[SkillEffect](#entry-2608-17007)；置信度：**中**。含义：后续应分别测量 resource-safe execution 与最终 artifact correctness（`resource safe execution not artifact correctness`）。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 执行与转换 · 双视图让定位、编辑与交付共享工作区边界。** <!-- timefirst:direction key="dual-view-versioned-workspace" state="new_signal" supports="2608.18050" confidence="medium" implication="test-version-binding-separately~synced-versus-unsynced-control-needed" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[StagedWorkspace](#entry-2608-18050)；置信度：**中**。含义：下一步需要 `synced versus unsynced control needed`，才能隔离版本绑定的作用。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。

<a id="last-30-days"></a>
### 过去 30 天 · 2026-07-27—2026-08-25

*时间基准是原生 Radar 接受时间；窗口含首尾两日。*

- **`new_signal` · 规划与语义交互 · 分工粒度需要用预算与故障对照检验。** <!-- timefirst:direction key="dependency-layer-decomposition-control" state="new_signal" supports="2608.23395" confidence="medium" implication="treat-partition-as-hypothesis~holm-token-and-fault-controls-required" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[VAT decomposition](#entry-2608-23395)；置信度：**中**。含义：将 partition 视为待检验假设，并要求 `Holm token and fault controls required`。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 数据发现与对齐 · 数据集知识可以成为版本化 Agent 接口。** <!-- timefirst:direction key="dataset-snapshot-skill-interface" state="new_signal" supports="2608.19625" confidence="medium" implication="isolate-routing-registration-content~matched-routed-raw-control-needed" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[Scientific Data Skills](#entry-2608-19625)；置信度：**中**。含义：需要 `matched routed raw control needed`，分别检验路由、注册与内容。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 验证与恢复 · 科学主张可以在执行后被限定或阻断。** <!-- timefirst:direction key="governed-scientific-claim-workflow" state="new_signal" supports="2608.19902" confidence="medium" implication="retain-human-claim-review~automated-review-missed-directionality" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[Brain Researcher](#entry-2608-19902)；置信度：**中**。含义：必须保留人类审查，因为 `automated review missed directionality`。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 执行与转换 · 可追踪状态可以贯穿完整计算 campaign。** <!-- timefirst:direction key="auditable-computational-campaign" state="new_signal" supports="2608.20434" confidence="medium" implication="compare-orchestration-to-script~same-tools-thresholds-compute-control" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[MAESTRO](#entry-2608-20434)；置信度：**中**。含义：需要 `same tools thresholds compute control` 比较 Agent 与静态 pipeline。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 验证与恢复 · 模型 pipeline 准入需要超过一次成功运行。** <!-- timefirst:direction key="verified-inference-pipeline-admission" state="new_signal" supports="2608.20525" confidence="medium" implication="require-output-level-oracles~runnable-dataflow-not-task-correctness" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[Bolo](#entry-2608-20525)；置信度：**中**。含义：应分别报告 `runnable dataflow not task correctness`，并增加 output-level oracle。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 验证与恢复 · 来源可回放性不能替代答案正确性。** <!-- timefirst:direction key="ontology-traceable-enterprise-evidence" state="new_signal" supports="2608.20661" confidence="medium" implication="separate-provenance-from-truth~provenance-complete-answer-still-wrong" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[KDAF](#entry-2608-20661)；置信度：**中**。含义：评价必须承认 `provenance complete answer still wrong`。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 验证与恢复 · 目录写入可以晚于证据提议。** <!-- timefirst:direction key="evidence-gated-catalog-enrichment" state="new_signal" supports="2608.20844" confidence="medium" implication="validate-current-write-policy~human-validate-unverified-writes" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[TRACE](#entry-2608-20844)；置信度：**中**。含义：必须 `human validate unverified writes`，才能评价当前发布门槛。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 规划与语义交互 · 中间产物可以成为流程控制接口。** <!-- timefirst:direction key="artifact-driven-workflow-compilation" state="new_signal" supports="2608.21341" confidence="medium" implication="match-total-inference-budget~same-calls-prompts-gates-budget" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[Artic](#entry-2608-21341)；置信度：**中**。含义：下一步需要 `same calls prompts gates budget`，才能隔离 artifact materialization。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 执行与转换 · 执行授权前可以加入可检查的资源边界。** <!-- timefirst:direction key="checked-bounded-tool-lowering" state="new_signal" supports="2608.17007" confidence="medium" implication="separate-resource-safety-from-delivery~resource-safe-execution-not-artifact-correctness" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[SkillEffect](#entry-2608-17007)；置信度：**中**。含义：后续应分别测量 resource-safe execution 与最终 artifact correctness（`resource safe execution not artifact correctness`）。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 执行与转换 · 双视图让定位、编辑与交付共享工作区边界。** <!-- timefirst:direction key="dual-view-versioned-workspace" state="new_signal" supports="2608.18050" confidence="medium" implication="test-version-binding-separately~synced-versus-unsynced-control-needed" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="2026-08-25T03:15:40Z" prior="none" --> 支撑：[StagedWorkspace](#entry-2608-18050)；置信度：**中**。含义：下一步需要 `synced versus unsynced control needed`，才能隔离版本绑定的作用。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**2026-08-25T03:15:40Z (UTC)**。先验地图证据：**none**。

十项原生支持分别绑定到十个不同方向键；它们都是独立 `new_signal`，不能互相算作 `reinforces`。当前证据只增加早期信号，领域地图保持不变。

<a id="field-map"></a>
## 领域地图

`意图 → 数据发现 / 对齐 → 规划 → 执行 / 转换 → 检查 / 验证 → 恢复 → 学习 / 复用 → 交付`

| 研究问题 | 核心问题 | 当前张力 |
|---|---|---|
| **Data Discovery & Grounding** | Agent 如何找到真正相关的数据库模式、表、文件、文档、指标和业务定义？ | `静态元数据 ↔ 主动探查` |
| **Planning & Semantic Interaction** | 用户意图如何转化为可执行、可检查的分析计划？ | `直接生成 SQL / 代码 ↔ 语义 / 中间计划` |
| **Execution & Transformation** | SQL、Python、计算笔记本、数据库 / API 工具和真实计算机操作如何协同？ | `单次生成 ↔ 基于数据对齐的多工具执行` |
| **Verification & Recovery** | 一个已经成功执行的结果何时仍可能出错？Agent 应如何恢复？ | `执行成功 ↔ 业务真实性 / 产物验证` |
| **Learning & Reuse** | 哪些历史分析、工作流、技能和记忆值得持续复用？ | `每次从零开始 ↔ 复用经验` |

[看 Data Agent 如何被评价 →](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)

<a id="reading-paths"></a>
## 阅读路径

| 你想回答的问题 | 建议顺序 | 应该学到什么 |
|---|---|---|
| **Agent 应如何理解企业数据库？** | APEX-SQL → Semantic-Layer-Mediated Agent → AgentSM | 主动数据分析、语义抽象和数据库专属的可复用知识分别解决不同的对齐问题。 |
| **受资源约束的执行如何保留可检查的产物状态？** | SkillEffect → StagedWorkspace | 前者在执行授权前检查资源关系，后者把检索视图、原生编辑、diff 与交付放入同一工作区边界；两者都不能替代最终产物验证。 |
| **如何从“能执行”走到“结果可信”？** | SkillEffect → StagedWorkspace → Business Truth / QueryProof → Benchmark Radar 的 Data Agent 评测 | 资源安全、工作区状态、业务语义和产物验证是不同的成功边界，应分别测量。 |
| **增加 Agent 规划何时有价值？** | CIPHER → Polaris → VAT decomposition | 测试时搜索、动态编排与固定依赖分区是不同控制面；VAT pilot 表明点估计排序必须同时经受 Holm、多预算和故障时序检查，才能解释为架构收益。 |
| **科学数据如何从发现走到可辩护主张？** | Scientific Data Skills → MAESTRO → Brain Researcher | 数据集语义、计算 campaign 与主张审查必须保留各自的来源和失败边界；可复现执行仍不等于科学真实。 |
| **产物与证据何时足以获准发布？** | Bolo → Artic → KDAF → TRACE | runtime、artifact dataflow、来源可回放性与 write policy 是不同 gate；任何一层通过都不能自动替代业务真实性。 |

<a id="library"></a>
## 研究资料库

- **[按研究问题 / 研究路线 / 年份浏览](library/README.md)**
- [Data Agent 评测演进脉络](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)

## 收录范围

高优先级工作应改变真实数据工作中的一个重要控制边界：数据发现与对齐、语义规划、多工具执行、验证与恢复、工作流学习与复用，或企业分析编排。仅报告 Text-to-SQL 排行榜结果、没有实质性 Agent 控制、数据交互或验证贡献的论文，通常不是高优先级条目。

## 仓库分工

这个仓库追踪方法、系统与研究分歧。Data Agent 的评测演进脉络、协议有效性和评测缺口统一放在 [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)，避免同系列维护两套相互漂移的评测地图。
