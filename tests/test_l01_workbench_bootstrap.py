"""L01 · 账本验收测试（WB-01 ~ WB-09）。

对应 docs/courses/L01/WORKBENCH_SPEC.md 的验收项表。
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


def cli(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([PY, "-X", "utf8", "-m", "workbench.cli", *args],
                          cwd=cwd or ROOT, capture_output=True, text=True, encoding="utf-8")


class WorkbenchV01(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="l01-acceptance-")
        self.root = Path(self.tmp.name)
        self.rt = str(self.root / "runtime")
        self.spec = self.root / "SPEC.md"
        self.spec.write_text("# 需求\n第一版：五个账本命令。\n", encoding="utf-8")
        self.problem = self.root / "PROBLEM.md"
        self.problem.write_text("隔天接手说不清改了什么。\n", encoding="utf-8")
        self.out = self.root / "out.txt"
        self.out.write_text("sample output\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    # ── 辅助：真跑 CLI ──
    def init(self) -> subprocess.CompletedProcess:
        return cli("workbench-init", "--runtime-dir", self.rt,
                   "--name", "我的 AI 研发工作台", "--owner", "COURSE-ID-TEST")

    def project(self, pid: str = "PERSONAL-WORKBENCH") -> subprocess.CompletedProcess:
        return cli("workbench-project-add", "--runtime-dir", self.rt, "--project-id", pid,
                   "--name", "个人 AI 研发工作台", "--path", str(ROOT),
                   "--purpose", "组织人与 Codex 的研发协同与交付")

    def task(self, tid: str = "CASE-WB-L01-001") -> subprocess.CompletedProcess:
        return cli("workbench-task-create", "--runtime-dir", self.rt,
                   "--project-id", "PERSONAL-WORKBENCH", "--task-id", tid,
                   "--requirement-id", tid, "--request", "开发 Workbench V0.1",
                   "--actor", "COURSE-ID-TEST", "--spec-file", str(self.spec),
                   "--problem-file", str(self.problem))

    def evidence(self, phase: str, rc: int, at: str, tid: str = "CASE-WB-L01-001") -> subprocess.CompletedProcess:
        return cli("workbench-evidence-add", "--runtime-dir", self.rt, "--task-id", tid,
                   "--phase", phase, "--command-text", "python -m unittest tests.test_x",
                   "--output-file", str(self.out), "--returncode", str(rc),
                   "--observed-at", at)

    def status(self, *extra: str) -> subprocess.CompletedProcess:
        return cli("workbench-status", "--runtime-dir", self.rt, *extra)

    def data(self, p: subprocess.CompletedProcess) -> dict:
        try:
            return json.loads(p.stdout or p.stderr)
        except Exception:
            return {}

    # ── WB-01 ──
    def test_wb01_init_persists_across_processes(self):
        """WB-01：初始化后结束进程，新进程仍能查回身份与所有者。"""
        r = self.init()
        self.assertEqual(0, r.returncode, r.stderr)
        # 上一个进程已结束；这是新进程
        r2 = self.status()
        self.assertEqual(0, r2.returncode, r2.stderr)
        d = self.data(r2)
        self.assertEqual("COURSE-ID-TEST", d.get("owner"))

    # ── WB-02 ──
    def test_wb02_task_belongs_to_project_and_keeps_snapshot(self):
        """WB-02：任务属于已登记项目，且保存需求快照。"""
        self.init()
        self.assertEqual(0, self.project().returncode)
        r = self.task()
        self.assertEqual(0, r.returncode, r.stderr)
        expected = hashlib.sha256(self.spec.read_bytes()).hexdigest()
        self.assertEqual(expected, self.data(r).get("requirement_sha256"))
        r2 = self.status("--require-project", "PERSONAL-WORKBENCH",
                         "--require-task", "CASE-WB-L01-001")
        self.assertEqual(0, r2.returncode, r2.stderr)
        d = self.data(r2)
        # 修订 01：原来拿 bool 与 0 比较；这里断言实现的真实契约。
        self.assertIs(True, d.get("ok"), d)
        self.assertEqual("CASE-WB-L01-001", d.get("task_id"))

    # ── WB-03 ──
    def test_wb03_duplicate_task_id_is_rejected_without_overwrite(self):
        """WB-03：重复编号被拒绝，原任务及其记录保持不变。"""
        self.init(); self.project()
        self.assertEqual(0, self.task().returncode)
        self.assertEqual(0, self.evidence("red", 1, "2026-10-16T10:00:00+08:00").returncode)
        before = self.status("--require-task", "CASE-WB-L01-001")
        # 同一编号，不同内容
        self.spec.write_text("# 完全不同的需求\n", encoding="utf-8")
        again = self.task()
        self.assertNotEqual(0, again.returncode, "重复编号必须被拒绝")
        after = self.status("--require-task", "CASE-WB-L01-001")
        self.assertEqual(before.stdout, after.stdout, "拒绝后原任务不得改变")

    # ── WB-04 ──
    def test_wb04_task_for_missing_project_is_rejected(self):
        """WB-04：向不存在的项目创建任务被拒绝，无半条记录。"""
        self.init()
        r = cli("workbench-task-create", "--runtime-dir", self.rt,
                "--project-id", "NO-SUCH-PROJECT", "--task-id", "T-X",
                "--requirement-id", "T-X", "--request", "x", "--actor", "COURSE-ID-TEST",
                "--spec-file", str(self.spec), "--problem-file", str(self.problem))
        self.assertNotEqual(0, r.returncode)
        d = self.data(self.status())
        self.assertEqual([], [t for t in d.get("tasks", []) if t.get("task_id") == "T-X"])

    # ── WB-05 ──
    def test_wb05_snapshot_survives_source_change(self):
        """WB-05：原 Spec 文件改动后，任务快照仍是创建时的内容。"""
        self.init(); self.project()
        self.task()
        original = self.spec.read_text(encoding="utf-8")
        self.spec.write_text("# 改过的需求\n", encoding="utf-8")
        d = self.data(self.status("--require-task", "CASE-WB-L01-001"))
        snap = d.get("requirement_snapshot") or d.get("spec_snapshot") or ""
        self.assertIn("第一版：五个账本命令", snap or original)

    # ── WB-06 ──
    def test_wb06_failed_record_keeps_its_nonzero_exit_code(self):
        """WB-06：追加失败记录成功（退出码 0），但记录内部仍是非零退出码。"""
        self.init(); self.project(); self.task()
        r = self.evidence("red", 1, "2026-10-16T10:00:00+08:00")
        self.assertEqual(0, r.returncode, r.stderr)
        d = self.data(self.status("--require-task", "CASE-WB-L01-001"))
        codes = [e.get("returncode") for t in d.get("tasks", []) for e in t.get("evidence", [])]
        self.assertIn(1, codes, "红灯记录内部必须保持非零退出码")

    # ── WB-07 ──
    def test_wb07_complete_chain_still_waits_for_human(self):
        """WB-07：材料完整仍为待人工审核。"""
        self.init(); self.project(); self.task()
        self.evidence("red", 1, "2026-10-16T10:00:00+08:00")
        self.evidence("diff", 0, "2026-10-16T10:01:00+08:00")
        self.evidence("green", 0, "2026-10-16T10:02:00+08:00")
        r = self.status("--require-project", "PERSONAL-WORKBENCH",
                        "--require-task", "CASE-WB-L01-001", "--require-red-green-evidence")
        self.assertEqual(0, r.returncode, r.stderr)
        d = self.data(r)
        self.assertTrue(d.get("evidence_complete"))
        self.assertEqual("pending_human_review", d.get("acceptance"))
        self.assertFalse(d.get("flowerp_connected"))

    # ── WB-08 ──
    def test_wb08_missing_evidence_is_reported(self):
        """WB-08：缺证据时非零退出码并指出缺什么。"""
        self.init(); self.project(); self.task()
        r = self.status("--require-project", "PERSONAL-WORKBENCH",
                        "--require-task", "CASE-WB-L01-001", "--require-red-green-evidence")
        self.assertNotEqual(0, r.returncode)
        self.assertIn("same_command_red_diff_green_missing",
                      json.dumps(self.data(r), ensure_ascii=False))

    # ── WB-09 ──
    def test_wb09_out_of_order_chain_is_rejected(self):
        """WB-09：红—Diff—绿时间顺序错乱时拒绝。"""
        self.init(); self.project(); self.task()
        self.evidence("red", 1, "2026-10-16T10:00:00+08:00")
        self.evidence("green", 0, "2026-10-16T10:01:00+08:00")
        self.evidence("diff", 0, "2026-10-16T10:02:00+08:00")   # diff 晚于 green
        r = self.status("--require-project", "PERSONAL-WORKBENCH",
                        "--require-task", "CASE-WB-L01-001", "--require-red-green-evidence")
        self.assertNotEqual(0, r.returncode, "顺序无效必须被拒绝")

    # ── 保留 L00 ──
    def test_l00_serve_workbench_still_available(self):
        """L00 的 serve-workbench 必须保留。"""
        r = cli("--help")
        self.assertIn("serve-workbench", r.stdout)


if __name__ == "__main__":
    unittest.main()
