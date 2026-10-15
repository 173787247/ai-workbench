"""L04 Ticket A · 最小 Eval Harness：登记 ✗ 逐项运行 ✗ 分级汇总 ✗ 报告与出口码。

⭐ 为什么要它（**L04 独立复验者指出**）：
  合同「验收用例」第一条写着「正常任务能保存调用 ✗ 输出 ✗ 退出码 ✗ Diff 和**验证命令**」，
  而当时 **`eval/` 目录只有 `__init__.py`** ⇒ 那半句**零实现**。
  本模块补上它。

⭐ 职责边界（**L06 会专门建设**：统一分级与报告）：
  · 本讲只做**最小**版本：登记用例 → 逐项跑 → 按等级汇总 → 写报告与退出码。
  · ⚠️ **不实现自动返工 ✗ 不实现 Agent 平台 ✗ 不做分级调度**。
  · ⚠️ **检查通过不等于业务正确**（**L03 的边界：结构通过 ≠ 业务正确**）。

⭐ 两级出口（**手册 §4 的等级语义**）：
  · `blocking` —— 任一失败 ⇒ **非零退出码**（阻断交付）
  · `observing` —— 失败只记告警 ✗ **不阻断**
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

LEVELS = ("blocking", "observing")


class HarnessError(Exception):
    def __init__(self, message: str, code: str = "harness_error") -> None:
        super().__init__(message)
        self.code = code


@dataclass
class Check:
    """一项检查：**名称 ✗ 等级 ✗ 原函数**（L06 的说法：登记名称 ✗ 等级和原函数）。"""
    name: str
    level: str
    run: object                    # callable(cwd) -> (bool, str)  或子进程命令
    command: list[str] | None = None
    cwd: Path | None = None


@dataclass
class Harness:
    checks: list[Check] = field(default_factory=list)

    def register(self, name: str, level: str, *, command=None, cwd=None, run=None) -> None:
        if level not in LEVELS:
            raise HarnessError(f"未知等级：{level}；只允许 {LEVELS}", "level_invalid")
        if command is None and run is None:
            raise HarnessError(f"检查 {name} 既没有命令也没有函数", "check_empty")
        self.checks.append(Check(name=name, level=level, run=run, command=command, cwd=cwd))

    def run_all(self) -> dict:
        """逐项运行 ✗ 返回**机器可读报告**。每项独立计时 ✗ 互不影响。"""
        if not self.checks:
            # ⚠️ **零个用例不能写成通过**（AGENTS.md 验证一节）
            raise HarnessError("没有任何登记的检查 ✗ 零用例不算通过", "no_checks")
        items = []
        for chk in self.checks:
            started = time.monotonic()
            try:
                if chk.run is not None:
                    passed, detail = chk.run(chk.cwd)
                else:
                    proc = subprocess.run(chk.command, cwd=chk.cwd, capture_output=True,
                                          text=True, encoding="utf-8", errors="replace")
                    passed = proc.returncode == 0
                    tail = (proc.stdout or proc.stderr or "").strip().splitlines()[-3:]
                    detail = f"rc={proc.returncode} " + " / ".join(tail)
            except Exception as error:                       # noqa: BLE001 — 检查自身出错也算失败
                passed, detail = False, f"检查自身出错：{type(error).__name__}: {error}"
            items.append({"name": chk.name, "level": chk.level, "passed": bool(passed),
                          "detail": detail[:600],
                          "elapsed_sec": round(time.monotonic() - started, 3)})
        blocking_failed = [i for i in items if i["level"] == "blocking" and not i["passed"]]
        observing_failed = [i for i in items if i["level"] == "observing" and not i["passed"]]
        decision = "block" if blocking_failed else "pass"
        return {
            "total": len(items),
            "passed": sum(1 for i in items if i["passed"]),
            "blocking_failed": [i["name"] for i in blocking_failed],
            "observing_failed": [i["name"] for i in observing_failed],
            "decision": decision,
            "items": items,
            # ⭐ **检查通过不等于业务正确 ✗ 也不等于已验收**
            "note": "分级只决定是否阻断；**通过不代表业务正确 ✗ 更不代表已验收**",
            "review_status": "pending_human_review",
        }

    @staticmethod
    def exit_code(report: dict) -> int:
        """阻断失败 ⇒ 非零；观察失败 ⇒ 0（**只记告警**）。"""
        return 1 if report.get("decision") == "block" else 0


def main(argv=None) -> int:
    """`python -m eval.harness --suite blocking` —— 手册给的入口形式。

    ⚠️ **本讲的最小套件只是演示**：真正的套件由各讲自己登记。
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    suite = "blocking"
    if "--suite" in argv:
        suite = argv[argv.index("--suite") + 1]
    harness = Harness()
    # 最小套件：**跑课程已有的测试文件**（不新造检查语义）
    mods = [("l01-账本", "tests.test_l01_workbench_bootstrap"),
            ("l00-壳", "tests.test_workbench_server"),
            ("l02-状态不变量", "tests.test_l02_status_invariants"),
            ("l03-解析器", "tests.test_l03_spec_parser"),
            ("l04-V0", "tests.test_l04_workbench_v0")]
    for name, mod in mods:
        harness.register(name, "blocking",
                         command=[sys.executable, "-X", "utf8", "-m", "unittest", mod],
                         cwd=Path(__file__).resolve().parent.parent)
    report = harness.run_all()
    report["suite"] = suite
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return Harness.exit_code(report)


if __name__ == "__main__":
    raise SystemExit(main())
