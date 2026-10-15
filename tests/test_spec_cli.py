"""L03 CLI 集成测试：证明 CLI 真的调用 workbench.spec，而不是一个没人用的练习模块。"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GOOD = """# 合同

## 1. 来源

需求。

## 2. 目标

导出。

## 3. 非目标

不发邮件。

## 4. 约束

只读。

## 5. 验收用例

A1：固定列。

## 6. 完成定义

L03 完成。
"""


class SpecCliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="l03-cli-")
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name).resolve()

    def run_cli(self, *args):
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", "-m", "workbench.cli", *args],
            cwd=str(ROOT), capture_output=True, text=True,
            encoding="utf-8", errors="replace")
        return proc.returncode, proc.stdout, proc.stderr

    def test_cli_accepts_valid_spec_and_prints_six_fields(self):
        p = self.base / "good.md"; p.write_text(GOOD, encoding="utf-8")
        code, out, err = self.run_cli("spec", str(p))
        self.assertEqual(code, 0, f"应退出 0\n{out}\n{err}")
        data = json.loads(out)
        self.assertEqual(len(data), 6)
        for key in ("来源", "目标", "非目标", "约束", "验收用例", "完成定义"):
            self.assertIn(key, data, f"缺少字段 {key}")

    def test_cli_rejects_missing_section_with_nonzero_exit(self):
        text = GOOD.replace("## 4. 约束\n\n只读。\n", "")
        p = self.base / "bad.md"; p.write_text(text, encoding="utf-8")
        code, out, err = self.run_cli("spec", str(p))
        self.assertNotEqual(code, 0, "缺章必须非零退出")
        self.assertIn("约束", out + err, "错误信息应能定位到缺失的章节")

    def test_cli_does_not_modify_input(self):
        p = self.base / "good.md"; p.write_text(GOOD, encoding="utf-8")
        before = hashlib.sha256(p.read_bytes()).hexdigest()
        self.run_cli("spec", str(p))
        self.assertEqual(before, hashlib.sha256(p.read_bytes()).hexdigest())

    def test_cli_uses_the_real_parser_module(self):
        """调用路径证据：把 workbench.spec 标记后，CLI 行为必须依赖它。"""
        p = self.base / "good.md"; p.write_text(GOOD, encoding="utf-8")
        probe = (
            "import sys, json;"
            "import workbench.spec as s;"
            "s.parse_spec = lambda t: (_ for _ in ()).throw(RuntimeError('PROBE_HIT'));"
            "from workbench.cli import main;"
            "sys.exit(main(['spec', %r]))" % str(p)
        )
        proc = subprocess.run([sys.executable, "-X", "utf8", "-c", probe],
                              cwd=str(ROOT), capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
        self.assertIn("PROBE_HIT", proc.stdout + proc.stderr,
                      "CLI 必须通过 workbench.spec.parse_spec 解析，而不是另有一套逻辑")

    def test_existing_commands_still_work(self):
        proc = subprocess.run([sys.executable, "-X", "utf8", "-m", "workbench.cli", "--help"],
                              cwd=str(ROOT), capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
        self.assertIn("spec", proc.stdout)
        self.assertIn("serve-workbench", proc.stdout)
        self.assertIn("workbench-status", proc.stdout)


if __name__ == "__main__":
    unittest.main()
