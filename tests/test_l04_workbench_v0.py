"""L04 Ticket A：工作台 V0 的验收测试。

合同：`lesson-04-submission/WB-L04-BOOTSTRAP.md`

本测试要同时守住**两个方向**：
- 正常路径：有效输入能走通；
- 拒绝路径：**「执行退出码 0 但改动越界」必须判失败** ——
  防止实现退化成一律拒绝（那样正常路径也会挂）。

八项能力逐项对应：
① Spec 绑定 ② 任务创建 ③ 仅复验／允许写入 ④ 目录／写集／超时
⑤ 输出／退出码／Diff ⑥ 失败停止 ⑦ 最小 Eval／摘要 ⑧ 待人审
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


from workbench.execution import (  # noqa: E402
    ExecutionError,
    ExecutionLimits,
)
from workbench.spec import SpecError  # noqa: E402


def run_task(*args, **kwargs):
    """测试用包装：默认 `register_if_missing=True`，让用例专注于被测行为。

    ⚠ **生产默认不是这样** —— `workbench.cli execute-task` 默认**要求任务已存在**
    （与 L01「任务必须属于已登记项目」一致），只有显式 `--register-if-missing` 才自动登记。
    这条默认行为由 `test_v4_default_requires_registered_task` 单独覆盖。
    """
    from workbench.execution import run_task as _real
    kwargs.setdefault("register_if_missing", True)
    return _real(*args, **kwargs)


GOOD_SPEC = """# T

## 1. 来源

需求编号：TEST-1

## 2. 目标

目标。

## 3. 非目标

非目标。

## 4. 约束

约束。

## 5. 验收用例

A-1：能跑。

## 6. 完成定义

人审。
"""


class V0Tests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="l04-v0-")
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name).resolve()
        self.workdir = self.base / "candidate"
        self.workdir.mkdir()
        (self.workdir / "src").mkdir()
        (self.workdir / "src" / "app.py").write_text("x = 1\n", encoding="utf-8")
        self.spec = self.base / "SPEC.md"
        self.spec.write_text(GOOD_SPEC, encoding="utf-8")
        # v4：run_task 默认绑定 L01 账本，所以测试环境也要先建账本。
        self.runtime = self.base / "rt"
        from workbench import bootstrap as _bs
        _bs.workbench_init(self.runtime, "tester", "测试工作台")
        _bs.project_add(self.runtime, "P-TEST", "测试项目")

    def limits(self, **kw):
        defaults = dict(workdir=self.workdir, write_scope=("src/",), timeout=30.0)
        defaults.update(kw)
        return ExecutionLimits(**defaults)

    def py(self, code: str) -> list[str]:
        return [sys.executable, "-X", "utf8", "-c", code]

    # ---------- ① Spec 绑定 ----------
    def test_bad_spec_is_rejected_and_creates_no_task(self):
        bad = self.base / "BAD.md"
        bad.write_text("# 只有标题\n", encoding="utf-8")
        with self.assertRaises(ExecutionError) as ctx:
            run_task(bad, task_id="T-1", command=self.py("pass"),
                     limits=self.limits(), runtime=self.runtime)
        self.assertIn("Spec", str(ctx.exception))
        # v4：账本由 setUp 建好（run_task 默认绑定账本），
        # 所以这里断言的是「**不产生新任务**」，而不是「不建库」。
        from workbench import bootstrap as _bs
        status = _bs.workbench_status(self.runtime)
        self.assertNotIn("T-1", status["tasks"], "错误 Spec 不得创建任务")

    def test_good_spec_produces_task_and_evidence(self):
        result = run_task(self.spec, task_id="T-1",
                          command=self.py("import pathlib; pathlib.Path('src/app.py').write_text('x = 2\\n')"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertEqual(result.returncode, 0)
        self.assertIn("src/app.py", result.changed_files)

    # ---------- ③ 仅复验 ----------
    def test_verify_only_does_not_execute(self):
        marker = self.workdir / "should-not-exist.txt"
        result = run_task(self.spec, task_id="T-1",
                          command=self.py(f"import pathlib; pathlib.Path({str(marker)!r}).write_text('x')"),
                          limits=self.limits(), runtime=self.runtime,
                          verify_only=True)
        self.assertTrue(result.verify_only)
        self.assertFalse(marker.exists(), "仅复验不得执行命令")

    # ---------- ④ 目录／写集 / ⑥ 失败停止 ----------
    def test_out_of_scope_change_fails_even_with_zero_exit(self):
        """★ 关键：退出码 0，但改了写集外的文件 → 必须判失败。"""
        result = run_task(self.spec, task_id="T-1",
                          command=self.py(
                              "import pathlib;"
                              "pathlib.Path('src/app.py').write_text('x = 3\\n');"
                              "pathlib.Path('OUTSIDE.txt').write_text('越界')"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertEqual(result.returncode, 0, "命令本身是成功的")
        self.assertIn("OUTSIDE.txt", result.out_of_scope)
        self.assertTrue(result.stopped, "越界必须停止")
        self.assertFalse(result.accepted, "越界不得被接受")

    def test_change_outside_workdir_is_detected(self):
        outside = self.base / "elsewhere.txt"
        result = run_task(self.spec, task_id="T-1",
                          command=self.py(f"import pathlib; pathlib.Path({str(outside)!r}).write_text('x')"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped, "写工作目录之外必须被发现")

    def test_nonzero_exit_is_not_success(self):
        result = run_task(self.spec, task_id="T-1",
                          command=self.py("import sys; sys.exit(3)"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertEqual(result.returncode, 3)
        self.assertFalse(result.accepted)
        self.assertIn("退出码", result.stop_reason)

    def test_timeout_stops_and_is_not_success(self):
        result = run_task(self.spec, task_id="T-1",
                          command=self.py("import time; time.sleep(30)"),
                          limits=self.limits(timeout=1.0), runtime=self.runtime)
        self.assertTrue(result.timed_out)
        self.assertFalse(result.accepted)
        self.assertIn("超时", result.stop_reason)

    def test_cli_subcommand_name_survives_option_values(self):
        """回归：--command 的 dest 曾与 subparsers 的 dest="command" 撞名，
        导致 args.command 被命令字符串覆盖，CLI 静默退 2 且无输出。"""
        from workbench.cli import build_parser
        args = build_parser().parse_args(
            ["execute-task", "--spec", "S.md", "--task-id", "T",
             "--command", "true", "--workdir", ".", "--write-scope", "."])
        self.assertEqual(args.command, "execute-task",
                         "子命令名不得被 --command 的值覆盖")
        self.assertEqual(args.command_text, "true")

    def test_missing_command_is_controlled_failure(self):
        """回归：命令不存在时曾抛未捕获的 FileNotFoundError（表现为 CLI 静默退出 2）。

        正确行为是**受控失败**：returncode=127、留下证据、不写成成功。
        """
        result = run_task(self.spec, task_id="T-1",
                          command=["this-command-does-not-exist-xyz"],
                          limits=self.limits(), runtime=self.runtime)
        self.assertEqual(result.returncode, 127)
        self.assertTrue(result.stopped)
        self.assertFalse(result.accepted)
        self.assertIn("无法启动", result.stderr)
        self.assertTrue(Path(result.evidence_path).exists(), "失败也必须留证据")

    # ---------- 独立复验指出的 4 个反例（回归）----------
    def test_scope_uses_path_component_boundary(self):
        """反例 2：裸 startswith 会把 `src_evil/x` 判成写集 `src` 之内。"""
        limits = self.limits()          # write_scope=("src/",)
        self.assertTrue(limits.in_scope("src/app.py"))
        self.assertFalse(limits.in_scope("src_evil/x.txt"),
                         "分量边界：src_evil 不属于 src")

    def test_blank_write_scope_element_is_rejected(self):
        """反例 3：空写集元素让 startswith("") 恒真，检查静默失效。"""
        with self.assertRaises(ExecutionError) as ctx:
            self.limits(write_scope=("",))
        self.assertIn("空元素", str(ctx.exception))

    def test_absolute_or_parent_escape_scope_is_rejected(self):
        """写集不得是绝对路径或含 ..（否则可以逃出写集）。"""
        for bad in (("/tmp",), ("../outside",)):
            with self.subTest(scope=bad):
                with self.assertRaises(ExecutionError):
                    self.limits(write_scope=bad)
        limits = self.limits()
        self.assertFalse(limits.in_scope("../escape.txt"))
        self.assertFalse(limits.in_scope("/etc/passwd"))

    def test_evidence_records_stdout_stderr_diff_and_verify_command(self):
        """A-1：输出曾被采集后丢弃；diff_summary 与验证命令曾未落盘。"""
        marker = "MARKER-ONLY-IN-OUTPUT-42"
        result = run_task(self.spec, task_id="T-1",
                          command=self.py(f"print({marker!r})"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertIn(marker, result.stdout, "stdout 必须保留")
        data = result.as_dict()
        for key in ("stdout", "stderr", "diff_summary", "verify_command", "watch_roots"):
            self.assertIn(key, data, f"证据必须含 {key}")
        self.assertIn("execute-task", data["verify_command"], "必须给出可重跑的验证命令")
        # 落盘的那份也要有
        import json as _json
        on_disk = _json.loads(Path(result.evidence_path).read_text(encoding="utf-8"))
        self.assertIn(marker, on_disk.get("stdout", ""), "落盘证据同样要含 stdout")

    def test_watch_roots_are_recorded_so_blind_spots_are_visible(self):
        """反例 1：监视不到的地方要**可见**，而不是默认假成功。"""
        result = run_task(self.spec, task_id="T-1", command=self.py("pass"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.watch_roots, "必须记录实际监视根，让盲区可见")

    def test_acceptance_field_cannot_be_turned_into_accepted_by_construction(self):
        """A-4 补充：钉住 acceptance 不可被调用方构造改写成已接受。"""
        from workbench.execution import ExecutionResult
        import inspect as _inspect
        # accepted 是只读 property，赋值必须失败
        r = run_task(self.spec, task_id="T-1", command=self.py("pass"),
                     limits=self.limits(), runtime=self.runtime)
        with self.assertRaises(AttributeError):
            r.accepted = True
        # as_dict / 落盘都必须是常量
        self.assertEqual(r.as_dict()["acceptance"], "pending_human_review")
        self.assertFalse(r.as_dict()["accepted"])

    # ---------- 二次复验（round 2）指出的 7 个 bug 的回归 ----------
    def test_fix4_evidence_files_are_never_overwritten(self):
        """修 4：同 task-id 先失败、后成功，两次的证据文件都必须存在。"""
        run_task(self.spec, task_id="SAME", command=self.py("import sys; sys.exit(3)"),
                 limits=self.limits(), runtime=self.runtime)
        run_task(self.spec, task_id="SAME", command=self.py("import pathlib; pathlib.Path('src/app.py').write_text('y')"),
                 limits=self.limits(), runtime=self.runtime)
        files = sorted(Path(self.base / "rt" / "evidence").glob("SAME-*-execution.json"))
        self.assertEqual(len(files), 2, f"两次运行的证据都要留下，实际 {[f.name for f in files]}")
        import json as _json
        rcs = sorted(_json.loads(f.read_text(encoding="utf-8"))["returncode"] for f in files)
        self.assertEqual(rcs, [0, 3], "失败的 rc=3 必须仍然可查")

    def test_fix7_evidence_directory_outside_write_scope_required(self):
        """修 7：证据目录落在写集内必须被拒绝（否则能删改自己的证据）。"""
        rt = self.workdir / "rt"          # 故意放进工作目录，且写集覆盖它
        with self.assertRaises(ExecutionError) as ctx:
            run_task(self.spec, task_id="T-1", command=self.py("pass"),
                     limits=self.limits(write_scope=("rt/",)),
                     runtime=rt)
        self.assertIn("证据目录落在写集内", str(ctx.exception))

    def test_fix7_deleting_previous_evidence_is_detected(self):
        """修 7：本次运行删掉既有证据 → 判失败（run5 的攻击步 2）。"""
        rt = self.base / "rt"
        run_task(self.spec, task_id="V1", command=self.py("import sys; sys.exit(3)"),
                 limits=self.limits(), runtime=rt)
        victim = sorted((rt / "evidence").glob("V1-*-execution.json"))[0]
        result = run_task(self.spec, task_id="V2", command=self.py(
            f"import pathlib; pathlib.Path({str(victim)!r}).unlink()"),
            limits=self.limits(), runtime=rt)
        self.assertTrue(result.stopped, "删除既有证据必须被发现")
        # 纵深防御：可能是「越界」先抓到，也可能是「证据被删除」抓到，两者都算拦住
        self.assertTrue("既有证据被删除" in result.stop_reason
                        or "写集外" in result.stop_reason,
                        f"必须被拦下，实际理由：{result.stop_reason}")

    def test_fix7_rewriting_previous_evidence_is_detected(self):
        """修 7：本次运行改写既有证据 → 判失败（run5 的攻击步 3）。"""
        rt = self.base / "rt"
        run_task(self.spec, task_id="W1", command=self.py("pass"),
                 limits=self.limits(), runtime=rt)
        victim = sorted((rt / "evidence").glob("W1-*-execution.json"))[0]
        result = run_task(self.spec, task_id="W2", command=self.py(
            f"import json,pathlib; p=pathlib.Path({str(victim)!r});"
            f"d=json.loads(p.read_text()); d['returncode']=0; d['stopped']=False;"
            f"p.write_text(json.dumps(d))"),
            limits=self.limits(), runtime=rt)
        self.assertTrue(result.stopped, "改写既有证据必须被发现")
        self.assertTrue("既有证据被改写" in result.stop_reason
                        or "写集外" in result.stop_reason,
                        f"必须被拦下，实际理由：{result.stop_reason}")

    def test_fix5_ignored_directories_are_no_longer_blind(self):
        """修 5：.git/.runtime/__pycache__ 里的改动也必须被看见。"""
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import pathlib;"
            "pathlib.Path('src/app.py').write_text('z');"
            "pathlib.Path('.git').mkdir(exist_ok=True);"
            "pathlib.Path('.git/config').write_text('x')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertIn(".git/config", result.changed_files, "忽略目录不再是盲区")
        self.assertIn(".git/config", result.out_of_scope)
        self.assertTrue(result.stopped)

    def test_fix6a_unused_symlink_does_not_fail_the_task(self):
        """修 6 第二次修订：目录里**存在**指向根外的链接，但命令没碰它 → 不该失败。

        复验指出原实现「只要存在就判失败」，含 `node_modules/.bin` 的仓库会永远无法通过。
        """
        far = Path(tempfile.mkdtemp(prefix="l04-far2-")) / "t.txt"
        self.addCleanup(shutil.rmtree, far.parent, ignore_errors=True)
        far.write_text("ORIG", encoding="utf-8")
        (self.workdir / "src" / "unused_link.txt").symlink_to(far)
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('ok')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertFalse(result.stopped,
                         f"未被使用的根外链接不该判失败：{result.stop_reason}")
        self.assertEqual(far.read_text(encoding="utf-8"), "ORIG", "链接目标不该被动过")

    def test_fix6b_used_symlink_escape_is_detected(self):
        """修 6：**通过链接**写到监视根之外 → 必须被报出。"""
        far_dir = Path(tempfile.mkdtemp(prefix="l04-far3-"))
        self.addCleanup(shutil.rmtree, far_dir, ignore_errors=True)
        far = far_dir / "t.txt"
        far.write_text("ORIG", encoding="utf-8")
        (self.workdir / "src" / "link.txt").symlink_to(far)
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import pathlib; pathlib.Path('src/link.txt').write_text('EVIL')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertEqual(far.read_text(encoding="utf-8"), "EVIL", "攻击真的发生了（作为对照前提）")
        self.assertTrue(any("symlink:src/link.txt" in x for x in result.out_of_scope),
                        f"被使用的逃逸链接必须报出，实得 {result.out_of_scope}")
        self.assertTrue(result.stopped)

    def test_fix2_metadata_change_is_detected(self):
        """修 2：内容不变但权限/mtime 变了，也算改动。"""
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import pathlib,os; p=pathlib.Path('src/app.py'); os.chmod(p,0o600); os.utime(p,(1,1))"),
            limits=self.limits(), runtime=self.runtime)
        self.assertIn("src/app.py", result.changed_files, "元数据变化也算改动")

    def test_fix1_verify_command_quotes_each_argument(self):
        """修 1：含空格的参数在 verify_command 里必须保持成单个参数。"""
        import shlex as _shlex
        tricky = 'import pathlib; pathlib.Path("src/app.py").write_text("x = 1")'
        result = run_task(self.spec, task_id="T-1",
                          command=["/usr/bin/python3", "-c", tricky],
                          limits=self.limits(), runtime=self.runtime)
        cmd = result.verify_command
        self.assertIn("-c", cmd)
        # 取出 --command 后面的那一段，做 shlex.split 再 shlex.split 两次应还原
        idx = cmd.index("--command") + len("--command")
        rest = cmd[idx:].strip()
        outer = _shlex.split(rest)[0]        # 交给 CLI 的那个字符串
        inner = _shlex.split(outer)          # CLI 内部再切一次
        self.assertEqual(inner, ["/usr/bin/python3", "-c", tricky],
                         f"含空格参数必须忠实还原，实得 {inner}")

    def test_fix5b_in_scope_pycache_is_allowed(self):
        """写集**内**的 `__pycache__` 放行（那是解释器必然副产物）。

        ⚠ 写集**外**的 `__pycache__`/`.pyc` **一律不放行** ——
        第三次复验证明，把它们做成白名单等于「写集外任意写删判成功」。
        """
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('ok');"
            "d=pathlib.Path('src/__pycache__'); d.mkdir(parents=True, exist_ok=True);"
            "(d/'m.cpython-311.pyc').write_bytes(b'P')"),
            limits=self.limits(), runtime=self.runtime)     # 写集含 src/
        self.assertFalse(result.stopped, f"写集内的副产物不该判失败：{result.stop_reason}")
        self.assertTrue(result.eval_ok, result.eval_message)

    def test_fix5c_ignored_directories_still_reported(self):
        """修 5 的本体不能因为上面的放行而退化：.git 等仍必须报越界。"""
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import pathlib;"
            "pathlib.Path('.git').mkdir(exist_ok=True);"
            "pathlib.Path('.git/config').write_text('x')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped)
        self.assertIn(".git/config", result.out_of_scope)

    # ---------- v4：绑定 L01 账本 ----------
    def test_v4_default_requires_registered_task(self):
        """v4 默认：任务未登记 → 拒绝执行（与 L01「任务必须属于已登记项目」一致）。"""
        from workbench.execution import run_task as real_run_task
        with self.assertRaises(ExecutionError) as ctx:
            real_run_task(self.spec, task_id="NOT-REGISTERED",
                          command=self.py("pass"), limits=self.limits(),
                          runtime=self.runtime)          # 不传 register_if_missing
        self.assertIn("任务未登记", str(ctx.exception))

    def test_v4_registered_task_gets_ledger_evidence(self):
        """v4：已登记任务的执行会**追加**进 L01 账本，并给出 evidence_id。"""
        from workbench import bootstrap as _bs
        _bs.task_create(self.runtime, "P-TEST", "T-LEDGER",
                        title="账本绑定", spec_file=str(self.spec))
        result = run_task(self.spec, task_id="T-LEDGER",
                          command=self.py("import pathlib; pathlib.Path('src/app.py').write_text('led')"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertIsNotNone(result.ledger_evidence_id, "应返回账本里的 evidence_id")
        status = _bs.workbench_status(self.runtime, require_task="T-LEDGER")
        self.assertTrue(status["evidence"].get("T-LEDGER"), "账本里应能查到该任务的运行记录")

    def test_v4_failure_also_goes_into_ledger(self):
        """v4：**失败也要进账本** —— 「不删除失败输出」在执行层面同样成立。"""
        from workbench import bootstrap as _bs
        _bs.task_create(self.runtime, "P-TEST", "T-FAIL-LEDGER",
                        title="失败也入账", spec_file=str(self.spec))
        result = run_task(self.spec, task_id="T-FAIL-LEDGER",
                          command=self.py("import sys; sys.exit(4)"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped)
        self.assertIsNotNone(result.ledger_evidence_id)
        status = _bs.workbench_status(self.runtime, require_task="T-FAIL-LEDGER")
        rows = status["evidence"]["T-FAIL-LEDGER"]
        self.assertTrue(any(r["returncode"] == 4 for r in rows),
                        f"失败记录必须能查回，实得 {[r['returncode'] for r in rows]}")

    # ---------- 第三次复验的 5 条要求 ----------
    def test_rev3_pycache_whitelist_does_not_allow_out_of_scope_writes(self):
        """第三次复验的核心判据：写集外任何路径都不能借 __pycache__/.pyc 之名放行。"""
        cases = ["docs/__pycache__/payload.pyc", "docs/__pycache__/payload.txt",
                 "docs/totally-unrelated.pyc", "docs/deep/deeper/__pycache__/x.pyc"]
        for target in cases:
            with self.subTest(target=target):
                result = run_task(self.spec, task_id="T-1", command=self.py(
                    f"import pathlib; pathlib.Path('src/app.py').write_text('ok');"
                    f"p=pathlib.Path({target!r}); p.parent.mkdir(parents=True, exist_ok=True);"
                    f"p.write_bytes(b'x')"),
                    limits=self.limits(), runtime=self.runtime)
                self.assertTrue(result.stopped, f"{target} 必须判越界")
                self.assertIn(target, result.out_of_scope)

    def test_rev3_deleting_out_of_scope_pyc_is_detected(self):
        """删除写集外的 pyc 也必须被发现。"""
        victim = self.workdir / "docs" / "__pycache__" / "pre.cpython-311.pyc"
        victim.parent.mkdir(parents=True, exist_ok=True)
        victim.write_bytes(b"x")
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('ok');"
            f"pathlib.Path({str(victim)!r}).unlink()"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped, "删除写集外的 pyc 必须判越界")

    def test_rev3_verify_only_evidence_names_are_unique(self):
        """修 4 只修了一半：verify_only 的证据名也曾固定，会被互相覆盖。"""
        for i in range(3):
            run_task(self.spec, task_id="VO", command=self.py("pass"),
                     limits=self.limits(), runtime=self.runtime, verify_only=True)
        files = sorted((self.runtime / "evidence").glob("VO-*-verify-only.json"))
        self.assertEqual(len(files), 3, f"三次 verify_only 的证据都要在，实得 {[f.name for f in files]}")

    def test_rev3_verify_command_note_is_recorded(self):
        """修 3「说了没做」：说明必须落进证据 JSON，而不只在文档里。"""
        result = run_task(self.spec, task_id="T-1", command=self.py("pass"),
                          limits=self.limits(), runtime=self.runtime)
        data = result.as_dict()
        self.assertIn("verify_command_note", data)
        self.assertIn("干净副本", data["verify_command_note"])

    def test_rev3_deleting_whole_workdir_is_detected(self):
        """N-3：把整个工作目录删掉曾经判成功。"""
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import shutil, pathlib; shutil.rmtree(pathlib.Path('.').resolve())"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped, "工作目录被删必须判失败")
        self.assertIn("工作目录", result.stop_reason)

    # ---------- 第五轮复验的 R 组回归 ----------
    def test_r1_unreadable_directory_fails_closed(self):
        """R-1：不可读目录 ⇒ 内容不可知 ⇒ 拒绝执行（不能假装它没变化）。"""
        import os
        secret = self.workdir / "secret"
        secret.mkdir(exist_ok=True)
        (secret / "k.txt").write_text("old", encoding="utf-8")
        os.chmod(secret, 0o000)
        self.addCleanup(os.chmod, secret, 0o755)
        with self.assertRaises(ExecutionError) as ctx:
            run_task(self.spec, task_id="R1", command=self.py("pass"),
                     limits=self.limits(), runtime=self.runtime)
        self.assertIn("不可读", str(ctx.exception))

    def test_r1_readable_directory_still_works(self):
        """对照：可读目录不受影响。"""
        (self.workdir / "secret").mkdir(exist_ok=True)
        (self.workdir / "secret" / "k.txt").write_text("o", encoding="utf-8")
        result = run_task(self.spec, task_id="R1C", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('ok')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertFalse(result.stopped, result.stop_reason)

    def test_r2_ledger_append_failure_is_a_failure(self):
        """R-2a：账本追加失败 ⇒ 判失败（不再静默吞掉）。"""
        import sqlite3
        result = run_task(self.spec, task_id="R2", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('1')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.eval_ok)
        conn = sqlite3.connect(str(self.runtime / "workbench.db"))
        conn.execute("DELETE FROM workbench")     # 让后续追加干净失败
        conn.commit(); conn.close()
        result2 = run_task(self.spec, task_id="R2", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('2')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result2.stopped, "追加失败必须判失败")
        self.assertIn("账本追加失败", result2.stop_reason)

    def test_r2_eval_binds_to_this_run_not_previous(self):
        """R-2b：Eval 必须绑定**本次** ✗ 不能引用上一轮的证据。"""
        run_task(self.spec, task_id="R2B", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('one')"),
            limits=self.limits(), runtime=self.runtime)
        # 第二轮零改动 → 必须报「没有可核对的改动」✗ 而不是拿上一轮说通过
        result = run_task(self.spec, task_id="R2B", command=self.py("pass"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertFalse(result.eval_ok, "零改动不得通过")
        self.assertIn("没有产生可核对的改动", result.eval_message)

    def test_r4_directory_symlink_escape_is_detected(self):
        """R-4：**目录**符号链接写穿透 → 必须判失败（文件链接那套判据对它无效）。"""
        far = Path(tempfile.mkdtemp(prefix="l04-r4-"))
        self.addCleanup(shutil.rmtree, far, ignore_errors=True)
        (self.workdir / "link").symlink_to(far, target_is_directory=True)
        result = run_task(self.spec, task_id="R4", command=self.py(
            "import pathlib;"
            "pathlib.Path('src/app.py').write_text('ok');"
            "pathlib.Path('link/evil.txt').write_text('PWNED')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertEqual((far / "evil.txt").read_text(encoding="utf-8"), "PWNED",
                         "攻击真的发生了（作为对照前提）")
        self.assertTrue(result.stopped, "目录链接写穿透必须判失败")

    def test_r4_unused_file_symlink_still_passes(self):
        """对照：未被使用的文件链接仍放行（复验者批过的假阳性不能回来）。"""
        far = Path(tempfile.mkdtemp(prefix="l04-r4c-"))
        self.addCleanup(shutil.rmtree, far, ignore_errors=True)
        (far / "t.txt").write_text("ORIG", encoding="utf-8")
        (self.workdir / "unused.txt").symlink_to(far / "t.txt")
        result = run_task(self.spec, task_id="R4C", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('ok')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertFalse(result.stopped, f"未使用的链接不该判失败：{result.stop_reason}")

    # ---------- 第六轮复验的 D 组回归 ----------
    def test_d1_paths_starting_with_angle_bracket_are_visible(self):
        """D-1：**合成键不得按名字形状过滤真实路径** —— `other/<pwn>.txt` 必须可见。"""
        (self.workdir / "other").mkdir(exist_ok=True)
        cases = ["other/<pwn>.txt", "other/deep/<pwn>.txt", "other/<evil-dir>/payload.txt"]
        for target in cases:
            with self.subTest(target=target):
                result = run_task(self.spec, task_id="T-1", command=self.py(
                    f"import pathlib; pathlib.Path('src/app.py').write_text('ok');"
                    f"p=pathlib.Path({target!r}); p.parent.mkdir(parents=True, exist_ok=True);"
                    f"p.write_text('PWNED')"),
                    limits=self.limits(), runtime=self.runtime)
                self.assertTrue(result.stopped, f"{target} 必须判越界")
                self.assertIn(target, result.out_of_scope)

    def test_d1_deleting_angle_bracket_file_is_detected(self):
        """D-1 变体：**删除**写集外的 `other/<victim>.txt` 也必须可见。"""
        (self.workdir / "other").mkdir(exist_ok=True)
        victim = self.workdir / "other" / "<victim>.txt"
        victim.write_text("v", encoding="utf-8")
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('ok');"
            f"pathlib.Path({str(victim)!r}).unlink()"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped)
        self.assertIn("other/<victim>.txt", result.out_of_scope)

    def test_d2_unreadable_file_fingerprint_has_mode_and_mtime(self):
        """D-2：不可读**文件**的指纹必须含 mode/mtime ✗ 不能是裸常量。"""
        import os
        target = self.workdir / "other"
        target.mkdir(exist_ok=True)
        locked = target / "locked.txt"
        locked.write_text("SECRET-ORIGINAL\n", encoding="utf-8")
        os.chmod(locked, 0o000)
        self.addCleanup(os.chmod, locked, 0o644)
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import os, pathlib; pathlib.Path('src/app.py').write_text('ok');"
            "p=pathlib.Path('other/locked.txt');"
            "os.chmod(p,0o600); p.write_text(p.read_text()+'PWNED-APPEND'); os.chmod(p,0o000)"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped, "改权限写入再改回必须被发现")
        self.assertIn("other/locked.txt", result.out_of_scope)

    def test_d3_watch_root_blind_spots_are_checked(self):
        """D-3：盲区检查必须覆盖**每一个监视根** ✗ 不只工作目录。"""
        import os
        outside = self.base / "secrets"
        outside.mkdir(exist_ok=True)
        os.chmod(outside, 0o000)
        self.addCleanup(os.chmod, outside, 0o755)
        with self.assertRaises(ExecutionError) as ctx:
            run_task(self.spec, task_id="T-1", command=self.py("pass"),
                     limits=self.limits(), runtime=self.runtime)
        self.assertIn("不可读", str(ctx.exception))

    def test_d4_watch_root_symlink_does_not_fail_the_task(self):
        """D-4：监视根里**未被使用**的链接不得让本次失败（否则 runtime 被永久毒化）。"""
        far = Path(tempfile.mkdtemp(prefix="l04-d4-"))
        self.addCleanup(shutil.rmtree, far, ignore_errors=True)
        old_cand = self.base / "candidates" / "T-OLD-xyz"
        old_cand.mkdir(parents=True, exist_ok=True)
        (old_cand / "node_modules_bin_link").symlink_to(far / "nowhere")
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('ok')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertFalse(result.stopped,
                         f"监视根里未被使用的链接不该判失败：{result.stop_reason}")
        # 但仍要**可见**
        self.assertTrue(any("watch-symlink" in k for k in result.diff_summary),
                        "监视根里的链接仍应记进证据（可见）")

    def test_d5_ledger_append_only_is_enforced(self):
        """D-5：删账本记录必须被发现（append-only 断言）。"""
        import sqlite3
        run_task(self.spec, task_id="T-1", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('1')"),
            limits=self.limits(), runtime=self.runtime)
        db = self.runtime / "workbench.db"
        result = run_task(self.spec, task_id="T-1", command=self.py(
            "import sqlite3, pathlib;"
            f"c=sqlite3.connect({str(db)!r});"
            "c.execute('DELETE FROM evidence'); c.commit(); c.close();"
            "pathlib.Path('src/app.py').write_text('2')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped, "删账本记录必须判失败")

    def test_d6_pexec_project_only_created_when_registered(self):
        """D-6：不传 `register_if_missing` 时**不得**新建 `P-EXEC` 项目。"""
        import sqlite3
        from workbench import bootstrap as _bs
        _bs.project_add(self.runtime, "P-REV", "复验项目")
        _bs.task_create(self.runtime, "P-REV", "D6T", title="t", spec_file=str(self.spec))
        conn = sqlite3.connect(str(self.runtime / "workbench.db"))
        before = sorted(r[0] for r in conn.execute("SELECT project_id FROM projects"))
        conn.close()
        run_task(self.spec, task_id="D6T", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('ok')"),
            limits=self.limits(), runtime=self.runtime, register_if_missing=False)
        conn = sqlite3.connect(str(self.runtime / "workbench.db"))
        after = sorted(r[0] for r in conn.execute("SELECT project_id FROM projects"))
        conn.close()
        self.assertEqual(before, after, f"不该新建项目：{before} → {after}")

    # ---------- 第六轮留下的缺口：course-submit 真的跑一遍 ----------
    def test_cs_customer_root_is_watched(self):
        """复验者第 4 轮的 ⑤：**源客户仓库必须被监视**。

        它当时报「写了源仓库仍 `writeback: false` + rc=0」✗
        第六轮复验**无法验证**（它被禁止读参考仓库 ✗ 跑不了 `course-submit`）✓
        我这边实测复现了：`out_of_scope=[]` ✗ `stopped=False` ✗ 而源文件真被写 ✓
        """
        from workbench.candidate import run_ticket
        from workbench import bootstrap as _bs
        _bs.task_create(self.runtime, "P-TEST", "CS1", title="cs", spec_file=str(self.spec))
        cust = self.base / "cust"
        (cust / "flowerp").mkdir(parents=True)
        (cust / "flowerp" / "service.py").write_text("# c\n", encoding="utf-8")
        # 客户仓库需要 .venv（course-submit 会检查）
        (cust / ".venv" / "bin").mkdir(parents=True)
        (cust / ".venv" / "bin" / "python").symlink_to(sys.executable)

        payload = run_ticket(cust, self.runtime, spec_path=self.spec, task_id="CS1",
                             command=["/bin/sh", "-c",
                                      f"printf BACKDOOR > {cust}/flowerp/backdoored.py"],
                             write_scope=("flowerp",))
        self.assertTrue(payload["candidate"]["writeback"],
                        "**观察到的** writeback 必须为 True")
        self.assertTrue(payload["stopped"], "写源仓库必须判失败")
        self.assertIn("写回", payload["stop_reason"])
        self.assertTrue(any("backdoored.py" in x for x in payload["out_of_scope"]))

    def test_cs_normal_run_has_writeback_false(self):
        """对照：只改候选里的文件 → `writeback` 为 False（**观察出来的** ✗ 不是写死的）。"""
        from workbench.candidate import run_ticket
        from workbench import bootstrap as _bs
        _bs.task_create(self.runtime, "P-TEST", "CS2", title="cs", spec_file=str(self.spec))
        cust = self.base / "cust2"
        (cust / "flowerp").mkdir(parents=True)
        (cust / "flowerp" / "service.py").write_text("# c\n", encoding="utf-8")
        (cust / ".venv" / "bin").mkdir(parents=True)
        (cust / ".venv" / "bin" / "python").symlink_to(sys.executable)

        payload = run_ticket(cust, self.runtime, spec_path=self.spec, task_id="CS2",
                             command=["/bin/sh", "-c", "printf hi > flowerp/out.txt"],
                             write_scope=("flowerp",))
        self.assertFalse(payload["candidate"]["writeback"])
        self.assertIn("未发生写回", payload["candidate"]["writeback_note"])
        self.assertFalse(payload["stopped"], payload["stop_reason"])

    # ---------- 第七轮复验的 F 组回归 ----------
    def test_f3_fifo_does_not_hang_the_snapshot(self):
        """F3：**非普通文件不得读内容** —— FIFO 曾让 CLI 永久挂死。"""
        result = run_task(self.spec, task_id="F3", command=self.py(
            "import os, pathlib; pathlib.Path('src/app.py').write_text('y'); os.mkfifo('p')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped, "建 FIFO 必须判越界（而不是挂死）")
        self.assertIn("p", result.out_of_scope)

    def test_f3_preexisting_fifo_does_not_hang(self):
        """F3 变体：预先存在的 FIFO 曾让 `before` 快照就阻塞。"""
        import os
        os.mkfifo(self.workdir / "pre.fifo")
        result = run_task(self.spec, task_id="F3B", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('z')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertFalse(result.stopped, f"预置 FIFO 不该让本次失败：{result.stop_reason}")

    def test_f2_unreadable_file_fingerprint_uses_ctime(self):
        """F2：指纹必须含**同 UID 无法复原**的字段（`ctime`）✗
        否则「chmod 600 → 改 → chmod 000 → utime(原值)」能让指纹相同。"""
        import os
        target = self.workdir / "other"
        target.mkdir(exist_ok=True)
        locked = target / "locked.txt"
        locked.write_text("SECRET-ORIGINAL\n", encoding="utf-8")
        os.chmod(locked, 0o000)
        self.addCleanup(os.chmod, locked, 0o644)
        st = locked.stat()
        result = run_task(self.spec, task_id="F2", command=self.py(
            "import os, pathlib; pathlib.Path('src/app.py').write_text('ok');"
            "p=pathlib.Path('other/locked.txt');"
            f"os.utime(p, ns=({st.st_atime_ns}, {st.st_mtime_ns}));"
            "os.chmod(p, 0o600); f=open(p,'a'); f.write('ROTATED'); f.close();"
            "os.chmod(p, 0o000)"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped, "改不可读文件的内容必须被发现")
        self.assertIn("other/locked.txt", result.out_of_scope)

    def test_f1_ledger_sampling_happens_before_the_command(self):
        """F1：账本计数必须在**命令之前**取 ✗ 否则命令清空账本看不见。"""
        import inspect as _inspect
        from workbench import execution as _ex
        src = _inspect.getsource(_ex.run_task)
        i_before = src.find("ledger_before = _ledger_counts")
        i_cmd = src.find("proc = subprocess.run")
        self.assertGreater(i_before, -1, "找不到取样")
        self.assertLess(i_before, i_cmd, "**取样必须在命令之前**")

    def test_f1_clearing_ledger_is_detected(self):
        """F1：命令清空账本 → 必须判失败（append-only）。"""
        run_task(self.spec, task_id="F1", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('1')"),
            limits=self.limits(), runtime=self.runtime)
        db = self.runtime / "workbench.db"
        result = run_task(self.spec, task_id="F1", command=self.py(
            "import sqlite3, pathlib;"
            f"c=sqlite3.connect({str(db)!r}); c.execute('DELETE FROM evidence');"
            "c.commit(); c.close();"
            "pathlib.Path('src/app.py').write_text('2')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped, "清空账本必须判失败")

    def test_f4_illegal_utf8_filename_does_not_crash(self):
        """F4：非法 UTF-8 文件名曾让写证据抛 `UnicodeEncodeError` ✗ 留 0 字节证据。"""
        result = run_task(self.spec, task_id="F4", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('ok');"
            "p = pathlib.Path(b'other/\xff\xfe-pwn.txt');"
            "p.parent.mkdir(exist_ok=True); p.write_bytes(b'x')"),
            limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.stopped, "非法 UTF-8 名字的越界写入必须判失败")
        # 而且证据必须**完整落盘**（>0 字节）
        self.assertTrue(Path(result.evidence_path).stat().st_size > 0,
                        "证据不能是 0 字节")

    def test_f5_deleting_evidence_dir_is_controlled_failure(self):
        """F5：命令删掉证据目录 → 受控失败 ✗ 不是未捕获的 `OSError`。"""
        rt = self.runtime
        run_task(self.spec, task_id="F5", command=self.py(
            "import pathlib; pathlib.Path('src/app.py').write_text('1')"),
            limits=self.limits(), runtime=rt)
        result = run_task(self.spec, task_id="F5", command=self.py(
            f"import shutil, pathlib; shutil.rmtree({str(rt / 'evidence')!r}, ignore_errors=True);"
            "pathlib.Path('src/app.py').write_text('2')"),
            limits=self.limits(), runtime=rt)
        self.assertTrue(result.stopped, "删证据目录必须判失败")
        self.assertTrue(Path(result.evidence_path).is_file(), "本次证据仍要落盘")

    # ---------- ⑦ 最小 Eval ----------
    def test_minimum_eval_failure_blocks(self):
        from eval.harness import minimum_eval
        ok, message = minimum_eval(self.base / "rt", expect_task="T-1")
        self.assertFalse(ok)
        self.assertIn("T-1", message)

    def test_minimum_eval_passes_after_real_run(self):
        """回归：Eval 曾在证据落盘之前运行，导致正常路径也报「找不到证据」。"""
        from eval.harness import minimum_eval
        result = run_task(self.spec, task_id="T-1",
                          command=self.py("import pathlib; pathlib.Path('src/app.py').write_text('x = 9\\n')"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertTrue(result.eval_ok, result.eval_message)
        self.assertFalse(result.stopped)
        self.assertTrue(result.evidence_complete, "正常路径应是 evidence_complete")
        ok, message = minimum_eval(self.base / "rt", expect_task="T-1")
        self.assertTrue(ok, message)

    # ---------- ⑧ 待人审 ----------
    def test_success_still_waits_for_human_review(self):
        result = run_task(self.spec, task_id="T-1",
                          command=self.py("import pathlib; pathlib.Path('src/app.py').write_text('x = 4\\n')"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertEqual(result.acceptance, "pending_human_review")
        self.assertFalse(result.accepted, "程序永远不能替人签字")

    # ---------- ⑤ Diff 与证据 ----------
    def test_diff_and_evidence_are_recorded(self):
        result = run_task(self.spec, task_id="T-1",
                          command=self.py("import pathlib; pathlib.Path('src/app.py').write_text('x = 5\\n')"),
                          limits=self.limits(), runtime=self.runtime)
        self.assertIn("src/app.py", result.diff_summary)
        self.assertTrue(result.evidence_path and Path(result.evidence_path).exists(),
                        "执行证据必须落盘")

    def test_as_dict_has_all_eight_fields(self):
        result = run_task(self.spec, task_id="T-1",
                          command=self.py("pass"),
                          limits=self.limits(), runtime=self.runtime)
        data = result.as_dict()
        for key in ("task_id", "returncode", "changed_files", "out_of_scope",
                    "timed_out", "stopped", "evidence_complete", "acceptance"):
            self.assertIn(key, data)


if __name__ == "__main__":
    unittest.main()
