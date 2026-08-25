# Data Agent Research Library

[中文](README.md) | **English** · [Home](../README.en.md)

Papers are organized by research problem, research line, and year; “new this week” is not a long-term archive key.

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

[APEX-SQL](../papers/2602.16720.en.md) → [Semantic-Layer-Mediated Agent](../papers/2606.31041.en.md)

Enterprise data grounding is more than schema matching. APEX-SQL lets the agent inspect real data distributions to verify hypotheses; the Semantic-Layer-Mediated Agent hides physical schema behind a semantic intermediate representation.

### 2. Execute successfully → verify business truth

[SkillEffect](../papers/2608.17007.en.md) → [StagedWorkspace](../papers/2608.18050.en.md) → [Business Truth / QueryProof](../papers/2608.09254.en.md) → [DataSpace](https://github.com/H20Zhang/Agent-Benchmark-Radar) / [DSAgentBench](https://github.com/H20Zhang/Agent-Benchmark-Radar) (protocol audits live in Benchmark Radar)

Query or code execution is only a floor. SkillEffect checks tool-stage resource obligations; StagedWorkspace places parsed views, native files, and diffs on a workspace boundary. Data agents must still handle business-definition ambiguity, unanswerable questions, artifact verification, and false success.

### 3. One-shot plan → plan search / orchestration → reusable experience

[CIPHER](../papers/2607.14386.en.md) → [Polaris](https://arxiv.org/abs/2608.14246) → [VAT decomposition](../papers/2608.23395.en.md) → [AgentSM](../papers/2601.15709.en.md)

Long-horizon data work can gain control capacity from test-time search, specialized-agent orchestration, dependency-layer partitioning, or persistent memory. The VAT pilot's negative result shows why a higher intermediate point estimate still needs budget, multiple-testing, and fault-timing controls before decomposition receives causal credit.

### 4. Checked lowering and admission → parsed/native dual view → staged review and publication

[SkillEffect](../papers/2608.17007.en.md) → [StagedWorkspace](../papers/2608.18050.en.md)

This path connects resource-bounded execution to persistent artifact state, but it is not an empirical causal chain. The first requires manually audited relation plugins; the second isolates dual-view access, not hash synchronization itself.

### 5. Dataset interface → traced computational campaign → scientific claim review

[Scientific Data Skills](../papers/2608.19625.en.md) → [MAESTRO](../papers/2608.20434.en.md) → [Brain Researcher](../papers/2608.19902.en.md)

A dataset snapshot, computational state, and final claim are distinct boundaries. SciDSK organizes dataset semantics and operating guidance; MAESTRO connects large-scale deterministic scientific tools; Brain Researcher keeps execution artifacts subject to method and claim-scope review.

### 6. Runnable → artifact structure → replayable evidence → authorized publication

[Bolo](../papers/2608.20525.en.md) → [Artic](../papers/2608.21341.en.md) → [KDAF](../papers/2608.20661.en.md) → [TRACE](../papers/2608.20844.en.md)

The four works respectively check inference dataflow, explicit workflow artifacts, enterprise evidence chains, and a production catalog write gate. Together they separate execution, artifacts, provenance, and business truth, but distinct direction keys and controls prevent a reinforced claim.

## Browse by Year

- **2026:** current emphasis includes enterprise grounding, versioned dataset interfaces, explicit artifact control, verification/publication gates, test-time planning, multi-agent analytics, and reusable semantic memory.
- **2025 and earlier:** foundational Text-to-SQL, data-science code, and early data-agent systems will be backfilled along research lines rather than as a month-by-month dump.

## Evaluation ownership

Data Agent benchmark genealogy, protocol/confounder analysis, and measurement gaps live in [Agent Benchmark Radar](https://github.com/H20Zhang/Agent-Benchmark-Radar). This library tracks methods/systems research lines so the family does not independently interpret the same benchmark in two repositories.
