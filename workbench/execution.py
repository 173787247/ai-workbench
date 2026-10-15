"""L04 Ticket A · 受控执行：能力信封 ✗ 写集 ✗ 超时 ✗ 输出/退出码/Diff。

⭐ 接口对齐参考实现（`~/GO/CodexFDE/workbench/execution.py` ✗ 697 行 ✗ **只读参考 ✗ 不复制源码**）：

    normalize_write_scope(values) -> list[str]
    validate_v0_authorization(mode, workspace_path, scopes, timeout)

⭐ 三条硬规矩（**手册点名**）：
  ① **仅复验模式不调用写入执行器**。
  ② ⭐ **执行退出码 0 但改动越界 ⇒ 拒绝**（**防止实现退化为一律拒绝**）。
  ③ ⭐ **超时或越界是"停止"✗ 不是"自动回滚"** —— 措辞与字段都按这个写。

⚠️⚠️ **写集检查的真实覆盖范围（必须照实读 ✗ 别读大）**：

```
✅ **覆盖**：**候选目录内部**——逐文件快照 ✗ 与写集比对 ✗
   命令退出码为 0 但改了写集之外的文件 ⇒ `out_of_scope` ⇒ 拒绝
❌ **不覆盖**：**候选目录之外的任何写入** ⇒ **完全没有检测** ✗ **零告警**
```

⇒ ⭐ **检测器不是边界。** 真正的边界要靠工作区权限（**本环境没有**）。
⇒ ⚠️ **这件事的经过**（**L04 两轮独立复验 ✗ 如实记**）：
  第一轮复验发现"候选目录之外的写入零告警"⇒ 我加了一个 `_snapshot_outside()`
  去扫候选的父目录 ⇒ **第二轮复验证明它只覆盖"父目录子树内 ✗ 深度 ≤ 2 ✗ 非 `.git`"**
  ✗ **6 类形状仍漏检** ✗ 而且**新引入假阳性**：别的进程改父目录下的文件 ⇒
  合法执行被拒 ✗ 罪名算错。
  ⇒ ⭐ **并且它在真实流程里当场发作过**：候选放在 `/tmp` 下时，
  检查支架自己写的证据文件被当成"越界"⇒ 一次**五用例全过**的复验被判成失败。
  ⇒ **处置：撤掉那个函数 ✗ 把口径照实写在这里**（**复验者建议的选项 (a)**）。
⇒ ⚠️ **这条口径要不要改成"只覆盖候选目录内部"并接受它 ✗ 是人的决定**（见 `lesson-04-submission/SUBMISSION.md`）。
"""
from __future__ import annotations

import difflib
import os
import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

# ── 与参考实现对齐的保护清单 ──
PROTECTED_PARTS = {".git", ".runtime", ".tmp", ".codex", "__pycache__"}
PROTECTED_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".pem", ".key", ".p12", ".pfx"}
MAX_DIFF_CHARS = 50_000
MAX_SNAPSHOT_BYTES = 1_000_000
TIMEOUT_MIN, TIMEOUT_MAX = 30, 3600
MODES = ("verify", "codex")


class ExecutionError(Exception):
    """执行层的明确失败。`code` 供程序判断。"""

    def __init__(self, message: str, code: str = "execution_error", exit_code: int = 2) -> None:
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code


def _is_sensitive_path(relative: str) -> bool:
    path = PurePosixPath(relative.lower())
    name = path.name
    return (
        name == ".env"
        or (name.startswith(".env.") and name != ".env.example")
        or path.suffix in PROTECTED_SUFFIXES
        or any(part in PROTECTED_PARTS for part in path.parts)
        or "secret" in name
        or "credential" in name
    )


def normalize_write_scope(values) -> list[str]:
    """返回**安全的工作区相对路径**（对齐参考实现的契约）。

    拒绝：空 ✗ `.` ✗ `*` ✗ 绝对路径 ✗ 含 `..` ✗ 含 `:` ✗ 含 `*` ✗ 受保护/敏感路径。
    """
    normalized: list[str] = []
    for raw in values or []:
        value = str(raw).strip().replace("\\", "/")
        if not value:
            continue
        path = PurePosixPath(value)
        parts = path.parts
        if (value in {".", "*"} or path.is_absolute() or ".." in parts
                or ":" in value or "*" in value):
            raise ExecutionError(f"写入范围必须是明确的工作区相对路径：{raw}",
                                 "write_scope_invalid")
        if _is_sensitive_path(value):
            raise ExecutionError(f"写入范围包含受保护路径：{raw}", "write_scope_protected")
        normalized.append(value)
    return normalized


def validate_v0_authorization(mode: str, workspace_path: str, scopes, timeout: int) -> Path:
    """校验能力信封（**对齐参考实现的契约**）✗ 返回解析后的候选绝对路径。"""
    if mode not in MODES:
        raise ExecutionError("执行模式必须是 verify 或 codex", "mode_invalid")
    if type(timeout) is not int or not TIMEOUT_MIN <= timeout <= TIMEOUT_MAX:
        raise ExecutionError(f"超时必须是 {TIMEOUT_MIN}..{TIMEOUT_MAX} 秒的整数", "timeout_invalid")
    if not workspace_path:
        raise ExecutionError("必须指定候选目录", "candidate_required")
    ws = Path(workspace_path)
    if not ws.is_absolute() or not ws.is_dir():
        raise ExecutionError(f"候选必须是存在的绝对目录：{workspace_path}", "candidate_invalid")
    ws = ws.resolve()
    if mode == "codex":
        if not isinstance(scopes, list) or any(not isinstance(v, str) for v in scopes):
            raise ExecutionError("逐文件允许清单必须是路径数组", "write_scope_invalid")
        controller = Path(__file__).resolve().parents[1]
        if ws == controller or controller.is_relative_to(ws):
            raise ExecutionError(
                "编码必须使用隔离候选目录 ✗ 不能直接修改工作台源仓库", "candidate_is_controller")
    return ws


@dataclass(frozen=True)
class Envelope:
    """能力信封（**辅导资料 §2 的五件**）。"""
    mode: str
    candidate: Path
    write_scope: list[str]
    timeout: int


def build_envelope(*, mode: str, candidate: str, write_scope, timeout: int) -> Envelope:
    scope = normalize_write_scope(write_scope)
    ws = validate_v0_authorization(mode, candidate, scope, timeout)
    return Envelope(mode=mode, candidate=ws, write_scope=scope, timeout=timeout)


def _snapshot(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts:
            continue
        try:
            if p.stat().st_size > MAX_SNAPSHOT_BYTES:
                out[str(p.relative_to(root))] = f"<too large: {p.stat().st_size} bytes>"
                continue
            out[str(p.relative_to(root))] = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            out[str(p.relative_to(root))] = "<unreadable>"
    return out


def _diff(before: dict[str, str], after: dict[str, str]) -> str:
    lines: list[str] = []
    for name in sorted(set(before) | set(after)):
        b, a = before.get(name), after.get(name)
        if b == a:
            continue
        if b is None:
            lines.append(f"+++ 新增 {name}")
        elif a is None:
            lines.append(f"--- 删除 {name}")
        else:
            lines.extend(difflib.unified_diff(b.splitlines(), a.splitlines(),
                                              fromfile=f"a/{name}", tofile=f"b/{name}",
                                              lineterm=""))
    blob = "\n".join(lines)
    return blob[:MAX_DIFF_CHARS] + ("\n…（截断）" if len(blob) > MAX_DIFF_CHARS else "")


def _in_scope(name: str, allow: list[str]) -> bool:
    if not allow:
        return False                     # **没给写集 ⇒ 什么都不许改（不是"全都许"）**
    for pat in allow:
        pat = pat.rstrip("/")
        if name == pat or name.startswith(pat + "/"):
            return True
    return False


def run_candidate(*, envelope: Envelope, command: str | None = None) -> dict:
    """在候选目录跑一次受控执行 ✗ 返回**真实结果**（不改成功与否的表述）。"""
    cand = envelope.candidate
    before = _snapshot(cand)

    if envelope.mode == "verify":
        return {"ok": True, "mode": "verify_only", "candidate": str(cand),
                # ⚠️ 复验者 R6：**没有跑任何命令** ⇒ returncode 记 None ✗ 不记 0
                #    （记 0 会被误读成"跑过并通过"）
                "returncode": None, "command_executed": False,
                "stdout": "", "stderr": "", "diff": "",
                "changed": [], "out_of_scope": [], "timed_out": False,
                "rolled_back": False,
                "stop_semantics": "仅复验，未执行任何写入",
                "note": "仅复验模式：未调用写入执行器"}

    if not envelope.write_scope:
        raise ExecutionError("缺写集：真实执行必须先声明允许修改的文件", "write_scope_required")
    if not command:
        raise ExecutionError("允许写入模式必须给命令", "exec_required")

    argv = shlex.split(command)
    started = time.monotonic()
    timed_out = False
    try:
        proc = subprocess.run(argv, cwd=cand, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=envelope.timeout,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        rc, out, err = proc.returncode, proc.stdout or "", proc.stderr or ""
    except FileNotFoundError as error:
        # ⭐ 复验者 R5：命令不存在也要**留下证据** ✗ 不能抛 traceback 完事
        raise ExecutionError(f"命令不存在：{argv[0] if argv else command}（{error}）",
                             "command_not_found") from error
    except subprocess.TimeoutExpired as error:
        # ⭐ **停止** ✗ 不是回滚。已发生的改动留在原地 ✗ 如实报告。
        timed_out, rc = True, None
        out = error.stdout if isinstance(error.stdout, str) else ""
        err = error.stderr if isinstance(error.stderr, str) else ""
    elapsed = round(time.monotonic() - started, 3)

    after = _snapshot(cand)
    changed = sorted({n for n in set(before) | set(after) if before.get(n) != after.get(n)})
    out_of_scope = [n for n in changed if not _in_scope(n, envelope.write_scope)]
    diff = _diff(before, after)

    result = {"ok": False, "mode": "codex", "candidate": str(cand),
              "returncode": rc, "stdout": out[-4000:], "stderr": err[-4000:],
              "diff": diff, "changed": changed, "out_of_scope": out_of_scope,
              "timed_out": timed_out, "elapsed_sec": elapsed,
              "write_scope": list(envelope.write_scope), "timeout": envelope.timeout,
              # ⭐ 「不把停止误写成自动回滚」⇒ 显式声明：**不回滚 ✗ 改动留在原地**
              "rolled_back": False,
              "stop_semantics": "停止执行并保留证据；不自动回滚"}

    if timed_out:
        result["error_code"] = "timeout"
        result["note"] = "命令超时 ⇒ **已停止**；已发生的改动保留在原地 ✗ 未自动回滚"
        return result
    if out_of_scope:
        result["error_code"] = "out_of_scope"
        result["note"] = (f"命令退出码 {rc} ✗ 但改动越出写集：{out_of_scope} ⇒ **拒绝**"
                          "（**退出码 0 不构成范围内**）")
        return result
    if rc != 0:
        result["error_code"] = "command_failed"
        result["note"] = f"命令退出码 {rc} ⇒ **失败如实保存 ✗ 不写成成功**"
        return result

    result["ok"] = True
    result["note"] = "范围内执行成功；**自动检查通过仍等待人工复核**"
    return result
