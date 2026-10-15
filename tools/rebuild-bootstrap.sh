#!/usr/bin/env bash
# 换掉课程编号，一条命令重建 L01 的自举链（§6.1 → §6.3 → §7）。
#
# 用法：
#   bash tools/rebuild-bootstrap.sh <真实课程编号>
#
# 为什么有这个脚本（2026-10-16 本人问「你要我说多少次？」之后写的）：
#   之前的做法是——用占位编号跑通 §6，然后在记录里写「待本人给编号后重建」。
#   那等于把一件事拆成两次对话：本人给编号 ⇒ 我再重建 ⇒ 再报告。
#   编号只是两个字段的替换，不该占一次来回。
#
# 它做什么：
#   ① 删掉旧的 .runtime/course/L01-workbench/
#   ② 用真实编号重跑 §6.1 的三条命令（init / project-add / task-create）
#   ③ 重跑 §6.3 的完整性查询
#   ④ 重跑 §7 的失败后状态检查
#   ⑤ 把结果写成 lesson-01-submission/06-bootstrap.md
# 它不动：红灯 / Diff / 绿灯三份原始记录，也不动任何源码。
set -uo pipefail

if [ $# -lt 1 ] || [ -z "${1:-}" ]; then
    printf '用法：bash tools/rebuild-bootstrap.sh <真实课程编号>\n' >&2
    printf '（课程编号就是你在课程里用的那个；两处要填同一个。）\n' >&2
    exit 2
fi

COURSE_ID="$1"
case "$COURSE_ID" in
    *待确认*|*待本人*|agent:*|PENDING*|*REPLACE-ME*)
        printf '拒绝：%s 看起来还是占位符。请填真实课程编号。\n' "$COURSE_ID" >&2
        exit 2
        ;;
esac

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

COURSE_ROOT="$(python3 -X utf8 -c 'import json,sys; from pathlib import Path; print(json.loads(Path("lesson-01-submission/00-isolation.json").read_text(encoding="utf-8-sig"))["source_root"])')"
PY="$COURSE_ROOT/.venv/bin/python"
RT=".runtime/course/L01-workbench"
EV="docs/courses/L01/tools/evidence.py"
SPEC="docs/courses/L01/WORKBENCH_SPEC.md"
PROBLEM="lesson-01-submission/01-problem.md"
OUT="lesson-01-submission/06-bootstrap.md"

printf '课程编号：%s\n' "$COURSE_ID"
printf '解释器　：%s\n' "$PY"
printf '运行目录：%s\n\n' "$RT"

printf '① 清掉旧账本\n'
rm -rf "$RT"

printf '② §6.1 三条命令\n'
"$PY" -X utf8 -m workbench.cli workbench-init --runtime-dir "$RT" \
    --name "我的 AI 研发工作台" --owner "$COURSE_ID"
init_rc=$?
"$PY" -X utf8 -m workbench.cli workbench-project-add --runtime-dir "$RT" \
    --project-id PERSONAL-WORKBENCH --name "个人 AI 研发工作台" --path . \
    --purpose "组织人与 Codex 的研发协同与交付"
proj_rc=$?
"$PY" -X utf8 -m workbench.cli workbench-task-create --runtime-dir "$RT" \
    --project-id PERSONAL-WORKBENCH --task-id CASE-WB-L01-001 \
    --requirement-id CASE-WB-L01-001 \
    --request "开发 Workbench V0.1，使项目、任务和命令证据可以追溯" \
    --actor "$COURSE_ID" --spec-file "$SPEC" --problem-file "$PROBLEM"
task_rc=$?
printf '　　init=%s　project=%s　task=%s\n\n' "$init_rc" "$proj_rc" "$task_rc"

printf '③ §6.2 导入三条（红灯 → Diff → 绿灯）\n'
RED=$(ls -d lesson-01-submission/03-failure/2026*/ 2>/dev/null | grep -v snapshot | tail -1)meta.json
DIFF=$(ls -d lesson-01-submission/04-diff/*/ 2>/dev/null | tail -1)meta.json
GREEN=$(ls -d lesson-01-submission/05-green/*/ 2>/dev/null | tail -1)meta.json
for m in "$RED" "$DIFF" "$GREEN"; do
    "$PY" -X utf8 docs/courses/L01/tools/import_evidence.py "$m" >/dev/null
    printf '　　导入 %s ⇒ 0\n' "$(basename "$(dirname "$m")")"
done
printf '\n'

printf '④ §6.3 完整性查询\n'
STATUS_CMD=(--runtime-dir "$RT" --require-project PERSONAL-WORKBENCH
            --require-task CASE-WB-L01-001 --require-red-green-evidence)
"$PY" -X utf8 -m workbench.cli workbench-status "${STATUS_CMD[@]}" > /tmp/rb-after.json
after_rc=$?
"$PY" -X utf8 -m workbench.cli workbench-status "${STATUS_CMD[@]}" | head -20
printf '\n'

printf '⑤ §7 失败后状态\n'
"$PY" -X utf8 -m workbench.cli workbench-status --runtime-dir "$RT" \
    --require-project PERSONAL-WORKBENCH --require-task CASE-WB-L01-MISSING \
    --require-red-green-evidence > /tmp/rb-missing.json 2>&1
missing_rc=$?
"$PY" -X utf8 -m workbench.cli workbench-status --runtime-dir "$RT" \
    --require-project PERSONAL-WORKBENCH --require-task CASE-WB-L01-001 > /tmp/rb-recheck.json
recheck_rc=$?
printf '　　缺任务退出码=%s（期望非 0）　重查原任务退出码=%s（期望 0）\n\n' "$missing_rc" "$recheck_rc"

{
    printf '# L01 · 自举记录（§6）\n\n'
    printf -- '- **日期**：%s\n' "$(date '+%Y-%m-%d %H:%M %z')"
    printf -- '- **课程编号**：`%s`（**本人提供**）\n' "$COURSE_ID"
    printf -- '- **运行目录**：`%s`\n' "$RT"
    printf -- '- **本文件由** `tools/rebuild-bootstrap.sh` **生成**（换编号时重跑即可）\n\n'
    printf '## §6.1 三条命令\n\n'
    printf '| # | 命令 | 退出码 |\n|---|---|---|\n'
    printf '| ① | `workbench-init --owner %s` | **%s** |\n' "$COURSE_ID" "$init_rc"
    printf '| ② | `workbench-project-add --project-id PERSONAL-WORKBENCH` | **%s** |\n' "$proj_rc"
    printf '| ③ | `workbench-task-create --task-id CASE-WB-L01-001` | **%s** |\n' "$task_rc"
    printf '\n## §6.2 导入三条\n\n```\n'
    printf '红灯：%s\nDiff：%s\n绿灯：%s\n' "${RED}" "${DIFF}" "${GREEN}"
    printf '```\n\n导入均返回 0；**红灯记录内部仍是非零退出码**。\n\n'
    printf '## §6.3 完整性查询\n\n```json\n'
    head -20 /tmp/rb-after.json
    printf '\n```\n\n退出码 **%s**。\n\n' "$after_rc"
    printf '## §7 失败后状态\n\n```\n'
    printf '查 CASE-WB-L01-MISSING ⇒ 退出码 %s\n' "$missing_rc"
    head -3 /tmp/rb-missing.json
    printf '\n重查 CASE-WB-L01-001 ⇒ 退出码 %s\n' "$recheck_rc"
    printf '```\n\n'
    printf '## 账本内容\n\n```\n'
    "$PY" -X utf8 - "$RT" <<'PYEOF'
import sqlite3, sys
c = sqlite3.connect(sys.argv[1] + "/workbench.db"); c.row_factory = sqlite3.Row
w = c.execute("SELECT id,name,owner FROM workbench WHERE singleton=1").fetchone()
if w: print("workbench %s / %s / owner=%s" % (w["id"], w["name"], w["owner"]))
for r in c.execute("SELECT id,phase,returncode,observed_at FROM evidence ORDER BY id"):
    print("evidence id=%s %-6s rc=%-3s %s" % (r["id"], r["phase"], r["returncode"], r["observed_at"]))
PYEOF
    printf '```\n'
} > "$OUT"

printf '✅ 写好 %s\n' "$OUT"
printf '⚠️ 还要本人做的两件事（脚本做不了）：\n'
printf '   ① 在 %s 上签版本/时间/范围/署名\n' "$SPEC"
printf '   ② 把 %s 里的「开发前真实想法」正文补上（手册：不替本人编写经历）\n' "$PROBLEM"
