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

⭐ **它实现的接口**（来自 `~/GO/CodexFDE/workbench/execution.py:219-223` ✗ 只读参考）：

```
argv:  <executable> exec <headless_options…> --json --sandbox workspace-write --ephemeral
                    --output-schema <schema.json> --output-last-message <final.json>
                    --cd <workspace> -
stdin: prompt 全文
必须做:
  ① 在 `--cd` 指的目录里完成工作
  ② 把结果按 `--output-schema` 写成 JSON 到 `--output-last-message`
     （schema: {summary, tests[], risks[], next_step} ✗ 全是 required ✗ additionalProperties=false）
  ③ 往 stdout 写 `--json` 事件行 ✗ 其中 `file_change` 事件带 path/kind/status
     （工作台从 `execution.py:573-602` 解析它们 ✗ 用来核对"实际改了什么"）
```

⚠️ **本文件只懂 L05 那一个缺口**（幂等分支被 `if False and` 短路）✗
**不是通用编码代理** ✗ 遇到不认识的仓库状态**会停下不动手** ✓
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ── L05 的修复内容（与 tools/codex-substitute-l05.py 同一处 ✗ 保持一份真源）──
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
                # ⭐ 同一入库键重放：不再写账 ✗ 不增库存 ✗ 返回原来的那条流水。
                #    只有同一个 event_key 才走这里 ⇒ **新编号 B 仍然正常入账**。
                row = conn.execute(
                    "SELECT p.*,s.on_hand,s.reserved,(s.on_hand-s.reserved) AS available "
                    "FROM products p JOIN stock s USING(sku) WHERE p.sku=?", (sku,)
                ).fetchone()
                result = dict(row)
                result["idempotent_replay"] = True
                return result
"""


def _emit(event: dict) -> None:
    """按 `--json` 的约定往 stdout 写一行事件。"""
    print(json.dumps(event, ensure_ascii=False), flush=True)


def _apply(workspace: Path) -> dict:
    target = workspace / "flowerp" / "service.py"
    if not target.is_file():
        raise SystemExit(f"写集内的文件不存在：{target}")
    text = target.read_text(encoding="utf-8")
    if "if exists:" in text and "if False and exists:" not in text:
        return {"changed": False, "reason": "幂等分支已经是恢复状态"}
    if BROKEN not in text:
        raise SystemExit("找不到要修的片段 ✗ 候选与预期不符 ✗ 停下不动手")
    target.write_text(text.replace(BROKEN, FIXED, 1), encoding="utf-8")
    return {"changed": True}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # ⚠️ 字典序解析：只挑我们要的三个 ✗ 其余（headless_options / --sandbox …）原样忽略
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("positional", nargs="*")
    parser.add_argument("--output-schema", dest="schema")
    parser.add_argument("--output-last-message", dest="result")
    parser.add_argument("--cd", dest="cd")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--sandbox")
    parser.add_argument("--ephemeral", action="store_true")
    args, _unknown = parser.parse_known_args(argv)

    prompt = sys.stdin.read() if not sys.stdin.isatty() else ""
    workspace = Path(args.cd or ".").resolve()

    _emit({"type": "thread.started", "thread_id": "substitute-local"})
    _emit({"type": "item.completed", "item": {
        "type": "reasoning",
        "text": "本机没有 Codex CLI；本次由本人授权的替代执行器完成（不是 Codex）"}})

    outcome = _apply(workspace)

    if outcome.get("changed"):
        _emit({"type": "item.completed", "item": {
            "type": "file_change", "path": "flowerp/service.py",
            "kind": "update", "status": "completed"}})

    final = {
        "summary": ("撤回 `if False and exists:` 短路，恢复幂等分支"
                    if outcome.get("changed") else
                    f"未改动：{outcome.get('reason')}"),
        "tests": ["未由本执行器运行；由工作台在候选里跑冻结的检查"],
        "risks": [
            "本次不是 Codex CLI 执行的，而是本人授权的替代执行器",
            "只覆盖顺序重放；并发、崩溃、同键异内容未验",
        ],
        "next_step": "由工作台运行冻结检查并交人复核；状态保持 pending_human_review",
    }

    if args.result:
        Path(args.result).write_text(json.dumps(final, ensure_ascii=False, indent=2),
                                     encoding="utf-8")
    # schema 存在则核对一眼自己的输出（**不满足就明确报错 ✗ 不硬塞**）
    if args.schema:
        schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
        required = set(schema.get("required", []))
        missing = required - set(final)
        if missing:
            raise SystemExit(f"输出缺少 schema 要求的字段：{sorted(missing)}")
    _emit({"type": "item.completed", "item": {"type": "message", "text": final["summary"]}})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
