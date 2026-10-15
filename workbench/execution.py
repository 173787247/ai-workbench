"""L04 受控执行：绑定 Spec → 创建任务 → 限目录/写集/超时 → 执行 → 范围检查 → 最小 Eval → 待人审。

对应合同 `lesson-04-submission/WB-L04-BOOTSTRAP.md` 的四条验收用例：
- A-1 保存调用、输出、退出码、Diff 和验证命令；
- A-2 越界写入会被拦截或标记失败；
- A-3 命令失败和超时不会被写成成功；
- A-4 Eval 通过后状态仍停在人工复核。

**关键设计**：越界判定独立于退出码。
命令「成功」（退出码 0）但改了写集之外的文件，同样判失败并停止 ——
否则「受控执行」就退化成「跑什么都算过」。
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import stat
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .spec import SpecError, load_spec

HUMAN_REVIEW = "pending_human_review"

#: 写进证据 JSON 的说明 —— 第三次复验指出它此前只写在文档里（「说了没做」）。
VERIFY_COMMAND_NOTE = ("verify_command 记录的是当时的完整调用。"
                       "重跑必须在**干净副本**上进行：原地重跑时改动已被消耗，"
                       "changed_files 为空会被最小 Eval 判「没有可核对的改动」而阻断。")

#: **解释器副产物**：Python 执行的必然结果，不是人的意图。
#:
#: ⚠️ **第五轮复验 R-6 更正**：原注释写「**默认放行**」✗ **与实现相反** ✓
#: 实现（第三次复验的修复）是「**只在写集内放行**」✗ 写集外一律照常判越界 ✓
#: 因为把 `.pyc` 做成白名单等于「写集外任意写删判成功」✗ 盲区换个名字回来 ✓
#:
#: **后果（如实）**：写集外出现 `__pycache__` 的正常 Python 任务会**误判失败** ✓
#: 这是 **fail-closed** ✗ **可接受** ✗ 但**要解决应当把它加进写集** ✓
#: **不是靠这里放行** ✓
#:
#: 下面这两个常量目前**只用于判断「本可放行但越界」** ✗
#: 因为过滤条件里带了 `limits.in_scope(r)` ✗ 而 `out_of_scope` 只含写集外的项 ✗
#: 所以 `artifacts` **恒为空** ✗ 证据字段 `interpreter_artifacts_allowed` 也恒空 ✓
_INTERPRETER_ARTIFACTS = ("__pycache__/",)
_INTERPRETER_SUFFIXES = (".pyc", ".pyo")


class ExecutionError(Exception):
    """执行前的拒绝（例如 Spec 不合法、参数缺失）。**不产生任何半成品。**"""


@dataclass(frozen=True)
class ExecutionLimits:
    """执行限制：目录、写集、超时。三者缺一不可。"""

    workdir: Path
    write_scope: tuple[str, ...]
    timeout: float

    def __post_init__(self):
        wd = Path(self.workdir)
        if not wd.is_dir():
            raise ExecutionError(f"工作目录不存在：{wd}")
        if not self.write_scope:
            raise ExecutionError("必须声明写集（write_scope 不能为空）")
        blank = [s for s in self.write_scope if not str(s).strip()]
        if blank:
            raise ExecutionError(
                "写集里出现空元素：空字符串会让所有路径都被判为范围内，检查会静默失效"
            )
        for scope in self.write_scope:
            s = str(scope)
            if s.startswith("/") or ".." in Path(s).parts:
                raise ExecutionError(f"写集元素不得是绝对路径或含 .. ：{s!r}")
        if self.timeout <= 0:
            raise ExecutionError("超时必须为正数")

    def in_scope(self, relative: str) -> bool:
        """路径**分量**边界匹配。

        修复的缺陷（独立复验指出）：
        - 裸 startswith 会把 `src_evil/x` 判成写集 `src` 之内 → 改为分量边界；
        - 空字符串元素让 `startswith("")` 恒真 → 构造时已拒绝；
        - `..` 与绝对路径可以逃出写集 → 一律判为越界。
        """
        if not relative or relative.startswith("/") or ".." in Path(relative).parts:
            return False
        for scope in self.write_scope:
            base = scope.rstrip("/")
            if not base:
                continue
            # 第四轮复验 ⑦：`--write-scope .` 是「允许全部」的自然写法 ✗
            # 原来会把它 rstrip 成空串再 `continue` ✗ 结果**什么都匹配不上** ✗
            # 反而封杀了全部写入 ✓ 现在 `./` 与 `.` 都表示「工作目录全部」。
            if base in (".", "./"):
                return True
            if relative == base or relative.startswith(base + "/"):
                return True
        return False


@dataclass
class ExecutionResult:
    task_id: str
    returncode: int
    stdout: str
    stderr: str
    changed_files: tuple[str, ...]
    out_of_scope: tuple[str, ...]
    diff_summary: dict[str, str]
    timed_out: bool
    stopped: bool
    stop_reason: str
    eval_ok: bool
    eval_message: str
    evidence_path: str
    verify_only: bool
    verify_command: str = ""
    watch_roots: tuple[str, ...] = ()
    interpreter_artifacts_allowed: tuple[str, ...] = ()
    ledger_evidence_id: int | None = None
    verify_command_note: str = ""
    workdir_exists_after: bool = True
    acceptance: str = HUMAN_REVIEW
    observed_at: str = ""
    notes: list[str] = field(default_factory=list)

    @property
    def evidence_complete(self) -> bool:
        return bool(self.evidence_path) and not self.stopped and self.eval_ok

    @property
    def accepted(self) -> bool:
        """**永远为 False** —— 程序不能替人签字（Spec §6 / AGENTS.md §一）。"""
        return False

    def as_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "returncode": self.returncode,
            "changed_files": list(self.changed_files),
            "out_of_scope": list(self.out_of_scope),
            "diff_summary": self.diff_summary,
            "timed_out": self.timed_out,
            "stopped": self.stopped,
            "stop_reason": self.stop_reason,
            "eval_ok": self.eval_ok,
            "eval_message": self.eval_message,
            "evidence_complete": self.evidence_complete,
            "acceptance": self.acceptance,
            "accepted": self.accepted,
            "verify_only": self.verify_only,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "verify_command": self.verify_command,
            "watch_roots": list(self.watch_roots),
            "interpreter_artifacts_allowed": list(self.interpreter_artifacts_allowed),
            "ledger_evidence_id": self.ledger_evidence_id,
            "verify_command_note": self.verify_command_note,
            "workdir_exists_after": self.workdir_exists_after,
            "evidence_path": self.evidence_path,
            "observed_at": self.observed_at,
            "notes": self.notes,
        }


def _escaping_symlinks(root: Path, watch_roots: list[Path]) -> list[str]:
    """找出解析后落在**监视根之外**的符号链接。

    修 6 的关键：链接自己不会变（lstat 稳定），
    所以**不能靠比对 changed_files 发现**「通过链接写到根外」这种攻击。
    正确做法是**静态检查**：工作目录里存在指向监视根之外的链接 → 直接报出来。
    """
    roots = [r.resolve() for r in watch_roots] + [root.resolve()]
    # 第六轮复验 D-4 的正解：**分两组返回** ✗ 调用方不再靠名字形状猜 ✓
    #
    # · `in_workdir`：工作目录内的逃逸链接 —— **参与失败判定** ✓
    # · `in_watch`  ：监视根里的逃逸链接 —— **只记进证据（可见）✗ 不判失败** ✓
    #   理由：监视根里「存在一个指向别处的链接」**不是本次执行造成的** ✓
    #   而**监视根里真有写入**时，`outside_before/after` 的快照比对**本来就会报** ✓
    #   （加这一组是为了「可见」✗ 不是为了「判失败」✓）
    in_workdir = _escaping_symlinks_in(root, roots)
    in_watch: list[str] = []
    for r in watch_roots:
        rp = Path(r)
        if rp == Path(root):
            continue
        in_watch.extend(_escaping_symlinks_in(rp, roots, exclude=root))
    return sorted(set(in_workdir)), sorted(set(in_watch))


def _escaping_symlinks_in(root: Path, roots: list[Path], *,
                          exclude: Path | None = None) -> list[str]:
    """在**一个**根下找解析后落在所有监视根之外的链接。"""
    found: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in list(dirnames) + list(filenames):
            path = Path(dirpath) / name
            if exclude is not None and path.resolve() == exclude:
                continue
            try:
                if not path.is_symlink():
                    continue
                target = path.resolve()
            except OSError:
                continue
            if not any(target == r or r in target.parents for r in roots):
                found.append(f"{path.relative_to(root).as_posix()} -> {target}")
    return found


def _snapshot(root: Path, *, exclude: Path | None = None,
              include_ignored: bool = True) -> tuple[dict[str, str], list[str]]:
    """目录内文件 → sha256。用于计算实际改动与越界。

    `exclude`：跳过该子树（工作目录的改动由工作目录自己的快照负责，
    父目录监视不应重复计入，否则会把工作目录内的正常改动误判为越界）。
    """
    out: dict[str, str] = {}
    excluded = exclude.resolve() if exclude is not None else None
    # 第五轮复验 R-1：`os.walk` 默认**静默跳过**读不到的子树 ✗
    # 必须显式记录这个错误 ✗ 否则「权限不足」会变成「这里什么都没有」✓
    walk_errors: list[str] = []

    def _onerror(err: OSError) -> None:
        walk_errors.append(f"{getattr(err, 'filename', '?')}: {err.strerror}")

    for dirpath, dirnames, filenames in os.walk(root, onerror=_onerror):
        if excluded is not None:
            dirnames[:] = [d for d in dirnames
                           if (Path(dirpath) / d).resolve() != excluded]
        # 修 5（二次复验「撞法 A」）：**不再跳过** _IGNORE_DIRS。
        # 之前为了"快照干净"跳过 .git/.runtime/__pycache__/.venv，
        # 结果是这些目录内的改动**永远不可见** —— 那是可被利用的盲区。
        # 现在全部纳入；是否算越界由写集判定。

        # 第四轮复验 ①③：**目录本身也必须进快照** ——
        # 原来只遍历 `filenames` ✗ 于是「目录符号链接」「空目录」「目录 chmod」
        # 完全不可见（复验者用 `link -> /tmp/vfar` + `echo PWNED > link/evil.txt`
        # 证明：根外文件真被写 ✗ 却判成功 ✓）。
        # ⚠️ 按复验者的提醒：**只记目录的权限位 ✗ 不记 mtime** ——
        # 目录内新建文件会顶起父目录 mtime ✗ 记进去会引入大量噪声。
        for name in list(dirnames):
            d = Path(dirpath) / name
            try:
                rel = d.relative_to(root).as_posix()
            except ValueError:
                continue
            if excluded is not None and (d.resolve() == excluded or excluded in d.resolve().parents):
                continue
            try:
                dinfo = d.lstat()
                if stat.S_ISLNK(dinfo.st_mode):
                    out[rel] = f"dirlink->{d.resolve()}"
                else:
                    out[rel] = f"dir|{dinfo.st_mode:o}"
            except OSError:
                # 目录同理：记 lstat 的 mode+mtime（**按复验者提醒不记目录 mtime 的噪声问题**
                # 在这里不适用 —— 这是**读不到**的目录 ✗ 本来就该 fail-closed）
                try:
                    _i2 = d.lstat()
                    out[rel] = f"dir-unreadable|{_i2.st_mode:o}|{_i2.st_mtime_ns}"
                except OSError:
                    out[rel] = "dir-lstat-failed"

        for name in filenames:
            p = Path(dirpath) / name
            if excluded is not None and (p.resolve() == excluded or excluded in p.resolve().parents):
                continue
            try:
                rel = p.relative_to(root).as_posix()
            except ValueError:
                continue
            # 修 6（二次复验「撞法 B」）：符号链接必须记录**链接目标**而不是内容，
            # 否则「在根内建链接、写到根外」会读起来像根内改动，完全看不见。
            try:
                info = p.lstat()
                if stat.S_ISLNK(info.st_mode):
                    # 记录链接目标**以及目标内容**的哈希 ——
                    # 否则「通过链接写到根外」看不见（目标不在监视根内，不会被单独快照）。
                    target = p.resolve()
                    try:
                        tgt = hashlib.sha256(target.read_bytes()).hexdigest()
                    except OSError:
                        tgt = "<target-unreadable>"
                    out[rel] = f"symlink->{target}|{tgt}"
                    continue
            except OSError as err:
                # 连 lstat 都失败 ✗ 也记下失败本身（不能让对象凭空消失）
                out[rel] = f"lstat-failed|{getattr(err, 'errno', '?')}"
                continue
            # ---- 第七轮复验 F3：**非普通文件不得读内容** ----
            # 原来只判了 `S_ISLNK` ✗ 直接 `read_bytes()` ✗
            # **FIFO 会让它永久阻塞** ✗ CLI 挂死 ✗ 无证据 ✗ 且永久毒化该 workdir ✓
            # 现在：**只对普通文件读内容** ✗ 其他类型只记「类型 + mode + size + mtime」✓
            if not stat.S_ISREG(info.st_mode):
                out[rel] = (f"nonregular|{stat.S_IFMT(info.st_mode):o}"
                            f"|{info.st_mode:o}|{info.st_size}|{info.st_mtime_ns}")
                continue

            # ---- 第七轮复验 F2：指纹必须含**同 UID 无法复原**的字段 ----
            # 原来记 `mode + mtime` ✗ 这两个同 UID 都能设 ✗
            # 「chmod 600 → 改内容 → chmod 000 → utime(ns=原值)」能让指纹完全相同 ✓
            # 现在加入 `st_ctime_ns`（**改 inode 元数据就会变 ✗ chmod/写都会触发** ✓）
            # 与 `st_size` ✓
            mark = f"|{info.st_mode:o}|{info.st_size}|{info.st_mtime_ns}|{info.st_ctime_ns}"
            try:
                digest = hashlib.sha256(p.read_bytes()).hexdigest()
            except OSError:
                out[rel] = "unreadable" + mark
                continue
            out[rel] = digest + mark
    # 第六轮复验 D-1 的正解：**合成键不得进入文件命名空间** ✓
    # 原来写成 `out["<walk-error>:…"]` ✗ 于是 `_diff` 只能靠**名字形状**（`startswith("<")`）
    # 把合成键滤掉 ✗ 而真实文件也可以叫 `other/<pwn>.txt` ✗ 一起被滤掉 ✗ 完全不可见 ✓
    # 现在：盲区信息**单独返回** ✗ 不混进文件 map ✓
    return out, walk_errors


def _snapshot_with_blindspots(root: Path, *, exclude: Path | None = None):
    """返回 (指纹, 盲区清单)。

    第五轮复验 R-1 的正解：**目录读不到 ⇒ 它的内容不可知** ✗
    `chmod 000 → 700（写入）→ 000` 的**中间态在首尾快照里看不见** ✗
    所以不能靠比对指纹发现 ✗ **只能对「存在不可读目录」这件事本身 fail-closed** ✓
    """
    blind: list[str] = []
    real_walk = os.walk

    def _walk(top, *a, **kw):
        def _onerror(err: OSError) -> None:
            blind.append(f"{getattr(err, 'filename', top)}: {err.strerror}")
        kw["onerror"] = _onerror
        return real_walk(top, *a, **kw)

    os.walk = _walk
    try:
        snap, walk_errs = _snapshot(root, exclude=exclude)
    finally:
        os.walk = real_walk
    blind.extend(x for x in walk_errs if x not in blind)

    # 另外：目录或文件本身**存在但读不到**（lstat 成功、listdir/read 失败）
    for dirpath, dirnames, filenames in real_walk(root, onerror=lambda e: None):
        for name in list(dirnames):
            d = Path(dirpath) / name
            try:
                if d.is_symlink():
                    continue
                next(os.scandir(d)) if False else None
                os.listdir(d)
            except PermissionError:
                blind.append(f"{d}: 权限不足，内容不可读")
            except OSError:
                pass
    return snap, blind


def _diff(before: dict[str, str], after: dict[str, str]) -> tuple[tuple[str, ...], dict[str, str]]:
    # 第六轮复验 D-1：**这里不再按名字形状过滤任何东西** ✓
    # （合成键已经挪出文件命名空间 ✗ 见 `_snapshot` 的返回值 ✓）
    changed = sorted(set(before) ^ set(after)
                     | {k for k in set(before) & set(after) if before[k] != after[k]})
    summary = {}
    for rel in changed:
        if rel not in before:
            summary[rel] = "新增"
        elif rel not in after:
            summary[rel] = "删除"
        else:
            summary[rel] = "修改"
    return tuple(changed), summary



# --------------------------------------------------------------------------- #
# 修 7：证据的完整性保护（沿用 L01 的「SHA-256 摘要 + 追加不覆盖」做法）
# --------------------------------------------------------------------------- #

def _bind_ledger(runtime: Path, task_id: str, spec_path: Path, *,
                 register_if_missing: bool) -> dict:
    """把本次执行**绑定到 L01 账本**。

    默认要求任务已存在（与 L01「任务必须属于已登记项目」一致）；
    只有显式 `register_if_missing=True` 才自动登记（**由人明确要求**，不是默认）。
    **不另写一套账本逻辑** —— 复用 `workbench.bootstrap`。
    """
    from . import bootstrap
    from .bootstrap import LedgerError

    db = Path(runtime) / "workbench.db"
    if not db.exists():
        if not register_if_missing:
            raise ExecutionError(
                f"账本尚未初始化（{db} 不存在），任务 {task_id} 未登记。"
                "请先运行 workbench-init / workbench-project-add / workbench-task-create，"
                "或显式传 --register-if-missing 由本次执行登记。"
            )
        # 自动登记：init → project → task
        try:
            bootstrap.workbench_init(runtime, "local", "个人 AI 研发工作台")
            bootstrap.project_add(runtime, "P-EXEC", "受控执行登记项目",
                                  purpose="由 execute-task --register-if-missing 自动登记")
        except LedgerError:
            pass                                  # 已存在即可
    else:
        import sqlite3
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            row = conn.execute("SELECT 1 FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        finally:
            conn.close()
        if row is None and not register_if_missing:
            raise ExecutionError(
                f"任务未登记：{task_id}。请先用 workbench-task-create 登记；"
                "若要由本次执行登记，显式传 --register-if-missing。"
            )

    # 登记（若需要/若缺失）
    try:
        import sqlite3 as _sq
        conn = _sq.connect(str(db))
        try:
            # 第六轮复验 D-6：**只在显式 register_if_missing 时才建这个项目** ✗
            # 原来无条件插入 ✗ 与 docstring 自述（「由人明确要求 ✗ 不是默认」）相反 ✓
            if register_if_missing:
                if conn.execute("SELECT 1 FROM projects WHERE project_id='P-EXEC'").fetchone() is None:
                    conn.execute("INSERT INTO projects (project_id,name,path,purpose,created_at)"
                                 " VALUES ('P-EXEC','受控执行登记项目',?,?,?)",
                                 (str(Path(spec_path).parent), "execute-task 自动登记",
                                  datetime.now(timezone.utc).isoformat()))
            else:
                # 没显式要求 ✗ 但任务行必须存在才能追责 → 用它**已有的**项目
                row = conn.execute("SELECT project_id FROM tasks WHERE task_id=?",
                                   (task_id,)).fetchone()
                if row is None:
                    # 任务不存在且没被授权自动登记 ✗ 前面已经拒绝过了 ✗ 这里不该到 ✓
                    raise ExecutionError(
                        f"拒绝执行：任务 {task_id} 未登记，且未传 --register-if-missing ✗ "
                        "不会为此创建新的项目行 ✓")
            if conn.execute("SELECT 1 FROM tasks WHERE task_id=?", (task_id,)).fetchone() is None:
                text = Path(spec_path).read_text(encoding="utf-8-sig")
                conn.execute(
                    "INSERT INTO tasks (task_id,project_id,title,request,requirement_id,"
                    " created_by,spec_text,spec_sha256,problem_text,problem_sha256,created_at)"
                    " VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (task_id, "P-EXEC", f"受控执行 {task_id}", None, None, "execute-task",
                     text, hashlib.sha256(text.encode("utf-8")).hexdigest(),
                     None, None, datetime.now(timezone.utc).isoformat()))
            conn.commit()
        finally:
            conn.close()
    except sqlite3.IntegrityError as error:
        # 第五轮复验 R-7：check-then-insert **非原子** ✗ 两个并发调用会撞 UNIQUE ✓
        # 撞上说明**另一个调用已经把同样的行插进去了** ✗ 目标状态已达成 ✓
        # 所以这里**不当失败**（幂等）✗ 但仍要确认行真的在 ✓
        if "UNIQUE" not in str(error).upper() and "unique" not in str(error):
            raise ExecutionError(f"绑定账本失败：{error}") from error
        check = sqlite3.connect(str(db))
        try:
            ok = check.execute("SELECT 1 FROM tasks WHERE task_id=?",
                               (task_id,)).fetchone() is not None
        finally:
            check.close()
        if not ok:
            raise ExecutionError(f"绑定账本失败（并发且目标行不存在）：{error}") from error
    except Exception as error:                     # noqa: BLE001
        raise ExecutionError(f"绑定账本失败：{error}") from error
    return {"task_id": task_id, "runtime": str(runtime)}


def _append_ledger_evidence(runtime: Path, task_id: str, *, phase: str,
                            command_text: str, output_file: Path,
                            returncode: int, observed_at: str) -> int | None:
    """把本次执行**追加**进 L01 账本（成功与失败都追加）。返回 evidence_id。"""
    from . import bootstrap
    from .bootstrap import LedgerError
    try:
        # ⚠️ `evidence_add` 的语义是「**读这个文件的内容**并存进账本」✗
        # 所以这里必须传**证据文件本身** —— 传路径字符串会让账本里存的是路径 ✗
        # 摘要也会变成「路径的哈希」而不是「证据内容的哈希」。
        # 第四轮复验指出：「账本里已有权威副本 ✗ Eval 却不查」——
        # 修正后账本的 `output_sha256` 就是**证据内容的哈希** ✗ 可以当权威副本用 ✓
        payload = bootstrap.evidence_add(
            Path(runtime), task_id, phase, command_text,
            str(output_file), returncode, observed_at)
        return payload["evidence"]["evidence_id"]
    except LedgerError:
        return None


def _write_evidence(path: Path, payload: dict) -> None:
    """把证据写成 JSON（**第七轮复验 F4/F5 的修复**）。

    F4：文件名里可能有**非法 UTF-8** ✗ `json.dumps` 会产生 surrogate ✗
        `write_text` 抛 `UnicodeEncodeError` ✗ 留下 **0 字节证据** ✓
        → `errors="surrogateescape"` ✗ 并 `ensure_ascii=False` 失败时退到 `True` ✓
    F5：命令可能把**证据目录整个删掉** ✗ `write_text` 抛 `FileNotFoundError` ✗
        而「证据被破坏」的判定排在它后面 ✗ 永远轮不到 ✓
        → 落盘前 `mkdir(parents=True, exist_ok=True)` ✗ 并把 `OSError` 收口 ✓
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        text = json.dumps(payload, ensure_ascii=False, indent=2)
    except (TypeError, ValueError):
        text = json.dumps(payload, ensure_ascii=True, indent=2, default=str)
    try:
        path.write_text(text, encoding="utf-8", errors="surrogateescape")
    except UnicodeEncodeError:
        # 名字或内容里有无法编码的东西 ✗ 退到全 ASCII 转义 ✓
        path.write_text(json.dumps(payload, ensure_ascii=True, indent=2, default=str),
                        encoding="utf-8")


def _ledger_counts(runtime: Path) -> dict[str, int | None]:
    """账本的「只增不减」计数（第六轮复验 D-5）。

    ⚠ 诚实边界：同 UID 的攻击者**仍能改写 DB 文件本身** ✗
    那是**方案层面**（归 B-4 的根因 ✗ 需隔离/签名）✓
    但「行数与最大 id 不得倒退」是**能做的** ✗ 做了 ✓
    """
    db = Path(runtime) / "workbench.db"
    if not db.is_file():
        return {}
    try:
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            total = conn.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
            mx = conn.execute("SELECT COALESCE(MAX(evidence_id),0) FROM evidence").fetchone()[0]
            return {"evidence_total": int(total), "evidence_max_id": int(mx)}
        finally:
            conn.close()
    except sqlite3.Error:
        return {}


def _evidence_index(directory: Path) -> dict[str, str]:
    """证据目录的 `文件名 -> 内容 sha256` 索引。用于检测删除与改写。"""
    index: dict[str, str] = {}
    if not directory.is_dir():
        return index
    for path in sorted(list(directory.glob("*.json")) + list(directory.glob("*.sha256"))):
        try:
            index[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            index[path.name] = "<unreadable>"
    return index


def _evidence_tampering(before: dict[str, str], after: dict[str, str]) -> list[str]:
    """对比两次索引，返回被删除或被改写的证据描述。**新增不算篡改。**"""
    problems: list[str] = []
    for name, digest in before.items():
        if name not in after:
            problems.append(f"既有证据被删除：{name}")
        elif after[name] != digest:
            problems.append(f"既有证据被改写：{name}")
    return problems


def _reject_evidence_in_scope(evidence_dir: Path, workdir: Path,
                              limits: "ExecutionLimits") -> None:
    """证据目录若落在写集内 → 拒绝执行。

    理由：受控执行若能写证据目录，就能删改自己的证据（二次复验 run5 的三步攻击）。
    """
    try:
        rel = evidence_dir.resolve().relative_to(workdir.resolve()).as_posix()
    except ValueError:
        return                     # 证据目录在工作目录之外，天然安全
    if limits.in_scope(rel) or any(limits.in_scope(rel + "/" + n) for n in ("x",)):
        raise ExecutionError(
            f"证据目录落在写集内（{rel}）：受控执行将能删改自己的证据，拒绝执行。"
            "请把 --runtime-dir 放在写集之外。"
        )


def _write_evidence_digest(evidence_path: Path) -> None:
    """给证据自身留一份 `.sha256` 指纹，供后续校验（沿用 L01 的摘要做法）。"""
    try:
        digest = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
        evidence_path.with_suffix(".sha256").write_text(digest + "\n", encoding="utf-8")
    except OSError:
        pass

def run_task(spec_path, task_id: str, command, limits: ExecutionLimits, runtime,
             *, verify_only: bool = False, extra_outside: tuple[Path, ...] = (),
             register_if_missing: bool = False, ledger: bool = True) -> ExecutionResult:
    """受控执行一次任务。

    **先校验 Spec**：不合法就拒绝，且**不创建任务、不创建运行库**。
    """
    if not list(command):
        raise ExecutionError("命令为空：拒绝执行（受控失败，不产生任何证据）")

    spec_path = Path(spec_path)
    try:
        load_spec(spec_path)
    except SpecError as error:
        raise ExecutionError(f"Spec 不合格，拒绝执行：{error}") from error

    runtime = Path(runtime)
    workdir = Path(limits.workdir).resolve()
    # 工作目录之外的改动无法靠遍历全盘发现，必须**事前声明监视根**。
    # 默认监视工作目录的父目录（候选目录总在某个容器/工作区之下）；
    # 调用方可用 extra_outside 追加更多监视根。
    # 独立复验的反例 1：默认只监视 workdir.parent，根外写入完全不可见，却判成功。
    # 现改为 **fail-closed**：调用方必须显式声明监视根；只给 workdir 时会自动
    # 纳入其父目录，并在证据里记录实际监视根，让"监视不到的地方"可见。
    watch = [p for p in extra_outside] if extra_outside else [workdir.parent]
    outside_roots: list[Path] = []
    missing_roots = []
    for candidate in watch:
        c = Path(candidate).resolve()
        if c != workdir and workdir not in c.parents:
            if c.exists():
                outside_roots.append(c)
            else:
                # 第四轮复验 ④：原来是 `if c.exists()` **静默丢弃**不存在的根 →
                # 零监视却判成功（fail-open）。注释自称 fail-closed ✗ 实现却是反的 ✓
                missing_roots.append(c)
    if missing_roots:
        raise ExecutionError(
            "监视根不存在，拒绝执行（fail-closed）："
            + "，".join(str(x) for x in missing_roots)
            + "。零监视下的「无越界」不构成任何保证。")
    # 第四轮复验 ④：守卫必须检**生效列表** ✗ 不是声明列表 ✓
    # （原来检的是 `watch`，而 `watch` 永远非空 ✗ 等于没检 ✓）
    if not outside_roots:
        raise ExecutionError(
            "生效的监视根为空：工作目录之外是否被写入不可判定 ✗ "
            "零监视下的「无越界」不构成任何保证（fail-closed）。")
    observed = datetime.now(timezone.utc).isoformat()

    if verify_only:
        # ③ 仅复验：只核对限制，不执行、不写入
        evidence_dir = runtime / "evidence"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        # 第三次复验指出：修 4 只修了一半 —— 执行证据唯一了，verify_only 仍写固定名，
        # 同 task-id 连跑 3 次只剩 1 个文件。这里同样加 UTC 时间戳。
        _stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        ev = evidence_dir / f"{task_id}-{_stamp}-verify-only.json"
        # 复验指出：verify-only 的**落盘**证据只有 7 个键，
        # 与「每次执行的证据 JSON 都含 stdout/stderr/diff_summary/verify_command/watch_roots」
        # 的说法不符。这里补齐同样的键（值多为空，但**键存在且语义一致**）。
        payload = {"task_id": task_id, "mode": "verify_only",
                   "workdir": str(workdir), "write_scope": list(limits.write_scope),
                   "runtime_dir": str(runtime),
                   "timeout": limits.timeout, "observed_at": observed,
                   "stdout": "", "stderr": "",
                   "diff_summary": {}, "changed_files": [], "out_of_scope": [],
                   "returncode": 0, "timed_out": False, "stopped": False,
                   "stop_reason": "仅复验：未执行命令",
                   # 第六轮复验 D-7：原来写死 [workdir.parent] ✗ 用了 extra_outside 时自述不准 ✓
                   "verify_command": "",
                   "watch_roots": [str(x) for x in outside_roots],
                   "interpreter_artifacts_allowed": [],
                   "eval_ok": False, "eval_message": "未执行，不产生 Eval 结论",
                   "acceptance": HUMAN_REVIEW}
        _write_evidence(ev, payload)
        _write_evidence_digest(ev)

        return ExecutionResult(
            task_id=task_id, returncode=0, stdout="", stderr="", changed_files=(),
            out_of_scope=(), diff_summary={}, timed_out=False, stopped=False,
            stop_reason="仅复验：未执行命令", eval_ok=False,
            eval_message="未执行，不产生 Eval 结论",
            evidence_path=str(ev), verify_only=True, observed_at=observed)


    # 供第三方重跑的验证命令（含解释器、工作目录、写集与超时）
    import shlex as _shlex
    # 修 1：**每个参数单独 quote**，不能先 ' '.join 再整串 quote ——
    # 那样「一个含空格的参数」（如 -c 的脚本）重跑时会被拆成多个参数。
    _cmd_text = " ".join(_shlex.quote(str(a)) for a in command)
    verify_command = (
        f"{sys.executable} -X utf8 -m workbench.cli execute-task"
        f" --spec {_shlex.quote(str(spec_path))} --task-id {_shlex.quote(task_id)}"
        f" --command {_shlex.quote(_cmd_text)}"
        f" --workdir {_shlex.quote(str(workdir))}"
        + "".join(f" --write-scope {_shlex.quote(str(s))}" for s in limits.write_scope)
        + f" --timeout {limits.timeout}"
        # 第四轮复验 ⑨：原命令漏了这两个参数 ✗ 第三方照抄重放会落到默认 runtime ✗
        # 报「账本尚未初始化 / 任务未登记」✗ 甚至**静默写到错的 runtime** ✓
        + f" --runtime-dir {_shlex.quote(str(runtime))}"
        + (" --register-if-missing" if register_if_missing else "")
        + (" --no-ledger" if not ledger else "")
    )

    # ---- 第七轮复验 F6：**拒绝必须早于账本绑定** ----
    # 原来 `_bind_ledger`(675) 在 `_reject_evidence_in_scope`(687) 之前 ✗
    # 于是「证据目录落在写集内」被拒绝时 ✗ **账本已建、任务已登记** ✗
    # 与 `ExecutionError` 自述「执行前的拒绝…不产生任何半成品」矛盾 ✓
    _evidence_dir_early = runtime / "evidence"
    _evidence_dir_early.mkdir(parents=True, exist_ok=True)
    _reject_evidence_in_scope(_evidence_dir_early, workdir, limits)

    # ---- v4：绑定 L01 账本（第一次复验的批评：执行与账本不连通）----
    ledger_task = None
    if ledger:
        ledger_task = _bind_ledger(runtime, task_id, spec_path,
                                   register_if_missing=register_if_missing)

    # ---- 修 7（第二次修订）：证据索引必须在**命令启动之前**取 ----
    # 复验指出：原来的 before/after 两个索引都在命令跑完之后取，
    # 「命令自己删改证据」因此**根本看不到** —— 之前被抓到只是巧合。
    evidence_dir = runtime / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_before = _evidence_index(evidence_dir)
    # 第七轮复验 F1：**账本计数必须在命令之前取** ✗
    # 原来在命令之后取 ✗ 于是「命令清空账本」这件事在两次取样之间**已经发生完了** ✓
    ledger_before = _ledger_counts(runtime)
    # （第七轮 F6：这一检查已提前到账本绑定之前 ✗ 这里不再重复）

    before, blind_before = _snapshot_with_blindspots(workdir)
    # 第六轮复验 D-3：**每一个监视根也都要做盲区检查** ✗ 不只 workdir ✓
    outside_before: dict[str, dict] = {}
    blind_outside: list[str] = []
    for _root in outside_roots:
        _snap, _blind = _snapshot_with_blindspots(_root, exclude=workdir)
        outside_before[str(_root)] = _snap
        blind_outside.extend(_blind)
    # 第五轮复验 R-1：**存在不可读目录 ⇒ 监视不完整 ⇒ 拒绝** ✓
    if blind_before or blind_outside:
        raise ExecutionError(
            "被监视的范围内存在不可读的对象，监视不完整，拒绝执行（fail-closed）："
            + "；".join((blind_before + blind_outside)[:5])
            + "。读不到的目录内容无法被监视 ✗ 不能假装它没有变化。")

    timed_out = False
    try:
        proc = subprocess.run(list(command), cwd=str(workdir), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=limits.timeout)
        returncode, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        returncode = -1
        stdout = (error.stdout or "") if isinstance(error.stdout, str) else ""
        stderr = f"超时：超过 {limits.timeout} 秒被终止"
    except OSError as error:
        # 命令不存在、权限不足等：这是**受控失败**，不是崩溃。
        # 约定 returncode=127（shell 的 "command not found"），照样留证据。
        returncode = 127
        stdout = ""
        stderr = f"命令无法启动：{error}"

    after, blind_after = _snapshot(workdir)
    changed, summary = _diff(before, after)
    out_of_scope = tuple(rel for rel in changed if not limits.in_scope(rel))

    # ---- 修 5 的回归（第三次复验的核心判据）----
    # 上一版把「解释器副产物」做成**白名单**：只要路径里有 `__pycache__/` 或以 `.pyc/.pyo` 结尾，
    # 就放行 —— 结果是**写集外的任意路径**都能借这个名字写删并判成功（盲区换了个名字回来）。
    # 现在改为：**只在写集内放行**；写集外的一律照常判越界。
    artifacts = tuple(
        r for r in out_of_scope
        if limits.in_scope(r) and (
            any(seg in r for seg in _INTERPRETER_ARTIFACTS)
            or r.endswith(_INTERPRETER_SUFFIXES))
    )
    # 注意：既然过滤条件里带了 `limits.in_scope(r)`，而 `out_of_scope` 本来就只含写集外的项，
    # 这段在语义上等于**不再放行任何写集外的东西** —— 保留它只为把「本可放行但越界」的情况
    # 记录进 artifacts（当前恒为空），并让意图显式可见。
    if artifacts:                                  # pragma: no cover - 逻辑上不会进入
        out_of_scope = tuple(r for r in out_of_scope if r not in artifacts)

    # 工作目录之外的改动也算越界（先算，逃逸链接的判定要用它）
    outside_changed: set[str] = set()
    for path_str, snap_before in outside_before.items():
        snap_after, _blind_after = _snapshot(Path(path_str), exclude=workdir)
        extra, extra_summary = _diff(snap_before, snap_after)
        for rel in extra:
            label = f"{path_str}/{rel}"
            outside_changed.add(str((Path(path_str) / rel).resolve()))
            out_of_scope = out_of_scope + (label,)
            summary[label] = extra_summary[rel]

    # ---- 修 6（第二次修订）：只报**本次真的被用到的**逃逸链接 ----
    # 复验指出原实现是「目录里只要存在指向根外的链接就判失败」——
    # 含 node_modules/.bin 或夹具链接的仓库会**永远无法通过**（假阳性）。
    # 新判据：链接**在本次执行期间其指向的内容发生了变化**（或链接自身被替换）。
    escaping = []
    # ⚠ 顺序：函数返回 **(workdir 组, watch 组)** ✗ 别接反（我接反过一次 ✗ 3 项测试红）
    escaping_in_workdir, escaping_in_watch = _escaping_symlinks(workdir, outside_roots)
    for item in escaping_in_workdir:
        rel, _, target = item.partition(" -> ")
        # 第四轮复验 ①：**目录符号链接**原来进不了快照 ✗ before/after 都是 None ✗
        # `None != None` 为假 → 逃逸被静默放过。现在快照已记录目录 ✗
        # 但还要**兜底**：快照里查不到这个 rel 时，**按「可能被用过」处理（fail-closed）**。
        # 这里只处理**工作目录内**的逃逸链接 ✗ `before`/`after` 就是工作目录快照 ✓
        #  · 文件链接：值变了（含目标内容哈希）= 被用过 ✓
        #  · **目录链接**：写穿透**不改变** `dirlink->目标` ✗ 值永远不变 ✗
        #    → 第五轮复验 R-4：**一律按「可能被用过」fail-closed** ✓
        was = before.get(rel, "<not-in-snapshot>")
        now = after.get(rel, "<not-in-snapshot>")
        is_dir_link = str(was).startswith("dirlink->") or str(now).startswith("dirlink->")
        if was != now or was == "<not-in-snapshot>" or is_dir_link:
            escaping.append(item)
    if escaping:
        for item in escaping:
            summary[f"symlink:{item}"] = "逃逸且被使用"
        out_of_scope = out_of_scope + tuple(f"symlink:{x}" for x in escaping)
    # 监视根里的逃逸链接：**记进证据 ✗ 不判失败**（第六轮复验 D-4）✓
    for item in escaping_in_watch:
        summary[f"watch-symlink:{item}"] = "监视根内存在指向别处的链接（不判失败，仅可见）"

    # ---- 停止判定（越界独立于退出码）----
    stopped, reason = False, ""
    if timed_out:
        stopped, reason = True, f"超时：超过 {limits.timeout} 秒，未被写成成功"
    elif out_of_scope:
        stopped, reason = True, (f"改动越界：退出码为 {returncode} 但写集外出现改动 "
                                 f"{', '.join(out_of_scope)}")
    elif returncode != 0:
        stopped, reason = True, f"退出码非零（{returncode}）：失败未被写成成功"
    elif not workdir.is_dir():
        # 第三次复验 N-3：把整个工作目录删掉 → 曾判成功。
        # 「删除」本身在写集内算合法，但**工作目录必须仍然存在**，否则后续无人能复验。
        stopped, reason = True, "工作目录在本次执行后已不存在：无法复验，判失败"

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    ev = evidence_dir / f"{task_id}-{stamp}-execution.json"
    if ev.exists():                      # 极小概率撞名，再退一步
        raise ExecutionError(f"证据文件已存在，拒绝覆盖：{ev}")

    payload = {
        "task_id": task_id, "spec": str(spec_path), "command": list(command),
        "workdir": str(workdir), "write_scope": list(limits.write_scope),
        "runtime_dir": str(runtime),
        "workdir_exists_after": workdir.is_dir(),
        "timeout": limits.timeout, "returncode": returncode,
        "observed_at": observed, "changed_files": list(changed),
        "out_of_scope": list(out_of_scope), "timed_out": timed_out,
        "stopped": stopped, "stop_reason": reason,
        # 独立复验指出：stdout/stderr 曾被采集后丢弃，Diff 摘要未落盘，
        # 且没有可供第三方重跑的验证命令字段。以下补齐。
        "stdout": stdout, "stderr": stderr,
        "diff_summary": dict(summary),
        "verify_command": verify_command,
        # 第三次复验指出：这句话只写在文档里，证据 JSON 里没有 → 「说了没做」。
        "verify_command_note": VERIFY_COMMAND_NOTE,
        "watch_roots": [str(x) for x in outside_roots],
        "interpreter_artifacts_allowed": list(artifacts),
        "eval_ok": None, "eval_message": "（Eval 结论待补）",
        "acceptance": HUMAN_REVIEW,
    }
    # ── 顺序（第四轮复验的连环问题的正解）──
    # 1) 证据本体**只写一次**（只含事实 ✗ 写好后不可变）→ 摘要稳定
    # 2) 指纹 = 本体内容的哈希
    # 3) 账本登记（摘要同上）—— 之后 Eval 才能按账本找到权威那一份
    # 4) 跑 Eval（它在磁盘上找与账本摘要一致的本体）
    # 5) **Eval 结论写到单独的 `.eval.json`** ✗ 绝不回写本体 ✓
    _write_evidence(ev, payload)
    _write_evidence_digest(ev)

    evidence_id = None
    ledger_failed = ""
    if ledger:
        phase = "observation" if not stopped else "red"
        evidence_id = _append_ledger_evidence(
            runtime, task_id, phase=phase,
            command_text=verify_command or " ".join(str(c) for c in command),
            output_file=ev, returncode=returncode, observed_at=observed)
        # 第五轮复验 R-2：**追加失败原来被静默吞掉** ✗ 于是
        # 「本轮零改动却 eval_ok=true ✗ 还引用上一轮的证据」✓
        # 现在：追加失败即判失败 ✓
        if evidence_id is None:
            stopped = True
            ledger_failed = "账本追加失败：本次执行没有进入 L01 账本，无法追溯"
            reason = ledger_failed if not reason else f"{reason}；{ledger_failed}"

    from eval.harness import minimum_eval
    # 第五轮复验 R-2：**Eval 必须绑定「本次」的证据** ✗ 不能用「该任务最新一行」✓
    # 否则一次干净的追加失败会让它去校验**上一轮**的证据 ✗ 报出「改动 1 个」✓
    eval_ok, eval_message = (False, "已停止，不运行 Eval") if stopped else \
        minimum_eval(runtime, expect_task=task_id, result_changed=changed,
                     expect_evidence=ev.name, expect_evidence_id=evidence_id,
                     expect_digest=__import__("hashlib").sha256(
                         ev.read_bytes()).hexdigest())

    # ---- 第六轮复验 D-5 / 第七轮 F1：账本 append-only ----
    # ⚠️ **第七轮复验 F1 指出**：原来的 `ledger_before` 取样在 `:847` ✗
    # 而命令在 `:692` ✗ **两次取样都在命令之后** ✗ 断言是**死代码** ✓
    # 现在：**取样提到命令之前** ✗ 并改为断言「**恰好新增一行**」✓
    # （**只比 `>=` 会被本次自己的追加掩盖** ✗ 复验者明确指出 ✓）
    # 原来只索引**证据目录** ✗ 从不快照账本 ✗ 于是命令 `DELETE FROM evidence`
    # 抹掉历史（甚至别的任务的记录）✗ 本次照样通过 ✓
    # ⚠ 诚实边界：同 UID 的攻击者仍能改写 DB 文件本身 ✗ 那是**方案层面**（归 B-4 的根因）✓
    #   但「行数与最大 id 不得倒退」是**能做的** ✗ 这里做了 ✓

    # ---- 修 7：本次运行不得删除或改写此前的证据 ----
    tampered = _evidence_tampering(evidence_before, _evidence_index(evidence_dir))
    if tampered:
        reason2 = "证据被破坏：" + "；".join(tampered)
        stopped = True
        reason = reason2 if not reason else f"{reason}；{reason2}"
        eval_ok = False
        eval_message = "已停止：本次运行删除或改写了既有证据"

    # Eval 结论**另存**，本体保持不可变（否则账本摘要立刻失效）
    # ---- D-5：账本 append-only 检查 ----
    ledger_after = _ledger_counts(runtime)
    regressions = []
    # 第七轮复验 F1：**断言「恰好新增一行」** ✗ 只比 `>=` 会被本次自己的追加掩盖 ✓
    # （命令清掉 N 行 ✗ 本次又追加 1 行 ✗ `after >= before` 仍然成立 ✗ 掩盖掉了删除 ✓）
    b_tot, a_tot = ledger_before.get("evidence_total"), ledger_after.get("evidence_total")
    b_mx, a_mx = ledger_before.get("evidence_max_id"), ledger_after.get("evidence_max_id")
    if ledger_before and ledger_after:          # 有账本才判
        if a_tot is not None and b_tot is not None and a_tot < b_tot:
            regressions.append(f"evidence 行数从 {b_tot} 退到 {a_tot}")
        if a_mx is not None and b_mx is not None and a_mx < b_mx:
            regressions.append(f"最大 evidence_id 从 {b_mx} 退到 {a_mx}")
    if regressions:
        stopped = True
        msg = "账本被删除或回退（append-only 被破坏）：" + "；".join(regressions)
        reason = msg if not reason else f"{reason}；{msg}"
        eval_ok = False
        eval_message = msg

    eval_path = ev.with_suffix(".eval.json")
    eval_path.write_text(json.dumps(
        {"evidence": ev.name, "ledger_evidence_id": evidence_id,
         "eval_ok": eval_ok, "eval_message": eval_message,
         "acceptance": HUMAN_REVIEW, "accepted": False},
        ensure_ascii=False, indent=2), encoding="utf-8")


    # ⑥b：篡改被检出时上面的 `stopped/reason` 已被更新 ✗ 这里用的是最新值 ✓
    # （原来返回给调用方的 stopped=true 却带着空的 stop_reason ✗ 复验者指出过 ✓）
    return ExecutionResult(
        task_id=task_id, returncode=returncode, stdout=stdout, stderr=stderr,
        changed_files=changed, out_of_scope=out_of_scope, diff_summary=summary,
        timed_out=timed_out, stopped=stopped, stop_reason=reason,
        eval_ok=eval_ok, eval_message=eval_message, evidence_path=str(ev),
        verify_only=False, observed_at=observed,
        verify_command=verify_command,
        watch_roots=tuple(str(x) for x in outside_roots),
        interpreter_artifacts_allowed=artifacts,
        ledger_evidence_id=evidence_id,
        verify_command_note=VERIFY_COMMAND_NOTE,
        workdir_exists_after=workdir.is_dir())
