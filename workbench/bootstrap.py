"""L01 账本：初始化、项目登记、任务创建、运行记录追加、状态查询。

实现依据：`docs/courses/L01/WORKBENCH_SPEC.md`（本人签署版 v1.0）。

设计要点（对应 Spec 的决定 2~4）：
- 摘要一律是**内容的 SHA-256**，用于**发现保存内容是否变化**；
  **不证明作者身份或观察时间真实**。
- 失败即失败：不覆盖旧对象、不改写原任务、**不删除失败输出**。
- `status` 是**只读**的：尚未初始化时明确失败，**绝不靠查询创建运行库**。
- 程序只报 `evidence_complete`；`acceptance` **永远是 `pending_human_review`**。
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS workbench (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    owner TEXT NOT NULL,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    uuid TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    path TEXT,
    purpose TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(project_id),
    title TEXT NOT NULL,
    request TEXT,
    requirement_id TEXT,
    created_by TEXT,
    spec_text TEXT NOT NULL,
    spec_sha256 TEXT NOT NULL,
    problem_text TEXT,
    problem_sha256 TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS evidence (
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL REFERENCES tasks(task_id),
    phase TEXT NOT NULL,
    command_text TEXT NOT NULL,
    output_text TEXT NOT NULL,
    output_sha256 TEXT NOT NULL,
    returncode INTEGER NOT NULL,
    observed_at TEXT NOT NULL,
    recorded_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_evidence_task ON evidence(task_id);
"""

PHASES = ("red", "diff", "green", "observation")
HUMAN_REVIEW = "pending_human_review"


class LedgerError(Exception):
    """明确的失败。调用方据此返回非零退出码并保留既有数据。"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _db(runtime: Path) -> Path:
    return Path(runtime) / "workbench.db"


def _connect(runtime: Path) -> sqlite3.Connection:
    """写入用连接：会创建运行目录与库。仅 init 及之后的写操作可用。"""
    runtime = Path(runtime)
    runtime.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_db(runtime))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def _connect_readonly(runtime: Path) -> sqlite3.Connection:
    """只读连接：库不存在就失败，绝不创建。"""
    path = _db(runtime)
    if not path.exists():
        raise LedgerError(
            f"工作台尚未初始化：{path} 不存在。请先运行 workbench-init。"
            "（状态查询不会创建运行库）"
        )
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _read_text(path_like: str, what: str) -> str:
    path = Path(path_like)
    if not path.is_file():
        raise LedgerError(f"{what}不可读取：{path} 不存在")
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as error:
        raise LedgerError(f"{what}不可读取：{path}（{error}）") from error
    if not text.strip():
        raise LedgerError(f"{what}为空：{path}")
    return text


def _parse_observed_at(value: str) -> str:
    """必须带时区；否则明确失败（Spec §5）。"""
    try:
        stamp = datetime.fromisoformat(value)
    except ValueError as error:
        raise LedgerError(f"--observed-at 不是合法 ISO 时间：{value}") from error
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise LedgerError(
            f"--observed-at 缺少时区：{value}。观察时间必须带时区，否则无法核对。"
        )
    return stamp.isoformat()


def _require_workbench(conn: sqlite3.Connection) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM workbench WHERE id = 1").fetchone()
    if row is None:
        raise LedgerError("工作台尚未初始化。请先运行 workbench-init。")
    return row


def _require_project(conn: sqlite3.Connection, project_id: str) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM projects WHERE project_id = ?", (project_id,)).fetchone()
    if row is None:
        raise LedgerError(f"项目不存在：{project_id}")
    return row


def _require_task(conn: sqlite3.Connection, task_id: str) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
    if row is None:
        raise LedgerError(f"任务不存在：{task_id}")
    return row


# --------------------------------------------------------------------------- #
# 五个账本操作
# --------------------------------------------------------------------------- #

def workbench_init(runtime: Path, owner: str, name: str | None = None) -> dict:
    owner = (owner or "").strip()
    if not owner:
        raise LedgerError("--owner 不能为空")
    conn = _connect(runtime)
    with conn:
        existing = conn.execute("SELECT * FROM workbench WHERE id = 1").fetchone()
        if existing is not None:
            if existing["owner"] != owner:
                # Spec：不用另一个所有者覆盖既有工作台
                raise LedgerError(
                    f"工作台已属于 {existing['owner']}，拒绝被 {owner} 覆盖。"
                )
            return {
                "workbench": {"owner": existing["owner"], "name": existing["name"],
                              "version": existing["version"], "uuid": existing["uuid"]},
                "already_initialised": True,
            }
        import uuid as _uuid
        ident = _uuid.uuid4().hex
        conn.execute(
            "INSERT INTO workbench (id, owner, name, version, uuid, created_at)"
            " VALUES (1, ?, ?, ?, ?, ?)",
            (owner, name or "个人 AI 研发工作台", "V0.1", ident, _now()),
        )
    conn.close()
    return {"workbench": {"owner": owner, "name": name or "个人 AI 研发工作台",
                          "version": "V0.1", "uuid": ident},
            "already_initialised": False}


def project_add(runtime: Path, project_id: str, name: str,
                path: str | None = None, purpose: str | None = None) -> dict:
    if not (project_id or "").strip():
        raise LedgerError("--project-id 不能为空")
    if not (name or "").strip():
        raise LedgerError("--name 不能为空")
    conn = _connect(runtime)
    with conn:
        _require_workbench(conn)
        if conn.execute("SELECT 1 FROM projects WHERE project_id = ?",
                        (project_id,)).fetchone():
            raise LedgerError(f"项目编号已存在：{project_id}（不覆盖旧项目）")
        conn.execute(
            "INSERT INTO projects (project_id, name, path, purpose, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (project_id, name, path, purpose, _now()),
        )
    conn.close()
    return {"project": {"project_id": project_id, "name": name}}


def task_create(runtime: Path, project_id: str, task_id: str, *,
                title: str | None = None, request: str | None = None,
                spec_file: str, problem_file: str | None = None,
                created_by: str | None = None,
                requirement_id: str | None = None) -> dict:
    if not (task_id or "").strip():
        raise LedgerError("任务编号不能为空")
    if not (title or request or "").strip():
        raise LedgerError("--title 与 --request 至少要有一个")
    # 先读文件：不可读就失败，绝不留下半个任务
    spec_text = _read_text(spec_file, "需求文件")
    problem_text = _read_text(problem_file, "原始问题文件") if problem_file else None

    conn = _connect(runtime)
    with conn:
        _require_workbench(conn)
        _require_project(conn, project_id)          # 项目不存在 → 失败
        if conn.execute("SELECT 1 FROM tasks WHERE task_id = ?", (task_id,)).fetchone():
            raise LedgerError(f"任务编号已存在：{task_id}（不改写原任务）")
        conn.execute(
            "INSERT INTO tasks (task_id, project_id, title, request, requirement_id,"
            " created_by, spec_text, spec_sha256, problem_text, problem_sha256, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (task_id, project_id, (title or request or "").strip(), request, requirement_id,
             created_by, spec_text, sha256_text(spec_text), problem_text,
             sha256_text(problem_text) if problem_text is not None else None, _now()),
        )
    conn.close()
    return {"task": {"task_id": task_id, "project_id": project_id,
                     "spec_sha256": sha256_text(spec_text)}}


def evidence_add(runtime: Path, task_id: str, phase: str, command_text: str,
                 output_file: str, returncode: int, observed_at: str) -> dict:
    if phase not in PHASES:
        raise LedgerError(f"--phase 必须是 {PHASES} 之一，收到 {phase!r}")
    if not (command_text or "").strip():
        raise LedgerError("--command-text 不能为空")
    output_text = _read_text(output_file, "输出文件")   # 空输出 → 失败
    stamp = _parse_observed_at(observed_at)            # 缺时区 → 失败

    conn = _connect(runtime)
    with conn:
        _require_workbench(conn)
        _require_task(conn, task_id)                   # 任务不存在 → 失败，旧记录保留
        cur = conn.execute(
            "INSERT INTO evidence (task_id, phase, command_text, output_text,"
            " output_sha256, returncode, observed_at, recorded_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (task_id, phase, command_text, output_text, sha256_text(output_text),
             int(returncode), stamp, _now()),
        )
        evidence_id = cur.lastrowid
    conn.close()
    return {"evidence": {"evidence_id": evidence_id, "task_id": task_id, "phase": phase,
                         "output_sha256": sha256_text(output_text)}}


def _red_green_problem(rows) -> str | None:
    """同一命令的红→绿链检查。返回问题描述，或 None 表示通过。

    Spec §6：先失败 → 后保存改动 → 再用同一测试命令成功；改动与最后成功的返回码应为 0；
    后来再次失败时，不能继续用旧绿灯说明当前材料完整。
    """
    reds = [r for r in rows if r["phase"] == "red"]
    greens = [r for r in rows if r["phase"] == "green"]
    diffs = [r for r in rows if r["phase"] == "diff"]
    if not reds:
        return "缺少红灯（red）记录：无法证明目标能力曾经缺失"
    if not diffs:
        return "缺少改动（diff）记录"
    if not greens:
        return "缺少绿灯（green）记录"

    def when(row):
        return datetime.fromisoformat(row["observed_at"])

    red = max(reds, key=when)          # 取最后一条真实失败
    if red["returncode"] == 0:
        return "红灯记录的返回码为 0：失败原因无效，不能证明能力缺失"
    green = max((g for g in greens if g["command_text"] == red["command_text"]),
                key=when, default=None)
    if green is None:
        return "没有与红灯使用同一命令的成功记录：不能形成同一命令的失败到成功链"
    if green["returncode"] != 0:
        return "最后一条同命令成功记录的返回码不为 0"
    if when(green) <= when(red):
        return "绿灯时间不在红灯之后：顺序无效"
    if not any(when(red) < when(d) < when(green) for d in diffs):
        return "改动记录不在红灯与绿灯之间：顺序无效"
    # 绿灯之后又出现同一命令的失败 → 旧绿灯失效
    later_fail = [r for r in rows
                  if r["command_text"] == red["command_text"]
                  and r["phase"] in ("red", "green")
                  and when(r) > when(green)
                  and r["returncode"] != 0]
    if later_fail:
        return "绿灯之后同一命令再次失败：不能用旧绿灯说明当前材料完整"
    return None


def workbench_status(runtime: Path, *, require_project: str | None = None,
                     require_task: str | None = None,
                     require_red_green: bool = False) -> dict:
    conn = _connect_readonly(runtime)      # 未初始化 → 明确失败；不创建任何东西
    try:
        wb = _require_workbench(conn)
        projects = [dict(r) for r in conn.execute("SELECT * FROM projects ORDER BY created_at")]
        tasks = {r["task_id"]: dict(r) for r in conn.execute("SELECT * FROM tasks ORDER BY created_at")}
        evidence: dict[str, list] = {k: [] for k in tasks}
        for r in conn.execute("SELECT * FROM evidence ORDER BY evidence_id"):
            evidence.setdefault(r["task_id"], []).append(dict(r))

        problems: list[str] = []
        if require_project and require_project not in {p["project_id"] for p in projects}:
            problems.append(f"要求的项目不存在：{require_project}")
        if require_task:
            if require_task not in tasks:
                problems.append(f"要求的任务不存在：{require_task}")
            else:
                rows = evidence.get(require_task, [])
                if require_red_green:
                    issue = _red_green_problem(rows)
                    if issue:
                        problems.append(f"{require_task}：{issue}")

        # 任务里的需求摘要：始终来自创建时的快照，不重读原文件
        for tid, t in tasks.items():
            t["spec_sha256"] = t["spec_sha256"]
            t.pop("spec_text", None)
            t.pop("problem_text", None)

        return {
            "workbench": {"owner": wb["owner"], "name": wb["name"], "version": wb["version"]},
            "projects": projects,
            "tasks": tasks,
            "evidence": evidence,
            "evidence_complete": not problems,
            "problems": problems,
            "acceptance": HUMAN_REVIEW,
            "flowerp_connected": False,
            "checked_at": _now(),
        }
    finally:
        conn.close()
