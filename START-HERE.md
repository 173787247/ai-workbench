# START-HERE · 个人 AI 研发工作台（Codex AI 工程交付行动营）

> **写给下一个会话 —— 读完这一份就能接手。**
> 最后更新：2026-10-16 02:30 +0800
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
