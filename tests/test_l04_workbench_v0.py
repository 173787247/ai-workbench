"""L04 · Ticket A：工作台 V0 的受控执行能力（**只测本讲范围**）。

对应 `lesson-04-submission/WB-L04-BOOTSTRAP.md` 的六条验收用例。
**测试调用真实 CLI ✗ 使用独立临时数据 ✗ 经过进程边界。**
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
SPEC = ROOT / "lesson-04-submission" / "WB-L04-BOOTSTRAP.md"


def cli(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([PY, "-X", "utf8", "-m", "workbench.cli", *args],
                          cwd=cwd or ROOT, capture_output=True, text=True, encoding="utf-8")


class V0Tests(unittest.TestCase):
    """A-01 ~ A-09 ✗ 对应 Ticket A 的验收用例。"""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="l04-a-")
        self.dir = Path(self.tmp.name)
        self.rt = str(self.dir / "rt")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @staticmethod
    def data(p: subprocess.CompletedProcess) -> dict:
        try:
            return json.loads(p.stdout or p.stderr)
        except Exception:
            return {}

    def mk(self, *, allow: str | None = "workbench/", timeout: int = 60,
           task_id: str = "A-1") -> subprocess.CompletedProcess:
        args = ["task-create", "--task-id", task_id, "--spec-file", str(SPEC),
                "--runtime-dir", self.rt, "--actor", "TESTER", "--timeout", str(timeout)]
        if allow:
            args += ["--allow-write", allow]
        return cli(*args)

    # ── ① Spec 与任务 ──
    def test_a01_task_create_binds_spec_and_stores_digest(self):
        """A-01 建任务时绑定 Spec ✗ 保存原文摘要（**复用 L03 的解析器**）。"""
        r = self.mk()
        self.assertEqual(0, r.returncode, r.stderr)
        d = self.data(r)
        self.assertTrue(d.get("ok"))
        self.assertEqual(hashlib.sha256(SPEC.read_bytes()).hexdigest(), d.get("spec_sha256"))

    def test_a02_task_show_keeps_status_at_human_review(self):
        """A-02 查询任务时状态停在人工复核 ✗ 不自动变成已接受。"""
        self.assertEqual(0, self.mk(task_id="A-2").returncode)
        r = cli("task-show", "--task-id", "A-2", "--runtime-dir", self.rt)
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertEqual("pending_human_review", self.data(r).get("status"))

    # ── ② 受控执行 ──
    def test_a03_verify_only_mode_does_not_write(self):
        """A-03 **仅复验模式**：不调用写入执行器 ✗ 候选目录一字不变。"""
        cand = self.dir / "cand"
        cand.mkdir()
        (cand / "keep.txt").write_text("original", encoding="utf-8")
        self.assertEqual(0, self.mk(task_id="A-3").returncode)
        r = cli("task-run", "--task-id", "A-3", "--candidate", str(cand),
                "--verify-only", "--runtime-dir", self.rt)
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertEqual("original", (cand / "keep.txt").read_text(encoding="utf-8"))
        self.assertEqual("verify_only", self.data(r).get("mode"))

    def test_a04_out_of_scope_write_is_rejected_even_when_command_succeeds(self):
        """⭐ A-04 执行退出码 0 **但改动越界** ⇒ 必须拒绝。

        **手册：「防止实现退化为一律拒绝」** ⇒ 这条与 A-05 成对。
        """
        cand = self.dir / "cand"
        cand.mkdir()
        self.assertEqual(0, self.mk(task_id="A-4").returncode)
        r = cli("task-run", "--task-id", "A-4", "--candidate", str(cand),
                "--allow-write", "workbench/", "--timeout", "60",
                "--exec", f'{PY} -c "open(chr(111)+chr(117)+chr(116)+chr(46)+chr(116)+chr(120)+chr(116),chr(119)).write(chr(120))"',
                "--runtime-dir", self.rt)
        self.assertNotEqual(0, r.returncode, "越界写入必须被拒绝")
        self.assertEqual("out_of_scope", self.data(r).get("error_code"))

    def test_a05_in_scope_write_is_accepted_with_evidence(self):
        """A-05 正常路径：范围内写入被接受 ✗ 保存输出/退出码/Diff。"""
        cand = self.dir / "cand"
        (cand / "workbench").mkdir(parents=True)
        self.assertEqual(0, self.mk(task_id="A-5").returncode)
        r = cli("task-run", "--task-id", "A-5", "--candidate", str(cand),
                "--allow-write", "workbench/", "--timeout", "60",
                "--exec", f'{PY} -c "open(chr(119)+chr(111)+chr(114)+chr(107)+chr(98)+chr(101)+chr(110)+chr(99)+chr(104)+chr(47)+chr(110)+chr(46)+chr(112)+chr(121),chr(119)).write(chr(120))"',
                "--runtime-dir", self.rt)
        self.assertEqual(0, r.returncode, r.stderr)
        d = self.data(r)
        self.assertEqual(0, d.get("returncode"))
        self.assertIn("diff", d)
        self.assertIn("workbench/n.py", d.get("changed", []))

    def test_a06_missing_write_scope_is_rejected_up_front(self):
        """⭐ A-06 **缺写集 ⇒ 先拒绝**（**手册：「真实执行缺写集应先拒绝」**）。"""
        cand = self.dir / "cand"
        cand.mkdir()
        r = self.mk(allow=None, task_id="A-6")
        self.assertEqual(0, r.returncode, r.stderr)
        r2 = cli("task-run", "--task-id", "A-6", "--candidate", str(cand),
                 "--timeout", "60",
                 "--exec", f'{PY} -c "open(chr(97),chr(119)).write(chr(120))"',
                 "--runtime-dir", self.rt)
        self.assertNotEqual(0, r2.returncode, "缺写集必须先拒绝")
        # ⭐ 修订（复验者指出）：原来 assertIn 放行了 out_of_scope，
        #   而它与 write_scope_required **语义相反**（一个是事后判一个是事前拒）
        #   ⇒ 收紧成只认事前拒绝，并**断言命令真的没被执行**。
        self.assertEqual("write_scope_required", self.data(r2).get("error_code"))
        self.assertFalse((cand / "a").exists(), "缺写集时必须先拒绝，不能跑完再判")

    def test_a10_write_outside_candidate_is_detected_and_rejected(self):
        """⭐ A-10 **候选目录之外的写入必须被发现并拒绝**。

        这一条是 L04 独立复验者查出来的高危缺口：
        原来 `--allow-write workbench/` 下用 `../` 改掉候选目录外的文件，
        报告却是 `{"ok": true, "changed": [], "out_of_scope": []}` —— **零告警**。
        """
        cand = self.dir / "cand"
        cand.mkdir()
        sibling = self.dir / "sibling"
        sibling.mkdir()
        victim = sibling / "victim.txt"
        victim.write_text("原样", encoding="utf-8")
        self.assertEqual(0, self.mk(task_id="A-10").returncode)
        r = cli("task-run", "--task-id", "A-10", "--candidate", str(cand),
                "--allow-write", "workbench/", "--timeout", "60",
                "--exec", f'{PY} -c "import pathlib; pathlib.Path(chr(46)+chr(46)+chr(47)+chr(115)+chr(105)+chr(98)+chr(108)+chr(105)+chr(110)+chr(103)+chr(47)+chr(118)+chr(105)+chr(99)+chr(116)+chr(105)+chr(109)+chr(46)+chr(116)+chr(120)+chr(116)).write_text(chr(88))"',
                "--runtime-dir", self.rt)
        self.assertNotEqual(0, r.returncode, "候选目录之外的写入必须被拒绝")
        d = self.data(r)
        self.assertEqual("escaped_candidate", d.get("error_code"))
        self.assertTrue(d.get("escaped_candidate"), "要列出被越界改动的文件")
        self.assertNotIn("已回滚", json.dumps(d, ensure_ascii=False))

    # ── ③ 失败与超时 ──
    def test_a07_failing_command_is_not_recorded_as_success(self):
        """A-07 命令失败不会被写成成功。"""
        cand = self.dir / "cand"
        cand.mkdir()
        self.assertEqual(0, self.mk(task_id="A-7").returncode)
        r = cli("task-run", "--task-id", "A-7", "--candidate", str(cand),
                "--allow-write", "workbench/", "--timeout", "60",
                "--exec", f'{PY} -c "import sys; sys.exit(3)"', "--runtime-dir", self.rt)
        self.assertNotEqual(0, r.returncode)
        self.assertFalse(self.data(r).get("ok"))

    def test_a08_timeout_stops_and_is_not_written_as_rollback(self):
        """A-08 超时**停止**；断言 `rolled_back` 为假 ✗ 且不出现"已回滚"。"""
        cand = self.dir / "cand"
        cand.mkdir()
        self.assertEqual(0, self.mk(task_id="A-8", timeout=30).returncode)
        r = cli("task-run", "--task-id", "A-8", "--candidate", str(cand),
                "--allow-write", "workbench/", "--timeout", "30",
                "--exec", f'{PY} -c "import time; time.sleep(40)"', "--runtime-dir", self.rt)
        self.assertNotEqual(0, r.returncode)
        d = self.data(r)
        self.assertFalse(d.get("rolled_back"), "停止不得被写成已回滚")
        self.assertNotIn("已回滚", json.dumps(d, ensure_ascii=False))
        self.assertIn("停止", json.dumps(d, ensure_ascii=False))

    # ── ④ 最小 Eval 与审核入口 ──
    def test_a09_eval_pass_still_waits_for_named_human(self):
        """A-09 自动检查通过后仍待人审 ✗ 且**没有具名的人就不能接受**。"""
        cand = self.dir / "cand"
        (cand / "workbench").mkdir(parents=True)
        self.assertEqual(0, self.mk(task_id="A-9").returncode)
        cli("task-run", "--task-id", "A-9", "--candidate", str(cand),
            "--allow-write", "workbench/", "--timeout", "60",
            "--exec", f'{PY} -c "open(chr(119)+chr(111)+chr(114)+chr(107)+chr(98)+chr(101)+chr(110)+chr(99)+chr(104)+chr(47)+chr(110)+chr(46)+chr(112)+chr(121),chr(119)).write(chr(120))"',
            "--runtime-dir", self.rt)
        # ① ⭐ 修订（复验者指出）：原来 docstring 说"仍待人审"却直接 accept，
        #   断言里**没有** pending_human_review ⇒ 换成"执行通过即自动 accept"照样过。
        #   ⇒ 先断言状态**仍是**待审，且执行结果确实通过了自动检查。
        show = cli("task-show", "--task-id", "A-9", "--runtime-dir", self.rt)
        self.assertEqual(0, show.returncode, show.stderr)
        sd = self.data(show)
        self.assertEqual("pending_human_review", sd.get("status"),
                         "自动检查通过后必须仍停在人工复核")
        self.assertTrue((sd.get("execution") or {}).get("ok"),
                        "这一步的前提是自动检查确实通过了")
        # ② 再由具名的人接受
        r = cli("task-review", "--task-id", "A-9", "--decision", "accept",
                "--actor", "REVIEWER", "--runtime-dir", self.rt)
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertEqual("accepted", self.data(r).get("status"))
        # ③ 不存在的任务不能接受
        r2 = cli("task-review", "--task-id", "NOPE", "--decision", "accept",
                 "--actor", "REVIEWER", "--runtime-dir", self.rt)
        self.assertNotEqual(0, r2.returncode)
        # ④ 匿名/agent 不能当审核人
        r3 = cli("task-review", "--task-id", "A-9", "--decision", "accept",
                 "--actor", "agent:bot", "--runtime-dir", self.rt)
        self.assertNotEqual(0, r3.returncode, "agent 前缀不得当审核人")


if __name__ == "__main__":
    unittest.main()
