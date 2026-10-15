"""L03 · Spec 解析器的结构检查（六字段 ✗ 围栏 ✗ 顺序 ✗ 只读）。

对应 `docs/courses/L03/FDE_SPEC.md` 与手册第 5 步的检查清单。
**测试调用真实 CLI ✗ 使用独立临时数据 ✗ 经过进程边界。**
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
FENCE = chr(96) * 3

HEADINGS = ("来源", "目标", "非目标", "约束", "验收用例", "完成定义")
FIELDS = ("source", "goal", "non_goals", "constraints", "acceptance", "done")


def contract(**overrides: str) -> str:
    """造一份六段合同。`None` ⇒ 整节删掉。"""
    body = {
        "来源": "运营原话：想知道还能承诺多少，以及货在哪里。",
        "目标": "导出可定位货物的库存明细。",
        "非目标": "不发邮件，不自动补货，不修改库存。",
        "约束": "八列，顺序 sku,name,site,location,lot_id,on_hand,reserved,available。",
        "验收用例": "东仓在库 8、预占 3，可用量应为 5。",
        "完成定义": "交接确认合同与可用解析器。",
    }
    body.update(overrides)
    parts = []
    for h in HEADINGS:
        if body[h] is None:
            continue
        parts.append("## " + h + "\n" + body[h] + "\n")
    return "# FDE_SPEC\n\n" + "\n".join(parts)


class SpecParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="l03-spec-")
        self.dir = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, text: str, name: str = "FDE_SPEC.md") -> Path:
        p = self.dir / name
        p.write_text(text, encoding="utf-8")
        return p

    def run_cli(self, spec: Path) -> subprocess.CompletedProcess:
        return subprocess.run([PY, "-X", "utf8", "-m", "workbench.cli", "spec", str(spec)],
                              cwd=ROOT, capture_output=True, text=True, encoding="utf-8")

    @staticmethod
    def data(p: subprocess.CompletedProcess) -> dict:
        try:
            return json.loads(p.stdout or p.stderr)
        except Exception:
            return {}

    # ── 正常 ──
    def test_wb10_full_contract_returns_six_fields_verbatim(self):
        """WB-10 六字段与原文一致（原样返回，不做加工）。"""
        p = self.write(contract())
        r = self.run_cli(p)
        self.assertEqual(0, r.returncode, r.stderr)
        d = self.data(r)
        for f in FIELDS:
            self.assertIn(f, d)
        self.assertIn("导出可定位货物的库存明细。", r.stdout)
        self.assertIn("东仓在库 8、预占 3，可用量应为 5。", r.stdout)

    # ── 结构错误（**手册：缺章 ✗ 空章 ✗ 重复 ✗ 乱序 ✗ 未知标题** ✓）──
    def test_wb11_missing_section_is_rejected(self):
        """WB-11 缺章被拒绝，且错误指出是哪一章。"""
        p = self.write(contract(约束=None))
        r = self.run_cli(p)
        self.assertNotEqual(0, r.returncode)
        blob = r.stdout + r.stderr
        self.assertIn("约束", blob)
        self.assertIn("missing_section", blob)

    def test_wb12_empty_section_is_rejected(self):
        """WB-12 空章被拒绝。"""
        p = self.write(contract(目标="   "))
        r = self.run_cli(p)
        self.assertNotEqual(0, r.returncode)
        self.assertIn("empty_section", r.stdout + r.stderr)

    def test_wb13_duplicate_section_is_rejected(self):
        """WB-13 重复标题不能悄悄覆盖。"""
        p = self.write(contract() + "\n## 目标\n另一个目标。\n")
        r = self.run_cli(p)
        self.assertNotEqual(0, r.returncode)
        self.assertIn("duplicate_section", r.stdout + r.stderr)

    def test_wb14_out_of_order_is_rejected(self):
        """WB-14 乱序被拒绝。"""
        swapped = ("# S\n\n## 目标\nG.\n\n## 来源\nS.\n\n## 非目标\nNG.\n\n"
                   "## 约束\nC.\n\n## 验收用例\nA.\n\n## 完成定义\nD.\n")
        r = self.run_cli(self.write(swapped))
        self.assertNotEqual(0, r.returncode)
        self.assertIn("section_out_of_order", r.stdout + r.stderr)

    def test_wb15_unknown_heading_is_rejected(self):
        """WB-15 未知二级标题明确报错。"""
        r = self.run_cli(self.write(contract() + "\n## 备注\n多余的。\n"))
        self.assertNotEqual(0, r.returncode)
        self.assertIn("unknown_heading", r.stdout + r.stderr)

    # ── 代码围栏（**辅导资料点名** ✓）──
    def test_wb16_fenced_heading_is_not_a_section(self):
        """WB-16 围栏里的 `## 目标` 只是正文示例，不当章节。"""
        text = contract(约束="见示例：\n\n" + FENCE + "markdown\n## 目标\n这是示例。\n" + FENCE + "\n")
        r = self.run_cli(self.write(text))
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertIn("导出可定位货物的库存明细。", r.stdout)

    def test_wb17_unclosed_fence_is_rejected(self):
        """WB-17 未闭合围栏应拒绝（**否则会吞掉后面的章节**）。"""
        text = contract(约束="开了不关：\n\n" + FENCE + "markdown\n## 目标\n被吞掉的。\n")
        r = self.run_cli(self.write(text))
        self.assertNotEqual(0, r.returncode)
        self.assertIn("unclosed_fence", r.stdout + r.stderr)

    # ── 只读（**手册：失败前后原文件哈希不变** ✓）──
    def test_wb18_input_file_hash_unchanged(self):
        """WB-18 成功与失败前后，原文件哈希都不变。"""
        for text in (contract(), contract(约束=None)):
            p = self.write(text, name="x.md")
            before = hashlib.sha256(p.read_bytes()).hexdigest()
            self.run_cli(p)
            self.assertEqual(before, hashlib.sha256(p.read_bytes()).hexdigest())

    # ── 集成：**CLI 必须用同一个 parse_spec** ──
    def test_wb19_cli_uses_workbench_spec_module(self):
        """WB-19 调用路径证明 CLI 用的是 `workbench.spec`，不是另写一套。"""
        import workbench.cli as cli_mod
        import workbench.spec as spec_mod
        self.assertIs(cli_mod.load_spec, spec_mod.load_spec)
        self.assertFalse(hasattr(cli_mod, "_scan"), "cli 里不应有第二套解析逻辑")
        self.assertFalse(hasattr(cli_mod, "SECTIONS"), "cli 里不应有第二份章节表")


if __name__ == "__main__":
    unittest.main()
