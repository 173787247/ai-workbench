"""L04 Ticket A · 任务存储：Spec 绑定 ✗ 受控执行 ✗ 状态与证据。

⭐ 与 L01 账本的边界（**AGENTS.md：`bootstrap.py` 是账本 ✗ 本模块管一次交付**）：
  · L01 `bootstrap.py` 管**长期账本**（项目 ✗ 任务 ✗ 命令证据 ✗ 红绿链）。
  · 本模块管**Ticket 级**（Spec 绑定 ✗ 写集 ✗ 执行结果 ✗ 人审状态）。
  · ⚠️ **两者各有自己的库** ⇒ 用不同的 runtime 子目录 ✗ 不互相写。
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

from .execution import Envelope, ExecutionError, build_envelope, run_candidate
from .spec import SpecError, load_spec

STATUSES = ("pending_human_review", "accepted", "rejected", "insufficient_evidence")


class TaskError(Exception):
    def __init__(self, message: str, code: str = "task_error", exit_code: int = 2) -> None:
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code


def _require_actor(actor: str | None, what: str) -> str:
    """**AGENTS.md 与手册共同要求**：具名 ✗ 拒绝 agent 前缀与"待确认"字样。"""
    a = (actor or "").strip()
    if not a:
        raise TaskError(f"{what}需要署名", "actor_required")
    if a.startswith("agent:"):
        raise TaskError("不接受 agent: 前缀 —— 操作者必须是具名的人", "actor_invalid")
    if "待确认" in a or "待本人" in a:
        raise TaskError("请填写真实操作人的署名", "actor_invalid")
    return a


def _db(runtime_dir: str | None) -> Path:
    """Ticket A 自己的库。

    ⚠️ **不改 `runtime_paths.service_runtime`** —— 它属 L00/L01 的壳 ✗ 只服务 `workbench`
    （**手册：「保留已有模块的其他职责和兼容接口」**）⇒ 本模块自带目录规则 ✓
    """
    base = Path(runtime_dir) if runtime_dir else Path.cwd() / ".runtime"
    d = Path(base) / "l04-tasks"
    d.mkdir(parents=True, exist_ok=True)
    return d / "tasks.db"


def _connect(runtime_dir: str | None) -> sqlite3.Connection:
    c = sqlite3.connect(_db(runtime_dir))
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS tasks(
        task_id TEXT PRIMARY KEY, spec_path TEXT, spec_sha256 TEXT, spec_digest TEXT,
        write_scope TEXT, timeout INTEGER, actor TEXT, status TEXT, execution TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    return c


def create_task(*, task_id: str, spec_file: str, allow_write, timeout: int, actor: str,
                runtime_dir: str | None = None) -> dict:
    """建任务：**绑定 Spec**（复用 L03 的解析器）并保存原文摘要。"""
    if not task_id or not spec_file:
        raise TaskError("task-create 需要 --task-id 与 --spec-file", "task_fields_required")
    actor = _require_actor(actor, "task-create")
    try:
        parsed = load_spec(Path(spec_file))          # ⭐ 复用 L03 的解析器，不复制第二套
    except SpecError as error:
        raise TaskError(f"Spec 不可用：{error}", error.code) from error

    # 写集先过信封校验（**与候选无关的那部分**）
    scope = []
    if allow_write:
        try:
            scope = build_envelope(mode="verify", candidate=str(Path.cwd()),
                                   write_scope=allow_write, timeout=60).write_scope
        except ExecutionError as error:
            raise TaskError(str(error), error.code) from error

    raw = Path(spec_file).read_bytes()
    digest = {k: hashlib.sha256(v.encode()).hexdigest()[:16] for k, v in parsed.fields.items()}
    with _connect(runtime_dir) as c:
        if c.execute("SELECT 1 FROM tasks WHERE task_id=?", (task_id,)).fetchone():
            raise TaskError(f"任务编号已存在：{task_id}", "duplicate_task_id")
        c.execute("INSERT INTO tasks(task_id,spec_path,spec_sha256,spec_digest,write_scope,"
                  "timeout,actor,status) VALUES(?,?,?,?,?,?,?,?)",
                  (task_id, str(spec_file), hashlib.sha256(raw).hexdigest(),
                   json.dumps(digest, ensure_ascii=False), json.dumps(scope, ensure_ascii=False),
                   int(timeout), actor, "pending_human_review"))
    return {"task_id": task_id, "spec_path": str(spec_file),
            "spec_sha256": hashlib.sha256(raw).hexdigest(), "spec_digest": digest,
            "write_scope": scope, "timeout": int(timeout), "actor": actor,
            "status": "pending_human_review"}


def _row(row: sqlite3.Row) -> dict:
    return {"task_id": row["task_id"], "spec_path": row["spec_path"],
            "spec_sha256": row["spec_sha256"],
            "spec_digest": json.loads(row["spec_digest"]),
            "write_scope": json.loads(row["write_scope"]),
            "timeout": row["timeout"], "actor": row["actor"], "status": row["status"],
            "execution": json.loads(row["execution"]) if row["execution"] else None}


def show_task(task_id: str, runtime_dir: str | None = None) -> dict:
    with _connect(runtime_dir) as c:
        row = c.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
    if not row:
        raise TaskError(f"任务不存在：{task_id}", "required_task_missing")
    return _row(row)


def run_task(*, task_id: str, candidate: str, verify_only: bool, exec_command: str | None,
             allow_write, timeout: int, runtime_dir: str | None = None) -> dict:
    """在候选目录受控执行一次 ✗ 保存真实结果。"""
    task = show_task(task_id, runtime_dir)
    if task["status"] == "accepted" and not verify_only:
        # 已接受的任务不因新执行而改变状态；执行仍记录，但状态另算
        pass
    scope = list(task["write_scope"])
    if allow_write:
        scope = list(allow_write)
    mode = "verify" if verify_only else "codex"
    try:
        env: Envelope = build_envelope(mode=mode, candidate=candidate,
                                       write_scope=scope, timeout=timeout)
        result = run_candidate(envelope=env, command=exec_command)
    except ExecutionError as error:
        raise TaskError(str(error), error.code) from error

    with _connect(runtime_dir) as c:
        c.execute("UPDATE tasks SET execution=? WHERE task_id=?",
                  (json.dumps(result, ensure_ascii=False), task_id))
    return result


def review_task(*, task_id: str, decision: str, actor: str, note: str = "",
                runtime_dir: str | None = None) -> dict:
    """人审入口。⚠️ **只有具名的人**能作接受决定（**AGENTS.md 完成条件第 4 项**）。"""
    actor = _require_actor(actor, "task-review")
    if decision not in ("accept", "reject", "insufficient"):
        raise TaskError(f"未知决定：{decision}；只允许 accept/reject/insufficient",
                        "decision_invalid")
    with _connect(runtime_dir) as c:
        row = c.execute("SELECT status,execution FROM tasks WHERE task_id=?",
                        (task_id,)).fetchone()
        if not row:
            raise TaskError(f"任务不存在：{task_id}", "required_task_missing")
        execu = json.loads(row["execution"]) if row["execution"] else None
        if decision == "accept" and (not execu or not execu.get("ok")):
            raise TaskError("没有通过的自动检查结果 ✗ 不能接受", "not_ready_for_acceptance")
        status = {"accept": "accepted", "reject": "rejected",
                  "insufficient": "insufficient_evidence"}[decision]
        c.execute("UPDATE tasks SET status=? WHERE task_id=?", (status, task_id))
    return {"task_id": task_id, "decision": decision, "status": status, "actor": actor,
            "note": note, "note_human": "**完整性检查不能代替人的决定**"}
