"""命令行入口：`python -m capstone <snapshot.json> [--expected codes.txt] [--out DIR]`"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .risk_check import (
    SnapshotError, load_snapshot, render_markdown, run_checks,
    HUMAN_REVIEW,
)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="capstone",
                                 description="每日持仓风控检查（只读）")
    ap.add_argument("snapshot", help="持仓快照 JSON")
    ap.add_argument("--expected", help="应有持仓清单（每行一个代码）✗ 用于漏项检测")
    ap.add_argument("--out", help="报告输出目录（默认只打到 stdout）")
    args = ap.parse_args(argv)

    try:
        snap = load_snapshot(args.snapshot)
    except SnapshotError as error:
        # **受控失败**：缺输入是 unknown ✗ 不是崩溃 ✗ 也不是通过。
        print(json.dumps({"error": str(error), "acceptance": HUMAN_REVIEW,
                          "accepted": False}, ensure_ascii=False, indent=2))
        return 2

    expected = None
    if args.expected:
        text = Path(args.expected).read_text(encoding="utf-8")
        expected = [ln.strip() for ln in text.splitlines() if ln.strip()]

    report = run_checks(snap, expected_codes=expected)
    md = render_markdown(report)

    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        stamp = snap["as_of"].replace("-", "")
        # **文件名唯一 ✗ 绝不覆盖**（L04 的教训）
        jpath, mpath = out / f"risk-{stamp}.json", out / f"risk-{stamp}.md"
        n = 1
        while jpath.exists() or mpath.exists():
            jpath = out / f"risk-{stamp}-{n}.json"
            mpath = out / f"risk-{stamp}-{n}.md"
            n += 1
        jpath.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        mpath.write_text(md, encoding="utf-8")
        print(json.dumps({"json": str(jpath), "md": str(mpath),
                          "counts": report["counts"],
                          "acceptance": report["acceptance"]}, ensure_ascii=False, indent=2))
    else:
        print(md)

    # **退出码语义**（借用 L06 的分级思路）：
    #   0 = 全部通过或仅 unknown；1 = 有 triggered（需人处置）
    return 1 if report["counts"]["triggered"] else 0


if __name__ == "__main__":
    sys.exit(main())
