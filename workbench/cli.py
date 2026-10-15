"""Keep the same command entry point as the course project.

L00 提供 `serve-workbench`；L01 在其上接入五个账本命令
（依据 `docs/courses/L01/WORKBENCH_SPEC.md` 本人签署版 v1.0）。
"""
from __future__ import annotations

import argparse
import json
import sys

from .runtime_paths import service_runtime


def _emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _runtime(args) -> str:
    return str(service_runtime("workbench", getattr(args, "runtime_dir", None)))


def _ledger():
    from . import bootstrap
    return bootstrap


def _run(action):
    """统一收口：明确的失败 → 退出码 2，且不产生半成品。"""
    from .bootstrap import LedgerError
    try:
        payload = action()
    except LedgerError as error:
        print(f"失败：{error}", file=sys.stderr)
        return 2
    except (OSError, ValueError) as error:
        print(f"失败：{error}", file=sys.stderr)
        return 2
    _emit(payload)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="个人 AI 研发工作台")
    commands = parser.add_subparsers(dest="command", required=True)

    # ---- L00：保留原样 ----
    serve = commands.add_parser("serve-workbench", help="启动工作台页面壳（默认 :8001）")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8001)
    serve.add_argument("--runtime-dir")

    # ---- L01：五个账本命令 ----
    init = commands.add_parser("workbench-init", help="初始化工作台")
    init.add_argument("--owner", required=True)
    init.add_argument("--name")
    init.add_argument("--runtime-dir")

    proj = commands.add_parser("workbench-project-add", help="登记项目")
    proj.add_argument("--project-id", required=True)
    proj.add_argument("--name", required=True)
    proj.add_argument("--path")
    proj.add_argument("--purpose")
    proj.add_argument("--runtime-dir")

    task = commands.add_parser("workbench-task-create", help="创建任务并保存需求/问题快照")
    task.add_argument("--project-id", required=True)
    task.add_argument("--task-id", required=True)
    task.add_argument("--title")
    task.add_argument("--request")
    task.add_argument("--spec-file", required=True)
    task.add_argument("--problem-file")
    task.add_argument("--created-by")
    task.add_argument("--requirement-id")
    task.add_argument("--runtime-dir")

    ev = commands.add_parser("workbench-evidence-add", help="追加一条运行记录")
    ev.add_argument("--task-id", required=True)
    ev.add_argument("--phase", required=True, choices=["red", "diff", "green", "observation"])
    ev.add_argument("--command-text", required=True)
    ev.add_argument("--output-file", required=True)
    ev.add_argument("--returncode", required=True, type=int)
    ev.add_argument("--observed-at", required=True)
    ev.add_argument("--runtime-dir")

    st = commands.add_parser("workbench-status", help="查询完整性（只读，不创建运行库）")
    st.add_argument("--require-project")
    st.add_argument("--require-task")
    st.add_argument("--require-red-green-evidence", action="store_true")
    st.add_argument("--runtime-dir")

    # ---- L03：合同结构闸门（只检查六段结构，不判断业务口径）----
    spec = commands.add_parser("spec", help="解析六段式合同：只检查结构，不判断业务正确性")
    spec.add_argument("spec_path", help="六段式合同文件路径（UTF-8 Markdown）")

    # ---- L04：受控执行（绑定 Spec、限目录/写集/超时、范围检查、最小 Eval）----
    ex = commands.add_parser("execute-task", help="受控执行一次任务：越界/失败/超时都会停止")
    ex.add_argument("--spec", required=True, help="六段式合同路径")
    ex.add_argument("--task-id", required=True)
    # ⚠ dest 必须避开 "command"：subparsers 已占用 dest="command" 存子命令名，
    # 同名会让 --command 的值覆盖子命令名（曾导致 execute-task 静默退 2）。
    ex.add_argument("--command", dest="command_text", required=True,
                    help="要执行的命令（单个字符串，按 shell 语义拆分请自行加引号）")
    ex.add_argument("--workdir", required=True, help="执行目录（必须存在）")
    ex.add_argument("--write-scope", action="append", required=True,
                    help="允许写入的相对路径前缀，可重复；不声明则拒绝执行")
    ex.add_argument("--timeout", type=float, default=60.0)
    ex.add_argument("--verify-only", action="store_true", help="只核对限制，不执行")
    ex.add_argument("--register-if-missing", action="store_true",
                    help="任务未登记时由本次执行自动登记（默认要求任务已存在）")
    ex.add_argument("--no-ledger", action="store_true",
                    help="不绑定 L01 账本（默认绑定；仅用于无账本的临时实验）")
    ex.add_argument("--runtime-dir")

    # ---- L04 Ticket B：在隔离候选里执行（读独立客户仓库，不写回）----
    cs = commands.add_parser("course-submit",
                             help="从独立客户仓库创建隔离候选并在其中受控执行")
    cs.add_argument("--spec", required=True, help="本讲业务合同路径")
    cs.add_argument("--task-id", required=True)
    cs.add_argument("--command", dest="command_text", required=True)
    cs.add_argument("--write-scope", action="append", required=True)
    cs.add_argument("--customer-root", help="独立 FlowERP 仓库绝对路径（默认取 FLOWERP_PROJECT_ROOT）")
    cs.add_argument("--timeout", type=float, default=120.0)
    cs.add_argument("--verify-only", action="store_true")
    cs.add_argument("--runtime-dir")

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "serve-workbench":
        from .workbench_server import serve
        try:
            serve(args.host, args.port, _runtime(args))
        except (OSError, ValueError) as error:
            print(f"启动失败：{error}", file=sys.stderr)
            return 2
        return 0

    if args.command == "spec":
        # 唯一解析入口：调用 workbench.spec，不在 CLI 复制第二套解析逻辑
        from .spec import SpecError, load_spec
        try:
            parsed = load_spec(args.spec_path)
        except SpecError as error:
            print(f"结构不合格：{error}", file=sys.stderr)
            return 1
        _emit(parsed.as_dict())
        return 0

    if args.command == "execute-task":
        import shlex
        from .execution import ExecutionError, ExecutionLimits, run_task
        try:
            limits = ExecutionLimits(workdir=args.workdir,
                                     write_scope=tuple(args.write_scope),
                                     timeout=args.timeout)
            result = run_task(args.spec, task_id=args.task_id,
                              command=shlex.split(args.command_text), limits=limits,
                              runtime=service_runtime("workbench", args.runtime_dir),
                              verify_only=args.verify_only,
                              register_if_missing=args.register_if_missing,
                              ledger=not args.no_ledger)
        except ExecutionError as error:
            print(f"拒绝执行：{error}", file=sys.stderr)
            return 2
        _emit(result.as_dict())
        return 0 if (not result.stopped and result.eval_ok) or result.verify_only else 1

    if args.command == "course-submit":
        import shlex
        from .candidate import resolve_customer_root, run_ticket
        from .execution import ExecutionError
        try:
            customer = resolve_customer_root(args.customer_root)
            payload = run_ticket(
                customer, service_runtime("workbench", args.runtime_dir),
                spec_path=args.spec, task_id=args.task_id,
                command=shlex.split(args.command_text),
                write_scope=tuple(args.write_scope), timeout=args.timeout,
                verify_only=args.verify_only)
        except ExecutionError as error:
            print(f"拒绝执行：{error}", file=sys.stderr)
            return 2
        _emit(payload)
        return 0 if (not payload["stopped"] and payload["eval_ok"]) or payload["verify_only"] else 1

    ledger = _ledger()
    rt = _runtime(args)

    if args.command == "workbench-init":
        return _run(lambda: ledger.workbench_init(rt, args.owner, args.name))
    if args.command == "workbench-project-add":
        return _run(lambda: ledger.project_add(rt, args.project_id, args.name,
                                               args.path, args.purpose))
    if args.command == "workbench-task-create":
        return _run(lambda: ledger.task_create(
            rt, args.project_id, args.task_id, title=args.title, request=args.request,
            spec_file=args.spec_file, problem_file=args.problem_file,
            created_by=args.created_by, requirement_id=args.requirement_id))
    if args.command == "workbench-evidence-add":
        return _run(lambda: ledger.evidence_add(
            rt, args.task_id, args.phase, args.command_text, args.output_file,
            args.returncode, args.observed_at))
    if args.command == "workbench-status":
        def _status():
            payload = ledger.workbench_status(
                rt, require_project=args.require_project, require_task=args.require_task,
                require_red_green=args.require_red_green_evidence)
            if payload["problems"]:
                # 查询本身成功，但要求的对象/证据不满足 → 非零退出码，且不改写任何数据
                _emit(payload)
                return None
            return payload

        from .bootstrap import LedgerError
        try:
            payload = ledger.workbench_status(
                rt, require_project=args.require_project, require_task=args.require_task,
                require_red_green=args.require_red_green_evidence)
        except LedgerError as error:
            print(f"失败：{error}", file=sys.stderr)
            return 2
        _emit(payload)
        return 0 if not payload["problems"] else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
