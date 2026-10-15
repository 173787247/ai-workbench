"""L02 · 状态语义的更强不变量（**钉住 AGENTS.md 里那条"已知缺口"**）。

⭐ 为什么有这个文件：

`AGENTS.md` 的「已知缺口」写着—— **"测试全绿"在本仓库不构成"这个改动是对的"的证据**。
L02 的 N1 执行者把这句话当成**待检验的断言**去实测，结果发现缺口是真的：

    变体 B = **只把两处文案改成「已验收通过」✗ 字段取值不动**
    ⇒ `tests.test_l01_workbench_bootstrap` + `tests.test_workbench_server`
       **Ran 14 tests ✗ OK ✗ 退出码 0（全绿）**
    ⇒ 系统会一边输出 `acceptance="pending_human_review"` ✗ 一边文案写「已验收通过」
    ⇒ **规定测试毫无反应** ⚠️

本文件补上三条不变量 ✗ 让"只改文案"这条路**走不通**。

**辨别力验证**（**不是"跑通了就算"** ✗ 要证明它抓得住那个变体）：
对未改的仓库 ⇒ 通过；对变体 B 的副本 ⇒ **必须失败**。
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
BOOTSTRAP = ROOT / "workbench" / "bootstrap.py"

# 替人签字的说法（**AGENTS.md:44-46 点名禁止**）
FORBIDDEN = ("已验收通过", "验收通过", "accepted", "已接受", "人工已接受")
# 三处同一语义的位置（**AGENTS.md:47-48 禁止只改之一**）
SITES = ("review_status", "review_note", "note")


def cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([PY, "-X", "utf8", "-m", "workbench.cli", *args],
                          cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


class StatusInvariantTests(unittest.TestCase):
    """三条不变量 ✗ 对应 AGENTS.md「状态与历史」一节。"""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="l02-inv-")
        self.rt = str(Path(self.tmp.name) / "rt")
        self.spec = Path(self.tmp.name) / "SPEC.md"
        self.spec.write_text("# 需求\nL02 不变量测试。\n", encoding="utf-8")
        self.problem = Path(self.tmp.name) / "P.md"
        self.problem.write_text("隔天接手说不清。\n", encoding="utf-8")
        self.out = Path(self.tmp.name) / "o.txt"
        self.out.write_text("out\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _complete_chain(self) -> dict:
        cli("workbench-init", "--runtime-dir", self.rt, "--owner", "T-1", "--name", "W")
        cli("workbench-project-add", "--runtime-dir", self.rt, "--project-id", "P", "--name", "N")
        cli("workbench-task-create", "--runtime-dir", self.rt, "--project-id", "P",
            "--task-id", "T", "--spec-file", str(self.spec),
            "--problem-file", str(self.problem), "--actor", "T-1")
        for phase, rc, minute in (("red", 1, 0), ("diff", 0, 1), ("green", 0, 2)):
            cli("workbench-evidence-add", "--runtime-dir", self.rt, "--task-id", "T",
                "--phase", phase, "--command-text", "python -m unittest",
                "--output-file", str(self.out), "--returncode", str(rc),
                "--observed-at", f"2026-10-16T10:0{minute}:00+08:00")
        r = cli("workbench-status", "--runtime-dir", self.rt, "--require-task", "T",
                "--require-red-green-evidence")
        self.assertEqual(0, r.returncode, r.stderr)
        return json.loads(r.stdout)

    # ── 不变量 1 ──
    def test_inv01_acceptance_is_a_fact_field_and_stays_pending(self):
        """三条记录齐全时，`acceptance` 仍必须是 `pending_human_review`（**事实字段**）。"""
        d = self._complete_chain()
        self.assertTrue(d.get("evidence_complete"))
        self.assertEqual("pending_human_review", d.get("acceptance"))
        self.assertEqual("pending_human_review", d.get("review_status"))

    # ── 不变量 2 ──
    def test_inv02_no_site_claims_acceptance(self):
        """⭐ **任何一处文案都不得出现替人签字的说法**。

        这一条正是变体 B（**只改文案**）会踩中的：
        `test_l01_*` 只看字段值 ✗ 所以对"文案写成已验收"没有反应。
        """
        d = self._complete_chain()
        blob = json.dumps(d, ensure_ascii=False)
        for word in FORBIDDEN:
            self.assertNotIn(word, blob, f"输出里出现了替人签字的说法：{word}")

    # ── 不变量 3 ──
    def test_inv03_three_sites_stay_consistent(self):
        """⭐ **源码里三处同一语义必须一致表达"待人工审核"**（AGENTS.md:47-48）。"""
        src = BOOTSTRAP.read_text(encoding="utf-8")
        # 取出三处的字面量
        got: dict[str, list[str]] = {}
        for label, pat in (("review_status", r'"review_status":\s*"([^"]+)"'),
                           ("review_note", r'"review_note":\s*"([^"]+)"'),
                           ("note", r'result\["note"\]\s*=\s*"([^"]+)"')):
            got[label] = re.findall(pat, src)
        self.assertTrue(got["review_note"], "取不到 review_note ✗ 锚点可能变了")
        self.assertTrue(got["note"], "取不到 completeness.note ✗ 锚点可能变了")
        # 三处都不得替人签字
        flat = " ".join(v for vs in got.values() for v in vs)
        for word in FORBIDDEN:
            self.assertNotIn(word, flat, f"源码文案里出现了：{word}")
        # 两项事实分别表达：字段是取值 ✗ 文案是说明
        self.assertEqual(["pending_human_review"] * len(got["review_status"]),
                         got["review_status"], "review_status 取值被改了 ✗ 它是事实字段")


if __name__ == "__main__":
    unittest.main()
