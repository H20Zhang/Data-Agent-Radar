# Data Agent Radar

**中文** | [English](README.en.md)

*追踪 Agent 如何完成端到端 data work：理解数据、规划分析、执行 query/code/transform、验证结果、恢复错误并交付 artifact。*

**Radar Family：** [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) · [Agent Memory](https://github.com/H20Zhang/Agent-Memory-Radar) · [Agentic RAG](https://github.com/H20Zhang/Agentic-RAG-Radar) · **Data Agent**

[30 秒：最新工作](#latest) · [5 分钟：领域地图](#field-map) · [15 分钟：阅读路径](#reading-paths) · [浏览全部](#library)

> **先建立一个简单模型：** `intent → discover/ground data → plan → query/code/transform → inspect/verify → revise/recover → deliver`
>
> **当前判断：** Data Agent 不应被缩成“会生成 SQL 的 Agent”。真正困难的是把 **business semantics、heterogeneous data、tool execution、intermediate state、verification 与 recovery** 连接成一个可靠闭环。

最后更新：**2026-08-20**

<a id="latest"></a>
## 最新研究信号

### [Polaris: Multi Agentic System for Conversational Enterprise Analytics](https://arxiv.org/abs/2608.14246)
`Planning & Orchestration` · **2026-08-14**

**Research delta.** Polaris 把 enterprise analytics 拆给 querying、visualization、reasoning 等 specialized agents，并用 Dynamic Task Coordination 在线做 agent-task assignment；真正要验证的是 multi-agent coordination 相比更简单的 single-agent + tool routing 到底多带来了什么。

### [Business Truth, not SQL Accuracy: A Rule-Gated 7B Analytics Agent Outperforms a Direct-Prompted 32B Baseline](https://arxiv.org/abs/2608.09254)
`Verification & Reliability` · **2026-08-10**

**Research delta.** 这项工作把“SQL 能执行”与“business meaning 正确”分开，把 clarification、abstention、schema drift 与 deterministic post-execution checks 都纳入 analytics-agent correctness。

<details><summary><strong>约 60 秒理解为什么这件事重要</strong></summary>

Production analytics 的失败经常不是 syntax error，而是两个 business definition 都合理、warehouse 根本回答不了、column 已 deprecated，或者 query 正常执行却返回错误 business number。QueryProof 利用 semantic-layer / physical-catalog rules 决定行为，并在输出前做 deterministic post-execution checks。

论文报告它的 Business Truth Rate 高于一个 direct-prompted 更大模型 baseline，但两边 scaffolding 并不匹配，而且没有 component ablation 单独隔离 deterministic layer。因此更稳的研究结论不是“小模型打赢大模型”，而是：**business-semantic correctness、clarification、abstention、false success 应从 execution match 中单独拿出来测。**

</details>

### [CIPHER: A Decoupled Exploration-Selection Framework for Test-Time Scaling of Data Science Agents](https://arxiv.org/abs/2607.14386)
`Planning & Search` · **2026-07-15**

**Research delta.** CIPHER 不把整个 data-science trajectory 绑死在一个 initial state 上，而是生成多个候选起点，把 exploration 与 selection 分离，再并行执行多个路径。

### [A Semantic-Layer-Mediated Agent for Natural Language to SQL over Heterogeneous Enterprise Databases](https://arxiv.org/abs/2606.31041)
`Semantic Grounding & Execution` · **2026-06-30**

**Research delta.** Agent 不直接对 raw physical schema 生成 SQL，而是在 curated semantic layer 上产生 compact Semantic Model Query，再由 deterministic compiler 负责 physical schema 与 SQL dialect。

<details><summary><strong>约 60 秒理解这个 design point</strong></summary>

直接 NL→SQL over hundreds of physical tables，等于让模型同时解决 business semantic grounding 与 dialect-specific execution。这个设计在两者之间插入 semantic intermediate representation：LLM 组合已经验证过的 business concepts，deterministic code 再把它编译成具体 SQL。

这能提高 grounding，但也把大量系统质量移到了 semantic layer。真正该比较的不是抽象的“semantic layer 好不好”，而是它需要多少 curation cost、coverage 能否跟上、以及 semantic layer 缺失或错误时系统如何退化。

</details>

### [APEX-SQL: Talking to the data via Agentic Exploration for Text-to-SQL](https://arxiv.org/abs/2602.16720)
`Data Discovery & Grounding` · **2026-02-11**

**Research delta.** Schema linking 从静态匹配变成 `hypothesis → data profiling → verification`：Agent 主动查看真实 values / distributions 来验证 column 与 join 假设，再生成 SQL。

### [AgentSM: Semantic Memory for Agentic Text-to-SQL](https://arxiv.org/abs/2601.15709)
`Learning & Reuse` · **2026-01-22**

**Research delta.** 历史 execution traces 被整理成可解释的 semantic programs，作为 database-specific persistent memory，让未来 query 复用 reasoning path，而不是每次从零探索。

<a id="changes"></a>
## 最近真正发生了什么变化

| 变化 | 新证据 | 对研究设计的含义 |
|---|---|---|
| **Semantic grounding 正在前移到 code generation 之前。** | APEX-SQL 主动 profile 数据；semantic-layer agent 先在 business concepts 上规划，再落到 physical SQL。 | 不只看 execution accuracy，要把 exploration / curation cost 一起算。 |
| **Verification 正在变成一等 stage。** | QueryProof 类工作把 business truth、clarification、abstention 与 post-execution checks 从“能执行”里拆出来。 | Data Agent 需要明确什么时候**不应该返回一个数字**。 |
| **Data work 正在变成长时程 control problem。** | CIPHER 搜索多个 initial plan；Polaris 做 multi-agent coordination；AgentSM 复用历史 execution knowledge。 | Planning、intermediate state、recovery、reuse 应与 final artifact 分开测。 |

<a id="field-map"></a>
## 领域地图

`intent → discover/ground → plan → execute/transform → inspect/verify → recover → learn/reuse → deliver`

| Research problem | 核心问题 | 当前张力 |
|---|---|---|
| **Data Discovery & Grounding** | Agent 怎么找到真正相关的 schema、table、file、document、metric 与 business definition？ | `static metadata ↔ active profiling` |
| **Planning & Semantic Interaction** | 用户意图如何变成可执行、可检查的 analytic plan？ | `direct NL→SQL/code ↔ semantic/intermediate plan` |
| **Execution & Transformation** | SQL、Python、notebook、DB/API 与 real-computer actions 怎么组合？ | `single-shot generation ↔ grounded multi-tool execution` |
| **Verification & Recovery** | 一个成功执行的结果什么时候仍然是错的？失败后如何恢复？ | `execution success ↔ business truth / artifact verification` |
| **Learning & Reuse** | 哪些历史 analysis、workflow、skill、memory 值得持续复用？ | `restart from scratch ↔ reusable experience` |

[看 Data Agent 如何被评价 →](https://github.com/H20Zhang/Agent-Benchmark-Radar#data-agents)

<a id="reading-paths"></a>
## 阅读路径

| 你想回答的问题 | 建议顺序 | 应该学到什么 |
|---|---|---|
| **Agent 应如何理解一个 enterprise database？** | APEX-SQL → Semantic-Layer-Mediated Agent → AgentSM | Active profiling、semantic abstraction、database-specific reusable knowledge 分别解决不同 grounding 问题。 |
| **怎么从“能执行”走到“结果可信”？** | QueryProof / Business Truth → Benchmark Radar 的 DataSpace / DSAgentBench | Business semantics、clarification/abstention、artifact verification 与 real-computer execution 会扩展 success contract。 |
| **更多 agentic planning 什么时候有价值？** | CIPHER → Polaris | Test-time plan search 与 multi-agent orchestration 增加 control capacity，但必须用更简单 matched control 隔离收益。 |

<a id="library"></a>
## Research Library

- **[按 problem / research line / year 浏览](library/README.md)**
- [Data Agent evaluation genealogy](https://github.com/H20Zhang/Agent-Benchmark-Radar)

## Scope

高优先级工作应该改变真实 data work 中一个重要 control boundary：data discovery/grounding、semantic planning、multi-tool execution、verification/recovery、workflow learning/reuse、enterprise analytics orchestration。

纯 Text-to-SQL leaderboard paper 如果没有实质性的 agent control、data interaction 或 verification contribution，通常不是这个 Radar 的高优先级条目。

## About

这个 repo 讲 methods、systems 与 research tensions。Data Agent 的 benchmark genealogy、protocol validity、evaluation gaps 统一放在 [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar)，避免 family 内维护两套相互漂移的 benchmark map。
