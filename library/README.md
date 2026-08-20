# Data Agent Research Library

**中文** | [English](README.en.md) · [返回首页](../README.md)

这里按 research problem 与 research line 找历史工作，不把“本周新增”当成长期 archive。

## 按 Research Problem 浏览

| 问题 | 研究焦点 |
|---|---|
| **Data Discovery & Grounding** | schema linking、metadata、active profiling、heterogeneous evidence discovery、business semantics |
| **Planning & Semantic Interaction** | semantic layer、intermediate representation、analytic plan、query decomposition |
| **Execution & Transformation** | SQL / Python / notebook / DB / API / OS tool orchestration |
| **Verification & Recovery** | business truth、artifact validation、clarification/abstention、failure recovery |
| **Learning & Reuse** | database-specific memory、workflow/skill reuse、experience accumulation |

## 按 Research Line 浏览

### 1. Static schema → active profiling → semantic layer

[APEX-SQL](https://arxiv.org/abs/2602.16720) → [Semantic-Layer-Mediated Agent](https://arxiv.org/abs/2606.31041)

**带走的结论：** enterprise data grounding 不只是 schema matching。一个方向让 agent 主动看真实 data distribution 验证假设；另一个方向把 physical schema 隔离在 semantic intermediate representation 之后。

### 2. Execute successfully → verify business truth

[Business Truth / QueryProof](https://arxiv.org/abs/2608.09254) → [DataSpace](https://arxiv.org/abs/2608.03451) / [DSAgentBench](https://arxiv.org/abs/2608.10366)（evaluation 在 Benchmark Radar）

**带走的结论：** execution success 只是最低门槛。Data Agent 还要处理 business-definition ambiguity、unanswerable questions、artifact verification、OS/tool grounding 与 false success。

### 3. One-shot plan → plan search / orchestration → reusable experience

[CIPHER](https://arxiv.org/abs/2607.14386) → [Polaris](https://arxiv.org/abs/2608.14246) → [AgentSM](https://arxiv.org/abs/2601.15709)

**带走的结论：** long-horizon data work 的 control capacity 可以来自 test-time search、specialized-agent orchestration 或 persistent reusable memory；三者应该用更简单 matched controls 分别验证。

## 按年份浏览

- **2026：** 当前重点包括 enterprise grounding、verification、test-time planning、multi-agent analytics 与 reusable semantic memory。
- **2025 及更早：** 作为 foundation/precursor 的 text-to-SQL、data-science code 与 early data-agent systems 会在后续 backfill 中按 research line 补齐，而不是按月份堆列表。

## Evaluation

Data Agent 的 benchmark genealogy、protocol/confounder、measurement gaps 统一在 [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar) 维护。这个 Library 只维护 methods/systems research line，避免同一 benchmark 在两个 repo 被独立解释。
