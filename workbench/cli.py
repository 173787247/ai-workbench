"""Keep the same command entry point as the course project.

L01 在 L00 壳的基础上接入五个账本命令，**保留原有的 `serve-workbench`**。
账本逻辑在 `workbench/bootstrap.py`（Spec「结构分工」指定的位置）。
"""
from __future__ import annotations

import argparse
import json
import sys

from .bootstrap import BootstrapLedger, LedgerError
from .runtime_paths import service_runtime
# ⭐ L03：CLI 的 spec 分支**调用** workbench/spec.py 的同一个解析实现，
# 不复制第二套解析逻辑（**手册第 5 步的集成要求**）。
from .spec import SpecError, load_spec
# ⭐ L04 Ticket A：任务存储（Spec 绑定 ✗ 状态 ✗ 证据）与受控执行。
from .execution import ExecutionError
from .task_store import TaskError, create_task, review_task, run_task, show_task

LEDGER_COMMANDS = ("workbench-init", "workbench-project-add", "workbench-task-create",
                   "workbench-evidence-add", "workbench-status")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="个人 AI 研发工作台：L00 壳 + L01 账本")
    commands = parser.add_subparsers(dest="command", required=True)

    # ── L00 原有能力：必须保留 ──
    command = commands.add_parser("serve-workbench", help="启动工作台页面壳（默认 :8001）")
    command.add_argument("--host", default="127.0.0.1")
    command.add_argument("--port", type=int, default=8001)
    command.add_argument("--runtime-dir")

    # ── 1. 初始化 ──
    p = commands.add_parser("workbench-init", help="初始化工作台")
    p.add_argument("--owner", required=True)
    p.add_argument("--name", default="个人 AI 研发工作台")
    p.add_argument("--runtime-dir")

    # ── 2. 项目登记 ──
    p = commands.add_parser("workbench-project-add", help="登记项目")
    p.add_argument("--project-id", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--path", default=".")
    p.add_argument("--purpose", default="组织人与 Codex 的研发协同与交付")
    p.add_argument("--runtime-dir")

    # ── 3. 任务创建 ──
    p = commands.add_parser("workbench-task-create", help="创建任务（含需求与问题快照）")
    p.add_argument("--task-id", required=True)
    p.add_argument("--project-id", required=True)
    p.add_argument("--title")
    p.add_argument("--request", dest="request_alias")
    p.add_argument("--requirement-id")
    p.add_argument("--actor")
    p.add_argument("--spec-file", required=True)
    p.add_argument("--problem-file")
    p.add_argument("--runtime-dir")

    # ── 4. 记录追加 ──
    p = commands.add_parser("workbench-evidence-add", help="为任务追加一条运行记录")
    p.add_argument("--task-id", required=True)
    p.add_argument("--phase", required=True, choices=("red", "diff", "green", "note"))
    p.add_argument("--command-text", required=True)
    p.add_argument("--output-file", required=True)
    p.add_argument("--returncode", required=True, type=int)
    p.add_argument("--observed-at", required=True)
    p.add_argument("--runtime-dir")

    # ── 5. 状态查询 ──
    p = commands.add_parser("workbench-status", help="查询工作台、项目、任务与完整性")
    p.add_argument("--require-project")
    p.add_argument("--require-task")
    p.add_argument("--require-red-green-evidence", action="store_true")
    p.add_argument("--runtime-dir")

    # ── L04 Ticket A 接入：任务存储与受控执行 ──
    p = commands.add_parser("task-create", help="建任务并绑定 Spec（L04 A）")
    p.add_argument("--task-id", required=True)
    p.add_argument("--spec-file", required=True)
    p.add_argument("--allow-write", action="append", default=[])
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("--actor", required=True)
    p.add_argument("--runtime-dir")

    p = commands.add_parser("task-show", help="查任务状态与证据（L04 A）")
    p.add_argument("--task-id", required=True)
    p.add_argument("--runtime-dir")

    p = commands.add_parser("task-run", help="在候选目录受控执行（L04 A）")
    p.add_argument("--task-id", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--allow-write", action="append", default=[])
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("--exec", dest="exec_command")
    p.add_argument("--verify-only", action="store_true")
    p.add_argument("--runtime-dir")

    p = commands.add_parser("task-review", help="人审入口（L04 A）")
    p.add_argument("--task-id", required=True)
    p.add_argument("--decision", required=True)
    p.add_argument("--actor", required=True)
    p.add_argument("--note", default="")
    p.add_argument("--runtime-dir")

    # ── L03 接入：只检查结构的 Spec 解析器 ──
    p = commands.add_parser("spec", help="只检查结构的 Spec 解析器（L03）")
    p.add_argument("spec_path", help="六段合同的 Markdown 路径")

    return parser


def _run_ledger(args) -> int:
    ledger = BootstrapLedger(args.runtime_dir or ".runtime/workbench")
    try:
        if args.command == "workbench-init":
            result = ledger.initialize(owner=args.owner, name=args.name)
        elif args.command == "workbench-project-add":
            result = ledger.add_project(project_id=args.project_id, name=args.name,
                                        path=args.path, purpose=args.purpose)
        elif args.command == "workbench-task-create":
            result = ledger.create_task(
                task_id=args.task_id, project_id=args.project_id,
                request=args.request_alias, actor=args.actor, spec_file=args.spec_file,
                problem_file=args.problem_file, requirement_id=args.requirement_id,
                title=args.title)
        elif args.command == "workbench-evidence-add":
            result = ledger.add_evidence(
                task_id=args.task_id, phase=args.phase, command_text=args.command_text,
                output_file=args.output_file, returncode=args.returncode,
                observed_at=args.observed_at)
        else:
            result = ledger.status(require_project=args.require_project,
                                   require_task=args.require_task,
                                   require_red_green_evidence=args.require_red_green_evidence)
    except LedgerError as error:
        print(json.dumps({"ok": False, "error": str(error), "error_code": error.code},
                         ensure_ascii=False), file=sys.stderr)
        return error.exit_code
    print(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2, default=str))
    return 0


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    # ⭐ L04 Ticket A：四个任务命令。
    if args.command in ("task-create", "task-show", "task-run", "task-review"):
        try:
            if args.command == "task-create":
                out = {"ok": True, **create_task(
                    task_id=args.task_id, spec_file=args.spec_file,
                    allow_write=args.allow_write, timeout=args.timeout,
                    actor=args.actor, runtime_dir=args.runtime_dir)}
            elif args.command == "task-show":
                out = {"ok": True, **show_task(args.task_id, args.runtime_dir)}
            elif args.command == "task-run":
                out = run_task(task_id=args.task_id, candidate=args.candidate,
                               verify_only=args.verify_only,
                               exec_command=args.exec_command,
                               allow_write=args.allow_write, timeout=args.timeout,
                               runtime_dir=args.runtime_dir)
            else:
                out = {"ok": True, **review_task(
                    task_id=args.task_id, decision=args.decision, actor=args.actor,
                    note=args.note, runtime_dir=args.runtime_dir)}
        except (TaskError, ExecutionError) as error:
            print(json.dumps({"ok": False, "error": str(error),
                              "error_code": getattr(error, "code", "task_error")},
                             ensure_ascii=False), file=sys.stderr)
            return getattr(error, "exit_code", 2)
        ok = bool(out.get("ok", True))
        print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
        return 0 if ok else 1

    # ⭐ L03：spec 分支 —— 成功输出六个原文字段；失败非零且错误能定位。
    if args.command == "spec":
        try:
            parsed = load_spec(args.spec_path)
        except SpecError as error:
            print(json.dumps({"ok": False, "error": str(error),
                              "error_code": error.code}, ensure_ascii=False),
                  file=sys.stderr)
            return 2
        print(json.dumps({"ok": True, "path": parsed.path, **parsed.as_dict()},
                         ensure_ascii=False, indent=2))
        return 0

    if args.command in LEDGER_COMMANDS:
        return _run_ledger(args)

    # L00 的页面壳
    from .workbench_server import serve
    try:
        serve(args.host, args.port, str(service_runtime("workbench", args.runtime_dir)))
    except (OSError, ValueError) as error:
        print(f"启动失败：{error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
