"""L01 · 账本：初始化、项目登记、任务创建、记录追加、状态查询。

对应 docs/courses/L01/WORKBENCH_SPEC.md。

职责边界（Spec「结构分工」一节）：
  本模块 = 任务与记录逻辑 + 存储；
  命令入口在 cli.py（只做参数解析与转发）。
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

PHASES = ("red", "diff", "green", "note")


class LedgerError(Exception):
    """账本层的明确失败。`code` 供程序判断，`exit_code` 决定 CLI 退出码。"""

    def __init__(self, message: str, code: str = "ledger_error", exit_code: int = 2) -> None:
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code


@dataclass
class BootstrapLedger:
    runtime_dir: Path

    def __post_init__(self) -> None:
        self.runtime_dir = Path(self.runtime_dir)
        self.runtime_dir.mkdir(parents=True, exist_ok=True)
        self.db = self.runtime_dir / "workbench.db"
        with self._connect() as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS workbench(
                    singleton INTEGER PRIMARY KEY CHECK(singleton=1),
                    id TEXT NOT NULL, name TEXT NOT NULL, owner TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP);
                CREATE TABLE IF NOT EXISTS projects(
                    id TEXT PRIMARY KEY, name TEXT NOT NULL, path TEXT, purpose TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP);
                CREATE TABLE IF NOT EXISTS tasks(
                    id TEXT PRIMARY KEY, project_id TEXT NOT NULL, title TEXT,
                    request TEXT, requirement_id TEXT,
                    spec TEXT NOT NULL, spec_sha256 TEXT NOT NULL, spec_path TEXT,
                    problem TEXT, problem_sha256 TEXT, problem_path TEXT,
                    actor TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
                CREATE TABLE IF NOT EXISTS evidence(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL,
                    phase TEXT NOT NULL, command_text TEXT NOT NULL,
                    output TEXT NOT NULL, output_sha256 TEXT NOT NULL,
                    returncode INTEGER NOT NULL, observed_at TEXT NOT NULL,
                    imported_at TEXT DEFAULT CURRENT_TIMESTAMP);
            """)

    def _connect(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.db)
        c.row_factory = sqlite3.Row
        return c

    # ── 内部：读快照，拒绝空与不可读 ──
    @staticmethod
    def _read_snapshot(path: str, label: str) -> tuple[str, str]:
        p = Path(path)
        try:
            text = p.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise LedgerError(f"{label}不存在：{path}", "input_missing") from None
        except UnicodeDecodeError as e:
            raise LedgerError(f"{label}不是 UTF-8：{path}（{e}）", "input_unreadable") from e
        except OSError as e:
            raise LedgerError(f"{label}不可读取：{path}（{e}）", "input_unreadable") from e
        if not text.strip():
            raise LedgerError(f"{label}内容为空：{path}", "input_empty")
        return text, hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def _require_actor(actor: str | None, what: str) -> str:
        a = (actor or "").strip()
        if not a:
            raise LedgerError(f"{what}需要署名", "actor_required")
        if a.startswith("agent:"):
            raise LedgerError("不接受 agent: 前缀 —— 操作者必须是具名的人", "actor_invalid")
        if "待确认" in a or "待本人" in a:
            raise LedgerError("请填写真实操作人的署名", "actor_invalid")
        return a

    # ── 1. 初始化 ──
    def initialize(self, *, owner: str, name: str) -> dict:
        owner = self._require_actor(owner, "workbench-init")
        with self._connect() as c:
            existing = c.execute("SELECT * FROM workbench WHERE singleton=1").fetchone()
            if existing:
                if existing["owner"] != owner:
                    raise LedgerError(
                        f"工作台已由 {existing['owner']!r} 初始化；不能用另一个所有者 {owner!r} 覆盖",
                        "owner_conflict")
                return {"workbench_id": existing["id"], "name": existing["name"],
                        "owner": existing["owner"], "already_initialized": True}
            wid = "WB-L01-" + hashlib.sha256(f"{owner}|{name}".encode()).hexdigest()[:12].upper()
            c.execute("INSERT INTO workbench(singleton,id,name,owner) VALUES(1,?,?,?)",
                      (wid, name, owner))
        return {"workbench_id": wid, "name": name, "owner": owner}

    # ── 2. 项目登记 ──
    def add_project(self, *, project_id: str, name: str, path: str, purpose: str) -> dict:
        if not project_id or not name:
            raise LedgerError("workbench-project-add 需要 --project-id 与 --name",
                              "project_fields_required")
        with self._connect() as c:
            if c.execute("SELECT 1 FROM projects WHERE id=?", (project_id,)).fetchone():
                raise LedgerError(f"项目编号已存在：{project_id}（不覆盖旧项目）",
                                  "duplicate_project_id")
            c.execute("INSERT INTO projects(id,name,path,purpose) VALUES(?,?,?,?)",
                      (project_id, name, path, purpose))
        return {"project_id": project_id, "name": name, "path": path, "purpose": purpose}

    # ── 3. 任务创建（保存 Spec 与问题快照）──
    def create_task(self, *, task_id: str, project_id: str, request: str, actor: str,
                    spec_file: str, problem_file: str | None, requirement_id: str | None,
                    title: str | None) -> dict:
        if not task_id or not project_id:
            raise LedgerError("workbench-task-create 需要 --project-id 与 --task-id",
                              "task_fields_required")
        actor = self._require_actor(actor, "workbench-task-create")
        spec, spec_sha = self._read_snapshot(spec_file, "需求文件")
        problem, problem_sha = ("", "")
        if problem_file:
            problem, problem_sha = self._read_snapshot(problem_file, "问题文件")
        with self._connect() as c:
            if not c.execute("SELECT 1 FROM projects WHERE id=?", (project_id,)).fetchone():
                raise LedgerError(f"项目不存在：{project_id}（任务必须属于已登记项目）",
                                  "project_missing")
            if c.execute("SELECT 1 FROM tasks WHERE id=?", (task_id,)).fetchone():
                raise LedgerError(f"任务编号已存在：{task_id}（不覆盖原任务）",
                                  "duplicate_task_id")
            c.execute("""INSERT INTO tasks(id,project_id,title,request,requirement_id,
                          spec,spec_sha256,spec_path,problem,problem_sha256,problem_path,actor)
                         VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                      (task_id, project_id, title, request, requirement_id,
                       spec, spec_sha, spec_file, problem, problem_sha, problem_file, actor))
        return {"task_id": task_id, "project_id": project_id, "title": title,
                "requirement_id": requirement_id, "requirement_sha256": spec_sha,
                "problem_sha256": problem_sha, "actor": actor,
                "review_status": "pending_human_review"}

    # ── 4. 记录追加 ──
    def add_evidence(self, *, task_id: str, phase: str, command_text: str, output_file: str,
                     returncode: int, observed_at: str) -> dict:
        if not task_id or not phase:
            raise LedgerError("workbench-evidence-add 需要 --task-id 与 --phase",
                              "evidence_fields_required")
        if phase not in PHASES:
            raise LedgerError(f"未知阶段：{phase}；只允许 {PHASES}", "phase_invalid")
        try:
            dt = datetime.fromisoformat(observed_at)
        except ValueError:
            raise LedgerError(f"--observed-at 不是合法时间：{observed_at!r}",
                              "observed_at_invalid") from None
        if dt.tzinfo is None:
            raise LedgerError(
                f"--observed-at 必须带时区（如 2026-10-16T10:00:00+08:00），实际：{observed_at!r}",
                "observed_at_timezone_required")
        output, output_sha = self._read_snapshot(output_file, "输出文件")
        with self._connect() as c:
            if not c.execute("SELECT 1 FROM tasks WHERE id=?", (task_id,)).fetchone():
                raise LedgerError(f"任务不存在：{task_id}（旧记录保留不动）",
                                  "required_task_missing")
            cur = c.execute("""INSERT INTO evidence(task_id,phase,command_text,output,
                                 output_sha256,returncode,observed_at)
                               VALUES(?,?,?,?,?,?,?)""",
                            (task_id, phase, command_text, output, output_sha,
                             int(returncode), observed_at))
        return {"evidence_id": cur.lastrowid, "task_id": task_id, "phase": phase,
                "returncode": int(returncode), "observed_at": observed_at,
                "output_sha256": output_sha, "output_excerpt": output.strip()[:80],
                "source": "user_supplied_observation"}

    # ── 5. 状态查询 ──
    def status(self, *, require_project: str | None = None, require_task: str | None = None,
               require_red_green_evidence: bool = False) -> dict:
        with self._connect() as c:
            wb = c.execute("SELECT * FROM workbench WHERE singleton=1").fetchone()
            projects = [dict(r) for r in c.execute("SELECT * FROM projects ORDER BY id")]
            tasks: list[dict] = []
            for r in c.execute("SELECT * FROM tasks ORDER BY id"):
                t = dict(r)
                t["evidence"] = [dict(e) for e in c.execute(
                    "SELECT * FROM evidence WHERE task_id=? ORDER BY id", (r["id"],))]
                tasks.append(t)

        errors: list[str] = []
        if not wb:
            raise LedgerError("工作台尚未初始化，请先运行 workbench-init",
                              "workbench_not_initialized")
        if require_project and not any(p["id"] == require_project for p in projects):
            raise LedgerError(f"要求的项目不存在：{require_project}", "required_project_missing")

        selected = [t for t in tasks
                    if (not require_task or t["id"] == require_task)
                    and (not require_project or t["project_id"] == require_project)]
        if require_task and not selected:
            raise LedgerError(f"要求的任务不存在：{require_task}", "required_task_missing")

        chain_ok = bool(selected) and all(self._chain(t["evidence"]) for t in selected)
        if require_red_green_evidence and not chain_ok:
            raise LedgerError(
                "完整性检查失败：" + "；".join(self._problems(selected)),
                "same_command_red_diff_green_missing", 1)

        result = {
            "ok": not errors,
            "owner": wb["owner"], "workbench_id": wb["id"], "name": wb["name"],
            "workbench_version": "V0.1",
            "projects": projects, "tasks": tasks if require_task else [],
            "evidence_complete": chain_ok,
            "flowerp_connected": False,
            "acceptance": "pending_human_review",
            "review_status": "pending_human_review",
            "review_note": "材料完整，仍待人工审核",
            "errors": errors,
            "limitations": [
                "用户导入的观察记录，未认证命令执行者和时间",
                "有效红灯原因、Diff 写集与 Spec 签署仍须人工核验；完整性不等于验收完成",
            ],
        }
        if require_task and selected:
            t = selected[0]
            result["task_id"] = t["id"]
            result["project_id"] = t["project_id"]
            result["requirement_sha256"] = t["spec_sha256"]
            result["requirement_snapshot"] = t["spec"]
        if require_red_green_evidence:
            result["ok_chain"] = chain_ok
            result["completeness"] = "ok" if chain_ok else "incomplete"
            result["note"] = "红灯 → 改动 → 同命令绿灯齐全，仍待人工审核"
        return result

    # ── 内部：链与顺序 ──
    @staticmethod
    def _chain(evidence: list[dict]) -> bool:
        by = {}
        for e in evidence:
            by.setdefault(e["phase"], []).append(e)
        if not all(p in by for p in ("red", "diff", "green")):
            return False
        red, diff, green = by["red"][0], by["diff"][0], by["green"][0]
        if red["command_text"] != green["command_text"]:
            return False
        if red["returncode"] == 0 or green["returncode"] != 0:
            return False
        return red["observed_at"] <= diff["observed_at"] <= green["observed_at"]

    @staticmethod
    def _problems(selected: list[dict]) -> list[str]:
        out: list[str] = []
        for t in selected:
            by: dict[str, list[dict]] = {}
            for e in t["evidence"]:
                by.setdefault(e["phase"], []).append(e)
            for phase, label in (("red", "有效失败记录"), ("diff", "改动记录"),
                                 ("green", "修复后成功记录")):
                if phase not in by:
                    out.append(f"缺少{label}（phase={phase}）")
            if all(p in by for p in ("red", "diff", "green")):
                red, diff, green = by["red"][0], by["diff"][0], by["green"][0]
                if not (red["observed_at"] <= diff["observed_at"] <= green["observed_at"]):
                    out.append("时间顺序无效：必须是 红灯 → 改动 → 绿灯")
        return out
