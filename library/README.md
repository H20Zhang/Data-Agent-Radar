# Data Agent 研究文献库

**中文** | [English](README.en.md) · [返回首页](../README.md)

文献按研究问题、研究路线和年份组织；“本周新增”不作为长期归档方式。

## 按研究问题浏览

| 问题 | 研究焦点 |
|---|---|
| **Data Discovery & Grounding** | 数据库模式关联、元数据、主动数据分析、异构证据发现、业务语义 |
| **Planning & Semantic Interaction** | 语义层、中间表示、分析计划、查询分解 |
| **Execution & Transformation** | SQL / Python / 计算笔记本 / 数据库 / API / 操作系统工具编排 |
| **Verification & Recovery** | 业务真实性、产物验证、澄清/拒答、失败恢复 |
| **Learning & Reuse** | 数据库专属记忆、工作流/技能复用、经验积累、跨查询共享结构 |

## 按研究路线浏览

### 1. 静态数据库模式 → 主动探查 → typed query control → 语义层

[APEX-SQL](../papers/2602.16720.md) → [ReAct-SQL](../papers/2608.22651.md) → [Semantic-Layer-Mediated Agent](../papers/2606.31041.md)

企业数据对齐不只是数据库模式匹配。APEX-SQL 让 Agent 主动检查真实数据来验证 schema 假设；ReAct-SQL 进一步用 matched ablation 把 **probe policy** 与 **typed relational representation** 拆开，显示 grounding 与 composition 的主要瓶颈会随 workload 改变；Semantic-Layer-Mediated Agent 则把业务概念放进更重的语义中间层。三者对应不同控制边界，不能简单解释为“结构越多越好”。

### 2. 成功执行 → 验证业务真实性

[SkillEffect](../papers/2608.17007.md) → [StagedWorkspace](../papers/2608.18050.md) → [Business Truth / QueryProof](../papers/2608.09254.md) → [DataSpace](https://github.com/H20Zhang/Agent-Benchmark-Radar/blob/main/benchmarks/dataspace.md) / [DSAgentBench](https://github.com/H20Zhang/Agent-Benchmark-Radar/blob/main/benchmarks/dsagentbench.md)（评测分析见 Benchmark Radar）

查询或代码能够执行只是最低门槛。SkillEffect 检查工具阶段的资源义务，StagedWorkspace 让解析视图、原生文件与 diff 共享工作区边界；Data Agent 仍需继续处理业务定义歧义、无法回答的问题、产物验证与虚假成功。

### 3. 单次规划 → 规划搜索/编排 → 可复用经验

[CIPHER](../papers/2607.14386.md) → [Polaris](https://arxiv.org/abs/2608.14246) → [VAT decomposition](../papers/2608.23395.md) → [AgentSM](../papers/2601.15709.md)

长时程数据工作的控制能力可以来自测试时搜索、专用 Agent 编排、依赖层分区或持久化记忆。VAT pilot 的负面结果强调：即使中间粒度点估计最高，也必须先排除预算、multiple testing 与故障注入时序，才能把收益归因给分工。

### 4. 受检降层与准入 → 解析/原生双视图 → 分阶段审阅与发布

[SkillEffect](../papers/2608.17007.md) → [StagedWorkspace](../papers/2608.18050.md)

这条路径连接资源受限执行与持久产物状态，但不是经验上的因果链：前者依赖人工审计的关系插件，后者的匹配实验只隔离双视图访问，没有隔离哈希同步本身。

### 5. 数据集接口 → 可追踪计算 campaign → 科学主张审查

[Scientific Data Skills](../papers/2608.19625.md) → [MAESTRO](../papers/2608.20434.md) → [Brain Researcher](../papers/2608.19902.md)

数据集快照、计算状态和最终主张是三个不同边界。SciDSK 组织数据集语义与使用指导；MAESTRO 连接大规模确定性科学工具；Brain Researcher 让执行产物继续接受方法与主张范围审查。

### 6. 能运行 → 产物有结构 → 证据可回放 → 答案可复现 → 获准发布

[Bolo](../papers/2608.20525.md) → [Artic](../papers/2608.21341.md) → [KDAF](../papers/2608.20661.md) → [BLIP](../papers/2608.25210.md) → [TRACE](../papers/2608.20844.md)

这条路径拆分五个不同 gate：inference dataflow、显式 workflow artifact、企业来源链、可执行的 answer-reproduction provenance、生产写入授权。BLIP 比 relevance-style provenance 多了一个“删掉其余输入后还能否复现答案”的检查，但仍不证明答案正确或业务真实；五项工作的方向键与控制条件不同，不能合并成强化结论。

### 7. 每次重读原文 → workload-adaptive structure → 持久复用

[Agentic Data Cracking](../papers/2608.31082.md) → [AgentSM](../papers/2601.15709.md)

两者都让后续请求继承历史状态，但复用对象不同。Agentic Data Cracking 把已经打开的非结构化文档逐步物化为共享的 evidence-backed data structure；AgentSM 复用的是 database-specific execution semantic programs。前者的关键未知量是 query locality、demand-only cache 对照与 corpus invalidation，后者则主要面对 schema / workload drift。它们说明“记忆”不是一个组件名，而是不同 persistent state 的生命周期问题。

## 按年份浏览

- **2026：** 当前重点包括企业数据对齐、主动数据库探查、typed query control、版本化数据集接口、workload-adaptive structured reuse、显式产物控制、可验证 provenance、验证/发布门槛、测试时规划、多 Agent 分析和可复用语义记忆。
- **2025 及更早：** 后续将沿研究路线补充作为基础或先驱的 Text-to-SQL、数据科学代码和早期 Data Agent 系统，而不是按月份堆叠列表。

## 与评测仓库的分工

Data Agent 评测基准的演进脉络、评测协议、混杂因素和评测缺口统一由 [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) 维护。本库只维护方法与系统的研究路线，避免同一个评测基准在两个仓库中被分别解释。
