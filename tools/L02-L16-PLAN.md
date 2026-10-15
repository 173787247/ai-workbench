# L02~L16 + 结营毕设 · 执行清单

> 生成于 2026-10-16 ✗ 2026-10-16 02:05 更新。
> ⚠️ **病灶（本人问「L05 的 readme 看了吗」之后发现）**：

```
**我读了 README ✗ 按手册步骤做完了 ✗ 但跳过了 README 里标成"唯一当前课件"与"按需"的材料。**
**证据**：L05 / L06 / L07 三讲的 `lesson-XX-submission/` 里 **PPT 派生文件 = 0**
✗ 而三期 README 都把 PPT 列为「**唯一当前课件**」✓
⇒ ⭐ 漏东西的方式**不是"跳过大步骤"✗ 是"不读被标成按需的材料"** ✓
```

## ⭐ 每讲开工前：**逐行扫 README 的链接**（**硬要求**）

```bash
R=~/GO/CodexFDE/docs/courses/LNN
grep -oE '\[[^]]+\]\([^)]+\)' "$R/README.md"      # README 引用的每一个链接
ls -1 "$R/reference/" "$R/examples/" "$R/assets/"      # 三个按需目录
wc -l /tmp/ppt-text/LNN.txt                            # PPT 文字行数
```

逐个问"我读了没"：

- [ ] `辅导资料.md` → ★ 必读 ✗ 开工就读
- [ ] `实践操作手册.md` → ★ 必读
- [ ] `SUBMISSION.md` → ★ 必读（**证据字段**）
- [ ] ⭐ **唯一当前课件 / 当前课件（`.pptx`）**
      ⇒ 读 `/tmp/ppt-text/LNN.txt` ✗ **并写一份"PPT 与我的工作对照"**（**不能只"读过"**）
- [ ] `examples/` → 按手册用到的**逐个用**（**不是"打开目录"**）
- [ ] ⭐ **`assets/README.md`** → **读**（**它给每份证据标结论边界**）
- [ ] ⭐ **`reference/参考说明.md`** → **读**（**可能写着别的讲的坑的解释** ——
      **L05 那份就写着我在 L06 踩的那个坑** ✓）
- [ ] `reference/` 下**其他文件** → 扫文件名 ✗ 判断要不要读（**"选读"≠不读**）
- [ ] `examples/skills/` → **记"采用了哪个 skill 的哪一版"**（**手册有这一节**）

## 每讲的固定动作（**九项 ✗ 缺一不可**）

```
① docs/courses/LNN/README.md          —— 起点 / 新增 / 交给下一讲 / 三步顺序 / 按需材料
② docs/courses/LNN/辅导资料.md         —— 为什么
③ docs/courses/LNN/实践操作手册.md     —— 怎么做（按步走 ✗ 到停点才停）
④ docs/courses/LNN/SUBMISSION.md       —— 证据字段
⑤ /tmp/ppt-text/LNN.txt               —— PPT 文字
⑥ 按需材料 examples/ scripts/ reference/ assets/
⑦ ⭐ 扫 README 的每一个链接（见上）
⑧ ⭐ 写"PPT 与我的工作对照"
⑨ 执行 → 留原始证据 → 更新 lesson-NN-submission/ → 更新 START-HERE.md
```

**完成判据**：`grep -n '完成条件\|看到什么才算完成\|逐项核对\|通过标准' <手册>`

## ⚠️ 已经欠下的（**要回头补**）

```
[x] **L05** ✅ 已补（`09-ppt-comparison.md` ✗ `08-readme-gap-fix.md`）
[ ] **L06** ⚠️ 待补（PPT 292 行 ✗ reference/ 6 项 ✗ assets/README 13 行）
[ ] **L07** ⚠️ 待补（PPT 310 行 ✗ reference/ 2 项 ✗ assets/README 11 行）
[ ] **L01~L04** ⚠️ 也要回头量一遍（**那四讲我也只走了手册步骤**）
```

## 需要本人签的地方（**每讲都有 ✗ 一次问完**）

```
· Spec / 合同 的签署：版本 ✗ 时间 ✗ 接受范围 ✗ 署名
· 同伴或教师复核：无则写"待复核"
· 本人对设计的解释
· L05 起还需要：FlowERP 的实际运行业务结果由人核对
```

## L01 起已验证可复用的手法（**后续照用**）

```
· 红灯 / Diff / 绿灯**必须按这个顺序**采集（observed_at 严格递增）
· 用 `docs/courses/LNN/tools/evidence.py {red,diff,green,observation} -- <命令>`
  ⚠️ L03 及以后没有自己的 tools ✗ 用 L01 的 ⇒ 记录落进 lesson-01-submission/
     ⇒ 复制到本讲目录 ✗ 原件保留
· 手写 meta.json 无法被 import_evidence.py 读取 —— 必须用工具采
· 换课程编号：`bash tools/rebuild-bootstrap.sh <真实编号>`
· 防伪造检查会拒 待确认 / agent: 前缀 —— 不要绕过
· 写 Markdown 不要用未加引号的 heredoc（bash 会执行反引号）
· 非交互终端跑不了 input() 提示 ⇒ 用等价显式传参
· ⚠️ 子代理的输出路径要先清空（/tmp/xxx-answer.md 可能有旧一轮残留）
· ⚠️ **追加 `##` 会破坏六段 Spec 的解析** ⇒ 加内容要用 `###`（L03 与 L07 各踩一次）
· ⚠️ **zip 里不要写非法字节** ⇒ 用 `write` 工具或 python 写 Markdown ✗ 别用未加引号的 heredoc
· ⚠️ **`codex-substitute.py` 支持 `l05` 与 `l07` 两分支**
  （`--candidate <路径> --which l05|l07|auto` ✗ 或按工作台的 `codex exec` 契约调用）
```

## ⚠️ 本机没有 Codex CLI（**已确认 3 次**）

```
l05 / l06 / l07 都核实过：`codex` ✗ `~/.codex` ✗ `OPENAI_API_KEY` ✗ Windows 侧也没有
⇒ 手册里"会实际调用本机 Codex CLI"的步骤 ⇒ **用替代执行器 ✗ 并如实标注**
⚠️ ⚠️ **工作台会把它记成 `provenance: codex_cli`**（`execution.py:307` 的分支）
   ⇒ **真相在 `invocation.command[0]`** ⇒ **报告里必须写明这一点**
```

## 结营毕设

```
要求（目标原文）：用建好的工作台组织本人与 AI 助手解决一个真实小问题 ✗
                 交付「完成思路 + 代码链接」
⇒ 时机：L16 之后 ✗ 先读 L16 的辅导资料「全课程总结」与「四件亲手工作」
```
