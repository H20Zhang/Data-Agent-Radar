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
| **Learning & Reuse** | 数据库专属记忆、工作流/技能复用、经验积累 |

## 按研究路线浏览

### 1. 静态数据库模式 → 主动数据分析 → 语义层

[APEX-SQL](../papers/2602.16720.md) → [Semantic-Layer-Mediated Agent](../papers/2606.31041.md)

企业数据对齐不只是数据库模式匹配。APEX-SQL 让 Agent 主动检查真实的数据分布来验证假设；Semantic-Layer-Mediated Agent 则用语义中间表示隔离物理数据库模式。

### 2. 成功执行 → 验证业务真实性

[SkillEffect](../papers/2608.17007.md) → [StagedWorkspace](../papers/2608.18050.md) → [Business Truth / QueryProof](../papers/2608.09254.md) → [DataSpace](https://github.com/H20Zhang/Agent-Benchmark-Radar/blob/main/benchmarks/dataspace.md) / [DSAgentBench](https://github.com/H20Zhang/Agent-Benchmark-Radar/blob/main/benchmarks/dsagentbench.md)（评测分析见 Benchmark Radar）

查询或代码能够执行只是最低门槛。SkillEffect 检查工具阶段的资源义务，StagedWorkspace 让解析视图、原生文件与 diff 共享工作区边界；Data Agent 仍需继续处理业务定义歧义、无法回答的问题、产物验证与虚假成功。

### 3. 单次规划 → 规划搜索/编排 → 可复用经验

[CIPHER](../papers/2607.14386.md) → [Polaris](https://arxiv.org/abs/2608.14246) → [AgentSM](../papers/2601.15709.md)

长时程数据工作的控制能力可以来自测试时搜索、专用 Agent 编排或持久化可复用记忆；它们各自的收益都需要用更简单、条件匹配的对照系统分别验证。

### 4. 受检降层与准入 → 解析/原生双视图 → 分阶段审阅与发布

[SkillEffect](../papers/2608.17007.md) → [StagedWorkspace](../papers/2608.18050.md)

这条路径连接资源受限执行与持久产物状态，但不是经验上的因果链：前者依赖人工审计的关系插件，后者的匹配实验只隔离双视图访问，没有隔离哈希同步本身。

## 按年份浏览

- **2026：** 当前重点包括企业数据对齐、验证、测试时规划、多 Agent 分析和可复用语义记忆。
- **2025 及更早：** 后续将沿研究路线补充作为基础或先驱的 Text-to-SQL、数据科学代码和早期 Data Agent 系统，而不是按月份堆叠列表。

## 与评测仓库的分工

Data Agent 评测基准的演进脉络、评测协议、混杂因素和评测缺口统一由 [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) 维护。本库只维护方法与系统的研究路线，避免同一个评测基准在两个仓库中被分别解释。
