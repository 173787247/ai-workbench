"""L01 账本验收测试：初始化、项目登记、任务创建、记录追加、状态查询。

对应 `docs/courses/L01/WORKBENCH_SPEC.md` §5（五个命令输入与结果）、§6（完整性与人工审核）
与 §8（验收用例 WB-01~WB-12）。

设计约束：
- 全部通过**子进程**调用真实 CLI，不使用 mock，确保测的是实际入口。
- 每个用例使用**独立的临时运行目录**，互不污染。
- 断言**退出码**与**失败后状态**，不只断言输出文字。

> 本文件在实现前先写，用于产生「有效的实现前失败」。
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-X", "utf8", "-m", "workbench.cli"]


def run(args, runtime: Path, *, cwd: Path = ROOT):
    """跑一次 CLI，返回 (退出码, stdout, stderr)。"""
    cmd = [*CLI, *args, "--runtime-dir", str(runtime)]
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


class WorkbenchBootstrapTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="l01-ledger-")
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name).resolve()
        self.runtime = self.base / "runtime"

    # ---------- WB-01 初始化并跨进程重查 ----------
    def test_wb01_init_then_query_persists(self):
        code, out, err = run(["workbench-init", "--owner", "test-owner",
                              "--name", "个人 AI 研发工作台"], self.runtime)
        self.assertEqual(code, 0, f"init 应成功，实际 {code}\nstdout={out}\nstderr={err}")
        code, out, err = run(["workbench-status"], self.runtime)
        self.assertEqual(code, 0, f"status 应成功，实际 {code}\n{err}")
        payload = json.loads(out)
        self.assertEqual(payload["workbench"]["owner"], "test-owner")

    def test_wb01b_init_refuses_to_overwrite_other_owner(self):
        run(["workbench-init", "--owner", "alice"], self.runtime)
        code, out, err = run(["workbench-init", "--owner", "bob"], self.runtime)
        self.assertNotEqual(code, 0, "第二个所有者不得覆盖既有工作台")
        code, out, _ = run(["workbench-status"], self.runtime)
        self.assertEqual(json.loads(out)["workbench"]["owner"], "alice")

    # ---------- WB-02 项目登记 + 任务创建 + 快照 ----------
    def setUpLedger(self):
        self.assertEqual(run(["workbench-init", "--owner", "test-owner"], self.runtime)[0], 0)
        self.assertEqual(run(["workbench-project-add", "--project-id", "P-1",
                              "--name", "个人 AI 研发工作台"], self.runtime)[0], 0)
        self.spec = self.base / "spec.md"
        self.spec.write_text("# 需求\n原始需求内容 A\n", encoding="utf-8")
        self.problem = self.base / "problem.md"
        self.problem.write_text("原始问题内容 A\n", encoding="utf-8")

    def test_wb02_task_belongs_to_project_and_snapshots(self):
        self.setUpLedger()
        code, out, err = run(["workbench-task-create", "--project-id", "P-1",
                              "--task-id", "T-1", "--title", "建账本",
                              "--spec-file", str(self.spec),
                              "--problem-file", str(self.problem)], self.runtime)
        self.assertEqual(code, 0, f"task-create 应成功，实际 {code}\n{err}")
        code, out, _ = run(["workbench-status", "--require-task", "T-1"], self.runtime)
        self.assertEqual(code, 0)

    # ---------- WB-03 不存在的项目 ----------
    def test_wb03_task_on_missing_project_fails(self):
        self.setUpLedger()
        code, out, err = run(["workbench-task-create", "--project-id", "P-NOPE",
                              "--task-id", "T-404", "--title", "x",
                              "--spec-file", str(self.spec)], self.runtime)
        self.assertNotEqual(code, 0, "项目不存在时必须失败")
        code, out, _ = run(["workbench-status"], self.runtime)
        self.assertNotIn("T-404", out, "不得产生无所属项目的任务")

    # ---------- WB-04 重复任务编号不覆盖 ----------
    def test_wb04_duplicate_task_id_does_not_overwrite(self):
        self.setUpLedger()
        run(["workbench-task-create", "--project-id", "P-1", "--task-id", "T-1",
             "--title", "第一版", "--spec-file", str(self.spec)], self.runtime)
        self.spec.write_text("# 需求\n改过的内容 B\n", encoding="utf-8")
        code, _, _ = run(["workbench-task-create", "--project-id", "P-1", "--task-id", "T-1",
                          "--title", "第二版", "--spec-file", str(self.spec)], self.runtime)
        self.assertNotEqual(code, 0, "同编号第二次必须失败")
        code, out, _ = run(["workbench-status", "--require-task", "T-1"], self.runtime)
        self.assertEqual(code, 0)
        self.assertIn("第一版", out, "原任务标题不得被改写")
        self.assertNotIn("第二版", out)

    # ---------- WB-05 快照不随原文件改变 ----------
    def test_wb05_snapshot_survives_source_edit(self):
        self.setUpLedger()
        run(["workbench-task-create", "--project-id", "P-1", "--task-id", "T-1",
             "--title", "快照", "--spec-file", str(self.spec)], self.runtime)
        code1, out1, _ = run(["workbench-status", "--require-task", "T-1"], self.runtime)
        self.spec.write_text("# 需求\n完全不同的内容 C\n", encoding="utf-8")
        code2, out2, _ = run(["workbench-status", "--require-task", "T-1"], self.runtime)
        self.assertEqual(code1, 0)
        self.assertEqual(code2, 0)
        self.assertEqual(json.loads(out1)["tasks"]["T-1"]["spec_sha256"],
                         json.loads(out2)["tasks"]["T-1"]["spec_sha256"],
                         "原文件改了，任务里的需求摘要不得变")

    # ---------- WB-06 / WB-10 缺证据与错误查询 ----------
    def test_wb06_missing_evidence_fails_red_green_check(self):
        self.setUpLedger()
        run(["workbench-task-create", "--project-id", "P-1", "--task-id", "T-1",
             "--title", "缺证据", "--spec-file", str(self.spec)], self.runtime)
        code, out, err = run(["workbench-status", "--require-task", "T-1",
                              "--require-red-green-evidence"], self.runtime)
        self.assertNotEqual(code, 0, "没有红灯/绿灯记录时完整性检查必须失败")
        self.assertIn("T-1", out + err, "失败也要保留任务")

    def test_wb10_query_missing_task_or_uninitialised(self):
        code, _, _ = run(["workbench-status"], self.runtime)
        self.assertNotEqual(code, 0, "未初始化目录查询必须失败")
        self.assertFalse((self.runtime / "workbench.db").exists(),
                         "查询不得偷偷创建运行库")

    def test_wb10b_query_missing_task_fails_without_creating(self):
        self.setUpLedger()
        code, _, _ = run(["workbench-status", "--require-task", "T-NOPE"], self.runtime)
        self.assertNotEqual(code, 0)

    # ---------- WB-07 / WB-08 / WB-09 红绿链 ----------
    def _add(self, task, phase, cmd, output, rc, observed):
        f = self.base / f"{phase}.txt"
        f.write_text(output, encoding="utf-8")
        return run(["workbench-evidence-add", "--task-id", task, "--phase", phase,
                    "--command-text", cmd, "--output-file", str(f),
                    "--returncode", str(rc), "--observed-at", observed], self.runtime)

    def test_wb07_same_command_red_then_green_passes_but_pending_human(self):
        self.setUpLedger()
        run(["workbench-task-create", "--project-id", "P-1", "--task-id", "T-1",
             "--title", "红绿", "--spec-file", str(self.spec)], self.runtime)
        self.assertEqual(self._add("T-1", "red", "python -m unittest tests.x",
                                   "FAILED (failures=1)", 1, "2026-10-15T09:00:00+00:00")[0], 0)
        d = self.base / "d.diff"; d.write_text("--- a\n+++ b\n", encoding="utf-8")
        self.assertEqual(run(["workbench-evidence-add", "--task-id", "T-1", "--phase", "diff",
                              "--command-text", "git diff", "--output-file", str(d),
                              "--returncode", "0",
                              "--observed-at", "2026-10-15T09:05:00+00:00"], self.runtime)[0], 0)
        self.assertEqual(self._add("T-1", "green", "python -m unittest tests.x",
                                   "OK", 0, "2026-10-15T09:10:00+00:00")[0], 0)
        code, out, err = run(["workbench-status", "--require-task", "T-1",
                              "--require-red-green-evidence"], self.runtime)
        self.assertEqual(code, 0, f"同命令红→绿应通过完整性检查\n{out}\n{err}")
        payload = json.loads(out)
        self.assertTrue(payload.get("evidence_complete"))
        self.assertEqual(payload.get("acceptance"), "pending_human_review",
                         "程序永远不能替人签字")

    def test_wb08_different_command_green_cannot_pair_with_red(self):
        self.setUpLedger()
        run(["workbench-task-create", "--project-id", "P-1", "--task-id", "T-1",
             "--title", "不同命令", "--spec-file", str(self.spec)], self.runtime)
        self._add("T-1", "red", "python -m unittest tests.a", "FAILED", 1,
                  "2026-10-15T09:00:00+00:00")
        self._add("T-1", "green", "python -m unittest tests.b", "OK", 0,
                  "2026-10-15T09:10:00+00:00")
        code, _, _ = run(["workbench-status", "--require-task", "T-1",
                          "--require-red-green-evidence"], self.runtime)
        self.assertNotEqual(code, 0, "不同命令不能形成失败到成功链")

    def test_wb09_invalid_order_or_stale_green(self):
        self.setUpLedger()
        run(["workbench-task-create", "--project-id", "P-1", "--task-id", "T-1",
             "--title", "顺序", "--spec-file", str(self.spec)], self.runtime)
        self._add("T-1", "green", "python -m unittest tests.a", "OK", 0,
                  "2026-10-15T09:00:00+00:00")
        self._add("T-1", "red", "python -m unittest tests.a", "FAILED", 1,
                  "2026-10-15T09:10:00+00:00")
        code, _, _ = run(["workbench-status", "--require-task", "T-1",
                          "--require-red-green-evidence"], self.runtime)
        self.assertNotEqual(code, 0, "绿灯在红灯之前，不能算完整")

    # ---------- 记录追加的失败语义 ----------
    def test_evidence_add_rejects_missing_timezone_and_empty_output(self):
        self.setUpLedger()
        run(["workbench-task-create", "--project-id", "P-1", "--task-id", "T-1",
             "--title", "记录", "--spec-file", str(self.spec)], self.runtime)
        f = self.base / "o.txt"; f.write_text("x", encoding="utf-8")
        code, _, _ = run(["workbench-evidence-add", "--task-id", "T-1", "--phase", "red",
                          "--command-text", "c", "--output-file", str(f),
                          "--returncode", "1", "--observed-at", "2026-10-15T09:00:00"],
                         self.runtime)
        self.assertNotEqual(code, 0, "时间缺时区必须失败")
        e = self.base / "e.txt"; e.write_text("", encoding="utf-8")
        code, _, _ = run(["workbench-evidence-add", "--task-id", "T-1", "--phase", "red",
                          "--command-text", "c", "--output-file", str(e),
                          "--returncode", "1",
                          "--observed-at", "2026-10-15T09:00:00+00:00"], self.runtime)
        self.assertNotEqual(code, 0, "输出为空必须失败")

    # ---------- WB-12 数据边界 ----------
    def test_wb12_no_flowerp_connection(self):
        run(["workbench-init", "--owner", "test-owner"], self.runtime)
        code, out, _ = run(["workbench-status"], self.runtime)
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertFalse(payload.get("flowerp_connected"),
                         "本讲不得连接 FlowERP 业务库")

    # ---------- 保留既有能力 ----------
    def test_existing_serve_workbench_still_available(self):
        proc = subprocess.run([*CLI, "--help"], cwd=str(ROOT),
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace")
        self.assertIn("serve-workbench", proc.stdout, "L00 的 serve-workbench 必须保留")


if __name__ == "__main__":
    unittest.main()
