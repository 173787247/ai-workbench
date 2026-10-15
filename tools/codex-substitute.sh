#!/usr/bin/env bash
# 壳：把工作台要调的 `codex` 换成**本人授权的替代执行器**（⚠️ 不是 Codex）。
# ⚠️ 本文件写死了本机路径 ⇒ **是本机脚本 ✗ 不进公开仓** ✓
set -u
PY="${DSH_WORKBENCH_PYTHON:-$HOME/GO/CodexFDE/.venv/bin/python}"
IMPL="${DSH_CODEX_SUBSTITUTE:-$HOME/GO/learning/CodexFDE/tools/codex-substitute.py}"
[ -x "$PY" ] || { echo "找不到课程解释器：$PY" >&2; exit 127; }
[ -f "$IMPL" ] || { echo "找不到替代执行器：$IMPL" >&2; exit 127; }
exec "$PY" -B -X utf8 "$IMPL" "$@"
