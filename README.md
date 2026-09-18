# IELTS Listening Lift

**雅思听力早读 · 把听过的表达，变成能说、能写的材料。**

中文 · [English](README.en.md)

给 Codex 一份雅思听力 Part 1–4 原稿，得到中英对照的早读讲义。优先生成 **Word**，也可输出 **Markdown**。内容随稿件变化，保留稳定、紧凑的阅读格式。

![Word 实际输出局部：黑色词条、青绿色英文重点、灰色中文译文，序号紧邻文字](assets/readme/word-preview.png)

*实际生成的 C16 Test2 示例局部。* [查看完整 Markdown](examples/c16-test2.md) · [下载 Word](examples/c16-test2.docx)

## 一句话使用

安装后，在 Codex 中输入，再粘贴或附上原稿：

> 使用 `$ielts-listening-lift`，把下面的剑雅听力稿整理成早读材料。优先生成 Word，沿用五部分结构；内容按原稿决定，不要为缩短篇幅删掉有用条目。

只有一个 Part 也可以。只想要 MD 时，加一句“这次输出 Markdown”。后续说“间距再紧一点”，技能会在原有内容上调整版式。

## 每份材料包含什么

| 部分 | 学习内容 |
| --- | --- |
| 口语表达 | 可复用表达、中文义、英文例句与译文 |
| 阅读和写作搭配 | 自然搭配及迁移语境 |
| N组句式 | 按本次材料选择的句式骨架和例句 |
| 完整的话 | 连贯的口语回答或写作段落，中英对照 |
| 补充材料 | 新句式重点、阅读易误解表达、搭配使用边界 |

每部分独立从 **1.** 开始，三个补充小节也分别重启。N 是实际句式数量，**不是固定八组**；没有固定条目上限或四页要求。

## 保留内容，让页面更好读

- **“看起来太长”先调整排版。** 缩紧间距、简化重复说明、改善分页；明确要求精选时才减少内容。
- **一条表达，连着读完。** 词条和中文义同行，英文例句与译文紧跟；重点短语加粗并用青绿色标出。
- **数字不再离文字太远。** Word 使用原生编号，默认间隔 4 磅，续行与文字对齐。
- **原稿决定选材。** 区分原文和迁移表达，保留语气与使用边界；不为了“高级”堆砌基础连接词或生僻句式。

## 安装到 Codex

将整个仓库文件夹下载或克隆到本地。仓库根目录就是技能目录，包含 `SKILL.md`。

macOS / Linux：在仓库根目录运行以下命令，复制技能到默认位置。如果目标已存在，命令会停止，避免覆盖本地修改。

```bash
skill_root="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skill_root"
if [ -e "$skill_root/ielts-listening-lift" ]; then
  echo "目标已存在，请先检查已有版本。"
else
  mkdir "$skill_root/ielts-listening-lift"
  cp -R SKILL.md agents scripts references examples assets tests requirements.txt \
    "$skill_root/ielts-listening-lift/"
fi
```

Windows：把同样的文件复制到 `%USERPROFILE%\.codex\skills\ielts-listening-lift`；如设置了 `CODEX_HOME`，使用其下的 `skills` 目录。安装后刷新技能列表或重新打开 Codex，即可用 `$ielts-listening-lift` 调用。

## Word 与 Markdown 如何选择

默认尽量生成 Word。格式由脚本完成，不必每次重新编写排版代码。用户选择 MD，或预算、环境不适合完成 Word 时，改用相同内容的 Markdown，并说明原因。

**换格式不删内容。** 两种输出共用一份学习数据。Markdown 保留标题、编号、粗体和中英换行；字体、颜色、分页取决于阅读器，不能与 Word 完全一致。技能不估报无法读取的 token 消耗。

Word 生成需要 **Python 3.10+**、`python-docx` 和可用的中文字体；Markdown 只需要 Python 标准库。Word 的视觉检查还需要文档渲染环境。Codex 桌面端有配套运行时时优先使用，否则可在独立 Python 环境安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

## 复现示例与维护

Codex 先从原稿提炼内容，再交给脚本排版。脚本的输入是整理后的 JSON，**不会直接把原始听力稿自动分析成教材**。

```bash
python3 scripts/build_reader.py examples/c16-test2.json \
  --output outputs/c16-test2 --format both \
  --break-before collocations --break-before passages

python3 -m unittest discover -s tests -v
```

示例包含 13 条口语、17 条搭配、8 组句式、2 段完整表达，以及三个补充小节。这是当前样稿的内容量，不是新材料的配额。示例 Word 在本次 macOS 环境中渲染为 4 页；不同字体和编辑器可能改变分页。

[选材原则](references/content-guide.md) · [数据格式与参数](references/data-format.md) · [排版与检查](references/layout-and-qa.md)

<details>
<summary>目录与常见问题</summary>

```text
SKILL.md                  技能入口
agents/openai.yaml        Codex 显示名称和调用提示
scripts/build_reader.py   共用的 Word / Markdown 生成器
references/               选材、数据结构、版式与验收规则
examples/                 C16 Test2 学习数据和两种成品
assets/readme/            实际文档预览
tests/                    内容保留、编号和降级检查
```

**为什么编辑器里可能出现黑方块和蓝箭头？**

它们可能是非打印编辑标记。在 Word/WPS 中关闭“显示／隐藏编辑标记 ¶”即可隐藏；不要因此删除用于保持例句与译文相邻的分页设置。

**中文变成方框怎么办？**

检查字体是否安装，必要时用 `--cjk-font` 指定可用中文字体。默认 macOS 为 PingFang SC、Windows 为 Microsoft YaHei、其他平台为 Noto Sans CJK SC。仓库不附带字体，生成脚本不会安装字体。

**示例是官方教材吗？**

不是。它是基于用户提供的 C16 Test2 材料整理的学习示例，包含迁移造句和必要的短原文锚点；仓库不收录完整考试原稿，也不代表 Cambridge 或 IELTS 官方。

</details>
