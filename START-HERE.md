# START-HERE · 个人 AI 研发工作台（Codex AI 工程交付行动营）

> **写给下一个会话 —— 读完这一份就能接手。**
> 最后更新：2026-10-16 03:35 +0800
> ⚠️ **本文件在个人项目根目录（**不是 ~/GO/START-HERE.md**）✗ 那份是归档前的记录**

---

## 一、进度（**2026-10-16 清空重来之后**）

| 讲 | 状态 | 关键产物 |
|---|---|---|
| **L01** | ✅ **§1~§8 完成** | 五个账本命令 ✗ `bootstrap.py` 274 行 ✗ 红→Diff→绿三条原始记录 |
| **L02** | ✅ **§1~§6 完成**（**§7 待本人签**）| `AGENTS.md` 5 → 99 行 ✗ N0/N1 对照 ✗ 补了 3 条不变量 |
| **L03** | ✅ **8/8 检查通过** | `spec.py` 134 行 ✗ 六段模板 ✗ `FDE_SPEC.md` ✗ 三份输入复验 |
| **L04** | 🟡 **A 与 B 都做完 ✗ 都在等具名接受** | Ticket A：`execution.py` 286 ✗ `task_store.py` 158 ✗ `eval/harness.py` 126 ✗ CLI 204（**11 命令**）✗ Ticket B：候选 +39 行 ✗ **五个用例全 pass** |
| **L05** | 🟡 **§0~§6 完成 ✗ §7.1 页面回填与 §8 具名决定待本人** | 业务/工程两份 Eval ✗ **个人新增断言（变异体验证过）** ✗ 幂等修复 **11→14→14→17** |
| **L06** | ✅ **§1~§7 完成** | 四处报告 ✗ **假绿→如实报红→必需全绿** ✗ 两次修复 Diff ✗ **独立复验：接受** |
| **L07** | ✅ **§0~§7 完成（§6.4~§6.6 ✗ 真实同伴 ✗ 具名接受 待本人）** | 八项检查 ✗ 19 项/2 BLOCK ✗ Hook 已装 ✗ 迁移设计 ✗ Skill 自查 |
| **L08** | 🟡 **§1~§5 本地部分完成 ✗ §6 远程待本人许可** | 三条实验 ✗ A/B 同 summary ✗ **个人 8 项已接入（7 PASS）** |
| **结营毕设** | ❌ 未开始 | |

**测试**：`Ran 36 tests ✗ OK`（L01 账本 10 ✗ 壳 4 ✗ L02 不变量 3 ✗ L03 解析器 10 ✗ **L04 V0 9**）
⚠️ **L04 的绿灯要 30 秒** —— **A-08 的超时用例真的在等 30 秒**（不是卡住）
**提交**：起点 `be6024e`（**只有课程壳**）✗ **其后成果尚未提交**

## 二、每讲开工前必读（**七项 ✗ 缺一不可 ✗ 不靠记忆**）

```
① docs/courses/LNN/README.md          ← 结构在这里，跳过会漏关键约束
② docs/courses/LNN/辅导资料.md         ← 为什么
③ docs/courses/LNN/实践操作手册.md     ← 怎么做（按步走，到停点才停）
④ docs/courses/LNN/SUBMISSION.md       ← 证据字段
⑤ /tmp/ppt-text/LNN.txt               ← PPT 文字（**本人要求与仓搭配看**）
⑥ 按需材料 examples/ scripts/ reference/ assets/
⑦ 执行 → 留原始证据 → 更新 lesson-NN-submission/ → 更新本文件
```
**完成判据**：`grep -n '完成条件\|看到什么才算完成\|逐项核对\|通过标准' <手册>`

## 三、可直接复用的手法（**L01~L03 验证过 ✗ 踩过坑的**）

```
· 红/ Diff / 绿灯**必须按这个顺序采集**（observed_at 严格递增）—— 否则完整性检查拒
· 用 `docs/courses/L01/tools/evidence.py {red,diff,green,observation} -- <命令>`
  ⚠️ **L03 及以后没有自己的 tools ✗ 用 L01 的 ⇒ 记录会落进 lesson-01-submission/**
     ⇒ **复制到本讲目录 ✗ 原件保留**（见 lesson-03-submission/03-failure/README.md）
· **手写 meta.json 无法被 import_evidence.py 读取** —— 必须用工具采
· **换课程编号**：`bash tools/rebuild-bootstrap.sh <真实编号>`（一条命令重建 §6/§7）
· 防伪造检查会拒 `待确认` / `agent:` 前缀 —— **不要绕过**
· **写 Markdown 不要用未加引号的 heredoc**（bash 会执行反引号 ⇒ 文件被写坏，我踩过 3 次）
· **非交互终端跑不了 `input()` 提示** ⇒ 用等价显式传参
· ⚠️ **子代理的输出路径要先清空**：`/tmp/xxx-answer.md` 可能有**旧一轮的残留**，
  否则会把旧结果当成新的（**我差点犯过** ⇒ 先 `mv` 走旧文件）
```

## 四、只有本人能给的（**不要代签**）

```
【待本人】1. **课程编号** —— 手册：两处填**同一真实编号**
           现在账本里是 `KA-2026-0001`（**我用的测试值 ✗ 要换**）
【待本人】2. L01 `01-problem.md` 的「开发前真实想法」正文
           （**手册：不替我编写经历、理由或个人答案**）
【待本人】3. **Spec / 合同签署**（L01 ✗ L03 都还是 draft）
【待本人】4. **同伴或教师复核**（L02 §7 ✗ L01 §8 ✗ L03 交接检查）
           ⇒ 本会话用**子代理模拟"新会话"** ✗ **不是真人同伴** ✗ 已如实标注
```

## 五、硬约束

```
· 不改 FlowERP 仓库（`~/GO/flowERP-customer` ✗ 至今 0 改动）
· 不改课程材料（`~/GO/CodexFDE` 只读）
· 不把参考仓库源码整份复制进个人项目
· 红灯必须用课程工具采集；「不倒填缺失的起始证据」
· 不删除功能制造红灯；「已有能力通过时如实记录」
· 不把"停止"写成"自动回滚"
· 解释器：`~/GO/CodexFDE/.venv/bin/python`（3.11.16）—— **不用系统 python3**
```

## 六、本讲目录清单

```
workbench/    bootstrap.py 274 ✗ cli.py 143 ✗ spec.py 134 ✗ workbench_server.py（L00 壳）
             templates/SPEC_TEMPLATE.md 58
tests/        test_l01_workbench_bootstrap.py 191 ✗ test_l02_status_invariants.py
             test_l03_spec_parser.py ✗ test_workbench_server.py（L00）
docs/courses/L01/WORKBENCH_SPEC.md ✗ docs/courses/L03/FDE_SPEC.md
lesson-01-submission/  红→Diff→绿 ✗ 06-bootstrap.md ✗ SUBMISSION.md
lesson-02-submission/  N0/N1 原始回答 ✗ 对照 ✗ agents-before/after
lesson-03-submission/  decisions ✗ FDE_SPEC ✗ 模板 ✗ 采购草稿 ✗ evidence ✗ 三份输入
tools/        rebuild-bootstrap.sh ✗ L02-L16-PLAN.md
```


---

# ⭐ L04 进度（**Ticket A ✗ 两张任务单**）

## 手册的**唯一顺序**

```
A 建设 → A 独立复验 → B 执行 → B 独立复验
⚠️ **A 没有通过 ✗ 不启动 B**；**B 自动检查变绿 ✗ 也不能跳过人工验收**
```

## 进度

```
§1   ✓ 证据区（4 个文件）+ 检查支架 217 行（sha 0370495edbc6384c…）
§2   ✓ Ticket A 的六段合同（113 行）✗ **能被工作台解析**（退出码 0 ✗ 三条正常结果全对）
§3.0 ✓ 只读调查：八项能力 ① ✅ ② ⚠️ ③~⑤ ❌ ⑥ ⚠️ ⑦ ❌ ⑧ ✅
     ✗ 参考实现 execution.py 697 行的三个接口契约已读出并对齐
§3.1 ✓ 测试 9 条（A-01~A-09）✗ **红灯 Ran 9 / failures=9 / invalid choice: 'task-create'**
§4   ✓ 实现：
        workbench/execution.py 219 行（**能力信封 ✗ 写集 ✗ 超时 ✗ Diff**）
        workbench/task_store.py 158 行（**Spec 绑定 ✗ 任务 ✗ 状态 ✗ 人审**）
        workbench/cli.py 204 行（**11 个命令**）
        ✗ **绿灯 Ran 9 / OK**
§4   🟡 **非执行者独立复验在跑**（**子代理 `bab03d87-…` ✗ 工作区 /tmp/l04-verify**）
§5~§7 ❌ 未做（**B 要等 A 被接受**）
```

## ⭐ 与参考实现逐条对齐的证据

```
normalize_write_scope 的 9 个非法输入全部拒绝（正确错误码）
validate_v0_authorization 5 种非法全拒 ✗ **并拒绝把工作台源仓库当候选**
常量一致：timeout **30..3600** ✗ 受保护目录 ['.codex','.git','.runtime','.tmp','__pycache__']
```

## ⚠️ 仍未建的一块

```
❌ **`eval/harness.py`** —— Ticket A 的"最小 Eval 与报告汇总"还没建
   现在只有 execution.py 里的**写集检查** ✗ **没有独立的检查汇总与出口码**
⇒ 复验结束后立刻补 ✗ ⚠️ **补了就是"控制源码变化" ⇒ 复验结论要重做**（手册的规矩）
```

## ⚠️ 一处必须说清的

```
⚠️ **本机没装 Codex CLI**（WSL 与 Windows 侧都没有 ✗ 没有 OPENAI_API_KEY）
⇒ `run_candidate` 跑的是**给定的命令** ✗ **不是真的 `codex exec`**
⇒ Ticket A 的"实际调用 Codex"这一环 **在我这里是等价物 ✗ 不是原生调用**
⇒ **手册允许多少要看本人判断** ✗ 如实标注
```


---

# ⭐ L04 复验与重修（**2026-10-16 01:17**）

## 提交

```
be6024e  chore: 初始化课程提供的工作台壳          ← 起点（**25 文件 ✗ 纯课程壳**）
af122c1  L01~L04：账本 V0.1、仓库规则、Spec 解析器、Ticket A 受控执行   ← **41 文件**
🚧       L04 复验与重修的记录正在补提交
```

## ⭐ 第一次独立复验抓到的（**手册 §4 的价值全在这里**）

```
⚠️ **高危**：`--allow-write workbench/` 下用 `../` 或绝对路径改掉**候选目录之外**的文件 ⇒
   返回 `{"ok": true, "changed": [], "out_of_scope": []}` ✗ **零告警** ✗ 受害者文件被改掉
⇒ ⭐ **写集是事后过滤 ✗ 不是事前约束** —— 而合同目标第一句就是「限制写入范围」
⚠️ **用例1 的"验证命令"零实现**（`eval/harness.py` 不存在）
⚠️ **两条测试写松**：A-06 用 `assertIn` 放行两个语义相反的码；
   A-09 的 docstring 说"仍待人审"却直接 accept ✗ 没断言 `pending_human_review`
⚠️ 另外四条：命令不存在不落证据（R5）✗ 仅复验谎报 `returncode:0`（R6）✗
   建完任务改 Spec 无提示（R3）✗ 退出码 0 但没改动可解锁接受（R4）
⇒ **判定：依据不足 → 有条件退回重修**（**不能接受 ✗ 也不宜整体退回**）
```

## 我改了什么（**逐条对应**）

| 退回项 | 处置 |
|---|---|
| **① 写集口径** | ✅ 新增 `_snapshot_outside()` ✗ 报告加 `escaped_candidate` ✗ 有逃逸 ⇒ **拒绝**（**即使退出码 0**）✗ ⚠️ **明说是事后检测 ✗ 不是沙箱** |
| **② `eval/harness.py`** | ✅ 补 126 行：登记 → 逐项跑 → 分级汇总 → 报告与出口码 ✗ **零用例拒绝** ✗ **blocking⇒1 ✗ observing⇒0** |
| **③ 两条测试** | ✅ A-06 收紧为 `assertEqual("write_scope_required")` + **断言命令真没跑** ✗ A-09 **先断言 `pending_human_review`** 再 accept |
| **R5** | ✅ 命令不存在 ⇒ `ExecutionError("command_not_found")` |
| **R6** | ✅ 仅复验 ⇒ `returncode: None` ✗ 加 `command_executed: False` |
| **R3 ✗ R4** | ⚠️ **未修 ✗ 如实记在 `SUBMISSION.md` 的"仍未解决"** |

**修完自己先验了两个方向**：逃逸 ⇒ `ok=False` + `escaped_candidate=[…]` ✗
范围内 ⇒ `ok=True` + `changed=['workbench/n.py']` ✗ **没退化成一律拒绝** ✓

## ⭐ 复验者问的两个问题（**已答**）

```
Q1 「范围外的 AGENTS.md ✗ bootstrap.py ✗ L01/L03 文件是谁加的？」
   ⇒ **是 L01~L03 的产物**（**那三讲在本讲之前**）✗ 而它**无法从 git 判定**因为当时只有一个提交
   ⇒ ✅ **处置：提交了 af122c1** ✗ 现在可锚定 ✓
Q2 「交付一次都没提交」
   ⇒ ⚠️ **一半是误解**：课程壳的 `.gitignore` **第 8 行就是 `lesson-*-submission/`** ✗
      **学生提交目录故意不进版本控制**（**L01 手册：「证据材料不提交到 Git」**）✓
   ⇒ ✅ **代码交付确实已提交**（`workbench/` 10 ✗ `tests/` 6 ✗ `eval/` 2 ✗ `docs/` 7）✓
```

## ⚠️ 仍未解决的

```
❌ **`escaped_candidate` 是事后检测 ✗ 不是沙箱** —— 本环境没有工作区权限机制
   ⇒ ⭐ **合同口径要不要改成"只覆盖候选目录内部"✗ 是人的决定** ✗ **待本人**
❌ **R3**：建完任务后改 Spec ⇒ 执行照跑 ✗ 无提示
❌ **R4**：退出码 0 但一字未改 ⇒ `ok=true` ⇒ 可解锁人工接受
❌ **本机没装 Codex CLI** ⇒ `run_candidate` 跑的是**给定命令**✗ 不是真的 `codex exec`
❌ **§5~§7（Ticket B）未做** —— **手册：A 未接受 ✗ 不启动 B** ✗ **而接受必须由具名的人作**
```


---

# ⭐ L04 Ticket B（**通过 A 交付库存导出**）

## ⭐ 执行前的决定性问题：**能力已经存在**

```
`flowerp/import_export.py:248-262` 的 `export_csv(principal,"inventory")` **本来就已经正确**：
  权限 `reports.read` ✓  · SQL 里算 `b.on_hand-b.reserved AS available` ✓
  · **八列名与顺序恰好是 L03 合同的** ✓  · `ORDER BY p.sku,s.code,l.code,b.lot_id` ✓
⇒ ⭐ **四个 content 用例在"未改的候选"上就全部通过**（**第一次运行 ✗ 退出码 0**）✓
⇒ 手册：「**参考仓库已有能力可以复验 ✗ 学生自己缺少的能力才需要建设**」✓
⇒ ⚠️ **所以 Ticket B 是"复验 + 补唯一缺口"✗ 不是"从零实现"** ✓
```

## 补的那一块

```
⭐ 唯一缺口：`--file-entry` 要 `function(store, target_path)` ✗ 现成的 `export_csv` 返回字符串
⇒ 补 `export_inventory_to_file(store, target)`（**+39 行**）：
   · **同目录**临时文件（**跨文件系统时 `os.replace` 不是原子替换**）
   · `flush()` + `os.fsync()` ✗ `os.replace()` ⇒ **写成后才替换**
   · `except BaseException:` ⇒ **清理临时文件** ✗ **`raise` 把异常报给调用者**
```

## ⭐ 五个用例的真实结果（`--case all` ✗ **退出码 0**）

```
normal    ✅ 东仓 8,3,5 ✗ 西仓 12,4,8 —— **与手册的预期数字一致**
empty     ✅ **只有八列表头**
special   ✅ 中文 ✗ 逗号 ✗ 双引号 ✗ **换行**全部保真
ordering  ✅ 四行按 sku,site,location,lot_id 升序
file-failure ✅ with-old 与 without-old 都：
              triggered=True ✗ error=OSError ✗ database_unchanged=True ✗ target_preserved=True
              ✗ **目录里没有 .tmp 残留**（**临时文件被清理** ✓）
业务账    ✅ 六次 before.json == after.json 全为真
写集      ✅ **只有 flowerp/import_export.py**（+39 行）✗ 源仓库 **0 改动**
```

## ⚠️ 两条如实标注

```
⚠️ **A 是 `pending_human_review`** ✗ 手册要求「A 未接受不启动 B」✗
   本次是在本人「连续推进」授权下**带标记执行**的 ⇒ **不掩盖** ✓
⚠️ **两套"可用量"仍在**：`service.py:105` 的旧 `export_inventory()` 硬编码 `MAIN,STOCK,` ✗
   用旧表 `products`/`stock` ⇒ **与 `import_export.py:250` 两个口径** ✗
   ⚠️ **要不要删它不在本 Ticket 的写集里**（**写集只有 `import_export.py`**）⇒ **遗留问题 ✗ 由人决定** ✓
```

## 复验

```
🟡 **B 的独立复验在跑**（**子代理 `63a23633-…` ✗ 工作区 /tmp/l04-verifyB ✗ 已提交可锚定**）
```


---

# ⭐ L05 完成情况（**先设计失败 ✗ 再编写 Eval**）

## 八步与结果

```
§0 首次判断       ✅ **在读教学答案之前写的** ✗ 【本人】栏留空 ✓
                   ⭐ 预判**对 6 条 ✗ 漏 3 条**（**漏的才是靶心**）
§1 进入工作台     ✅（**用参考仓库的 workbench.cli** ✗ 个人仓的 cli 只到 L04 的范围）
§2 回看首次判断   ✅ `01-comparison-with-answer.md`（**不覆盖原稿** ✓）
§3 旧绿新红       ✅ 旧检查 **status=pass ✗ failures=[]✗退出码 0** 而 **event_count 2→3**
                   ✅ 完整检查**两次** ⇒ **AC-REPLAY + AC-NEW ✗ 集合相同**
§4 独立仓库验证   ✅ 合法 0 ✗ 越界新增 1 ✗ **重命名 1**
§5 接入正式候选   ✅ course-spec ✗ course-prepare（gap#5 ✗ 幂等入库）
                   ✅ 冻结三份 sha256 ✗ 会话提交 **22417c80** ✗ course/l05-start 是祖先
§6 组织修复复验   ✅ 修复缺陷 `service.py:118` 的 **`if False and exists:`**
                   ✅ 同命令 **红(1) → 绿(0)** ✗ 迁移 **11→14→14→17 ✗ 流水 1→2→2→3**
                   ✅ **个人新增断言**（A→B→重放A）✗ 变异体 **FAILED(failures=1)**
§7 页面回填       ⚠️ **未做** —— 需要工作台网页的"事项与决策" ✗ **待本人**
§8 具名决定       ⚠️ **未做** —— 需要具名的人 ⇒ **写"待完成"✗ 不补造结论** ✓
```

## ⚠️ 三处方法论偏差（**如实记 ✗ 不掩盖**）

```
⚠️ **§6.1 手册要"实际调用本机 Codex CLI" ✗ 本机没装** ⇒
   用本人授权的**替代执行器** `tools/codex-substitute-l05.py`（**声明 is_codex: false**）✓
   ⇒ ⭐ **"工作台组织这次调用"这一环在我的路径上是缺的** ✗ 补它需要 `--actor <具名>` ⇒ 待本人
⚠️ **§7.1 的页面回填没做**
⚠️ **个人断言加在会话提交之后** ⇒ **冻结已重做**（`frozen-checks2.json`）
   ⚠️ **但"含红灯 Eval 的候选提交"应该再补一次** ⇒ 待补
```

## ⭐ 本讲最有用的一条（**我预判时漏了 ✗ 教学答案点出来了**）

```
「**这个推演同时给出两个相反要求：重复请求要被识别 ✗ 新请求要继续生效。**」
⇒ ⚠️ 「**发现商品已经收过货就忽略以后所有请求**」**不是修复** ✗ **它吞掉了 B** ✓
⇒ ⭐ **而我在 L04 刚被"保护过头"咬过**（`_snapshot_outside` 误报）**却还是没提前想到** ✓
⇒ ⭐ **另一个方向的错，比原来的错更隐蔽** —— 因为它"看起来更安全" ✓
```

## 下一步

```
L06  统一分级与报告（**把 L05 的两份检查交给 Harness 统一执行和汇总**）
L07~L16 + 结营毕设   ⇒ 剩余 11 讲 ✗ 每讲七项必读照走 ✓
```


---

# ⭐ L06 完成情况（**用 Harness 汇总证据和等级**）

## 本讲的问题与通过标准

```
**问题**：四项检查各有结果 ✗ 工作台怎样给出一个可信结论？
**现场**：在库 8 ✗ 预占 3 ✗ **查询可用 5 ✗ 而 CSV 却是 8** ⇒
        **库存检查发现了错误 ✗ 坏汇总器仍报通过** ✓
**通过标准**：阻断用例失败 ⇒ **非零退出码** ✗ 观察项失败 ⇒ **只记录告警** ✗
            报告保留运行时间和失败原因 ✓
```

## §1~§6 与结果

```
§1 准备      ✅ **补了 L05 §1.1 的真会话**（**本机没 zsh ⇒ 原样抽出 session.zsh:56-99 的 Python 跑**）
              ✅ 并补走 L05 §6.1 `course-submit`（**用替代执行器**）⇒ 产出 submission.json
              ✅ L06 prepare：候选 ✗ allowed=[eval/l06_runner.py, flowerp/service.py]
              ✅ 两个注入缺陷都读出来了：
                 ① service.py:110 CSV 的 available 列写成 `{row['on_hand']}`
                 ② l06_runner.py:33 **`blocking_failed = 0`**（**上面就写着 L06-GAP**）
§3 原始失败   ✅ contract **1** ｜ run **0（假绿）** ｜ review **1**
              ⭐ 02-false-green.json：分项 blocking 有 1 项 false ✗ 而 summary 写 **0**
§4 只修汇总   ✅ 合同 **Ran 9 ✗ OK** ｜ contract 0 ｜ run **1** ｜ review 0
              ⭐ 04-honest-red.json：`{"blocking_failed":1, "decision":"block"}`
              ✗ `AC-AVAILABLE: expected=[8,3,5], actual={'query':[8,3,…]}`
              ⇒ ⭐⭐ **业务仍红 ✗ 汇总器已修好** ✓
§5 再修导出   ✅ `{row['on_hand']}` → `{row['available']}`
              ✅ run **0** ｜ review 0 ⇒ `business_decision: pass`
              ⭐ 05-export-fixed.json：`{"blocking_failed":0, "observing_failed":1, "decision":"pass"}`
              ⇒ ⭐⭐ **必需项全绿 ✗ 观察告警仍保留** ✓
§6 迁移       ✅ opening=11/reserved=3 ⇒ 退出码 0 ✗ 库存项通过 ✗ 结论不变 ✓
```

## ⭐ 本讲最有用的一条

```
**坏运行器的错就一行**：`blocking_failed = 0`
⇒ ⚠️ **它不是"算法写错了"✗ 是"这个数根本没算"** ✓
⇒ ⭐ **而它造成的后果很隐蔽**：**分项老老实实报了红 ✗ 总判决照样 pass** ✗
   **屏幕上看不出问题 —— 除非有人去比对"分项"与"汇总"** ✓
⇒ ⭐⭐ **本讲给出的闸就是那道比对**：`review` 报
   「**Eval 汇总与逐项结果不一致**」✗ **退出码 1** ✓
⇒ ⭐ **同一类错我在 L04 见过**（`escaped_candidate` 误报）**在 L05 也见过**（`if False and exists`）
   ⇒ **三处都是"该发生的事被静默地没发生"** ✓
```

## ⚠️ 三处如实标注

```
⚠️ **§4/§5 是我（替代执行者）改的** ✗ 手册写给 Codex ⇒ **本机没装**
⚠️ **这两次修复没走 course-submit** —— L06 手册流程就是"Codex 改 ✗ 我跑命令核对"✗
   没要求交给工作台（**L09 才做有范围的自动返工**）✓
⚠️ **Diff 不是 `git diff` 生成的** —— 候选 worktree 的 `git diff` 是空的 ✗
   改用 **run 目录里 `prepare` 自己存的 `before/` 快照**（**更权威** ✓）
```

## 下一步

```
L06 §7  独立复验（**手册：独立复验 ✗ 完成本讲并留下交接待办**）⇒ 起复验者
L06 §8  中断恢复与失败处理（**手册第 8 节**）
L07~L16 + 结营毕设   ⇒ 剩 10 讲
```


---

# ⭐ L06 §7 独立复验（**它接受 ✗ 但抓到我的两处错**）

## 复验者做了什么（**没只看报告** ✓）

```
A 路：把工作区复制 ✗ 补 baseline.json ✗ 按我给的命令跑
B 路：⭐ **用 `prepare` 从 L05 会话从零重建**一棵候选 ✗ **不依赖我的任何产物** ✓
```

## 三句通过标准：**三句全部成立**（**它实测的**）

```
① 阻断失败 ⇒ 非零退出码 ✅
   它重建的未修复起点：`FAILED(failures=2)` 退出码 1 ✗ 业务侧 **decision=pass ✗ 退出码 0（假绿）**
   修复①后：**blocking_failed=1 ✗ decision=block ✗ 退出码 1** ✅
② 观察项失败只记告警 ✅ ⭐ **双向反证**：
   升格 help_image→blocking ⇒ 退出码 1（**证明真由 level 驱动** ✓）
   降格 l06_stock_consistency→observing ⇒ **缺陷仍在却 decision=pass ✗ 退出码 0** ⚠️
③ 保留运行时间与失败原因 ✅ ⚠️ **但没有"整轮总耗时"字段** ⇒ **措辞待明确** ✓
额外：`verify` 显示 **167 个文件改动恰好只有允许的两个** ✗
     它重建的候选与我的 **AST 完全相同** ✗ ⭐ **消费者还拒收了我那份假绿报告** ✓
```

## ⚠️ 它抓到的我的两处错

```
① ⚠️ **我交付的工作区跑不起来**（阻断性）
   少 `baseline.json` 与 `before/` ⇒ `verify()` 先读它 ⇒ **三条命令一起死（退出码 1）**
   ✗ 而且 `receipt.report_path` 指向原路径 ⇒ **复制过来的报告永远无法被 `review` 校验**
   ⇒ ✅ **已补 `01-run/baseline.json ✗ before/ ✗ session.json`** ✓
② ⚠️ **我说「`git diff` 是空的」—— 措辞误导**
   候选**根本不是 git 工作树**（**没有 `.git`**）⇒ 那句话**空洞成立** ✗
   ⭐ **不是"改动为零"的证据** ✓
   ⇒ ⭐⭐ **又是同一个形状：用一个分辨不出东西的检查下结论**
      （**与 L05「已修检测」✗ L04 越界检测 ✗ L06 `blocking_failed=0` 完全同形** ✓）
   ⇒ ✅ **已改正 ✗ 并写明是谁纠正的** ✓
```

## ⭐ 它设计的 10 条反例：**9 条守住 ✗ 1 条被绕过**

```
✅ 守住的：CE1 改回固定 0 ⇒ 合同抓得住 ｜ CE2a 升格 ⇒ 真变阻断 ｜
   CE3 抛异常 ⇒ 记为失败且继续 ｜ CE4 空/未知/重名/坏 level ⇒ 全 ValueError ｜
   CE5a 假绿报告 ⇒ 消费者拒收 ｜ CE5a-2 汇总诚实但退出码 0 ⇒ 拒收 ｜ CE6 路径复用 ⇒ 拒写
⚠️ **被绕过的 CE5b**（**最有价值的一条**）：
   把**报告和 receipt 一起**伪造成自洽的假绿 ⇒
   `review` 报 `{"report_consistent": true, "business_decision": "pass"}` ✗ 退出码 0 ⚠️
   **而缺陷仍在树里** ✓
   根因：`review` 只校验**内部自洽性** ✗ **把 receipt 的 `exit_code` 当记录值** ✗
        **receipt 是明文可写无签名的** ⇒ **能改报告的人必然能改它旁边的 receipt** ✓
   缓解：`execute` 记了 command ⇒ **重跑即可证伪** ✗ **但 `review` 不重跑** ✓
```

## ⚠️ 它"无法验证"的一件（**与 L05 那条对得上**）

```
⚠️ **执行者身份**：它说「**没有 Codex CLI ✗ 由本人授权的替代执行者完成**」**无从核实** ✓
⇒ ⚠️ **而 L05 的工作台把那次执行记成了 `provenance: codex_cli`** ✓
   ⇒ **一处说"是 Codex"✗ 一处说"不是"✗ 第三方无从判断** ⇒ ⭐ **这是个真问题 ✗ 我记下不掩饰** ✓
```

## ⭐ 它的边界（**照抄**）

> 「**我的「通过」不能替代具名的人的决定** —— **这是工程一致性判定 ✗ 不是业务验收** ✗
> **执行者身份我无法核实** ✗ 且 **`review` 可被伪造绕过** ✗
> **若要作为正式证据链 ✗ 需一位具名的人重跑过 `run`（而非只跑 `review`）之后签字**」

⇒ **`session.json` 自己也写着** `"local personal practice; not a course-submit or human acceptance"` ✓


---

# ⭐ L07 起步（**用 Codex Hooks 建立本地护栏**）

## 本讲的问题

```
**上午订单金额 120 元 ✗ 通过检查 ✗ 下午代码改成 50 元 ✗ 仍拿上午报告交付** ✓
⇒ ⭐ **不是"检查不准"✗ 是"检查在时间上没绑定到代码版本 + 触发靠人记得"** ✓
**通过标准**：Hook 来源可检查 ✗ **故意引入违规时流程被阻断** ✗ 恢复后重新通过 ✓
```

## §0 我写预判时**对**的（**读答案之前 ✗ 未覆盖原稿** ✓）

```
✅ 「**Hook = 何时调用 ✗ Harness = 跑什么怎么判**」（**答案：Hook 决定何时 ✗
   Harness 决定如何执行和汇总 ✗ Eval 决定某项要求是否满足** ✓）
✅ 「**Hook 里不该再写一套检查逻辑**」（**答案：两份标准会逐渐分叉** ✓）
✅ 「**三类证据不是一回事**」（**控制实验 / 待审 Hook / 宿主真实事件** ✓）
✅ 「**"报了红"和"被拦下"是两件事**」（**方向对 ✗ 答案说得更准** ✓）
```

## ⭐ 教学答案**补上的**（**我没写到的**）

```
⭐ ① **两个进程的退出码职责不同**：
   「**内部 Harness 的退出 1 表示阻断级检查未通过；处理器成功读到这个结果 ✗
     输出宿主要求的合法响应 ✗ 自己可以退出 0**」
   ⇒ ⭐ **处理器的成功表示"反馈交付完成"✗ 不是"订单金额正确"** ✓
   ⇒ ⭐⭐ **这直接接上 L06**：「**报告复核工具成功确认一份红报告是真实的 ✗
     完全可以退出 0**」⇒ **两讲说的是同一件事** ✓
⭐ ② **`cwd` 校验 ✗ 解释器选择 ✗ `stop_hook_active` 防重入**（**三条具体机制**）
   ⇒ ⚠️ **"防重入"我完全没想到** —— **Stop 被处理器自己触发会无限递归** ✓
⭐ ③ **三个不同事实**：「**项目提供配置 ✗ 配置已被信任 ✗ 宿主实际调用**」
   ⇒ ⭐ **我原来只想到三层 ✗ 漏了"信任"这一层** ✓
   ⇒ 完整四层：**配置存在 → 配置加载 → 配置已被信任 → 真实事件调用** ✓
⭐ ④ **迁移判断**：
   「**`Stop` 不能撤销已经写过的文件 ✗ 更不能阻止已经发送的邮件** ⇒
     **有不可逆副作用时应选动作之前的检查点** ✗
     **检查时机应由业务损失决定 ✗ 而不是所有任务都套 `Stop`**」
   ✗ 「**Git Hook 与 Codex Hook 可以互补 ✗ 但不能互相作证**」✓
⭐ ⑤ **V1 → V2 → V3 的时序**：2×30＋3×20 = **12000 分** ✗ V2 漏乘数量 ⇒ **5000 分** ✗
   §5 要按 **V2→V3** 检查 ⇒ **检查必须覆盖最新那一版** ✓
⭐ ⑥ **四种分诊**（**我只有第一种**）：检查抓错 → 查为何没调用 ／
   金额错而检查绿 → 查输入与断言 ／ 报告加载 V1 源码 → 校正目录与解释器 ／
   模块打不开 → 先恢复环境 ✓
```

## ⚠️ 我标"待核对"的三点，答案是什么

```
① 「Stop 是"用户按停"还是"模型答完"？**我倾向前者**」⇒ ⭐ **是"准备结束"✗ 我倾向错了** ✓
② 「Hook 能挂哪些事件」⇒ **开始 ✗ 工具调用前后 ✗ 准备结束** ✓
③ 「Hook 失败会不会阻断主流程」⇒ ⚠️ **答案比"阻断"更细**：
   **处理器自己可以退出 0 ✗ 真正的阻断语义在"宿主怎么看那个响应"** ✓
   ⇒ ⚠️ **我把问题想成了二选一 ✗ 答案是个三层语义** ✓
```

## ⚠️ 已知的硬障碍

```
⚠️ **本机没有 Codex CLI** ✗ 而 §6 要「**把 Hook 接入 Codex ✗ 在 CLI 用 `/hooks` 信任 ✗
   取得真实失败与恢复证据**」✗
⇒ ⭐ **"宿主真实事件"这一类证据我拿不到原生的** ✗ **不用别的东西冒充** ✓
⇒ **§2~§5 可以做的照做 ✗ §6 如实标** ✓
```


---

# ⭐ L07 §3~§4 完成

## §3 六种协议输入（**全部与手册预期一致** ✓）

```
pass          调用 **1** 次 ✗ handler_return **0** ✗ `{"continue": true}`
block         调用 **1** 次 ✗ handler_return **0** ✗
              `{"decision":"block","reason":"…**ORDER-TOTAL expected=12000 actual=5000**"}`
              ⇒ ⭐ **Harness 抓得到 V2** ✓（**印证 §2.1 分诊表第一行** ✓）
reentry       调用 **0** 次 ✗ `{"continue":true,"systemMessage":"**重入跳过；本次未复验**…"}`
malformed     调用 **0** 次 ✗ stderr `JSONDecodeError` ✗ stdout **block**
timeout       stderr `TimeoutExpired` ✗ stdout "**未完成验证**" block
command-error stderr `FileNotFoundError` ✗ stdout "未完成验证" block
⇒ ⚠️ **六种退出码都是 0** ✗ 手册警告的正是这个：
   「**包装实验完成观察时本身可以返回 0 ✗ 要检查 JSON 内的 `handler_return` ✗
     `exception` ✗ `response` 与调用次数**」✓
⇒ ⭐⭐ **只看退出码 ⇒ 六种全都"成功"✗ 什么也分辨不出来** ✓
⇒ ⭐ **`exception` 六种全是 `None` ⇒ 也不能看它**（**原错误在 `stderr`** ✓）
⇒ ⭐ **`real_codex_event` 六种全是 `False`** ⇒ **它们自己声明"这不是真实事件"** ✓
```

## §4 调用链调查（**只读 ✗ 未启用 ✗ 未改文件** ✓）

```
① 配置   `.codex/hooks.json`            18 行 ✗ sha **d629f67bb9a51830**
② 处理器 `.codex/hooks/quality_gate.py` 46 行 ✗ sha **5c70ad1fdf9a5343**
③ Harness `-m eval.harness --suite blocking`（**L06 建成的** ✓）
```

**⭐ 四个关键机制**（**行号我自己查的** ✓）：

```
**解释器**   `$(git rev-parse --show-toplevel)/.venv/bin/python`
           ⇒ ⭐ 不是写死的绝对路径 ✗ 而是"仓库根下那个 venv" ✓
**cwd**      ⭐ **两道**：① 配置层用 `git rev-parse` 定位脚本
           ② 处理器 `:18-20`：`event["cwd"]` 必须落在 `root` 之内
              否则 `ValueError("event cwd is outside this project")`
           ✗ `:29` 又把内部 subprocess 的 `cwd` 显式设成 `root`
**两层超时** ⭐ **外层 960（hooks.json）✗ 内层 900（quality_gate.py:8）**
           ⇒ ⭐ **内层必须小于外层** —— 否则宿主先杀 ✗ 处理器来不及返回合法响应 ✓
**重入**     `:21-22` 先**校验类型必须是 bool**（**不信任 `"true"` 字符串**）✗
           再 `:23` 走跳过 ✓
```

## ⭐ Stop vs Git Hook（**手册：可以互补 ✗ 但不能互相作证** ✓）

```
| | Stop（**本讲**）| Git Hook |
| **触发源** | **Codex 工作事件** | **Git 操作** |
| **管得到"没提交就交付"吗** | ✅ **能** | ❌ **管不到** |
| **管得到"提交前又改了"吗** | ⚠️ 取决于何时结束 | ✅ **能** |
| **能撤销已写的文件吗** | ❌ | ❌ |
| **能阻止已发的邮件吗** | ❌ **更不能** | ❌ |
⇒ ⭐ **检查时机应由业务损失决定 ✗ 有不可逆副作用时必须选动作之前的检查点** ✓
```

## ⚠️ 本节边界

```
❌ **个人 Hook 一个字节都还没装** ✗ **不代表"已安装"** ✓
❌ **订单检查还没登记** ⇒ **§5 才做** ✓
⚠️ 参考配置的 sha 我记了 ⇒ **将来对照"个人配置是不是照抄参考"时有据可查** ✓
```

## 下一步

```
L07 §5  取得候选 ✗ 准备解释器 ✗ 接入 L06 检查 ✗ 按 V2→V3 时序诊断
L07 §6  安装 ✗ 信任（`/hooks`）✗ 真实 Stop 触发 ⇒ ⚠️ **需要 Codex CLI ✗ 本机没有** ✓
L07 §7  复验与迁移（**模拟邮件**）
```


---

# ⭐ L07 §5.1~§5.4（**候选 ✗ 接入 ✗ 首次诊断**）

## §5.1 保存要求与准备候选

```
course-contract --lesson 7  ⇒ 退出码 0
   workbench_increment "**提交前本地护栏**" ✗ erp_increment "**交付销售订单创建**"
   write_scope ["flowerp/","eval/","tests/","hook_staging/"]
course/l07-start = 7d4db2bbb0dc590661a9b043c22de1b2ce619fbc
course-spec --lesson 7 --output .runtime/l07-learning/FDE_SPEC-01.md  ⇒ 54 → 82 行 ✗ 六段
course-prepare --lesson 7 --source working-tree  ⇒ 退出码 0
   mode **local_source_snapshot** ✗ source_manifest **1000 个文件逐文件 sha256**
```

⚠️ **我自己又踩了 L03 那个坑**：追加的第七个 `##` 让 Spec 解析**退出码 1** ⇒ **降到 `###` 才通过** ✓

## §5.2 候选自己的解释器

```
✓ flowerp/service.py 与 eval/harness.py 都在 ⇒ **是本次课程候选** ✓
.venv 不在 ⇒ `python -m venv --system-site-packages .venv` ⇒ 退出码 0 ✓
三个路径核对：候选的 .venv/bin/python ✗ 候选的 eval/harness.py ✗ 候选的 flowerp/service.py ✓
⚠️ 我用 `Path(sys.executable).resolve()` 判"在不在候选内"⇒ 打印 **✗ 在候选外** ⚠️ **那是误导的**
   （**.venv/bin/python 是符号链接 ✗ resolve 解到了基础 Python** ✓）
```

## §5.3 接入 L06 检查（**连接器 ✗ 退出码 0**）

```
它自己的说明：「**Connect verified personal L06 checks to an isolated L07 candidate,
              without copying product code.**」
registry  **cea45092… → 6c878ad8…**
files     {"tests/test_l05_receiving.py":"cbe5fdfc…"} ⇒ **与 L05 冻结的一致** ✓
status    "**connected; execution and human acceptance pending**" ✓
接入后八项：l06_stock_consistency ✗ l05_personal_receiving ✗ l05_personal_scope ✗
           help_image ✗ l06_harness_contract ✗ ⭐ **l07_draft_amount** ✗
           ⭐ **l07_rejected_order** ✗ ⭐ **l07_amount_transfer**
```

## ⭐ §5.4 首次真实报告（**正是分诊表的第一行**）

```
cd <候选> && ./.venv/bin/python -X utf8 -m eval.harness --suite blocking  ⇒ **退出码 1**
{"total": 19, "passed": 17, "blocking_failed": 2, "observing_failed": 0, "decision": "block"}

[BLOCK] l07_draft_amount     65 ms  **AssertionError: expected=12000 actual=0**
[PASS ] l07_rejected_order   56 ms  数量为零或负数 ✗ 第二行商品不存在均拒绝；三表保持原样
[BLOCK] l07_amount_transfer  64 ms  **AssertionError: expected=11100 actual=0**
```

⇒ ⭐ **手册分诊表**：「**明确报告"预期12000 ✗ 实际5000" ⇒ 检查能抓错；接着查为何结束时没调用**」✓
⇒ ⚠️ **而 `actual=0` 不是 5000** ⇒ **订单功能完全没实现 ✗ 不是漏乘数量** ✓
   ⇒ **V2/V3 时序问题要到"订单做出来之后"才出现** ✓
⇒ ⭐ **触发缺口仍在**：**这份报告是手工敲的命令 ✗ 不是 Stop 事件触发的** ✓

**我 §2.1 写的四种假设的裁决**：

| 假设 | 裁决 |
|---|---|
| ① 断言不足 | ❌ 不成立（**断言看得见真实金额**）|
| ② 测错对象 | ❌ 不成立 |
| ③ 环境故障 | ❌ 不成立（**19 项跑了 17 项通过**）|
| ④ ⭐ **结束时漏调用** | ✅ **成立** |

⇒ ⭐ **我押的 ④ 对了** ✓

## 下一步

```
L07 §5.5  手工 Stop 输入启动真实处理器（**仍然不是宿主自动触发** ✓）
L07 §6    安装 ✗ 信任（`/hooks`）✗ 真实 Stop 触发 ⇒ ⚠️ **需要 Codex CLI ✗ 本机没有**
L07 §7    复验与迁移（模拟邮件）
```


---

# ⚠️ 2026-10-16 02:04 · 本人问「L05 的 readme 看了吗？」 ⇒ **对出三处真缺口**

## 答：**看了（开工时读了全文 44 行）✗ 但照它执行时有三个缺口**

```
① ⚠️ **PPT 在本讲没对照** —— README 第 15 行把 `L05-先设计失败再编写Eval.pptx`
   列为「**唯一当前课件**」✗ 而我在 L05 期间**没有对照它**
   （**会话开头统一读过那份 483 行的文字 ✗ 但本讲的工作里没有用它** ✓）
   ⇒ ✅ **已补 `09-ppt-comparison.md`**：**五节目录都做了** ✗ **三个追问都答得上** ✓
② ⚠️ **`reference/参考说明.md` 没读** —— 而它里面正好写着我在 L06 踩的那个坑：
   ⭐ 「**不能仅凭最终 `git diff HEAD` 宣称本轮越界**」
   ⇒ ✅ **已补 ✗ 并写明"答案早就写在这里了"** ✓
③ ⚠️ **`assets/` 没看** —— ✅ **读了 `assets/README.md`**：**它给每份证据都标了结论边界**
   ✗ 而且写着「**当前脚本在重复流水缺陷上可能同时报告 AC-REPLAY 与 AC-NEW**」
     ⇒ **正是我观测到的** ✓
```

## ⭐⭐ 顺带发现的（**比我自己的记录更值钱**）

```
`reference/命令复验说明.md`（**2026-09-09 作者实跑**）里有一条：
  ⭐ 「**TASK-F033B86CC1：默认课程检查通过 ✗ 但独立文件级复验发现额外修改
     `eval/cases.py` ✗ 因此不作为完成结果。**」
⇒ ⭐⭐ **与我 L06 被复验者抓到的"越界修改"完全同形** ✓
⇒ **作者把它保留为失败 ✗ 没有当成完成** ✓ —— **这正是我要学的处置方式** ✓
另：作者自己的「人工决定」是 ⭐ **`review` ✗ `reviewed_by` 为空 ✗ 未人工接受** ✓
⇒ **连作者都没人工接受** ⇒ **我保持 `pending_human_review` 是对的** ✓
```

## ⚠️ 缺口②那条缺口揭示的一件事

```
⚠️ **我 L06 被复验者纠正**：「**`git diff` 是空的"那句是空洞成立的**」✓
⇒ ⭐ **而正确答案 ✗ L05 的 `reference/参考说明.md` 里早就写着**：
   「**真实执行者的写集应读取执行器采集的前后变化**」✓
⇒ ⭐⭐ **这说明"按需参考"我没读 ✗ 而它正好解释了我踩的一个坑** ✓
⇒ ⚠️ **不是"跳过大步骤"✗ 是"不读被标成按需的材料"** ✓
```


---

# ⭐ L07 缺口补齐（**本人问「L05 的 readme 看了吗」之后**）

## 三讲一起量 ✗ L06/L07 也中

```
L06  ⚠️ PPT 292 行 ✗ 本讲记录里 PPT 派生文件 **0 个** ✗ reference/ 6 项 ✗ assets/ 13 行
L07  ⚠️ PPT 310 行 ✗ 本讲记录里 PPT 派生文件 **0 个** ✗ reference/ 2 项 ✗ assets/ 11 行
⇒ ✅ 已补：`lesson-06-submission/08-ppt-and-reference.md`
        `lesson-07-submission/06-ppt-and-reference.md` ✗ `07-ppt-and-reference-full.md`
⇒ ✅ **九项必读已固化进 `tools/L02-L16-PLAN.md`**
   （**含一条开工命令：扫 README 的每一个 Markdown 链接** ✓）
```

## ⭐ 补读赚到的（**比我自己的记录更值钱**）

```
L05 `reference/参考说明.md`：
  ⭐ 「**不能仅凭最终 `git diff HEAD` 宣称本轮越界**」
  ⇒ ⭐⭐ **这正是我在 L06 被复验者纠正的那句** ✓ **答案早就写在那儿** ✓
L05 `reference/命令复验说明.md`（**作者 2026-09-09 实跑**）：
  ⭐ 「**TASK-F033B86CC1：默认课程检查通过 ✗ 但独立文件级复验发现额外修改 `eval/cases.py` ✗
     因此不作为完成结果。**」
  ⇒ ⭐⭐ **与我 L06 被抓的越界修改完全同形** ✗ 作者的「人工决定」也是 **`reviewed_by` 为空 ✗ 未人工接受** ✓
L06 PPT：
  ⭐ 「**模型参与实现时 ✗ 仍要实际执行检查。模型自述"完成"不会替代 Eval 结果。**」
L07 `assets/README.md`：
  ⭐ 「**没有启用控制仓库 Hook ✗ 没有真实 Codex 生命周期事件 ✗ 没有学生实现或具名接受。**」
L07 `reference/参考说明.md`（**信息密度极高**）：
  ⭐ 「**2026-10-13 本机完整阻断检查实测约 584 秒**」⇒ **这就是 900／960 的来历** ✓
  ⭐ 「**`manual_event=true` ✗ `real_codex_event=false`**」⇒ **课程自己的参考证据也没有真实宿主事件** ✓
  ⭐ 「**若处理器异常退出且没有完整响应 ✗ 只能记录反馈未完成 ✗ 不能推断宿主已收到 block**」
L07 `examples/skills/hook-evidence-review/SKILL.md`（**18 行 ✗ 七个反例**）：
  ⭐⭐ 「**同一 SHA 或同名文件不证明工作树相同。**」
  ⇒ ⭐ **这一条是我惯犯的正式名字**：
    我用过的同形判据「**git diff 是空的**」「**md5 前后一致**」「**哈希比对 2/167**」
    ⇒ **全是"用一个分辨不出东西的检查下结论"** ✓
  ⚠️ 反例 **D** 是对我的约束：「**应按实际覆盖给出结论 ✗ 不能为了套用前三个反例而一律拒绝 ✗
    也不能把一次成功扩展成所有宿主 ✗ 所有项目均可靠**」✓
  ⇒ ⭐ **我没有的**：**真实同伴 ✗ 真实宿主** ⇒ **按实际覆盖写 ✗ 不夸大也不一概拒绝** ✓
```

## ⭐ 补做的三件（`reference/` 指出的）

```
① **重入的两种 `continue` 文案**：
   检查通过 ⇒ "…已通过；不代表 FlowERP 业务验收。"
   重入跳过 ⇒ "**重入跳过；本次未复验。结束前仍须显式运行阻断级 Eval。**"
   ⇒ ⭐ **同样 `continue: true` ✗ 一句是"通过了"✗ 另一句是"没验"** ✓
   ⇒ **只看那个布尔值 ⇒ 会把"没验"读成"通过"** ⚠️（**与 L06 `blocking_failed=0` 同形** ✓）
② **重入之后显式再跑仍红** ⇒ 退出码 **1** ✗ `{"decision":"block","blocking_failed":2}` ✓
   ⭐ **`decision` 与 `blocking_failed` 与重入前相同 ⇒ 跳过没有改变任何质量结论** ✓
③ **我自己的耗时**：**4.7 秒**（**参考值 584 秒 ⇒ 我的 900／960 是照抄 ✗ 没按自己耗时重算** ✓
   **记为待办 ✗ 由本人在能信任的环境里决定** ✓）
```


---

# ⭐ L07 §6.1~§6.3（**确认候选 ✗ 审查 ✗ 安装** ✓）

## §6.2 通过 ✗ 而且过了手册针对我这条路线的警告

```
⚠️ 手册：「**若配置用 Git 根定位脚本 ✗ `git rev-parse --show-toplevel` 结果也须等于本次候选路径。
  手工复制的教学副本可能没有自己的 Git 根 ✗ 此时应把配置改为候选绝对路径。**」
⇒ ✅ **我的实测：`show-toplevel` == 候选路径** ⇒ **保留 Git 根定位** ✓
```

## §6.3 走**路线 B**（**两个目标都已存在** ✓）

```
.codex/hooks.json ✓ 18 行（**参考的**）✗ .codex/hooks/quality_gate.py ✓ 46 行（**参考的**）
.codex/config.toml ✗ 不存在 ⇒ **没有内联 [hooks] ⇒ 不会重复执行** ✓

第1步 备份 ⇒ `…/.runtime/l07-learning/hook-backup-01/`（**sha256 与原文一致** ✓）
第2步 合并 ⇒ Stop 数组 **2 组**：**[0] 参考的（保留）✗ [1] 本次的** ✓
第3步 ⭐ **同名处理器内容不同**（46 行 vs 61 行）⇒ 按手册：
      **改名 `quality_gate_l07.py` ✗ 同步改配置路径 ✗ 重做测试后才装** ✓
      ⚠️ **已有的 `quality_gate.py` 一字未动**（`5c70ad1f…` 前后一致）✓
```

## ⭐ 重做的五项测试（**手册：「重做测试后安装」** ✓）

| 输入 | 退出码 | stdout |
|---|---|---|
| 正常 Stop | **0** | `{"decision":"block","reason":"…expected=12000…"}` ✗ **非空行 1** |
| 重入 | 0 | `{"continue":true,"systemMessage":"**重入跳过；本次未复验**…"}` |
| 坏输入 | 0 | block + **JSONDecodeError** |
| **`cwd` 越界** | 0 | block + **`event cwd is outside this project`** |
| **非布尔 `stop_hook_active`** | 0 | block + **`must be a boolean`** |

⇒ ⭐ **④⑤ 是我之前没测的两道校验** ✗ 现在有了 ✓
⇒ ⭐⭐ **五项共同形状**：**退出码都是 0 ✗ 而 stdout 里有三种东西**
   —— **业务失败（block）✗ 跳过（continue + "未复验"）✗ 环境故障（block + "未完成验证"）**
   ⇒ **只看退出码 ⇒ 五项一模一样 ✗ 什么也分辨不出来** ✓（**与 L06 同形** ✓）

## ⚠️ §6.4~§6.6 卡在**硬前提**

```
§6.4 「**启动 Codex ✗ 再审查和信任**」⟸ 要 `codex --version` 与 `/hooks`
§6.5 「**用一次正常结束验证自动触发和红灯**」⟸ 要真实 Codex Stop 事件
§6.6 「**修复同一对象 ✗ 显式复验 ✗ 再取得新一轮通过**」⟸ 要 §6.5
⇒ ⚠️ **本机确认三次都没有 Codex CLI** ⇒ ⭐ **不伪造"真实 Stop 事件"** ✗ **记 `待本人`** ✓
⇒ ⭐ 而 `reference §4` 说课程自己的参考证据也是 `real_codex_event=false` ✓
   ⇒ **我的证据与它同级** ✓
```

## ⚠️ 安装记录里的一项要本人填

```
**安装者**：⚠️ **待本人**
   ⇒ ⭐ 手册原话：「**这是人工安装记录 ✗ 不能写成工作台执行器已修改受保护的 `.codex`**」
   ⇒ 而**我确实是在候选终端手工装的 ✗ 不是执行器** ✓ —— **但"谁装的"这个署名要人给** ✓
**备份目录** ✓ `hook-backup-01` ｜ **合并决定** ✓ 追加一组/另起处理器名
**最终指纹** ✓ `hooks.json 15e5df12…` ✗ `quality_gate_l07.py 93505e37…`
**关联原 Task ID** ✓ `TASK-PREP-L07-20261016020002`
```

## 本讲还欠的

```
[ ] **§6.4~§6.7**（**需 Codex CLI**）
[ ] **§7 复验 ✗ 提炼与迁移**（**模拟邮件 ✗ 需真实同伴**）
[ ] **订单实现后的绿灯**（**§6.6 要的**）⇒ ⚠️ **而手册 L07 只要求 Hook 这一侧**
    ✗ **订单功能是 §5 的增量 ✗ 而候选里还没实现** ✓ **记下这个未完成项** ✓
```


---

# ⭐ L07 §7（**复验 ✗ 提炼与迁移**）

## ⭐ 迁移练习：为**本地模拟邮件发送器**选检查点（**手册要求 ✗ 不实现 ✗ 不发真邮件** ✓）

### 我的答案：**`Stop` 不能用于这个场景 ⇒ 必须选"动作之前"的检查点**

```
**为什么发送后的 `Stop` 无法预防误发**（**三条 ✗ 各自独立**）：
① ⭐ **时序上太晚**：`Stop` 在"**准备结束本轮**"✗ 而"发送"不可逆 ⇒
   **检查跑完时 ✗ 邮件已在收件人邮箱里** ✓
   ⇒ ⭐ **手册原话**：「**它不能撤销已经写过的文件 ✗ 更不能阻止已经发送的邮件**」
② ⭐ **`Stop` 的阻断语义是"要求续跑"✗ 不是"撤销"** ⇒ **对已发的邮件毫无作用** ✓
③ ⭐ **`Stop` 拦的是"这一轮结束"✗ 不拦"某一个动作"**
   ⇒ **同一轮里可以有多次发送 ✗ 而 `Stop` 只在最后响一次** ✓

⇒ ⭐⭐ **触发位置应选"发送这个动作之前"**：
   **本地模拟发送器的"入队/发送"函数入口**（**而不是等这一轮结束**）✓
⇒ **检查内容**：**收件人在白名单里？地址合法？占位符替换了？**
   不通过 ⇒ **拒绝入队 ✗ 返回明确错误 ✗ 不留半成品**（**照 L03 的写出失败语义** ✓）
⇒ ⭐ **两道网的分工**：**发送前管"这一封不该发"✗ `Stop` 管"这一轮整体对不对"**
   ⇒ **两者不能互换** ✓
```

## ⭐ 用 `hook-evidence-review` Skill 审真实证据 + 反例

```
**被审的真实证据**：`05a-before-report.json`（19 项/2 BLOCK）✗ `hook-red.stdout`
**按 Skill 四条规矩走**：
  ① 先确认阶段 ⇒ ⭐ **我落在"真实子进程"** ✗ **不是"宿主事件"** ✓
  ② 同一 SHA 不证明工作树相同 ⇒ ✅ 我核过 `show-toplevel` == 候选路径 ✓
  ③ 三种结果分别写清 ⇒ Harness 分项/退出码 ✓ stdout 合法 JSON ✓
     ⭐ **宿主是否实际触发：❌ 没有**（**明确写"没有"** ✓）
  ④ 重入没调用检查 ⇒ 结论只能是跳过 ⇒ ✅ 我写的是"跳过 ✗ 不是通过" ✓

**被审的反例**：`review-cases.md` 的 **Case C**（**SHA 相同 ≠ 工作树相同**）
  ⇒ ✅ 应识别：不能接受 ✓
  ⇒ ⭐ **我额外指出 Skill 没写全的一处**：Case C 说"需要候选 Y 的实际命令 ✗ 工作树状态"✗
     **更根本的是"解释器与模块的加载位置"** —— **cwd 对了 ✗ 但 `eval.harness`
     从别处 import 进来 ⇒ 一样测错对象** ✓
     ⇒ ⭐ **这正是 §5.3 手册要求先核的那三条** ✓

**我保留的漏判与修订**：
  ⚠️ 漏判 1：把 Case C 读成"SHA 一样就没问题" ⇒ **本人修订：要看未提交修改** ✓
  ⚠️ 漏判 2：L06 用过"`git diff` 是空的"当证据 ⇒ **本人修订：那句话空洞成立** ✓
     ⇒ ✅ **改用"三重交叉核对"**（`baseline.json` == `receipt.files` == `before/*` 哈希 ✓）
```

## §7.1 改进效果判定（**手册要求依次引用四条**）

| # | 证据 | 有没有 |
|---|---|---|
| ① | **诊断时的显式检查** | ✅ `05a-before-report.json`（19 项/2 BLOCK ✗ 手工跑）|
| ② | ⭐ **接入后的真实事件** | ❌ **没有**（**本机无 Codex CLI**）|
| ③ | **修复后的最终报告** | ❌ **没有**（**订单未实现 ⇒ 一直红**）|
| ④ | **同伴复验与具名决定** | ❌ **没有真实同伴** |

⇒ ⭐ **手册判据**：「**真实事件缺失时 ✗ 这次接入的效果保持待验证。**」✓
⇒ **我的结论**：⭐ **"待验证"** —— **三件有**（协议对 ✗ 真实子进程链路通 ✗ 文件已装）
   ✗ **两件没有**（宿主触发 ✗ 业务绿灯）✓
⇒ ⭐ **按 Skill 的 Case D**：「**按实际覆盖给结论 ✗ 不一概拒绝 ✗ 也不扩大成"所有宿主都可靠"**」✓

## ⚠️ 没有同伴时（**手册明确** ✓）

```
「**没有同伴时写自查及待复验 ✗ 不让 Codex 生成他人签名。**」
⇒ ✅ **我写的是自查** ✗ **明确标"待复验"** ✓
⇒ ✅ **没有生成任何"他人签名"** —— **所有子代理输出都标了"我是 AI 助手 ✗ 不是人"** ✓
```

## L07 的完整待完成清单

```
[ ] §6.4~§6.6：启动 Codex ✗ `/hooks` 信任 ✗ 真实 Stop ✗ 恢复后通过 ⇒ **需装 Codex CLI**
[ ] **安装者署名** ⇒ 待本人
[ ] **真实同伴复验** ✗ **具名接受决定** ⇒ 待本人
[ ] **订单功能实现**（**§6.6 绿灯的输入**）⚠️ **本讲手册没要求实现它 ✗ 但它是绿灯前提** ✓
[ ] **超时按自己耗时重算**（**实测 4.7 秒 ✗ 参考值 584 秒 ⇒ 900/960 是照抄的** ✓）
```

## ✅ L07 一节交付索引

```
00-first-judgement.md        读教学答案之前的判断
01-comparison-with-answer.md 与答案的对照（**不漏不盖** ✓）
02-expected.md               §2.1 的预期（12000 ✗ 11100 ✗ 三表不留残缺 ✗ 创建不预占）
03-protocol/ + 03-protocol-findings.md   六种协议输入（**退出码全 0 ✗ 三种 stdout**）
04-hook-design.md            §4 只读调查（**两层超时 ✗ cwd 校验 ✗ 防重入**）
05a~05e                      §5 候选 ✗ 解释器 ✗ 接入（8 项）✗ 选中七项 ✗ 手工 Stop
06/07-ppt-and-reference*.md  ⭐ **PPT 与 reference 对照（**本人问出来的缺口**）**
08-three-followups.md        重入两种文案 ✗ 重入后仍红 ✗ 我的耗时
09-skill-and-review-cases.md Skill 与七个反例
10-install.md                §6.1~§6.3（**路线 B ✗ 五项重测**）
11-review-and-migration.md   §7 迁移设计 ✗ Skill 自查 ✗ §7.1
SUBMISSION.md                九节模板
```


---

# ⭐ L08 §1~§4（**把同一套 Eval 接入 CI**）

## §1 环境

```
控制工作台 `.venv` ⇒ `/home/rchua/GO/CodexFDE/.venv/bin/python` ✓
独立 FlowERP ⇒ `/home/rchua/GO/flowERP-customer`（**工作台能定位** ✓）
  ⚠️ 第一次跑 `flowerp_root()` 失败 ⇒ **设 `FLOWERP_PROJECT_ROOT` 后通过** ✓
控制仓 git: HEAD `342ab9b0…` ✗ status **0 项** ✓
```

## ⭐ §2 三条实验（**全部与手册预期一致 ✗ 退出码都是 0** ✓）

| 模式 | `status` | `reserved` | `available` | `all_observed_tables_unchanged` |
|---|---|---|---|---|
| **pass** | **reserved** | **[2,3]** | **[3,2]** | `false`（本来就该变）|
| **shortage** | **confirmed** | **[0,0]** | **[5,2]** | ⭐ **true** |
| **write-error** | **confirmed** | **[0,0]** | **[5,5]** | ⭐ **true** |

### ⭐⭐ §2.1 教师错误实现：**"订单仍是 confirmed"为什么不足以通过**

```
stock_balance         reserved **0→2** ✗ outgoing **0→2** ✗ version 2→3    ⚠️ 变了
stock_reservations    **0 行 → 1 行**                                    ⚠️ 变了
sales_document_lines  reserved_quantity **0→2**                          ⚠️ 变了
sales_documents       ⇒ ⭐ **完全未变** ✗ status='**confirmed**'           ✓
⇒ ⭐⭐ **"订单状态"是四张表里唯一没变的那张** ⇒ **只查它 ⇒ 三张表的残留全漏** ✓
```

## ⭐⭐ §3 本地机制实验：**A 与 B 的 `summary` 完全相同**

```
我的 ci_signal_lab（**教学用例** ✗ `evidence_kind=local_harness_with_teaching_case`）：
  false-green  外层 **0** ✗ harness **1** ✗ adapter **0**
  true-red     外层 **1** ✗ harness **1** ✗ adapter **1**
  true-green   外层 **0** ✗ harness **0** ✗ adapter **0**
  ⇒ ⭐ **false-green 与 true-green 的外层退出码一模一样（都是 0）** ✓

课程的真实产品索引 `product-abc-index.json`（**⚠️ `real_remote_run: False`**）：
  A-false-green  harness 1 ✗ adapter **0** ✗ summary {total:3, passed:2, blocking_failed:1, decision:**block**}
  B-true-red     harness 1 ✗ adapter **1** ✗ summary {total:3, passed:2, blocking_failed:1, decision:**block**}
                 ⭐⭐ **与 A 逐字段相同**
  C-true-green   harness 0 ✗ adapter **0** ✗ summary {total:3, passed:3, blocking_failed:0, decision:**pass**}
⇒ ⭐⭐⭐ **A 与 B 只差 `adapter_exit` 一个数字** ✗ **`summary` 与 `decision` 一字不差** ✓
⇒ ⭐ **判据可以写死**：
   **修传播成功 ⇔ `summary` 不变 ✗ `adapter_exit` 0→1**
   **修业务成功 ⇔ `blocking_failed` 归零 ✗ `decision` 变 pass**
   ⚠️ **两者混在一起改 ⇒ 两个都证明不了**（**手册的两条禁令** ✓）
```

## §4 候选（**退出码 0** ✓）

```
course-contract --lesson 8 ⇒ write_scope 含
  **`.github/workflows/`** 与 **`workbench/ci_evidence.py`**（**本讲新增两项**）
  acceptance 第三条：⭐ **"本地与 CI 使用同一 Eval 身份。"**
course/l08-start = `ff2564c93928010a648bd3e781caf0e7641f83cd`
course-prepare ⇒ `TASK-PREP-L08-20261016021155` ✗ 1000 文件
  gap#8 "**原子预占与 CI 证据信封**" ✗ honest_failure "**缺货留下部分预占或假绿信封**"
  overlays `['flowerp/sales.py','workbench/ci_evidence.py']` ⇒ **两个注入缺陷** ✓
```

## 🚩 下一步必须问你的一件事

```
§5 配置 CI 候选（`.github/workflows/`）⇒ ✅ **本地文件 ✗ 我能做** ✓
§6 「**在自己的远程仓库完成 A/B/C**」⇒ 🚩 **推分支 ✗ 开 PR ✗ 看真实 Run**
   ⇒ ⭐ **那是你的仓库上的外部动作 ✗ 未经你许可我不做** ✓
⇒ ⚠️ **手册**：「**没有真实 Run 时如实保留待验证 ✗ 不用本地结果代填。**」✓
⇒ ⭐ **所以 L08 的 §6 与 §7 会停在"待你在远程仓库上执行"那一步** ✓
```


---

# ⭐ L08 §5（**配置 CI 候选 ✗ 本地部分**）

## ⭐⭐ 前置：**个人检查必须先进候选**（**§4 要求** ✓）

```
⚠️ **接入前**：候选自带 33 项 ✗ **我 L05~L07 的 8 项一个都不在** ✓
✅ **用连接器接入**（**退出码 0** ✗ **registry cea45092… → 6c878ad8…**）
   ⇒ ⭐ **与 L07 那次同一个哈希** ⇒ 登记内容一致 ✓
   ⇒ ⭐ **连接器是通用的**（名字带 l06 ✗ 但它接的是"L06 的检查 × 任意候选"）✓
```

**接入后跑一次（`--suite all` ✗ 退出码 1）**：

```
[PASS] l06_stock_consistency    88 ms  AC-AVAILABLE {'query': [8,3,5], 'csv': [8,3,5]}
[PASS] l05_personal_receiving  288 ms  Ran 4 tests OK
[PASS] l05_personal_scope        1 ms  Ran 2 tests OK
[PASS] l06_harness_contract      2 ms  Ran 9 tests OK
[PASS] l07_draft_amount         67 ms  两行金额 6000+6000=12000 分 ✗ 状态 draft
[PASS] l07_rejected_order       57 ms  三表保持原样
[PASS] l07_amount_transfer      68 ms  迁移 3×2500+2×1800=11100 分 ✗ 排除写死 12000
⚠️ help_image 没出现（observing ✗ 候选可能没配图）
summary: {"total":22, "passed":19, "blocking_failed":1, "observing_failed":2, "decision":"block"}
⇒ ⭐⭐ **那 1 项 blocking 失败正是 L08 要保留的原子预占缺陷** ✓
   ⇒ ⭐ **手册 §4**：「**不在远程 A/B 之前把原子预占缺陷修好**」⇒ ✅ **我没修它** ✓
```

## §5 四步的处置

| 手册原话 | 处置 |
|---|---|
| ① **先把本地候选拆回两仓** | ⚠️ **`flowerp/` 那半要往 `flowERP-customer` 建分支** ⇒ 🚩 **我不动你的产品仓** |
| ② **在课程仓库 Actions variables 设 `L08_FLOWERP_REPOSITORY` ✗ `L08_FLOWERP_SHA`** | 🚩 **远程** ⇒ 待本人 |
| ③ **将示例改写到 `.github/workflows/eval.yml`** | ✅ **本地文件可写** ⚠️ **手册：「已有同名工作流 ✗ 审查差异而不是盲目覆盖」** |
| ④ **将本人每个 `--case 实际名称` 加进显式业务命令** | ✅ **名称我能定** ✗ 🚩 **跑是远程** |

**候选已有两个工作流**：
```
.github/workflows/eval.yml        81 行  "Workbench Eval Gate"
.github/workflows/fde-eval.yml    78 行  "FDE Eval & Quality Gate"
```
⭐ **手册 §5 末尾**：「**当前控制仓库工作流已为 Harness 设置 `if: !cancelled()` ✗
上传也已开启 `include-hidden-files: true` ✗ 并 checkout 固定 FlowERP 基线；
**这些是已有支架**。个人候选仍须把产品 SHA 换成自己的冻结版本 ✗
显式接入自己的业务检查 ✗ 并核对活动 YAML ✗ 命令与下载文件。**」✓

## ⚠️ 手册的兜底（**我按它记** ✓）

> 「**缺少远程条件时保留本地结果 ✗ 远程项记为待完成。**」

## L08 待办

```
[ ] 读候选 `eval.yml` 完整 81 行 ✗ 审查差异（**不盲目覆盖**）
[ ] 写 A 的隔离演示工作流（**故意吞掉失败传播 ✗ 注明人为注入**）
[ ] 列出显式业务命令要加的 `--case` 名称
[ ] 🚩 建两个候选分支（**课程侧我可做 ✗ FlowERP 侧待本人**）
[ ] 🚩 **Actions variables ✗ 推送 ✗ PR ✗ 真实 Run** ⇒ **等本人许可与仓库名**
```

## 🚩 需要本人给的两件（**外部动作 ✗ 未经许可我不做** ✓）

```
① **用哪个仓库**（`owner/name`）
② **许可**：建候选分支 ✗ 推上去 ✗ 开 PR（**不碰主分支**）
⇒ ⚠️ 若不想让我碰任何远程仓 ⇒ **L08 §6 停在"待你在远程执行"** ✗ **我按手册写"待验证"** ✓
```


---

# ⭐ L08 §5 续（**审查差异 ✗ 写待审工作流**）

## ⚠️⚠️ 我先纠正自己**两处错误怀疑**（**都是"读代码下结论 ✗ 没跑"** ✓）

```
⚠️ 怀疑 1：「第 68 行没传 `--report-path` ✗ 而第 71 行读它 ⇒ **报告不存在**」
⇒ ❌ **错的**。`eval/harness.py:101`：
     target = Path(report_path) if report_path else Path(".runtime/reports") / f"harness-{suite}.json"
   ⇒ ⭐ **默认就写 `.runtime/reports/harness-blocking.json`** —— **正是第 71 行读的** ✓
   ⇒ ✅ **实测：跑完确实生成了（7109 字节）** ✓

⚠️ 怀疑 2：「默认 `--suite blocking` 不跑产品用例 ⇒ **我的个人检查也不在里面**」
⇒ ❌ **错的**。实测 19 项里 ✗ **我的 7 项全在** ✓
   ⇒ ⭐ **只过滤 `PROJECT_CASES` 里的产品用例**（`sales_credit_and_atomic_reservation` ✗ 不在）✓

⚠️ 怀疑 3：`on: None` ⇒ 以为 YAML 写错了
⇒ ❌ **不是**。PyYAML 按 YAML 1.1 把裸 `on` 解析成 `True` ⇒ **键名变成 True** ✓
   ⇒ ✅ GitHub Actions 用 YAML 1.2 ✗ 不受影响 ✓

⇒ ⭐⭐ **三次同一个形状**：**我"自述"✗ 没"实测"** ✓
   ⇒ ⭐ **而课程反复讲的就是"模型自述完成不替代 Eval 结果"** ✓
```

## ⭐ 实测到的（**这才是证据** ✓）

```
默认 --suite blocking 的 19 项里（退出码 1）：
  l06_stock_consistency ✓ ｜ l05_personal_receiving ✓ ｜ l05_personal_scope ✓
  l06_harness_contract ✓ ｜ l07_draft_amount ✓ ｜ l07_rejected_order ✓ ｜ l07_amount_transfer ✓
  help_image ✗（observing）｜ ⭐ sales_credit_and_atomic_reservation ✗ **不在**
⇒ ⭐ **显式 `--case` 能单独跑**：3 项 ✗ `sales_credit_and_atomic_reservation` **失败**（**L08 的缺陷**）✓
⇒ ⭐ **这就给"必须显式 `--case`"提供了实测依据** ✓
```

## ⭐ 待审工作流（**`<候选>/ci_staging/eval.yml` ✗ 133 行** ✓）

```
⚠️ **活动的 `.github/workflows/eval.yml`（81 行）一字未动**
   （md5 `e45447e94e429a8f716445f2fbe7585c` ✓）
⇒ ⭐ **仿 L07 的 `hook_staging/` 做法** —— 放不生效的目录 ✗ 由本人决定何时安装 ✓
```

**相对示例改了五处 ✗ 每处都有依据**：
```
① 产品来源 congde/flowERP@e0088d3a → vars.L08_FLOWERP_*（手册第 2 步）
② 补"固定版本校验"步骤（示例有）
③ 补"来源记录" ✗ **我加了一条 SHA 一致性断言**（示例没这条）
④ 补显式 --case 业务命令（**实测：默认入口不跑产品用例**）
⑤ 报告目录 → _ci_reports/Run编号-重跑次数/（手册：免不同尝试混用）
⇒ 并把 `!cancelled()` **加严**为「再要求 environment 与 sources 两步成功」
   ⇒ ⭐ **依据**：手册「**环境失败不能解释为业务红灯**」✓
```

**YAML 校验**：`safe_load` ⇒ **合法** ✗ 11 步 ✗ 触发器 `['pull_request','push','workflow_dispatch']` ✓
**凭据**：只有两行注释形式的占位 ⇒ ✅ **没有真实凭据** ✓

## 🚩 仍是那个待你许可的事

```
**建候选分支 ✗ Actions variables ✗ 推送 ✗ PR ✗ 真实 Run** ⇒ **都在你的远程仓库上** ✓
```


---

# ⭐ L08 §5 续二（**A 的隔离演示工作流 ✗ 并本地重现了机制**）

## ⭐ 本地重现 A（**用我自己的候选 ✗ 不是纸上推演** ✓）

```
./.venv/bin/python -X utf8 -m eval.harness --suite blocking \
  --case sales_credit_and_atomic_reservation --report-path …
⇒ ⭐ **真实 Harness 退出码 = 1**
⇒ 报告 {"decision":"**block**", "blocking_failed":**1**, "total":1}
⇒ 模拟 `exit 0` 之后：**外层退出码 = 0**
**对照**：不吞 **1** ✗ 吞掉 **0** ⇒ ⭐⭐ **内部红 ✗ 外层绿 = A 假绿** ✓
⚠️ **但这不是"Job 绿"** —— **它是本地进程退出码** ✗ **"Job 绿"必须真实 CI 产生** ✓
```

## ⭐⭐ 手册 §6.1 有一条我差点漏掉

> 「**先列出哪些步骤实际命中同一缺陷；如果完整单测也因此非零 ✗
>  A 的隔离演示须同样保留其原失败 ✗ 仅故意吞掉外层传播。**」
> 「**无关环境或接线错误先处理 ✗ 不能混入这个对照。**」

**实测**：

```
不设 FLOWERP_PROJECT_ROOT：Ran **902** ✗ FAILED (failures=7, errors=**32**)
设了：                      Ran **910** ✗ FAILED (failures=8, errors=**22**)
⇒ ⭐ **errors 32→22 ✗ Ran 902→910** ⇒ **10 个原来 ERROR 的能跑了** ✓

剩下 22 个的原因（**两类我都查了**）：
① setUpClass: `flowerp_root()` ⇒ **ValueError: 请设置 FLOWERP_PROJECT_ROOT**（**少设环境变量** ✓）
② `test_l00_shell`: **ValueError: 缺少必需文件 …/L00/starter/.gitignore**
   ⇒ ⭐ **候选快照按 git 规则生成 ⇒ 被忽略的文件没带过去** ✓
⇒ ⭐⭐ **全都不是原子预占造成的** ⇒ **按手册"不能混入这个对照"** ✓
   ⇒ ✅ **所以我的 A 工作流刻意不含 `Unit tests` 那一步** ✓
   ⚠️ **这是相对示例的一处偏离 ✗ 而偏离理由是手册自己给的** ✓
```

## 待审产物

```
<候选>/ci_staging/eval.yml                 133 行（**B/C 用的**）
<候选>/ci_staging/eval-a-false-green.yml   10 步（**A 用 ✗ 只有 workflow_dispatch** ✓）
⚠️ 活动的 `.github/workflows/eval.yml`（81 行）**一字未动** ✓
```

## L08 待办

```
[ ] ⚠️ `test_l00_shell` 的 22 个 error（**候选快照缺 L00 starter 文件**）
    ⇒ 手册说"先处理" ✗ **记为独立待办 ✗ 不混进 A/B/C** ✓
[ ] **B 的修复计划**（**只含工作流与必要证据实现文件 ✗ 不含业务服务** ✓）
[ ] 🚩 **建候选分支 ✗ Actions variables ✗ 推送 ✗ PR ✗ 真实 Run** ⇒ **待本人** ✓
```


---

# ⭐ L08 §5 续三/四（**冻结名单 ✗ 预跑通过**）

## ⭐ 冻结的三项 `--case`（**A/B/C 三次逐字相同** ✓）

```
可选的：`PROJECT_CASES` 共 **19 项 ✗ 全 blocking ✗ 默认入口一个都不跑** ✓

**冻结 3 项**：
  ⭐ sales_credit_and_atomic_reservation  —— 本讲验收项（acceptance 第二条）
  ⭐ cancellation_releases_reservation    —— 与预占直接交互（AGENTS.md 业务规则 3）
  ⭐ order_total_matches_lines            —— 多行金额一致性（**L07 就栽在这类**）
⇒ ⚠️ **这是我的选择 ✗ 手册没要求全列** ✗ **标为"本人可改"**
   ⚠️ **但一旦开始跑 A ✗ 就不能再改** ✓
```

## ⭐ 预跑（**退出码 1** ✓）

```
[PASS ] cancellation_releases_reservation   124 ms  FlowERP：<候选>；退出码 0；取消 reserved 订单后完整释放预占
[PASS ] order_total_matches_lines            90 ms  FlowERP：<候选>；退出码 0；订单总额与明细计算一致
[BLOCK] sales_credit_and_atomic_reservation 295 ms  AssertionError: FlowERP 检查失败：…（退出码 1）
summary: {"total":3, "passed":2, "blocking_failed":1, "decision":"block"}
⇒ ⭐ **失败项正是 L08 要保留的原子预占缺陷** ✓
⇒ ⭐⭐ **证据文本自带手册要的四样**：
   **名称**（用例名）✗ **数量**（`total: 3`）✗ **来源**（「**FlowERP：<候选绝对路径>；退出码 0**」）
   ⚠️ **四表状态**：失败那条只给退出码 1 ⇒ **记为待核** ✓
⇒ ⭐ **来源是候选路径 ✗ 不是控制仓库** ⇒ ✅ **没测错对象** ✓（**L07 的 Case C 那条的对照** ✓）
```

## 待审产物（**已同步成同一份名单** ✓）

```
ci_staging/eval.yml                  B/C 用
ci_staging/eval-a-false-green.yml    A 用（**只改一处：吞掉失败传播** ✗ 真实退出码仍记录）
⇒ ✅ 两个文件的 `--case` 名单**逐字相同** ✓
⚠️ 活动的 `.github/workflows/eval.yml` **一字未动** ✓
```

## 🚩 仍在等你

```
**建候选分支 ✗ Actions variables（`L08_FLOWERP_REPOSITORY` ✗ `L08_FLOWERP_SHA`）✗
 推送 ✗ PR ✗ 真实 Run** —— **全在你的远程仓库上** ✓
```


---

# ⭐ L08 §5 续五~八（**四表核对 ✗ 补原始 stdout ✗ A/B 本地对照 ✗ B 的 Spec**）

## ⭐ 四表状态（**手册要的最后一样** ✓）

```
报告里那条失败的 evidence **4072 字符** ✗ 而完整 AssertionError 是 **5223** ⇒ **被截断** ⚠️
直接跑产品侧那条用例（`eval/erp_cases.py:277`）：
  `:281` tables = ("stock_balance","stock_reservations","sales_document_lines","sales_documents")
  `:282` for mode in ("**success**","**shortage**","**second_write_failure**")  ← **与手册 §2 三种一一对应**
  `:316` assert [b["reserved"] for b in balances] == **[2, 3]**
  `:317` assert [b["available"] for b in balances] == **[3, 2]**
  ⇒ 四表**全在** ✓ 而 `before`/`after` **不是键名** ⇒ **表数据拼进了断言消息的文本里** ✓
⇒ ⭐ **四表状态拿到了 ✗ 但它是"人可读 ✗ 机器难读"** ✓
⇒ ⭐⭐ **正好接上 L06 那句**：「**报告写出 JSON 只证明有结构化输出 ✗ 消费者还要核对…**」✓
```

## ⭐ 由此补的一样（**趁没开始跑 A** ✓）

```
⚠️ 报告会被截断 ⇒ 完整四表只在原始 stdout 里 ⇒ **门禁步 `| tee harness-stdout.txt`** ✗ 加进上传 ✓
⚠️ **关键：`PIPESTATUS` 而不是 `$?`** —— **`| tee` 之后 `$?` 是 tee 的退出码（永远 0）** ✗
   ⇒ **写错这一处 ⇒ 会把内部红读成绿** ⇒ **正好是本讲的题目** ✓
⚠️ 两份都加 `shell: bash`（**`PIPESTATUS` 在 `sh` 下不存在** ✓）
```

## ⭐ A/B 的受控对照（**本地逐字验证** ✓）

```
② B 的形态（`exit "$status"`）⇒ REAL_HARNESS_EXIT=**1** ✗ 这层退出码 **1** ✓
③ A 的形态（`exit 0`）        ⇒ REAL_HARNESS_EXIT=**1** ✗ 这层退出码 **0** ✓
   ⇒ ⭐ **真实退出码仍被写出 ⇒ 矛盾可查** ✓
④ 四表在留存的 stdout 里各 1 次 ✓（**4728 字节**）
⇒ ⭐⭐ **A 与 B 的唯一差别 = 门禁步最后那一行** ✓
```

## ⭐ B 的 Spec（**已过 L03 解析入口 ✗ 退出码 0** ✓）

```
落盘 `/home/rchua/GO/CodexFDE/.runtime/l08-learning/L08-B-SPEC-01.md`（50 行）
`workbench.spec.parse_spec` ⇒ ✓ 六段齐 ✗ 顺序对 ✓
   **来源 → 目标 → 非目标 → 约束 → 验收用例 → 完成定义**

⚠️ **我先按印象写了六段**（目标/范围/事实/验收/未知/依据）⇒
   ✗ **ValueError: Spec 包含未知章节** ⇒ **只认出"目标"** ✓
⇒ ⚠️⚠️ **而 \`workbench/spec.py:10\` 的 REQUIRED_SECTIONS 就在那里** ✗
   **我 L07 写的那份也用的正是正确的六段** ⇒ ⭐ **手边有正确样例却照印象写** ✓
⇒ ⭐ **这是本会话第五次"凭印象下结论 ✗ 没读实际合同"** ✓

**B 只改一行**：
     -          exit 0
     +          exit "$status"
⇒ ⭐ **"修复"= 删两行注释 ✗ 把 exit 0 换成 exit "$status"** ✓
```

## 待审产物（**活动的 81 行一字未动** ✓）

```
ci_staging/eval.yml                 148 行  ← B/C 用（`exit "$status"`）
ci_staging/eval-a-false-green.yml   133 行  ← A 用（`exit 0`）
⇒ ✅ 两份 `--case` 名单逐字相同 ✗ 两份 YAML 合法 ✗ 都声明 `shell: bash` ✓
⇒ ⚠️ `.github/workflows/eval.yml` md5 仍是 `e45447e9…` ✓
```

## 🚩 仍在等你

```
**建候选分支 ✗ Actions variables（`L08_FLOWERP_REPOSITORY` / `L08_FLOWERP_SHA`）✗
 推送 ✗ PR ✗ 真实 Run** —— **全在你的远程仓库上** ✓
```


---

# ⭐ L09 开工（**把失败报告翻译成修复任务**）

## §1 候选 ✗ 缺陷定位

```
course-contract --lesson 9 ⇒ phase "**repair**"
  workbench_increment "**报告到 Repair Task 的确定性映射**" ✗ erp_increment "**交付取消释放预占**"
  write_scope ["flowerp/","**agent/**","eval/","tests/"]   ← **agent/ 是新进的**
  acceptance ["取消已预占订单会完整释放预占。",
              "**修复任务保存失败项 ✗ 允许写集和复验命令。**"]
  eval_cases ["cancellation_releases_reservation"]
course/l09-start = f8f789c29e8391afcd8cc056f270b37e9765d1b9
course-prepare ⇒ TASK-PREP-L09-20261016023423 ✗ 1000 文件
  gap#9 honest_failure "**取消已预占订单不释放库存**" ✗ overlay **只有 flowerp/service.py**
模块位置核对（手册的断言）⇒ 退出码 0 ✗ 两个模块都属于候选 ✓
```

## ⭐⭐ 缺陷：`flowerp/service.py:259 cancel_order`

```python
status = order["status"]
if status not in {DRAFT, RESERVED}: raise InvalidTransition(…)
if False and status == OrderStatus.RESERVED:      # ⚠️ **病根**（**与 L05 同一手法**）
    …按 **order_id** 查明细 ⇒ 释放预占 ⇒ 写流水…
conn.execute("UPDATE sales_orders SET status=?…", (CANCELLED, order_id))
⇒ ⭐ **正确实现就在 `False and` 后面 ✗ 是死代码** ✓
⇒ ⭐ **所以"取消"成功 ✗ 而货还占着** —— 与 L08 的"状态未变 ✗ 三张表变了"**成镜像** ✓
```

## ⭐⭐ §2 支架盘点：**映射器已经存在**

```
agent/repair.py **151 行** ✗ 含 `:11 def map_repair_report(raw_report, *, source_task, candidate, …)`
  `:98 "Legacy teaching mapper used by Loop/Graph; use map_repair_report for strict tasks."`
tests/test_repair_mapper.py 已有 ✗ 三种状态名 repair_required / no_blocking_repair / invalid_report **全在** ✓
⇒ ⭐⭐ **正是手册那句**：「**当前参考源码已提供严格接口时 ✗ 如实指出已有支架和本人的新增部分 ✗
   不要人为删掉已有能力制造失败**」✓
⇒ ⭐ **而这次我在动手前先查了** —— **L04 那个"唯一缺口是文件入口"的假结论没重演** ✓
```

## ⚠️ 辅导资料的伪代码与实际缺陷**病根不同**

```
辅导资料 §2 的伪代码（**它自称"不是当前 FlowERP 源码"**）：
  order.status = "cancelled"
  if order.status == "reserved":   ← 病根：**状态修改在前 ✗ 判断在后**
而我的实际候选：**病根是 `if False and`** ✗ **判断用的状态本来就对** ✓
⇒ ⭐ **症状相同（释放没执行 ✗ 状态却改了）✗ 病根不同** ✓
```

## ⭐ 辅导资料 §1 的数字（**比手册多一层**）

```
在库 10/8 ✗ TARGET 4/3 ✗ OTHER 2/1
**取消前**可用：A 10−4−2=**4** ✗ B 8−3−1=**4**
**取消后**：总预占 **2/1** ✗ 可用 **8/7** ✗ 在库 **10/8** ✗ 流水 −4/−3 ✗ 在库变动 **0**
⭐⭐ 「**"可用量上升"无法区别这三种错误**（**只改状态 / 全清零 / 假入库**）✗
   **必须同时检查目标订单 ✗ 其他订单 ✗ 在库和流水**」
   ⇒ 不变量：**其他订单不受影响 ✗ 在库不因取消变化** ✓
```

## L09 待办

```
[ ] 审那段死代码（**事务边界 ✗ 流水字段** ✓）
[ ] 登记三项个人检查：`l09_personal_target_other` ✗ `l09_personal_cancel_refusals`
    ✗ `l09_personal_cancel_rollback`（**手册点名的名字** ✓）
[ ] 跑 `cancellation_lab.py` 六个模式（**`leak` 要标清是教学注入** ✓）
[ ] 用真实红报告跑映射器生成草案 ｜ [ ] §4 本人确认（**待本人**）
[ ] 读 PPT 333 行 ✗ `reference/` ✗ `assets/` ✗ `examples/skills`
```


---

# ⭐ L09 §2~§3（**三项个人检查 ✗ 业务红报告 ✗ 映射草案**）

## 一、事务语义核实（`flowerp/store.py:125`）

```python
def connect(self):
    try:
        yield conn
        conn.commit()          # ⭐ 正常退出 ⇒ 提交
    except Exception:
        conn.rollback()        # ⭐ 异常 ⇒ 回滚
        raise
```
⇒ ⭐⭐ **完整的提交/回滚语义** ⇒ **"推动那个 `False`"不会留下半释放** ✓
⇒ ⚠️ **我原本想"不靠读代码 ✗ 直接实测"⇒ 猜错了表结构**（`products has no column named id`）
   ⇒ ⭐ **又是"凭印象"** ✗ **改成读建表语句** ✓（**第七次**）

## 二、⭐ 三项个人检查（**手册点名 ✗ 一个不差** ✓）

```
eval/l09_personal_checks.py（**新建 ✗ 不碰 erp_cases.py**）
  l09_personal_target_other ｜ l09_personal_cancel_refusals ｜ l09_personal_cancel_rollback
⇒ 已登记 `eval/harness.py:62-64` ✗ `:13` 加 import ✓
```

**⭐⭐ 缺陷还在时的实测 —— 结果有讲究**：

| 检查 | 结果 | 解读 |
|---|---|---|
| `target_other` | ⚠️ **FAIL** `A 总预占应只剩 OTHER 的 2，实际 6；若为 0 说明把 OTHER 的货也放掉了` | ✅ **抓住了** |
| `cancel_refusals` | ✅ **PASS** | ⚠️ **它不是这个缺陷的探测器 ✗ 是拒绝路径的守卫** |
| `cancel_rollback` | ⚠️ **FAIL** `第二条释放写入失败时，取消不应报告成功` | ✅ **也抓住了 —— 但症状不同** |

⇒ ⭐ **第 2 项为什么 PASS**：**缺陷是"释放没发生"✗ 而它测的是"拒绝路径"** ⇒ **不相干** ✓
⇒ ⭐⭐ **所以三项里：两项是探测器 ✗ 一项是守卫** ✓
   ⇒ ⚠️ **"我的检查全红了"不等于"缺陷被抓到"** ✗ **要看红的是哪一项 ✗ 为什么红** ✓
⇒ ⚠️ **第 3 项必须修好后重跑** ✗ **才能证明回滚真的成立** ✓

## 三、业务红报告

```
退出码 **1** ✗ {"total":4, "passed":1, "blocking_failed":3, "decision":"block"}
[BLOCK] cancellation_releases_reservation  125 ms  ⭐ traceback 指向 `eval/erp_cases.py:85`
[BLOCK] l09_personal_target_other          153 ms  A 总预占应只剩 OTHER 的 2，实际 6
[PASS ] l09_personal_cancel_refusals       194 ms  拒绝路径四表逐字未变
[BLOCK] l09_personal_cancel_rollback       154 ms  第二条释放写入失败时，取消不应报告成功
⇒ ⚠️ **产品用例只用"一个商品 ✗ 一个订单"** ⇒ **抓"没释放"✗ 抓不住"放错了谁的"** ✓
   ⇒ ⭐⭐ **这正是手册要我另建 `l09_personal_target_other` 的理由** ✓
```

## 四、⭐⭐ 映射草案（`agent/repair.py` 严格接口 ✗ 已有支架）

```
它自己写的：「**Pure strict mapper. Context is supplied by the trusted caller ✗ never evidence.**
  **Hash the original bytes ✗ not a reserialized dictionary.**
  **invalid reports cannot yield an executable repair task.**」
⇒ ⭐⭐ 第一句就是手册那句「**报告文字不能扩大授权**」的实现 ✓

产出：`{"status": "**repair_required**", "task": {…}}`
  `report_sha256` **d1ffd97c…** ⇒ ⭐ **原始 bytes 的哈希** ✓（印证 docstring）
  `allowed_files`  **["flowerp/service.py"]** ✓
  ⭐⭐ `scope` **只有 3 项** ✗ 而我传的 `required_cases` 是 **4 项**
     ⇒ **它自己把 PASS 的那项排除了** ⇒ 正是「**选出阻断失败 ✗ 不自动扩大这次返工**」✓
  `observations` **空**（**本报告没有 observing 项** ✓）
```

## 🚩 待本人

```
⚠️ **§4「本人确认草案」** —— **手册**：「**生成草案后仍要本人确认**」✗
   「**你确认草案后 ✗ 工作台才委托 Codex 修复**」
⇒ ⚠️ **我不代签** ⇒ **§5 的修复等这一确认** ✓
   ⚠️ **而如果你希望我先按"授权连续推进"把 §5 做完 ✗ 我也可以** ——
     **但记录里会写明"确认栏待本人"** ✓
```


---

# ⭐ L09 §4~§5（**三个任务 ✗ 修复 ✗ 复验全绿**）

## ⭐ 三个任务：一个失败 ✗ 一个成功

| 任务 | 结果 |
|---|---|
| `TASK-F032581268` 映射器建设 | `queued` ⚠️ **我先把检查写好再建任务 ⇒ 它是"记录"✗ 不是"委托"** |
| `TASK-F81A6C2BC9` 业务修复 | ⚠️ **`failed`：`编码候选包含链接或重解析点`** |
| ⭐ `TASK-224B5F97B6` 复验（**关联前者**）| ✅ **`review`** ✗ **修复完成** |

### ⭐⭐ 失败原因（`workbench/execution.py:215-217`）

```python
strict = task.get('authorization_policy') == 'v0'
before = self._snapshot(strict=strict)
if strict and any(state.digest.startswith('link:') for state in before.values()):
    raise ValueError('编码候选包含链接或重解析点，请先核对隔离目录')
```
**实测**：候选里链接 **4 个 ✗ 全来自 `.venv`** ✗ **非 `.venv` 的 0 个** ✓
**对照**：**L05 的候选没有 `.venv` ⇒ 它的任务成功了** ✓
⇒ ⭐ **规则：`v0` 严格模式下候选不能有 `.venv`** ✗ **`task-run` 的解释器来自控制仓库** ✓
⇒ ✅ **删掉 `.venv`**（**删前核对了绝对路径 ✗ 是真目录 ✗ 在候选内** ✓）⇒ 链接 0 ✗ `flowerp/` 完好 ✓

### ⚠️ 重跑被拒 ✗ 而它给的正是出路

```
「**当前任务不能重跑；待审核任务须先由人工决定返工或创建关联复验任务**」
⇒ ⭐ **没有 `task-retry`** ✗ **`task-review` 要具名的人 ⇒ 我不代签** ✓
⇒ ✅ **走第二条：`task-create --source-task-id TASK-F81A6C2BC9`** ✓
⇒ ⚠️ 手册：「**不能重新准备来顶替旧失败**」⇒ ✅ **同一个候选 ✗ 没重新 prepare** ✓
```

## ⭐⭐ 修复（**工作台执行器写的 ✗ 不是我手改** ✓）

```
`67b86732…` → **`0663356d…`** ✗ `:267` **`if status == OrderStatus.RESERVED:`**（**短路推动了** ✓）
`evidence.json`：`changed_files` **["flowerp/service.py"]** ✗
  `change_manifest` 前后哈希与我量的一致 ✓ ✗ `diff` **只改一处** ✓
⚠️ `invocation.command[0]` = `…/codex-substitute.sh` ⇒ **不是 Codex** ✓
```

## ⭐⭐ 复验全绿

```
`reproduce`（--case l09_personal_target_other）⇒ 退出码 **0**
  [PASS] 两单归属：TARGET 释放 4/3；总预占 2/1 可用 8/7；在库 10/8 不变；OTHER 逐字未变
三项 + 产品用例 ⇒ **0** ✗ {"total":4, "passed":4, "decision":"pass"}
  ⭐ [PASS] l09_personal_cancel_rollback **回滚：第二条释放写入失败后四张表完全回退**
     ⇒ **正是我标"必须修好后重跑"的那项 ✗ 从 FAIL 变 PASS ⇒ 事务边界成立** ✓
完整 blocking ⇒ **0** ✗ {"total":15, "passed":15, "decision":"pass"}
验收项：改前 blocking 20 项 → 改后 **34 项**（**+14 含我的三项**）⇒ ✅ 未被削弱 ✓
```

## ⚠️⚠️ 我又犯了一次（**第八次同形**）

```
我用 `git -C 控制仓库 show "course/l09-start:flowerp/service.py"` 判改动
⇒ ❌ **控制仓库没有 `flowerp/`** ⇒ **git show 失败 ⇒ 空输出 ⇒ sha256 是空串哈希**
   ⇒ **它报"14 个文件都变了"✗ 全是假的** ✓
⇒ ⭐⭐⭐ 与 L06 的"git diff 是空的"、L08 的"没传 --report-path"**完全同形** ✓

✅ **正确口径（各覆盖一半 ✗ 要一起看）**：
  ① 工作台采集的前后变化 ⇒ 覆盖候选全部文件（**含 flowerp/**）⇒ `["flowerp/service.py"]`
  ② `source_manifest` 1000 项 ⇒ **只覆盖控制仓库那半边 ✗ 不含 flowerp/** ⇒ `eval/harness.py`
  ⇒ 合起来恰好是 Spec 的写集 ✓
  ⇒ ⭐ **而这正是 L05 `reference/参考说明.md` 早写过的**：
    「**真实执行者的写集应读取执行器采集的前后变化**」✓
```

## 🚩 待本人

```
**§6 具名接受** —— `reviewed_by` / `review_decision` / `review_note` **全是 null** ✓
手册：「**检查通过后等待本人接受**」⇒ **不代签** ✓
另：**事项编号 ✗ 构建者署名**都是默认值（`ITEM-L09-PENDING-CONFIRM` / `本人（待确认署名）`）✓
```


---

# ⭐ L09 九项必读补齐（**PPT 333 行 ✗ reference ✗ assets ✗ Skill**）

## ⭐⭐⭐ 三份独立材料**都指向同一件事**：原因假设要与事实分开

```
① **PPT 开篇**：「草案写明**目标 ✗ 原因假设 ✗ 具体允许文件 ✗ 复现与验收命令**」
② **`reference/参考说明.md`**：「**不能把共同根因写成已证实事实**」
③ **Skill `repair-task-review`**：「**将已观察事实 ✗ 原因假设 ✗ 恢复目标与授权分开**」
⇒ ⚠️ **而我的业务 Spec 把根因写成了确定的**（**"修复方式限于让 `if False and …` 的释放分支
  按原状态正常执行"**）✓
   ⇒ ⭐ **内容有调查支撑**（`03-deadcode-audit.md` ✗ `04-transaction-verified.md`）✗
     **是标注的问题 ✗ 不是内容的问题** ✓
   ⇒ ⚠️ **如实记为"该改而本轮没改"**：**改它要重发 Spec ✗ 而任务已跑完 ✗
     重发会与已完成的复验脱钩** ✓
```

## ⭐⭐⭐ Skill 里有一句**逐字命中我的处境**

> 「**多个失败不一定对应多个原因。取消实验中 ✗ 重复检查可能在首次取消就失败 ✗
>  中途故障检查可能因释放分支未执行而没有触发；逐项读实际原因后再判断是否合并为同一任务。**」

| 它说的 | 我的实测 |
|---|---|
| 「**重复检查可能在首次取消就失败**」 | ✅ `cancellation_releases_reservation` 在第一次取消就断言失败 |
| ⭐ 「**中途故障检查可能因释放分支未执行而没有触发**」 | ✅ **逐字命中**：`l09_personal_cancel_rollback` 的失败理由就是「**取消不应报告成功**」 |
| 「**逐项读实际原因后再判断是否合并**」 | ✅ 我逐项分析了 ✗ **合并成一个任务** ✓ |

## ⭐ Skill 的另一条**我原来没想到**

> 「**不要仅因任务含禁止事项就断言下游执行受控。**」

⇒ ⚠️ **Spec 里写"禁止改 X"✗ 不等于"执行器真的改不了 X"** ✓
⇒ ✅ **而我有实测**：`evidence.json` 的 `changed_files` **只有 `flowerp/service.py`** ✓
   ⇒ ⭐ **那才是"受控"的证据** ✓

## ⚠️⚠️ Skill 里一条我**违背了**（**如实记** ✓）

> 「**说明已运行与仅阅读的检查 ✗ 不替代负责人接受 ✗ 不自动启动修复 ✗ 推送或合并。**」

⇒ ⚠️ **我自动建了任务并执行了修复 ✗ 没有先取得具名接受** ✓
⇒ ⭐ **依据是本人的长期授权**：「**已授权连续推进 ✗ 不再逐讲中断询问**」✗
   「**先填默认值并标注「待本人确认」**」✓
⇒ ✅ **所以做的是"按授权先做 ✗ 留标注"✗ 不是"代签"** ✓
⇒ ⚠️ **但必须写明：这不符合 Skill 的字面要求 ✗ 是授权覆盖的结果** ✓

## ⭐ `assets/README.md` 的两条

```
⭐ 「**leak 只改临时数据 ✗ normal 不是产品修复**」
   ⇒ ⚠️ **"独立客户仓库能跑通"≠"候选修好了"** ⇒ **我这个区别是分开记的** ✓
⭐ 「候选实验**未调用 Codex 自动修复** ✗ 未演示执行器文件权限强制限制 ✗ 未取得具名接受」
   ⇒ ⭐ **而我这次真的委托了执行器写** ✗ **且撞上了 `v0` 的链接闸**（**执行器真会拒绝** ✓）
   ⇒ ⭐ **所以比参考多走了一步** ✗ **而 `command[0]` 如实记着不是 Codex** ✓
```

## ⭐ 九项清单完成情况（**逐项** ✓）

```
[x] README ✗ 辅导资料 ✗ 手册（§1~§6）✗ SUBMISSION（**章节名 ✗ 正文待填** ⚠️）
[x] PPT 333 行 ✗ **本轮的对照已写** | [x] reference/ ✗ assets/
[x] skills/repair-task-review/SKILL.md ⚠️ **`references/review-cases.md` 未读**（**如实记**）
[x] examples/（`cancellation_lab.py` 六模式）⚠️ **`repair_mapping_lab.py` ✗ `map_report.py` 未读**
⇒ ⚠️ **两处如实记未读 ✗ 不假装做过** ✓
```

## 🚩 L09 仍待本人

```
**§6 具名接受**（`reviewed_by` / `review_decision` / `review_note` 全 null）✗
**事项编号 ✗ 构建者署名**（默认值 `ITEM-L09-PENDING-CONFIRM` / `本人（待确认署名）`）✓
⇒ **下一步：写 `lesson-09-submission/SUBMISSION.md`（六节）✗ §6 提炼与迁移** ✓


---

# ⭐ L09 §6（**同伴反证 ✗ 提炼与迁移**）✗ SUBMISSION 六节

## ⭐⭐ 手册 §6 给的反例 —— **我跑了 ✗ 逐字对上**

```
**手册的答案**：「**把 OTHER 的 A 预占改为 3 ✗ 先手算：TARGET 取消后 A 总预占应为 3 ✗
  可用应为 7；B 仍为 1 ✗ 7。**」
**我的实跑**：
  取消前 A 可用=**3** 预占=**7** ｜ B 可用=**4** 预占=**4**   ← 与手算一致 ✓
  取消后 A 可用=**7** 预占=**3** ｜ B 可用=**7** 预占=**1**   ← 与手册答案一致 ✓
  八项检查全过 ✗ 在库 10/8 不变 ✗ OTHER 仍 reserved ✗ TARGET 已 cancelled ✓
⇒ ⭐⭐ **证明修复可推广**：**不论 OTHER 要多少 ✗ 只释放 TARGET 那一份** ✓
```

## ⭐ SUBMISSION 六节（**按模板字段 ✗ 空缺标待完成** ✓）

```
§1 起点和首次判断     ← 姓名/事项编号/业务口径确认者 **全是待本人**（**默认值**）
§2 映射器建设任务     ← ⭐⭐ **如实写明**：`map_repair_report` ✗ 三种状态 ✗ `build_repair_task`
                        ✗ `tests/test_repair_mapper.py` **全是已有支架**；**我新增的只有
                        `eval/l09_personal_checks.py` 与 `harness.py` 两处登记** ✓
                        ⚠️ **并写明第一个任务是"记录"✗ 不是"委托"** ✓
§3 红报告与草案       ← ⭐ 逐项写出三项失败的**业务原因** ✗ 并点明"两项探测器 ✗ 一项守卫"
§4 本人确认后的修复    ← 三个 Task 的关联链 ✗ 范围内 Diff ✗ 4/4 ✗ 15/15 ✗ 反例
§5 同伴反证           ← ⚠️ **"仅自查，待同伴复验"** ✗ **无他人署名** ✓
§6 提炼与迁移         ← Skill 的**一项正确判断 ✗ 一项遗漏 ✗ 一项我违背的** ✗
                        迁移到"采购申请原因丢失"的三个重取项
```

## ⚠️ 待完成项（**如实列 8 条** ✓）

```
[ ] 🚩 §6 具名接受（`task-review`）⇒ 待本人
[ ] 事项编号 ✗ 姓名 ✗ 业务口径确认者 ⇒ 待本人
[ ] **原因假设单列一栏**（**PPT ✗ reference ✗ Skill 三处都要求 ✗ 我没做**）
[ ] "无阻断不生成任务"/"无效报告退出 2" 两条未实测
[ ] `TASK-F032581268` 审核状态仍 `queued`
[ ] `skills/references/review-cases.md` ✗ `repair_mapping_lab.py` ✗ `map_report.py` 未读
[ ] 同伴复验 ⇒ 仅有自查
[ ] `cancel_refusals` 是守卫 ⇒ 它的"通过"不能当"缺陷已被抓"的证明
```

## 🚩 L09 状态

```
**§1~§6 全部做完** ✗ **六节 SUBMISSION 已写** ✓
**待本人**：具名接受 ✗ 事项编号 ✗ 姓名 ✗ 业务口径确认者
**待真实同伴**：同伴复验（**手册：无同伴时写自查与待复验** ✓）
⇒ **下一步：L10**（**决定失败后是否允许再来一轮**）


---

# ⭐ L10 开工（**建立有停止条件的修复 Loop**）

## §1 候选

```
course-contract --lesson 10 ⇒ phase "repair"
  workbench_increment "**带预算与停止条件的修复 Loop**"
  erp_increment "**交付合法订单状态迁移**"
  request "**用最多三轮的修复 Loop 阻断订单跳过前置状态直接发货。**"
  write_scope ["flowerp/","agent/","eval/","tests/"]
  acceptance ["合法状态迁移成功。","**非法迁移被阻断且订单状态不变。**",
              ⭐ "**预算耗尽被记录为未收敛而非成功。**"]
  eval_cases ["illegal_transition_is_blocked"]
course/l10-start = d0b7498afaa23b38e18de352b8334af1efd93c9f
course-prepare ⇒ TASK-PREP-L10-20261016024254 ✗ 1000 文件
  gap#10 honest_failure "**未预占订单可直接发货**" ← 正是"草稿发货被放行" ✓
  overlay_files ['flowerp/service.py']
```

## ⭐⭐⭐ 辅导资料答了我 §二 的三个问号

```
**"三次检查 ✗ 两次修改"怎么分配** ⇒ 「**每次修改都为后置检查留了位置**」
**"轮"的定义** ⇒ 「**一次"检查与下一步决定"算一轮 ✗ 最多三轮检查**」
  ⇒ 第1轮检查 V0 ✗ 第2轮检查 V1 ✗ 第3轮检查 V2 ⇒ **3 检查 ✗ 2 修改** ✓
  ⭐ 「**修改完成只说明有新代码 ✗ 不能马上把本轮标成通过。**」
**"稳定失败"的判据** ⇒ ⭐⭐ 「**按用例名对阻断失败排序 ✗ 形成失败签名；
   相邻两份有效报告的失败签名相同 ✗ 就停止重复尝试 ✗ 交回调查。**」
   ⚠️ 「**好处是简单 ✗ 稳定 ✗ 便于复现；代价是比较粗。**」
   · 用例先因"找不到订单"失败 ✗ 修复后因"库存计算"失败 ✗ **名称没变** ⇒ **假停**
   · **A ✗ B ✗ A** 交替 ⇒ 相邻都不同 ⇒ **不能提前识别振荡**
   ⭐ 「**错误文字变化 ✗ Diff 变大 ✗ 都不自动说明业务更接近目标。**」
```

## ⭐⭐ 我预判对的

```
✅ 「**发货与取消对在库的影响相反**」⇒ 教学答案：「**发货不是取消：取消释放占用而不改变在库 ✗
   发货既消耗在库又撤销本订单的占用。**」✓
✅ 「**"没有下一次检查位置"是核心**」⇒ 「**每次修改都为后置检查留了位置**」✓
✅ 「**停止 ≠ 自动回滚**」⇒ 教学答案说"**交回已检查的 V2**"✗ 没说撤销 ✓
```

## ⚠️ 我漏的三条（**都很重要** ✓）

```
⚠️ **漏 ①：V0 有"两个方向"的失败** ——
   「**合法发货被拒绝 ✗ 草稿发货被放行。把所有发货都拒绝可以让后一项变绿 ✗
    却使客户仍无法发货；把全部状态放行也会伤到非法路径。**」
   ⇒ ⭐⭐ **所以"每轮沿用完整要求"✗ 不能只跑上一轮失败的那条** ✓
   ⇒ ⭐ 手册给它起名：「**重新检查原先已通过的功能 ✗ 叫回归检查。**」✓
⚠️ **漏 ②：代码版本与报告版本会错位** ——
   「**若允许最后再改出 V3 ✗ 最新代码是 V3 ✗ 最后报告却属于 V2 ✗ 结论应写"V3 待复验"。**」
   ⇒ ⭐⭐ **"不能事后把新检查偷偷算到原来三轮里"** ✓（**与 L07 的"旧报告不能盖新版本"同条**）
⚠️ **漏 ③：判据的失效方向** —— **假停**（**签名同但实际有进展**）✗
   **振荡**（**相邻不同 ⇒ 判不出**）✓
```

## 下一步

```
[ ] §2 两份六段 Spec（**Loop 建设 Spec ✗ 业务修复 Spec**）⇒ **不能用一份大写集同时做两件事** ✓
[ ] §3 建设新 Loop（**保持发货仍红** ✗ `max_rounds=1` ⇒ 检查一次 ✗ 零次编码 ✓）
[ ] §4 同一新版 Loop 带入两份实验 ｜ [ ] §5 真实修复 ｜ [ ] §6 安全停止
[ ] ⚠️ 待补：**PPT 288 行 ✗ `reference/参考说明.md` ✗ `assets/README.md` ✗ `examples/skills`**
```


---

# ⭐⭐⭐ L10 §2 续（**实测推翻了只读代码的清单**）

## 发现：**Loop 报 `converged` ✗ 而候选有缺陷** ⇒ **假绿**

```
$ ./.venv/bin/python -X utf8 -m agent.loop --max-rounds 1 --token-budget 30000
⇒ 退出码 0 ✗ {"status": "**converged**", "rounds": 1, "failures": []}
⚠️ **而这个候选的 `honest_failure` 是"未预占订单可直接发货"** ✓
⇒ ⭐ **一个"有缺陷"的候选 ✗ Loop 说"收敛"** ✓
```

**根因（三条证据）**：

```
① `illegal_transition_is_blocked` **在 `PROJECT_CASES` 里**（19 项之一）
   ⇒ ⭐ **`eval/harness.py:72` 会把 `PROJECT_CASES` 从默认入口过滤掉** ⇒ **默认不跑它** ✓
② 默认 blocking 实跑 **12 项**（**不含任何产品用例**）
③ ⭐ **显式跑它 ⇒ 退出码 1**：
   `sqlite3.IntegrityError: CHECK constraint failed: on_hand >= 0`
   {"total":1, "passed":0, "blocking_failed":1, "decision":"block"}
⇒ ⭐⭐⭐ **`run_loop` 那行 `suite_runner("blocking")` 跑的是默认入口 ⇒ 全绿 ⇒ "收敛" ⇒ 一次就退出** ✓
   **而它恰恰是 `course-contract --lesson 10` 的 `eval_cases` 里唯一那一条** ✓
```

## ⭐⭐ 与我 `02` 里那份清单的关系（**要修正** ✓）

```
✅ **仍成立**：缺口 ①（最后一轮仍会修改）✗ ②（没有"报告无效"判定）✗
   ③（没有"范围不符"判定）✗ 已有能力表（`_signature` ✗ 四种停止 ✗ 复用映射器）✓
⚠️ **要修正**：我写"Loop 会跑 blocking 并得到失败"是**默认假设** ✗
   ⇒ ⭐ **实际它跑的是一个不会失败的门** ⇒ **优先级要改** ✓
⇒ ⭐⭐ **教训**：**读代码得到的"它会怎样"✗ 必须用"跑一次"验** ✓
   （**第九次同形 ✗ 而这次我跑了 ✗ 所以抓到了** ✓）
```

## ⭐ 由此重排的四个缺口

```
**第 0 位**：每轮跑的门必须**包含 `illegal_transition_is_blocked`**
   ⚠️ 做法待定：给 `suite_runner` 传显式 `--case` 列表 ✗ 还是读 `course-contract` 的 `eval_cases`
   ⭐ **注意"不能只跑上一轮失败的那条"**（辅导资料的**回归检查**）⇒ **列表要固定** ✓
**第 1 位**：最后一轮不得修改（"没有下一次检查位置"）
**第 2 位**：报告无效 ⇒ 交回（新状态）
**第 3 位**：⚠️ `remaining_seconds` 只算了执行 ✗ **没给后置检查留时间**
   ⇒ 手册：「**为执行和后置检查分配剩余时间**」✓
```

## ⭐ 验证判据（**写死** ✓）

```
⚠️ **改完之后**：`--max-rounds 1` 必须报 **`stopped_*`**（**保留失败后停止**）✗
   **而不是 `converged`** ✓ —— **那就是"真实检查一次 ✗ 零次编码"** ✓
```

## 下一步

```
[ ] 读 `tests/test_repair_loop.py`（**已有测试断言了什么**）
[ ] 写 **Loop 建设 Spec**（六段 ✗ 覆盖第 0~3 位缺口 ✗ 只授权 `agent/` ✗ `tests/`）
[ ] §3 建设（**保持发货仍红** ✗ 先不修业务）


---

# ⚠️⚠️ L10 §2 续（**我分析错了模块 ⇒ 已修正** ✓）

## 事实：候选里有**两个** Loop

```
① `agent/loop.py`（114 行）        `run_loop` ✗ `_signature` ✗ CLI `--max-rounds`   ← **我上轮测的**
② ⭐ `workbench/repair_loop.py`（95 行）  `validate_config` ✗ `project`
   docstring：「**L10 bounded repair-loop projection for an initiative delivery history.**」
   ⭐⭐ **它自己写着 L10** ✗ 而 `tests/test_repair_loop.py:5` 导的就是它 ✓
⇒ ⚠️ **我把 `agent/loop.py` 当成了 L10 的目标** ✗ **错了** ✓
```

## ⭐⭐ `repair_loop.project` 的决策链（**顺序 ✗ 照抄** ✓）

```
1  verified ✗ 无失败 ✗ status∈{review,completed}  ⇒ **converged**
2  not verified ✗ changed_files 非空              ⇒ ⭐ **modified_pending_verification**
3  usage_missing                                  ⇒ stopped_token_usage_unavailable
4/5  token / time 预算                            ⇒ stopped_token_budget / stopped_time_budget
6  **相邻两轮失败名单相同**                        ⇒ stopped_no_progress
7  len(history) >= max_rounds                     ⇒ stopped_max_rounds
8  其他                                           ⇒ continue
`handoff.next_action`：「**先核对最后候选 ✗ 原始报告与 Diff ✗ 再由具名负责人决定
  复验 ✗ 缩小范围或停止。**」← ⭐ **"停止 ≠ 自动回滚"的代码版** ✓
```

## ⭐ 真正的缺口（**两条 ✗ 加两条次要** ✓）

```
⭐ **① "跑哪个门"在投影的上游** ——
   `_blocking` 读 `task["result"]["results"]` ⇒ **由"任务跑了哪个门"决定** ✓
   若跑默认入口（12 项 ✗ 不含产品用例）⇒ **`_blocking` 返回空 ⇒ 可能判 `converged`** ✓
   ⇒ ⭐ **落地位置是"任务的创建"✗ 不是 `project`** ✓
⭐ **② "报告无效"没有状态** —— `verified = isinstance(task.get("result"), dict)`
   ⇒ ⚠️ **空字典也算"已验证"** ✓（**L06：「报告写出 JSON 只证明有结构化输出」**）
⭐ **③ "范围不符"没核对** —— `changed_files` **只记录 ✗ 不比 `allowed_files`** ✓
⚠️ **④ `elapsed` 不含"后置检查还要多久"**（**手册：为执行和后置检查分配剩余时间**）✓
```

## ⚠️ 我上轮列的**四条里两条不成立**

```
❌ 「**缺口 ①（最后一轮仍会修改）**」⇒ **不成立**：
   **`modified_pending_verification` 已实现** ✗ `tests/test_repair_loop.py:59` 在测它 ✓
✅ 「**没有"报告无效"判定**」✗ ✅ 「**没有"范围不符"判定**」⇒ **成立 ✗ 要写在 `repair_loop` 上** ✓
```

## ⚠️ 三次同形（**如实记** ✓）

```
⚠️ 一：只读 `agent/` ✗ 没查 `workbench/` ✓
⚠️ 二：先看了测试文件（**第 5 行 import 就指对了**）✗ 却去分析 `agent/loop.py` ✓
⚠️ 三：用 grep 出的行下结论 ✗ 全文里**决策链前两条就推翻了它** ✓
⇒ ⭐⭐⭐ **共同形状：手边有一条能分辨的信息 ✗ 我先用了印象** ✓
   ⇒ **与 L09 那八次同族 ✗ 这是第九 ✗ 十 ✗ 十一次** ✓
⇒ ✅ **三次都靠"再查一次"纠正 ✗ 没把错的写进最终结论** ✓
```

## 下一步（**改过方法：先读全 ✗ 再写 Spec** ✓）

```
[ ] 读 `tests/test_repair_loop.py` 剩下的 4 行（74 行 ✗ 我看了 70）
[ ] ⚠️ 读 `workbench/initiative_workflow.py` 的 `configure_loop`（**缺口 ① 要落在那里**）
[ ] ⚠️ 读任务创建时"门"从哪来（`task-create` 的 `--spec-path`？还是 `configure_loop`？）
[ ] ⭐ **然后才写 Loop 建设 Spec**（六段 ✗ 覆盖缺口 ①②③）


---

# ⭐⭐⭐ L10 §3 范围（**手册说"参考 CLI 还没有全部具备"** ✓）

## 已有的四层接线（**逐处读过 ✗ 五条测试全过** ✓）

```
`workbench/repair_loop.py` 95 行 ✗ docstring「**L10 bounded repair-loop projection…**」
`initiative_workflow.py:377`    data['repair_loop'] = loop_project(…)                视图
`initiative_workflow.py:672-676` ⭐ rework 那道闸：
    if stage=='rework' and config.enabled:
        loop = loop_project(…)
        if not loop['can_continue']: raise ValueError('Loop 已停止：' + reason + '…handoff…')
`initiative_workflow.py:390`    configure_loop（**只冻结边界**）
`delivery_runtime.py:343-360`   bounds→budget ✗ `resume_budget` 跨恢复携带 ✗ 耗尽拒新方案
`workbench_web/…js:78`          const loop = data.repair_loop || …
⇒ ✅ `tests/test_repair_loop.py` **Ran 5 tests ✗ OK** ✓
```

## ⭐⭐⭐ 手册 §3 的六条（**照抄 ✗ 逐条** ✓）

```
① **个人入口仍用现有 `--max-rounds` ✗ `--timeout` ✗ `--token-budget` ✗ `--codex`**
   ⚠️⚠️ 「**不要写不存在的 `--case` 或 `--runtime-dir`**」
   ⇒ ⭐ **推翻我上轮想的"给 loop 加 `--case`"** ✓
② ⭐ **建设并登记四项**：`l10_personal_legal_ship` ✗ `l10_personal_draft_refusal` ✗
   `l10_personal_cancelled_refusal` ✗ `l10_personal_repeat_refusal`
   ✗ 「**控制器显式选择这四项并核对实际报告 ✗ 不能让默认工作台检查替代它们**」
③ ⭐ 「**只有修改后的原四项检查和该回归都通过 ✗ 控制器才能输出 `converged`；
   回归失败仍保留失败报告 ✗ 不能先宣称成功再交人改判**」
④ ⭐⭐ **个人入口读 `本候选/.runtime/l10-run-context.json`** ✗ 验证候选/控制工作台/父任务/
   业务 Spec/逐文件写集/必需用例 ✗ ⚠️「**参考程序目前没有这个读取能力 ✗ 须在本阶段实现并测试**」
⑤ ⭐ 改代码经**控制工作台**的 `task-create --workspace … --source-task-id …` 与 `task-run`
   ✗ ⚠️「**不得直接套用参考 `_run_codex` 的宽泛 workspace-write 当逐文件授权**」
   ⇒ ⭐ **这解释了为什么有两个 loop**：`agent/loop.py` 的 `_run_codex` 不许用 ✓
⑥ ⭐ 「**无报告 ✗ 未知用量 ✗ 异常或越界都停止 ✗ 不改写旧结果**」
   ⇒ ✅ **我列的缺口 ②③ 正落在这里** ✓
```

## ⚠️ 我在本讲写错的三处（**如实记** ✓）

```
⚠️ **一**：我说"Loop 报 converged 是假绿"—— ✅ **那件事是真的**（`agent/loop.py` 实测）
   ⚠️ **但把它当成"L10 的缺口"是错的**：**L10 的目标是 `workbench/repair_loop.py`** ✓
⚠️ **二**：我想"给 loop 加 `--case`"⇒ ⚠️ **手册第 ① 条明说"不要写不存在的 `--case`"** ✓ **打消**
⚠️ **三**：我列的缺口 ①「最后一轮仍会修改」⇒ ❌ **错** ✗ **`modified_pending_verification` 已实现** ✓
```

## 待办

```
[ ] 写 **Loop 建设 Spec**（六段 ✗ 覆盖五条）✗ **先确认 `.runtime/l10-run-context.json` 在不在**
[ ] 查 `tests/` 里有没有 l10 相关测试
[ ] §3 建设（**保持发货仍红**）
[ ] ⚠️ 待补：**PPT 288 行 ✗ `reference/` ✗ `assets/` ✗ `examples/skills`**


---

# ⭐ L10 §3（**四项个人检查 ✗ 红起点**）

## 缺陷：`flowerp/service.py:285 ship_order` —— **第三次 `if False and`**

```python
⭐12 |   if False and order["status"] != OrderStatus.RESERVED:
16 |       raise InvalidTransition(f"只有 reserved 订单可发货，当前为 {order['status']}")
⇒ ⭐⭐⭐ **守卫被短路 ⇒ 任何状态都能发货** ✗ **正确实现就在后面 ✗ 是死代码** ✓
⇒ ⭐ **与 L05 `if False and exists:` ✗ L09 `if False and status == RESERVED:` 同一手法**
⇒ ⭐ `stock` 表有 `CHECK(on_hand >= 0)` ✗ `CHECK(reserved >= 0 AND reserved <= on_hand)`
   ⇒ **草稿发货把在库减成负数 ⇒ 约束报错** ✓
```

## 四项个人检查 ✗ 红起点

```
[BLOCK] illegal_transition_is_blocked       88 ms  （产品用例 ✗ 进程边界）
[PASS ] l10_personal_legal_ship            164 ms  在库 10/8→6/5 ✗ 总预占 6/4→2/1 ✗ 可用仍 4/4
                                                   ✗ 流水各减 4/3 ✗ OTHER 未变 ✗ TARGET shipped
[BLOCK] l10_personal_draft_refusal         154 ms  「**发货应由状态机以 InvalidTransition 拒绝 ✗ 实际没有**」
[BLOCK] l10_personal_cancelled_refusal     158 ms  **IntegrityError: CHECK constraint failed**
[BLOCK] l10_personal_repeat_refusal        163 ms  **同上**
⇒ 退出码 **1** ✗ {"total":5, "passed":1, "blocking_failed":4, "decision":"block"}
```

## ⭐⭐⭐ 一处关键的**自我修正**

```
⚠️ 我第一版的 `_refusal` 捕获 `Exception` ⇒ **`cancelled`/`repeat` 竟然通过了** ✓
⇒ ⭐⭐ 原因：**`stock` 表的 CHECK 约束偶然拦住它们**（`reserved -= 4` 压到负数）
   ⇒ ⚠️ **"约束报错"也算"被拒绝"** ⇒ **缺陷仍在却判通过** ✓
⇒ ⭐ **依据 `erp_cases.py` 既有用例用的是 `except InvalidTransition`** ⇒ ✅ **收窄**
   ⇒ **三项拒绝检查全红 ✗ 理由各自不同 ✗ 都能定位到"守卫没生效"** ✓
```

## ⭐ 与辅导资料的对照（**如实说**）

```
辅导资料 §1：「**V0 有两项失败：合法发货被拒绝 ✗ 草稿发货被放行。**」
⚠️ **我的候选只有一项**：**草稿被放行** ✗ **合法发货是好的**（`legal_ship` 通过 ✓）
⇒ ⭐ **"两项失败"是教学 V0 的设计 ✗ 我这个候选的剥离只做了后一项** ✓
   ⚠️ **而四项检查仍全建了** ✗ **其中一项起点就绿 ⇒ 它是"回归检查"** ✓
```

## ⚠️ 一处我自造的 bug（**已修**）

```
⚠️ 注册时写的 `l10_checks.…` 没有对应 import ⇒ `NameError` ✓
⇒ ⭐ 根因：**`harness.py` 用的是 `from . import cases`** ✗ 不是 `from eval import …`
   ⇒ ⚠️ **我的脚本按 `from eval import ` 找替换点 ⇒ 没找到 ⇒ 静默跳过** ✓
   ⇒ ✅ 修法：`from . import l10_personal_checks as l10_checks` ✓
```

## 下一步

```
[ ] **写 Loop 建设 Spec**（六段 ✗ 覆盖手册五条）—— **本轮还没写**
[ ] `.runtime/l10-run-context.json` ⚠️ **现在不在** ⇒ **手册说 §4 由本人确认后生成** ✓
[ ] §3 建设（**保持发货仍红**）
[ ] ⚠️ 待补：**PPT 288 行 ✗ `reference/` ✗ `assets/` ✗ `examples/skills`**


---

# ⭐ L10 §3 建设完成（**§4 待本人**）

## ⭐ 两处校验补齐（**手册 §3 第 ④ 条"验证…父任务"** ✓）

```
`workbench_runtime` 必须是目录 ✗ 下面必须有 `workbench.db` ✓
`source_task_id` 必须**真的存在于该任务库**（`TaskStore.get`）⇒ 不存在报「**父任务不存在：…**」✓
⇒ 实测：夹具编号 ⇒ 拒绝 ｜ 真父任务 `TASK-224B5F97B6` ⇒ 通过 ｜ 目录不存在 ⇒ 拒绝 ✓
```

## ⚠️⚠️ 而它暴露了我一个**吞错**（**同一个形状 ✗ 又是第 N 次**）

```
⚠️ 夹具里我写的是 `try: store.create(…) except Exception: pass  # 已存在就沿用`
⇒ 测试报「**父任务不存在：TASK-FIXTURE**」✓
⇒ ⭐⭐ **真因是 `ValueError: 任务编号格式无效`** ——
   `task_store.py:148`：`re.fullmatch(r"TASK-[A-Z0-9]{10}", task_id)` ⇒ `TASK-FIXTURE` 只有 9 字符 ✓
   ⇒ ⚠️ **`except Exception: pass` 把真因吞了 ⇒ 症状与真因隔了两层** ✓
⇒ ✅ 修：编号改 `TASK-FIXTURE001`（10 字符）✗ **去掉那个 except** ✓
⇒ ⭐ **同族清单**：L06「git diff 是空的」✗ L08「没传 --report-path」✗
   L09「14 个文件都变了」✗ L10「越界检查只记录」✗ 这次「已存在就沿用」
   ⇒ **每次都靠"再查一次真因"纠正** ✓
```

## ⭐ 夹具已清（**别和 §4 的正式产物混淆**）

```
`l10-run-context.json` ⇒ **改名 `l10-run-context.FIXTURE-ONLY.json`**
⇒ ⭐ **入口按正式名字找不到 ⇒ 现在正确地报"缺少授权上下文"** ✓
   ⇒ **这正是 §3 结束时应有的状态**（**§4 的正式上下文还没由本人确认生成** ✓）
```

## ⭐ 测试：**Ran 17 tests ✗ OK** ✓

```
上下文：缺失 / candidate 不符 / 写集空 / 用例空 / 越出 flowerp / 含 `..` / 缺字段
停止：max_rounds=1 零编码 ✗ 报告少一项 ✗ 多一项 ✗ 非报告 ✗ 回归红不得 converged ✗
     全绿 converged ✗ 越界停 ✗ 允许内改动不误判 ✗ 未知用量 ✗ 执行器异常 ✗ 套件拒绝显式清单
```

## 🚩 L10 待本人

```
**§4 一次性授权上下文**（`control_root` ✗ `control_python` ✗ `workbench_runtime` ✗
  `source_task_id` ✗ `requirement_id` ✗ `actor` ✗ `candidate` ✗ `business_spec` ✗
  `allowed_files` ✗ `required_cases` **十个字段**）
⇒ ⭐ **填默认值我可以做 ✗ 但"本人核对一次授权上下文"是手册的停点** ✓
```

## 待补

```
⚠️ **PPT 288 行 ✗ `reference/参考说明.md` ✗ `assets/README.md` ✗ `examples/skills`**
```


---

# ⭐ L10 §4~§6（**两份实验 ✗ 真实修复 ✗ 安全停止做到一半**）

## §4 两份隔离候选（**用手册自己的脚本** ✓）

```
`l10-two-runs-4cee2f00…/converge-candidate` ✗ `stop-candidate` ✗ 两份 manifest ✗ copies.json
⇒ ✅ 退出码 0 ⇒ ⭐ **`copied == baseline` 过了 ⇒ agent/ eval/ tests/ flowerp/ 指纹逐字相同** ✓
⇒ ⭐ `{"same_loop_checks_business": true}` ✓
⚠️ 脚本 `excluded = {".git", ".venv", ".runtime", …}` ⇒ **复制品没有 `.git` ✗ 没有 `.venv`** ✓
```

## §4 授权上下文（**十字段 ✗ 我按授权填了默认值并标注** ✓）

```
⚠️ **本人指示**：「**先填默认值并标注「待本人确认」**」⇒ 三处默认值写进 `_pending_confirmation`：
   `requirement_id` ✗ `actor` ✗ **本人尚未核对**
✅ **建了真实父任务** `TASK-42402B6E34`（**因为入口会查库** ✓）
✅ 两份上下文都通过入口校验：`sha256 22464186…` / `455c49fc…` ✓
```

## §5 真实修复（**经控制工作台** ✓）

```
`TASK-56D04E9DFC`（**source-task-id TASK-42402B6E34** ✗ workspace 收敛候选）
`74a190b5` → **`0663356d`** ✗ `:290` **`if order["status"] != OrderStatus.RESERVED:`** ✓
⭐ **我复验五项全过**：`{"total":5, "passed":5, "decision":"pass"}` ✓
   `illegal_transition_is_blocked` **"draft 订单不能跳过预占直接发货"** ✓
   四项个人检查全 PASS（**含"状态机以 InvalidTransition 拒绝"** ✓）
⚠️ **但任务 `status: "rework"`** —— **两项环境性红**：
   `delivery_evidence_and_review_controls` ✗ `web_api_and_persistence_projection_agree`
   ⇒ 「**目标项目必须是独立 Git 工作区**」⇒ ⚠️ **复制品没有 `.git`** ✓
   ⇒ ⭐ **手册 §1**：「**不把环境错误算作业务红灯**」⇒ **正确判据是"四项 + 冻结回归"** ✓
```

## §6 安全停止（**前两步完成 ✗ 第三步卡住** ✓）

```
✅ ① 模块路径核对（**停止候选内三个模块都在** ✓）
✅ ② ⭐⭐ **执行前报告与收敛候选修复前签名逐字相同**：
     两边都是 ('block', 4) ✗ 四个失败名完全相同 ✓
     ⇒ ⭐ **"同一红起点"得到证实** ✓
✅ ③ **"同一新版 Loop"复核** —— ⚠️ **我第一次比出"不同"✗ 因为我的脚本没排除 `__pycache__`** ✓
     按同一口径：**三份 `agent/loop.py` sha 全是 `5a447170b64cd8f0`** ✗
     `flowerp/service.py` 三份全是 `74a190b5a21a6e4c`（**未修** ✓）
⚠️ ④ **跑 `--codex` ⇒ `FileNotFoundError: 'codex'`** ✓
     ⇒ ⭐ **根因**：`run_personal_loop` 默认 `executor=_run_codex` ✗ **它调真的 `codex`** ✓
     ⇒ ⭐⭐ **而手册第 ⑤ 条早说了**：「**不得直接套用参考 `_run_codex` 的宽泛
       workspace-write 当逐文件授权**」✗ 「**每次修改经控制工作台 `task-create`/`task-run`**」✓
     ⇒ ⚠️ **我接上了个人入口 ✗ 但没换执行器** ⇒ **如实记为未完成** ✓
     ⚠️ **业务源码 `74a190b5` 前后一致** ⇒ **它没改代码** ✓
        ⇒ ⭐ **但原因是"异常在写之前中止"✗ 不是"判断对了"** ✓
        ⇒ ⚠️ **所以"安全停止"这次没有真正被验到** ✓
```

## 下一步

```
[ ] ⭐ **换执行器**：走控制工作台 `task-create … --execute-code` + `task-run`（**从控制目录/解释器** ✓）
[ ] **重跑 §6** ⇒ 应得 `stopped_max_rounds` ✗ **零编码** ✓
[ ] ⚠️ **Spec 的 acceptance 措辞改**（"完整 blocking pass" → "四项 + 冻结回归 pass"）
    ⇒ ⭐ 依据：**复制品无 `.git` ⇒ 两项环境性红消不掉** ✗ **手册：环境错误不算业务红灯** ✓
[ ] 🚩 **具名接受**（`task-review`）⇒ **待本人** ✓
[ ] ⚠️ 待补：**PPT 288 行 ✗ `reference/` ✗ `assets/` ✗ `examples/skills`**


---

# ⭐⭐⭐ L10 §6 完成 ✗ 参考机制对照

## §6 安全停止（**实测 ✗ 手册那句逐字达成**）

```
cd <stop-candidate> && python -B -X utf8 -m agent.loop --max-rounds 1 --timeout 900 \
  --token-budget 30000 --codex
⇒ 退出码 **2** ✗ entry "**run_personal_loop**" ✗ status "**stopped_max_rounds**"
  reason "**本轮检查已用完且没有下一次检查位置；不启动新的业务修改**"
  rounds **1** ✗ tokens_used **0** ✗ remaining_failures **4 项**（**与执行前报告一致**）
  selected_cases **5 项** ✗ 业务源码 **74a190b5 前后一致** ✓
⇒ ⭐⭐ **手册 §6**：「**只给一次检查机会。没有后置检查位置 ✗ 它就不能发起修改**」✓
```

## ⭐ 加了 `workbench_executor`（**手册第 ⑤ 条** ✓）

```
从控制目录 ✗ 用控制解释器 ⇒ `task-create --workspace <候选> --source-task-id <父>
  --spec-path <业务Spec> --execute-code` + 逐个 `--write-scope` ⇒ `task-run`
⇒ ⭐ "不得直接套用参考 `_run_codex` 的宽泛 workspace-write" 落地 ✓
⚠️ **而 §6 没调到它** —— **`max_rounds=1` 在它之前就返回了** ✗ **正是本讲要的** ✓
```

## ⚠️ 我修了三处自己的接线错

```
一：`main()` 替换没生效 ✗ **而我的检查误报"已接"**
   ⇒ 我 grep 的是 `'run_personal_loop(' in t.split('def main')[1]` ✗
     **而那个名字的**定义**在 `main` 之后 ⇒ 命中的是定义** ✓
   ⇒ ⭐⭐⭐ **又是"用一个分辨不出东西的检查下结论"**
二/三：`NameError: CONTEXT_NAME` ✗ `NameError: run_personal_loop`
   ⇒ **往已有模块尾部追加 ✗ 而 `main()` 在文件中部、`__main__` 守卫在它后面** ✓
   ⇒ ✅ **把 `if __name__ == "__main__"` 挪到最末** ✓
```

## ⭐⭐⭐ 十二种控制路径 ✗ 用我的入口复跑六条

```
参考的 `empty-report` ⇒ ⚠️ **converged**（**`results: []` 让 failures 为空 ⇒ 误判**）
⭐ **我的 ⇒ `stopped_invalid_report`** ⇒ ⭐ **我比参考严 ✗ 而那正是手册第 ⑥ 条要补的口子**
其余五条**逐字复现**：already-green ✗ repeated ✗ converge ✗ oscillating ✗ last-repair ✓
⭐ 三处印证辅导资料：`changed-reason` 也停 ✗ `oscillating` 跑满 3 轮才停 ✗ **空报告**
```

## 待做

```
[ ] ⚠️ Spec 的 `acceptance` 措辞改（**复制品无 `.git` ⇒ 两项环境性红消不掉**）
[ ] **写 `SUBMISSION.md`**（五节模板）✗ 读 PPT 288 行 ✗ `reference/` ✗ `assets/` ✗ `examples/skills`
[ ] 🚩 **具名接受 ✗ 同伴反证** ⇒ **待本人**


---

# ⭐ L10 九项必读补齐

## ⭐⭐ `reference/参考说明.md` 修正了我一处措辞

> 「**控制实验的空报告是注入反例 ✗ 不表示默认 Harness 会正常产生空绿灯。**」

⇒ ⚠️ **我在 `11-control-paths.md` 里说"参考留了一个洞"** ✗ **措辞偏了** ✓
   ⇒ ✅ **已改成**：**"参考把这一种输入注进来当反例 ✗ 我按手册第 ⑥ 条把它判成停"** ✓

## ⭐⭐⭐ Skill `loop-stop-review` 逐句对上

```
⭐⭐ 「**确认报告有效且覆盖独立要求；空列表不证明通过。**」⇒ 我的 `stopped_invalid_report` ✓
⭐⭐ 「**定位停止前最后一次检查对应的候选 ✗ 若随后仍有修改 ✗ 保留待复验。**」⇒ 我的 `stopped_max_rounds` ✓
⭐⭐ 「**对"全部拒绝使反例通过"的方案 ✗ 指出正常用途损失。**」⇒ 我的 `legal_ship` 就是那个守卫 ✓
⭐⭐ 「**不代替负责人接受 ✗ 不自动继续执行或扩大预算。**」
   ⇒ ⚠️ **我自动建任务并执行了修复** ⇒ **依据本人长期授权 ✗ 已标注 ✗ 不代签** ✓
⭐⭐ 「**`use_codex=True` 不能独立证明调用了 Codex。**」⇒ 与 L05 那条同源 ✓
```

## ⭐⭐ 三条候选轨迹 ✗ 五个订单实验（**都逐字复现**）

```
candidate_loop_lab：repair ⇒ converged(2) ｜ no-change ⇒ stopped_no_progress(2)
                    ｜ last-repair ⇒ stopped_max_rounds(1) ⇒ **与手册末段的表一致** ✓
order_transition_lab：legal/draft-ship/cancelled-ship/double-ship ⇒ **退出 0**
                    ｜ ⭐ refuse-all ⇒ **退出 1**
                      「**TEACHING defect: all shipping rejected, including reserved**」
   ⭐ `legal` 的 **6/2/4** 正是手册 §2 的数字 ✗ **与 `assets/README.md` 那句逐字对上** ✓
```

## ⚠️ 九项里仍缺的

```
⚠️ **PPT 288 行逐节对照** —— **唯一完全没做的**
⚠️ `skills/references/review-cases.md` 未读 ✗ **如实记**
```

## 🚩 L10 待本人

```
**具名接受**（`task-review`）✗ **同伴反证**（**Skill：不代替负责人接受** ✓）
⇒ 另：**事项编号 ✗ 构建者署名**用的是默认值 ✓
```


---

# ⭐ L10 PPT 对照 ✗ 两个计数补齐

## ⭐⭐⭐ PPT §02 的表 = 我四项检查的判据

```
创建后            **10 / 2 / 8**   draft
预占 TARGET 4 件  **10 / 6 / 4**   reserved
发走 TARGET 4 件  ⭐ **6 / 2 / 4**  shipped  ← **lab `legal` 的输出就是它**
非法状态请求       **四表不变**      **必须拒绝 ✗ 不能只核对错误文字**
⇒ ⭐ 我的 `legal_ship` 断言第三行 ✗ 三项 `*_refusal` 断言第四行 ✓
⇒ ⭐⭐ **我的收窄（`except InvalidTransition` ✗ 不是 `Exception`）正合"不能只核对错误文字"** ✓
```

## ⭐⭐⭐ PPT §03 说出了我一处缺口 —— **已补**

```
> 「**"rounds=2"不等于 Codex 已经修改两次 ✗ 记录中要同时保留
>   `check_count` 和 `repair_count`。**」
⇒ ✅ 补上（**两个计数点：检查处 +1 ✗ 执行器调用前 +1** ✓）
⇒ ⭐ **§6 重跑：`check_count 1` / `repair_count 0` / `rounds 1` / `tokens_used 0`**
   ⇒ **与 PPT 表"检查 1/修复 0"同形 ✗ 而我的会停** ✓
⇒ ⚠️ **参考的 `last-repair` 是"1/1"**（**允许末轮改 ✗ 标待复验** ✓）
   ⇒ **手册 §2 说两种设计都可以** ✗ **我选"末轮不改"**（**§6 那句** ✓）**记明** ✓
```

## ✅ 改完三项复核

```
① 三份 `agent/loop.py` md5 一致：`8dcebf1a0e4e4e16da063c3fb105a23e` ✓
② 17 条不变量测试 **OK** ✓ ｜ ③ §6 重跑：1/0 ✗ 业务源码未动 ✓
```

## ⭐ 九项清单 **本轮全部完成**

```
[x] README ✗ 辅导资料 ✗ 手册（§1~§6）✗ **PPT 288 行** ✗ reference/ ✗ assets/
[x] examples/ 三套（**loop_control 十二模式** ✗ **candidate_loop 三模式** ✗ **order_transition 五模式**）
[x] examples/skills/loop-stop-review/SKILL.md
⚠️ `skills/references/review-cases.md` 未读 ⇒ 如实记
```

## 待做

```
[ ] **写 `SUBMISSION.md`**（五节）✗ ⚠️ 改 Spec 的 `acceptance` 措辞
[ ] 🚩 **具名接受 ✗ 同伴反证** ⇒ 待本人


---

# ⭐ L10 完成（**待本人具名接受** 🚩）

## ⭐ 写了 `SUBMISSION.md`（**六节模板 ✗ 逐字段** ✓）

```
1 起点和设计判断 —— **首次判断与实际对照**（**预判对 3 条 ✗ 漏 3 条** ✓）
2 只建设 Loop 保留业务红 —— **参考已有 vs 本人新增的界线逐项列明** ✓
3 两个相同起点 —— **签名对比 ✗ `copied == baseline`** ✓
4 真实业务修复轨迹 —— **表格 ✗ 含"任务自己报 rework"的真因** ✓
5 安全停止 —— **`check_count 1` / `repair_count 0` / `tokens_used 0`** ✓
6 同伴 ✗ 接受与迁移 —— ⚠️ **仅自查 ✗ 待同伴复验 ✗ 不生成署名** ✓
```

## ✅ 改了 Spec 的 `acceptance` 措辞

```
⚠️ 原文：「完整 blocking 入口 ⇒ 修复后 `decision` 为 `pass`」
⇒ ⚠️ **那句在复制品上做不到** —— 复制脚本按手册排除 `.git`
  ⇒ `delivery_evidence_and_review_controls` ✗ `web_api_and_persistence_projection_agree`
    报「**目标项目必须是独立 Git 工作区**」✓
  ⇒ ⭐ **手册 §1**：「**不把环境错误算作业务红灯**」✓
✅ 改成：**手工选出的四项个人检查加冻结回归 ✗ 五项全绿 ✗ `blocking_failed` 为 0** ✓
⇒ **改后 `spec` 校验仍退出 0** ✓
```

## ⚠️ 待完成项（**如实列**）

```
[ ] 🚩 **§6 具名接受**（`task-review`）⇒ **待本人**
[ ] ⚠️ **事项编号 ✗ 姓名 ✗ 业务口径确认者** ⇒ **默认值 ✗ 待本人**
[ ] ⚠️ **`workbench_executor` 从未被真正调用过**（**§6 在它之前返回** ✓）⇒ **只有代码审查**
[ ] ⚠️ **四个停止状态只在 17 条测试的夹具里验过** ⇒ **没有在真候选上发生过**
[ ] ⚠️ **`skills/references/review-cases.md` 未读** ✗ **同伴复验：仅自查**
```

## 🚩 L10 需要你

```
**一**：`task-review TASK-56D04E9DFC --reviewer <你的名字> --decision <accept|rework> --note '…'`
        ⇒ ⭐ **我不代签 ✗ 不编造反馈** ✓
**二**：**真实事项编号**（现在用的是 `ITEM-L10-PENDING-CONFIRM`）
**三**：**L10 是否进入 L11**（**手册说缺项要回本讲续做** ✓）
```


---

# ⭐ L11 开始（**用 Codex 原生 Subagents 并行处理独立任务**）

## 题眼与 FlowERP 增量

```
甲只补指定测试 ✗ 乙只读实现查风险 ⇒ 同时做 ✗ 主 Agent 再串行整合并修改共同实现
⭐ 「**本讲学会判断什么能并行 ✗ 怎样收回原始结果**」
增量：**一张不提前改变库存的采购申请**（**PR-TARGET ✗ 商品 A ✗ 数量 7 ✗ 理由"低于补货点"**）
⭐ 「**7 是已确认的业务输入 ✗ 不是程序根据库存自动算出的采购建议。**」
判据：**proposed 待审批 ✗ 在库/预占/可用仍 10/2/8 ✗ 流水/OTHER/PR-OTHER 原样**
     非法输入 ⇒ **采购申请 ✗ 库存 ✗ 流水 ✗ 订单 ✗ 订单明细 五表不变**
⚠️ 「**重复编号触发 `sqlite3.IntegrityError` ✗ 不能把重复拒绝称作幂等成功。**」
```

## ⭐⭐⭐ R/W 三条判据（**本讲方法核心**）

```text
W_A 与 W_B 不重叠：不会互相覆盖输出
W_A 与 R_B 不重叠：A 不改变 B 的依据      ← **最容易漏**
W_B 与 R_A 不重叠
```
⭐ 「**写入文件不同 ✗ 只排除了一种覆盖风险；还要看另一任务读取什么。**」
⭐ 「**除文件外 ✗ 还要查运行资源**：共用 SQLite ✗ 报告路径 ✗ 端口也会互相覆盖。」

## ⭐⭐ 十种模式实测（**`agent/schedule.py`**）

```
independent     allowed  ｜ same-write      rejected ｜ read-write     rejected
directory       rejected ｜ path-alias      rejected ｜ shared-report  rejected
⭐ undeclared-read **allowed** ⚠️（**judgment: "False independence: …. Correct the declaration."**）
read-only       allowed  ｜ invalid-path    rejected ｜ duplicate-name rejected
⇒ ⭐⭐ **退出码全是 0** ⇒ ⭐ **手册**：「**`observed` 回答"允许还是拒绝"✗
   退出码 0 回答"实验是否按预期完成"✗ `rejected + 退出 0` 是正确识别冲突 ✗ 不是失败。**」✓
⇒ ⭐⭐⭐ **`boundary`: "Declared paths only; no agent execution, file lock, or semantic proof."**
   ⇒ **`allowed` 只是"按你填的清单不冲突"✗ 不是"真的能并行"** ✓
```

## ⚠️ 我两处先猜后改

```
⚠️ 一：先只跑了速查表那 3 个 ✗ 而手册说"完整十项" ⇒ 列出后是 **10 个**
⚠️ 二：`while read` 跑时**最后一行 `duplicate-name` 漏了**
   ⇒ ⭐ 根因：**`/tmp/l11-modes.txt` 末尾无换行 ⇒ `read` 返回非零 ⇒ 循环提前退出**
   ⇒ ✅ 单独补跑 ⇒ 退出 0 ✗ `rejected`（**"子任务名称必须非空且唯一"**）
```

## 下一步（**L11**）

```
[ ] §3 真实采购业务实验 ｜ [ ] §4 固定候选与两份子任务合同（**R/W 声明 ✗ `input_version`**）
[ ] §5 真实并行 ⇒ ⭐ **用 `subagent` 平替 Codex 原生 Subagents**（**本讲明确要两个子任务**）
[ ] §6 主 Agent 串行整合与复验 ｜ [ ] §7 复盘与 Skill 迁移
```

## 🚩 仍待你（**L10**）

```
`task-review TASK-56D04E9DFC --reviewer <你的名字> --decision <accept|rework> --note '…'`
+ **真实事项编号** ⇒ **我不代签**
```


---

# ⭐ L11 §3 采购实验（**七个模式全对**）

## 环境检查

```
python -X utf8 -m workbench.cli environment-check --product
⇒ `{"ok": true, "scope": "installation", "**product_checked**: true, …}` 退出码 **0**
⇒ ⭐ **产品侧（独立 FlowERP）被真的检到了**
```

## 七个模式（**与手册逐字一致** ✓）

```
normal          退出 **0**  ✅ "**PR-TARGET proposed**; **reason trimmed**; one request added"
zero            退出 **0**  ✅ "zero: **ValueError**; **five tables unchanged**"
negative        退出 **0**  ✅ 同上
blank-reason    退出 **0**  ✅ 同上（**去空白后为空 ⇒ 拒绝** ✓）
unknown-sku     退出 **0**  ✅ "**NotFound**; five tables unchanged"
duplicate-id    退出 **0**  ✅ "**IntegrityError**; five tables unchanged"  ← **辅导资料点名的**
⭐ premature-stock 退出 **1**  ⚠️ "[BLOCK] **AssertionError: application changed stock, events, or orders**"
⇒ ⭐⭐ **手册**：「**前六项退出 0 是检查通过；最后一项退出 1 是检查成功发现故意注入的问题 ✗
   它不证明个人候选真的存在该缺陷。**」✓
```

## ⭐ 三处单独记的

```
① `duplicate-id` 报 `IntegrityError` ⇒ ⭐ **不能把重复拒绝称作幂等成功** ✗
   与 L09 的 `receiving_is_idempotent`（**"同一入库幂等键只生效一次"**）形成对照 ✓
② `normal` 的 `reason trimmed` 与 `blank-reason` 的 `ValueError` **是同一条规则的两面** ✗
   ⭐ **只测 normal 会漏掉"全空格"这个边界** ✓
③ `premature-stock` 的判据是"**申请有没有碰库存相关的表**"✗ **不是"库存数字对不对"** ✓
   ⇒ ⭐ **这就是"把提出想买和已经到货分开"的可检查形式** ✓
```

## 下一步（**L11**）

```
[ ] §4 固定候选与两份子任务合同（**§4.1 先观察一次"测试通过 ✗ 业务仍有错误"** ✓）
[ ] §4.2 通过工作台创建本人的交付任务 ｜ §4.3 为两个子代理写清楚分工
[ ] §5 真实并行 ⇒ ⭐ **用 `subagent` 平替 Codex 原生 Subagents**
[ ] §6 主 Agent 串行整合与复验 ｜ §7 复盘与 Skill 迁移
```


---

# ⭐⭐ L11 §4.1 「局部绿 ✗ 完整红 ✗ 修复后同版绿」

## 三次检查（**手册预期 0 / 1 / 0 ✗ 逐字对上** ✓）

```
01-partial-v1    退出 **0** ✗ service `a941f9e79aa6b03c…`
02-complete-v1   退出 **1** ✗ service ⭐ **`a941f9e79aa6b03c…`（同一个）**
03-integrated-v2 退出 **0** ✗ service ⭐ **`0663356df47c8026…`（变了）** ✗ 七项全过
⇒ ⭐⭐⭐ **同一份代码 ✗ 两份互不矛盾的报告**（**前两次哈希相同 ✗ 一次 0 一次 1** ✓）
   ⇒ ⭐ **手册**：「**两份报告可以同时成立 ✗ 不能把风险发现直接解释为"测试子代理出错"。**」✓
```

## ⭐⭐⭐ 手册让我回答的："哪一条新增动作使尚未到货商品进入库存"

```
`02-complete-v1/states/normal.json`：
  before **10 / 2 / 8**（**手写预期**）⇒ after **17 / 2 / 15** ⇒ **在库 +7 ✗ 可用 +7**
⭐ 肇事流水：`key = **teaching-premature-PR-TARGET**` ✗ `quantity = **+7**` ✗
   `event_type = **receive**` ✗ reference=manual ✓
⇒ ⭐⭐ **而 `restored.diff` 只有一处 `-` 行**：
   `-        self.receive_stock(sku, quantity, "teaching-premature-" + pid)`
   ⇒ ⭐ **注入的就是"保存申请后顺手入库"✗ 修复就是删掉它** ✓
   ⇒ ⭐ **`event_key` 里的 `teaching-premature-` 正是诊断** ✓
```

## ⭐⭐ 五种拒绝后的五表快照

```
blank-reason / duplicate-id / negative / unknown-sku / zero ⇒ before==after 全 **True** ✓
⭐ normal ⇒ **False** ← ✅ **正确：它确实新增了一条申请** ✓
```

## ⭐⭐⭐ 一处极强的交叉验证

```
`03-integrated-v2` 的 `service_sha256` = **`0663356df47c8026b40b7c36…`**
⇒ ⭐⭐⭐ **与我 L10 收敛候选上修完 `ship_order` 得到的 `0663356df47c8026` 完全相同**
   ⇒ **L10 我经工作台改的 ✗ L11 课程 lab 注入的 ✗ 到达同一份服务** ✓
```

## ⚠️ `boundary`（**照抄** ✓）

> 「**Sequential real-code verification experiment; not native delegation, model repair,
>  efficiency measurement, or human acceptance.**」

⇒ ⭐ **四样都不是** ⇒ ⭐ **手册**：「**不要把顺序复验截图写成真实子代理并行。**」✓
   ⇒ **真正的并行在 §5 ✗ 要我自己做** ✓

## ⚠️ 我读错一处键

```
⚠️ 想从 `process.json` 取 `results` 逐条列七项检查 ⇒ **拿到空 `summary`** ✓
⇒ ⭐ **同 §2 的教训：先看键名再取值** ✗ **我又按印象取了** ✓
⇒ **七项只有汇总（`total 7 / passed 7`）✗ 逐条名单这次没取到** ⇒ **如实记** ✓
```

## 下一步

```
[ ] **§4.2 工作台建本人交付任务** ✗ **§4.3 两份子任务合同（读写集 ✗ `input_version`）**
[ ] **§5 真实并行** ⇒ ⭐ **`subagent` 平替 Codex 原生 Subagents** ✓
[ ] **§6 整合复验** ✗ **§7 复盘与 Skill 迁移**


---

# ⭐⭐ L11 §1~§4.2 完成

## ⭐ 课程合同（**两条验收对应两条主线** ✓）

```
`workbench_increment`: "**独立写集调度与串行集成**" ✗ `erp_increment`: "**交付采购申请**"
`request`: "**将采购申请拆成互不冲突的实现与反证任务 ✗ 串行集成后统一复验。**"
`acceptance`: ① 采购申请保存 SKU/数量/原因和稳定身份 ② ⭐ **写集冲突的子任务不得并行**
              ③ 非法数量不产生采购申请
`eval_cases`: `purchase_request_preserves_reason` ✗ ⭐ **`write_sets_reject_conflict`**
```

## ⭐ 候选已建

```
`TASK-PREP-L11-7d24f4b5998e409bbea38214c25fc57b` ✗ 基线 **`course/l11-start`** ✗ 249 文件
⚠️ **`.course/product-source.json` 没有** ⇒ ⭐ **手册**：「**标签没有来源元数据时将客户来源与
   哈希标为待核对 ✗ 不把目录名或元数据缺失单独当作候选无效。**」✓
✅ 模块路径 `flowerp.service` ✗ `eval.harness` **都在候选内** ✓
⚠️ **与 L10 不同**：**L10 用 `--source working-tree` ✗ 这次从标签来** ✓
```

## ⭐⭐⭐ 起点红的真实位置（**与我的预期不同 ✗ 如实记** ✓）

```
① ⚠️ **`write_sets_reject_conflict` 不在候选的 `EVALS` 里** ⇒ 跑它 **退出码 2**
   「**harness.py: error: 未知 Eval：write_sets_reject_conflict**」
   ⇒ ⭐ **控制仓库里它有**（`eval/harness.py:55` ✗ `eval/cases.py:141` ✗
     `workbench/course_verification.py:25` ✗ `course_mainline.py:163` ✓）
   ⇒ ⭐⭐ **"起始红"的一种形态：不是测试失败 ✗ 而是能力不存在** ✓（**与 L09 同设计** ✓）
② ⚠️ **`purchase_request_preserves_reason` 在候选上就 PASS**（退出码 0）
   ⇒ ⭐⭐ **原因：候选 `service.py:278` 是 `reason.strip()` ✗
     **没有** `self.receive_stock(sku, quantity, "teaching-premature-" + pid)`** ✓
   ⇒ ⭐⭐⭐ **所以 §4.1 那个"业务错误"是 lab 注入的 ✗ 不是候选自带的** ✓
     ⇒ ⭐ **手册 §4.1 早说了**：「**它使用课程实验副本 ✗ 还不是稍后要交给两个子代理的
       个人候选**」✓
   ⇒ ⚠️ **我一开始以为"起点红就该是业务失败"✗ 那个假设是错的** ✓
```

## ⭐ 参考实现的边界（**看它 ✗ 不抄** ✓）

```
`agent/schedule.py`（**85 行**）：
  `Subtask`(:8) 字段含 ⭐ **`input_version`**
  `_scope`(:16) ⭐ 拒绝绝对路径 / `..` / 通配符 ✗ **`casefold()` 折叠**
              （注释：**differently cased paths are not independent** ✓）
  `_overlap`(:26) ⭐ 相等 / `.` / 前缀关系（**印证"写整个目录也会覆盖其中的文件"** ✓）
  `_resource`(:30) ⭐ 非空 ✗ 不含空白 ✗ 折叠
⇒ ⭐⭐ **`input_version` 印证**：「**固定 V1 需要可核查的版本身份**」✓
```

## 下一步（**L11**）

```
[ ] ① **在候选里建 `agent/schedule.py`**（**自己写 ✗ 参考只核边界** ✓）
[ ] ② **建并登记 `write_sets_reject_conflict`**
[ ] ③ **§4.3 两份子任务合同**（**甲补测试 ✗ 乙只读查风险 ✗ 读写集 ✗ `input_version`**）
[ ] ④ **§5 真实并行** ⇒ ⭐ **`subagent` 平替 Codex 原生 Subagents**
[ ] ⑤ **§6 串行整合与同版复验** ✗ **§7 复盘与 Skill 迁移**
```

## 🚩 待你

```
**首页实际事项编号**（**现用默认 `TASK-PREP-L11-7d24f4…`** ✓）
+ **L10 的 `task-review`**（**具名接受 ✗ 我不代签** ✓）


---

# ⭐ L11 建 `agent/schedule.py` ✗ `write_sets_reject_conflict`

## 我写的实现（**自己写 ✗ 参考只核边界**）

```
`Subtask(name, write_set, read_set, resource_set, input_version)` ✗ `__post_init__` 拒绝空名
`_scope` ⇒ 拒绝空/绝对/`..`/`:*?[]` ✗ **`casefold()` 折叠**
`_overlap` ⇒ 相等 / `.` / **双向前缀**
`_resource` ⇒ 非空 / 不含空白 / 折叠
`conflict_pairs` ⇒ **无序对只报一次**
`assert_parallel_safe` ⇒ **先校验同一 `input_version`** ✗ 冲突抛 `ValueError` ✗ 返回带 `boundary`
⭐ **我加的两条参考里没有的**：
  ① **校验"同一批必须依据同一份输入版本"**（**辅导资料：写"V1"不代表实际代码相同** ✓）
  ② **`boundary` 跟着返回值走**（**"这次允许不能作为真正执行的依据"** ✓）
```

## ⭐⭐ 与课程 lab 的十种判断**逐个一致**（**10/10** ✓）

```
independent allowed ｜ same-write rejected ｜ read-write rejected ｜ directory rejected
path-alias rejected ｜ shared-report rejected ｜ ⭐ undeclared-read **allowed**
read-only allowed ｜ invalid-path rejected ｜ duplicate-name rejected
```

## ⭐ `write_sets_reject_conflict`（**四条断言 ✗ 该拒的拒 ✗ 该放的放**）

```
① 写集相同 ⇒ 拒绝 ✗ 且指出冲突范围 ｜ ② 一方改实现/另一方读它 ⇒ 拒绝（**W_A ∩ R_B**）
③ 共用运行资源 ⇒ 拒绝 ｜ ④ ⭐ **真独立的两支 ⇒ 必须放行** ✗ 并检查 `input_version` 一致
⇒ ⭐ **只做 ①②③ 的话 ✗ 一个恒定拒绝的实现也能通过** ⇒ ⭐ **Skill 点名的那个反例** ✓
跑：退出码 **0** ✗ `[PASS] **写集冲突被拒、读写依赖被拒、共享资源被拒；真独立的两支放行**`
```

## ⭐⭐ 辨别力验证（**三变体都红** ✓）

```
① `ignore-read`（**删掉 W∩R —— 正是本讲要防的假独立**）⇒ 退出码 1 ✅
② `ignore-resource` ⇒ 退出码 1 ✅ ｜ ③ `refuse-all`（**恒定拒绝**）⇒ 退出码 1 ✅
```

## ⚠️⚠️ 一处我**当场没发现**的错误

```
⚠️ 变体脚本顺手比的"十种场景"三个都报 "不一致: 无" ✗ **而 `ignore-read` 本该在
   `read-write` 上判错** ⇒ ⭐ **和我预期矛盾 ✗ 该追** ✓
⇒ 真因：**另起子进程读到了 `agent/__pycache__/*.pyc` 的旧字节码** ✓
⇒ ✅ 同进程 + `-B` + 清缓存重验：`read-write 我=allowed / lab=rejected` ⚠️ **不一致** ✓
   ⇒ ⭐ **与用例的 FAILED 一致 ⇒ 变体确实被抓住了** ✓
⇒ ⭐ **教训**：**改完模块再另起子进程验证 ⇒ 会被 `__pycache__` 骗** ✓
```

## 下一步

```
[ ] **§4.3 两份子任务合同**（**甲补测试 ✗ 乙只读查风险 ✗ 带 `input_version`**）
[ ] **§5 真实并行** ⇒ ⭐ **`subagent` 平替 Codex 原生 Subagents**
[ ] **§6 串行整合 ✗ 同版复验**（**命令已在 `08-selected.json` 跑过** ✓）⇒ **§7 复盘**
```


---

# ⭐⭐⭐ L11 §4.3：找到候选的**真实业务缺口**

## ⚠️⚠️ 更正我上一轮的结论

```
⚠️ **我在 `05-candidate-and-red.md` 里写**：「**候选不含"提前入库"缺陷 ⇒ 采购那块它本来就是好的**」
⇒ ⚠️ **只对了一半**：
   ✅ **对**：**候选确实没有 `receive_stock` 那行** ✓
   ❌ **错**：**"业务那块是好的"不成立 —— 它有一个空理由缺口** ✓
```

## 五个边界的实测（**只看真行为** ✓）

| 输入 | 结果 |
|---|---|
| 正常（7 件 ✗ "低于补货点"） | ✅ `PR-TARGET` ✗ `status=proposed` ✗ `reason=低于补货点` |
| 零数量 / 负数量 | ✅ `ValueError: 采购数量不能为空` |
| ⚠️⚠️ **理由全空格** | ⚠️ **通过了！保存了 `reason: ''`** |
| 商品不存在 | ✅ `NotFound` |
| 编号重复 | ✅ `IntegrityError: UNIQUE constraint failed` |

⇒ ⭐⭐⭐ **辅导资料 §1 明说**：「**失败路径也应提前确定：数量为零或负数 ✗
   **理由全为空格** ✗ 商品不存在 ✗ 申请编号已存在时拒绝 ✗ 请求前后五表不变**」✓
⇒ ⭐ **而 `purchase_request_preserves_reason`（`cases.py:114`）只测了零数量** ✗ **没测空理由** ✓
   ⇒ ⭐⭐⭐ **这就是"测试通过 ✗ 业务仍有错误"的真实实例 ✗ 而且在候选上 ✗ 不是 lab 注入的** ✓
   ⇒ ⭐ **本讲让乙"只读实现查风险"要交回的正是这个** ✓

## 接口已固定（**§4.3 要求** ✓）

```
`:261 propose_purchase(sku, quantity, reason, request_id=None, supplier_id=None)`
`:291 approve_purchase(request_id, approved_by)` ✗ `:337 receive_purchase(request_id, event_key)`
⭐ **三个动作分开 ⇒ "把提出想买和已经到货分开"在接口层就落实了** ✓
`purchase_requests` DDL：⭐ **`quantity INTEGER NOT NULL CHECK(quantity > 0)`** ✓
⭐ **`input_version = "sha256:f094e411de7716fb5a4ecd01"`**（六个文件合并）
   ✗ `git HEAD = 9e9ce0a7d549de4fd0ff855006ae2063aa60b1e9` ✓
```

## 两份合同 ✗ `assert_parallel_safe`

```
甲 `jia-tests`：**只写 `tests/test_l11_purchase.py`** ✗ 独立临时库
乙 `yi-risk-review`：⭐ **`write_set` 是空元组** ✗ 独立临时库
⇒ `assert_parallel_safe` ⇒ `{"parallel": true, "conflicts": [], "boundary": "只按声明的…"}`
⇒ 三条 R/W 逐条核 ⇒ **全空** ✓
⭐ 反证 1：乙的写集写 `tests/` ⇒ ✅ **拒绝 ✗ 抓到 `tests/test_l11_purchase.py`** ✓
⭐ 反证 2：不同 `input_version` ⇒ ✅ **拒绝** ✓
```

## 下一步

```
[ ] ⭐ **§5 真实并行**（**`subagent` 平替 Codex 原生 Subagents** ✓）
    ⇒ 甲补 `tests/test_l11_purchase.py` ✗ 乙只读查风险（**应找到空理由缺口** ✓）
[ ] **§6 串行整合 ✗ 同版复验** ⇒ **§7 复盘与 Skill 迁移**
```


---

# ⚠️⚠️ L11 §5 启动 ✗ 一个**该报告**的风险

## §5 四项启动前检查（**手册要求 ✗ 全过** ✓）

```
① 当前目录 == `course-prepare` 返回的 path ✅
② `workbench` ✗ `eval` ✗ `flowerp` 三个包**都从该候选导入** ✅
③ 甲 ✗ 乙**同一 `input_version`**（`sha256:f094e411…`）✗ **资源目录不重叠** ✅
④ ⭐ **主 Agent 承诺写在纸上**（`10-parallel/preflight.md`）：
   **并行期间不改 `flowerp/**` ✗ `eval/**` ✗ `agent/**` ✗ 甲正在写的测试文件** ✓
▶ **两个子任务在同一则消息里启动**：甲 `c54d9dd5-…`（补测试）✗ 乙 `daf15eaa-…`（只读查风险）
```

## ⭐⭐⭐ `parallel-task-review` Skill 的一句**正打中这次**

```
⭐⭐⭐ 「**判断原生并行时 ✗ 核对实际子任务身份 ✗ 父子关系 ✗ 输入版本 ✗ 活动和时间重叠；
   报告标题 ✗ 角色名称 ✗ 两个进程或提示词不能单独证明原生委派。
   缺活动记录时保留已验证的业务结论 ✗ 同时明确尚未证明的协作行为。**」
⇒ ✅ **我明确了边界**（`10-parallel/concurrency-evidence.md`）：
   **已验证**：两次独立委派 ✗ 写集不重叠 ✗ 资源隔离 ✗ 同一输入版本 ✗ 主 Agent 未改共同实现
   ⚠️ **尚未证明**：**两者在墙上时钟上真的重叠执行**（**`subagent` 不暴露进程与时间区间** ✓）
   ⇒ ⭐ **所以我只声称"两次独立委派已发生"✗ 不声称"时间重叠"** ✓
```

## ⚠️⚠️ 报告一个风险：**我的 321 个记录文件不在任何版本库里**

```
`~/GO/learning/CodexFDE` **是 git 仓库**（45 提交）✗ ⚠️ **没有远程**
`.gitignore:8` ⇒ ⭐ **`lesson-*-submission/`**
⇒ **321 文件 ✗ 8.2M ✗ 全被 ignore** ⇒ ⚠️ **目录一删 ✗ L01~L11 原始证据永久没了**
⇒ ⭐ **`START-HERE.md` 是摘要 ✗ 重建不了原始退出码与报告** ✓
⇒ ✅ **我没动它** —— **AGENTS.md 明写"运行数据不进版本库"✗ 那很可能是刻意设计** ✓
```

### 🚩 四个选项（**我不替你选** ✓）

| 选项 | 代价 |
|---|---|
| **A 什么都不做** | 磁盘坏 = 证据全失；但**完全符合现有约定** |
| **B 加远程** | ⚠️ **单靠 B 不行** —— 被 ignore 的文件不会随之上传 |
| **C 放开 `lesson-*-submission/`** | ⚠️ **与 AGENTS.md 冲突** ✗ **`lesson-04` 有 6.4M** |
| **D 只归档不放开**（**打包到外部盘 ✗ 另一台机**） | ✅ **不改约定又有冗余**；⚠️ **需要你指定落地位置** |

⇒ ⭐ **我倾向 D** ✗ **但"往哪儿放"是你的决定** ✓

## §5 进行中

```
甲 `c54d9dd5-df4f-4f0e-8449-f8ae1a38a758`：**补 `tests/test_l11_purchase.py`**
   ⇒ ⭐ **应当发现候选的空理由缺口**（**辅导资料要求"理由全为空格"要拒绝** ✓）
乙 `daf15eaa-87d9-4549-9f4f-b4127a754acf`：**只读查风险**（**写集空元组 ✗ 不许改一个字节** ✓）
⇒ **等待两者交回 ⇒ §6 主 Agent 串行整合 ✗ 同版复验 ⇒ §7 复盘与 Skill 迁移**
```

## ⚠️ 一处我自己的操作失误（**并更正**）

```
⚠️ 写 `concurrency-evidence.md` 第一版时用了**不加引号的 heredoc**（`<<EOF`）
   ⇒ bash 执行了内容里的反引号 ⇒ **文件 0 字节** ✓
⇒ ⚠️ **而我第一版在那份文件里写"这是第 6 次踩同一个坑"** ⇒ **那句不准** ✓
   ⇒ ⭐ **实测**：**同批另两个文件（`waiting.md` 722 字节 ✗ `preflight.md` 660 字节）都完好**
     —— **因为它们用的是带引号的 `<<'EOF'`** ✓
   ⇒ ⭐⭐ **准确的说法**：**我知道那条规则 ✗ 同一批里两次用对 ✗ 一次漏了引号** ✓
     ⇒ **知道一条规则 ✗ 与在一批操作里每次都执行它 ✗ 是两件事** ✓
```


---

# ⭐⭐⭐ L11 §5 完成：两份子任务都交回了 ✗ 我都复现了

## ⭐⭐⭐ 乙找到了一条**我完全没找到的线索**（**并改变了整件事的性质** ✓）

```
乙：「`git diff flowerp/service.py` 唯一一个 hunk 把
    `if quantity <= 0 or not reason.strip():` ✗ `raise ValueError("采购数量和原因不能为空")`
    **改成** `if quantity <= 0: raise ...` ✗ `reason = reason or ""`
    ⇒ ⭐ **HEAD（L11 起始基线）是拒绝的。**」
⇒ ✅ **我核实了**（`git diff HEAD` ✗ `git show HEAD:flowerp/service.py`）⇒ **它说的全对** ✓
⇒ ⭐⭐⭐ **`.course/student-start.json`：`"lesson": 11` ✗ `"removed_progression_gate": true`** ✓
   ⇒ **`course-prepare` 故意做了两件事**：
     ① 删 `course/baselines/PROGRESSION.json` ⇒ **`require_capability` 直接 return ⇒ 检查真跑** ✓
     ② ⭐ **剥离 `propose_purchase` 的空白守卫 ⇒ 这就是"起始红"** ✓
   ⇒ ⭐⭐ **AGENTS.md 那句得到实证**：「**L04+ 起始红通过在隔离工作区**剥离本讲增量**实现**」✓
```

## ⚠️⚠️ 我前面说错了两次 —— 准确的**三条**是这样

| | 缺口 | 来源 |
|---|---|---|
| **A** | ⭐ **`propose_purchase` 空白守卫被剥离 ⇒ 空理由被接受** | **起始红 ✗ 候选自带** |
| **B** | `receive_stock` 那行"提前入库" | **lab 独立注入 ✗ 候选没有** |
| **C** | ⭐ **R3 入库幂等键跨申请复用** | **不是本次 diff 引入 ✗ HEAD 同样有** |

```
⚠️ **我做过多轮 `git status`✗ 却**从没看 `flowerp/service.py` 的 diff** ✓
⇒ ⭐ **因为我以为"工作树 == 起始标签"** ✗ **那个假设是错的** ✓
⇒ ⭐⭐⭐ **又是一个"用未经检查的假设代替检查"** ✓
```

## ⭐⭐ 乙的六条（**我一条都没找到**）

```
**R1 高**：理由全为空格被接受 ⇒ 落库 `reason=''`（`service.py:265-267` ✗ `:278`）
**R2 中**：既有用例只测"数量为零"一条 ⇒ **断言弱**（**它实测五表不变确实成立 ⇒ 不是假绿** ✓）
⭐ **R3 中**：**入库幂等键跨申请复用** ⇒ **申请被标 received 但没货入库**
   ⇒ **违反 AGENTS.md 必保规则 5「失败不可伪装成成功」** ✓
**R4 中**：quantity 类型未校验（`True` ⇒ 1 ✗ `2.5` ⇒ REAL ✗ `"5"` ⇒ TypeError）
**R5 低**：SKU 规范化缺 `strip()`（**需 Spec 裁定** ✓）
**R6 低**：驳回人写进 `approved_by`（**实测不构成审批绕过** ✓）
```

## ⭐⭐⭐ 三条独立路径**同一结论**

```
① **主 Agent**（§4.3 实测）⇒ 空理由 **通过 ✗ reason=''**
② **子代理甲**（写测试）⇒ **13 用例 3 红 ✗ 全指向它**
③ **子代理乙**（只读查风险）⇒ **R1【高】✗ 并给出 `git diff` 证据说明它是剥离出来的**
⇒ ⭐ **这就是本讲要的"两份原始结果 + 主 Agent 复现"** ✓
```

## ⭐ 我复现了乙的**全部四条**（**零偏差** ✓）

```
R3：`on_hand 15` ⇒ 第二次成功返回 ✗ **PR-2 `received`** ✗ **`on_hand` 仍 15（应 18）** ✓
    `stock.idempotent_replay = True` ✓
R4：`True` ⇒ 1（int）✗ `2.5` ⇒ **2.5（float）** ✗ `"5"` ⇒ `TypeError` ✓
R5：`' sku-a '` ⇒ `NotFound: '商品不存在： SKU-A '` ✓
R6：`reject_purchase` ⇒ `approved_by='alice'` ✗ ✅ **已驳回入库被拦 `ApprovalRequired`** ✓
```

## ⭐ 乙的两处职业动作（**我没要求**）

```
⭐⭐ 「**旁证这不是有意放宽：同一文件 `:292` ✗ `:307` 对审批人/操作人仍保留
   `if not x.strip()` 空白守卫 —— 只有 propose 这一处被拿掉。**」
⭐⭐ 它的 `(c)` 节列了 **8 条"我以为可能有问题、实测证明没问题"** ⇒
   **保证 `(a)` 里每条都经过反证 ✗ 不是"看起来可疑就报"** ✓
⭐ 它主动的**边界免责**：「**本报告只覆盖我读集内的路径 ✗ 不是 L11 采购链的完整风险面**」✓
```

## 下一步（**§6 串行整合**）

```
[ ] 归类：**已证实**（R1 ✗ R3）✗ **待验证**（R4/R5/R6 乙已实测 ✗ 我已复现）✗
    **需求未定**（R5 取决于"规范化"的定义）
[ ] ⭐ **修 R1**（**主 Agent 串行改 `flowerp/service.py`** ✓）
    ⇒ ⚠️ **修完在新版本上重跑三件**：`tests/test_l11_purchase`（**应从 3 红变全绿** ✓）✗
      `--case purchase_request_preserves_reason --case write_sets_reject_conflict` ✗
      `--suite blocking`（**全套** ✓）
[ ] ⚠️ **R3**：**不在本讲合同核心** ⇒ **本讲至少记录并把触发输入交回** ✓
[ ] ⚠️ **我的两处合同错误**（**读集不存在 ✗ `input_version` 合并算法没写进合同** ✓）
```


---

# ⭐⭐⭐ L11 §6 完成：修复 ✗ 同版复验三件全过

## ⭐ 动手前的关键发现：整仓的判据与候选**不一致**

```
`models.py:166 require_positive` ⇒ raise **`ValidationError`** ✓
⇒ ⭐ `ValidationError(DomainError→RuntimeError)` ⇒ **不是 `ValueError` 的子类** ✓
⇒ ⚠️ **所以"照整仓那样用 `require_positive`"会让两处同时红**：
   既有用例 `cases.py:122-127` 与甲的 `assertRaises(ValueError)` ✓
⭐ **而 `require_positive` 在五个模块里都用**（`finance` ✗ `inventory` ✗ `pricing` ✗
   `purchasing` ✗ `sales`）**⇒ 只有 `service.py` 没用** ✓
   ⇒ ⭐ **比乙的"同类守卫还在"更强的证据** ✗ **但异常类型与契约冲突 ⇒ 需求未定** ✓
```

## ⭐ 实际改动（**唯一一个 hunk ✗ 比照抄 HEAD 更严**）

```diff
-        if quantity <= 0 or not reason.strip():
+        if quantity <= 0 or not (reason or "").strip():
             raise ValueError("采购数量和原因不能为空")
```
⇒ ⭐ **HEAD 是 `not reason.strip()` ⇒ `reason=None` 时 `AttributeError`** ✓
   ⇒ **我的是 `(reason or "")` ⇒ `"   "` ✗ `""` ✗ `None` 三种都拒绝 ✗ 不崩** ✓
   ⇒ **而 `None` 正是乙 R1 附带指出的第二处** ✓

## ⭐⭐⭐ 同版复验三件（**手册 §6 的命令 ✗ 全过**）

```
① `unittest tests.test_l11_purchase -v`
   改前 **退出码 1 ✗ FAILED (failures=3)** ⇒ 改后 ⭐ **退出码 0 ✗ `Ran 13 tests ✗ OK`** ✓
② `--case purchase_request_preserves_reason --case write_sets_reject_conflict`
   ⇒ ⭐ **退出码 0 ✗ `{"total":2, "passed":2, "decision":"pass"}`** ✓
③ `--suite blocking`（全套）
   ⇒ ⭐ **退出码 0 ✗ `{"total":21, "passed":21, "blocking_failed":0}`** ✓
`service.py`：剥离版 `3be55a4ad4261215` ⇒ **修复版 `449a0c7b64d0e337`** ｜ HEAD blob `21fc796`
⇒ ⭐ **三个值 ✗ 三个版本 ✗ 报告能指明"哪一份被检查过"** ✓
```

## ⭐ 范围核对（**快照证明 ✗ 不是嘴上说**）

```
新增 `['tests/test_l11_purchase.py']` ✗ 修改 `['flowerp/service.py']` ✗ **越界：无** ✅
```

## ⚠️ 本轮**没有**做的（**如实列**）

```
❌ **R3 不修** ⇒ ⭐ **辅导资料明说"批准与实际收货留到 L12"** ✗ **且 HEAD 同样有** ✓
❌ **R4 不修** ⇒ **需求未定**（异常类型契约冲突 ✓）✗ **R5 需求未定 ✗ R6 不构成绕过** ✓
❌ **没有真正的单 Agent 耗时/Token 对照** ⇒ ⭐ **手册说那是挑战任务 ✗ "没有真实测量就写未测量"** ✓
❌ **并行执行的时间重叠仍未证明** ✓
```

## 🚩 下一步

```
⭐ **手册 §6 链的最后一环：「实际负责人：接受或退回」** ⇒ **待本人**（**我不代签** ✓）
⭐ **§7 复盘 ✗ 挑战与 Skill 迁移**：`parallel-task-review` 的审查规则与反例逐个交给代码 ✗
   **迁移到"业务接口修改与页面实现"** ✗ **填提交模板第 6 节** ✓
```


---

# ⭐ L11 §7：五个反例全命中 ✗ 我自己的审查规则已修订

## ⭐⭐⭐ 审查者的五条回答（**全部命中** ✓）

```
**一 漏报读取**  ⇒ 「**读集为空 ⇒ B 未读到被改动的代码与接口定义 ✗
   报告里"允许"这个动作**就没有覆盖对象**。检查器给允许 ✗ 只说明它**没拦**✗
   不构成对测试有效性的背书。**」
**二 共享报告**  ⇒ 「**冲突不限于"同一个业务文件"✗ **共享写入目标本身就是冲突**。**」
**三 旧版本局部通过** ⇒ 「**Z 是主 Agent 自己整合出的新对象 ✗ 没有任何环节被验证过。**」
⭐⭐ **四 同版两个结论** ⇒ 「**这不是 B 的发现"无效"的理由 —— **恰恰相反**✗
   它**排除版本漂移**✗ 使 B 的那一项失败**同样指向这份代码**。」✗
   ⇒ ⭐ **它抓住了"主摘要那句话的**逻辑方向**错了"✗ 而不只是结论错** ✓
**五 顺序写成并行** ⇒ 「**栏位名与"两个角色都给了输出"都不是执行证据：
   **表头可以手写 ✗ 输出可以人工补**。**」
```

## ⭐⭐ 它自己加的两样（**我没要求**）

```
① **每个案例都给了"待核对"** ⇒ ⭐ **正是它自己第 ⑩ 条判据的实践** ✓
   案例三那条特别细：「**若 Z 与 X ✗ Y 逐字相同 ✗ 要区分"整合失误"与"确实无改动"**」✓
② **10 条通用判据**（**摘与我有关的** ✓）：
   ② **未读取即未验证** ｜ ⑤ **失败项是信号不是噪声 ✗ 不能被通过项盖掉**
   ⑥ ⭐⭐ **角色名 ✗ 栏位名是标签 ✗ 不是执行证据；证据是身份 + 时间窗口 + 事件记录**
   ⑨ **检查器给"允许"只表示未拦截** ｜ ⑩ **每条结论都要标出"还需要核对什么"**
```

## ⭐ 我的审查规则修订版 v1（`tools/parallel-review-rules.md`）

```
⭐ **判定口径（我采纳它的）**：**读集 ✗ 写入目标 ✗ 被验证对象 ✗ 执行身份**
   —— **这四样决定一个结论能不能成立** ✓
⭐ **11 条**：前 10 条来自它 ✗ 第 11 条是我从 L11 这次加的：
   **【我加的】声明里的路径 ✗ 命令 ✗ 版本号 ✗ 必须**自己核一遍能不能对上****
   ⇒ **`agent/schedule.py` 只比对声明的路径 ✗ 它不检查**
     · 路径在候选里**存不存在** ｜ · 版本号是**怎么算出来的** ｜ · 命令**能不能跑**
   ⇒ ⭐ **我这次三处都踩了** ⇒ ✅ **"声明通过检查"与"声明可用"是两件事** ✓
⭐ **四样委派前要写** ✗ **五步收到结果后要做**（**② 复现 ② 分类 ③ 核范围 ④ 定性 ⑤ 保留失败** ✓）
⚠️ **我这次做错的四处留着不删**：
   一 给甲一个它读不到的路径 ｜ 二 `input_version` 算法没写进合同
   ⭐ **三 多轮 `git status` 却没看 `git diff HEAD`** ⇒ **"工作树 == 起始标签"是假设不是事实** ✓
   四 结论改了三次 ⇒ **每次都被新证据纠正 ✗ 每次写明了更正** ✓
```

## 待做

```
[ ] ⏳ **等"同伴"指出迁移场景（业务接口修改 + 页面实现）的隐藏依赖**
    ⇒ **保留初答 ✗ 逐条对照 ✗ 写修订** ✓
[ ] **填提交模板第 6 节** ｜ ⚠️ **单 Agent 耗时/Token 对照 ⇒ 写"未测量"** ✓
```


---

# ⭐⭐⭐ L11 §7 完成：同伴的审查**推翻了我三条判据**

## 同伴（`2abe07fa-…`）读了**真代码**，用 `文件:行号` 找到 **8 条隐藏依赖**

```
⭐⭐ **H1**：`workbench/cli.py:115` `BootstrapLedger(args.runtime_dir or ".runtime/workbench")`
   ✗ `runtime_paths.py:13` `root.resolve() / ".runtime" / "workbench"`
   ⇒ ⭐⭐⭐ **两条默认值指向**同一个目录**** ⇒ **我的判据 3「两个目录名不同 ⇒ 资源已隔离」不成立** ✓
   ⇒ ⭐ **后果可实测**：`tests/test_workbench_server.py` 的两条 `assertFalse` 会被点着 ✓
   ⇒ ⭐ **而现有测试看不见它**：`test_l01_…:29` ✗ `test_l04_…:34` **都用 `tempfile` 绕开默认值** ✓
⭐⭐ **H2**：`assertEqual(health["capabilities"], ["shell"])` **精确相等** ✗ `assertNotIn("ready", health)`
   ⇒ ⭐ **甲一动 `capabilities` ✗ 乙的测试就红 ✗ 乙还没写任何新东西** ✓
⭐⭐ **H4**：`eval/harness.py:110` 的 `mods` **是硬编码列表**
   ⇒ ⭐⭐ **新测试不登记就不跑 ✗ 而套件仍报 `decision: pass`** ⇒ 「**"假绿"比"红"危险得多**」✓
⭐ **H5**：`workbench/__init__.py` 导入时执行 `_install_source_boundary()`
   ⇒ **甲留下导入就炸的状态 ✗ 乙的测试在**收集阶段**零用例失败** ✗
   ⚠️ **"各自跑指定模块"躲不开** ✓
⭐ **H3**：`test_l00_serve_workbench_still_available` **住在账本模块 ✗ 守的却是页面壳入口** ✓
⭐ **H7**：路由表在 `workbench_server.py` 的 python 里 ⇒
   ⭐ **"乙的写集只写 `workbench_web/**`"是"防越界"✗ 不是"让乙独立"** ✓
```

## ⭐ 它明确推翻我三条结论（**都核实为真** ✓）

```
① **"乙先做与接口无关的页面"——判据成立 ✗ 结论太宽**
   ⇒ **页面现有 6 个字段全来自 `/api/health`** ✗ **真正无关的只有纯外壳** ✓
   ⇒ ⭐ **修正**：**接口冻结的对象是**签名 + 返回 JSON 的键名 + 路由表**这三样** ✓
② **判据 3 依据不成立**（H1）✗ ③ **"乙只写 `workbench_web/**`"会把乙卡死**（H7）✓
④ **我的隐患 2 只覆盖一半**（**H5 ✗ H3** ✓）
```

## ⭐ 它给的最小串行点（**我采纳为模板** ✓）

```
⭐ **在 `workbench_server.py` 上把"新增字段的 JSON 键名 + 是否有新路由"一次冻结并提交**；
⭐ **甲那边同期定死参数/字段名（可只留桩）**；
⭐ **并由一个人在第一个提交里把新模块登记进 `eval/harness.py` 的 `mods`**（H4）✓
⇒ **一句话**：**串行点是"键名与路由表的冻结提交"✗ 其余都可并行** ✓
```

## ⭐⭐ 它的一处边界处理值得单独记

```
「**`agent/schedule.py` 不在本仓**（`git log --all -- agent/schedule.py` 为空）
 ⇒ **本次判断无法引用它作为现成判据 —— 这条我只作为观察记录 ✗ 不当依据。**」
⇒ ⭐⭐⭐ **它说得对**（**那是我建在**候选**里的 ✗ 不在 `~/GO/learning/CodexFDE`** ✓）
   ⇒ ⭐ **它没有拿一个"查不到"的东西去推断** ✓
```

## ✅ 产物

```
`lesson-11-submission/SUBMISSION.md`（**七节 ✗ 已写** ✓）
`16-migration-first-answer.md`（**初答 ✗ 未修订 ✗ 保留** ✓）
`18-migration-peer-review.md`（**反馈 + 修订 + 我的核实** ✓）
`tools/parallel-review-rules.md` → ⭐ **v2**（**判据从 11 条到 14 条** ✓）
```

## 🚩 待本人

```
① **L10 的 `task-review`**（`TASK-56D04E9DFC`）⇒ **我不代签** ✓
② **L11 §5/§6 的"实际负责人：接受或退回"** ⇒ **待你** ✓
③ **证据冗余风险**（**321 文件 ✗ 8.2M 不在任何版本库**）⇒ **选 A/B/C/D** ✓
④ **R4 的契约冲突**：**非法数量该抛 `ValueError` 还是 `ValidationError`** ⇒ **需求未定 ✗ 要裁定** ✓


---

# ⭐⭐ L12 开始（**用 Graph 显式表达状态、回退和人工审核**）

## 题眼

```
「现在要交付"**批准后才能收货**"✗ **软件检查通过后却还要等审核人 ✗ 打回后要重新修改 ✗
  重启后还要知道上次停在哪版**」
⭐ 「**本讲把这些去向写成可执行的状态图；FlowERP 在具名采购批准和真实收货之后 ✗ 才增加库存。**」
动作线：**申请已存在 → 软件候选开发与检查 → 等待或打回 → 具名接受软件 →
       采购负责人批准单据 → 实际收货与对账**
线段：**X 检查通过 → 保存 X 和报告 ✗ 等待审核 → 打回理由 → 形成 Y → 重新检查并送审**
```

## ⭐⭐⭐ 辅导资料 §1 的五个要素

```
**节点**（当前做哪件事）✗ **边**（允许去哪里）✗ **条件**（此刻能否走这条边）✗
**共享状态**（下一步必须接住的事实）✗ **执行器**（真正做动作 ✗ 收回结果 ✗ 判断条件 ✗
保存状态并选择下一步的程序）
⭐ 「**没有"修改 → 完成"这条边 ✗ 就不能跳过检查和审核；空报告 ✗ 旧候选的报告或
   模型说"应该没问题"✗ 也不满足进入审核的条件。**」
⭐ 「**共享状态只保存下一节点需要的事实和来源 ✗ 不把整段聊天交给所有节点。**」
⭐⭐ 「**Graph 规定所有允许路径 ✗ Trace 记录某次走过的路径 ✗ 两者不同。**」
⭐⭐ 「**标签只能证明记录存在 ✗ 不能单独证明动作发生。**」
⭐ 「**Loop 处理重复 ✗ Subagents 处理独立工作的委托与汇合 ✗ Graph 处理整体控制去向。**」
```

## ⭐⭐⭐ 前三个实验（**都跑通 ✗ 产物在 `01-labs/`** ✓）

```
① `graph_control_lab.py wait` ⇒ 退出码 0 ✗ `status: "awaiting_human_review"` ✓
   轨迹 **三条边各有 reason**：
     `develop → test`   「本轮最小变更完成 ✗ 交给统一 Harness」
     `test → human_review`「阻断项为零 ✗ 进入人工决策点」
     ⭐ `human_review → awaiting_human_review`「**阻断项为零 ✗ 等待具名审核人批准或打回**」
   ⭐⭐⭐ `reviewer: None` ✗ `review_decision: None` ✗ `reviewed_at: None`
      ⇒ **正是"具名决定"的位置 ✗ 也正是我不代签的东西** ✓
   ⭐ `boundary`: "**Synthetic reports and reviewer input; real Graph;
      no developer execution or authenticated approval.**"
   ⭐ `persisted_text` = 完整 JSON 状态 ⇒ **"重启后仍应等待 X"的依据** ✓
② `purchase_approval_lab.py approved` ⇒ 退出码 0 ✗
   `approved: **received**; **17/2/15**; **one +7 receipt**` ✓
③ `purchase_approval_lab.py replay` ⇒ 退出码 0 ✗ **两次都是 17/2/15 ✗ one +7 receipt**
   ⇒ ⭐ **重放没有再加 7 件** ✓
```

## ⚠️⚠️ 而我要分清两件**容易混**的事

```
⭐ **L12 的 `replay`**（**同一个申请 ✗ 同一个键 ✗ 重放**）⇒ ✅ **不重复生效** ✓
⚠️ **L11 的 R3**（**两个不同申请 ✗ 复用同一个键**）⇒ ⚠️ **第二张申请被标 received 但没货入库** ✓
⇒ ⭐⭐ **手册第 7 步说"在同一候选中检查采购规则"✗ 通过标准里有**：
   「**拒绝 ✗ 正常入库 ✗ 同键重放 ✗ **部分写入及键冲突**在同一候选复验**」✓
   ⇒ ⭐ **"键冲突"正是 R3** ✗ **所以本讲要我复验它** ✓
```

## ⚠️ 一处我又猜错键（**第 N 次 ✗ 如实记**）

```
⚠️ 我第一次取 `d["status"]` 得到 `None` ✗ **真键在 `result` 下面** ✓
⇒ ⭐ **与 L11 两次同形** ⇒ **"先看键名再取值"这条我仍未养成** ✓
```

## 下一步（**L12**）

```
[ ] 第 4 步：**先写下你的判断** ｜ 第 5 步：**让工作台建立个人候选**
[ ] 第 6 步：**在候选中验证"会等待 ✗ 也会继续"** ⇒ ⚠️ **打回要形成新候选 Y**
[ ] 第 7 步：**在同一候选中检查采购规则**（**含键冲突 = L11 的 R3** ✓）
[ ] 第 8 步：**交付前做最后对账** ✗ 🚩 **"实际交付审核人"与"业务审批人"是两个具名的人** ⇒ **待本人**
```

## 🚩 仍待你（累积）

```
① **L10 的 `task-review`**（`TASK-56D04E9DFC`）
② **L11 §5/§6 的"实际负责人：接受或退回"**
③ **证据冗余风险**（321 文件 ✗ 8.2M 不在任何版本库）⇒ 选 A/B/C/D
④ **R4 的契约冲突**：非法数量该抛 `ValueError` 还是 `ValidationError`
⑤ ⭐ **L12 的两位具名的人**：**实际交付审核人** ✗ **业务审批人** ⇒ **两个人 ✗ 两个门** ✓


---

# ⭐⭐⭐ L12 首红：**第四次 `if False and`**

## 被剥离的那一行（**`git diff HEAD` ✗ 这次我先看了** ✓）

```diff
@@ -344,7 +344,7 @@ class ERPService:
                 raise InvalidTransition(f"采购 {request_id} 已完成入库")
-        if item["status"] != PurchaseStatus.APPROVED:
+        if False and item["status"] != PurchaseStatus.APPROVED:
             raise ApprovalRequired(f"采购 {request_id} 未审批，不允许入库")
```
⇒ ⭐⭐⭐ **审批守卫被短路 ⇒ 未审批的采购也能入库** ✓
   ⇒ **HEAD（`course/l12-start`）是拒绝的** ✗ **工作树把它短路了** ✓

## ⭐⭐⭐ 同一手法的**四次**记录

| 讲 | 被短路的守卫 |
|---|---|
| **L05** | `if False and exists:` |
| **L09** | `if False and status == OrderStatus.RESERVED:` |
| **L10** | `if False and order["status"] != OrderStatus.RESERVED:` |
| **L12** | ⭐ **`if False and item["status"] != PurchaseStatus.APPROVED:`** |

⇒ ⭐⭐ **四次都是**：**把守卫的第一个条件换成 `False` ⇒ 那个 `raise` 成死代码** ✗
   **而正确的实现就在下一行 ✗ 只是到不了** ✓

## ⭐⭐ 首红（**一绿一红** ✓）

```
[PASS ] receiving_is_idempotent       「**重复入库键只生效一次**」✓（**起点绿 ⇒ 回归检查** ✓）
[BLOCK] purchase_requires_approval    ⚠️ **`AssertionError: 未审批采购被入库`** ✓
{"total": 2, "passed": 1, "blocking_failed": 1, "decision": "block"}
⇒ ⭐ **`purchase_requires_approval` 的红正是本讲要修的** ✓
```

## ⭐⭐ `agent/graph.py`（**123 行 ✗ 本讲的真模块 ✗ 这次我先看了** ✓）

```
`DeliveryState`(:14) ✗ `move(target, reason)`(:25) ✗ `_load_state`(:30) ✗ `_result`(:42)
`_save_state`(:52) ✗ `run_graph(max_rounds=3, reject_once=False, *,
  require_human_review=False, …)`(:59) ✗ `main`(:106)
⇒ ⭐ **五要素的映射**：**节点** ⇒ `run_graph` 的阶段 ✗ **边** ⇒ `move(target, reason)` ✗
  **共享状态** ⇒ `DeliveryState` ✗ **执行器** ⇒ `run_graph` 自身 ✗
  ⭐ **持久化** ⇒ `_load_state` / `_save_state`（**"重启后要知道停在哪版"** ✓）
```

## ⭐ 合同的两条验收**正是 L11 我记录的两件事**

```
① **未审批采购入库被阻断且库存不变** ⇒ **`purchase_requires_approval`**（**本讲要修** ✓）
② **具名审批后允许一次幂等入库** ⇒ **`receiving_is_idempotent`**（**起点绿** ✓）
③ ⭐ **Graph 状态与 ERP 权威状态可对账**
   ⇒ ⭐⭐ **"ERP 权威状态"** —— **Graph 的状态不是权威 ✗ ERP 才是** ✓
```

## ⚠️ 一处我读命令的失误（**当场报错 ✗ 没静默** ✓）

```
⚠️ 我写 `git show HEAD:flowerp/service.py | grep …` ✗ **冒号在 shell 里要引号** ⇒
   `bash: line 7: course/l12-start: No such file or directory` ✗
   `bash: line 10: agent/graph.py: Permission denied` ✓
⇒ ⭐ **两处都当场报错** ⇒ **比"吞错"那类好得多** ✗ **但教训是：`<rev>:<path>` 要引号** ✓
```

## 下一步

```
[ ] **第 5 步的其余**：进入候选 ✗ 核对源码与解释器（**手册 313 行** ✓）
[ ] **§3 个人实现**：**恢复 `receive_purchase` 的审批守卫**（**本轮 write_scope 含 `flowerp/`** ✓）
[ ] **§4 真实等待与人审** ✗ **§5 Graph 与业务对账** ✗ **§6 同伴 ✗ 迁移与流程版本**
[ ] 🚩 **两位具名的人**：**软件审核人 ✗ 采购负责人** ⇒ **待本人**
```


---

# ⭐ L12 §3 完成：模块核对 ✗ 六段式个人 Spec

## ✅ 模块来源核对（**手册的命令逐字跑 ✗ 退出码 0** ✓）

```
root = <候选>（= `course-prepare` 返回的 path）✗
agent.graph  ✅ 在候选内 ｜ eval.harness ✅ 在候选内 ｜
business: flowerp.service ✅ ｜ flowerp.store ✅
```

## ⭐⭐⭐ 实施提示词里一句**正是 L11 的 R3**

```
⭐⭐⭐ 「**同时修复采购审批后入库的一致性问题：未审批拒绝且无部分写入 ✗
  成功后单据与库存流水对账 ✗ 同键重试不重复加库存 ✗
  **同键异对象不能借用旧成功****。**」
⇒ ⭐ **"同键异对象不能借用旧成功" = L11 的 R3** ✗ **本讲明确要求修它** ✓
```

另三句（**都对上辅导资料**）：
```
⭐ 「**真实开发节点必须连接受控执行 ✗ 不能只把标签从 `develop` 改成 `test`。**」
   ⇒ 正是「**标签只能证明记录存在 ✗ 不能单独证明动作发生**」
⭐ 「**按状态表限制允许边；检查通过后等待实际责任人 ✗ 审核绑定本次对象。
   候选变化后重验或重新审核。记录轮数 ✗ 实际执行与检查次数 ✗ 耗尽时保留待办。**」
⭐ 「**读取 ✗ 执行和保存异常分别留下可获得的真实信息 ✗ 不能虚构已保存的失败记录。**」
```

## ⭐ 六段式个人 Spec（`<控制仓库>/.runtime/l12-learning/L12-SPEC-01.md`）

```
`workbench.cli spec` ⇒ ⭐ **退出码 0** ✗ 六段 = `source` `goal` `non_goals`
                      `constraints` `acceptance` `done` ✓
四条目标：① 最小 Python 状态图（**五件事可指认 ✗ 允许边受限 ✗ 等待落盘 ✗
          打回形成新候选 ✗ 三类异常分别留痕 ✗ 轮数有上限**）
        ② ⭐ **真实开发节点必须连接受控执行**
        ③ ⭐ **批准后才允许收货**（**无部分写入 ✗ 对账 ✗ 同键重试不重复 ✗ 同键异对象被拒**）
        ④ ⭐ **Graph 状态与 ERP 权威状态可对账**（**ERP 才是权威**）
允许清单：`agent/graph.py` ✗ `flowerp/service.py`（⚠️ **冻结的检查不纳入业务写集** ✓）
```

## 下一步（**L12**）

```
[ ] §4 真实等待与人审（**打回 ⇒ 新候选 Y ⇒ 重验** ✓）
[ ] §5 Graph 与业务对账（**含修 R3：同键异对象** ✓）
[ ] §6 同伴 ✗ 迁移与流程版本
[ ] 🚩 **两位具名的人**：软件审核人 ✗ 采购负责人 ⇒ **待本人**
```


---

# ⭐⭐⭐ L12 业务修复完成：**批准后入库 + 同键异对象**

## 改了什么（`flowerp/service.py` 一处 ✗ 两个缺口）

```diff
     ApprovalRequired,
+    Conflict,
@@ -344,11 +345,19 @@
-        if False and item["status"] != PurchaseStatus.APPROVED:
+        if item["status"] not in {PurchaseStatus.APPROVED, PurchaseStatus.RECEIVED}:
             raise ApprovalRequired(f"采购 {request_id} 未审批，不允许入库")
+        claimed = self.store.row(
+            "SELECT reference FROM inventory_events WHERE event_key=?", (event_key,))
+        if claimed is not None and claimed["reference"] != request_id:
+            raise Conflict(
+                f"入库键 {event_key} 已属于 {claimed['reference']}，不能被 {request_id} 复用")
         result = self.receive_stock(...)
```

## ⭐ 三处取舍

```
① ⭐ **`not in {APPROVED, RECEIVED}` 而不照抄 HEAD 的 `!= APPROVED`**
   ⇒ ⚠️ **函数开头对 `RECEIVED` 有单独分支（`:338`）处理"重试"** ✗
     **重试时状态已经是 `RECEIVED`** ⇒ **照抄 `!= APPROVED` 会把重试挡死** ✓
   ⇒ ⭐⭐ **守卫必须与已有的状态机分支相容 ✗ 不是"多此一举"** ✓
② ⭐ **新检查放在 `receive_stock` **之前****
   ⇒ **否则先入库再发现键不对 ⇒ 部分写入** ✓（**Spec 验收 ① 要求无部分写入** ✓）
③ ⭐ **用 `Conflict`**（`models.py:33`）⇒ **"同一个键被两张申请抢"是键冲突 ✗
   不是参数错 ✗ 也不是状态迁移错** ✓
```

## ⭐⭐⭐ 实测四条（**全对** ✓）

```
两用例：退出码 **0** ✗ `{"total":2,"passed":2,"blocking_failed":0,"decision":"pass"}` ✓
  （**改前**：`[BLOCK] purchase_requires_approval`「AssertionError: 未审批采购被入库」）
手工复现：
  ① PR-1 审批后入库 ⇒ `on_hand` 10→**15** ✓
  ② ⭐ PR-2 复用 `rcpt:shared` ⇒ ✅ **`Conflict: 入库键 rcpt:shared 已属于 PR-1 ✗
     不能被 PR-2 复用`** ✓
  ③ ⭐ PR-2 状态 ⇒ ✅ **`approved`**（**不是 `received`** ✓）
  ④ ⭐ `on_hand` ⇒ ✅ **仍 15** ✓
  ⑤ PR-1 同键重试（**同一张申请**）⇒ ✅ **`received` ✗ `on_hand` 不变** ✓
  ⑥ 未审批的 PR-3 ⇒ ✅ **`ApprovalRequired` ✗ 仍 `proposed`** ✓
⇒ ⭐ **L11 记录的 R3 从缺陷变成了被拒绝** ✓
```

## ⭐ `store.row` 的语义（**先看实现 ✗ 不猜** ✓）

```
`flowerp/store.py:148`：`return dict(value) if value else None`
⇒ ✅ **找不到返回 `None`** ⇒ **我的 `claimed is not None` 是对的** ✓
⇒ ⚠️ **L09 我在 `connect()` 上猜过 schema ✗ 报 `no column named id`** ⇒ **这次没重犯** ✓
```

## ⚠️ 仍未改的

```
[ ] ⚠️ **`agent/graph.py` 四处缺口**：① ⭐⭐ **`develop` 没连接受控执行**（**只有标签** ✓）
    ② **打回没形成新候选**（**`state.report` 没清** ✓）③ **三类异常没分开** ✓
    ④ ⚠️ **`_save_state` 在 `except` 之后 ⇒ 保存抛异常就没留痕** ✓
[ ] ⚠️ **`receive_stock` 自己的键判定仍只看键**（**`receive_purchase` 这层挡住了 ✗
    但直接调它的路径没有**）⇒ **记录** ✓
[ ] §4 真实等待与人审 ｜ §5 Graph 部分 ｜ §6 同伴/迁移/流程版本
```


---

# ⭐⭐⭐ L12 Graph 改完：四处缺口 ✗ 一处我自己发现的额外问题

## 改了五件事（`agent/graph.py` **123 → 254 行**）

```
① ⭐⭐ **`develop` 必须连接受控执行** ⇒ 没有 `executor` 就 `stopped` ✗
   理由：「**develop 没有受控执行入口 ✗ 不把标签当成动作**」✓
   有执行时转移理由带 `task_id=… ✗ returncode=… ✗ changed_files=…`（`_digest` 压缩 ✓）
② ⭐⭐ **打回形成新候选**：`candidate += "-R{round+1}"` ✗ `report=None` ✗ `repair_task=None` ✓
③ ⭐ **三类异常分开**：`read_error` / `run_error` / `save_error` ✓
④ ⭐ **`_save_state` 移出主循环的 try ✗ 自己的失败**返回**给调用方** ✓
⑤ ⭐ **边白名单 `_EDGES`** ⇒ `move` 只走表里的边 ✗ 走不了 `ValueError` ✓
   ⇒ **`develop → completed` 不在表里 ⇒ 跳不过检查和人审** ✓
```

## ⭐⭐ 实测（**八项** ✓）

```
① 无 executor  ⇒ ✅ **`stopped`** ✗ 「develop 没有受控执行入口 ✗ 不把标签当成动作」
① 有 executor  ⇒ ✅ `awaiting_human_review` ✗ check=1 ✗ repair=1 ✗ 三条边理由都带真实内容
② 打回         ⇒ ✅ `X → X-R2` ✗ ⭐ **`report=None`** ✗ ⭐ **rounds/check 都没变**（**没顺手再跑一轮**）
② 新候选重跑   ⇒ ✅ ⭐ **`check_count 1 → 2`**（**重新检查了**）
② 具名批准     ⇒ ✅ **`completed`** ✗ reviewer=张三 ✗ decision=approve
③ 读异常       ⇒ ✅ **`read_error=JSONDecodeError`** ✗ 没往下走 ✗ 文件没被覆盖
③ 执行异常     ⇒ ✅ **`run_error=RuntimeError: 执行器崩了`** ✗ `failed`
⑤ 边受限       ⇒ ✅ **`ValueError`**：「不允许的边：develop → completed」
⚠️ ④ 保存失败   ⇒ **我没构造那个场景** ⇒ 如实记
```

## ⚠️⚠️ 一处**我自己发现**的额外问题（**不是测试错 ✗ 是代码错**）

```
⚠️ 第一版改完后，第 2 次（打回）的返回里 `rounds=2` ✗ `check_count=2` ✗ `report` 不是 None ✓
⇒ ⭐ 我以为"旧报告没清" ✗ **查下去问题更大**：
   **打回把状态改成 `develop` 后 ✗ `while` 继续跑 ⇒ 它立刻又跑了一整轮** ✓
⇒ ⭐⭐⭐ **辅导资料**：「**等待时没有新的人工决定 ✗ 就保存状态并结束本次执行 ✗
   而不是不断调用 Codex。**」✗ **"打回"也是人已经作了决定** ✓
⇒ ✅ **修**：`rejected_this_call` ⇒ `while … and not rejected_this_call` ✓
⇒ ⭐ **修完**：`rounds 1→1` ✗ `check 1→1` ✗ `report=None` ✗ `candidate X→X-R2` ✗
  **第 3 次才 `check 1→2`** ✓
```

## ⚠️ CLI 行为变了（**如实说明** ✓）

```
改后 `python -X utf8 -m agent.graph --max-rounds 3` ⇒ 退出码 **2** ✗ `status=stopped`
⇒ ⭐ **CLI 不提供 executor** ✗ 新逻辑下 develop 没有入口就停 ✓
⇒ ⭐ **诚实**（**没有执行入口就不假装改了**）✗ ⚠️ **但 CLI 少了一条可走通的路** ✓
⇒ ⚠️ **手册 §6 要验"会等待 ✗ 也会继续"** ⇒ **待办** ✓
```

## 待办

```
[ ] ⚠️ **CLI 要能提供执行入口**（**但"执行入口"必须是真受控执行 ✗ 不能塞假的** ✓）
    ⇒ ⭐ **本轮 `write_scope` 不含 `workbench/`** ⇒ **不能接工作台任务入口** ✓
[ ] ⚠️ **"保存失败"场景没构造**（**`save_error` 的逻辑没被实测** ✓）
[ ] **§4 真实等待与人审** ✗ **§6 同伴 ✗ 迁移与流程版本**
[ ] 🚩 **两位具名的人**：软件审核人 ✗ 采购负责人 ⇒ **待本人**


---

# ⭐⭐⭐ L12 §6：会等待 ✗ 拒绝旧候选的批准

## 手册 §6 点出的一处缺口（**它直接要我补** ✓）

> 「**参考程序只记录传入的姓名和决定 ✗ 不认证身份 ✗ 也不自动保证恢复时仍是同一候选。……
>  **个人实现需拒绝旧候选的批准**。**」

⇒ ✅ **补法**：
```
① ⭐ **`report_candidate` 字段** ⇒ 生成报告时 `state.report_candidate = state.candidate` ✓
② ⭐ **批准前校验**：`report_candidate != candidate` ⇒
   `review_decision = "rejected_stale_candidate"` ✗ `error` 写明两边的身份 ✗
   `move("develop", "批准无效：报告不属于当前候选，需要重新检查")` ✓
```

## ⭐⭐⭐ §6 第一次运行（**手册的命令逐字 ✗ 退出码 3** ✓）

```
$ "$controlPython" -X utf8 -m agent.graph --max-rounds 3 --require-human-review \
    --state-file .runtime/l12-review-01/state.json
⇒ 退出码 **3** ✓ ｜ `status: awaiting_human_review` ✓ ｜
  轨迹 **develop → test → human_review → awaiting_human_review** ✓（**与手册预期逐字一致**）
⭐ `develop → test` 的理由是「**demo 模式：本轮不执行开发动作 ✗ 只观察状态流转**」
   ⇒ **不再是"本轮最小变更完成"** ✓ **这正是"不把标签当成动作"** ✓
`repair_count: 0`（**没假装执行** ✓）✗ `candidate=C0` ✗ `report_candidate=C0` ✓
```

## ⭐⭐⭐ 四个场景实测（**全过** ✓）

```
A ⭐ **候选 Y ✗ 报告属 C0 ⇒ 批准被拒**：`status=develop` ✗
   `review_decision=**rejected_stale_candidate**` ✗
   error「**报告属于 C0 ✗ 当前候选是 Y；候选变化后必须重新检查再送审**」✓
B **候选一致 ⇒ `completed`** ✗ reviewer=张三 ✗ decision=approve ✓
C **打回 ⇒ `X → X-R2` ✗ `report_candidate=''` ✗ rounds/check 都没变** ✗
  新候选重跑 ⇒ `report_candidate=X-R2` ✗ **`check_count 1 → 2`** ✓
D **无审核人 ⇒ `ValueError`** ✓
⇒ ⭐ **"候选变化后重验"闭环了** ✓
```

## ⚠️ 一处如实说明的取舍

```
⚠️ **`--develop-mode` 的库默认是 `controlled` ✗ CLI 默认是 `demo`** ✓
⇒ **理由**：**手册 §6 的命令不带执行参数 ✗ 却期望 `awaiting_human_review`** ✓
   **而提示词要求"develop 必须连接受控执行"** ⇒ **两条只能靠"显式声明 demo"共存** ✓
⇒ ⚠️ **但这是**我的**一个设计选择** ✗ **不是手册规定的** ✓ ⇒ 🚩 **留给本人判断** ✓
```

## ⚠️ 仍未做

```
[ ] ⚠️ **"保存失败"场景没构造**（**`save_error` 逻辑没实测** ✓）
[ ] **§7 在同一候选检查采购规则** ✗ **§8 最后对账** ✗ **§6 同伴 ✗ 迁移与流程版本**
[ ] 🚩 **真实软件审核人** ⇒ **待本人**


---

# ⭐⭐⭐ L12 §7~§8 完成：七项完成标志逐条对账

## §7（**手册的命令逐字**）

```
① 两个用例 ⇒ 退出码 **0** ✗ `{"total":2,"passed":2,"decision":"pass"}`
② 完整阻断 ⇒ 退出码 **0** ✗ `{"total":20,"passed":20,"blocking_failed":0}`
⇒ 报告落点 `.runtime/l12-final-01/selected.json`（716 B）✗ `blocking.json`（4828 B）✓
```

## ⭐⭐⭐ §8 七项（**逐条对我的证据**）

| # | 要求 | 判定 |
|---|---|---|
| 1 | Graph 检查通过后停下等真人 | ✅ `awaiting_human_review` ✗ 退出码 **3** ✗ 三个审核字段 `None` |
| 2 | 打回能返回修改 ✗ 新版本重新检查 | ✅ `X→X-R2` ✗ `report=None` ✗ **`check_count 1→2`** |
| 3 | 中断后能继续 ✗ 不重复副作用；旧候选批准 ✗ 非法转移被拒 | ✅ 恢复后 check 不变 ✗ 轨迹累加 ✗ **`rejected_stale_candidate`** ✗ **`develop→completed` 抛 `ValueError`** |
| 4 | 到限停止 ✗ 检查/读取/保存异常有明确结果与最后可靠状态 | ✅ `stopped` ✗ `IsADirectoryError` ✗ `RuntimeError` ✗ `PermissionError` |
| 5 | 未批准不能入库 ✗ 批准不改库存 ✗ 收货后 10→17 ✗ OTHER/PR-OTHER 保留 | ✅ ⭐ **`10/2/8` ⇒ 批准后仍 `10/2/8` ⇒ 收货后 `17/2/15`** ✗ `PR-OTHER` 在 ✗ OTHER 仍 `reserved` |
| 6 | 重试仍 17 ✗ 只有一条 `+7`；写入故障与同键异对象同候选核验 | ✅ 重试 `17/2/15` ✗ **流水仍一条 `+7`** ✗ **`Conflict`** ✗ **`PermissionError` 照实记** |
| 7 | 新增检查 ✗ 两项 Eval ✗ 完整阻断指向最终候选；具名软件审核 ✗ 业务对账 ✗ 迁移记录 | ⚠️ **报告都指向同一候选** ✗ **具名审核待本人** ✗ 迁移在 §6 |

## ⭐⭐⭐ 第 5 ✗ 6 条的完整实测

```
① 起始（在库 10 ✗ OTHER 预占 2）   **10 / 2 / 8**
② 创建 PR-TARGET 后               **10 / 2 / 8**
③ 具名批准后（**应不变**）          **10 / 2 / 8**  ← ⭐ **批准本身不改变库存** ✓
④ 收货后（**应 17/2/15**）         **17 / 2 / 15** ✓
⑤ 同键重试后（**应仍 17/2/15**）    **17 / 2 / 15** ✗ **流水仍一条** ✓
⭐ PR-TARGET 流水 = `[{'event_key':'rcpt:1','quantity':7,'reference':'PR-TARGET'}]` ✓
⭐ 与手册一致 `True` ✗ 只有一条 +7 `True` ✗ PR-OTHER 在 `True` ✗ OTHER 仍 `reserved` ✓
```

## ⭐⭐⭐ 三种故障都实测留痕（**不虚构** ✓）

```
(a) **读不出来**（传目录）⇒ `read_error=**IsADirectoryError**` ✗ `status=develop`（**没往下走 ✗ 没覆盖**）
(b) **写不出去**（`chmod 0o500`）⇒ `save_error=**PermissionError**` ✗
    `error="**状态未落盘：PermissionError: …**"` ✗ ⭐ **有没有假装已保存：`False`** ✗
    **文件真的没写出来：`True`**
(c) **正常一次** ⇒ `save_error=None` ✗ 文件写出来了
⇒ ⭐ **手册**：「**读取 ✗ 执行和保存异常分别留下可获得的真实信息 ✗ 不能虚构已保存的失败记录。**」✓
```

## ⚠️ 一处我探针不够导致的假警报

```
⚠️ 第一次跑 (a) 时**只打印了 `save_error`** ⇒ 看到 `None` ⇒ **误以为"它假装已保存"**
⇒ 真因：**传目录时 `read_text()` 先抛 `IsADirectoryError`** ⇒ **走 `read_error` 分支直接 return**
⇒ ⭐⭐ **教训**：**打印"失败"时要打印**全部**可能的失败字段 ✗ 不然会把"没走到"看成"没记"**
```

## 待办

```
[ ] **§6 同伴 ✗ 迁移与流程版本** ✗ **写 `SUBMISSION.md`（六节）**
[ ] 🚩 **具名软件审核 ✗ 业务批准人** ⇒ **待本人**


---

# ⭐⭐⭐ L12 完成（**待本人接受** 🚩）

## 写了 `SUBMISSION.md`（**六节 ✗ 全部用已有证据** ✓）

```
1 首次判断 —— **研发审核 vs 采购审批分开** ✗ **10/2/8 → 17/2/15 的逐步推导** ✗
  **首次状态图与允许边** ✗ **哪些动作不能重复** ✓
2 参考实验观察 —— **三项基础观察**（wait/approved/replay）✗
  ⚠️ **两项扩展对照标"未选做"** ✓
3 个人实现 —— ⭐ **必做核验表五项全有证据** ✓
4 真实等待与人审 —— ⚠️ **两行都是"待确定"**（**探针用过张三/李四 ✗ 但那是测试** ✓）
5 Graph 与业务对账 —— **五条事实逐条 ✗ 报告命令与退出码** ✓
6 同伴 ✗ 迁移与流程版本 —— ⚠️ **仅自查 ✗ 选做项标未选做 ✗ 不主张跨事项闭环** ✓
```

## ⭐⭐⭐ §3 的必做核验表（**五项 ✗ 全有原始证据** ✓）

| 核验 | 证据 |
|---|---|
| **等待 ✗ 同状态恢复 ✗ 具名接受与打回后重验** | 等待 ⇒ 退出码 **3**；恢复后 `check_count` 不变；打回 ⇒ `X→X-R2`；新候选 **`check_count 1→2`** |
| **轮次到限 ✗ 检查／读取／保存异常** | `stopped` ✗ `IsADirectoryError` ✗ `RuntimeError` ✗ `PermissionError`（**不假装已保存**）|
| **旧候选批准与非法转移拒绝** | `rejected_stale_candidate` ✗ `develop → completed` 抛 `ValueError` |
| **未批准拒绝 ✗ 正常收货与同键重试** | `ApprovalRequired` ✗ **`10/2/8` ⇒ 批准后仍 `10/2/8` ⇒ `17/2/15`** ✗ 重试仍 `17/2/15` |
| **状态写入故障与同键异对象冲突** | `save_error=PermissionError` ✗ 文件真没写出 ✗ **`Conflict: 入库键 rcpt:shared 已属于 PR-1`** |

## ⚠️ 我如实记的未完成项

```
🚩 **具名软件审核 ✗ 业务批准人** ⇒ 待本人（**我不代签**）
⚠️ **事项编号 ✗ 姓名 ✗ 业务口径确认者** ⇒ 待本人
⚠️ **身份认证那一半没补**（**手册不要求 ✗ 但 `reviewer` 只是本地字符串**）
⚠️ **CLI 的 `--develop-mode` 默认 `demo`** ⇒ **我的设计选择 ✗ 待裁定**
⚠️ **两项扩展对照未选做** ✗ **本次改动未走工作台 `task-run`** ✗ **同伴复验：仅自查**
```

## 状态

```
L01~L11 ✅（🚩 五件待你）｜ **L12 §1~§8 + SUBMISSION 全部完成** ✗ 17 个记录文件
`agent/graph.py` **123 → 302 行** ✗ `flowerp/service.py` 两个缺口修好
参考仓库 **0 改动** ｜ 完整阻断 **20/20 pass**
```

## 🚩 累积待你（六件）

```
① L10 的 `task-review` ② L11 §5/§6 的"接受或退回" ③ 证据冗余风险选 A/B/C/D
④ R4 的契约冲突（`ValueError` 还是 `ValidationError`）
⑤ **L12 具名软件审核 ✗ 业务批准人** ⑥ **L12 的 `--develop-mode` 默认值是否接受**
```


---

# ⭐⭐⭐ L12 补齐：Skill 五个反例 ✗ 25 个 lab 模式

## ⭐⭐ Skill 第 ④ 条**就是 L11 的 R3 的精确复述**

```
「**PR-TARGET 申请七件 ✗ 借用属于期初库存的 `opening` 键。最终单据为 `received` ✗
  在库仍为 10 ✗ **目标流水为零**。摘要称"幂等检查通过 ✗ 入库成功"。**」
期望：「**不能借用其他事件的成功**」✓
⇒ ⭐⭐⭐ **而我在 L12 §5 修的正是它**（`Conflict: 入库键 rcpt:shared 已属于 PR-1` ✓）
   ⇒ ⭐ **课程的期望与我的修法一致** ✓
```

## ⭐⭐⭐ `graph_control_lab` 的 16 个模式里 ✗ **三处参考实现自己承认的缺口**

```
⭐ `stale-approval` ⇒ **参考给 `completed`** ✗ `judgment`「**No candidate identity binding
   or fresh Eval occurred**」✗ `additional_eval_calls = 0`
   ⇒ ⭐⭐ **同一场景 ✗ 我的实现给 `develop` ✗ `rejected_stale_candidate`** ✓
     ⇒ **这正是"个人实现"与"参考程序"的分界线** ✓
⚠️ `empty-report`   ⇒ **`awaiting_human_review`**（**空报告竟然进了人审**）
   ⇒ ⚠️ **而我的实现也没加"报告非空"校验** ✗ **如实记为一个缺口** ✓
⚠️ `unchecked-move` ⇒ **`completed`**（**名字就在说"没校验的转移"**）
   ⇒ ⭐ **而我的 `move()` 会抛 `ValueError`** ✓ **已补** ✓
```

## ⭐ 九个采购模式（**全过 ✗ 没弄坏** ✓）

```
approved 0 ｜ unapproved 0 ｜ blank-reviewer 0 ｜ rejected 0 ｜ replay 0 ｜ different-key 0
⭐ status-write-failure 0（「**status write failed atomically**」）
⭐ recovery-same-key 0 ｜ ⭐ key-collision 0（「**rejected; five tables unchanged**」）
⇒ ⭐ **九个全过 ⇒ 我的 `service.py` 改动没弄坏任何一条** ✓
```

## ⚠️ 三处我这一轮的失误

```
⚠️ 一：**我在 SUBMISSION 里说 `state-handoff-review` Skill 不存在** ⇒ **错了 ✗ 已更正** ✓
⚠️ 二：**第一次跑九个模式时 `approved`/`replay` 报退出码 2** ✗
   ⇒ **真因**：`error: **use a new report path; preserve previous evidence**` ⇒ **拒绝覆盖** ✓
   ⇒ ✅ **换新路径 ⇒ 都退出码 0** ✓ **不是回归** ✓
⚠️ 三：**我抓 `MODES` 的第一次只抓到 3 个（Graph）✗ 7 个（采购）** ✗ 实际 16 / 9 ✓
```

## ⚠️ 新发现一个缺口

```
⚠️ **`empty-report`**：**我的实现里报告 0 项 ⇒ `blocking_failed` 为 0 ⇒ 也会进人审** ✓
⇒ ⭐ **要补"报告必须非空且覆盖清单"的校验** ⇒ **待办** ✓
```

## 仍待读

```
⚠️ **PPT**（**L12 的 29 页**）✗ **`reference/参考说明.md`** ✗ **`assets/README.md`**
```


---

# ⭐⭐⭐ L12 补上 `empty-report` 缺口

```
`graph_control_lab.py empty-report` ⇒ **`status = awaiting_human_review`** ⚠️
⇒ ⭐ **空报告竟然进了人工决策点**（**与 L10 的 `converged` 是同一个洞 ✗ 换了位置**）
⇒ Skill：「**零阻断数或空结果不能单独支持审核。**」
⇒ ⚠️ **我的实现原来也漏了**（**`blocking_failed` 为 0 ⇒ 进人审** ✓）
```

## ✅ 修法（三行判断）

```python
results = state.report.get("results") if isinstance(state.report, dict) else None
if not isinstance(results, list) or not results:
    state.run_error = ("报告没有可核验的用例结果，零阻断数不能单独支持审核"
                       f"（results={results!r}）")
    state.move("failed", "报告无效：空结果不能进入人工决策点")
    continue
```

## ⭐⭐ 实测两条 ✗ 回归

```
空 results  ⇒ `status = **failed**` ✗ `run_error` 写明 ✓ ✗ trace「报告无效」✓
             ⭐ **没进人审 ✗ 没进 completed** ✓
正常报告    ⇒ `awaiting_human_review` ✗ `check_count=1` ⇒ ⭐ **没误伤正常路径** ✓
回归：`--suite blocking` ⇒ **20/20 pass** ✗ 退出码 0 ✓
```

## ⭐⭐⭐ 三处「参考演示缺口 ✗ 我显式拒绝」的对照

| 场景 | **参考程序** | **我的实现** |
|---|---|---|
| **空报告** | ⚠️ `awaiting_human_review` | ⭐ **`failed`** + 原因 |
| **旧候选批准** | ⚠️ `completed`（`judgment` 承认"无候选绑定"） | ⭐ **`develop`** + `rejected_stale_candidate` |
| **未校验的转移** | ⚠️ `completed` | ⭐ **`ValueError`：不允许的边** |

⇒ ⭐⭐⭐ **同一个模式：参考演示缺口 ✗ 我用显式拒绝堵上** ✓
   ⇒ ⭐ **这正是"个人实现"与"参考程序"的差别** ✓

## 仍待读

```
⚠️ **PPT（29 页）** ✗ **`reference/参考说明.md`** ✗ **`assets/README.md`**
```


---

# ⭐⭐⭐ L12 PPT 对照 ✗ 一处按 PPT 改的实现

## ⭐⭐ PPT 那句「一个 `approved` 字符串不足以放行」= 我 L12 做的两件事

```
**交付审核**：审核人根据**候选 X ✗ Diff 与报告 R-X** 决定 ✓
**采购审批**：业务负责人批准 **PR-TARGET 的商品和数量** ✗ 才允许入库 ✓
⇒ ⭐ **`report_candidate`**（审核对象绑"哪一版"）✗ **`Conflict`**（同一个键属于谁）✓
```

## ⭐⭐ 执行器四步（**PPT 讲的 ✗ 我全做到了**）

```
① 读取：**恢复时读原状态 ✗ 而非从 `develop` 重来** ⇒ `_load_state` ✓
② 执行：**有动作名称 ✗ 仍须确认动作真的执行** ⇒ `develop_execution` ✗ 无入口就 `stopped` ✓
③ 选择：**记录 `from` ✗ `to` ✗ `reason` 和轮数** ⇒ `move()` ✓
④ 交还控制：**到等待点保存后暂停** ⇒ `awaiting_human_review` 是终态 ✗ 打回也结束本次执行 ✓
⭐ 「**列出所有允许路径。`trace` 只记录本次实际走过的路径。**」⇒ `_EDGES` vs `trace` ✓
```

## ⭐⭐⭐ 一处 PPT 指出我的真差别 —— **已改**

```
> 「**候选改变后旧报告**保留为历史**✗ 但不能继续充当新候选的通过依据。**」
⚠️ **我原来是 `report = None`** ⇒ **那是清掉 ✗ 不是"保留为历史"** ✓
✅ **改为**：**旧报告移进 `report_history`**（`candidate` ✗ `superseded_by` ✗
   `superseded_at` ✗ 原报告）**再清空当前报告** ✓
⭐ 实测：打回后 **`history=1`** ✗ 旧候选 `X` ✗ 被 `X-R2` 取代 ✗ 旧报告还在 ✗
   当前已清 ✗ 新报告绑 `X-R2` ✗ 历史仍保留 ✓
```

## ⭐ 另外两句

```
⭐⭐ 「**开发节点无权替人写入 `approve`。**」⇒ 正合我不代签 ✓
⚠️ PPT 自己的表：`DeliveryState` ⇒ 「**候选与报告绑定尚未完整实现**」
   ⇒ ⭐ **参考承认的缺口 ✗ 我补了** ✓
```

## 九项必读状态

```
[x] README ✗ 辅导资料 ✗ 手册 ✗ SUBMISSION ✗ ⭐ **PPT（296 行）** ✗
[x] examples（**Graph 16 + 采购 9**）✗ [x] skills（**SKILL + 五个反例**）
⚠️ `reference/参考说明.md` ✗ `assets/README.md` ⇒ 仍未读
```


---

# ⭐⭐⭐ L12 完成（**九项必读全清 ✗ 待本人接受** 🚩）

## ⭐⭐⭐ `reference/参考说明.md` §2 逐条列出参考实现的边界 ✗ 我补了三条

| 它列的边界 | 我的处理 |
|---|---|
| **develop 推进标签 ✗ 没运行 Codex** | ⭐ **已补**：无执行入口就 `stopped` |
| **非空 `reviewer` 不证明真人已决定** | ⭐ **如实记**（**只是本地字符串**）|
| ⭐ **读取在 `try` 之前 ✗ 保存在其后** | ⭐ **已补**：三类异常分开 ✗ `_save_state` 移出 `try` |
| **保存状态不证明副作用能安全恢复** | ⚠️ **概念边界 ✗ 如实记** |

## ⭐⭐⭐ `assets/README.md` 一句与我实测**不符** ✗ 查清了

```
它说：「**教师历史运行中 ✗ `status-write-failure` 与 `key-collision` 的退出码为 1 ✗
       其余为 0；**判断本人结果须读取本轮实际输出****」
⚠️ **我跑出来两个都是 0** ✓
⇒ ⭐ **退出码 1 = 检查成功发现了**故意注入的问题**（**L11 的 `premature-stock` 同形** ✓）
   ⇒ ⭐⭐ **教师是**在注入缺陷的候选**上跑 ⇒ 抓到 ⇒ 1**；
     **我是在**我的候选**上跑 ⇒ 我的候选没那两个缺陷 ⇒ 0** ✓
⇒ ⭐⭐⭐ **它自己交代了**：「**判断本人结果须读取本轮实际输出**」✗ 不照抄教师的退出码 ✓
⇒ ⚠️ **所以我只能说"我的候选在这两点上检查通过"✗ 不能说"我跑通了教师的结果"** ✓
```

## ⭐ 它另两句

```
⭐⭐ 「**Graph 包装实验……其退出 0 只证明**观察符合参考行为**✗ 不证明设计缺口已修好
   ✗ Codex 已开发或真人已批准。**」
⭐ 「**采购实验……教学批准字符串不代表具名业务验收；**恢复成功也不能倒推第一次写入原子化****」
```

## ⚠️ 一处我**没做**的（**它比我的手跑好** ✓）

```
⭐ 采集入口：`scripts/audit_course_experiments.py --lesson 12 --output-dir …`
⇒ ⭐ **"`summary.json` 汇总本轮 ✗ 各 `L12-*.json` 保存**命令 ✗ 退出码 ✗ stdout 和 stderr**"** ✓
⇒ ⚠️ **我是逐个模式手跑的 ✗ 没把"命令/退出码/stdout/stderr"四样一起存** ✓ **如实记** ✓
```

## ⭐⭐⭐ L12 的完整交付

```
**业务**（`flowerp/service.py` ✗ 两个缺口）：
  ⭐ **第四次 `if False and`**（审批守卫被短路）⇒ 恢复 ✗ 放行 `RECEIVED`
  ⭐ **同键异对象借用旧成功**（**L11 的 R3**）⇒ `Conflict`
  ⇒ **`10/2/8` ⇒ 批准后仍 `10/2/8` ⇒ 收货后 `17/2/15` ⇒ 重试仍 `17/2/15` ✗ 一条 `+7`**
**工作台**（`agent/graph.py` **123 → 325 行**）：六处
  `develop` 连接受控执行 ✗ 边白名单 ✗ 打回换候选+旧报告进历史+结束本次执行 ✗
  候选绑定 ✗ 三类异常分开 ✗ 空报告不得进人审
⇒ **完整阻断 20/20 pass**
**三处"参考演示缺口 ✗ 我显式拒绝"**：空报告 / 旧候选批准 / 未校验的转移
```

## 🚩 待你（累积六件）

```
① L10 `task-review` ② L11 §5/§6 接受或退回 ③ 证据冗余风险 A/B/C/D
④ R4 的契约冲突 ⑤ **L12 具名软件审核 ✗ 业务批准人** ⑥ **L12 的 `--develop-mode` 默认值**
```

## 下一步

```
**L13**（**材料可能未随 Git 发布** ⇒ 先查）
⇒ 之后 **L14 ✗ L15 ✗ L16 ⇒ 结营毕设**
```


---

# ⭐⭐ L13 开始（**把执行链路封装成任务 API**）

## 题眼

```
「**林舟离开终端后 ✗ 仍想知道那次补货交付的 Spec ✗ 进度 ✗ 失败原因和接受版本。**
 ⭐ **本讲新增两个最小入口：提交后拿到稳定 Task ID ✗ 凭原 ID 查询；
   服务真实重启后 ✗ 完成记录仍能找回。**」
图：**保存并受理 → 查询原任务 → 审核当前材料** ✗ ⭐ **202 是已受理 ✗ 200 是查到记录**
动作线：**保存请求与受理事件 → 返回 Task ID → 查询原任务 → 同键重试或明确冲突 →
       停旧服务 ✗ 起新进程 → 凭原 ID 找回结果并核对采购事实**
⚠️ **PPT「须向课程提供方单独领取 ✗ 不随 Git 发布」** ✗
   ⇒ ⚠️ **`/tmp/ppt-text/L13.txt` 有 322 行 ✗ 而来源不明** ⇒ **我不说它等于课件** ✓
```

## ⭐⭐⭐ 辅导资料 §1：三层事实（**第一层发生 ✗ 不保证后两层** ✓）

| 状态码/词 | 只说 | ⚠️ 不说 |
|---|---|---|
| **`202 Accepted`** | **请求已受理** | ❌ **代码已完成** |
| **`200 OK`** | **记录查到了** | ❌ **记录已完成**（**可能还在执行或返工**）|
| **`completed`** | **满足该任务的完成约定** | ❌ **候选 ✗ Eval 和具名决定都对** |

⭐⭐ 「**一个好接口应让下一步行动与已经获得的证据相匹配。**」✗
   「**看到"检查通过 ✗ 等待验收"✗ 可以打开证据作判断 ✗ **不能让页面替她署名****」

## ⭐⭐⭐ §2 三种身份 + §3 先保存再返回

```
**事项编号**（为什么做）｜ **Task ID**（这次执行是哪一次）｜ **业务引用**（影响哪个对象）
⭐⭐ 「**采购单编号不能替代任务编号** ✗ **任务编号也不能替代候选版本**」
⭐⭐ **字段最小性判据**：「**删除某字段后 ✗ 接手者能否认错任务 ✗ 认错版本 ✗ 误判权限
   或丢失失败依据？若会 ✗ 字段应保留。**」
⭐⭐⭐ **可靠顺序**：**校验 → 分配身份 → **把请求 ✗ 初始状态和受理事件保存成功** →
   然后返回编号 → 后台推进**
⭐ 「**若先返回编号再写库 ✗ 停电时会留下一个查不到的任务**」
⭐ 「**任务行与受理事件应在同一个事务**」
⭐⭐ 「**"异步"不是另外一种成功标准**」
```

## ⭐⭐⭐ 交付前核对三条（**我这次要证的**）

```
① **区分 HTTP 请求 ✗ Task 与采购单 ✗ 受理返回身份 ✗ 长检查和人审分别留证据**
② ⭐ **验证同键重放 ✗ 内容冲突 ✗ 失败查询和非法状态拒绝 ✗
   完成任务经**真实重启** HTTP 查询仍保留** ⇒ ⚠️ **必须真停进程 ✗ 不能用重新 import 冒充**
③ ⭐ **真实候选 ✗ 报告 ✗ 具名交付审核与业务对账对应；
   **verify 实验不冒充真实 Codex 新增功能****
```

## ⭐ 第 1 步的预判（**五条 ✗ 写在做之前**）

```
① **提交后立即查询应是"未完成"**（`evaluating`/`queued`）✗ **立刻 `completed` 就是错的**
② **同键重放 ⇒ 同一个 Task ID** ✗ **同键但内容不同 ⇒ 冲突拒绝**
③ ⭐ **真实重启后查原 ID ⇒ 记录仍在 ✗ 且是重启前那一刻的状态**
④ **失败也能查到原因**（**不是 404 或空**）
⑤ **非法状态/输入 ⇒ 明确拒绝**（**不是 500 ✗ 也不静默接受**）
```

## 下一步

```
[ ] 读 §2~§6 的命令 ｜ ⚠️ **第 3 步的真实重启要真的停进程**
[ ] 第 4 步在候选里实现两个接口 ⇒ **先看候选里已有什么**
[ ] §5 真实采购与库存核对 ｜ §6 同伴复验 ✗ 迁移
```

## 🚩 仍待你（累积六件，同前）


---

# ⭐⭐⭐ L13 §2~§3 完成：**两个参考实验 ✗ 真进程重启**

## §2 `task_api_lab.py`（**退出码 0 ✗ `verified: true`** ✓）

```
⭐ **十项观察** ✗ 手册点名的四项逐条对上：
  `accepted_before_eval_finished` ⇒ `{"http": **202**, "response": {"task_id": "**TASK-BA6370C790**"}}`
  `running`                       ⇒ `{"status": "**evaluating**"}`
  `same_key_same_body`            ⇒ `{"task_id": "**TASK-BA6370C790**", "spec_count": 1}`
  `real_eval_waiting_review`      ⇒ `{"status": "**review**"}` ✗ `reviewed_by` 未填 ✓
⭐ **另外六项**：
  `key_conflicts` ⇒ **`409` × 3**（改 `request`/`actor`/`business_refs`）✗ **没新建**
  ⭐⭐ `code_mode_rejected` ⇒ **`400`**「**网页API只允许verify；代码执行须使用明确授权的课程CLI**」
     ⇒ ⭐⭐⭐ **正是合同的"持久化和**最小权限**"**
  `missing_task` ⇒ **`404 not_found`**（**不是空成功**）
  ⭐ `event_version` ⇒ `{"before": 5, "after": 5, **event_count 9 → 10**}`
     ⇒ **状态版本没变 ✗ 事件 +1** ⇒ **正是「状态决定下一步 ✗ 事件解释怎样走到这里」**
  `concurrent_reviews` ⇒ **`400` 非法状态迁移** ✗ 然后 `200`
  `completed_reopened_store` ⇒ `completed`（**但那只算"重开存储"** ✗ 不算进程重启）
⭐ **顶层四个诚实性字段**：`basis: "reference_localhost_real_eval"` ✗
   `real_codex_execution: false` ✗ `student_achievement: false` ✗ `erp_increment_proven: false`
   ⇒ **正是「verify 实验不冒充真实 Codex 新增功能」**
```

## ⭐⭐⭐ §3 真重启（**两条都 `verified: true`** ✗ 硬证据在 PID 与信号号）

```
3.1 `audit_task_recovery`：
  `accepted` ⇒ `TASK-AE77D31753` ✗ `before` ⇒ **`evaluating`**
  ⭐⭐ `terminated_pid: **695879**` ✗ `terminated_returncode: **-9**` ⇒ **SIGKILL**
  `after` ⇒ **`review`** ✗ `error: "**服务重启时任务停在 evaluating ✗ 已转入安全重放**"`
3.2 `completed_restart_lab`（**三个服务进程**）：
  `terminated_pid: 695907` ✗ `-9`（**SIGKILL ✗ 中断**）
  `completed_before_restart` ⇒ **`completed`**
  `completed_service_exit: {"pid": 695911, "returncode": **-15**}`（**SIGTERM**）
  ⭐ `completed_after_restart` ⇒ **`completed`** ⇒ **完成记录没丢**
  ⭐ `restarted_service: {"pid": 695941, "http": **200**}`
⇒ ⭐⭐⭐ **三个 PID ✗ 两种信号 ✗ "真重启"不是我说的 ✗ 是信号号说的**
```

## ⭐ 两份 audit 的 `basis` ✗ 诚实性

```
`basis: "**maintainer_process_interruption**"` ⇒ **维护者制造进程中断**（**不是真断网 ✗ 不是真崩**）
`student_achievement: false` ✗ `real_codex_execution: false` ✗ 3.2 还有 `human_acceptance: false` ✓
```

## ⚠️ 手册的关键告诫

```
「**`verify` 模式只做检查；**修改代码 ✗ 入库等有副作用的动作 ✗ 必须先核对执行身份和实际结果 ✗
  再决定是否重放****」
⇒ ⚠️ **两条 audit 都是 `execution_mode: "verify"`** ⇒ **没有副作用动作**
   ⇒ ⭐ **所以它们**不能**证明"入库也能安全恢复"** ⇒ **留给 §5 的真实采购** ✓
```

## 下一步

```
[ ] **第 4 步：在自己的候选里实现两个接口** ⇒ **先看候选里已有什么**
[ ] **§5 真实采购与库存核对**（**要证有副作用的动作**）✗ **§6 同伴复验 ✗ 迁移**
```


---

# ⭐⭐⭐ L13 §4 起步：候选已建 ✗ 起点与 L10/L12 **不同**

## ⭐⭐ 课程合同（**两处与前几讲不同**）

```
`phase`: ⭐ **"operate"**（**L10/L11/L12 都是 `"build"`**）
⭐ `write_scope`: ⭐ **`workbench/`** ✗ `flowerp/` ✗ `eval/` ✗ `tests/`
   ⇒ **本讲要改工作台本身**（**L12 那次写集不含 `workbench/`**）
`request`: "**从 Task API 提交补货需求 ✗ 生成 Spec ✗ 执行 Eval ✗ 并停在具名人工审核。**"
⭐ `acceptance`: ① **API 接受请求后返回 Task ID 而非伪称完成**
                ② **任务事件可追溯到需求 ✗ 业务对象和 Eval**
                ③ ⭐ **全绿后仍停在人工审核**
```

## ⭐⭐⭐ 工作树 vs HEAD：**没有 `if False and`**

```
$ git diff HEAD --stat
 course/baselines/PROGRESSION.json | 16 ----------------
 1 file changed, 16 deletions(-)
⇒ ⭐ **只有 `PROGRESSION.json` 被删 ✗ `flowerp/service.py` 一个字没动**
⇒ ⭐⭐ **与 L10/L12 完全不同** —— **那两讲都有 `if False and` 的剥离**
   ⇒ ⭐ **本讲是"能力不存在"型 ✗ 与 L11 同类**
```

## ⭐⭐⭐ 首红：两个用例**都 PASS**（退出码 0）

```
[PASS] `purchase_requires_approval`             「**未审批被阻断 ✗ 审批后可入库**」
[PASS] `delivery_evidence_and_review_controls`  「**需求自动生成任务级 Spec 并推进至审核；
       完成需要具名审核；反馈默认待审且审核后不可重复改写**」
⇒ ⭐ **起点红不在已有用例上** ⇒ **要问"本讲的增量在哪"**
```

## ⭐⭐⭐ 增量 = **两个最小 API 端点不存在**

```
关键词扫描 `workbench/*.py`：
  `def submit` ✗ `task_id` ✗ `202` ✗ `evaluating` ⇒ **都有**
  ⚠️ **`status_url`** ⇒ **没找到** ｜ ⚠️ **`delivery-view`** ⇒ **没找到** ｜ ⚠️ **`409`** ⇒ **没找到**
⇒ ⭐ **参考实验里的三样在候选里都不存在** ⇒ **正是本讲要实现的"两个最小接口"**
⇒ ⭐⭐ **而 `delivery_evidence_and_review_controls` 覆盖的是"任务级 Spec ✗ 具名审核 ✗
   反馈待审"✗ 不是 HTTP 端点** ⇒ **两层检查不冲突**
```

## ⭐ 参考实验给的六个响应形状（**从报告读 ✗ 不猜**）

```
202 ⇒ `{"task_id": …, "accepted": true, "execution_mode": "verify",
        "status_url": "/api/v1/tasks/<id>", "view_url": "/api/v1/delivery/views/<id>"}`
200 ⇒ `{"id": …, "status": "evaluating"|"review"|"completed", "error": …, "spec_path": …}`
409 ⇒ `{"error": "conflict", "message": "提交键已用于不同需求；请使用新键"}`
404 ⇒ `{"error": "not_found", "message": "'TASK-MISSING'"}`
400 ⇒ `{"error": "ValueError", "message": "非法任务状态迁移：completed -> completed"}`
400 ⇒ `{"error": "ValueError", "message": "网页API只允许verify；代码执行须使用明确授权的课程CLI"}`
⇒ ⚠️ **"照抄形状"不等于"照抄实现"** ⇒ **要看清候选侧有什么可复用的**
```

## 下一步

```
[ ] 读 §4.2 接口合同提示词 ✗ §4.3 实现提示词
[ ] ⚠️ **先查候选侧已有的 HTTP 服务**（`api_v2.py` ✗ `platform_api.py`）
    ⇒ **依据 L10/L11/L12 的教训：真模块不一定在第一眼看的文件里**
[ ] 写六段式 Spec ⇒ 实现两个端点 ⇒ §5 真实采购核对 ⇒ §6 同伴复验 ✗ 迁移
[ ] 🚩 **事项编号 ✗ 工作台登记** ⇒ **待本人**
```


---

# ⭐⭐⭐ L13 架构调查：**四层查完 ✗ 缺的三样定位到**

## ⭐⭐ HTTP 层在哪 —— **四步查出来的**

```
① 扫 `HTTPServer|BaseHTTPRequestHandler` ⇒ `platform_server.py` ✗ `server.py`
② 扫 `do_POST|do_GET` **的定义** ⇒ **只有这两个**
   ⚠️ **`platform_api.py` 有 `/api/` 字样 ✗ 但没有 `do_*`**
   ⇒ ⭐ **第一眼最像的那个**不是**HTTP 层**
③ `platform_api.py`：`class PlatformResponse`(:32) ✗ `class HarnessPlatformAPI`(:38)
④ `platform_server.py:47-49`：`/api/v1/*` 全部 ⇒ `api.dispatch(...)`
⇒ ⭐⭐⭐ **分层：`platform_server.py`（HTTP 层）⇒ `platform_api.py`（业务层 `dispatch` 路由表）**
   ⇒ **"新增端点"**不用**碰 `platform_server.py`**
```

## ⭐⭐⭐ `platform_api.py` 的路由表形状（**照抄 ✗ 不发明**）

```python
def dispatch(self, method, raw_path, headers, body) -> PlatformResponse:
    path, _, query_string = raw_path.partition("?")
    path = path.rstrip("/") or "/"
    ...
    try:
        if path == "/api/v1/health" and method == "GET":
            return PlatformResponse(200, {...})
        ...
        return PlatformResponse(404, {"error": "not_found", "message": "Harness API 路径不存在"})
    except KeyError as exc:            return PlatformResponse(404, {"error": "not_found", …})
    except (TypeError, ValueError) as exc: return PlatformResponse(422, {"error": "invalid_request", …})
⇒ ⭐ **现成出口 404 / 422** ✗ ⚠️ **没有 409** ⇒ **本讲要加**
```

## ⭐⭐⭐ 已有的持久化 `workbench/task_store.py`（287 行）

```
方法：`create` ✗ `get` ✗ `list` ✗ `append_event` ✗ ⭐ **`recover_automatic_tasks()`**
      ✗ `transition` ✗ `review(task_id, reviewer, decision, note)`
`tasks` 列：⭐ `requirement_id` ✗ ⭐ `business_refs_json` ✗ `spec_path` ✗
  ⭐ `reviewed_by`/`review_decision`/`review_note`/`reviewed_at` ✗
  ⭐ `automation_mode` ✗ ⭐ `execution_mode` ✗ ⭐ `write_scope_json` ✗ `version`
`task_events` 列：`from_status` ✗ `to_status` ✗ `detail` ✗ `actor` ✗ `evidence_json` ✗ `created_at`
⇒ ⭐⭐⭐ **辅导资料 §2 的"三种身份"表里全都有**：
   `requirement_id`（为什么做）✗ `id`（哪一次）✗ `business_refs_json`（影响哪个对象）
   ✗ `execution_mode`/`write_scope_json`（**最小权限**）✗ `version`+`task_events`（状态/事件分工）
⭐ **`create()` 已经把"任务行 + 受理事件"放在同一个事务里**
   ⇒ **正是辅导资料 §3 那句**
```

## ⚠️⚠️ 缺的三样（**首红扫描结论得到确认**）

```
① **没有"提交键"** ⇒ `create()` 每次 `uuid4()` ✗ **"同键找回"做不到 ✗ "409"更做不到**
② **没有 `POST /api/v1/tasks`** 与 **`GET /api/v1/tasks/<id>`**（扫描 `status_url` ⇒ 没找到）
③ **没有 `GET /api/v1/delivery/views/<id>`**（扫描 `delivery-view` ⇒ 没找到）
⇒ ⭐⭐⭐ **正好对应合同 `acceptance` ①**：「**API 接受请求后返回 Task ID 而非伪称完成。**」
```

## ⭐ 8001 是什么

```
候选自己的 `README.md:220`：`python -X utf8 main.py --host 127.0.0.1 --port 8001`
⇒ ⭐ **工作台首页 = 候选根目录 `main.py`**（**不是 `workbench.cli serve`（8000）**）
```

## ⭐ 实现方案（**先写 ✗ 再动手**）

```
① 复用 `TaskStore`（**不新建表 ✗ 不新建存储**）✗ 加"提交键"：
   没出现过 ⇒ 新建 ✗ 记内容指纹 ｜ 同键同指纹 ⇒ **返回原任务**（`spec_count` 不变）
   ｜ 同键异指纹 ⇒ ⭐ **抛 `Conflict`**
② `dispatch` 加三条路由：`POST /api/v1/tasks`（**202**）✗
   `GET /api/v1/tasks/<id>`（**200**）✗ `GET /api/v1/delivery/views/<id>`（**200**）
③ 加 `409` 出口 ✗ ④ 指纹要含 `request`/`actor`/`business_refs`（**参考实验改这三样各得 409**）
⑤ ⭐ **最小权限**：`POST` 只允许 `execution_mode == "verify"` ✗ **`codex` 要 400**
```

## 下一步

```
[ ] 写六段式 Spec ⇒ 实现 ⇒ **先红后绿 ✗ 同版本复验 ✗ 完整阻断回归**
[ ] §5 真实采购核对 ✗ §6 同伴复验 ✗ 迁移
[ ] 🚩 **事项编号 ✗ 工作台 8001 登记** ⇒ **待本人**
