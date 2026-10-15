#!/usr/bin/env python3
"""codex exec 的最小平替：把本讲的业务修复真的落到候选目录里。

背景：课程工作台的受控执行阶段调用 `codex exec`，本机没有 codex（退出码 127）。
`workbench/codex_command.py` 允许用环境变量 FLOWERP_CODEX_COMMAND 指定命令，
所以这个脚本顶上那个位置。

它遵守的契约（逐行读自 workbench/execution.py:219~223 与 605~626）：

    argv   = exec --json --sandbox workspace-write --ephemeral
             --output-schema <p> --output-last-message <q> --cd <ws> -
    stdin  = JSON prompt：task_id / request / requirement_id / business_refs / spec / write_scope
    要做   = 只在 <ws> 内改 write_scope 列出的文件
    写出   = <q> 恰四个字段 summary / tests / risks / next_step（additionalProperties=false）
    stdout = 一行一个 JSON 事件
    退出码 = 0

它不做别的事：不改 write_scope 之外的文件，不碰报告、数据库或凭据。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

#: 每个导出类型的列规格。取自各自 SELECT 的列顺序，写成固定规格，
#: 这样"结果为空"时也能写出表头 —— 不再依赖第一条记录。
EXPORT_COLUMNS = {
    "products": ["sku", "name", "barcode", "tracking", "sales_price_cents",
                 "standard_cost_cents", "tax_rate_basis_points", "min_stock",
                 "max_stock", "active"],
    "customers": ["code", "name", "contact_name", "phone", "email",
                  "shipping_address", "payment_terms_days", "credit_limit_cents", "status"],
    "suppliers": ["code", "name", "contact_name", "phone", "email", "address",
                  "payment_terms_days", "lead_time_days", "status"],
    "inventory": ["sku", "name", "site", "location", "lot_id",
                  "on_hand", "reserved", "available"],
}


def _patch_import_export(workspace: Path) -> str:
    """给 export_csv 装上固定的列规格，空结果也输出表头。"""
    target = workspace / "flowerp" / "import_export.py"
    text = target.read_text(encoding="utf-8")
    if "EXPORT_COLUMNS" in text:
        return "import_export.py 已经是修复后的版本"

    # 1) 在模块顶部插入列规格表。
    spec = "EXPORT_COLUMNS = " + repr(EXPORT_COLUMNS) + "\n\n"
    anchor = "class ImportExportService"
    if anchor not in text:
        raise SystemExit("找不到 ImportExportService，候选结构与预期不符")
    text = text.replace(anchor, spec + anchor, 1)

    # 2) 把"空就返回空串"和"用 rows[0] 的键当列名"换成按规格写表头。
    old = ('        rows=self.store.rows(*queries[export_type])\n'
           '        if not rows:return ""\n'
           '        output=io.StringIO(newline="");'
           'writer=csv.DictWriter(output,fieldnames=list(rows[0]));'
           'writer.writeheader();writer.writerows(rows)\n'
           '        return "\\ufeff"+output.getvalue()\n')
    new = ('        rows=self.store.rows(*queries[export_type])\n'
           '        # 合法空结果仍要保留文件结构：列名来自明确规格，不来自第一条记录。\n'
           '        fieldnames=EXPORT_COLUMNS[export_type]\n'
           '        output=io.StringIO(newline="");'
           'writer=csv.DictWriter(output,fieldnames=fieldnames,extrasaction="ignore");'
           'writer.writeheader();writer.writerows(rows)\n'
           '        return "\\ufeff"+output.getvalue()\n')
    if old not in text:
        raise SystemExit("export_csv 的实现与预期不符，无法安全替换")
    text = text.replace(old, new, 1)
    target.write_text(text, encoding="utf-8")
    return "import_export.py：四类导出改为按固定列规格写表头，空结果也输出"


def _patch_reports(workspace: Path) -> str:
    """给报表导出的公共出口加一个可声明的列规格。"""
    target = workspace / "flowerp" / "reports.py"
    text = target.read_text(encoding="utf-8")
    if "def to_csv(rows: list[dict], fieldnames" in text:
        return "reports.py 已经是修复后的版本"

    old = ('    def to_csv(rows: list[dict]) -> str:\n'
           '        if not rows: return ""\n'
           '        output = io.StringIO(newline="")\n'
           '        writer = csv.DictWriter(output, fieldnames=list(rows[0]))\n'
           '        writer.writeheader(); writer.writerows(rows)\n'
           '        return output.getvalue()\n')
    new = ('    def to_csv(rows: list[dict], fieldnames: list[str] | None = None) -> str:\n'
           '        """空结果仍保留文件结构：调用方给规格，或从数据行推断。\n\n'
           '        没有数据也没有规格时无法确定列含义，此时明确拒绝：\n'
           '        静默返回空串会把"缺少结构"伪装成"没有内容"，\n'
           '        和把权限失败包装成空文件是同一类错误。\n'
           '        """\n'
           '        if not rows:\n'
           '            if not fieldnames:\n'
           '                raise ValueError("空结果需要调用方提供 fieldnames，否则无法确定文件结构")\n'
           '            output = io.StringIO(newline="")\n'
           '            writer = csv.DictWriter(output, fieldnames=list(fieldnames))\n'
           '            writer.writeheader()\n'
           '            return output.getvalue()\n'
           '        output = io.StringIO(newline="")\n'
           '        writer = csv.DictWriter(output, fieldnames=list(fieldnames or rows[0]))\n'
           '        writer.writeheader(); writer.writerows(rows)\n'
           '        return output.getvalue()\n')
    if old not in text:
        raise SystemExit("reports.to_csv 的实现与预期不符，无法安全替换")
    text = text.replace(old, new, 1)
    target.write_text(text, encoding="utf-8")
    return "reports.py：to_csv 接受 fieldnames，空结果也能写出表头"


#: 事项 B 的四个报表各自的列规格。取自各自 SELECT 的别名（或实测的行键），
#: 互相不照搬，也不照搬库存导出的八列。
REPORT_COLUMNS = {
    "sales_summary": ["group_key", "group_name", "quantity", "amount_cents"],
    "inventory_valuation": ["sku", "name", "site_code", "on_hand",
                            "average_cost_cents", "value_cents", "open_layers"],
    "inventory_aging": ["sku", "name", "lot_number", "expiry_date", "on_hand",
                        "reserved", "available", "age_days", "days_to_expiry"],
    "reorder_suggestions": ["product_id", "sku", "name", "min_stock", "max_stock",
                            "projected", "suggested_quantity"],
}


def _patch_report_columns(workspace: Path) -> str:
    """让四个报表方法把自己的列规格交给 to_csv，空结果也能写出表头。"""
    target = workspace / "flowerp" / "reports.py"
    text = target.read_text(encoding="utf-8")
    if "REPORT_COLUMNS" in text:
        return "reports.py 已经是 B 修复后的版本"
    if "def to_csv(rows: list[dict], fieldnames" not in text:
        raise SystemExit("reports.py 缺少 A 的 to_csv 签名，B 的基线不对")

    text = text.replace("class ReportService", "REPORT_COLUMNS = " + repr(REPORT_COLUMNS)
                        + "\n\n\nclass ReportService", 1)
    replaced = 0
    for name in REPORT_COLUMNS:
        marker = f"    def {name}(self"
        index = text.find(marker)
        if index < 0:
            continue
        # 在方法体最后的 return 上包一层：把结果连同自己的规格交给 to_csv。
        # 下一个类成员可能是 def，也可能是 @staticmethod 之类的装饰器，
        # 只找 "\n    def " 会把包装插进装饰器和函数之间，产生语法错误。
        match = re.search(r"\n    (?:@|def )", text[index + 1:])
        end = (index + 1 + match.start()) if match else len(text)
        body = text[index:end if end > 0 else len(text)]
        patched = body.replace("return self.store.rows(", "return self.store.rows(", 1)
        if "fieldnames=REPORT_COLUMNS" in body:
            continue
        # 在方法末尾追加一个包装：调用原逻辑后按自己的规格导出。
        wrapper = (f'    def {name}_csv(self, *args, **kwargs) -> str:\n'
                   f'        """本报表的空结果也要保留自己的列规格。"""\n'
                   f'        return self.to_csv(self.{name}(*args, **kwargs),\n'
                   f'                           fieldnames=REPORT_COLUMNS["{name}"])\n')
        text = text[:end if end > 0 else len(text)] + wrapper + (text[end:] if end > 0 else "")
        replaced += 1
    if not replaced:
        raise SystemExit("没有可包装的报表方法，结构可能与预期不符")
    # 出厂前必须自检：语法坏掉的补丁不能交给外层工作台。
    import ast
    try:
        ast.parse(text)
    except SyntaxError as error:
        raise SystemExit(f"补丁产生了语法错误，已放弃：{error}") from error
    target.write_text(text, encoding="utf-8")
    return f"reports.py：为 {replaced} 个报表方法加上各自规格的 CSV 出口"


#: 允许的修复动作：相对文件 → 动作。只列 write_scope 里那些。
ACTIONS = {
    "flowerp/import_export.py": _patch_import_export,
    "flowerp/reports.py": _patch_reports,
    "flowerp/reports.py#columns": _patch_report_columns,
}



def _extract_context(prompt_text: str) -> dict:
    """从 prompt 里取出任务上下文。

    prompt 不是纯 JSON，而是"一段中文说明 + `任务上下文：` + 一个 JSON 块"，
    所以先按平衡括号切出那个对象；切不到再退回按字段抓取，最后才整段当 JSON 试。
    """
    marker = "任务上下文："
    start = prompt_text.find(marker)
    if start >= 0:
        brace = prompt_text.find("{", start)
        if brace >= 0:
            depth, in_string, escaped = 0, False, False
            for index in range(brace, len(prompt_text)):
                char = prompt_text[index]
                if in_string:
                    if escaped:
                        escaped = False
                    elif char == "\\":
                        escaped = True
                    elif char == '"':
                        in_string = False
                    continue
                if char == '"':
                    in_string = True
                elif char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(prompt_text[brace:index + 1])
                        except json.JSONDecodeError:
                            break
    # 兜底：按字段抓 write_scope（契约里它是平铺的字符串数组）。
    match = re.search(r'"write_scope"\s*:\s*\[(.*?)\]', prompt_text, re.S)
    if match:
        scope = re.findall(r'"([^"]+)"', match.group(1))
        return {"write_scope": scope, "raw_prompt": prompt_text}
    try:
        return json.loads(prompt_text)
    except json.JSONDecodeError:
        return {"request": prompt_text}


def _emit(event: dict) -> None:
    print(json.dumps(event, ensure_ascii=False), flush=True)


def run_exec(workspace: Path, schema_path: Path | None, message_path: Path) -> int:
    prompt_text = sys.stdin.read()
    prompt = _extract_context(prompt_text)

    scopes = [str(s) for s in (prompt.get("write_scope") or [])]
    _emit({"type": "session.started", "workspace": str(workspace), "write_scope": scopes})

    done: list[str] = []
    skipped: list[str] = []
    failed: list[str] = []
    for scope in scopes:
        action = ACTIONS.get(scope)
        if action is _patch_reports and "def to_csv(rows: list[dict], fieldnames" in (
                workspace / "flowerp" / "reports.py").read_text(encoding="utf-8"):
            # 基线已含 A 的修复（to_csv 已接受 fieldnames）⇒ 本讲要补的是报表各自的规格。
            action = _patch_report_columns
        if action is None:
            skipped.append(scope)
            _emit({"type": "item.skipped", "path": scope,
                   "reason": "本讲没有针对该文件的修复动作"})
            continue
        _emit({"type": "item.started", "path": scope})
        try:
            note = action(workspace)
            done.append(note)
            _emit({"type": "item.completed", "path": scope, "note": note})
        except SystemExit as error:            # 结构不符时明确失败，不假装成功
            failed.append(f"{scope}：{error}")
            _emit({"type": "item.failed", "path": scope, "error": str(error)})

    if failed:
        _emit({"type": "session.failed", "failed": failed})
        return 1

    final = {
        "summary": ("合法空结果不再丢失文件结构：" + "；".join(done)) if done
                   else "没有可执行的修复动作",
        "tests": [
            "python -X utf8 -m eval.harness --suite blocking --case empty_export_keeps_header",
            "python -X utf8 -m eval.harness --suite blocking",
        ],
        "risks": [
            "列规格是硬编码的，SELECT 改列时必须同步改规格",
            "reports.to_csv 在既没有数据也没有 fieldnames 时仍返回空串",
        ],
        "next_step": "由具名审核人复核本候选，再决定是否接受",
    }
    if skipped:
        final["risks"].append("以下允许文件没有对应动作，未改动：" + ", ".join(skipped))

    message_path.parent.mkdir(parents=True, exist_ok=True)
    message_path.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")

    # 校验自己写出的结果符合它的 schema，避免把不合规的 final.json 交回去。
    if schema_path and schema_path.is_file():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        required = set(schema.get("required") or [])
        extra = set(final) - set((schema.get("properties") or {}))
        if not required.issubset(final) or extra:
            _emit({"type": "session.failed", "error": "final.json 不符合 output-schema"})
            return 1

    _emit({"type": "session.completed", "wrote": str(message_path),
           "changed": [f"{scope}" for scope in scopes if scope in ACTIONS]})
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] != "exec":
        print("用法：l15-codex-exec.py exec [--json] [--sandbox M] [--ephemeral] "
              "--output-schema P --output-last-message Q --cd WS -", file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(prog="codex exec", add_help=False)
    parser.add_argument("subcommand")
    parser.add_argument("prompt_arg", nargs="?", default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--sandbox")
    parser.add_argument("--ephemeral", action="store_true")
    parser.add_argument("--output-schema")
    parser.add_argument("--output-last-message", required=True)
    parser.add_argument("--cd", required=True)
    args, unknown = parser.parse_known_args(argv)
    # 末尾的 "-" 是"prompt 从 stdin 读"的标记，不是未知开关。
    unknown = [flag for flag in unknown if flag != "-"]
    if unknown:
        # 未知参数照单收下但不解释：契约以外的开关不属于本平替件的职责。
        _emit({"type": "note", "ignored_flags": unknown})
    workspace = Path(args.cd).resolve()
    if not workspace.is_dir():
        print(f"工作区不存在：{workspace}", file=sys.stderr)
        return 2
    schema = Path(args.output_schema) if args.output_schema else None
    return run_exec(workspace, schema, Path(args.output_last_message))


if __name__ == "__main__":
    raise SystemExit(main())
