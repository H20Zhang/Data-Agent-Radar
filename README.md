# Data Agent Radar

**中文** | [English](README.en.md)

*追踪 Agent 如何完成端到端数据工作：理解数据、规划分析、执行查询与代码、转换数据、验证结果、从错误中恢复，并交付产物。*

**Radar Family：** [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) · [Agent Memory](https://github.com/H20Zhang/Agent-Memory-Radar) · [Agentic RAG](https://github.com/H20Zhang/Agentic-RAG-Radar) · **Data Agent**

[30 秒：最新时间线](#timeline) · [3 分钟：7/30 天变化](#periods) · [5 分钟：领域地图](#field-map) · [15 分钟：阅读路径](#reading-paths) · [浏览全部](#library)

> **先建立一个简单模型：** `意图 → 数据发现 / 对齐 → 规划 → 查询 / 编码 / 转换 → 检查 / 验证 → 修正 / 恢复 → 学习 / 复用 → 交付`
>
> **当前判断：** Data Agent 不应被缩成“会生成 SQL 的 Agent”。真正困难的是把**业务语义、异构数据、工具执行、中间状态、验证与恢复**连接成一个可靠闭环。

最后更新：**2026-08-20**

<a id="timeline"></a><a id="latest"></a>
## 最新时间线

> **时间说明。** 这 6 条记录在 v2 之前已经公开；原始 Radar 没有保存首次发现与首次收录时间。本次迁移只保留论文发布日期，因此下方日期与首批时间窗只能看作**按旧发布日期形成的信号**，不能解释成 Radar 的接受时间线。展开任一行即可查看问题、证据、限制、地图判断和深读链接。

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

首次迁移窗口按 `published_at` 聚合，只能看作按旧发布日期形成的信号；它不表示 Radar 在这些日期发现或收录了论文。一项工作可以提供新信号，但不能单独证明趋势。

<a id="last-7-days"></a>
### 过去 7 天 · 2026-08-14—2026-08-20

*时间基准是旧论文发布日期；它不编码 Radar 接受事件。*

- **`new_signal` · 规划与语义交互 · 动态编排目前只构成整套系统层面的新信号。** <!-- timefirst:direction key="dynamic-orchestration-package" state="new_signal" supports="2608.14246" confidence="low" implication="match-controller-cost-recovery~controller-total-cost-error-propagation" time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" synthesized="2026-08-20T00:00:00Z" prior="none" --> 支撑：[Polaris](#entry-2608-14246)；置信度：**低**。含义：下一步应匹配控制器，核算总成本和错误传播，并验证恢复能力（`controller total cost error propagation`）。时间基准：`legacy_publication_date`，**not Radar acceptance**。最后合成：**2026-08-20T00:00:00Z (UTC)**。先验地图证据：**none**。

<a id="last-30-days"></a>
### 过去 30 天 · 2026-07-22—2026-08-20

*时间基准是旧论文发布日期；它不编码 Radar 接受事件。*

- **`new_signal` · 规划与语义交互 · 动态编排扩大了系统的控制能力。** <!-- timefirst:direction key="dynamic-orchestration-package" state="new_signal" supports="2608.14246" confidence="low" implication="match-controller-cost-recovery~matched-controller-dtc-off" time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" synthesized="2026-08-20T00:00:00Z" prior="none" --> 支撑：[Polaris](#entry-2608-14246)；置信度：**低**。含义：需要与更简单的控制器做条件匹配，关闭 DTC，并报告总成本和真实企业负载（`matched controller DTC-off`）。时间基准：`legacy_publication_date`，**not Radar acceptance**。最后合成：**2026-08-20T00:00:00Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 验证与恢复 · 能否安全作答成为正确性的一部分。** <!-- timefirst:direction key="business-truth-safety-contract" state="new_signal" supports="2608.09254" confidence="medium" implication="separate-business-truth-from-execution~ambiguity-answerability-clarification" time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" synthesized="2026-08-20T00:00:00Z" prior="none" --> 支撑：[Business Truth / QueryProof](#entry-2608-09254)；置信度：**中**。含义：应分别评测歧义、可回答性与澄清（`ambiguity answerability clarification`），并单独统计拒答和执行后的检查。时间基准：`legacy_publication_date`，**not Radar acceptance**。最后合成：**2026-08-20T00:00:00Z (UTC)**。先验地图证据：**none**。

两项工作解决不同边界，不能互相算作 `reinforces`。CIPHER 发布于 2026-07-15，不在这个 30 天窗口内；它保留在下方稳定地图与阅读路径中。

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
| **如何从“能执行”走到“结果可信”？** | Business Truth / QueryProof → Benchmark Radar 的 Data Agent 评测 | 业务语义、澄清 / 拒答、产物验证和真实计算机执行共同扩大了成功判定范围。 |
| **增加 Agent 规划何时有价值？** | CIPHER → Polaris | 测试时方案搜索和多 Agent 编排提高了控制能力，但必须与更简单、条件匹配且总成本一致的对照系统比较，才能隔离增益。 |

<a id="library"></a>
## 研究资料库

- **[按研究问题 / 研究路线 / 年份浏览](library/README.md)**
- [Data Agent 评测演进脉络](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)

## 收录范围

高优先级工作应改变真实数据工作中的一个重要控制边界：数据发现与对齐、语义规划、多工具执行、验证与恢复、工作流学习与复用，或企业分析编排。仅报告 Text-to-SQL 排行榜结果、没有实质性 Agent 控制、数据交互或验证贡献的论文，通常不是高优先级条目。

## 仓库分工

这个仓库追踪方法、系统与研究分歧。Data Agent 的评测演进脉络、协议有效性和评测缺口统一放在 [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)，避免同系列维护两套相互漂移的评测地图。
