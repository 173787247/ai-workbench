#!/usr/bin/env bash
# 冻结检查 —— **改代码时会立刻看到 ✗ 而不是靠人记住**。
#
# 为什么有这个脚本（`AGENTS.md` §四 的机制版）：
#   我在六轮复验里**四次**破坏了冻结：
#     ① 第一次复验：「复核期间工作树仍在被写」
#     ② 第二次：「哈希没同步 ✗ 验收对象再次不可识别」
#     ③ 第三次：「60 秒内 tests 改了 4 次」
#     ④ 第七轮：我在它跑的时候改了 candidate.py
#   **光写规则不管用** ✗ 所以做成可执行的检查 ✓
#
# 用法：
#   tools/check-freeze.sh            # 用最新的 版本冻结-vN.md
#   tools/check-freeze.sh v7         # 指定某个冻结声明
#   tools/check-freeze.sh --write    # 生成/更新冻结声明里的哈希块
set -uo pipefail
cd "$(dirname "$0")/.."

FILES=(workbench/execution.py workbench/cli.py eval/harness.py
       tests/test_l04_workbench_v0.py workbench/spec.py workbench/candidate.py)

if [[ "${1:-}" == "--write" ]]; then
  V="${2:-v8}"
  echo "把下面的哈希块写进 lesson-04-submission/版本冻结-$V.md："
  echo '```'
  for f in "${FILES[@]}"; do printf '%-40s %s\n' "$f" "$(sha256sum "$f" | cut -d' ' -f1)"; done
  echo '```'
  exit 0
fi

V="${1:-}"
if [[ -z "$V" ]]; then
  V="$(ls -1 lesson-04-submission/版本冻结-v*.md 2>/dev/null \
       | sed 's/.*-v\([0-9]*\)\.md/\1/' | sort -n | tail -1)"
  V="v$V"
fi
DOC="lesson-04-submission/版本冻结-$V.md"
[[ -f "$DOC" ]] || { echo "找不到 $DOC" >&2; exit 2; }

echo "冻结声明：$DOC"
echo
bad=0
for f in "${FILES[@]}"; do
  now="$(sha256sum "$f" | cut -d' ' -f1)"
  fro="$(grep -oE "$(basename "$f")[[:space:]]+[0-9a-f]{64}" "$DOC" | grep -oE '[0-9a-f]{64}' | head -1)"
  if [[ -z "$fro" ]]; then
    printf '  ⚠ %-38s 声明里没找到哈希\n' "$f"; bad=$((bad+1))
  elif [[ "$now" == "$fro" ]]; then
    printf '  ✓ %-38s 未变\n' "$f"
  else
    printf '  ✗ %-38s **变了**\n' "$f"
    printf '     冻结 %s\n     现在 %s\n' "${fro:0:24}…" "${now:0:24}…"
    bad=$((bad+1))
  fi
done
echo
if [[ "$bad" -gt 0 ]]; then
  cat <<'MSG'
⚠⚠ **被冻结的文件变过了。**

**如果现在有复验在跑 ✗ 它的结论对这些文件已经无效** ✓
**要做的**：
  1. 在**当前**冻结声明末尾如实记一句「冻结被破坏了 ✗ 时间 ✗ 改了哪个文件」
  2. `tools/check-freeze.sh --write v<N+1>` 生成新哈希 ✗ 声明 **v<N+1>**
  3. **等复验结束再改** ✗ 或者在声明里说清「哪一轮的结论对哪些文件有效」
MSG
  exit 1
fi
echo "✓ 全部未变 —— 冻结成立"
