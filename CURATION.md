# Data Agent Radar Curation Policy

## Maintenance authority

The scheduled Daily Agent is the normal editor and only writer. It completes discovery, identity resolution, full-text reading, skeptical review, canonical update, bilingual projection, validation, and publication as one transaction under `docs/RADAR_AGENT_PROTOCOL.md`. Human approval is not a routine gate. Read-only research roles may disagree, but candidates and maintenance state remain only in ignored `.radar-private/` or ephemeral Agent memory; the writing orchestrator resolves the evidence ceiling. Public maintenance output is accepted research projections plus one atomic Git commit, never operational history.

## Scope

Include work when an LLM/agent materially controls one or more stages of **end-to-end data work**:

`intent → discover/ground → plan → execute/transform → inspect/verify → recover → learn/reuse → deliver`

High-priority work should change a reusable method, system boundary, control policy, interface, execution model, verification mechanism, or persistent state. A paper is not included merely because it uses an LLM on a data task.

## Canonical problem names

1. **Data Discovery & Grounding** — schema/metadata discovery, active profiling, heterogeneous evidence, business semantics.
2. **Planning & Semantic Interaction** — semantic layers, intermediate plans/representations, query decomposition, analytic intent.
3. **Execution & Transformation** — SQL/Python/notebook/DB/API/OS orchestration and grounded multi-tool execution.
4. **Verification & Recovery** — result/artifact verification, business truth, clarification/abstention, failure diagnosis and recovery.
5. **Learning & Reuse** — database/workspace-specific memory, workflow/skill reuse, experience accumulation and adaptation.

Use these five display names exactly in the stable Field Map. Existing registry machine keys remain stable and map upward: `data_discovery_grounding` → Data Discovery & Grounding; `planning_orchestration` and `planning_semantic_interaction` → Planning & Semantic Interaction; `verification_recovery` → Verification & Recovery; `learning_reuse` → Learning & Reuse. New subproblems may be described inside a note, but adding, splitting, renaming, or retiring a durable map node requires the protocol's `map_delta` gate. Planning/orchestration work that mainly coordinates tools stays under Planning & Semantic Interaction or Execution & Transformation according to its decisive boundary; architecture alone does not create a “Multi-Agent” problem.

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
- **1–2/5:** keep out of public reader surfaces; any exclusion rationale remains in private run state.

## Evidence discipline

Do not credit a component when model, semantic layer, tool interface, harness, prompt, retry policy, or resource budget changes with it. Preserve negative results and cost shifts. Executable SQL/code is not automatically semantically correct; business meaning and artifact verification are separate concerns.

One accepted work may be an `early_signal` but cannot by itself be called a trend or durable reinforcement. Multi-agent claims require a matched simpler controller; verification claims require separation of business truth from execution; reuse claims require drift and invalidation analysis.

Period support is bound through canonical `direction_keys`, not by a shared Field Map label or editorial proximity. Every support cited under direction key `K` carries `K`. Under native Radar-acceptance timing, a `reinforced` direction requires at least two distinct in-window native same-key supports plus independently linked prior Field Map evidence; `revised`, `splits`, and `retires` require canonical native support and the same prior-map witness. The current `legacy_publication_date` adapter cannot use those durable states: each block is contextual `new_signal` only, cites exactly one same-key `legacy_unknown` record with `map_delta=none | early_signal`, and uses `prior=none`. Polaris and Business Truth therefore stay separate and cannot be combined into reinforcement even if an editor gives them a shared key or prior-map link.

For every durable `map_delta` transition (`reinforces`, `revises`, `splits`, or `retires`), the changing canonical record is `native_v2` and names its evidence set in `map_support_ids`. The list is ordered, unique, resolves to canonical records, contains at least two identities, includes the changing native record, and includes at least one independent prior-map support with demonstrably earlier effective evidence. Use exact `radar_published_at` for native records and honest date-level `published_at` for a legacy record used only as historical prior evidence; never fabricate same-day ordering when either record lacks time-of-day precision. A later or chronologically indeterminate `early_signal` is not prior-map support. For `revises`, `splits`, and `retires`, preserve the earlier prior-map claim and the changing/new claim as separately attributable support.
