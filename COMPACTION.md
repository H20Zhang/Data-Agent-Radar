# Compaction and Digest Contract

The Daily Agent owns both rolling reader summaries and immutable closed-period digests. Separate weekly or monthly writers remain disabled.

## Rolling roots

`README.md` and `README.en.md` contain the current inclusive 7-day and 30-day windows. They are replaceable projections of canonical records and deep notes, not an append-only history. Native-v2 membership is based on `radar_published_at`; any legacy migration view must explicitly state its alternative time basis and must not be presented as Radar acceptance chronology.

The 2026-08-21 versioned migration uses structured per-direction metadata with `time_basis="radar_published_at"`, a visible `Radar acceptance` witness, ordered links to canonical supports, `low | medium | high` confidence, a `stable-key~bounded-visible-witness` implication, one exact last-synthesis timestamp plus timezone, and exact prior-map metadata on every direction. Each layer has exactly one visible date range derived from that synthesis cutoff. A direction block starts only at a visible list item and extends through its continuations and attached paragraphs; every scoped visible state, support, confidence, implication, time-basis/acceptance, synthesis, and prior field occurs exactly once. HTML comments are removed before visible validation, while the single machine direction comment may occur on the heading or a continuation and is parsed from the raw block. Native Timeline records and period supports may not exceed the exact cutoff shared with both rolling periods.

Every period support's canonical `direction_keys` contains the block key. Under the native adapter, `new_signal` has exactly one in-window `native_v2` support with `map_delta=early_signal` and `prior=none`; `reinforced` needs at least two same-key native supports and `prior=field-map`; durable revisions need their canonical map delta and the same prior witness; `no_material_change` has zero support and `prior=none`. The separate `legacy_publication_date` adapter remains contextual only and cannot upgrade legacy evidence into reinforcement or a durable map edit.

The synthesizer re-reads the canonical records and their primary-evidence notes inside each window. It never compounds a weekly paragraph into a monthly claim and never infers a trend from release count or shared vocabulary.

## Closed periods

On the first successful run after Monday 00:00 repository-local time, create the previous complete ISO-week digest if its stable identity is absent. On the first successful run of a new month, do the same for the previous complete calendar month. Boundary detection is idempotent: retries update no already-closed digest.

Closed digests are immutable evidence-index snapshots. A correction appends a clearly dated correction record or creates a versioned replacement; it does not silently rewrite prior chronology.

Each digest states:

- exact inclusive range, synthesis time, timezone, and record-time basis;
- accepted support identities and direct links to canonical deep notes;
- `new_signal | reinforced | revised | no_material_change`, confidence, and research-design implication;
- map decision and the evidence that met or failed the map gate;
- explicit `no_material_change` when no accepted evidence changed the period.

## Evidence rule

Closed digests and rolling summaries are navigation products, never sources for later research claims. Every later synthesis returns to canonical records, full-text notes, and primary sources. Candidate queues, blocked items, retries, scheduler state, validation details, and other operational traces remain only in ignored `.radar-private/` or ephemeral Agent memory; no public operational archive is created.
