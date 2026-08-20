# Data Agent Radar Curation Policy

## Scope

Include work when an LLM/agent materially controls one or more stages of **end-to-end data work**:

`intent → discover/ground → plan → execute/transform → inspect/verify → recover → learn/reuse → deliver`

High-priority work should change a reusable method, system boundary, control policy, interface, execution model, verification mechanism, or persistent state. A paper is not included merely because it uses an LLM on a data task.

## Primary research problems

1. **Data Discovery & Grounding** — schema/metadata discovery, active profiling, heterogeneous evidence, business semantics.
2. **Planning & Semantic Interaction** — semantic layers, intermediate plans/representations, query decomposition, analytic intent.
3. **Execution & Transformation** — SQL/Python/notebook/DB/API/OS orchestration and grounded multi-tool execution.
4. **Verification & Recovery** — result/artifact verification, business truth, clarification/abstention, failure diagnosis and recovery.
5. **Learning & Reuse** — database/workspace-specific memory, workflow/skill reuse, experience accumulation and adaptation.

## Inclusion test

For each candidate ask:

- What stage of the data-work loop changes?
- Compared with the strongest simple alternative, what operation/control/state is added?
- Is the evidence end-to-end system-level, or does it isolate the claimed component?
- What resource/curation/tooling cost moved elsewhere?
- What would make the result weaker: semantic-layer incompleteness, harness dependence, tool reliability, hidden business definitions, synthetic data, or evaluation shortcuts?

Plain Text-to-SQL or code-generation leaderboard papers without a substantive agent-control/data-interaction/verification contribution are normally lower priority.

## Relationship with Agent Benchmark Radar

This repo owns **methods, systems, and research tensions**. Agent Benchmark Radar owns Data Agent benchmark genealogy, protocol validity, coverage gaps, and the evolution of the evaluation object.

A benchmark paper may appear here only when it also introduces a method/system contribution necessary to understand the research line. Do not maintain a second independent benchmark map.

## Importance

Separate relevance from importance.

- **5/5:** changes a durable research coordinate or provides unusually strong matched evidence likely to shape future systems.
- **4/5:** strong new design point, causal control, or system result that changes a current research judgment.
- **3/5:** relevant and useful, but evidence/novelty/generalization is narrower.
- **1–2/5:** usually keep out of the primary reader surfaces; may remain in provenance/deferred notes.

## Evidence discipline

Do not credit a component when model, semantic layer, tool interface, harness, prompt, retry policy, or resource budget changes with it. Preserve negative results and cost shifts. Executable SQL/code is not automatically semantically correct; business meaning and artifact verification are separate concerns.
