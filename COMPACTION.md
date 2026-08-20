# Compaction and Digest Contract

The Daily Agent owns both rolling reader summaries and immutable closed-period digests. Separate weekly or monthly writers remain disabled.

## Rolling roots

`README.md` and `README.en.md` contain the current inclusive 7-day and 30-day windows. They are replaceable projections of canonical records and deep notes, not an append-only history. Native-v2 membership is based on `radar_published_at`; any legacy migration view must explicitly state its alternative time basis and must not be presented as Radar acceptance chronology.

The current migration uses structured per-direction metadata with `time_basis="legacy_publication_date"`, a visible `not Radar acceptance` witness, ordered links to canonical supports, `low | medium | high` confidence, a `stable-key~bounded-visible-witness` implication, one exact last-synthesis timestamp plus timezone, and exact prior-map metadata on every direction. Each layer has exactly one visible date range. A direction block starts only at a visible list item and extends through its continuations and attached paragraphs; every scoped visible state, support, confidence, implication, time-basis/non-acceptance, synthesis, and prior field occurs exactly once. HTML comments are removed before visible validation, while the single machine direction comment may occur on the heading or a continuation and is parsed from the raw block. Legacy supports may not postdate synthesis at available date precision; native Timeline records may not exceed the exact cutoff shared with both rolling periods. Replacing the time basis requires an explicit versioned migration after native-v2 history exists.

Every period support's canonical `direction_keys` contains the block key. The current `legacy_publication_date` adapter emits only contextual `new_signal`: each block has exactly one `legacy_unknown` support with `map_delta=none | early_signal` and `prior=none`. It cannot emit `reinforced`, `revised`, `splits`, `retires`, or `no_material_change`, regardless of support count or a Field Map link. Polaris and Business Truth retain separate keys and separate `new_signal` blocks. Native durable direction and no-change states begin only after an explicit versioned switch to Radar-acceptance timing.

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
