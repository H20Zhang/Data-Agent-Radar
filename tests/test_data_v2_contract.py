import json
from datetime import date, timedelta
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_reading as data_validator
from validate_reading import (
    family_routes,
    validate_data_note_links,
    validate_period_contracts,
    validate_period_membership,
    validate_registry,
    validate_registry_projection,
)


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise AssertionError(f"expected an occurrence of {old!r}")
    return text.replace(old, new, 1)


def sub_once(text: str, pattern: str, replacement: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise AssertionError(f"expected exactly one match for {pattern!r}")
    return updated


def legacy_record(identity: str = "legacy") -> dict[str, object]:
    return {
        "id": identity,
        "title": "Legacy",
        "published": "2026-01-01",
        "published_at": "2026-01-01",
        "first_seen_at": None,
        "radar_published_at": None,
        "time_provenance": "legacy_unknown",
        "map_delta": "early_signal",
        "status": "public",
        "url": f"https://example.com/{identity}",
        "note_path": f"papers/{identity}.md",
        "primary_problem": "planning_orchestration",
        "importance": 3,
        "research_delta": "A complete research delta.",
        "main_caveat": "A complete main caveat.",
    }


def native_record(identity: str, radar_published_at: str) -> dict[str, object]:
    record = legacy_record(identity)
    record.update(
        {
            "title": f"Native {identity}",
            "published": "2026-08-19",
            "published_at": "2026-08-19T00:00:00Z",
            "first_seen_at": "2026-08-20T00:00:00Z",
            "radar_published_at": radar_published_at,
            "time_provenance": "native_v2",
            "url": f"https://arxiv.org/abs/{identity}",
            "note_path": f"papers/{identity}.md",
        }
    )
    return record


def append_timeline_entry(text: str, record: dict[str, object], language: str) -> str:
    identity = str(record["id"])
    anchor_identity = identity.replace(".", "-", 1)
    map_label = "地图" if language == "zh" else "Map"
    links_label = "链接" if language == "zh" else "Links"
    entry = f'''<a id="entry-{anchor_identity}"></a>
<details><summary>{str(record["radar_published_at"])[:10]} · {record["title"]} · Planning & Semantic Interaction — Native delta</summary>

**{map_label}.** `{record["map_delta"]}`

**{links_label}.** [Primary]({record["url"]}) · [中文](papers/{identity}.md) · [English](papers/{identity}.en.md)

</details>

'''
    return replace_once(text, '<a id="periods"></a>', entry + '<a id="periods"></a>')


class DataRegistryContractTest(unittest.TestCase):
    def test_repository_registry_satisfies_contract(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        self.assertEqual([], validate_registry(records))

    def test_complete_canonical_shape_is_required(self):
        for field in ("primary_problem", "importance", "research_delta", "main_caveat"):
            with self.subTest(field=field):
                record = legacy_record()
                record.pop(field)
                self.assertTrue(
                    any(field in error for error in validate_registry([record]))
                )

    def test_legacy_unknown_times_are_explicit_not_fabricated(self):
        for map_delta in ("none", "early_signal"):
            with self.subTest(map_delta=map_delta):
                record = legacy_record()
                record["map_delta"] = map_delta
                self.assertEqual([], validate_registry([record]))

    def test_untouched_legacy_record_may_omit_the_complete_v2_bundle(self):
        record = legacy_record()
        for field in (
            "published_at",
            "first_seen_at",
            "radar_published_at",
            "time_provenance",
            "map_delta",
        ):
            record.pop(field)

        self.assertEqual([], validate_registry([record]))

    def test_any_v2_field_requires_the_complete_v2_bundle(self):
        record = legacy_record()
        record.pop("first_seen_at")

        errors = validate_registry([record])

        self.assertTrue(
            any("complete v2" in error and "first_seen_at" in error for error in errors),
            errors,
        )

    def test_direction_keys_are_unique_lowercase_stable_tokens(self):
        for direction_keys in (
            [],
            ["dynamic-orchestration-package", "dynamic-orchestration-package"],
            ["Not Stable"],
        ):
            with self.subTest(direction_keys=direction_keys):
                record = legacy_record()
                record["direction_keys"] = direction_keys

                errors = validate_registry([record])

                self.assertTrue(any("direction_keys" in error for error in errors), errors)

    def test_duplicate_identity_and_url_are_rejected(self):
        first = legacy_record("one")
        second = legacy_record("one")
        second["url"] = first["url"]
        errors = validate_registry([first, second])
        self.assertTrue(any("duplicate id" in error.lower() for error in errors))
        self.assertTrue(any("duplicate url" in error.lower() for error in errors))

    def test_publication_date_parity_is_enforced(self):
        record = legacy_record()
        record["published_at"] = "2026-01-02"
        self.assertTrue(any("published_at" in error for error in validate_registry([record])))

    def test_legacy_unknown_requires_null_discovery_times(self):
        record = legacy_record()
        record["first_seen_at"] = "2026-08-20T01:00:00Z"
        self.assertTrue(any("first_seen_at" in error for error in validate_registry([record])))

    def test_native_v2_record_requires_complete_ordered_times(self):
        record = legacy_record()
        record.update({
            "published_at": "2026-08-19T00:00:00Z",
            "published": "2026-08-19",
            "first_seen_at": None,
            "radar_published_at": "2026-08-20T03:00:00Z",
            "time_provenance": "native_v2",
        })
        self.assertTrue(any("first_seen_at" in error for error in validate_registry([record])))
        record["first_seen_at"] = "2026-08-20T04:00:00Z"
        self.assertTrue(any("chronology" in error.lower() for error in validate_registry([record])))

    def test_native_v2_radar_time_cannot_predate_cutover(self):
        record = legacy_record()
        record.update({
            "published": "2026-08-19",
            "published_at": "2026-08-19T00:00:00Z",
            "first_seen_at": "2026-08-19T22:00:00Z",
            "radar_published_at": "2026-08-19T23:00:00Z",
            "time_provenance": "native_v2",
        })
        self.assertTrue(any("cutover" in error.lower() for error in validate_registry([record])))

    def test_native_v2_published_at_requires_a_strict_utc_timestamp(self):
        record = native_record("2608.90000", "2026-08-20T03:00:00Z")
        record["published_at"] = "2026-08-19"

        errors = validate_registry([record])

        self.assertTrue(
            any("published_at" in error and "UTC timestamp" in error for error in errors),
            errors,
        )

    def test_native_v2_published_calendar_date_matches_published_at(self):
        record = native_record("2608.90001", "2026-08-20T03:00:00Z")
        record["published"] = "2026-08-18"

        errors = validate_registry([record])

        self.assertTrue(
            any("published date parity" in error for error in errors),
            errors,
        )

    def test_explicit_legacy_records_cannot_claim_durable_map_deltas(self):
        earlier = legacy_record("earlier")
        changing = legacy_record("changing")
        changing["published"] = "2026-01-02"
        changing["published_at"] = "2026-01-02"
        changing["map_support_ids"] = ["changing", "earlier"]

        for delta in ("reinforces", "revises", "splits", "retires"):
            with self.subTest(delta=delta):
                changing["map_delta"] = delta

                errors = validate_registry([changing, earlier])

                self.assertTrue(
                    any(
                        "legacy_unknown map_delta must be none or early_signal"
                        in error
                        for error in errors
                    ),
                    errors,
                )

    def test_native_durable_change_may_use_earlier_legacy_prior_evidence(self):
        changing = native_record("2608.90040", "2026-08-20T03:00:00Z")
        changing["map_delta"] = "reinforces"
        changing["map_support_ids"] = ["2608.90040", "historical-prior"]
        historical_prior = legacy_record("historical-prior")

        self.assertEqual([], validate_registry([changing, historical_prior]))

    def test_reinforces_requires_multiple_explicit_canonical_map_supports(self):
        record = native_record("2608.90100", "2026-08-20T03:00:00Z")
        record["map_delta"] = "reinforces"
        record["map_support_ids"] = ["2608.90100"]
        errors = validate_registry([record])
        self.assertTrue(any("map_support_ids" in error and "at least 2" in error for error in errors))

        second = native_record("2608.90101", "2026-08-20T02:00:00Z")
        record["map_support_ids"] = ["2608.90100", "2608.90101"]
        self.assertEqual([], validate_registry([record, second]))

    def test_durable_transitions_require_independent_prior_map_support(self):
        for delta in ("revises", "splits", "retires"):
            with self.subTest(delta=delta):
                record = native_record("2608.90110", "2026-08-20T03:00:00Z")
                record["map_delta"] = delta
                record["map_support_ids"] = ["2608.90110"]
                errors = validate_registry([record])
                self.assertTrue(
                    any(
                        "map_support_ids" in error and "at least 2" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_durable_transition_rejects_support_without_earlier_effective_time(self):
        changing = native_record("2608.90120", "2026-08-20T03:00:00Z")
        changing["map_delta"] = "revises"
        changing["map_support_ids"] = ["2608.90120", "2608.90121"]
        later = native_record("2608.90121", "2026-08-20T04:00:00Z")

        errors = validate_registry([changing, later])

        self.assertTrue(
            any("demonstrably earlier effective evidence time" in error for error in errors),
            errors,
        )

    def test_native_prior_map_chronology_uses_radar_time_not_source_date(self):
        changing = native_record("2608.90010", "2026-08-20T03:00:00Z")
        changing["map_delta"] = "splits"
        changing["map_support_ids"] = ["2608.90010", "2608.90011"]
        later_acceptance = native_record("2608.90011", "2026-08-20T04:00:00Z")
        later_acceptance["published"] = "2026-08-19"
        later_acceptance["published_at"] = "2026-08-19"

        errors = validate_registry([changing, later_acceptance])

        self.assertTrue(
            any("demonstrably earlier effective evidence time" in error for error in errors),
            errors,
        )

    def test_same_day_legacy_date_cannot_fabricate_prior_map_order(self):
        changing = native_record("2608.90020", "2026-08-20T03:00:00Z")
        changing["map_delta"] = "retires"
        changing["map_support_ids"] = ["2608.90020", "2608.90021"]
        imprecise_legacy = legacy_record("2608.90021")
        imprecise_legacy.update(
            {
                "published": "2026-08-20",
                "published_at": "2026-08-20",
                "url": "https://arxiv.org/abs/2608.90021",
                "note_path": "papers/2608.90021.md",
            }
        )

        errors = validate_registry([changing, imprecise_legacy])

        self.assertTrue(
            any("demonstrably earlier effective evidence time" in error for error in errors),
            errors,
        )

    def test_strictly_earlier_radar_time_is_valid_prior_map_support(self):
        changing = native_record("2608.90030", "2026-08-20T03:00:00Z")
        changing["map_delta"] = "reinforces"
        changing["map_support_ids"] = ["2608.90030", "2608.90031"]
        earlier = native_record("2608.90031", "2026-08-20T02:00:00Z")

        errors = validate_registry([changing, earlier])

        self.assertEqual([], errors)

    def test_map_supports_must_be_unique_known_canonical_identities(self):
        record = native_record("2608.90130", "2026-08-20T03:00:00Z")
        record["map_delta"] = "reinforces"
        for supports, expected in (
            (["2608.90130", "2608.90130"], "duplicates"),
            (["2608.90130", "missing"], "unknown canonical"),
        ):
            with self.subTest(supports=supports):
                record["map_support_ids"] = supports
                errors = validate_registry([record])
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_invalid_delta_provenance_status_or_url_is_rejected(self):
        mutations = (
            ("map_delta", "promotes", "map_delta"),
            ("time_provenance", "guessed", "time_provenance"),
            ("status", "pending", "status"),
            ("url", "https://example.com/not-canonical", "canonical primary"),
        )
        for key, value, expected in mutations:
            with self.subTest(key=key):
                record = legacy_record("2608.14246")
                record["url"] = "https://arxiv.org/abs/2608.14246"
                record["note_path"] = "papers/2608.14246.md"
                record[key] = value
                self.assertTrue(any(expected in error.lower() for error in validate_registry([record])))

    def test_repository_period_membership_is_exact_and_publication_based(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        self.assertEqual([], validate_period_membership(records, (ROOT / "README.md").read_text(encoding="utf-8")))

    def test_each_timeline_entry_has_corresponding_paired_notes(self):
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        self.assertEqual([], validate_data_note_links(zh, en))

    def test_registry_projection_binds_identity_primary_url_and_note(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        self.assertEqual([], validate_registry_projection(records, zh, en))
        wrong = en.replace(
            "https://arxiv.org/abs/2608.14246",
            "https://arxiv.org/abs/2608.99999",
            1,
        )
        self.assertTrue(
            any("canonical primary" in error.lower() for error in validate_registry_projection(records, zh, wrong))
        )

    def test_registry_projection_binds_displayed_date_map_and_field_label(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        mutations = (
            ("2026-08-14 · Polaris", "2026-08-13 · Polaris", "displayed date"),
            ("**地图。** `early_signal`", "**地图。** `none`", "map_delta"),
            ("Planning & Semantic Interaction", "Planning & Orchestration", "field-map problem"),
        )
        for old, new, expected in mutations:
            with self.subTest(expected=expected):
                mutated = zh.replace(old, new, 1)
                errors = validate_registry_projection(records, mutated, en)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_hidden_canonical_link_cannot_rescue_wrong_visible_timeline_link(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        canonical = "https://arxiv.org/abs/2608.14246"
        for language in ("zh", "en"):
            text = zh if language == "zh" else en
            text = replace_once(
                text,
                f"]({canonical})",
                f"](https://example.com/wrong) <!-- [Hidden]({canonical}) -->",
            )
            if language == "zh":
                zh = text
            else:
                en = text
        errors = validate_registry_projection(records, zh, en)
        self.assertTrue(
            any("2608-14246" in error and "canonical primary" in error for error in errors),
            errors,
        )

    def test_hidden_map_token_cannot_override_visible_timeline_map(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        source_zh = (ROOT / "README.md").read_text(encoding="utf-8")
        first_identity = data_validator._timeline_chunks(source_zh)[0][0]
        zh = replace_once(
            source_zh,
            "**地图。** `early_signal`",
            "**地图。** <!-- `early_signal` --> `none`",
        )
        en = replace_once(
            (ROOT / "README.en.md").read_text(encoding="utf-8"),
            "**Map.** `early_signal`",
            "**Map.** <!-- `early_signal` --> `none`",
        )
        errors = validate_registry_projection(records, zh, en)
        self.assertTrue(
            any(first_identity in error and "map_delta" in error for error in errors),
            errors,
        )

    def test_hidden_paired_note_link_does_not_count_as_visible(self):
        zh = replace_once(
            (ROOT / "README.md").read_text(encoding="utf-8"),
            "[中文深读](papers/2608.14246.md)",
            "<!-- [中文深读](papers/2608.14246.md) -->",
        )
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        errors = validate_data_note_links(zh, en)
        self.assertTrue(
            any("2608-14246" in error and "deep-note" in error for error in errors),
            errors,
        )

    def test_same_day_native_records_use_full_timestamp_order_before_legacy(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        earlier = native_record("2608.90001", "2026-08-20T01:00:00Z")
        later = native_record("2608.90002", "2026-08-20T02:00:00Z")
        records.extend((earlier, later))
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        for record in (earlier, later):
            zh = append_timeline_entry(zh, record, "zh")
            en = append_timeline_entry(en, record, "en")

        errors = validate_registry_projection(records, zh, en)

        self.assertTrue(
            any("full radar timestamp order" in error.lower() for error in errors),
            errors,
        )

    def test_native_timeline_date_uses_radar_publication_not_source_publication(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        records[0] = dict(records[0])
        records[0].update({
            "time_provenance": "native_v2",
            "first_seen_at": "2026-08-20T01:00:00Z",
            "radar_published_at": "2026-08-20T02:00:00Z",
        })
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        errors = validate_registry_projection(records, zh, en)
        self.assertTrue(any("displayed date" in error for error in errors), errors)

    def test_native_timeline_rejects_acceptance_after_public_synthesis_cutoff(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        synthesis_cutoff = data_validator._shared_public_synthesis(zh, en)
        self.assertIsNotNone(synthesis_cutoff)
        records[0] = dict(records[0])
        records[0].update(
            {
                "time_provenance": "native_v2",
                "radar_published_at": (
                    synthesis_cutoff + timedelta(seconds=1)
                ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )

        errors = validate_registry_projection(records, zh, en)

        self.assertTrue(
            any("Timeline" in error and "synthesis cutoff" in error for error in errors),
            errors,
        )

    def test_native_timeline_acceptance_at_public_synthesis_cutoff_is_inclusive(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")

        self.assertEqual([], validate_registry_projection(records, zh, en))

    def test_hidden_structural_anchor_decoys_do_not_rebound_data_sections(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        for language, text in (("zh", zh), ("en", en)):
            text = replace_once(
                text,
                '<a id="timeline"></a>',
                '<!-- <a id="periods"></a> -->\n<a id="timeline"></a>',
            )
            text = replace_once(
                text,
                '<a id="last-30-days"></a>',
                '<a id="last-30-days"></a>\n<!-- <a id="field-map"></a> -->',
            )
            text = replace_once(
                text,
                '<a id="last-7-days"></a>',
                '<!-- <a id="last-30-days"></a> -->\n'
                '<a id="last-7-days"></a>',
            )
            if language == "zh":
                zh = text
            else:
                en = text

        errors = [
            *validate_data_note_links(zh, en),
            *validate_registry_projection(records, zh, en),
            *validate_period_contracts(records, zh, en),
        ]

        self.assertEqual([], errors)

    def test_periods_are_exact_7_and_30_day_inclusive_windows(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        section = data_validator._period_section(text, "last-7-days", "last-30-days")
        match = data_validator.RANGE_RE.search(section)
        self.assertIsNotNone(match)
        start, end = match.group("start"), match.group("end")
        shifted_start = (date.fromisoformat(start) - timedelta(days=1)).isoformat()
        shifted = replace_once(text, f"{start}—{end}", f"{shifted_start}—{end}")
        self.assertTrue(any("inclusive length" in error.lower() for error in validate_period_membership(records, shifted)))


class DataPeriodDirectionContractTest(unittest.TestCase):
    def inputs(self) -> tuple[list[dict[str, object]], str, str]:
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        records = [
            record for record in records if record.get("time_provenance") == "legacy_unknown"
        ]
        zh = '''<a id="last-7-days"></a>
### 过去 7 天 · 2026-08-14—2026-08-20

- **`new_signal` · 规划与语义交互 · 动态编排目前只构成整套系统层面的新信号。** <!-- timefirst:direction key="dynamic-orchestration-package" state="new_signal" supports="2608.14246" confidence="low" implication="match-controller-cost-recovery~controller-total-cost-error-propagation" time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" synthesized="2026-08-20T00:00:00Z" prior="none" --> 支撑：[Polaris](#entry-2608-14246)；置信度：**低**。含义：下一步应匹配控制器，核算 controller total cost error propagation。时间基准：`legacy_publication_date`，**not Radar acceptance**。最后合成：**2026-08-20T00:00:00Z (UTC)**。先验地图证据：**none**。

<a id="last-30-days"></a>
### 过去 30 天 · 2026-07-22—2026-08-20

- **`new_signal` · 规划与语义交互 · 动态编排扩大了系统的控制能力。** <!-- timefirst:direction key="dynamic-orchestration-package" state="new_signal" supports="2608.14246" confidence="low" implication="match-controller-cost-recovery~matched-controller-dtc-off" time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" synthesized="2026-08-20T00:00:00Z" prior="none" --> 支撑：[Polaris](#entry-2608-14246)；置信度：**低**。含义：需要 matched controller DTC-off 条件对照。时间基准：`legacy_publication_date`，**not Radar acceptance**。最后合成：**2026-08-20T00:00:00Z (UTC)**。先验地图证据：**none**。
- **`new_signal` · 验证与恢复 · 能否安全作答成为正确性的一部分。** <!-- timefirst:direction key="business-truth-safety-contract" state="new_signal" supports="2608.09254" confidence="medium" implication="separate-business-truth-from-execution~ambiguity-answerability-clarification" time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" synthesized="2026-08-20T00:00:00Z" prior="none" --> 支撑：[Business Truth](#entry-2608-09254)；置信度：**中**。含义：分别测量 ambiguity answerability clarification。时间基准：`legacy_publication_date`，**not Radar acceptance**。最后合成：**2026-08-20T00:00:00Z (UTC)**。先验地图证据：**none**。

<a id="field-map"></a>
'''
        en = '''<a id="last-7-days"></a>
### Last 7 days · 2026-08-14—2026-08-20

- **`new_signal` · Planning & Semantic Interaction · Dynamic orchestration remains a packaged-system signal.** <!-- timefirst:direction key="dynamic-orchestration-package" state="new_signal" supports="2608.14246" confidence="low" implication="match-controller-cost-recovery~controller-total-cost-error-propagation" time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" synthesized="2026-08-20T00:00:00Z" prior="none" --> Support: [Polaris](#entry-2608-14246); confidence: **low**. Implication: next match the controller total cost error propagation evidence. Time basis: `legacy_publication_date`, **not Radar acceptance**. Last synthesized: **2026-08-20T00:00:00Z (UTC)**. Prior map evidence: **none**.

<a id="last-30-days"></a>
### Last 30 days · 2026-07-22—2026-08-20

- **`new_signal` · Planning & Semantic Interaction · Dynamic orchestration expands control capacity.** <!-- timefirst:direction key="dynamic-orchestration-package" state="new_signal" supports="2608.14246" confidence="low" implication="match-controller-cost-recovery~matched-controller-dtc-off" time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" synthesized="2026-08-20T00:00:00Z" prior="none" --> Support: [Polaris](#entry-2608-14246); confidence: **low**. Implication: require a matched controller DTC-off comparison. Time basis: `legacy_publication_date`, **not Radar acceptance**. Last synthesized: **2026-08-20T00:00:00Z (UTC)**. Prior map evidence: **none**.
- **`new_signal` · Verification & Recovery · Safe-to-answer enters correctness.** <!-- timefirst:direction key="business-truth-safety-contract" state="new_signal" supports="2608.09254" confidence="medium" implication="separate-business-truth-from-execution~ambiguity-answerability-clarification" time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" synthesized="2026-08-20T00:00:00Z" prior="none" --> Support: [Business Truth](#entry-2608-09254); confidence: **medium**. Implication: measure ambiguity answerability clarification separately. Time basis: `legacy_publication_date`, **not Radar acceptance**. Last synthesized: **2026-08-20T00:00:00Z (UTC)**. Prior map evidence: **none**.

<a id="field-map"></a>
'''
        return records, zh, en

    def direction_line(self, text: str, index: int = 0) -> str:
        lines = [line for line in text.splitlines() if "timefirst:direction" in line]
        if index >= len(lines):
            raise AssertionError(f"missing direction line at index {index}")
        return lines[index]

    def direction_metadata(self, line: str) -> str:
        match = re.search(r"<!--\s*timefirst:direction.*?-->", line)
        if match is None:
            raise AssertionError("missing direction metadata")
        return match.group(0)

    def native_direction_section(
        self,
        *,
        state: str = "new_signal",
        supports: str = "2608.90000",
        prior: str = "none",
        synthesized: str = "2026-08-21T03:00:00Z",
    ) -> str:
        visible_supports = (
            "**none**"
            if supports == "none"
            else ", ".join(
                f"[Native {identity}](#entry-{identity.replace('.', '-', 1)})"
                for identity in supports.split(",")
            )
        )
        visible_prior = (
            "**none**" if prior == "none" else "[Field Map](#field-map)"
        )
        return (
            f'- **`{state}` · Planning & Semantic Interaction · Bounded native signal.** '
            '<!-- timefirst:direction key="native-bounded-direction" '
            f'state="{state}" supports="{supports}" confidence="medium" '
            'implication="test-matched-control~matched-control-boundary" '
            'time_basis="radar_published_at" non_acceptance="radar-acceptance" '
            f'synthesized="{synthesized}" prior="{prior}" --> '
            f'Support: {visible_supports}; confidence: **medium**. '
            'Implication: preserve the matched control boundary evidence. '
            'Time basis: `radar_published_at`, **Radar acceptance**. '
            f'Last synthesized: **{synthesized} (UTC)**. '
            f'Prior map evidence: {visible_prior}.'
        )

    def parse_native_direction(
        self,
        record: dict[str, object],
        **section_kwargs: str,
    ) -> list[str]:
        errors: list[str] = []
        data_validator._parse_direction_items(
            "README.en.md",
            "last-7-days",
            self.native_direction_section(**section_kwargs),
            (date(2026, 8, 15), date(2026, 8, 21)),
            str(section_kwargs.get("synthesized", "2026-08-21T03:00:00Z")),
            {str(record["id"]): record},
            errors,
        )
        return errors

    def move_metadata_to_continuation(self, line: str) -> str:
        metadata = self.direction_metadata(line)
        return f"{line.replace(metadata, '', 1).rstrip()}\n  {metadata}"

    def test_repository_structured_period_contracts_are_valid(self):
        records = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        self.assertEqual([], validate_period_contracts(records, zh, en))

    def test_native_radar_acceptance_adapter_allows_one_early_signal(self):
        record = native_record("2608.90000", "2026-08-21T02:00:00Z")
        record["direction_keys"] = ["native-bounded-direction"]

        self.assertEqual([], self.parse_native_direction(record))

    def test_native_new_signal_requires_one_early_signal_support_and_no_prior(self):
        record = native_record("2608.90000", "2026-08-21T02:00:00Z")
        record["direction_keys"] = ["native-bounded-direction"]
        record["map_delta"] = "reinforces"

        errors = self.parse_native_direction(record, prior="field-map")

        self.assertTrue(
            any("radar_published_at adapter requires one early_signal support" in error for error in errors),
            errors,
        )

    def test_one_native_support_cannot_be_a_reinforced_direction(self):
        record = native_record("2608.90000", "2026-08-21T02:00:00Z")
        record["direction_keys"] = ["native-bounded-direction"]

        errors = self.parse_native_direction(
            record, state="reinforced", prior="field-map"
        )

        self.assertTrue(
            any("reinforced requires at least two" in error for error in errors),
            errors,
        )

    def test_native_period_membership_uses_radar_publication_time(self):
        record = native_record("2608.90000", "2026-08-14T23:59:59Z")
        record["direction_keys"] = ["native-bounded-direction"]

        errors = self.parse_native_direction(record)

        self.assertTrue(
            any("outside" in error and "radar_published_at" in error for error in errors),
            errors,
        )

    def test_period_windows_advance_with_shared_exact_synthesis_cutoff(self):
        records, zh, en = self.inputs()
        records[0] = dict(records[0])
        records[0]["published"] = "2026-08-15"
        records[0]["published_at"] = "2026-08-15"
        replacements = (
            ("2026-08-14—2026-08-20", "2026-08-15—2026-08-21"),
            ("2026-07-22—2026-08-20", "2026-07-23—2026-08-21"),
            ("2026-08-20T00:00:00Z", "2026-08-21T03:00:00Z"),
        )
        for old, new in replacements:
            zh = zh.replace(old, new)
            en = en.replace(old, new)

        self.assertEqual([], validate_period_contracts(records, zh, en))

    def test_direction_requires_synthesized_metadata(self):
        records, zh, en = self.inputs()
        for language, text in (("README.md", zh), ("README.en.md", en)):
            with self.subTest(language=language):
                mutated = text.replace(
                    ' synthesized="2026-08-20T00:00:00Z"', "", 1
                )
                errors = validate_period_contracts(
                    records,
                    mutated if language == "README.md" else zh,
                    mutated if language == "README.en.md" else en,
                )
                self.assertTrue(
                    any(
                        language in error
                        and "last-7-days" in error
                        and "synthesized" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_period_direction_blocks_require_exactly_one_scoped_visible_field(self):
        records, base_zh, base_en = self.inputs()
        duplicates = {
            "README.md": {
                "state": "旁注：**`no_material_change` · 矛盾状态。**",
                "supports": "旁注：支撑：[Polaris](#entry-2608-14246)；",
                "confidence": "旁注：置信度：**高**。",
                "time basis": (
                    "旁注：时间基准：`legacy_publication_date`，"
                    "**not Radar acceptance**。"
                ),
                "non-acceptance": "旁注：**not Radar acceptance**。",
                "synthesis": (
                    "旁注：最后合成："
                    "**2026-08-20T00:00:00Z (UTC)**。"
                ),
                "implication": "旁注：含义：controller total cost error propagation。",
            },
            "README.en.md": {
                "state": "Aside: **`no_material_change` · contradictory state.**",
                "supports": "Aside: Support: [Polaris](#entry-2608-14246);",
                "confidence": "Aside: confidence: **high**.",
                "time basis": (
                    "Aside: Time basis: `legacy_publication_date`, "
                    "**not Radar acceptance**."
                ),
                "non-acceptance": "Aside: **not Radar acceptance**.",
                "synthesis": (
                    "Aside: Last synthesized: "
                    "**2026-08-20T00:00:00Z (UTC)**."
                ),
                "implication": "Aside: Implication: controller total cost error propagation.",
            },
        }
        for language, fields in duplicates.items():
            for field, duplicate in fields.items():
                with self.subTest(language=language, field=field):
                    text = base_zh if language == "README.md" else base_en
                    line = self.direction_line(text)
                    mutated = replace_once(text, line, f"{line}\n  {duplicate}")
                    errors = validate_period_contracts(
                        records,
                        mutated if language == "README.md" else base_zh,
                        mutated if language == "README.en.md" else base_en,
                    )
                    self.assertTrue(
                        any(
                            language in error
                            and "last-7-days" in error
                            and f"exactly one visible {field} field" in error
                            for error in errors
                        ),
                        errors,
                    )

    def test_period_direction_fields_may_live_on_continuation_lines(self):
        records, zh, en = self.inputs()
        for language, text, tokens in (
            (
                "README.md",
                zh,
                (" 支撑：", "置信度：", "含义：", "时间基准：", "最后合成："),
            ),
            (
                "README.en.md",
                en,
                (" Support:", "confidence:", "Implication:", "Time basis:", "Last synthesized:"),
            ),
        ):
            line = self.direction_line(text)
            multiline = line
            for token in tokens:
                multiline = multiline.replace(token, f"\n  {token.lstrip()}", 1)
            if language == "README.md":
                zh = replace_once(zh, line, multiline)
            else:
                en = replace_once(en, line, multiline)

        self.assertEqual([], validate_period_contracts(records, zh, en))

    def test_direction_metadata_at_continuation_end_stays_in_item_block(self):
        records, zh, en = self.inputs()
        zh_line = self.direction_line(zh)
        en_line = self.direction_line(en)
        zh = replace_once(zh, zh_line, self.move_metadata_to_continuation(zh_line))
        en = replace_once(en, en_line, self.move_metadata_to_continuation(en_line))

        self.assertEqual([], validate_period_contracts(records, zh, en))

    def test_true_duplicate_metadata_on_continuation_is_rejected(self):
        records, zh, en = self.inputs()
        line = self.direction_line(zh)
        metadata = self.direction_metadata(line)
        zh = replace_once(zh, line, f"{line}\n  {metadata}")

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "README.md" in error
                and "last-7-days" in error
                and "exactly one stable direction metadata block" in error
                for error in errors
            ),
            errors,
        )

    def test_adjacent_visible_direction_items_remain_distinct_block_boundaries(self):
        records, zh, en = self.inputs()
        zh_line = self.direction_line(zh, 2)
        en_line = self.direction_line(en, 2)
        zh = replace_once(zh, zh_line, self.move_metadata_to_continuation(zh_line))
        en = replace_once(en, en_line, self.move_metadata_to_continuation(en_line))

        self.assertEqual([], validate_period_contracts(records, zh, en))

    def test_malformed_primary_fields_cannot_be_laundered_by_labeled_asides(self):
        records, base_zh, base_en = self.inputs()
        mutations = {
            "README.md": (
                (
                    "supports",
                    "支撑：[Polaris](#entry-2608-14246)；",
                    "支撑缺少结构。旁注：支撑：[Polaris](#entry-2608-14246)；",
                ),
                (
                    "confidence",
                    "置信度：**低**",
                    "置信度缺少结构。旁注：置信度：**低**",
                ),
                (
                    "time basis",
                    "时间基准：`legacy_publication_date`，",
                    "时间基准缺少结构。旁注："
                    "时间基准：`legacy_publication_date`，",
                ),
                (
                    "non-acceptance",
                    "**not Radar acceptance**",
                    "not Radar acceptance 缺少结构。"
                    "旁注：**not Radar acceptance**",
                ),
                (
                    "synthesis",
                    "最后合成：**2026-08-20T00:00:00Z (UTC)**",
                    "最后合成缺少结构。旁注："
                    "最后合成：**2026-08-20T00:00:00Z (UTC)**",
                ),
                (
                    "implication",
                    "含义：下一步应匹配控制器",
                    "含义缺少结构。旁注：含义：下一步应匹配控制器",
                ),
            ),
            "README.en.md": (
                (
                    "supports",
                    "Support: [Polaris](#entry-2608-14246);",
                    "Support lacks structure. Aside: "
                    "Support: [Polaris](#entry-2608-14246);",
                ),
                (
                    "confidence",
                    "confidence: **low**",
                    "confidence lacks structure. Aside: confidence: **low**",
                ),
                (
                    "time basis",
                    "Time basis: `legacy_publication_date`,",
                    "Time basis lacks structure. Aside: "
                    "Time basis: `legacy_publication_date`,",
                ),
                (
                    "non-acceptance",
                    "**not Radar acceptance**",
                    "not Radar acceptance lacks structure. "
                    "Aside: **not Radar acceptance**",
                ),
                (
                    "synthesis",
                    "Last synthesized: **2026-08-20T00:00:00Z (UTC)**",
                    "Last synthesized lacks structure. Aside: "
                    "Last synthesized: **2026-08-20T00:00:00Z (UTC)**",
                ),
                (
                    "implication",
                    "Implication: next match the controller",
                    "Implication lacks structure. Aside: "
                    "Implication: next match the controller",
                ),
            ),
        }
        for language, cases in mutations.items():
            for field, old, new in cases:
                with self.subTest(language=language, field=field):
                    text = base_zh if language == "README.md" else base_en
                    line = self.direction_line(text)
                    mutated_line = replace_once(line, old, new)
                    mutated = replace_once(text, line, mutated_line)
                    errors = validate_period_contracts(
                        records,
                        mutated if language == "README.md" else base_zh,
                        mutated if language == "README.en.md" else base_en,
                    )
                    self.assertTrue(
                        any(
                            language in error
                            and "last-7-days" in error
                            and f"exactly one visible {field} field" in error
                            for error in errors
                        ),
                        errors,
                    )

    def test_legacy_support_cannot_postdate_direction_synthesis(self):
        records, zh, en = self.inputs()
        records[0] = dict(records[0])
        records[0]["published"] = "2026-08-21"
        records[0]["published_at"] = "2026-08-21"

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "support identity 2608.14246" in error
                and "published after direction synthesized" in error
                for error in errors
            ),
            errors,
        )

    def test_direction_requires_complete_stable_metadata(self):
        records, zh, en = self.inputs()
        zh = zh.replace(' time_basis="legacy_publication_date"', "", 1)
        en = en.replace(' time_basis="legacy_publication_date"', "", 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("time_basis" in error for error in errors), errors)

    def test_visible_support_order_must_match_metadata_without_duplicates(self):
        records, zh, en = self.inputs()
        zh = zh.replace("[Polaris](#entry-2608-14246)", "[CIPHER](#entry-2607-14386)", 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("visible support order" in error for error in errors), errors)

    def test_hidden_visible_state_cannot_override_the_human_visible_state(self):
        records, zh, en = self.inputs()
        zh = replace_once(
            zh,
            "- **`new_signal` · 规划与语义交互",
            "- <!-- **`new_signal` --> **`reinforced` · 规划与语义交互",
        )
        en = replace_once(
            en,
            "- **`new_signal` · Planning & Semantic Interaction",
            "- <!-- **`new_signal` --> **`reinforced` · Planning & Semantic Interaction",
        )
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("visible state" in error for error in errors), errors)

    def test_hidden_support_link_does_not_satisfy_visible_support_parity(self):
        records, zh, en = self.inputs()
        zh = replace_once(
            zh,
            "[Polaris](#entry-2608-14246)",
            "<!-- [Polaris](#entry-2608-14246) -->",
        )
        en = replace_once(
            en,
            "[Polaris](#entry-2608-14246)",
            "<!-- [Polaris](#entry-2608-14246) -->",
        )
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("visible support" in error for error in errors), errors)

    def test_hidden_time_basis_token_cannot_rescue_wrong_visible_basis(self):
        records, zh, en = self.inputs()
        zh = replace_once(
            zh,
            "时间基准：`legacy_publication_date`",
            "时间基准：<!-- `legacy_publication_date` --> `radar_published_at`",
        )
        en = replace_once(
            en,
            "Time basis: `legacy_publication_date`",
            "Time basis: <!-- `legacy_publication_date` --> `radar_published_at`",
        )
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("visible time_basis" in error for error in errors), errors)

    def test_hidden_synthesis_timestamp_cannot_rescue_missing_visible_timestamp(self):
        records, zh, en = self.inputs()
        timestamp = "2026-08-20T00:00:00Z (UTC)"
        zh = replace_once(
            zh,
            f"最后合成：**{timestamp}**",
            f"<!-- 最后合成：**{timestamp}** -->最后合成：**不可用**",
        )
        en = replace_once(
            en,
            f"Last synthesized: **{timestamp}**",
            f"<!-- Last synthesized: **{timestamp}** -->Last synthesized: **unavailable**",
        )
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("last-synthesis" in error for error in errors), errors)

    def test_confidence_is_a_closed_enum(self):
        records, zh, en = self.inputs()
        zh = replace_once(zh, 'confidence="low"', 'confidence="certain"')
        en = replace_once(en, 'confidence="low"', 'confidence="certain"')
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("confidence" in error and "low|medium|high" in error for error in errors), errors)

    def test_hidden_confidence_cannot_override_visible_confidence(self):
        records, zh, en = self.inputs()
        zh = replace_once(
            zh,
            "置信度：**低**",
            "<!-- 置信度：**低** -->置信度：**高**",
        )
        en = replace_once(
            en,
            "confidence: **low**",
            "<!-- confidence: **low** -->confidence: **high**",
        )
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("visible confidence" in error for error in errors), errors)

    def test_implication_requires_a_stable_key_and_visible_witness(self):
        records, zh, en = self.inputs()
        zh = sub_once(zh, r'implication="[^"]+"', 'implication="free-form"')
        en = sub_once(en, r'implication="[^"]+"', 'implication="free-form"')
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("implication" in error and "witness" in error for error in errors), errors)

    def test_hidden_implication_witness_cannot_rescue_unrelated_visible_prose(self):
        records, zh, en = self.inputs()
        zh = sub_once(
            zh,
            r"含义：.*?。时间基准",
            "<!-- controller total cost error propagation -->含义：没有相关证据。时间基准",
        )
        en = sub_once(
            en,
            r"Implication: .*?\. Time basis",
            "<!-- controller total cost error propagation -->Implication: unrelated prose. Time basis",
        )
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("visible implication" in error for error in errors), errors)

    def test_duplicate_support_identity_is_rejected(self):
        records, zh, en = self.inputs()
        for old, new in (
            ('supports="2608.14246"', 'supports="2608.14246,2608.14246"'),
            (
                "[Polaris](#entry-2608-14246)",
                "[Polaris](#entry-2608-14246), [Polaris again](#entry-2608-14246)",
            ),
        ):
            zh = zh.replace(old, new, 1)
            en = en.replace(old, new, 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("duplicate support" in error for error in errors), errors)

    def test_out_of_window_cipher_support_is_rejected(self):
        records, zh, en = self.inputs()
        for old, new in (
            ('supports="2608.14246"', 'supports="2607.14386"'),
            ("[Polaris](#entry-2608-14246)", "[CIPHER](#entry-2607-14386)"),
        ):
            zh = zh.replace(old, new, 1)
            en = en.replace(old, new, 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("2607.14386" in error and "outside" in error for error in errors), errors)

    def test_legacy_publication_adapter_only_emits_new_signal(self):
        for state in (
            "reinforced",
            "revised",
            "splits",
            "retires",
            "no_material_change",
        ):
            with self.subTest(state=state):
                records, zh, en = self.inputs()
                for old, new in (
                    ('state="new_signal"', f'state="{state}"'),
                    ("**`new_signal`", f"**`{state}`"),
                ):
                    zh = zh.replace(old, new, 1)
                    en = en.replace(old, new, 1)

                errors = validate_period_contracts(records, zh, en)

                self.assertTrue(
                    any(
                        "legacy_publication_date adapter requires state=new_signal"
                        in error
                        for error in errors
                    ),
                    errors,
                )

    def test_legacy_publication_adapter_allows_context_with_map_delta_none(self):
        records, zh, en = self.inputs()
        records[0]["map_delta"] = "none"

        self.assertEqual([], validate_period_contracts(records, zh, en))

    def test_legacy_publication_adapter_requires_exactly_one_support(self):
        records, zh, en = self.inputs()
        second = dict(records[0])
        second["id"] = "2608.14247"
        second["title"] = "Second same-key legacy support"
        second["url"] = "https://arxiv.org/abs/2608.14247"
        second["note_path"] = "papers/2608.14247.md"
        records.append(second)
        for old, new in (
            (
                'supports="2608.14246"',
                'supports="2608.14246,2608.14247"',
            ),
            (
                "[Polaris](#entry-2608-14246)",
                "[Polaris](#entry-2608-14246), "
                "[Second support](#entry-2608-14247)",
            ),
        ):
            zh = zh.replace(old, new, 1)
            en = en.replace(old, new, 1)

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "legacy_publication_date adapter requires exactly one support identity"
                in error
                for error in errors
            ),
            errors,
        )

    def test_legacy_publication_adapter_support_cannot_carry_durable_map_delta(self):
        for delta in ("reinforces", "revises", "splits", "retires"):
            with self.subTest(delta=delta):
                records, zh, en = self.inputs()
                records[0]["map_delta"] = delta

                errors = validate_period_contracts(records, zh, en)

                self.assertTrue(
                    any(
                        "legacy_publication_date adapter support identity "
                        "2608.14246 map_delta must be none or early_signal"
                        in error
                        for error in errors
                    ),
                    errors,
                )

    def test_legacy_publication_adapter_requires_legacy_support(self):
        records, zh, en = self.inputs()
        records[0].update(
            {
                "published_at": "2026-08-14T00:00:00Z",
                "first_seen_at": "2026-08-20T00:00:00Z",
                "radar_published_at": "2026-08-20T00:00:00Z",
                "time_provenance": "native_v2",
            }
        )

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "2608.14246 is not an honest legacy publication-date record"
                in error
                for error in errors
            ),
            errors,
        )

    def test_legacy_publication_adapter_requires_prior_none(self):
        records, zh, en = self.inputs()
        for old, new in (
            ('prior="none"', 'prior="field-map"'),
            ("先验地图证据：**none**", "先验地图证据：[领域地图](#field-map)"),
        ):
            zh = zh.replace(old, new, 1)
        for old, new in (
            ('prior="none"', 'prior="field-map"'),
            ("Prior map evidence: **none**", "Prior map evidence: [Field Map](#field-map)"),
        ):
            en = en.replace(old, new, 1)

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "legacy_publication_date adapter requires prior=none" in error
                for error in errors
            ),
            errors,
        )

    def test_one_support_cannot_be_reinforced(self):
        records, zh, en = self.inputs()
        for old, new in (
            ('state="new_signal"', 'state="reinforced"'),
            ("**`new_signal`", "**`reinforced`"),
        ):
            zh = zh.replace(old, new, 1)
            en = en.replace(old, new, 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(
            any(
                "legacy_publication_date adapter requires state=new_signal" in error
                for error in errors
            ),
            errors,
        )

    def test_every_direction_requires_exact_prior_metadata_and_visible_field(self):
        records, zh, en = self.inputs()
        zh = zh.replace(' prior="none"', "", 1)
        en = en.replace(' prior="none"', "", 1)

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(any("prior" in error for error in errors), errors)

    def test_cross_key_polaris_and_business_truth_cannot_be_reinforced(self):
        records, zh, en = self.inputs()
        zh_lines = [line for line in zh.splitlines() if "timefirst:direction" in line]
        en_lines = [line for line in en.splitlines() if "timefirst:direction" in line]
        zh_combined = (
            '- **`reinforced` · Planning & Semantic Interaction · 跨方向合并。** '
            '<!-- timefirst:direction key="dynamic-orchestration-package" '
            'state="reinforced" supports="2608.14246,2608.09254" confidence="low" '
            'implication="reject-cross-key-merge~cross-key-evidence-merge" '
            'time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" '
            'synthesized="2026-08-20T00:00:00Z" prior="field-map" --> '
            '支撑：[Polaris](#entry-2608-14246)，[Business Truth](#entry-2608-09254)；'
            '置信度：**低**。含义：拒绝 cross key evidence merge 作为强化。'
            '时间基准：`legacy_publication_date`，**not Radar acceptance**。'
            '最后合成：**2026-08-20T00:00:00Z (UTC)**。'
            '先验地图证据：[领域地图](#field-map)。'
        )
        en_combined = (
            '- **`reinforced` · Planning & Semantic Interaction · Cross-direction merge.** '
            '<!-- timefirst:direction key="dynamic-orchestration-package" '
            'state="reinforced" supports="2608.14246,2608.09254" confidence="low" '
            'implication="reject-cross-key-merge~cross-key-evidence-merge" '
            'time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" '
            'synthesized="2026-08-20T00:00:00Z" prior="field-map" --> '
            'Support: [Polaris](#entry-2608-14246), [Business Truth](#entry-2608-09254); '
            'confidence: **low**. Implication: reject the cross key evidence merge as reinforcement. '
            'Time basis: `legacy_publication_date`, **not Radar acceptance**. '
            'Last synthesized: **2026-08-20T00:00:00Z (UTC)**. '
            'Prior map evidence: [Field Map](#field-map).'
        )
        zh = replace_once(zh, zh_lines[1], zh_combined)
        zh = replace_once(zh, zh_lines[2] + "\n", "")
        en = replace_once(en, en_lines[1], en_combined)
        en = replace_once(en, en_lines[2] + "\n", "")

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "2608.09254" in error
                and "direction_keys" in error
                and "dynamic-orchestration-package" in error
                for error in errors
            ),
            errors,
        )

    def test_polaris_and_business_truth_reinforced_with_prior_none_is_rejected(self):
        records, zh, en = self.inputs()
        zh_lines = [line for line in zh.splitlines() if "timefirst:direction" in line]
        en_lines = [line for line in en.splitlines() if "timefirst:direction" in line]
        zh_combined = (
            '- **`reinforced` · Planning & Semantic Interaction · 缺少地图先验。** '
            '<!-- timefirst:direction key="dynamic-orchestration-package" '
            'state="reinforced" supports="2608.14246,2608.09254" confidence="low" '
            'implication="reject-priorless-merge~missing-independent-map-prior" '
            'time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" '
            'synthesized="2026-08-20T00:00:00Z" prior="none" --> '
            '支撑：[Polaris](#entry-2608-14246)，[Business Truth](#entry-2608-09254)；'
            '置信度：**低**。含义：这是 missing independent map prior 的强化。'
            '时间基准：`legacy_publication_date`，**not Radar acceptance**。'
            '最后合成：**2026-08-20T00:00:00Z (UTC)**。'
            '先验地图证据：**none**。'
        )
        en_combined = (
            '- **`reinforced` · Planning & Semantic Interaction · Missing map prior.** '
            '<!-- timefirst:direction key="dynamic-orchestration-package" '
            'state="reinforced" supports="2608.14246,2608.09254" confidence="low" '
            'implication="reject-priorless-merge~missing-independent-map-prior" '
            'time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" '
            'synthesized="2026-08-20T00:00:00Z" prior="none" --> '
            'Support: [Polaris](#entry-2608-14246), [Business Truth](#entry-2608-09254); '
            'confidence: **low**. Implication: this reinforcement has missing independent map prior evidence. '
            'Time basis: `legacy_publication_date`, **not Radar acceptance**. '
            'Last synthesized: **2026-08-20T00:00:00Z (UTC)**. '
            'Prior map evidence: **none**.'
        )
        zh = replace_once(zh, zh_lines[1], zh_combined)
        zh = replace_once(zh, zh_lines[2] + "\n", "")
        en = replace_once(en, en_lines[1], en_combined)
        en = replace_once(en, en_lines[2] + "\n", "")

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "legacy_publication_date adapter requires state=new_signal" in error
                for error in errors
            ),
            errors,
        )

    def test_same_key_legacy_reinforcement_with_prior_field_map_is_rejected(self):
        records, zh, en = self.inputs()
        records[0]["direction_keys"] = [
            "dynamic-orchestration-package",
            "shared-enterprise-analytics-direction",
        ]
        records[1]["direction_keys"] = [
            "business-truth-safety-contract",
            "shared-enterprise-analytics-direction",
        ]
        zh_lines = [line for line in zh.splitlines() if "timefirst:direction" in line]
        en_lines = [line for line in en.splitlines() if "timefirst:direction" in line]
        zh_combined = (
            '- **`reinforced` · Enterprise analytics · 同方向合成。** '
            '<!-- timefirst:direction key="shared-enterprise-analytics-direction" '
            'state="reinforced" supports="2608.14246,2608.09254" confidence="medium" '
            'implication="match-enterprise-controls~matched-enterprise-control-evidence" '
            'time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" '
            'synthesized="2026-08-20T00:00:00Z" prior="field-map" --> '
            '支撑：[Polaris](#entry-2608-14246)，[Business Truth](#entry-2608-09254)；'
            '置信度：**中**。含义：需要 matched enterprise control evidence 形成判断。'
            '时间基准：`legacy_publication_date`，**not Radar acceptance**。'
            '最后合成：**2026-08-20T00:00:00Z (UTC)**。'
            '先验地图证据：[领域地图](#field-map)。'
        )
        en_combined = (
            '- **`reinforced` · Enterprise analytics · Same-direction synthesis.** '
            '<!-- timefirst:direction key="shared-enterprise-analytics-direction" '
            'state="reinforced" supports="2608.14246,2608.09254" confidence="medium" '
            'implication="match-enterprise-controls~matched-enterprise-control-evidence" '
            'time_basis="legacy_publication_date" non_acceptance="not-radar-acceptance" '
            'synthesized="2026-08-20T00:00:00Z" prior="field-map" --> '
            'Support: [Polaris](#entry-2608-14246), [Business Truth](#entry-2608-09254); '
            'confidence: **medium**. Implication: require matched enterprise control evidence in evaluation. '
            'Time basis: `legacy_publication_date`, **not Radar acceptance**. '
            'Last synthesized: **2026-08-20T00:00:00Z (UTC)**. '
            'Prior map evidence: [Field Map](#field-map).'
        )
        zh = replace_once(zh, zh_lines[1], zh_combined)
        zh = replace_once(zh, zh_lines[2] + "\n", "")
        en = replace_once(en, en_lines[1], en_combined)
        en = replace_once(en, en_lines[2] + "\n", "")

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "legacy_publication_date adapter requires state=new_signal" in error
                for error in errors
            ),
            errors,
        )

    def test_one_legacy_paper_cannot_claim_a_revised_direction(self):
        records, zh, en = self.inputs()
        for old, new in (
            ('state="new_signal"', 'state="revised"'),
            ("**`new_signal`", "**`revised`"),
        ):
            zh = zh.replace(old, new, 1)
            en = en.replace(old, new, 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(
            any(
                "legacy_publication_date adapter requires state=new_signal" in error
                for error in errors
            ),
            errors,
        )

    def test_one_legacy_paper_visible_prose_cannot_claim_a_durable_trend(self):
        records, zh, en = self.inputs()
        zh = replace_once(
            zh,
            "动态编排目前只构成整套系统层面的新信号",
            "该方向已形成稳定趋势",
        )
        en = replace_once(
            en,
            "Dynamic orchestration remains a packaged-system signal",
            "This is a reinforced durable trend",
        )
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("durable/reinforced trend" in error for error in errors), errors)

    def test_one_legacy_paper_cannot_make_any_generic_trend_claim(self):
        records, zh, en = self.inputs()
        zh = sub_once(
            zh,
            r"含义：.*?。时间基准",
            "含义：这显示一种趋势。时间基准",
        )
        en = sub_once(
            en,
            r"Implication: .*?\. Time basis",
            "Implication: this points to a trend. Time basis",
        )

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(any("trend/趋势 claim" in error for error in errors), errors)

    def test_one_legacy_paper_rejects_trend_in_english_indented_continuation(self):
        records, zh, en = self.inputs()
        en = replace_once(
            en,
            '\n\n<a id="last-30-days"></a>',
            '\n  This indented continuation calls it a trend.\n\n'
            '<a id="last-30-days"></a>',
        )

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "README.en.md" in error
                and "last-7-days" in error
                and "trend/趋势 claim" in error
                for error in errors
            ),
            errors,
        )

    def test_one_legacy_paper_rejects_trend_in_chinese_indented_continuation(self):
        records, zh, en = self.inputs()
        zh = replace_once(
            zh,
            '\n\n<a id="last-30-days"></a>',
            '\n  这个缩进续行称其为趋势。\n\n<a id="last-30-days"></a>',
        )

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "README.md" in error
                and "last-7-days" in error
                and "trend/趋势 claim" in error
                for error in errors
            ),
            errors,
        )

    def test_one_legacy_paper_rejects_trend_in_english_attached_paragraph(self):
        records, zh, en = self.inputs()
        en = replace_once(
            en,
            '\n\n<a id="last-30-days"></a>',
            '\n\nThis attached paragraph calls it a trend.\n\n'
            '<a id="last-30-days"></a>',
        )

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "README.en.md" in error
                and "last-7-days" in error
                and "trend/趋势 claim" in error
                for error in errors
            ),
            errors,
        )

    def test_one_legacy_paper_rejects_trend_in_chinese_attached_paragraph(self):
        records, zh, en = self.inputs()
        zh = replace_once(
            zh,
            '\n\n<a id="last-30-days"></a>',
            '\n\n这个附着段落称其为趋势。\n\n<a id="last-30-days"></a>',
        )

        errors = validate_period_contracts(records, zh, en)

        self.assertTrue(
            any(
                "README.md" in error
                and "last-7-days" in error
                and "trend/趋势 claim" in error
                for error in errors
            ),
            errors,
        )

    def test_next_period_and_field_map_prose_are_outside_direction_blocks(self):
        records, base_zh, base_en = self.inputs()
        mutations = (
            (
                "next-period",
                '<a id="last-30-days"></a>\n',
                '<a id="last-30-days"></a>\n\n'
                '下一个时间窗的趋势说明不属于上一条 direction。\n',
                '<a id="last-30-days"></a>\n\n'
                'The next period trend prose does not belong to the prior direction.\n',
            ),
            (
                "field-map",
                '<a id="field-map"></a>\n',
                '<a id="field-map"></a>\n\n这是领域地图的趋势说明。\n',
                '<a id="field-map"></a>\n\nThis is Field Map trend prose.\n',
            ),
        )
        for boundary, marker, zh_replacement, en_replacement in mutations:
            with self.subTest(boundary=boundary):
                zh = replace_once(base_zh, marker, zh_replacement)
                en = replace_once(base_en, marker, en_replacement)

                errors = validate_period_contracts(records, zh, en)

                self.assertEqual([], errors)

    def test_direction_metadata_parity_is_binding(self):
        records, zh, en = self.inputs()
        en = en.replace('confidence="low"', 'confidence="medium"', 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("direction parity" in error for error in errors), errors)

    def test_radar_acceptance_visible_claim_is_rejected(self):
        records, zh, en = self.inputs()
        old = "`legacy_publication_date`，**not Radar acceptance**"
        zh = zh.replace(old, "`legacy_publication_date`，**Radar acceptance**", 1)
        old = "`legacy_publication_date`, **not Radar acceptance**"
        en = en.replace(old, "`legacy_publication_date`, **Radar acceptance**", 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("non_acceptance" in error for error in errors), errors)

    def test_period_time_basis_must_match_support_provenance(self):
        records, zh, en = self.inputs()
        zh = zh.replace('time_basis="legacy_publication_date"', 'time_basis="radar_published_at"', 1)
        en = en.replace('time_basis="legacy_publication_date"', 'time_basis="radar_published_at"', 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("native_v2" in error for error in errors), errors)

    def test_last_synthesis_timestamp_and_timezone_are_paired(self):
        records, zh, en = self.inputs()
        en = en.replace("2026-08-20T00:00:00Z (UTC)", "2026-08-20T01:00:00Z (UTC)", 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("synthesis timestamp" in error for error in errors), errors)

    def test_paired_period_windows_cannot_shift_from_the_current_dates(self):
        records, zh, en = self.inputs()
        for old, new in (
            ("2026-08-14—2026-08-20", "2026-08-13—2026-08-19"),
            ("2026-07-22—2026-08-20", "2026-07-21—2026-08-19"),
        ):
            zh = zh.replace(old, new, 1)
            en = en.replace(old, new, 1)
        errors = validate_period_contracts(records, zh, en)
        self.assertTrue(any("current expected window" in error for error in errors), errors)

    def test_data_period_sections_require_exactly_one_visible_date_range(self):
        records, base_zh, base_en = self.inputs()
        fixtures = (
            (
                "last-7-days",
                "2026-08-14—2026-08-20",
                "2026-08-13—2026-08-19",
            ),
            (
                "last-30-days",
                "2026-07-22—2026-08-20",
                "2026-07-21—2026-08-19",
            ),
        )
        for anchor, correct, contradictory in fixtures:
            for mutation, replacement in (
                ("zero", ""),
                ("duplicate", f"{correct}\n\n{contradictory}"),
            ):
                with self.subTest(anchor=anchor, mutation=mutation):
                    zh = base_zh.replace(correct, replacement, 1)
                    en = base_en.replace(correct, replacement, 1)
                    errors = validate_period_contracts(records, zh, en)
                    self.assertTrue(
                        any(
                            anchor in error
                            and "exactly one visible date range" in error
                            for error in errors
                        ),
                        errors,
                    )

    def test_polaris_note_bounds_metrics_and_reproduction_claim(self):
        zh_note = (ROOT / "papers" / "2608.14246.md").read_text(encoding="utf-8")
        en_note = (ROOT / "papers" / "2608.14246.en.md").read_text(encoding="utf-8")
        for text in (zh_note, en_note):
            self.assertIn("retrieved-context semantic similarity", text)
            self.assertIn("context precision", text)
            self.assertIn("final-response answer relevancy", text)
            self.assertNotIn("visualization-related outputs", text)
            self.assertIn("no code/reproduction link", text)


class FamilyRouteVisibilityContractTest(unittest.TestCase):
    def test_hidden_exact_routes_cannot_rescue_wrong_visible_routes(self):
        exact = """[Agent Benchmark](https://github.com/H20Zhang/Agent-Benchmark-Radar)
[Agent Memory](https://github.com/H20Zhang/Agent-Memory-Radar)
[Agentic RAG](https://github.com/H20Zhang/Agentic-RAG-Radar)
[Data Agent evaluation](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)
"""
        visible = """[Agent Benchmark](https://github.com/H20Zhang/Agent-Benchmark-Radar#wrong)
[Agent Memory](https://github.com/H20Zhang/Agent-Memory-Radar#wrong)
[Agentic RAG](https://github.com/H20Zhang/Agentic-RAG-Radar#wrong)
[Data Agent evaluation](https://github.com/H20Zhang/Agent-Benchmark-Radar#wrong)
"""
        errors: list[str] = []
        family_routes(visible + f"<!--\n{exact}-->", "README.md", errors)
        self.assertEqual(4, len(errors), errors)


class DataAliasVisibilityContractTest(unittest.TestCase):
    def test_hidden_alias_cannot_satisfy_or_duplicate_visible_changes_alias(self):
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        en = (ROOT / "README.en.md").read_text(encoding="utf-8")
        anchor = '<a id="changes"></a>'

        hidden_only = zh.replace(anchor, f"<!-- {anchor} -->", 1)
        errors = data_validator.validate_data_aliases(hidden_only, en)
        self.assertTrue(
            any("missing Data compatibility alias changes" in error for error in errors),
            errors,
        )

        hidden_decoy = zh.replace(anchor, f"<!-- {anchor} -->{anchor}", 1)
        self.assertEqual([], data_validator.validate_data_aliases(hidden_decoy, en))

if __name__ == "__main__":
    unittest.main()
