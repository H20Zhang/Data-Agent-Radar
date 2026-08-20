# Daily Research-Maintenance Workflow

This is the authoritative orchestration contract for Data Agent Radar. The recurring scheduler should stay short and point here.

## Transaction

One run is one idempotent transaction:

`preflight → discover → independent judgment → canonical update → evidence note → research-line update → derive Chinese/English reader surfaces → editorial review → validate → log → notify only if material`

## 1. Preflight

Read `CURATION.md`, `docs/EDITORIAL_STANDARD.md`, the README pair, Research Library pair, canonical data/taxonomy when present, relevant notes, and recent run logs.

Repair reader/canonical drift before adding new work.

## 2. Discovery

Search recent primary sources broadly across data agents, data-science agents, analytics agents, text-to-SQL agents, database agents, semantic layers, enterprise analytics, notebook/computer-use agents, data discovery, data engineering, verification, workflow reuse, and adjacent systems work.

Use overlapping recent windows so late indexing is not missed. Also run bounded historical backfill when a current research line is missing a repeatedly cited predecessor.

## 3. Independent judgment

When supported, separate roles:

- discovery optimizes recall;
- scope/taxonomy judge decides which data-work boundary changes;
- research analyst reads the full paper for high-value work;
- skeptical reviewer challenges matched baselines, business semantics, tool/harness dependence, curation cost, and component attribution;
- editor decides which public surfaces deserve change.

Do not accept papers merely to keep the feed active.

## 4. Canonical-first publication

For accepted work:

`canonical record → evidence note → research-problem/research-line relationship → reader projections`

Preserve source identity, dates, links, mechanism, strongest comparison, decisive evidence, cost, negative results, and the strongest alternative explanation.

## 5. Research Explainer Standard

Current/high-visibility notes must resolve:

`Research delta → Problem → Mechanism → Closest comparison → Decisive evidence → What remains unproven → Field-map consequence → Related reading`

For Data Agents, explicitly separate semantic grounding, planning, tool/execution capacity, verification, recovery, and reusable state.

## 6. Chinese-first bilingual publication

- `README.md` is Simplified Chinese default; `README.en.md` is the full English counterpart.
- Research Library and high-value public narrative are bilingual.
- A material interpretation correction updates both languages in one transaction.
- English is rewritten naturally from the same research judgment.
- Keep paper/model/dataset/metric/SQL/tool/protocol names in canonical English when useful.

## 7. README projection

Reader flow:

`Latest Research Signals → What’s Changing → Field Map → Reading Paths → Research Library → Scope/About`

Latest should remain compact. Importance >=4/5 or field-map-changing work may receive a 60–90 second fold. Do not duplicate paper-note prose.

Field Map changes only when a durable data-work boundary changes. Reading Paths change only when the conceptual route improves.

## 8. Research Library

History must be discoverable by research problem, research line, and year. Time-based digests, when added, are movement views rather than the archive key.

Evaluation genealogy belongs in Agent Benchmark Radar. Cross-link rather than duplicating the benchmark map.

## 9. Editorial review

Apply `docs/EDITORIAL_STANDARD.md` after research judgment is stable. Review neighboring notes together for repeated sentence templates. In Chinese, watch machine-translated syntax and empty discourse markers.

## 10. Validation and log

Validate:

- Chinese default + English counterpart exist and cross-link;
- same current paper identities, primary links, and load-bearing claims across languages;
- Research Library routes resolve;
- domain-method content does not duplicate a benchmark registry;
- no operational internals leak to public surfaces;
- matched-baseline and system-vs-component attribution is explicit for strong claims.

Write one compact `runs/daily/YYYY/MM/DD.md` log when run-history infrastructure exists.

## Notification gate

Notify only for an important new paper, a correction that changes a research conclusion, a meaningful field-map/research-line change, or an exact blocker. Otherwise finish silently.
