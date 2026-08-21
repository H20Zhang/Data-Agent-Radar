# Data Agent Radar Schema

`data/papers.json` is the canonical machine-readable registry. Each record represents one resolved public research identity; the bilingual Timeline, rolling periods, Field Map, reading paths, and Library are projections of this state and its paired deep notes.

This adapter follows [Radar Agent Protocol v2](docs/RADAR_AGENT_PROTOCOL.md). Candidate, blocked, retry, scheduler, and validation state stays private; it is never encoded as a public registry status or operational run log.

## Required research fields

Every canonical Data record has:

- `id`, `title`, `published`, `url`, `note_path`, and `status=public`;
- `primary_problem`, using the stable machine vocabulary documented in [`CURATION.md`](CURATION.md);
- integer `importance` from 1 through 5;
- non-empty `research_delta` and `main_caveat`.

`published` preserves the source's public calendar date. ArXiv identities use the canonical `https://arxiv.org/abs/<id>` URL and `papers/<id>.md` note path, with the paired English note derived as `papers/<id>.en.md`.

## All-or-none v2 time and map bundle

Untouched legacy records with none of the following fields remain valid. Once any field is present, all five are required:

- `published_at`;
- `first_seen_at`;
- `radar_published_at`;
- `time_provenance`;
- `map_delta`.

For `native_v2`, all three event times are strict `YYYY-MM-DDTHH:MM:SSZ` UTC timestamps and satisfy `published_at <= first_seen_at <= radar_published_at`. `radar_published_at` cannot predate the family cutover `2026-08-20T00:00:00Z`. The historical `published` date remains the calendar projection of the source event.

For `legacy_unknown`, `published_at` exactly preserves the honest `published` date, both `first_seen_at` and `radar_published_at` are null, and no discovery or Radar-acceptance time is fabricated. Its `map_delta` is restricted to `none | early_signal`; an explicit legacy record never carries a durable map edit.

`map_delta` is one of `none | early_signal | reinforces | revises | splits | retires`. A durable transition belongs only to a changing `native_v2` record. It also uses ordered, unique `map_support_ids`, includes the changing record, and cites at least one independent record with demonstrably earlier effective evidence. An honest earlier `legacy_unknown` record may serve as that historical prior evidence for a later native change; it does not become a durable legacy edit itself.

## Period support-to-direction binding

`direction_keys` is an optional non-empty list of unique lowercase stable tokens. When present it requires the complete v2 bundle. Every canonical record cited by a Data rolling-period direction must carry the direction block's exact `key` in `direction_keys`; proximity in prose or a shared broad problem label is not a binding.

Each visible direction block carries exactly one machine value and one reader-visible witness for: `key`, `state`, ordered `supports`, `confidence`, `implication`, `time_basis`, `non_acceptance`, exact `synthesized`, and `prior`.

As of the versioned 2026-08-21 switch, rolling directions use native Radar-acceptance timing. `new_signal` has exactly one `early_signal` support and `prior=none`; `reinforced` has at least two distinct in-window native supports carrying the same exact direction key plus `prior=field-map`; `revised | splits | retires` have canonical native support plus the same prior Field Map evidence; and `no_material_change` has `supports=none` and `prior=none`.

The legacy-publication adapter remains available only for separately labeled historical context. Every legacy direction has `state=new_signal`, exactly one `legacy_unknown` support whose `direction_keys` contains the block key, support `map_delta=none | early_signal`, and `prior=none`. It never emits `reinforced`, `revised`, `splits`, `retires`, or `no_material_change`, and never edits the durable map. It must visibly use `legacy_publication_date` and **not Radar acceptance**; legacy records never enter the current native rolling windows.
