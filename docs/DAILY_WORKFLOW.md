# Data Agent Daily Workflow v2

This file adapts [`RADAR_AGENT_PROTOCOL.md`](RADAR_AGENT_PROTOCOL.md) to Data Agent research. The scheduled Daily Agent is the editor-in-chief and only writer. Its scheduler prompt should only identify this repository, branch, and these contracts; this file—not the scheduler text—owns research behavior.

## Frozen preflight

Freeze the run context required by the family protocol, then read `CURATION.md`, `COMPACTION.md`, `SCHEMA.md`, `data/papers.json`, the README pair, Library pair, relevant deep notes, and any useful ignored `.radar-private/` state. Verify the remote head and repair canonical/projection drift before discovery. Operational history is never a public repository surface.

The one writing orchestrator may delegate read-only roles. No scout, reader, judge, or reviewer edits files or publishes state.

## Source lanes

Give independent scouts overlapping, bounded windows across primary sources:

1. data agents, data-science agents, analytics agents, and enterprise analytics;
2. agentic Text-to-SQL, database agents, schema discovery, active profiling, and semantic layers;
3. notebooks, code/data transformation, DB/API/OS tools, and real-computer data work;
4. verification, business truth, clarification/abstention, artifact inspection, failure recovery, and workflow reuse;
5. primary repositories, datasets, protocol releases, and version changes attached to candidate papers.

Use overlap to catch late indexing. Bounded historical search is allowed only when an accepted current work exposes a repeatedly cited missing predecessor. Source-lane failures stay in ignored `.radar-private/` traces or ephemeral Agent memory.

## Identity and scope gates

Resolve arXiv/DOI/venue/repository identities and version relationships before scope judgment. Never merge by title similarity. Preserve earliest public `published_at`, actual `first_seen_at`, and actual `radar_published_at`; never substitute the run time for an unknown legacy event.

The Domain Judge applies the canonical problem names in `CURATION.md`. It must identify which part of the data-work loop changes and whether the contribution is a reusable agent control boundary rather than an ordinary Text-to-SQL or code-generation result.

## Full-text evidence record

For every accepted identity, read the full primary paper or equivalent complete protocol evidence and record:

`problem → mechanism → closest simple control → decisive/negative evidence → resource and curation cost → strongest alternative explanation → remaining uncertainty`

Explicitly separate:

- semantic grounding and business definitions;
- planning/intermediate representation;
- SQL/code/tool execution capacity;
- result and artifact verification;
- clarification, abstention, recovery, and error propagation;
- persistent workflow, skill, or execution state.

Executable SQL, code, or a plausible chart is not proof of business-semantic correctness.

## Skeptical audit

Before acceptance, a read-only skeptic checks model, prompt, context, semantic layer, tool interface, harness, retry policy, compute/token/latency budget, synthetic-task construction, and human curation. Multi-agent, search, verification, or memory claims require the simplest matched control capable of testing the named component. If evidence supports only the packaged system, publish only that ceiling.

Blocked full text, unresolved identity, or missing decisive evidence stays private with a retry trigger. There is no public pending, abstract-only, deferred, or blocked list.

## Canonical-to-reader transaction

For accepted work, the sole writer updates in this order:

1. canonical record and time provenance in `data/papers.json`;
2. paired deep note with the full-text evidence record;
3. compact paired Timeline disclosure with Question, Evidence, Caveat, Map, and Links;
4. rolling 7/30-day synthesis when the accepted set changes;
5. prior closed ISO-week or calendar-month digest when a boundary is due;
6. Field Map only when the evidence gate permits;
7. Reading Paths and Library routes only when conceptual navigation changes;
8. private validation, then one atomic commit of accepted public projections.

Timeline has no fixed count. Put every native-v2 entry first, ordered by the full `radar_published_at` timestamp descending (not by day or registry insertion order), then retain the approved legacy compatibility identities in their fixed source-date order under an explicit provenance notice. Timeline and both rolling periods share one exact public synthesis cutoff; a native-v2 Timeline/current-window record must not postdate it.

## Period and map judgment

Rolling periods state the current exact inclusive windows derived from one UTC synthesis cutoff and synthesize canonical records/deep notes inside them. Each period section contains exactly one human-visible date range after HTML comments are removed. Since the 2026-08-21 versioned switch, the public rolling layers use native Radar-acceptance timing and may emit `new_signal`, `reinforced`, `revised`, `splits`, `retires`, or `no_material_change` under the canonical gates, with ordered support identities, `low | medium | high` confidence, and a research-design implication. Similar vocabulary, release counts, or one paper do not establish a trend. Each complete human-visible Markdown block—including indented continuations and attached paragraphs—must not make any `trend` / `趋势` claim when it has fewer than two distinct native supports. The block ends at the next direction item or period-section boundary.

Each visible direction is one compact linked item backed by one `timefirst:direction` block carrying stable `key`, `state`, ordered `supports`, `confidence`, `implication`, `time_basis`, `non_acceptance`, `synthesized`, and `prior`. A block starts only at a human-visible direction list item, continues through indented or standalone attached paragraphs, and ends at the next visible direction or period boundary. Its single machine comment may sit on the heading line or any continuation, including at the trailing edge; a second comment is invalid. Encode implication as `stable-key~bounded-visible-witness`; the witness must occur inside the one scoped implication field in both language projections. Require exactly one scoped human-visible state, support, confidence, implication, time-basis/non-acceptance, synthesis, and prior-map field per item, so contradictory labels or validating asides cannot launder a malformed primary field. Bind these fields only after removing HTML comments; parse the single raw machine comment separately.

The canonical registry uses `direction_keys` as the stable support-to-direction binding. Every period support must carry the direction block's exact `key`; a shared display problem or adjacent prose is insufficient. In a native Radar-acceptance adapter, `reinforced` needs at least two distinct in-window native supports with that same key plus `prior="field-map"` and one visible `#field-map` link. `revised`, `splits`, and `retires` require canonical native support and the same independent prior-map witness; native `new_signal` requires one `early_signal` support and `prior="none"`; `no_material_change` requires `supports="none"` and `prior="none"`. Those gates do not upgrade legacy publication context. Polaris and Business Truth keep their separate keys and remain separate contextual `new_signal` items.

Current rolling layers use `time_basis="radar_published_at"` and visibly say `Radar acceptance`. Each support is an honest `native_v2` record whose full Radar timestamp falls in the stated window and is no later than the exact synthesis cutoff. Every direction states that ISO timestamp and UTC timezone. A separately labeled legacy context layer may still use `time_basis="legacy_publication_date"` and must visibly say `not Radar acceptance`; it cannot enter native membership, become reinforcement, or create a durable map edit.

Assign every accepted record one `map_delta`: `none | early_signal | reinforces | revises | splits | retires`. An explicit `legacy_unknown` record is restricted to `none | early_signal`; it never carries the durable edit. Every durable transition (`reinforces | revises | splits | retires`) belongs to a changing `native_v2` record and carries ordered, unique canonical `map_support_ids` with at least two identities: the changing native record and at least one independent prior-map support whose effective evidence time is demonstrably earlier. Native records use their exact `radar_published_at`; a legacy record may still supply historical prior evidence using only its honest date-level `published_at`. If either side lacks time-of-day precision, same-day order is unknown and cannot pass the gate. For `revises`, `splits`, or `retires`, the earlier independent record must support the prior map claim while the changing record supplies the new claim-level evidence. Preserve the stable map unless this family gate is met.

## Bilingual, validation, and exit

Chinese and English are one semantic transaction. Preserve identity/order, source dates, contracts, evidence scope, strongest caveat, map token, period window, and normalized links. Natural phrasing may differ. Detect stable anchors, Data compatibility aliases, structural Timeline boundaries, and human-visible Timeline field labels only after masking HTML comments without changing raw offsets; then slice the original Markdown so separate semantic comments remain available to the machine contract. Family routes are likewise evaluated only on the human-visible surface.

During the editorial pass, make Chinese prose follow Chinese sentence structure while preserving canonical identifiers. Keep layer-level reading-time navigation, but make every collapsed Timeline summary name its actual research change rather than a generic time promise or repeated label.

Run:

```bash
python -m unittest discover -s tests -v
python scripts/no_public_runs.py
python scripts/validate_reading.py
```

Recheck the frozen remote head immediately before publication. On drift, re-read affected canonical state, render again, validate again, and retry once without force-pushing. A material success is one atomic commit of accepted canonical data and reader projections. Candidate inventories, lane failures, retries, blockers, validation output, and other operational traces stay only in ignored `.radar-private/` or ephemeral Agent memory. If there is no material accepted change or due boundary digest, validate and exit silently without a content commit or notification.
