# Data Agent Radar Time-First v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give Data Agent Radar the same compact Timeline, inline evidence depth, period synthesis, and autonomous Daily Agent contract as the mature domain radars.

**Architecture:** Preserve the small canonical registry and current field map, but complete the missing evidence layer for all six visible works. Reuse the family protocol/parser, add honest legacy time metadata, a Data-specific workflow/compaction contract, and deterministic reader/registry validation.

**Tech Stack:** Markdown, Python 3.12 standard library, `unittest`, JSON, GitHub Actions.

**Spec:** `https://github.com/H20Zhang/Agent-Benchmark-Radar/blob/main/docs/superpowers/specs/2026-08-20-agent-maintained-time-first-radar-v2-design.md`

## Global Constraints

- Daily Scheduled Agent is the only writer; no public candidate queue or normal human gate.
- Public order is `Latest Timeline → 7-day / 30-day synthesis → Field Map → Reading Paths → Library`.
- Timeline has no fixed cap; all current records are compact inline disclosures with Question, Evidence, Caveat, Map, and Links.
- Do not fabricate historic discovery/Radar-publication times; represent unknown legacy values as null with provenance.
- Data Agent claims separate semantic grounding, planning, execution/tooling, verification/recovery, and reusable state.
- Executable SQL/code is not sufficient evidence of business-semantic correctness.
- A single work may be `early_signal`; durable map changes require independent support.
- Preserve the methods/systems versus Benchmark-genealogy boundary and bilingual semantic parity.

---

### Task 1: Apply the v2 family contract and complete Data's evidence layer

**Files:**
- Create: `docs/RADAR_AGENT_PROTOCOL.md`
- Modify: `docs/DAILY_WORKFLOW.md`
- Modify: `CURATION.md`
- Create: `COMPACTION.md`
- Create: `digests/README.md`
- Modify: `data/papers.json`
- Modify: `README.md`
- Modify: `README.en.md`
- Create: `papers/2608.14246.md`
- Create: `papers/2608.14246.en.md`
- Create: `scripts/timefirst_contract.py`
- Create: `tests/test_timefirst_contract.py`
- Modify: `scripts/validate_reading.py`
- Modify: `.github/workflows/validate.yml`

**Interfaces:**
- Consumes verbatim: shared protocol, parser, and generic fixtures from merged Benchmark v2.
- Adds `validate_registry(records: list[dict[str, object]]) -> list[str]` in `scripts/validate_reading.py`.
- Stable anchors: `timeline`, `latest`, `periods`, `changes`, `last-7-days`, `last-30-days`, `field-map`, `reading-paths`, `library`.
- Routes evaluation intent to `Agent-Benchmark-Radar#benchmark-data`.

- [ ] **Step 1: Write/copy failing behavior tests**

Copy the merged Benchmark parser and generic fixtures. Add real repository and Data time-contract tests:

```python
from validate_reading import validate_registry

def test_repository_readmes_satisfy_contract(self):
    self.assertEqual([], validate_pair(
        (ROOT / "README.md").read_text(encoding="utf-8"),
        (ROOT / "README.en.md").read_text(encoding="utf-8"),
    ))

def test_legacy_unknown_times_are_explicit_not_fabricated(self):
    record = {
        "id": "legacy", "title": "Legacy", "published": "2026-01-01",
        "published_at": "2026-01-01", "first_seen_at": None,
        "radar_published_at": None, "time_provenance": "legacy_unknown",
        "map_delta": "early_signal"
    }
    self.assertEqual([], validate_registry([record]))

def test_native_v2_record_requires_all_three_times(self):
    record = {
        "id": "new", "title": "New", "published": "2026-08-20",
        "published_at": "2026-08-20", "first_seen_at": None,
        "radar_published_at": "2026-08-20T03:00:00Z",
        "time_provenance": "native_v2", "map_delta": "early_signal"
    }
    self.assertTrue(any("first_seen_at" in error for error in validate_registry([record])))
```

Run: `python -m unittest discover -s tests -v`

Expected: import/contract failures because the shared parser and `validate_registry` do not yet exist and the README is not time-first.

- [ ] **Step 2: Migrate the six legacy registry records honestly**

For each existing record, retain `published` and add:

```json
"published_at": "<same existing publication date>",
"first_seen_at": null,
"radar_published_at": null,
"time_provenance": "legacy_unknown",
"map_delta": "early_signal"
```

Do not invent a migration-day timestamp. Add the local note path for each record where the registry supports it. Keep IDs, titles, URLs, and current problem/category facts unchanged.

- [ ] **Step 3: Complete Polaris full-text note and six Timeline disclosures**

Read the Polaris primary paper in full, verify mechanism, closest single-agent/tool-routing control, decisive result, cost/coordination confounder, and negative or missing evidence. Create paired Chinese/English notes `papers/2608.14246.md` and `.en.md` using the same semantic judgment and primary-source links. Do not claim a multi-agent benefit unless the paper isolates it.

Co-locate `<a id="timeline"></a><a id="latest"></a>` before Timeline. Convert all six current items to `entry-<arxiv-id>` plus one compact `<details>` summary ordered by existing publication date. The open body uses the five paired semantic labels and links to paper plus local Chinese/English note. Reuse existing deep notes for the other five records. Add the section-level legacy-time notice.

- [ ] **Step 4: Add honest 7-day/30-day synthesis and preserve the stable map**

Co-locate `<a id="periods"></a><a id="changes"></a>` after Timeline. Add:

- `last-7-days`, `2026-08-14—2026-08-20`, using only Polaris within the inclusive window and labeling it `new_signal`, not a trend;
- `last-30-days`, `2026-07-22—2026-08-20`, using Polaris and Business Truth / QueryProof as separate supported direction signals, with confidence and implications.

Do not pull CIPHER or older work into the 30-day section. Keep older evidence in Field Map and Reading Paths. Add `field-map` before the stable Data-work map, change top navigation to Timeline → periods → map → paths → Library, and route evaluation intent to `Agent-Benchmark-Radar#benchmark-data`.

- [ ] **Step 5: Install protocol, Data adapter, and compaction contract**

Copy the shared `docs/RADAR_AGENT_PROTOCOL.md` verbatim. Rewrite `docs/DAILY_WORKFLOW.md` as the Data adapter: source lanes, identity/version gate, data-work loop, full-text evidence, business-semantic confounders, skeptical audit, Timeline projection, period boundaries, map gate, bilingual transaction, validation, and silent no-change exit.

Update `CURATION.md` to make agent-only maintenance normal and define canonical problem names. Add `COMPACTION.md` with rolling-root versus closed ISO-week/calendar-month semantics and no recursive summary evidence. Add `digests/README.md` as the closed-period index contract without creating fake closed-period files for the still-open week/month.

- [ ] **Step 6: Implement validation and verify GREEN**

Make `validate_registry` enforce unique IDs, the five allowed `map_delta` transitions plus `none`, paired legacy/null rules, complete native-v2 timestamps, and no unknown public candidate state. Make `scripts/validate_reading.py` call both `validate_pair` and `validate_registry` while preserving bilingual links, route, and local-file checks.

Update `.github/workflows/validate.yml`:

```yaml
- name: Test time-first and registry contracts
  run: python -m unittest discover -s tests -v
- name: Validate bilingual reading surfaces and registry
  run: python scripts/validate_reading.py
```

Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_reading.py
```

Expected: all tests pass; validator exits 0 with pristine output.

- [ ] **Step 7: Self-review and commit**

Verify all six works have an inline evidence audit and paired deep note, no legacy timestamp was fabricated, 7/30-day windows use only in-window records, map remains stable, no fixed count/pending state/empty digest link exists, and Benchmark routing preserves problem intent.

Commit:

```bash
git add docs/superpowers/plans/2026-08-20-time-first-radar-v2-data.md docs/RADAR_AGENT_PROTOCOL.md docs/DAILY_WORKFLOW.md CURATION.md COMPACTION.md digests/README.md data/papers.json README.md README.en.md papers/2608.14246.md papers/2608.14246.en.md scripts/timefirst_contract.py tests/test_timefirst_contract.py scripts/validate_reading.py .github/workflows/validate.yml
git commit -m "Add agent-maintained time-first data radar"
```
