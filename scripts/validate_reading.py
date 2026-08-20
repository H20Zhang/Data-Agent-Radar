#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ZH = ROOT / "README.md"
EN = ROOT / "README.en.md"
LIB_ZH = ROOT / "library" / "README.md"
LIB_EN = ROOT / "library" / "README.en.md"
REGISTRY = ROOT / "data" / "papers.json"
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def check_links(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for raw in LINK_RE.findall(text):
        target = raw.strip().strip("<>")
        parsed = urlsplit(target)
        if not target or target.startswith("#") or parsed.scheme or parsed.netloc:
            continue
        rel = unquote(parsed.path)
        if not rel: continue
        resolved = (path.parent / rel).resolve()
        try: resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: link escapes repo: {target}")
            continue
        if not resolved.exists(): errors.append(f"{path.relative_to(ROOT)}: broken local link: {target}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    required = [ZH, EN, LIB_ZH, LIB_EN, REGISTRY, ROOT / "CURATION.md", ROOT / "docs" / "EDITORIAL_STANDARD.md", ROOT / "docs" / "DAILY_WORKFLOW.md"]
    for p in required:
        if not p.exists(): errors.append(f"missing contract: {p.relative_to(ROOT)}")
    if errors:
        for e in errors: print("ERROR", e)
        return 1

    records = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not records: errors.append("data/papers.json must be a non-empty list")
    zh = ZH.read_text(encoding="utf-8")
    en = EN.read_text(encoding="utf-8")
    if "README.en.md" not in zh or "README.md" not in en: errors.append("README language switch is incomplete")

    order = ["latest", "changes", "field-map", "reading-paths", "library"]
    for name, text in [("README.md", zh), ("README.en.md", en)]:
        pos = []
        for anchor in order:
            needle = f'<a id="{anchor}"></a>'
            if needle not in text: errors.append(f"{name}: missing stable anchor {anchor}")
            pos.append(text.find(needle))
        if any(p < 0 for p in pos) or pos != sorted(pos): errors.append(f"{name}: progressive-depth order drift")

    for term in ["Data Discovery & Grounding", "Planning & Semantic Interaction", "Execution & Transformation", "Verification & Recovery", "Learning & Reuse"]:
        if term not in zh or term not in en: errors.append(f"README pair missing field-map boundary: {term}")

    for pat in [r"真正重要的不是", r"关键不在于.*而在于", r"值得注意的是", r"this matters because", r"the important delta"]:
        n = len(re.findall(pat, zh + "\n" + en, flags=re.IGNORECASE))
        if n >= 3: warnings.append(f"repeated editorial skeleton {pat!r}: {n} occurrences")

    for p in [ZH, EN, LIB_ZH, LIB_EN]: check_links(p, errors)
    for w in warnings: print("WARN", w)
    if errors:
        for e in errors: print("ERROR", e)
        return 1
    print(f"Validated Data Agent bilingual reading surfaces and {len(records)} seed records.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
