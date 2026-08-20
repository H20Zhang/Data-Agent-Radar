import os
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from no_public_runs import (  # noqa: E402
    AUTHORITATIVE_DOCS,
    validate_authoritative_docs,
    validate_no_public_runs,
)


class NoPublicRunsTest(unittest.TestCase):
    def write_authoritative_docs(self, root: Path, text: str) -> None:
        for relative in AUTHORITATIVE_DOCS:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def test_repository_has_no_public_operational_run_paths(self):
        self.assertEqual([], validate_no_public_runs(ROOT))

    def test_absent_configured_path_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(
                [],
                validate_no_public_runs(Path(directory), ("runs/daily",)),
            )

    def test_configured_directory_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runs/daily").mkdir(parents=True)
            self.assertTrue(validate_no_public_runs(root, ("runs/daily",)))

    def test_configured_path_as_file_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runs").mkdir()
            (root / "runs/daily").write_text("private data", encoding="utf-8")
            self.assertTrue(validate_no_public_runs(root, ("runs/daily",)))

    def test_parent_component_as_file_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runs").write_text("not a directory", encoding="utf-8")
            self.assertTrue(validate_no_public_runs(root, ("runs/daily",)))

    def test_normal_symlink_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "private-target"
            target.mkdir()
            (root / "runs").mkdir()
            os.symlink(target, root / "runs/daily")
            self.assertTrue(validate_no_public_runs(root, ("runs/daily",)))

    def test_broken_symlink_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runs").mkdir()
            os.symlink(root / "missing-target", root / "runs/daily")
            self.assertTrue(validate_no_public_runs(root, ("runs/daily",)))

    def test_authoritative_repository_docs_are_consistent(self):
        self.assertEqual([], validate_authoritative_docs(ROOT))
        self.assertEqual(
            {
                "CURATION.md",
                "COMPACTION.md",
                "SCHEMA.md",
                "docs/RADAR_AGENT_PROTOCOL.md",
                "docs/DAILY_WORKFLOW.md",
                "docs/BILINGUAL_PUBLICATION.md",
                "docs/EDITORIAL_STANDARD.md",
                "docs/RESEARCH_EXPLAINER_STANDARD.md",
            },
            set(AUTHORITATIVE_DOCS),
        )

    def test_stale_public_run_log_phrases_are_rejected(self):
        stale_phrases = (
            "Every update emits one run log.",
            "Commit canonical state and the run log atomically.",
            "Run logs remain single-source.",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_authoritative_docs(root, "No public operational history.\n")
            for stale in stale_phrases:
                with self.subTest(stale=stale):
                    target = root / AUTHORITATIVE_DOCS[0]
                    target.write_text(stale + "\n", encoding="utf-8")
                    self.assertTrue(validate_authoritative_docs(root))
                    target.write_text(
                        "No public operational history.\n", encoding="utf-8"
                    )

    def test_without_public_run_log_counterexamples_are_rejected(self):
        stale_phrases = (
            "Never commit state without a public run log.",
            "Do not operate without a public run log.",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_authoritative_docs(root, "No public operational history.\n")
            target = root / AUTHORITATIVE_DOCS[0]
            for stale in stale_phrases:
                with self.subTest(stale=stale):
                    target.write_text(stale + "\n", encoding="utf-8")
                    self.assertTrue(validate_authoritative_docs(root))
                    target.write_text(
                        "No public operational history.\n", encoding="utf-8"
                    )

    def test_exact_canonical_commit_without_public_run_log_line_is_approved(self):
        canonical = (
            "- **Every successful material run:** update canonical records, "
            "Timeline, and rolling periods when evidence changes them; preserve "
            "the complete accepted projection in one atomic commit without "
            "a public run log.\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_authoritative_docs(root, "No public operational history.\n")
            (root / "docs/RADAR_AGENT_PROTOCOL.md").write_text(
                canonical,
                encoding="utf-8",
            )

            self.assertEqual([], validate_authoritative_docs(root))

    def test_canonical_allowlist_is_scoped_to_the_protocol_document(self):
        canonical = (
            "- **Every successful material run:** update canonical records, "
            "Timeline, and rolling periods when evidence changes them; preserve "
            "the complete accepted projection in one atomic commit without "
            "a public run log.\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_authoritative_docs(root, "No public operational history.\n")
            (root / "CURATION.md").write_text(canonical, encoding="utf-8")

            self.assertTrue(validate_authoritative_docs(root))

    def test_protocol_allowlist_rejects_split_and_multispace_variants(self):
        variants = (
            "Never commit state without a\npublic run log.\n",
            (
                "- **Every successful material run:** update canonical records, "
                "Timeline, and rolling periods when evidence changes them; preserve "
                "the complete accepted projection in one atomic commit without "
                "a   public run log.\n"
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_authoritative_docs(root, "No public operational history.\n")
            target = root / "docs/RADAR_AGENT_PROTOCOL.md"
            for variant in variants:
                with self.subTest(variant=variant):
                    target.write_text(variant, encoding="utf-8")
                    self.assertTrue(validate_authoritative_docs(root))
                    target.write_text(
                        "No public operational history.\n", encoding="utf-8"
                    )

    def test_public_run_log_is_forbidden_after_exact_allowlist_removal(self):
        variants = (
            "without a public run log, publish one atomic commit.\n",
            "Neutral glossary prose mentions PUBLIC   RUN\nLOGS here.\n",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_authoritative_docs(root, "No public operational history.\n")
            target = root / "docs/RADAR_AGENT_PROTOCOL.md"
            for variant in variants:
                with self.subTest(variant=variant):
                    target.write_text(variant, encoding="utf-8")
                    self.assertTrue(validate_authoritative_docs(root))
                    target.write_text(
                        "No public operational history.\n", encoding="utf-8"
                    )


if __name__ == "__main__":
    unittest.main()
