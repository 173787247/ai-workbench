"""L03 合同结构解析器的验收测试。

保护的风险（逐条对应）：
1. 缺章/空章/重复/乱序/未知标题 → 结构不全的合同进入 L04 执行；
2. 代码围栏里的 "## 标题" 被误认为章节 → 示例文本污染结构判定；
3. 未闭合围栏 → 后续内容被当作章节；
4. 非 UTF-8 读取 → 中文合同读坏；
5. 解析修改了输入文件 → 违反"只读"约束；
6. 解析器越权判断业务正确性 → 把结构检查当成业务验收。

**解析器只回答一个问题：合同的六段结构是否完整。它不判断库存公式是否正确。**
"""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from workbench.spec import (  # noqa: E402
    REQUIRED_SECTIONS,
    ParsedSpec,
    SpecError,
    load_spec,
    parse_spec,
)

GOOD = """# 示例合同

## 1. 来源

课堂需求。

## 2. 目标

提供一个导出。

## 3. 非目标

不发送邮件。

## 4. 约束

只读。

## 5. 验收用例

A1：列顺序固定。

## 6. 完成定义

L03 完成结构检查。
"""


def with_section_removed(name: str) -> str:
    out, skip = [], False
    for line in GOOD.splitlines(keepends=True):
        if line.startswith("## "):
            skip = line.strip().endswith(name)
        if not skip:
            out.append(line)
    return "".join(out)


class ParseSpecTests(unittest.TestCase):
    def test_normal_input_returns_six_sections_verbatim(self):
        parsed = parse_spec(GOOD)
        self.assertIsInstance(parsed, ParsedSpec)
        data = parsed.as_dict()
        self.assertEqual(list(data.keys()), list(REQUIRED_SECTIONS))
        self.assertIn("课堂需求。", data["来源"])
        self.assertIn("A1：列顺序固定。", data["验收用例"])
        # 原文字段：不应被改写
        self.assertEqual(data["目标"].strip(), "提供一个导出。")

    def test_missing_section_is_rejected_with_location(self):
        for name in REQUIRED_SECTIONS:
            with self.subTest(missing=name):
                with self.assertRaises(SpecError) as ctx:
                    parse_spec(with_section_removed(name))
                self.assertIn(name, str(ctx.exception))
                self.assertIn("缺", str(ctx.exception))

    def test_empty_section_is_rejected(self):
        text = GOOD.replace("## 4. 约束\n\n只读。\n", "## 4. 约束\n\n")
        with self.assertRaises(SpecError) as ctx:
            parse_spec(text)
        self.assertIn("空", str(ctx.exception))

    def test_duplicate_section_is_rejected(self):
        text = GOOD + "\n## 2. 目标\n\n又一个目标。\n"
        with self.assertRaises(SpecError) as ctx:
            parse_spec(text)
        self.assertIn("重复", str(ctx.exception))

    def test_out_of_order_is_rejected(self):
        parts = GOOD.split("## ")
        head, body = parts[0], parts[1:]
        body[1], body[2] = body[2], body[1]   # 交换第 2、3 节
        with self.assertRaises(SpecError) as ctx:
            parse_spec(head + "## " + "## ".join(body))
        self.assertIn("顺序", str(ctx.exception))

    def test_unknown_heading_is_rejected(self):
        text = GOOD + "\n## 7. 附录\n\n多余的章节。\n"
        with self.assertRaises(SpecError) as ctx:
            parse_spec(text)
        self.assertIn("未知", str(ctx.exception))

    def test_headings_inside_fenced_code_are_ignored(self):
        text = GOOD.replace(
            "只读。",
            "只读。示例如下：\n\n```markdown\n## 4. 约束\n\n这是示例，不是真章节。\n```\n",
        )
        parsed = parse_spec(text)
        self.assertIn("这是示例，不是真章节。", parsed.as_dict()["约束"])
        self.assertEqual(len(parsed.as_dict()), 6)

    def test_unclosed_fence_is_rejected(self):
        text = GOOD + "\n```markdown\n## 4. 约束\n\n未闭合。\n"
        with self.assertRaises(SpecError) as ctx:
            parse_spec(text)
        self.assertIn("围栏", str(ctx.exception))

    def test_third_level_headings_are_not_sections(self):
        """回归：### 三级标题曾被误当成二级章节（## 后面又跟了一个 #）。"""
        text = GOOD.replace("A1：列顺序固定。",
                            "### A1 列与顺序\n\n四样俱全。\n\n### A2 可用量\n\n可复算。")
        parsed = parse_spec(text)
        self.assertIn("### A1 列与顺序", parsed.as_dict()["验收用例"])
        self.assertIn("### A2 可用量", parsed.as_dict()["验收用例"])

    def test_parser_does_not_judge_business_correctness(self):
        """结构齐全但业务口径错误的合同，解析器必须照收 —— 业务验收归人。"""
        bad = GOOD.replace("只读。", "available = on_hand + reserved   # 故意写错的公式")
        parsed = parse_spec(bad)
        self.assertIn("on_hand + reserved", parsed.as_dict()["约束"])


class LoadSpecTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="l03-spec-")
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name).resolve()

    def _write(self, name: str, text: str) -> Path:
        p = self.base / name
        p.write_text(text, encoding="utf-8")
        return p

    def test_load_spec_reads_utf8(self):
        p = self._write("中文合同.md", GOOD.replace("课堂需求。", "课堂需求：核对可售数量。"))
        parsed = load_spec(p)
        self.assertIn("核对可售数量", parsed.as_dict()["来源"])

    def test_load_spec_does_not_modify_input(self):
        p = self._write("good.md", GOOD)
        before = hashlib.sha256(p.read_bytes()).hexdigest()
        load_spec(p)
        after = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(before, after, "解析不得修改输入文件")

    def test_load_spec_failure_does_not_modify_input(self):
        p = self._write("bad.md", with_section_removed("约束"))
        before = hashlib.sha256(p.read_bytes()).hexdigest()
        with self.assertRaises(SpecError):
            load_spec(p)
        self.assertEqual(before, hashlib.sha256(p.read_bytes()).hexdigest(),
                         "失败也不得修改输入文件")

    def test_load_spec_missing_file(self):
        with self.assertRaises(SpecError) as ctx:
            load_spec(self.base / "不存在.md")
        self.assertIn("不存在", str(ctx.exception))

    def test_real_spec_and_draft(self):
        """用本讲的两份真实合同跑：确认版应通过，采购草稿结构也有效。"""
        spec = ROOT / "lesson-03-submission" / "FDE_SPEC.md"
        draft = ROOT / "lesson-03-submission" / "procurement-draft.md"
        if spec.is_file():
            data = load_spec(spec).as_dict()
            self.assertEqual(len(data), 6)
        if draft.is_file():
            data = load_spec(draft).as_dict()
            self.assertEqual(len(data), 6)


if __name__ == "__main__":
    unittest.main()
