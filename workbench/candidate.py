"""L04 Ticket B：从独立客户仓库创建**隔离候选**，并在候选内受控执行。

对应合同 `lesson-04-submission/WB-L04-BOOTSTRAP.md` 与课程 `workspace_boundary`：

- **读**独立 FlowERP 仓库的位置，**不把它的 `flowerp/` 复制回工作台仓库**；
- 为本次任务创建**临时隔离候选**（含来源与哈希记录）；
- **候选修改不自动写回任何源仓库**；
- 执行复用 `workbench.execution.run_task` 的受控语义（目录/写集/超时/越界/失败/Eval/人审）。
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .execution import ExecutionError, ExecutionLimits, run_task

#: 独立客户仓库里必须存在的关键文件（按课程基线的真实文件名）
REQUIRED_CUSTOMER_FILES = ("flowerp/service.py",)

#: 创建候选时排除的目录
_EXCLUDE = {".git", "__pycache__", ".venv", ".runtime", ".mypy_cache", ".pytest_cache"}


@dataclass(frozen=True)
class Candidate:
    path: Path
    customer_root: Path
    source_hash: str
    created_at: str
    included: tuple[str, ...]


def resolve_customer_root(explicit: str | os.PathLike | None = None) -> Path:
    """确定独立客户仓库位置：显式参数优先，其次环境变量 FLOWERP_PROJECT_ROOT。"""
    raw = explicit or os.environ.get("FLOWERP_PROJECT_ROOT")
    if not raw:
        raise ExecutionError(
            "未指定独立客户仓库位置：请传 --customer-root，"
            "或设置环境变量 FLOWERP_PROJECT_ROOT。"
            "（工作台仓库不保存 flowerp/，必须由调用方指定来源）"
        )
    root = Path(raw).expanduser().resolve()
    if not root.is_dir():
        raise ExecutionError(f"客户仓库不存在或不是目录：{root}")
    missing = [f for f in REQUIRED_CUSTOMER_FILES if not (root / f).is_file()]
    if missing:
        raise ExecutionError(
            f"客户仓库未准备好，缺少：{', '.join(missing)}（位于 {root}）"
        )
    venv_python = root / ".venv" / "bin" / "python"
    if not venv_python.exists():
        venv_python = root / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        raise ExecutionError(f"客户仓库缺少可用的 .venv 解释器：{root}/.venv")
    return root


def _tree_hash(root: Path, *, subdirs: tuple[str, ...]) -> str:
    """对指定子目录做内容汇总哈希，用于记录来源版本。"""
    digest = hashlib.sha256()
    for sub in subdirs:
        base = root / sub
        if not base.is_dir():
            continue
        for path in sorted(p for p in base.rglob("*") if p.is_file()):
            if any(part in _EXCLUDE for part in path.parts):
                continue
            digest.update(path.relative_to(root).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def create_candidate(customer_root: Path, runtime: Path, *, task_id: str,
                     subdirs: tuple[str, ...] = ("flowerp",)) -> Candidate:
    """把客户源码**复制**成隔离候选。**只读源仓库：不修改、不写回。**"""
    customer_root = Path(customer_root).resolve()
    runtime = Path(runtime)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    candidate_root = runtime / "candidates" / f"{task_id}-{stamp}"
    if candidate_root.exists():
        raise ExecutionError(f"候选目录已存在，拒绝覆盖：{candidate_root}")
    candidate_root.mkdir(parents=True, exist_ok=False)

    source_hash = _tree_hash(customer_root, subdirs=subdirs)
    included: list[str] = []
    for sub in subdirs:
        src = customer_root / sub
        if not src.is_dir():
            continue
        dst = candidate_root / sub
        shutil.copytree(src, dst,
                        ignore=shutil.ignore_patterns(*_EXCLUDE))
        included.append(sub)

    created_at = datetime.now(timezone.utc).isoformat()
    meta = {
        "task_id": task_id,
        "customer_root": str(customer_root),
        "candidate_path": str(candidate_root),
        "source_hash": source_hash,
        "included": included,
        "created_at": created_at,
        "writeback": False,
        "note": "候选是副本；候选内的修改不自动写回源仓库。",
    }
    (candidate_root / ".course").mkdir(exist_ok=True)
    (candidate_root / ".course" / "candidate.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return Candidate(path=candidate_root, customer_root=customer_root,
                     source_hash=source_hash, created_at=created_at,
                     included=tuple(included))


def run_ticket(customer_root: Path, runtime: Path, *, spec_path, task_id: str,
               command, write_scope: tuple[str, ...], timeout: float = 120.0,
               verify_only: bool = False) -> dict:
    """创建隔离候选并在其中受控执行一次任务（Ticket B）。"""
    from .spec import SpecError, load_spec
    try:
        load_spec(spec_path)          # 合同必须先过结构闸门
    except SpecError as error:
        raise ExecutionError(f"Spec 不合格，拒绝启动任务：{error}") from error

    candidate = create_candidate(customer_root, runtime, task_id=task_id)
    after = _tree_hash(Path(customer_root), subdirs=candidate.included)
    if after != candidate.source_hash:
        raise ExecutionError("源仓库在创建候选期间发生变化，已停止（请核对来源版本）")

    limits = ExecutionLimits(workdir=candidate.path, write_scope=write_scope,
                             timeout=timeout)
    # ---- 第六轮复验（第 4 轮也提过）⑤：**源客户仓库必须被监视** ----
    # 原来没传 `extra_outside` ✗ 于是「命令直接写源仓库」**完全不可见** ✗
    # 实测：`printf BACKDOOR > <customer_root>/flowerp/backdoored.py` →
    #   `stopped=False ✗ out_of_scope=[] ✗ stop_reason=''` ✗ 而文件真的写进去了 ✓
    #
    # ⚠ `extra_outside` 是**替换**默认的 `workdir.parent` ✗ 所以要**两个都给** ✓
    #   候选目录的父目录（`candidates/`）与**源客户仓库**都要在监视范围内 ✓
    customer_root_p = Path(candidate.customer_root)
    watch = (customer_root_p, candidate.path.parent)
    result = run_task(spec_path, task_id=task_id, command=command, limits=limits,
                      runtime=runtime, verify_only=verify_only, extra_outside=watch)
    payload = result.as_dict()

    # ---- `writeback` 必须是**观察结果** ✗ 不是字面量 ----
    # 原来写死 `False` ✗ 复验者第 4 轮指出：「那是字面量常量 ✗ 不是观察结果」✓
    # 现在：**跑完后再算一次源仓库的树哈希** ✗ 变了就是真的发生了写回 ✓
    after_source = _tree_hash(customer_root_p, subdirs=candidate.included)
    writeback = after_source != candidate.source_hash
    payload["candidate"] = {
        "path": str(candidate.path),
        "customer_root": str(customer_root_p),
        "source_hash": candidate.source_hash,
        "source_hash_after": after_source,
        "included": list(candidate.included),
        # **观察出来的** ✗ 不是写死的 ✓
        "writeback": writeback,
        "writeback_note": ("源客户仓库的树哈希在执行后**发生了变化** ✗ 发生了写回 ✓"
                           if writeback else
                           "源客户仓库的树哈希与执行前一致 ✓ 未发生写回"),
        "watch_roots": [str(x) for x in watch],
    }
    if writeback:
        # 写回 = 越界 ✗ 判失败（即使受控执行自己没发现——比如写到了监视之外）
        payload["stopped"] = True
        payload["eval_ok"] = False
        msg = ("源客户仓库在执行期间被修改（写回）✗ 违反「不修改独立 FlowERP 仓库」的非目标")
        payload["stop_reason"] = (msg if not payload.get("stop_reason")
                                  else payload["stop_reason"] + "；" + msg)
        payload["eval_message"] = msg
    return payload
