# Research Radar Editorial Standard

This is the prose contract for reader-facing Data Agent Radar content.

## Reasoning contract

Before drafting a high-value paper explanation, settle:

1. **Research delta** — `previous design → changed variable → consequence`.
2. **Problem** — what still fails in the strongest reasonable existing data workflow?
3. **Mechanism** — actual data/control/tool flow.
4. **Closest comparison** — what is held fixed and what still changes together?
5. **Decisive evidence** — which 1–3 results should update belief?
6. **What remains unproven** — strongest alternative explanation, semantic-layer/tool/harness mismatch, or cost moved elsewhere.
7. **Field-map consequence** — which data-work boundary changes?

For Data Agents, explicitly ask whether the claimed gain comes from **better semantics, better planning, more tools, more test-time search, stronger verification, persistent memory, or a different harness**.

## Chinese-first bilingual rule

`README.md` is Simplified Chinese default; `README.en.md` is the complete English counterpart. Public bilingual prose derives from one semantic research judgment.

Keep paper titles, datasets, models, metrics, SQL/tool/protocol names, and established technical terms in English when that improves precision/search.

Chinese sentences should otherwise use Chinese syntax and connective structure. Do not preserve English clause order and replace only individual words.

## Public entry surfaces

- Lead with the current Timeline and the research map readers came for; keep the layer-level time budgets because they explain the depth of each route.
- Write collapsed Timeline summaries and research-line conclusions as direct, content-specific prose. Do not wrap every item in generic `Research delta`, `Takeaway`, or `带走的结论` labels.
- Keep inline expansion when comparison, evidence, mechanism, or caveat would otherwise overload the scan layer. Its summary names the finding rather than promising a reading time.
- Preserve paper, benchmark, dataset, model, metric, and standard acronym names. Translate surrounding grammar instead of translating identifiers.

## Preferred prose

- Explain the business/data problem before agent jargon.
- Name concrete operations: profile values, inspect schema, compile semantic plan, execute SQL, run notebook, validate artifact, abstain, retry, recover.
- Distinguish **execution correctness** from **business-semantic correctness**.
- Compare before evaluating.
- State when a system result changes several things at once.
- Charge exploration, semantic-layer curation, test-time branches, tool calls, and verification cost when discussing efficiency.
- Keep clarification/abstention and negative results visible.

## AI-house-style patterns to avoid

Warn on repeated sentence skeletons and generic transitions:

- `真正重要的不是 X，而是 Y`, `关键在于…`, `值得注意的是…` used across many notes;
- `this matters because…`, `the key insight is…`, `the important delta…` repeated mechanically;
- generic praise (`robust`, `comprehensive`, `novel`, `重要`, `强大`) without matched comparison/evidence;
- forced three-part symmetry;
- abstract “agent framework” language where a concrete data/tool flow can be named;
- claims that a smaller model “beats” a larger one when scaffolding/harness is unmatched.

Detect pattern density, not banned vocabulary.

## README fold contract

A README fold should explain the surviving data-work problem, actual control/data flow, closest comparison, decisive evidence, and strongest caveat without duplicating the full deep note.

## Epistemic language

- fact: `论文报告…` / `the paper reports…`;
- curator interpretation: `这个结果更支持 verification package，而不是单独证明 routing`;
- open hypothesis: `下一步最有判别力的实验是 semantic-layer completeness / tool reliability / cost-matched control…`.
