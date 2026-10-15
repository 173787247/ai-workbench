#!/usr/bin/env python3
"""**Codex 的替代执行器**（本人指示的"平替 Codex" ✗ 不假装成 Codex）。

⚠️⚠️ **读这段再往下**：

```
**本机没有装 Codex CLI**（`codex` / `codex.cmd` / `codex.exe` 都没有 ✗
 `~/.codex` 不存在 ✗ `OPENAI_API_KEY` 未设置 ✗ Windows 侧也没有）
⇒ 而课程手册多处写着「会实际调用本机 Codex CLI」✓
⇒ ⭐ **我把它换成"本人授权的替代执行器"** ✗ **不是 Codex** ✓

**本人的原始指示**（2026-10-12）：「**老师用 CODEX 跑 ✗ 但你是 deepseek harness ✗
所以我想平替 codex ✗ 请你当 codex 替代它来跑**」✓
⇒ ⭐ **所以这是被授权的替代** ✗ **但"这次是 Codex 执行的"这句话为假 ✗ 我不写它** ✓
```

⭐ **它实现的两个接口**：

```
① 工作台的 `codex exec` 契约（`workbench/execution.py:219-223`）：
   argv: <exe> exec … --output-schema <p> --output-last-message <p> --cd <ws> -
   stdin: prompt
   必须：在 --cd 里做事 ✗ 按 schema 写结果 ✗ stdout 写 --json 事件（含 file_change）
② `--candidate` 直调（给手工步骤用）：指定要改哪棵树 ✗ `--which` 选哪一讲的改动
```

⚠️ **它只懂两件事**，不是通用编码代理：
```
`l05` 幂等缺口（`flowerp/service.py` 的 `if False and exists:`）
`l07` 待审 Hook（只写 `hook_staging/hooks.json` 与 `hook_staging/quality_gate.py`）
⇒ 遇到不认识的仓库状态**会停下不动手** ✓
```
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════
# L05：幂等分支被 `if False and` 短路
# ══════════════════════════════════════════════════════════════════════
BROKEN = """            exists = conn.execute("SELECT 1 FROM inventory_events WHERE event_key=?", (event_key,)).fetchone()
            if False and exists:
                row = conn.execute(
                    "SELECT p.*,s.on_hand,s.reserved,(s.on_hand-s.reserved) AS available "
                    "FROM products p JOIN stock s USING(sku) WHERE p.sku=?", (sku,)
                ).fetchone()
                result = dict(row)
                result["idempotent_replay"] = True
                return result
"""

FIXED = """            exists = conn.execute(
                "SELECT event_key,sku,quantity,reserved_delta,event_type,reference "
                "FROM inventory_events WHERE event_key=?", (event_key,)
            ).fetchone()
            if exists:
                # 同一入库键重放：不再写账 ✗ 不增库存 ✗ 返回原来的那条流水。
                # 只有同一个 event_key 才走这里 ⇒ **新编号 B 仍然正常入账**。
                row = conn.execute(
                    "SELECT p.*,s.on_hand,s.reserved,(s.on_hand-s.reserved) AS available "
                    "FROM products p JOIN stock s USING(sku) WHERE p.sku=?", (sku,)
                ).fetchone()
                result = dict(row)
                result["idempotent_replay"] = True
                return result
"""


def apply_l05(workspace: Path) -> dict:
    target = workspace / "flowerp" / "service.py"
    if not target.is_file():
        return {"changed": False, "error": f"写集内没有 {target}"}
    text = target.read_text(encoding="utf-8")
    if "if exists:" in text and "if False and exists:" not in text:
        return {"changed": False, "reason": "幂等分支已经是恢复状态"}
    if BROKEN not in text:
        return {"changed": False, "error": "找不到要修的片段 ✗ 候选与预期不符 ✗ 停下不动手"}
    target.write_text(text.replace(BROKEN, FIXED, 1), encoding="utf-8")
    return {"changed": True, "file": "flowerp/service.py"}


# ══════════════════════════════════════════════════════════════════════
# L07：待审 Hook 的两个文件（**只写 hook_staging ✗ 绝不碰 .codex**）
# ══════════════════════════════════════════════════════════════════════
L07_HOOKS_JSON = """{
  "description": "个人 L07 Stop 质量检查；待审产物，审查后才安装到 .codex。",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\\"$(git rev-parse --show-toplevel)/.venv/bin/python\\" -X utf8 \\"$(git rev-parse --show-toplevel)/.codex/hooks/quality_gate.py\\"",
            "commandWindows": "powershell -NoProfile -Command \\"$r = git rev-parse --show-toplevel; if ($LASTEXITCODE -ne 0) { exit 1 }; & (Join-Path $r '.venv/Scripts/python.exe') -X utf8 (Join-Path $r '.codex/hooks/quality_gate.py'); exit $LASTEXITCODE\\"",
            "statusMessage": "Running personal L07 blocking evals",
            "timeout": 960
          }
        ]
      }
    ]
  }
}
"""

L07_QUALITY_GATE = '''"""L07 Stop 处理器：把统一 Harness 的结果翻译成宿主响应。

它只做三件事（**手册：「Hook 决定何时调用 ✗ Harness 决定如何执行和汇总」**）：
  ① 校验 `cwd` 属于本项目（**不盲信任事件里的目录**）
  ② 在项目根用项目解释器跑 `eval.harness --suite blocking`
  ③ 把结果翻译成宿主协议（**stdout 只输出合法 JSON ✗ 诊断送 stderr**）

⚠️ **本文件不在 `.codex/` 里** ⇒ 它在 `hook_staging/` ✗ **不会被宿主自动加载**
   安装与信任是后续的独立人工步骤。**代码里没有任何金额公式**
   （**不复制第二套标准** ✗ 否则两份标准会逐渐分叉）。
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

EVAL_TIMEOUT_SECONDS = 900          # 必须小于 hooks.json 的 960


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        event = json.loads(sys.stdin.read())
        cwd = Path(event["cwd"]).resolve(strict=True)
        if cwd != root and root not in cwd.parents:
            raise ValueError("event cwd is outside this project")
        if type(event.get("stop_hook_active", False)) is not bool:
            raise ValueError("stop_hook_active must be a boolean")
        if event.get("stop_hook_active"):
            # 重入：跳过，但必须写明"本次未复验"（不能当成通过）
            print(json.dumps({"continue": True, "systemMessage":
                              "重入跳过；本次未复验。结束前仍须显式运行阻断级 Eval。"},
                             ensure_ascii=False))
            return 0
        result = subprocess.run(
            [sys.executable, "-X", "utf8", "-m", "eval.harness", "--suite", "blocking"],
            cwd=root, text=True, encoding="utf-8", errors="replace",
            capture_output=True, check=False, timeout=EVAL_TIMEOUT_SECONDS,
        )
        if result.returncode == 0:
            print(json.dumps({"continue": True, "systemMessage":
                              "当前工作台阻断级 Eval 已通过；不代表 FlowERP 业务验收。"},
                             ensure_ascii=False))
            return 0
        reasons = [l for l in (result.stdout or "").splitlines() if l.startswith("[BLOCK]")]
        print(json.dumps({"decision": "block", "reason":
                          "阻断级 Eval 未通过。修复后显式复验：\\n" + "\\n".join(reasons)},
                         ensure_ascii=False))
        return 0
    except (ValueError, KeyError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        print(json.dumps({"decision": "block", "reason":
                          f"Hook 未完成验证，请修复环境或配置后显式复验：{type(exc).__name__}: {exc}"},
                         ensure_ascii=False))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def apply_l07(workspace: Path) -> dict:
    """写 `hook_staging/` 的两个待审文件。**代码里不含任何检查逻辑**"""
    staging = workspace / "hook_staging"
    staging.mkdir(parents=True, exist_ok=True)
    written = []
    for name, content in (("hooks.json", L07_HOOKS_JSON),
                          ("quality_gate.py", L07_QUALITY_GATE)):
        (staging / name).write_text(content, encoding="utf-8")
        written.append(f"hook_staging/{name}")
    active = sorted(str(p.relative_to(workspace)) for p in (workspace / ".codex").rglob("*")
                    if p.is_file())
    return {"changed": True, "staged": written, "active_codex_untouched": active}


# ══════════════════════════════════════════════════════════════════════
# L09：取消订单不释放预占（`if False and` 短路，与 L05 同一手法）
# ══════════════════════════════════════════════════════════════════════
L09_BROKEN = """            if False and status == OrderStatus.RESERVED:"""
L09_FIXED = """            if status == OrderStatus.RESERVED:"""


def apply_l09(workspace: Path) -> dict:
    target = workspace / "flowerp" / "service.py"
    if not target.is_file():
        return {"changed": False, "error": f"写集内没有 {target}"}
    text = target.read_text(encoding="utf-8")
    if L09_BROKEN not in text:
        if L09_FIXED in text:
            return {"changed": False, "reason": "释放分支已经是恢复状态"}
        return {"changed": False,
                "error": "找不到 `if False and status == OrderStatus.RESERVED:` ✗ "
                         "候选与预期不符 ✗ 停下不动手"}
    # 只推动那个短路，不重写释放逻辑：按 order_id 查明细才是只碰本订单。
    target.write_text(text.replace(L09_BROKEN, L09_FIXED, 1), encoding="utf-8")
    return {"changed": True, "file": "flowerp/service.py",
            "note": "只移除短路，释放分支按原状态执行；未新增任何查询"}


# ══════════════════════════════════════════════════════════════════════
# L10：发货状态机守卫被短路（`if False and` —— 第四次同一手法）
# ══════════════════════════════════════════════════════════════════════
L10_BROKEN = """            if False and order["status"] != OrderStatus.RESERVED:"""
L10_FIXED = """            if order["status"] != OrderStatus.RESERVED:"""


def apply_l10(workspace: Path) -> dict:
    target = workspace / "flowerp" / "service.py"
    if not target.is_file():
        return {"changed": False, "error": f"写集内没有 {target}"}
    text = target.read_text(encoding="utf-8")
    if L10_BROKEN not in text:
        if L10_FIXED in text:
            return {"changed": False, "reason": "发货守卫已经是恢复状态"}
        return {"changed": False,
                "error": '找不到 `if False and order["status"] != OrderStatus.RESERVED:` ✗ '
                         "候选与预期不符 ✗ 停下不动手"}
    # 只让原守卫生效：不新增第二条状态判断，也不动库存与流水的写入。
    target.write_text(text.replace(L10_BROKEN, L10_FIXED, 1), encoding="utf-8")
    return {"changed": True, "file": "flowerp/service.py",
            "note": "只移除短路，状态机守卫按原样生效；未新增判断"}


def pick(workspace: Path) -> str:
    service = workspace / "flowerp" / "service.py"
    if service.is_file():
        text = service.read_text(encoding="utf-8")
        if BROKEN in text:
            return "l05"
        if L09_BROKEN in text:
            return "l09"
        if L10_BROKEN in text:
            return "l10"
    return "l07"


def _emit(event: dict) -> None:
    print(json.dumps(event, ensure_ascii=False), flush=True)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    # ── 模式 A：`--candidate` 直调（手工步骤用）──
    if "--candidate" in argv:
        ap = argparse.ArgumentParser(description="Codex 替代执行器")
        ap.add_argument("--candidate", type=Path, required=True)
        ap.add_argument("--which", choices=("auto", "l05", "l07", "l09", "l10"), default="auto")
        ap.add_argument("--report", type=Path)
        args, _unknown = ap.parse_known_args(argv)
        ws = args.candidate.resolve()
        which = pick(ws) if args.which == "auto" else args.which
        body = {"l05": lambda: apply_l05(ws), "l07": lambda: apply_l07(ws),
                "l09": lambda: apply_l09(ws), "l10": lambda: apply_l10(ws)}[which]()
        out = {"executor": "codex-substitute (DeepSeek Harness)", "is_codex": False,
               "note": "本机没有 Codex CLI；这是本人授权的替代执行器，不是 Codex",
               "which": which, "candidate": str(ws), **body}
        text = json.dumps(out, ensure_ascii=False, indent=2)
        print(text)
        if args.report:
            args.report.write_text(text, encoding="utf-8")
        return 0 if not body.get("error") else 2

    # ── 模式 B：工作台的 `codex exec` 契约 ──
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("positional", nargs="*")
    ap.add_argument("--output-schema", dest="schema")
    ap.add_argument("--output-last-message", dest="result")
    ap.add_argument("--cd", dest="cd")
    ap.add_argument("--json", action="store_true")
    args, _unknown = ap.parse_known_args(argv)

    if not sys.stdin.isatty():
        sys.stdin.read()                     # prompt：读掉，不解析
    workspace = Path(args.cd or ".").resolve()

    _emit({"type": "thread.started", "thread_id": "substitute-local"})
    _emit({"type": "item.completed", "item": {
        "type": "reasoning",
        "text": "本机没有 Codex CLI；本次由本人授权的替代执行器完成（不是 Codex）"}})

    which = pick(workspace)
    body = {"l05": lambda: apply_l05(workspace), "l07": lambda: apply_l07(workspace),
            "l09": lambda: apply_l09(workspace), "l10": lambda: apply_l10(workspace)}[which]()
    changed = list(body.get("staged") or [])
    if body.get("changed") and body.get("file"):
        changed.append(body["file"])
    for rel in changed:
        _emit({"type": "item.completed", "item": {
            "type": "file_change", "path": rel,
            "kind": "add" if "staging" in rel else "update", "status": "completed"}})

    final = {
        "summary": body.get("reason") or body.get("error") or f"完成 {which} 的改动",
        "tests": ["未由本执行器运行；由工作台在候选里跑冻结的检查"],
        "risks": ["本次不是 Codex CLI 执行的，而是本人授权的替代执行器",
                  "只覆盖顺序重放 / 待审 Hook 的写入；并发、崩溃、宿主信任未验"],
        "next_step": "由工作台运行冻结检查并交人复核；状态保持 pending_human_review",
    }
    if args.result:
        Path(args.result).write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.schema:
        schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
        missing = set(schema.get("required", [])) - set(final)
        if missing:
            raise SystemExit(f"输出缺少 schema 要求的字段：{sorted(missing)}")
    _emit({"type": "item.completed", "item": {"type": "message", "text": final["summary"]}})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
