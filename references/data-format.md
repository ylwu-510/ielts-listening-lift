# Input format

The renderer consumes reviewed learning content, not a raw transcript. Codex performs selection and writing first. Use UTF-8 JSON with this shape; see [the complete example](../examples/c16-test2.json).

```json
{
  "schema_version": 1,
  "title": "雅思听力早读",
  "source_label": "练习稿 Part 3",
  "intro": "先读英文例句，再用中文提示复述；例句和完整段落为原文表达的迁移练习。",
  "oral": [{
    "phrase": "fit in with my lifestyle",
    "meaning": "适合我的生活方式",
    "source": {"part": "Part 3", "anchor": "fit in with my lifestyle", "relation": "exact"},
    "examples": [{"en": "Cycling **fits in with my lifestyle**.", "zh": "骑行适合我的生活方式。"}]
  }],
  "collocations": [],
  "patterns": [],
  "passages": [],
  "notes": {"patterns": [], "reading": [], "boundaries": []}
}
```

`oral`, `collocations`, `patterns` use the same entry shape. Every entry needs nonempty `phrase`, `meaning` and at least one bilingual example. `source` may be absent when repairing legacy content without a transcript; the extraction workflow requires it when the source is available. The renderer validates it when present and keeps it in JSON, not the handout.

`passages` items: `{"label": "口语谈运动习惯", "en": "... **target phrase** ...", "zh": "..."}`.

Each notes array contains `{"label": "correlation", "body": "表示相关性，不能直接当成因果关系。"}`. Notes may use `**...**` for emphasis. All array lengths are variable, including zero. Missing arrays and unknown fields are rejected to prevent accidental content loss.

Strings are single paragraphs. Use multiple examples for separate pairs; do not insert manual newlines, Markdown tables or HTML. Only paired `**bold**` markers are supported in examples, passages and note bodies. Other Markdown punctuation is escaped. Use plain text in labels, phrase, meaning, title and intro.

## CLI

```bash
python3 scripts/build_reader.py content.json --output outputs/reader --format docx
python3 scripts/build_reader.py content.json --output outputs/reader --format md
python3 scripts/build_reader.py content.json --output outputs/reader --format both
```

`--output` is a stem (a `.docx` or `.md` suffix is also accepted). Default format `auto` chooses DOCX if `python-docx` is available, otherwise MD with an explicit diagnostic. Explicit `docx` and `both` fail clearly when the dependency is absent. MD requires only Python's standard library. Python 3.10+ is supported.

Word options:

- `--cjk-font "PingFang SC"`: override the platform default. Defaults: PingFang SC on macOS, Microsoft YaHei on Windows, Noto Sans CJK SC elsewhere. These names do not install fonts.
- `--latin-font Arial`: change the Latin font.
- `--paper letter|a4`: default letter, matching the approved layout.
- `--break-before collocations --break-before passages`: optional section page breaks after visual review. These affect DOCX only.

The script prints output paths and section counts as JSON. It never truncates lists, calls a model, uses the network, installs dependencies, or publishes files. Both formats derive from the same validated content object.
