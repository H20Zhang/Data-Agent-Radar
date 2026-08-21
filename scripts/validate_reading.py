#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

from no_public_runs import validate_authoritative_docs, validate_no_public_runs
from timefirst_contract import strip_html_comments, validate_pair

ROOT = Path(__file__).resolve().parents[1]
ZH, EN = ROOT / "README.md", ROOT / "README.en.md"
LIB_ZH, LIB_EN = ROOT / "library/README.md", ROOT / "library/README.en.md"
REGISTRY = ROOT / "data/papers.json"
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
ENTRY_ANCHOR_RE = re.compile(r'<a\s+id=["\']entry-([^"\']+)["\']\s*></a>', re.I)
DATA_NOTE_RE = re.compile(r"\[[^\]]+\]\(papers/(?P<identity>\d{4}\.\d+)(?P<english>\.en)?\.md\)")
RANGE_RE = re.compile(r"(?P<start>\d{4}-\d{2}-\d{2})\s*[—–]\s*(?P<end>\d{4}-\d{2}-\d{2})")
SUMMARY_RE = re.compile(r"<details>\s*<summary>(?P<summary>.*?)</summary>", re.I | re.S)
VISIBLE_MAP_RE = re.compile(
    r"\*\*(?:Map|地图)(?:[.。:：])?\*\*.*?"
    r"`(none|early_signal|reinforces|revises|splits|retires)`",
    re.I | re.S,
)
DIRECTION_COMMENT_RE = re.compile(
    r"<!--\s*timefirst:direction\s+(?P<attributes>.*?)\s*-->", re.I
)
DIRECTION_ATTRIBUTE_RE = re.compile(
    r'(?P<name>[a-z_]+)="(?P<value>[^"]*)"', re.I
)
DIRECTION_STATE_LABEL_RE = re.compile(
    r"\*\*`(?P<value>new_signal|reinforced|revised|splits|retires|no_material_change)`",
    re.I,
)
DIRECTION_STATE_VALUE_RE = re.compile(
    r"\*\*`(?P<value>new_signal|reinforced|revised|splits|retires|no_material_change)`\s*·",
    re.I,
)
DIRECTION_HEADING_RE = re.compile(
    r"^\s*-\s+\*\*`(?P<state>new_signal|reinforced|revised|splits|retires|no_material_change)`"
    r"\s*·\s*(?P<heading>.*?)\*\*",
    re.I | re.M,
)
PERIOD_SUPPORT_RE = re.compile(r"\[[^\]]+\]\(#entry-([^)]+)\)", re.I)
VISIBLE_DIRECTION_LABELS = {
    "README.md": {
        "state": DIRECTION_STATE_LABEL_RE,
        "supports": re.compile(r"支撑"),
        "confidence": re.compile(r"置信度"),
        "time basis": re.compile(r"时间基准"),
        "non-acceptance": re.compile(r"\b(?:not\s+)?Radar\s+acceptance\b", re.I),
        "synthesis": re.compile(r"最后合成"),
        "implication": re.compile(r"含义"),
        "prior": re.compile(r"先验地图证据"),
    },
    "README.en.md": {
        "state": DIRECTION_STATE_LABEL_RE,
        "supports": re.compile(r"\bSupport\b", re.I),
        "confidence": re.compile(r"\bconfidence\b", re.I),
        "time basis": re.compile(r"\bTime basis\b", re.I),
        "non-acceptance": re.compile(r"\b(?:not\s+)?Radar\s+acceptance\b", re.I),
        "synthesis": re.compile(r"\bLast synthesized\b", re.I),
        "implication": re.compile(r"\bImplication\b", re.I),
        "prior": re.compile(r"\bPrior map evidence\b", re.I),
    },
}
VISIBLE_DIRECTION_VALUES = {
    "README.md": {
        "state": DIRECTION_STATE_VALUE_RE,
        "supports": re.compile(r"支撑\s*：\s*(?P<value>.*?)[；;]", re.S),
        "confidence": re.compile(
            r"置信度\s*：\s*\*\*(?P<value>low|medium|high|低|中|高)\*\*",
            re.I,
        ),
        "time basis": re.compile(
            r"时间基准\s*：\s*`(?P<value>[^`\n]+)`\s*[，,]\s*"
            r"\*\*(?:not\s+)?Radar\s+acceptance\*\*",
            re.I,
        ),
        "non-acceptance": re.compile(
            r"(?P<value>(?:not\s+)?Radar\s+acceptance)", re.I
        ),
        "synthesis": re.compile(
            r"最后合成\s*：\s*\*\*"
            r"(?P<value>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\s*"
            r"\([A-Za-z0-9_+\-/]+\))\*\*",
            re.I,
        ),
        "implication": re.compile(
            r"含义\s*：\s*(?P<value>.*?)(?=\s*时间基准\s*：)",
            re.I | re.S,
        ),
        "prior": re.compile(
            r"先验地图证据\s*：\s*(?P<value>[^\n。；]+)[。；]",
            re.I,
        ),
    },
    "README.en.md": {
        "state": DIRECTION_STATE_VALUE_RE,
        "supports": re.compile(
            r"\bSupport\s*:\s*(?P<value>.*?);", re.I | re.S
        ),
        "confidence": re.compile(
            r"\bconfidence\s*:\s*\*\*(?P<value>low|medium|high)\*\*",
            re.I,
        ),
        "time basis": re.compile(
            r"\bTime basis\s*:\s*`(?P<value>[^`\n]+)`\s*,\s*"
            r"\*\*(?:not\s+)?Radar\s+acceptance\*\*",
            re.I,
        ),
        "non-acceptance": re.compile(
            r"(?P<value>(?:not\s+)?Radar\s+acceptance)", re.I
        ),
        "synthesis": re.compile(
            r"\bLast synthesized\s*:\s*\*\*"
            r"(?P<value>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\s*"
            r"\([A-Za-z0-9_+\-/]+\))\*\*",
            re.I,
        ),
        "implication": re.compile(
            r"\bImplication\s*:\s*(?P<value>.*?)(?=\s*Time basis\s*:)",
            re.I | re.S,
        ),
        "prior": re.compile(
            r"\bPrior map evidence\s*:\s*(?P<value>[^\n.;]+)[.;]",
            re.I,
        ),
    },
}
VISIBLE_SYNTHESIS_VALUE_RE = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s*"
    r"\((?P<timezone>[A-Za-z0-9_+\-/]+)\)",
    re.I,
)
STRICT_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
STABLE_TOKEN_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
IMPLICATION_CONTRACT_RE = re.compile(
    r"^(?P<key>[a-z0-9][a-z0-9._-]*)~"
    r"(?P<witness>[a-z0-9][a-z0-9._-]*)$"
)
DURABLE_TREND_RE = re.compile(
    r"\b(?:durable|established|reinforced)\s+trend\b|"
    r"\btrend\s+(?:is\s+)?(?:durable|established|reinforced)\b|"
    r"\breinforces?\s+(?:the\s+)?trend\b|"
    r"(?:已形成|形成了|已成|巩固|强化|确立)(?:长期|稳定|可靠)?趋势|"
    r"趋势(?:已经|已)?(?:形成|巩固|强化|确立)",
    re.I,
)
ANY_TREND_CLAIM_RE = re.compile(r"\btrend(?:s|ed|ing)?\b|趋势", re.I)
ALLOWED_MAP_DELTAS = {"none", "early_signal", "reinforces", "revises", "splits", "retires"}
LEGACY_CONTEXT_MAP_DELTAS = {"none", "early_signal"}
ALLOWED_PROVENANCE = {"legacy_unknown", "native_v2"}
V2_FIELDS = (
    "published_at",
    "first_seen_at",
    "radar_published_at",
    "time_provenance",
    "map_delta",
)
ALLOWED_PROBLEMS = {
    "data_discovery_grounding",
    "planning_orchestration",
    "planning_semantic_interaction",
    "execution_transformation",
    "verification_recovery",
    "learning_reuse",
}
PROBLEM_LABELS = {
    "data_discovery_grounding": "Data Discovery & Grounding",
    "planning_orchestration": "Planning & Semantic Interaction",
    "planning_semantic_interaction": "Planning & Semantic Interaction",
    "execution_transformation": "Execution & Transformation",
    "verification_recovery": "Verification & Recovery",
    "learning_reuse": "Learning & Reuse",
}
MAP_SUPPORT_MINIMUM = {
    "reinforces": 2,
    "revises": 2,
    "splits": 2,
    "retires": 2,
}
CONFIDENCE_VALUES = {"low", "medium", "high"}
VISIBLE_CONFIDENCE_VALUES = {
    "low": "low",
    "medium": "medium",
    "high": "high",
    "低": "low",
    "中": "medium",
    "高": "high",
}
DIRECTION_ATTRIBUTES = (
    "key",
    "state",
    "supports",
    "confidence",
    "implication",
    "time_basis",
    "non_acceptance",
    "synthesized",
    "prior",
)
DIRECTION_STATES = {
    "new_signal",
    "reinforced",
    "revised",
    "splits",
    "retires",
    "no_material_change",
}
V2_CUTOVER = datetime(2026, 8, 20, tzinfo=timezone.utc)
SYNTHESIS_TIMESTAMP = "2026-08-20T00:00:00Z"
EXPECTED_PERIOD_WINDOWS = {
    "last-7-days": (date(2026, 8, 14), date(2026, 8, 20)),
    "last-30-days": (date(2026, 7, 22), date(2026, 8, 20)),
}
LEGACY_TIMELINE_COMPATIBILITY_IDS = (
    "2608.14246",
    "2608.09254",
    "2607.14386",
    "2606.31041",
    "2602.16720",
    "2601.15709",
)
FAMILY_ROUTES = {
    "Agent Benchmark": "https://github.com/H20Zhang/Agent-Benchmark-Radar",
    "Agent Memory": "https://github.com/H20Zhang/Agent-Memory-Radar",
    "Agentic RAG": "https://github.com/H20Zhang/Agentic-RAG-Radar",
    "Data Agent evaluation": "https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data",
}
DATA_ALIASES = ("changes",)


def _parse_date(value: object) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_utc(value: object) -> datetime | None:
    if not isinstance(value, str) or STRICT_UTC_RE.fullmatch(value) is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return None


def _rolling_window(anchor: str, cutoff: datetime) -> tuple[date, date]:
    days = 7 if anchor == "last-7-days" else 30
    return cutoff.date() - timedelta(days=days - 1), cutoff.date()


def _direction_syntheses(text: str) -> list[str]:
    values: list[str] = []
    for comment in DIRECTION_COMMENT_RE.finditer(text):
        attributes = {
            match.group("name").lower(): match.group("value")
            for match in DIRECTION_ATTRIBUTE_RE.finditer(comment.group("attributes"))
        }
        synthesized = attributes.get("synthesized")
        if synthesized is not None:
            values.append(synthesized)
    return values


def _shared_public_synthesis(zh: str, en: str) -> datetime | None:
    values = _direction_syntheses(zh) + _direction_syntheses(en)
    if not values or len(set(values)) != 1:
        return None
    return _parse_utc(values[0])


def _canonical_direction_keys(value: object) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not value:
        return None
    if any(
        not isinstance(key, str) or STABLE_TOKEN_RE.fullmatch(key) is None
        for key in value
    ):
        return None
    keys = tuple(value)
    if len(keys) != len(set(keys)):
        return None
    return keys


def _mask_html_comments(value: str) -> str:
    """Mask machine comments without changing structural offsets."""

    def mask(match: re.Match[str]) -> str:
        return "".join(
            character if character in "\r\n" else " "
            for character in match.group(0)
        )

    return HTML_COMMENT_RE.sub(mask, value)


def _anchor_matches(text: str, anchor: str) -> list[re.Match[str]]:
    return list(
        re.finditer(
            rf'<a\s+id=["\']{re.escape(anchor)}["\']\s*></a>',
            text,
            re.I,
        )
    )


def validate_data_aliases(zh: str, en: str) -> list[str]:
    """Return Data-only visible compatibility-alias cardinality violations."""

    errors: list[str] = []
    for language, raw_text in (("README.md", zh), ("README.en.md", en)):
        visible_text = strip_html_comments(raw_text)
        for alias in DATA_ALIASES:
            matches = _anchor_matches(visible_text, alias)
            if not matches:
                errors.append(f"{language}: missing Data compatibility alias {alias}")
            elif len(matches) > 1:
                errors.append(f"{language}: duplicate Data compatibility alias {alias}")
    return errors


def _effective_evidence_time(
    record: dict[str, object],
) -> tuple[date, datetime | None] | None:
    """Return honest evidence chronology without inventing legacy time-of-day."""

    if record.get("time_provenance") == "native_v2":
        radar_time = _parse_utc(record.get("radar_published_at"))
        if radar_time is None:
            return None
        return radar_time.date(), radar_time
    if record.get("time_provenance") == "legacy_unknown":
        published_date = _parse_date(record.get("published_at"))
        if published_date is None:
            return None
        return published_date, None
    return None


def _demonstrably_earlier_evidence(
    support: dict[str, object], changing: dict[str, object]
) -> bool:
    """Compare exact native times or date-level legacy evidence conservatively."""

    support_time = _effective_evidence_time(support)
    changing_time = _effective_evidence_time(changing)
    if support_time is None or changing_time is None:
        return False
    support_date, support_exact = support_time
    changing_date, changing_exact = changing_time
    if support_date != changing_date:
        return support_date < changing_date
    if support_exact is not None and changing_exact is not None:
        return support_exact < changing_exact
    return False


def validate_registry(records: list[dict[str, object]]) -> list[str]:
    """Return deterministic Data registry violations without reading the filesystem."""
    errors: list[str] = []
    if not isinstance(records, list) or not records:
        return ["data/papers.json must be a non-empty list"]
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    seen_notes: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record {index}: must be an object")
            continue
        identity = record.get("id")
        label = str(identity) if isinstance(identity, str) and identity else f"record {index}"
        for field in (
            "id",
            "title",
            "published",
            "url",
            "note_path",
            "primary_problem",
            "research_delta",
            "main_caveat",
        ):
            if not isinstance(record.get(field), str) or not str(record[field]).strip():
                errors.append(f"{label}: {field} must be a non-empty string")
        importance = record.get("importance")
        if (
            not isinstance(importance, int)
            or isinstance(importance, bool)
            or not 1 <= importance <= 5
        ):
            errors.append(f"{label}: importance must be an integer from 1 to 5")
        if record.get("primary_problem") not in ALLOWED_PROBLEMS:
            errors.append(
                f"{label}: primary_problem must be one of {sorted(ALLOWED_PROBLEMS)}"
            )

        if isinstance(identity, str):
            if identity in seen_ids:
                errors.append(f"{label}: duplicate id")
            seen_ids.add(identity)
        url = record.get("url")
        if isinstance(url, str):
            if url in seen_urls:
                errors.append(f"{label}: duplicate URL")
            seen_urls.add(url)
            if isinstance(identity, str) and re.fullmatch(r"\d{4}\.\d+", identity):
                canonical = f"https://arxiv.org/abs/{identity}"
                if url != canonical:
                    errors.append(f"{label}: canonical primary URL must be {canonical}")
        note_path = record.get("note_path")
        if isinstance(note_path, str):
            if note_path in seen_notes:
                errors.append(f"{label}: duplicate note_path")
            seen_notes.add(note_path)
            if isinstance(identity, str) and re.fullmatch(r"\d{4}\.\d+", identity):
                expected = f"papers/{identity}.md"
                if note_path != expected:
                    errors.append(f"{label}: note_path must be {expected}")

        published = _parse_date(record.get("published"))
        if published is None:
            errors.append(f"{label}: published must be an ISO date")
        if record.get("status") != "public":
            errors.append(f"{label}: status must be public; candidate states stay private")

        direction_keys_present = "direction_keys" in record
        if direction_keys_present and _canonical_direction_keys(
            record.get("direction_keys")
        ) is None:
            errors.append(
                f"{label}: direction_keys must be a non-empty list of unique "
                "lowercase stable tokens"
            )

        present_v2 = {field for field in V2_FIELDS if field in record}
        if not present_v2:
            if direction_keys_present:
                errors.append(f"{label}: direction_keys requires the complete v2 bundle")
            continue
        missing_v2 = [field for field in V2_FIELDS if field not in record]
        if missing_v2:
            for field in missing_v2:
                errors.append(
                    f"{label}: any v2 field requires the complete v2 field {field}"
                )
            continue

        if record.get("map_delta") not in ALLOWED_MAP_DELTAS:
            errors.append(f"{label}: map_delta must be one of {sorted(ALLOWED_MAP_DELTAS)}")
        provenance = record.get("time_provenance")
        if provenance not in ALLOWED_PROVENANCE:
            errors.append(f"{label}: time_provenance must be legacy_unknown or native_v2")
        first_seen, radar_published = record.get("first_seen_at"), record.get("radar_published_at")
        if provenance == "legacy_unknown":
            published_at = _parse_date(record.get("published_at"))
            if published_at is None:
                errors.append(f"{label}: legacy_unknown published_at must be an ISO date")
            if published is not None and published_at is not None and published != published_at:
                errors.append(f"{label}: published_at must preserve published date parity")
            if first_seen is not None:
                errors.append(f"{label}: legacy_unknown first_seen_at must be null")
            if radar_published is not None:
                errors.append(f"{label}: legacy_unknown radar_published_at must be null")
            if record.get("map_delta") not in LEGACY_CONTEXT_MAP_DELTAS:
                errors.append(
                    f"{label}: legacy_unknown map_delta must be none or early_signal"
                )
        elif provenance == "native_v2":
            published_dt = _parse_utc(record.get("published_at"))
            first_dt, radar_dt = _parse_utc(first_seen), _parse_utc(radar_published)
            if published_dt is None:
                errors.append(f"{label}: native_v2 published_at must be a UTC timestamp")
            elif published is not None and published != published_dt.date():
                errors.append(
                    f"{label}: native_v2 published date parity must match "
                    "published_at calendar date"
                )
            if first_dt is None:
                errors.append(f"{label}: native_v2 first_seen_at must be a UTC timestamp")
            if radar_dt is None:
                errors.append(f"{label}: native_v2 radar_published_at must be a UTC timestamp")
            if (
                published_dt is not None
                and first_dt is not None
                and radar_dt is not None
                and not published_dt <= first_dt <= radar_dt
            ):
                errors.append(
                    f"{label}: timestamp chronology requires "
                    "published_at <= first_seen_at <= radar_published_at"
                )
            if radar_dt is not None and radar_dt < V2_CUTOVER:
                errors.append(
                    f"{label}: native_v2 radar_published_at cannot predate v2 cutover"
                )

    record_by_id = {
        str(record.get("id")): record
        for record in records
        if isinstance(record, dict) and isinstance(record.get("id"), str)
    }
    canonical_ids = set(record_by_id)
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        identity = str(record.get("id", f"record {index}"))
        delta = record.get("map_delta")
        if delta in MAP_SUPPORT_MINIMUM:
            supports = record.get("map_support_ids")
            if not isinstance(supports, list) or not all(
                isinstance(item, str) and item for item in supports
            ):
                errors.append(
                    f"{identity}: {delta} requires explicit canonical map_support_ids"
                )
                continue
            if len(supports) != len(set(supports)):
                errors.append(f"{identity}: map_support_ids must not contain duplicates")
            minimum = MAP_SUPPORT_MINIMUM[str(delta)]
            if len(set(supports)) < minimum:
                errors.append(
                    f"{identity}: {delta} map_support_ids require at least {minimum} "
                    "distinct canonical records, including independent prior-map support"
                )
            if identity not in supports:
                errors.append(
                    f"{identity}: map_support_ids must include the changing record identity"
                )
            unknown = [support for support in supports if support not in canonical_ids]
            if unknown:
                errors.append(
                    f"{identity}: map_support_ids contain unknown canonical identities {unknown}"
                )
            earlier_supports = [
                support
                for support in supports
                if support != identity
                and support in record_by_id
                and _demonstrably_earlier_evidence(
                    record_by_id[support], record
                )
            ]
            if not earlier_supports:
                errors.append(
                    f"{identity}: {delta} map_support_ids require at least one "
                    "independent canonical support with demonstrably earlier effective "
                    "evidence time; native records use radar_published_at, legacy records "
                    "use published_at date precision, and mixed same-day order is unknown"
                )
        elif record.get("map_support_ids") not in (None, []):
            errors.append(
                f"{identity}: map_support_ids are only valid for durable map transitions"
            )
    return errors


def _timeline_chunks(text: str) -> list[tuple[str, str]]:
    structural = _mask_html_comments(text)
    timeline_matches = _anchor_matches(structural, "timeline")
    period_matches = _anchor_matches(structural, "periods")
    if not timeline_matches or not period_matches:
        return []
    start, end = timeline_matches[0].start(), period_matches[0].start()
    if end <= start:
        return []
    timeline = text[start:end]
    structural_timeline = structural[start:end]
    anchors = list(ENTRY_ANCHOR_RE.finditer(structural_timeline))
    return [
        (
            anchor.group(1),
            timeline[
                anchor.end() : (
                    anchors[index + 1].start()
                    if index + 1 < len(anchors)
                    else len(timeline)
                )
            ],
        )
        for index, anchor in enumerate(anchors)
    ]


def validate_data_note_links(zh: str, en: str) -> list[str]:
    errors: list[str] = []
    for language, text in (("README.md", zh), ("README.en.md", en)):
        for identity, chunk in _timeline_chunks(text):
            zh_notes: set[str] = set()
            en_notes: set[str] = set()
            for match in DATA_NOTE_RE.finditer(strip_html_comments(chunk)):
                (en_notes if match.group("english") else zh_notes).add(match.group("identity").replace(".", "-", 1))
            if identity not in zh_notes or identity not in en_notes:
                errors.append(f"{language}: entry identity {identity} needs corresponding Chinese and English deep-note links")
    return errors


def _visible_text(value: str) -> str:
    value = strip_html_comments(value)
    value = re.sub(r"<[^>]+>", "", value)
    return value.strip()


def _summary_parts(chunk: str) -> tuple[str, str, str] | None:
    match = SUMMARY_RE.search(chunk)
    if match is None:
        return None
    visible = _visible_text(match.group("summary"))
    parts = [part.strip() for part in visible.split(" · ", 2)]
    if len(parts) != 3 or " — " not in parts[2]:
        return None
    area = parts[2].split(" — ", 1)[0].strip()
    return parts[0], parts[1], area


def _expected_timeline_order(
    records: list[dict[str, object]], synthesis_cutoff: datetime
) -> list[str]:
    """Return in-cutoff native acceptances, followed by fixed legacy order."""

    native: list[tuple[datetime, str]] = []
    current_window = _rolling_window("last-30-days", synthesis_cutoff)
    record_by_id = {
        str(record.get("id")): record
        for record in records
        if isinstance(record, dict) and isinstance(record.get("id"), str)
    }
    for identity, record in record_by_id.items():
        if record.get("time_provenance") != "native_v2":
            continue
        radar_time = _parse_utc(record.get("radar_published_at"))
        if (
            radar_time is not None
            and current_window[0] <= radar_time.date() <= current_window[1]
            and radar_time <= synthesis_cutoff
        ):
            native.append((radar_time, identity.replace(".", "-", 1)))
    native.sort(key=lambda item: (-item[0].timestamp(), item[1]))

    legacy = [
        identity.replace(".", "-", 1)
        for identity in LEGACY_TIMELINE_COMPATIBILITY_IDS
        if identity in record_by_id
        and record_by_id[identity].get("time_provenance") == "legacy_unknown"
    ]
    return [identity for _, identity in native] + legacy


def validate_registry_projection(
    records: list[dict[str, object]], zh: str, en: str
) -> list[str]:
    """Bind each public Timeline identity to exactly one canonical registry record."""
    errors: list[str] = []
    record_by_anchor = {
        str(record.get("id", "")).replace(".", "-", 1): record for record in records
    }
    synthesis_cutoff = _shared_public_synthesis(zh, en)
    if synthesis_cutoff is None:
        return ["Data projection needs one exact shared public synthesis cutoff"]
    expected_order = _expected_timeline_order(records, synthesis_cutoff)
    for language, text in (("README.md", zh), ("README.en.md", en)):
        chunks = _timeline_chunks(text)
        identities = [identity for identity, _ in chunks]
        if identities != expected_order:
            errors.append(
                f"{language}: Timeline violates full Radar timestamp order or fixed legacy order"
            )
        for identity, chunk in chunks:
            record = record_by_anchor.get(identity)
            if record is None:
                errors.append(f"{language}: Timeline identity {identity} has no canonical registry record")
                continue
            if record.get("time_provenance") == "native_v2":
                radar_time = _parse_utc(record.get("radar_published_at"))
                if radar_time is not None and radar_time > synthesis_cutoff:
                    errors.append(
                        f"{language}: Timeline identity {identity} is after public "
                        f"synthesis cutoff {synthesis_cutoff.strftime('%Y-%m-%dT%H:%M:%SZ')}"
                    )
            visible_chunk = strip_html_comments(chunk)
            summary = _summary_parts(visible_chunk)
            if summary is None:
                errors.append(f"{language}: entry identity {identity} has no parseable summary")
            else:
                displayed_date, _, visible_problem = summary
                if record.get("time_provenance") == "native_v2":
                    radar_time = _parse_utc(record.get("radar_published_at"))
                    expected_date = radar_time.date().isoformat() if radar_time else None
                else:
                    expected_date = record.get("published_at")
                if displayed_date != expected_date:
                    errors.append(
                        f"{language}: entry identity {identity} displayed date does not "
                        "match its canonical time basis"
                    )
                expected_problem = PROBLEM_LABELS.get(str(record.get("primary_problem")))
                if visible_problem != expected_problem:
                    errors.append(
                        f"{language}: entry identity {identity} visible field-map problem "
                        "does not match canonical primary_problem"
                    )
            map_match = VISIBLE_MAP_RE.search(visible_chunk)
            visible_map = map_match.group(1).lower() if map_match else None
            if visible_map != record.get("map_delta"):
                errors.append(
                    f"{language}: entry identity {identity} visible map token does not "
                    "match canonical map_delta"
                )
            targets = [
                raw.strip().strip("<>") for raw in LINK_RE.findall(visible_chunk)
            ]
            canonical_url = str(record.get("url", ""))
            primary_urls = [target for target in targets if target.startswith("https://arxiv.org/abs/")]
            if primary_urls != [canonical_url]:
                errors.append(f"{language}: entry identity {identity} needs exactly one canonical primary URL")
            note = str(record.get("note_path", ""))
            english_note = re.sub(r"\.md$", ".en.md", note)
            if targets.count(note) != 1 or targets.count(english_note) != 1:
                errors.append(f"{language}: entry identity {identity} needs one-to-one canonical paired note links")
    return errors


def _period_section(text: str, anchor: str, next_anchor: str) -> str:
    structural = _mask_html_comments(text)
    starts = _anchor_matches(structural, anchor)
    ends = _anchor_matches(structural, next_anchor)
    if not starts or not ends:
        return ""
    start, end = starts[0].start(), ends[0].start()
    return text[start:end] if end > start else ""


def _support_identity(anchor_identity: str) -> str:
    return anchor_identity.replace("-", ".", 1)


def _direction_item_blocks(section: str) -> list[tuple[int, str]]:
    """Return complete visible direction items bounded by the next item."""

    lines = section.splitlines()
    visible_lines = _mask_html_comments(section).splitlines()
    starts = [
        index
        for index, visible_line in enumerate(visible_lines)
        if DIRECTION_HEADING_RE.search(visible_line) is not None
    ]
    return [
        (
            start + 1,
            "\n".join(
                lines[
                    start : starts[position + 1]
                    if position + 1 < len(starts)
                    else len(lines)
                ]
            ),
        )
        for position, start in enumerate(starts)
    ]


def _parse_direction_items(
    language: str,
    anchor: str,
    section: str,
    window: tuple[date, date],
    expected_synthesis: str,
    record_by_id: dict[str, dict[str, object]],
    errors: list[str],
) -> list[tuple[str, str, tuple[str, ...], str, str, str, str, str, str]]:
    """Parse one structured direction layer under its declared time adapter."""
    items: list[
        tuple[str, str, tuple[str, ...], str, str, str, str, str, str]
    ] = []
    seen_keys: set[str] = set()
    projection_language = (
        language if language in VISIBLE_DIRECTION_LABELS else "README.md"
    )
    label_patterns = VISIBLE_DIRECTION_LABELS[projection_language]
    value_patterns = VISIBLE_DIRECTION_VALUES[projection_language]
    for line_number, raw_block in _direction_item_blocks(section):
        location = f"{language}: {anchor} direction at line {line_number}"
        visible_block = strip_html_comments(raw_block)
        label_matches = {
            name: list(pattern.finditer(visible_block))
            for name, pattern in label_patterns.items()
        }
        visible_values: dict[str, str] = {}
        for name, matches in label_matches.items():
            if len(matches) != 1:
                errors.append(f"{location} requires exactly one visible {name} field")
                continue
            value_match = value_patterns[name].match(
                visible_block, matches[0].start()
            )
            if value_match is None or not value_match.group("value").strip():
                errors.append(
                    f"{location} requires exactly one visible {name} field "
                    "with valid structure"
                )
                continue
            visible_values[name] = value_match.group("value").strip()

        comments = list(DIRECTION_COMMENT_RE.finditer(raw_block))
        if len(comments) != 1:
            errors.append(f"{location} requires exactly one stable direction metadata block")
            continue

        attributes: dict[str, list[str]] = {
            name: [] for name in DIRECTION_ATTRIBUTES
        }
        for match in DIRECTION_ATTRIBUTE_RE.finditer(comments[0].group("attributes")):
            name = match.group("name").lower()
            if name in attributes:
                attributes[name].append(match.group("value"))
        complete = True
        for name, values in attributes.items():
            if len(values) != 1 or not values[0]:
                errors.append(f"{location} requires exactly one non-empty {name} value")
                complete = False
        if not complete:
            continue

        values = {name: found[0] for name, found in attributes.items()}
        key = values["key"]
        state = values["state"]
        synthesized = values["synthesized"]
        synthesized_time = _parse_utc(synthesized)
        prior = values["prior"]
        supports = (
            ()
            if values["supports"] == "none"
            else tuple(
                item.strip()
                for item in values["supports"].split(",")
                if item.strip()
            )
        )
        if state not in DIRECTION_STATES:
            errors.append(f"{location} has invalid direction state {state}")
        visible_state = visible_values.get("state")
        if visible_state is None or visible_state.lower() != state:
            errors.append(f"{location} visible state and stable direction state drift")
        for name in ("key", "non_acceptance", "prior"):
            if STABLE_TOKEN_RE.fullmatch(values[name]) is None:
                errors.append(f"{location} {name} must be a lowercase stable token")
        confidence = values["confidence"]
        if confidence not in CONFIDENCE_VALUES:
            errors.append(
                f"{location} confidence must use the closed enum low|medium|high"
            )
        visible_confidence_value = visible_values.get("confidence")
        visible_confidence = (
            VISIBLE_CONFIDENCE_VALUES.get(visible_confidence_value.lower())
            if visible_confidence_value is not None
            else None
        )
        if visible_confidence != confidence:
            errors.append(f"{location} visible confidence and stable metadata drift")

        implication = IMPLICATION_CONTRACT_RE.fullmatch(values["implication"])
        if implication is None:
            errors.append(
                f"{location} implication requires one stable key~visible-witness contract"
            )
        else:
            witness = implication.group("witness")
            visible_slug = re.sub(
                r"[^a-z0-9.]+",
                "-",
                visible_values.get("implication", "").lower(),
            ).strip("-")
            if re.search(
                rf"(?:^|-){re.escape(witness)}(?:-|$)", visible_slug
            ) is None:
                errors.append(
                    f"{location} visible implication does not carry bounded witness {witness}"
                )
        if values["time_basis"] not in {
            "legacy_publication_date",
            "radar_published_at",
        }:
            errors.append(
                f"{location} time_basis must be legacy_publication_date or radar_published_at"
            )
        expected_acceptance = (
            "radar-acceptance"
            if values["time_basis"] == "radar_published_at"
            else "not-radar-acceptance"
        )
        if values["non_acceptance"] != expected_acceptance:
            errors.append(
                f"{location} non_acceptance contract must be {expected_acceptance}"
            )
        visible_non_acceptance = re.sub(
            r"[^a-z0-9]+",
            "-",
            visible_values.get("non-acceptance", "").lower(),
        ).strip("-")
        if visible_non_acceptance != values["non_acceptance"]:
            errors.append(
                f"{location} visible non_acceptance semantic witness is missing"
            )
        if visible_values.get("time basis", "").lower() != values["time_basis"]:
            errors.append(f"{location} visible time_basis and stable metadata drift")
        if synthesized_time is None or synthesized != expected_synthesis:
            errors.append(
                f"{location} synthesized must be the exact UTC synthesis timestamp "
                f"{expected_synthesis}"
            )
        visible_synthesis = VISIBLE_SYNTHESIS_VALUE_RE.fullmatch(
            visible_values.get("synthesis", "")
        )
        if (
            visible_synthesis is None
            or visible_synthesis.group("timestamp") != synthesized
            or visible_synthesis.group("timezone") != "UTC"
        ):
            errors.append(
                f"{location} visible last-synthesis timestamp or timezone drift"
            )

        if len(supports) != len(set(supports)):
            errors.append(f"{location} contains duplicate support identities")
        visible_support_field = visible_values.get("supports")
        visible_supports = tuple(
            _support_identity(identity)
            for identity in PERIOD_SUPPORT_RE.findall(visible_support_field or "")
        )
        if len(visible_supports) != len(set(visible_supports)):
            errors.append(f"{location} contains duplicate visible support identities")
        if visible_supports != supports:
            errors.append(f"{location} visible support order and stable metadata drift")
        if not supports and visible_support_field != "**none**":
            errors.append(f"{location} zero support must be exactly **none**")
        if supports and visible_support_field is not None:
            remainder = PERIOD_SUPPORT_RE.sub("", visible_support_field)
            if re.sub(r"[\s,，·]+", "", remainder):
                errors.append(
                    f"{location} visible support field must contain only canonical "
                    "support links"
                )
        if key in seen_keys:
            errors.append(f"{location} repeats stable direction key {key}")
        seen_keys.add(key)

        for identity in supports:
            record = record_by_id.get(identity)
            if record is None:
                errors.append(f"{location} support identity {identity} has no canonical record")
                continue
            time_basis = values["time_basis"]
            expected_provenance = (
                "native_v2" if time_basis == "radar_published_at" else "legacy_unknown"
            )
            if record.get("time_provenance") != expected_provenance:
                if expected_provenance == "legacy_unknown":
                    errors.append(
                        f"{location} support identity {identity} is not an honest legacy "
                        "publication-date record"
                    )
                else:
                    errors.append(
                        f"{location} support identity {identity} is not a native_v2 "
                        "Radar-acceptance record"
                    )
            direction_keys = _canonical_direction_keys(record.get("direction_keys"))
            if direction_keys is None or key not in direction_keys:
                errors.append(
                    f"{location} support identity {identity} direction_keys must "
                    f"include {key}"
                )
            if time_basis == "radar_published_at":
                evidence_time = _parse_utc(record.get("radar_published_at"))
                if evidence_time is None or not window[0] <= evidence_time.date() <= window[1]:
                    errors.append(
                        f"{location} support identity {identity} falls outside "
                        f"{window[0].isoformat()}—{window[1].isoformat()} by radar_published_at"
                    )
                if (
                    evidence_time is not None
                    and synthesized_time is not None
                    and evidence_time > synthesized_time
                ):
                    errors.append(
                        f"{location} support identity {identity} has radar_published_at "
                        f"after direction synthesized={synthesized}"
                    )
            else:
                published_at = _parse_date(record.get("published_at"))
                if published_at is None or not window[0] <= published_at <= window[1]:
                    errors.append(
                        f"{location} support identity {identity} falls outside "
                        f"{window[0].isoformat()}—{window[1].isoformat()} by published_at"
                    )
                if (
                    published_at is not None
                    and synthesized_time is not None
                    and published_at > synthesized_time.date()
                ):
                    errors.append(
                        f"{location} support identity {identity} was published after "
                        f"direction synthesized={synthesized} at legacy date precision"
                    )

        distinct_supports = set(supports)
        if len(distinct_supports) == 1 and DURABLE_TREND_RE.search(visible_block):
            errors.append(
                f"{location} one legacy paper cannot claim a durable/reinforced trend"
            )
        if len(distinct_supports) == 1 and ANY_TREND_CLAIM_RE.search(visible_block):
            errors.append(
                f"{location} one legacy paper cannot make any trend/趋势 claim"
            )
        if values["time_basis"] == "legacy_publication_date":
            if state != "new_signal":
                errors.append(
                    f"{location} legacy_publication_date adapter requires "
                    "state=new_signal"
                )
            if len(distinct_supports) != 1:
                errors.append(
                    f"{location} legacy_publication_date adapter requires exactly "
                    "one support identity"
                )
            for identity in distinct_supports:
                support_delta = record_by_id.get(identity, {}).get("map_delta")
                if support_delta not in LEGACY_CONTEXT_MAP_DELTAS:
                    errors.append(
                        f"{location} legacy_publication_date adapter support identity "
                        f"{identity} map_delta must be none or early_signal"
                    )
            if prior != "none":
                errors.append(
                    f"{location} legacy_publication_date adapter requires prior=none"
                )
        elif values["time_basis"] == "radar_published_at":
            support_deltas = {
                record_by_id.get(identity, {}).get("map_delta")
                for identity in distinct_supports
            }
            if state == "new_signal":
                if (
                    len(distinct_supports) != 1
                    or support_deltas != {"early_signal"}
                    or prior != "none"
                ):
                    errors.append(
                        f"{location} radar_published_at adapter requires one "
                        "early_signal support and prior=none for new_signal"
                    )
            elif state == "reinforced":
                if len(distinct_supports) < 2:
                    errors.append(
                        f"{location} radar_published_at reinforced requires at least two "
                        "distinct native supports"
                    )
                if prior != "field-map":
                    errors.append(
                        f"{location} radar_published_at reinforced requires prior=field-map"
                    )
            elif state in {"revised", "splits", "retires"}:
                required_delta = {
                    "revised": "revises",
                    "splits": "splits",
                    "retires": "retires",
                }[state]
                if not distinct_supports or required_delta not in support_deltas:
                    errors.append(
                        f"{location} radar_published_at {state} requires a native "
                        f"{required_delta} support"
                    )
                if prior != "field-map":
                    errors.append(
                        f"{location} radar_published_at {state} requires prior=field-map"
                    )
            elif state == "no_material_change":
                if distinct_supports or prior != "none":
                    errors.append(
                        f"{location} radar_published_at no_material_change requires "
                        "supports=none and prior=none"
                    )

        visible_prior = visible_values.get("prior")
        if visible_prior == "**none**":
            visible_prior_token = "none"
        elif (
            visible_prior is not None
            and re.fullmatch(r"\[[^\]\r\n]+\]\(#field-map\)", visible_prior)
            is not None
        ):
            visible_prior_token = "field-map"
        else:
            visible_prior_token = None
        if visible_prior_token != prior:
            errors.append(f"{location} visible prior-map evidence and metadata drift")

        items.append(
            (
                key,
                state,
                supports,
                values["confidence"],
                values["implication"],
                values["time_basis"],
                values["non_acceptance"],
                synthesized,
                prior,
            )
        )
    if not items:
        errors.append(f"{language}: {anchor} has no parseable direction metadata")
    return items


def _synthesis_identity(
    language: str,
    anchor: str,
    items: list[
        tuple[str, str, tuple[str, ...], str, str, str, str, str, str]
    ],
    errors: list[str],
) -> str:
    syntheses = [item[7] for item in items]
    if not syntheses:
        errors.append(
            f"{language}: {anchor} requires a scoped synthesis field on each direction"
        )
        return ""
    if len(set(syntheses)) != 1:
        errors.append(f"{language}: {anchor} direction synthesis timestamps drift")
    return syntheses[0]


def _validate_period_language(
    language: str,
    records: list[dict[str, object]],
    text: str,
    errors: list[str],
) -> tuple[
    dict[
        str,
        list[tuple[str, str, tuple[str, ...], str, str, str, str, str, str]],
    ],
    dict[str, str],
]:
    record_by_id = {str(record.get("id")): record for record in records}
    direction_layers: dict[
        str,
        list[tuple[str, str, tuple[str, ...], str, str, str, str, str, str]],
    ] = {}
    syntheses: dict[str, str] = {}
    for anchor, next_anchor in (
        ("last-7-days", "last-30-days"),
        ("last-30-days", "field-map"),
    ):
        section = _period_section(text, anchor, next_anchor)
        section_syntheses = _direction_syntheses(section)
        unique_syntheses = set(section_syntheses)
        synthesis_time = (
            _parse_utc(section_syntheses[0])
            if len(unique_syntheses) == 1 and section_syntheses
            else None
        )
        if synthesis_time is None:
            errors.append(
                f"{language}: {anchor} needs one exact valid direction synthesis cutoff"
            )
            expected_synthesis = SYNTHESIS_TIMESTAMP
            fallback_cutoff = _parse_utc(SYNTHESIS_TIMESTAMP)
            assert fallback_cutoff is not None
            expected_window = _rolling_window(anchor, fallback_cutoff)
        else:
            expected_synthesis = section_syntheses[0]
            expected_window = _rolling_window(anchor, synthesis_time)
        range_matches = list(RANGE_RE.finditer(strip_html_comments(section)))
        observed_window: tuple[date, date] | None = None
        if len(range_matches) != 1:
            errors.append(
                f"{language}: {anchor} must contain exactly one visible date range "
                "with valid inclusive dates"
            )
        else:
            try:
                observed_window = (
                    date.fromisoformat(range_matches[0].group("start")),
                    date.fromisoformat(range_matches[0].group("end")),
                )
            except ValueError:
                errors.append(
                    f"{language}: {anchor} must contain exactly one visible date range "
                    "with valid inclusive dates"
                )
        if observed_window is not None:
            expected_days = 6 if anchor == "last-7-days" else 29
            if (observed_window[1] - observed_window[0]).days != expected_days:
                errors.append(
                    f"{language}: {anchor} inclusive length must be "
                    f"{expected_days + 1} days"
                )
            if observed_window != expected_window:
                errors.append(
                    f"{language}: {anchor} must use current expected window "
                    f"{expected_window[0].isoformat()}—{expected_window[1].isoformat()}"
                )
        items = _parse_direction_items(
            language,
            anchor,
            section,
            expected_window,
            expected_synthesis,
            record_by_id,
            errors,
        )
        direction_layers[anchor] = items
        syntheses[anchor] = _synthesis_identity(language, anchor, items, errors)

        actual = tuple(identity for item in items for identity in item[2])
        time_bases = {item[5] for item in items}
        if len(time_bases) != 1:
            errors.append(f"{language}: {anchor} must use one period time adapter")
        adapter = next(iter(time_bases), "legacy_publication_date")
        if adapter == "radar_published_at":
            expected_records = [
                record
                for record in records
                if record.get("time_provenance") == "native_v2"
                and _parse_utc(record.get("radar_published_at")) is not None
                and expected_window[0]
                <= _parse_utc(record.get("radar_published_at")).date()
                <= expected_window[1]
                and synthesis_time is not None
                and _parse_utc(record.get("radar_published_at")) <= synthesis_time
            ]
            expected_records.sort(
                key=lambda record: (
                    -_parse_utc(record.get("radar_published_at")).timestamp(),
                    str(record.get("id")),
                )
            )
            membership_label = "native Radar-acceptance"
        else:
            expected_records = [
                record
                for record in records
                if record.get("time_provenance") == "legacy_unknown"
                and _parse_date(record.get("published_at")) is not None
                and expected_window[0]
                <= _parse_date(record.get("published_at"))
                <= expected_window[1]
            ]
            expected_records.sort(
                key=lambda record: (
                    _parse_date(record.get("published_at")),
                    str(record.get("id")),
                ),
                reverse=True,
            )
            membership_label = "legacy publication-date"
        expected = tuple(str(record.get("id")) for record in expected_records)
        if actual != expected:
            errors.append(
                f"{language}: {anchor} ordered direction supports {actual} != "
                f"{membership_label} membership {expected}"
            )
        if len(actual) != len(set(actual)):
            errors.append(f"{language}: {anchor} repeats support across direction items")
    return direction_layers, syntheses


def validate_period_membership(records: list[dict[str, object]], text: str) -> list[str]:
    """Validate one language's structured legacy-publication period projection."""
    errors: list[str] = []
    _validate_period_language("README", records, text, errors)
    return errors


def validate_period_contracts(
    records: list[dict[str, object]], zh: str, en: str
) -> list[str]:
    """Validate structured direction contracts and bilingual synthesis parity."""
    errors: list[str] = []
    zh_layers, zh_syntheses = _validate_period_language(
        "README.md", records, zh, errors
    )
    en_layers, en_syntheses = _validate_period_language(
        "README.en.md", records, en, errors
    )
    for anchor in ("last-7-days", "last-30-days"):
        if zh_layers.get(anchor) != en_layers.get(anchor):
            errors.append(f"Chinese/English {anchor} direction parity drift")
        if zh_syntheses.get(anchor) != en_syntheses.get(anchor):
            errors.append(f"Chinese/English {anchor} synthesis timestamp parity drift")
    return errors


def check_links(path: Path, errors: list[str]) -> None:
    visible_text = strip_html_comments(path.read_text(encoding="utf-8"))
    for raw in LINK_RE.findall(visible_text):
        target, parsed = raw.strip().strip("<>"), urlsplit(raw.strip().strip("<>"))
        if not target or target.startswith("#") or parsed.scheme or parsed.netloc:
            continue
        rel = unquote(parsed.path)
        if not rel:
            continue
        resolved = (path.parent / rel).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: link escapes repo: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken local link: {target}")


def family_routes(text: str, name: str, errors: list[str]) -> None:
    visible_text = strip_html_comments(text)
    targets = {raw.strip().strip("<>") for raw in LINK_RE.findall(visible_text)}
    for label, target in FAMILY_ROUTES.items():
        if target not in targets:
            errors.append(f"{name}: missing canonical {label} family route")


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_no_public_runs(ROOT))
    errors.extend(validate_authoritative_docs(ROOT))
    required = [ZH, EN, LIB_ZH, LIB_EN, REGISTRY, ROOT / "CURATION.md", ROOT / "COMPACTION.md", ROOT / "SCHEMA.md", ROOT / "digests/README.md", ROOT / "digests/README.en.md", ROOT / "docs/RADAR_AGENT_PROTOCOL.md", ROOT / "docs/EDITORIAL_STANDARD.md", ROOT / "docs/DAILY_WORKFLOW.md"]
    for path in required:
        if not path.exists():
            errors.append(f"missing contract: {path.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print("ERROR", error)
        return 1
    records = json.loads(REGISTRY.read_text(encoding="utf-8"))
    zh, en = ZH.read_text(encoding="utf-8"), EN.read_text(encoding="utf-8")
    if "README.en.md" not in zh or "README.md" not in en:
        errors.append("README language switch is incomplete")
    errors.extend(validate_pair(zh, en))
    errors.extend(validate_data_aliases(zh, en))
    errors.extend(validate_registry(records))
    errors.extend(validate_data_note_links(zh, en))
    errors.extend(validate_registry_projection(records, zh, en))
    errors.extend(validate_period_contracts(records, zh, en))
    for name, text in (("README.md", zh), ("README.en.md", en)):
        family_routes(text, name, errors)
    for record in records:
        note = ROOT / str(record.get("note_path", ""))
        english_note = note.with_name(note.stem + ".en.md")
        if not note.is_file() or not english_note.is_file():
            errors.append(f"{record.get('id')}: canonical record needs paired local notes")
    for path in (
        ZH,
        EN,
        LIB_ZH,
        LIB_EN,
        *sorted((ROOT / "digests").rglob("*.md")),
    ):
        check_links(path, errors)
    if errors:
        for error in errors:
            print("ERROR", error)
        return 1
    print(f"Validated Data Agent time-first reading surfaces and {len(records)} canonical records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
