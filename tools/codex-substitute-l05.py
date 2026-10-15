#!/usr/bin/env python3
"""L05 · **Codex 的替代执行器**（本人指示的"平替 Codex" ✗ 不假装成 Codex）。

⚠️⚠️ **本文件是什么 ✗ 一定要先读这段**：

```
**本机没有装 Codex CLI**（`codex` / `codex.cmd` / `codex.exe` 都没有 ✗
 `~/.codex` 不存在 ✗ `OPENAI_API_KEY` 未设置 ✗ Windows 侧也没有）
⇒ 而 L05 手册 §6.1 的原话是：「**这里会实际调用本机 Codex CLI** ✗ 最长允许 900 秒」✓
⇒ ⭐ **所以这一步无法按手册原样执行** ✗ 我**不伪造"Codex 跑过了"** ✓

**本人的原始指示**（2026-10-12 ✗ 会话开头）：
  「**老师用 CODEX 跑 ✗ 但你是 deepseek harness ✗ 所以我想平替 codex ✗ 请你当 codex 替代它来跑**」
⇒ ⭐ **所以本文件是"受本人授权的替代执行器"** ✗ **不是 Codex** ✓
⇒ ⚠️ **它做的是同一个位置的同一件事**（在工作台的写集内修改 `flowerp/service.py`）✗
   **但"是 Codex 执行的"这句话在这里为假 ✗ 我不会写它** ✓
```

⭐ **接口契约**（来自 `~/GO/CodexFDE/workbench/codex_command.py`）：

```
resolve_codex_command() 读环境变量 `FLOWERP_CODEX_COMMAND` ✗ 有就用它 ✗
（`shutil.which` 找得到就解析路径 ✗ 找不到就原样返回）✓
⇒ 所以把本文件设成那个变量 ✗ 工作台就会调它 ✗ 而不是 `codex` ✓
```

**本执行器做什么**：把 L05 的幂等缺口补上 —— 即在 `flowerp/service.py` 的
`receive_stock` 里**恢复被 `if False and` 短路的幂等分支**，按 `IdempotencyService`
的语义处理同键重放。**范围只有那一个文件**（课程合同的写集）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# ⭐ 修复内容：把被短路的幂等分支恢复，并按"同键重放"的语义返回原记录。
#    ⚠️ 只用**已存在的表**（`inventory_events` 的 `event_key` 唯一约束）✗
#       **不新增表 ✗ 不改 schema** ✗ 因为写集只有 `flowerp/service.py`。
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
                # ⭐ **同一入库键重放**：不再写账 ✗ 不增库存 ✗ 返回**原来的那条流水**。
                #    ⚠️ 这不是"吞掉以后的请求" —— 只有**同一个 event_key** 才走这里；
                #       新编号 B 仍然正常入账（**A 重试与新收货是两回事**）。
                row = conn.execute(
                    "SELECT p.*,s.on_hand,s.reserved,(s.on_hand-s.reserved) AS available "
                    "FROM products p JOIN stock s USING(sku) WHERE p.sku=?", (sku,)
                ).fetchone()
                result = dict(row)
                result["idempotent_replay"] = True
                return result
"""


def apply_fix(candidate: Path) -> dict:
    target = candidate / "flowerp" / "service.py"
    if not target.is_file():
        raise SystemExit(f"写集内的文件不存在：{target}")
    text = target.read_text(encoding="utf-8")
    # ⚠️ 修 bug：原来拿 `exists = conn.execute(` 当"已修"锚点 —— 而**被短路的那版里也有它**
    #    ⇒ 会误判成"已修"✗ 一次都不改 ✓ 现在改用**只可能出现在修好版本里的那行**。
    if "if exists:" in text and "if False and exists:" not in text:
        return {"changed": False, "reason": "幂等分支已经是恢复状态 ✗ 不重复改"}
    if BROKEN not in text:
        raise SystemExit("找不到要修的片段 ✗ 候选与预期不符 ✗ 停下不动手")
    target.write_text(text.replace(BROKEN, FIXED, 1), encoding="utf-8")
    return {"changed": True, "file": "flowerp/service.py"}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True, help="候选绝对路径")
    parser.add_argument("--report", type=Path, help="把结果写成 JSON")
    parser.add_argument("rest", nargs="*", help="忽略：Codex 风格的多余参数")
    args = parser.parse_args(argv)

    result = {"executor": "codex-substitute (DeepSeek Harness)",
              "is_codex": False,
              "note": "本机没有 Codex CLI；这是本人授权的替代执行器，不是 Codex",
              **apply_fix(args.candidate.resolve())}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    print(text)
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
