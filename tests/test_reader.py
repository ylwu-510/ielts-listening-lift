import copy
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("reader", ROOT / "scripts/build_reader.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
HAS_DOCX = importlib.util.find_spec("docx") is not None
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def all_visible_content(data):
    yield data["title"]
    yield data["intro"]
    for section in reader.SECTIONS[:3]:
        for entry in data[section]:
            yield entry["phrase"]
            yield entry["meaning"]
            for example in entry["examples"]:
                yield from example.values()
    for passage in data["passages"]:
        yield from passage.values()
    for notes in data["notes"].values():
        for item in notes:
            yield from item.values()


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/c16-test2.json").read_text(encoding="utf-8"))

    def test_reference_content_is_preserved_in_markdown(self):
        reader.validate(self.data)
        md = reader.render_md(self.data)
        normalized = re.sub(r"\\([\\`*_\[\]<>#])", r"\1", md).replace("**", "")
        for value in all_visible_content(self.data):
            self.assertIn(value.replace("**", ""), normalized)
        self.assertEqual(reader.counts(self.data)["patterns"], 8)
        self.assertEqual(len(re.findall(r"^\d+\. ", md, re.M)), 56)

    def test_every_markdown_section_restarts_and_increments(self):
        groups = re.split(r"^#{2,3} .+$", reader.render_md(self.data), flags=re.M)[1:]
        found = []
        for group in groups:
            nums = [int(n) for n in re.findall(r"^(\d+)\. ", group, re.M)]
            if nums:
                self.assertEqual(nums, list(range(1, len(nums) + 1)))
                found.append(len(nums))
        self.assertEqual(found, [13, 17, 8, 2, 4, 7, 5])

    def test_variable_count_and_empty_parts_do_not_invent_content(self):
        d = copy.deepcopy(self.data)
        d["patterns"] = d["patterns"][:2]
        d["collocations"] = []
        d["passages"] = []
        d["notes"] = {k: [] for k in reader.NOTES}
        reader.validate(d)
        md = reader.render_md(d)
        self.assertIn("## 2组句式", md)
        self.assertNotIn("## 8组句式", md)
        self.assertNotIn(self.data["collocations"][0]["phrase"], md)
        self.assertEqual(len(re.findall(r"^\d+\. ", md, re.M)), 15)

    def test_invalid_input_fails_before_output(self):
        changes = [lambda d: d.pop("patterns"),
                   lambda d: d["oral"][0].update(exampels=[]),
                   lambda d: d["oral"][0].update(examples=[]),
                   lambda d: d["oral"][0]["examples"][0].update(zh=""),
                   lambda d: d["oral"][0]["examples"][0].update(en="**unclosed"),
                   lambda d: d["oral"][0]["examples"][0].update(en="two\nparagraphs")]
        for change in changes:
            with self.subTest(change=change):
                d = copy.deepcopy(self.data)
                change(d)
                with self.assertRaises(ValueError):
                    reader.validate(d)

    def test_markdown_escapes_markup_but_preserves_emphasis(self):
        self.assertEqual(reader.md_rich("A **useful** [label] <tag> _word_"),
                         "A **useful** \\[label\\] \\<tag\\> \\_word\\_")

    def test_cli_markdown_without_site_packages_and_auto_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = [sys.executable, "-S", str(ROOT / "scripts/build_reader.py"), str(ROOT / "examples/c16-test2.json"), "--output", str(Path(tmp) / "early reading")]
            for fmt in ("md", "auto"):
                result = subprocess.run(base + ["--format", fmt], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["format"], "md")
                if fmt == "auto":
                    self.assertIn("unchanged content", result.stderr)
            result = subprocess.run(base + ["--format", "docx"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((Path(tmp) / "early reading.docx").exists())

    @unittest.skipUnless(HAS_DOCX, "python-docx not installed")
    def test_word_preserves_content_and_native_list_restarts(self):
        with ZipFile(io.BytesIO(reader.render_docx(self.data))) as z:
            document = ET.fromstring(z.read("word/document.xml"))
            numbering = ET.fromstring(z.read("word/numbering.xml"))
        text = "".join(document.itertext())
        for value in all_visible_content(self.data):
            self.assertIn(value.replace("**", ""), text)
        ids = [el.get(W + "val") for el in document.iter(W + "numId")]
        self.assertEqual(len(ids), 56)
        self.assertEqual(len(set(ids)), 7)
        self.assertEqual([ids.count(i) for i in dict.fromkeys(ids)], [13, 17, 8, 2, 4, 7, 5])
        for ident in set(ids):
            num = next(e for e in numbering.findall(W + "num") if e.get(W + "numId") == ident)
            self.assertEqual(num.find(f'{W}lvlOverride/{W}startOverride').get(W + "val"), "1")
        abstract = numbering.findall(W + "abstractNum")[-1]
        level = abstract.find(W + "lvl")
        self.assertEqual(level.find(W + "lvlText").get(W + "val"), "%1.")
        self.assertEqual(level.find(W + "lvlJc").get(W + "val"), "right")
        ind = level.find(f'{W}pPr/{W}ind')
        self.assertEqual(ind.get(W + "hanging"), "80")
        self.assertEqual(ind.get(W + "left"), "380")
        self.assertNotIn("•", text)

    @unittest.skipUnless(HAS_DOCX, "python-docx not installed")
    def test_large_lists_expand_number_area_and_a4_is_supported(self):
        d = copy.deepcopy(self.data)
        d["oral"] = [copy.deepcopy(d["oral"][0]) for _ in range(105)]
        with ZipFile(io.BytesIO(reader.render_docx(d, paper="a4"))) as z:
            numbering = ET.fromstring(z.read("word/numbering.xml"))
            document = ET.fromstring(z.read("word/document.xml"))
        ind = numbering.findall(W + "abstractNum")[-1].find(f'{W}lvl/{W}pPr/{W}ind')
        self.assertEqual(ind.get(W + "left"), "500")
        self.assertEqual(ind.get(W + "hanging"), "80")
        self.assertEqual(len(list(document.iter(W + "numId"))), 148)
        size = document.find(f'.//{W}pgSz')
        self.assertAlmostEqual(int(size.get(W + "w")), 11906, delta=1)


if __name__ == "__main__":
    unittest.main()
