#!/usr/bin/env python3
"""Reject public operational run artifacts and stale publication guidance."""

from __future__ import annotations

import os
from pathlib import Path
import re
import sys
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

PUBLIC_OPERATIONAL_PATHS = (
    "runs",
    "run-logs",
    "run_logs",
    "operations/runs",
)

AUTHORITATIVE_DOCS = (
    "CURATION.md",
    "COMPACTION.md",
    "SCHEMA.md",
    "docs/RADAR_AGENT_PROTOCOL.md",
    "docs/DAILY_WORKFLOW.md",
    "docs/BILINGUAL_PUBLICATION.md",
    "docs/EDITORIAL_STANDARD.md",
    "docs/RESEARCH_EXPLAINER_STANDARD.md",
)

STALE_PUBLIC_RUN_LOG_PATTERNS = (
    re.compile(r"\bpublic\s+run\s+logs?\b", re.IGNORECASE),
    re.compile(r"\bone\s+(?:public\s+)?run log\b", re.IGNORECASE),
    re.compile(r"\bcommit[^\n]{0,120}\b(?:the\s+)?run log\b", re.IGNORECASE),
    re.compile(r"\brun logs?\s+remain(?:s)?\s+single[- ]source\b", re.IGNORECASE),
)
APPROVED_NO_PUBLIC_RUN_LOG_LINES = {
    "docs/RADAR_AGENT_PROTOCOL.md": frozenset(
        {
            "- **Every successful material run:** update canonical records, "
            "Timeline, and rolling periods when evidence changes them; preserve "
            "the complete accepted projection in one atomic commit without a "
            "public run log."
        }
    )
}


def _parts(relative: str) -> tuple[str, ...]:
    path = Path(relative)
    if path.is_absolute() or not path.parts or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"public operational path must be a normalized relative path: {relative!r}")
    return path.parts


def validate_no_public_runs(
    root: Path, configured_paths: Iterable[str] = PUBLIC_OPERATIONAL_PATHS
) -> list[str]:
    """Return errors when a configured public operational path can be reached.

    ``lexists`` is intentional: a broken symlink is still a committed path and
    therefore violates the absence contract. An ancestor that is a file or a
    symlink is also rejected instead of being mistaken for an absent child.
    """

    errors: list[str] = []
    for relative in configured_paths:
        parts = _parts(relative)
        current = root
        for index, part in enumerate(parts):
            current = current / part
            if not os.path.lexists(current):
                break
            final = index == len(parts) - 1
            if final:
                errors.append(f"public operational path must be absent: {relative}")
                break
            if current.is_symlink() or not current.is_dir():
                errors.append(
                    f"public operational path has non-directory ancestor "
                    f"{current.relative_to(root)}: {relative}"
                )
                break
    return errors


def validate_authoritative_docs(
    root: Path, authoritative_docs: Iterable[str] = AUTHORITATIVE_DOCS
) -> list[str]:
    """Reject bounded phrases that reintroduce public operational run logs."""

    errors: list[str] = []
    for relative in authoritative_docs:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing authoritative maintenance doc: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        approved_lines = APPROVED_NO_PUBLIC_RUN_LOG_LINES.get(
            relative, frozenset()
        )
        remaining: list[str] = []
        for raw_line in text.splitlines(keepends=True):
            if raw_line.endswith("\r\n"):
                exact_line = raw_line[:-2]
            elif raw_line.endswith(("\r", "\n")):
                exact_line = raw_line[:-1]
            else:
                exact_line = raw_line
            remaining.append("\n" if exact_line in approved_lines else raw_line)

        folded = re.sub(r"\s+", " ", "".join(remaining)).strip()
        matches = [
            match
            for pattern in STALE_PUBLIC_RUN_LOG_PATTERNS
            if (match := pattern.search(folded)) is not None
        ]
        if matches:
            match = min(matches, key=lambda candidate: candidate.start())
            errors.append(
                f"{relative}: stale public run-log guidance: {match.group(0)!r}"
            )
    return errors


def main() -> int:
    errors = validate_no_public_runs(ROOT)
    errors.extend(validate_authoritative_docs(ROOT))
    if errors:
        for error in errors:
            print("ERROR", error)
        return 1
    print("Validated absence of public operational run artifacts and stale guidance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
