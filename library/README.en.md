# Data Agent Research Library

[中文](README.md) | **English** · [Home](../README.en.md)

Use this library to find old work by research problem and design line rather than by week.

## Browse by Research Problem

| Problem | Research focus |
|---|---|
| **Data Discovery & Grounding** | schema linking, metadata, active profiling, heterogeneous evidence discovery, business semantics |
| **Planning & Semantic Interaction** | semantic layers, intermediate representations, analytic plans, query decomposition |
| **Execution & Transformation** | SQL / Python / notebook / DB / API / OS tool orchestration |
| **Verification & Recovery** | business truth, artifact validation, clarification/abstention, failure recovery |
| **Learning & Reuse** | database-specific memory, workflow/skill reuse, accumulated experience |

## Browse by Research Line

### 1. Static schema → active profiling → semantic layer

[APEX-SQL](https://arxiv.org/abs/2602.16720) → [Semantic-Layer-Mediated Agent](https://arxiv.org/abs/2606.31041)

**Takeaway:** enterprise data grounding is more than schema matching. One direction lets the agent inspect real data distributions to verify hypotheses; another hides physical schema behind a semantic intermediate representation.

### 2. Execute successfully → verify business truth

[Business Truth / QueryProof](https://arxiv.org/abs/2608.09254) → [DataSpace](https://arxiv.org/abs/2608.03451) / [DSAgentBench](https://arxiv.org/abs/2608.10366) (evaluation lives in Benchmark Radar)

**Takeaway:** execution success is only a floor. Data agents must also handle business-definition ambiguity, unanswerable questions, artifact verification, OS/tool grounding, and false success.

### 3. One-shot plan → plan search / orchestration → reusable experience

[CIPHER](https://arxiv.org/abs/2607.14386) → [Polaris](https://arxiv.org/abs/2608.14246) → [AgentSM](https://arxiv.org/abs/2601.15709)

**Takeaway:** long-horizon data work can gain control capacity from test-time search, specialized-agent orchestration, or persistent reusable memory. These should be tested against simpler matched controls separately.

## Browse by Year

- **2026:** current emphasis includes enterprise grounding, verification, test-time planning, multi-agent analytics, and reusable semantic memory.
- **2025 and earlier:** foundational Text-to-SQL, data-science code, and early data-agent systems will be backfilled along research lines rather than as a month-by-month dump.

## Evaluation

Data Agent benchmark genealogy, protocol/confounder analysis, and measurement gaps live in [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar). This library tracks methods/systems research lines so the family does not independently interpret the same benchmark in two repositories.
