# Data Agent Radar

**中文优先 · English version is being built in the v1 branch**

*追踪 Agent 如何完成端到端 data work：理解数据、规划分析、执行查询/代码/转换、验证结果、恢复错误并交付 artifact。*

**Radar Family：** [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) · [Agent Memory](https://github.com/H20Zhang/Agent-Memory-Radar) · [Agentic RAG](https://github.com/H20Zhang/Agentic-RAG-Radar) · **Data Agent**

> **先建立一个简单模型：** `intent → discover/ground data → plan → query/code/transform → inspect/verify → revise/recover → deliver`
>
> **当前判断：** Data Agent 不应被缩成“会生成 SQL 的 Agent”。真正困难的是把 **business semantics、heterogeneous data、tool execution、intermediate state、verification 与 recovery** 连接成一个可靠的闭环。

最后更新：**2026-08-20**

## 最新研究信号

### [Polaris: Multi Agentic System for Conversational Enterprise Analytics](https://arxiv.org/abs/2608.14246)
`Planning & Orchestration` · **2026-08-14**

**Research delta.** Polaris 把 enterprise analytics 拆成 specialized agents，并用 Dynamic Task Coordination 在线分配 querying、visualization 与 reasoning 工作；需要继续验证的是多 agent coordination 相比更简单单 agent + tool routing 到底隔离出多少独立收益。

### [Business Truth, not SQL Accuracy: A Rule-Gated 7B Analytics Agent Outperforms a Direct-Prompted 32B Baseline](https://arxiv.org/abs/2608.09254)
`Verification & Reliability` · **2026-08-10**

**Research delta.** 这项工作把“SQL 能执行”与“business meaning 正确”分开，并把 clarification、abstention、schema drift 与 deterministic post-execution checks 放进 analytics-agent correctness。

### [CIPHER: A Decoupled Exploration-Selection Framework for Test-Time Scaling of Data Science Agents](https://arxiv.org/abs/2607.14386)
`Planning & Search` · **2026-07-15**

**Research delta.** CIPHER 不把整个 data-science trajectory 绑死在一个初始思路上，而是并行生成多个 initial states，再把 exploration 与 selection 分离后执行。

### [A Semantic-Layer-Mediated Agent for Natural Language to SQL over Heterogeneous Enterprise Databases](https://arxiv.org/abs/2606.31041)
`Semantic Grounding & Execution` · **2026-06-30**

**Research delta.** Agent 不直接对 raw physical schema 生成 SQL，而是先在 curated semantic layer 上产生 compact Semantic Model Query，再由 deterministic compiler 落到具体 SQL dialect。

### [APEX-SQL: Talking to the data via Agentic Exploration for Text-to-SQL](https://arxiv.org/abs/2602.16720)
`Data Discovery & Grounding` · **2026-02-11**

**Research delta.** Text-to-SQL 从静态 schema linking 转向 hypothesis → profiling → verification：Agent 主动看真实 data distribution 来验证 schema/column 假设。

### [AgentSM: Semantic Memory for Agentic Text-to-SQL](https://arxiv.org/abs/2601.15709)
`Learning & Reuse` · **2026-01-22**

**Research delta.** 把历史 execution traces 压成可解释的 semantic programs，用 persistent semantic memory 复用数据库特定的 reasoning path，而不是每次重新探索。

## 领域地图

`intent → discover / ground → plan → execute / transform → inspect / verify → recover → learn / reuse → deliver`

| Research problem | 核心问题 | 当前张力 |
|---|---|---|
| **Data Discovery & Grounding** | Agent 怎么找到真正相关的 schema、table、file、document、metric 与 business definition？ | `static metadata ↔ active data profiling` |
| **Planning & Semantic Interaction** | 用户意图如何变成可执行、可检查的 analytic plan？ | `direct NL→SQL/code ↔ semantic/intermediate plan` |
| **Execution & Transformation** | SQL、Python、notebook、DB/API 与真实 computer tool 怎么组合？ | `single-shot generation ↔ grounded multi-tool execution` |
| **Verification & Recovery** | 一个成功执行的结果什么时候仍然是错的？失败后怎么恢复？ | `execution success ↔ business truth / artifact verification` |
| **Learning & Reuse** | 历史分析、workflow、skill、memory 什么值得持续复用？ | `restart from scratch ↔ persistent reusable experience` |

## 和 Benchmark Radar 的分工

这个 repo 讲 **methods / systems / research tensions**。Data Agent 的 benchmark genealogy、protocol validity 与 evaluation gaps 统一放在 [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar)；两边互相链接，但不维护两套 benchmark 列表。

## Scope

纳入的工作应覆盖真实 data work 的一个重要控制边界，并且不仅是普通 code generation：例如 data discovery/grounding、semantic planning、multi-tool execution、verification/recovery、workflow learning/reuse、enterprise analytics orchestration。

纯 Text-to-SQL leaderboard paper 如果没有新的 agent control / data interaction / verification contribution，通常不作为高优先级条目。

---

> v1 正在补齐：英文镜像、Research Library、curation/editorial/workflow contract、canonical records 与 daily maintenance。