# Data Agent Radar v1 Design

Date: 2026-08-20

## Problem statement

Data-agent research spans Text-to-SQL, data-science automation, enterprise analytics, computer-use agents, semantic layers, multi-tool execution, and workflow memory. A useful radar needs a tighter organizing object than “anything that uses an LLM on data.”

This repository treats a Data Agent as a system that controls meaningful stages of end-to-end data work:

`intent → discover/ground data → plan → query/code/transform → inspect/verify → recover → learn/reuse → deliver artifact`

Scope: methods, systems, and research tensions across that loop. Benchmark genealogy and evaluation-object evolution live in Agent Benchmark Radar.

Non-goals: exhaustive Text-to-SQL paper listing; duplicate benchmark registry; product catalog; GitHub Pages/frontend.

## Reading architecture

Chinese-first bilingual projections:

```text
research record
  ├─ README scan
  ├─ README fold for high-value work
  ├─ evidence note when decision value warrants it
  ├─ Research Library / research line
  └─ temporal synthesis when the corpus becomes large enough
```

`README.md` is Simplified Chinese default; `README.en.md` is full English.

## Field Map

1. **Data Discovery & Grounding** — schema/metadata discovery, active profiling, heterogeneous evidence, business semantics.
2. **Planning & Semantic Interaction** — semantic layer/intermediate representation, analytic plan, decomposition.
3. **Execution & Transformation** — SQL/Python/notebook/DB/API/OS tool orchestration.
4. **Verification & Recovery** — artifact validation, business truth, clarification/abstention, diagnosis/recovery.
5. **Learning & Reuse** — database/workspace-specific memory, workflow/skill reuse, accumulated experience.

These are control boundaries, not mutually exclusive application categories.

## Core research tensions

- `static metadata ↔ active profiling`
- `direct NL→SQL/code ↔ semantic/intermediate plan`
- `single-shot generation ↔ grounded multi-tool execution`
- `execution success ↔ business truth / artifact verification`
- `restart from scratch ↔ persistent reusable experience`

## Research Explainer Standard

For high-value work:

`Research delta → Problem → Mechanism → Closest comparison → Decisive evidence → What remains unproven → Field-map consequence → Related reading`

Strong analysis must identify whether a gain comes from semantic grounding, planning, more tools, test-time search, stronger verification, persistent memory, or a changed harness—and whether those variables were isolated.

## Relationship with Benchmark Radar

Agent Benchmark Radar is the family entry/evaluation layer. Its Data Agent map explains how evaluation evolved from executable NL→SQL/code toward workflows, heterogeneous analytics, and real-computer end-to-end work.

Data-Agent-Radar links to that evaluation map, but owns methods/systems only. A benchmark paper appears here only if it also contributes a method/system necessary for a research line.

## Initial research lines

- **Grounding:** APEX-SQL → Semantic-Layer-Mediated Agent → AgentSM.
- **Reliability:** execution accuracy → business truth / clarification / abstention → heterogeneous artifact verification.
- **Control capacity:** one-shot plan → CIPHER-style test-time plan search → Polaris-style orchestration → reusable experience.

## Maintenance

Recurring maintenance uses `docs/DAILY_WORKFLOW.md`; scheduler stays thin. Future canonical data should support source identity, taxonomy, importance, evidence state, links, and research-line membership without turning README into the database.

## Success criteria

A reader should be able to:

- understand the Data Agent loop in under a minute;
- see the highest-signal current methods without reading a survey;
- distinguish semantic grounding, planning, execution, verification, recovery, and reuse;
- find older work by research line rather than week;
- jump to Benchmark Radar for evaluation genealogy;
- read Chinese by default and switch to a complete English counterpart.
