from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
DETAILS_RE = re.compile(r"<details><summary>.*?</summary>(.*?)</details>", re.S)
FIELD_RE = re.compile(
    r"\*\*(?P<label>问题|证据|限制|地图|链接)[。.]\*\*(?P<value>.*?)(?=\*\*(?:问题|证据|限制|地图|链接)[。.\u3002]\*\*|$)",
    re.S,
)
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
ENGLISH_CLAUSE_RE = re.compile(
    r"\b[A-Za-z][A-Za-z0-9.+/-]*(?:\s+[A-Za-z][A-Za-z0-9.+/-]*){2,}\b"
)


def timeline_fields(text: str) -> list[dict[str, str]]:
    start = text.index('<a id="timeline"></a>')
    end = text.index('<a id="periods"></a>', start)
    entries = []
    for body in DETAILS_RE.findall(text[start:end]):
        entries.append(
            {
                match.group("label"): match.group("value")
                for match in FIELD_RE.finditer(body)
            }
        )
    return entries


def visible_prose(value: str) -> str:
    value = HTML_COMMENT_RE.sub("", value)
    value = re.sub(r"`[^`\n]+`", "", value)
    value = re.sub(r"(?<!\*)\*[^*\n]+\*(?!\*)", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("**", "")
    return value.strip()


class ChineseTimelineStyleTest(unittest.TestCase):
    def test_chinese_timeline_expansion_uses_chinese_sentence_structure(self):
        zh = (ROOT / "README.md").read_text(encoding="utf-8")
        entries = timeline_fields(zh)
        self.assertTrue(entries, "Timeline must expose at least one expandable entry")

        for index, fields in enumerate(entries, start=1):
            with self.subTest(entry=index):
                self.assertEqual({"问题", "证据", "限制", "地图", "链接"}, set(fields))
                for label in ("问题", "证据", "限制"):
                    prose = visible_prose(fields[label])
                    self.assertRegex(prose, r"^[\u3400-\u4dbf\u4e00-\u9fff]")
                    self.assertGreaterEqual(len(CJK_RE.findall(prose)), 8)
                    self.assertIsNone(ENGLISH_CLAUSE_RE.search(prose), (label, prose))

                map_prose = visible_prose(fields["地图"])
                map_prose = re.sub(r"^[\s—;；:：-]+", "", map_prose)
                self.assertRegex(map_prose, r"^[\u3400-\u4dbf\u4e00-\u9fff]")

                links = visible_prose(fields["链接"])
                self.assertNotIn("Paper", links)
                self.assertNotIn("English note", links)


if __name__ == "__main__":
    unittest.main()
