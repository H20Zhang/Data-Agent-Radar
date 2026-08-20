# Data Agent Radar

**中文** | [English](README.en.md)

本清单追踪 Agent 如何完成端到端数据工作：理解数据、规划分析、执行查询和代码、转换数据、验证结果、从错误中恢复，并交付产物。

同系列：[Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) · [Agent Memory](https://github.com/H20Zhang/Agent-Memory-Radar) · [Agentic RAG](https://github.com/H20Zhang/Agentic-RAG-Radar) · **Data Agent**

[最新工作](#latest) · [领域地图](#field-map) · [阅读路径](#reading-paths) · [文献库](#library)

最后更新：**2026-08-20**

<a id="latest"></a>
## 最新研究信号

### [Polaris: Multi Agentic System for Conversational Enterprise Analytics](https://arxiv.org/abs/2608.14246)
`规划与编排` · **2026-08-14**

Polaris 将企业分析任务分配给负责查询、可视化和推理的专用 Agent，并通过 Dynamic Task Coordination 动态匹配 Agent 与任务。接下来需要验证的是，与更简单的单 Agent + 工具路由对照相比，多 Agent 协作究竟带来了多少额外收益。

### [Business Truth, not SQL Accuracy: A Rule-Gated 7B Analytics Agent Outperforms a Direct-Prompted 32B Baseline](https://arxiv.org/abs/2608.09254)
`验证与可靠性` · **2026-08-10**

这项工作不再把“SQL 可以执行”等同于“业务含义正确”，而是把澄清、拒答、数据库模式漂移和执行后的确定性检查都纳入分析 Agent 的正确性判断。

<details><summary><strong>SQL 执行成功与 Business Truth 的差距</strong></summary>

生产分析中的失败通常不是语法错误，而是存在多个合理的业务定义、数据仓库无法回答问题、字段已经弃用，或者查询正常执行却返回了错误的业务数值。QueryProof 根据语义层规则和物理数据目录规则决定如何处理，并在查询执行后、输出答案前进行确定性检查。

论文报告的 Business Truth Rate 高于一个参数更多但只使用直接提示的模型基线。不过，两套系统的脚手架并不匹配，也没有组件消融实验单独隔离确定性层。因此，更稳妥的结论不是“小模型打赢大模型”，而是：**业务语义正确性、澄清、拒答和虚假成功率应与执行匹配分开评测。**

</details>

### [CIPHER: A Decoupled Exploration-Selection Framework for Test-Time Scaling of Data Science Agents](https://arxiv.org/abs/2607.14386)
`规划与搜索` · **2026-07-15**

CIPHER 不让整条数据科学任务轨迹受单个初始状态约束。它生成多个候选起点，将探索与选择分开，然后并行执行多条路径。

### [A Semantic-Layer-Mediated Agent for Natural Language to SQL over Heterogeneous Enterprise Databases](https://arxiv.org/abs/2606.31041)
`语义对齐与执行` · **2026-06-30**

Agent 不再直接从原始物理模式生成 SQL，而是先在经过整理的语义层上生成紧凑的 Semantic Model Query，再由确定性编译器处理物理模式和 SQL 方言。

<details><summary><strong>为什么引入 Semantic Model Query</strong></summary>

面对数百张物理表时，直接做 NL→SQL 会要求模型同时解决业务语义对齐和特定 SQL 方言的执行。这个设计在两者之间加入语义中间表示：LLM 组合已经验证的业务概念，再由确定性代码编译成具体 SQL。

这种设计可以改善语义对齐，但也让系统质量更依赖语义层。比较时应关注所需的整理成本、覆盖率是否足够，以及语义层缺失或错误时系统如何退化。

</details>

### [APEX-SQL: Talking to the data via Agentic Exploration for Text-to-SQL](https://arxiv.org/abs/2602.16720)
`数据发现与对齐` · **2026-02-11**

在 APEX-SQL 中，数据库模式关联从静态匹配变为 `假设 → 数据分析 → 验证`：Agent 主动检查真实的字段值和数据分布，在验证字段和连接关系假设后再生成 SQL。

### [AgentSM: Semantic Memory for Agentic Text-to-SQL](https://arxiv.org/abs/2601.15709)
`学习与复用` · **2026-01-22**

AgentSM 将历史执行轨迹整理为可解释的语义程序，并作为数据库专属的持久化记忆保存。后续查询可以复用已有的推理路径，不必每次从零探索。

<a id="changes"></a>
## 研究变化

| 变化 | 新证据 | 对研究设计的含义 |
|---|---|---|
| **语义对齐环节正在移到代码生成之前。** | APEX-SQL 主动分析数据分布；Semantic-Layer-Mediated Agent 先基于业务概念规划，再生成物理 SQL。 | 评估时不能只看执行准确率，还要计入探索和语义层维护成本。 |
| **验证正成为独立阶段。** | QueryProof 这类工作把业务真实性、澄清、拒答和执行后检查从“能执行”中区分出来。 | Data Agent 需要明确何时**不应返回一个数值**。 |
| **数据工作正成为长时程控制问题。** | CIPHER 搜索多个初始方案；Polaris 协调多个 Agent；AgentSM 复用历史执行经验。 | 规划、中间状态、恢复和复用应与最终产物分开评测。 |

<a id="field-map"></a>
## 领域地图

`意图 → 发现/对齐 → 规划 → 执行/转换 → 检查/验证 → 恢复 → 学习/复用 → 交付`

| 研究问题 | 核心问题 | 当前张力 |
|---|---|---|
| **Data Discovery & Grounding** | Agent 如何找到真正相关的数据库模式、表、文件、文档、指标和业务定义？ | `静态元数据 ↔ 主动数据分析` |
| **Planning & Semantic Interaction** | 用户意图如何转化为可执行、可检查的分析计划？ | `直接 NL→SQL/代码 ↔ 语义/中间计划` |
| **Execution & Transformation** | SQL、Python、计算笔记本、数据库/API 工具和真实计算机操作如何协同？ | `单次生成 ↔ 基于数据对齐的多工具执行` |
| **Verification & Recovery** | 一个已经成功执行的结果何时仍可能出错？Agent 应如何恢复？ | `执行成功 ↔ 业务真实性/产物验证` |
| **Learning & Reuse** | 哪些历史分析、工作流、技能和记忆值得持续复用？ | `从零开始 ↔ 复用经验` |

[看 Data Agent 如何被评价 →](https://github.com/H20Zhang/Agent-Benchmark-Radar#data-agents)

<a id="reading-paths"></a>
## 阅读路径

| 你想回答的问题 | 建议顺序 | 应该学到什么 |
|---|---|---|
| **Agent 应如何理解企业数据库？** | APEX-SQL → Semantic-Layer-Mediated Agent → AgentSM | 主动数据分析、语义抽象和数据库专属的可复用知识分别解决不同的对齐问题。 |
| **如何从“能执行”走到“结果可信”？** | QueryProof / Business Truth → Benchmark Radar 的 DataSpace / DSAgentBench | 业务语义、澄清/拒答、产物验证和真实计算机执行共同扩大了成功判定的范围。 |
| **增加 Agent 规划何时有价值？** | CIPHER → Polaris | 测试时方案搜索和多 Agent 编排提高了控制能力，但必须与更简单、条件匹配的对照系统比较，才能隔离增益。 |

<a id="library"></a>
## 研究文献库

- [按研究问题 / 研究路线 / 年份浏览](library/README.md)
- [Data Agent 评测演进脉络](https://github.com/H20Zhang/Agent-Benchmark-Radar)

## 收录范围与分工

高优先级工作应改变真实数据工作中的一个重要控制边界：数据发现与对齐、语义规划、多工具执行、验证与恢复、工作流学习与复用，或企业分析编排。

仅报告 Text-to-SQL 排行榜结果、没有实质性 Agent 控制、数据交互或验证贡献的论文，通常不属于本清单的高优先级条目。

本仓库收录方法、系统和研究分歧。Data Agent 评测基准的演进脉络、评测协议有效性和评测缺口统一由 [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) 维护，避免同一系列出现两份相互漂移的评测基准地图。
