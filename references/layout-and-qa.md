# Approved layout and quality checks

## Typography

| Element | Size / line spacing | Treatment |
| --- | --- | --- |
| Title | 22 / 27 pt | Black, bold, native Title style |
| Main section | 16 / 21 pt | Black, bold |
| Supplement heading | 12 / 17 pt | Black, bold |
| Expression / pattern | 10.7 / 13.5 pt | Bold, short meaning on the same line |
| English example | 11.5 / 14 pt | Ink #182326, target phrase bold teal #216A68 |
| Chinese translation | 10 / 12.5 pt | Grey #536168 |
| Complete passage | 11.5 / 15.2 pt | Same target-phrase emphasis |
| Usage note | 10.5 / 14 pt | Bold label, plain explanation |

Letter portrait; top/bottom margins 0.50 in, left/right 0.62 in. A4 can be requested. No cover page, title rules, decorative cards or study-list tables. Footer shows short source label and native PAGE / NUMPAGES fields, which may update when opened or printed.

Use explicit Latin and CJK font names rather than theme fonts. Remove inherited title borders and italic styling. The generator does not embed, distribute or install fonts. Check installed font coverage when rendering, especially on Linux. Do not copy proprietary fonts into the repository.

## Numbering and grouping

Native decimal list `%1.`; independent list instance and start override `1` per main section and supplement subsection. Right-aligned number; 4 pt gap to text; normal text start 19 pt from the margin. Two-digit numbers stay aligned. For three or more digits the renderer expands the number area while preserving the gap.

English and Chinese continuations align with expression text. Keep entry heading with its example and example with translation. Short entries stay together; long passages can flow across pages rather than creating large blank areas. A genuinely empty category uses an unnumbered explanation.

Four pages describes the retained C16 example, not a quota. That example has section breaks before collocations and passages; other transcripts may work better with natural flow.

## Render and inspect

If a documents skill/runtime is available, use its current renderer and artifact workflow. Do not hardcode a local username, cache version, interpreter or font-asset path. In Codex desktop, resolve bundled dependencies through `load_workspace_dependencies`; use bundled LibreOffice instead of the user's desktop LibreOffice when provided.

Otherwise use local headless LibreOffice and PDF-to-image tools. Rendering is QA, not a requirement for generating Markdown. Keep QA outputs separate from final files. Check every rendered page:

- Chinese text displays without tofu boxes or missing glyphs.
- Numbering restarts; `1.` is close to its text; no actual bullet prefixes exist.
- Titles and examples are not stranded; translations stay near examples.
- Nothing clips or overlaps; no accidental blank pages; footer is visible.
- Bold/teal matches target phrases, not whole paragraphs.

If CJK fails under a bundled renderer, check fonts and theme overrides. A task-local fontconfig file can reference actual system font directories and a writable local cache. Discover those directories; never publish machine-specific paths or change global font settings as a shortcut.

## Formatting marks

Small black squares can indicate keep-with-next / keep-lines settings. Blue arrows can indicate paragraph or manual break markers in the editing application. They do not print. Verify the OOXML and render contain no real bullets before diagnosing. Toggle the application's ¶ display when appropriate; retain useful pagination properties.

## Regression check

```bash
python3 -m unittest discover -s tests -v
```

Tests cover variable item counts, content preservation, native list restarts and spacing, malformed input, and dependency-free Markdown. They supplement visual review, not linguistic or page-appearance checks.
