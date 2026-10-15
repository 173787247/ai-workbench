# 结营毕设 · 完成思路 + 代码链接

> 🚩 **本文件是本毕设的**正式交付物**** ✗ **对应要求**：「**用建好的工作台组织本人与 AI 助手
> 解决一个真实小问题 ✗ 并按毕设要求交付「完成思路 + 代码链接」**」✓
> ⚠️ **凡需具名或对外可见的动作**：🚩 **待本人** ✗ **我不代签 ✗ 不擅自推送** ✓

**日期**：2026-10-16｜**执行者**：🚩 **待本人署名**（**会话里用的 actor 是 `course-learner` ✗ 占位**）

---

## 一、完成思路

### 1. 问题是怎么找到的（**不是编的 ✗ 是从既有记录里长出来的** ✓）

```
⭐ **它的最早出处是我自己写的 L15-B 记录**：
   L15-B（`TASK-E978708191`）给 `ReportService` 加了四个 CSV 出口
   （`sales_summary_csv` ✗ `inventory_valuation_csv` ✗ `inventory_aging_csv` ✗
   `reorder_suggestions_csv`），列规格集中在 `REPORT_COLUMNS`。
   ⚠️ **而我在那份记录里就写下了剩余缺口**：**`ar_aging` 返回 `dict` ✗
      **结构不同 ⇒ 没有 CSV 出口** ✓
⇒ ⭐ **所以这条需求的来源是**一次真实交付暴露出的缺口**** ✗ **不是为毕设另找的题目** ✓
```

### 2. 先用工作台登记（**这是"用建好的工作台组织"那一步** ✓）

```
⭐ **入口**：**工作台首页 `http://127.0.0.1:8001/` 的「事项与决策」** ✓
   ⇒ ⭐ **依据**：`AGENTS.md`「**工作台唯一日常入口是 `http://127.0.0.1:8001/`…
      **需求从首页"事项与决策"开始****」✓
⭐ **实际动作**：**`POST /api/v1/delivery/requests`** ✗ **带 `verification_key`** ✓
   ⇒ ⭐ **它生成了 `TASK-892BF97942`**（**`accepted: true` ✗ `execution_mode: "verify"`**）✓
⚠️ **这一路上有三条约束是**撞出来才知道的****（**都留了原始报错** ✓）：
   · **请求体上限 8192 字节**（`workbench_server.py:599` 的 `else 8192`）
   · **现场需求描述上限 1000 字符**（**而网页表单写的是 40000 ✗ 两者不一致** ✓）
   · **必须先 `GET /api/course/verification?lesson=16` 拿 `verification_key`** ✓
⇒ ⭐ **这一段的完成思路是**：**让报错指路 ✗ 每步都把报错原文记下来** ✓
```

### 3. 判断真缺口（**`acceptance` ①："仓库基线中尚未实现"** ✓）

```
⚠️ **我没有直接动手 ✗ 而是先在**将要实施的那份基线**上核实** ✓
   ⇒ ⭐ **依据**：**辅导资料 §3**「**课程命令使用的起始标签可能包含历史组合源码 ✗
      和你刚冷启动的当前双仓版本不同。**正式执行前 ✗ 须在**将要实施的那份基线**上
      **再次确认缺口与检查结果****」✓
⭐ **核实结果**：**`ar_aging` 在整个 `reports.py` 里只出现一次（`def ar_aging` 自己）** ✗
   **而同类的四个都有 `_csv` 出口** ✓
⇒ ⭐ **所以它是**唯一没有 CSV 出口的报表**✗ 缺口是真的** ✓
```

### 4. ⭐⭐ 两次**据实改设计**（**这是本毕设最有价值的部分** ✓）

```
⚠️ **第一次**：**我以为可以复用 L15-B 的 `REPORT_COLUMNS`** ✓
   ⇒ ⭐ **实测**：**`grep -c '_csv(self\|REPORT_COLUMNS' flowerp/reports.py` ⇒ **0**** ✓
     ⇒ ⭐⭐ **因为 L15-B 的 `TASK-E978708191` 也停在 `review` ✗ 没合入产品仓库** ✓
       ⇒ ✅ **改设计**：**`ar_aging_csv` **自己声明 `AR_AGING_COLUMNS` ****✗
         **不依赖另一个未被接受的候选的状态** ✓
         ⇒ ⭐ **依据（反向同理）**：**辅导资料**「**不能把当前客户仓库的失败拼到
           另一份候选上**」⇒ **也不能把另一份候选的**存在**当成前提** ✓
⚠️ **第二次**：**我以为可以直接调 `self.to_csv(rows, fieldnames=…)`** ✓
   ⇒ ⭐ **实测**：**那个仓库的 `to_csv` 还是旧版**：
     `def to_csv(rows: list[dict]) -> str:` ✗ `if not rows: return ""`
     ⇒ ⭐⭐ **它**没有** `fieldnames` 参数 ✗ 也**没有**"无规格就拒绝"**（**停在 L15-A 之前** ✓）
       ⇒ ✅ **改设计**：**`ar_aging_csv` **自己用 `csv.DictWriter` 显式给 `fieldnames`****✗
         **这样它不依赖 `to_csv` 的任何版本** ✓
```

### 5. 检查先行（**红 ⇒ 绿 ✗ 而不是"写完再说"** ✓）

```
⭐ **顺序**：**先只加检查 ⇒ 跑 ⇒ 它必红 ⇒ 再实现 ⇒ 再跑 ⇒ 它应绿** ✓
   ✗ ⭐ **而且红的**原因**必须能解释成"目标能力缺失"** ✓
     ⇒ **依据手册 D 区**：「**未知用例 ✗ 环境错误不算产品缺口**」✓
```

### 6. 两层验证（**产品侧的红 ⇒ 绿 ✗ 控制侧的委托与无回归** ✓）

```
⭐ **产品侧**（**独立 FlowERP**）：**起点 `19/19` ⇒ 加检查 `1 红` ⇒ 实现后 `20/20`** ✓
⭐ **控制侧**（**工作台**）：**委托包装**证明**进程边界是通的 ✗ 且项目类 `19 ⇒ 20` 只新增不回归** ✓
⚠️ **我如实区分这两段 ✗ 不把控制侧的 `20/20` 说成"产品侧被验了两次"** ✓
```

---

## 二、代码链接

### ⚠️⚠️ 先说明一件**必须由你决定**的事

```
⚠️ **两个仓库都有 GitHub 远端**：
   · **FlowERP**：`origin https://github.com/**congde/flowERP.git**`
   · **控制仓库**：`origin https://github.com/**congde/CodexFDE.git**`
⇒ ⭐ **我只做了**本地提交 ✗ **没有推送** ✓
  ⇒ ⭐⭐ **因为推送是**对外可见的改动****（**别人可能已经看到或复刻** ✓）
    ⇒ 🚩 **按规则：你的仓库不是我的 ✗ 要你明确要求那个具体仓库那个改动才推** ✓
      ⇒ ✅ **所以下面给两种链接**：**本地提交 SHA**（**现在就能用**）✗
        **GitHub 链接**（**待你确认推送后才有** ✓）
```

### 链接一：**本地提交**（**已存在 ✗ 现在可用** ✓）

| 仓库 | 提交 | 说明 |
|---|---|---|
| ⭐ **独立 FlowERP** | **`a11cbe219fe302de38aee21dc5f42377452e1279`** | **`feat(flowerp): 应收账龄可导出明细`** ✗ **3 files ✗ +80** |
| ⭐ **控制仓库** | **`a6dfe4e234aaf4d48c1445d8b34f58c45a3b7b4c`** | **`eval: 委托应收账龄导出检查到独立 FlowERP`** ✗ **2 files ✗ +7 −1** |

**本地查看命令**（**复制即用** ✓）：
```bash
# 产品侧：新增的出口与列规格
cd /home/rchua/GO/flowERP-customer
git show a11cbe2 --stat
git diff HEAD~1 HEAD -- flowerp/reports.py

# 控制侧：委托包装与注册
cd /home/rchua/GO/CodexFDE
git show a6dfe4e
git diff HEAD~1 HEAD -- eval/
```

### 链接二：**GitHub 链接**（🚩 **待你确认 ✗ 现在还不存在** ✓）

```
🚩 **推送后**会是（**我**没有**推送 ✗ 所以现在打开会是旧内容** ✓）：
   · FlowERP：https://github.com/congde/flowERP/commit/a11cbe2…
   · 控制仓库：https://github.com/congde/CodexFDE/commit/a6dfe4e…
⇒ ⭐ **要推送的话 ✗ 你明确说"把这两个提交推到那两个仓库"✗ 我再做** ✓
  ⇒ ⚠️ **而按规则我不批量推广到"类似的仓库"** ✓
```

### 代码清单（**改了什么 ✗ 为什么** ✓）

#### ⭐ 产品侧 `a11cbe2`（**80 insertions ✗ 3 文件**）

```python
# flowerp/reports.py（21 行）
#: 应收账龄导出的明细列。取自 ar_aging 里 items 的字段与它追加的 bucket；
#: id 与 partner_id 是内部主键，不进面向财务的导出。
AR_AGING_COLUMNS = ("invoice_number", "partner_code", "partner_name", "due_date",
                    "outstanding_cents", "overdue_days", "bucket")

    def ar_aging_csv(self, principal: Principal, as_of: str | None = None) -> str:
        """应收账龄的明细导出：逐张发票一行，空结果也保留列名。…"""
        report = self.ar_aging(principal, as_of)
        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=list(AR_AGING_COLUMNS),
                                extrasaction="ignore")
        writer.writeheader()
        writer.writerows(report["items"])
        return output.getvalue()
```

```python
# eval/cases.py（58 行）：ar_aging_export_keeps_columns 验五件事
① 空结果：没有应收发票时只有表头一行，且表头正好是那七列
② 不混汇总：表头里不能出现 as_of / buckets / total_cents / items
③ 有数据：明细行数等于 ar_aging()["items"] 的长度，且它仍返回带 items 的 dict
④ 只读：导出前后 ar_aging() 的分桶、总额、明细逐字相等
⑤ 权限：没有 finance.read 的身份要 PermissionDenied，不是拿到空文件

# eval/harness.py（1 行）：注册进 EVALS
```

#### ⭐ 控制侧 `a6dfe4e`（**+7 −1 ✗ 2 文件**）

```python
# eval/cases.py：委托包装（照既有 payable_aging_tracks_open_supplier_exposure 的写法）
def ar_aging_export_keeps_columns():
    from workbench.external_project import evaluate_case
    return evaluate_case('ar_aging_export_keeps_columns')

# eval/harness.py：PROJECT_CASES 加一个名字，EVALS 加一行（blocking）
```

---

## 三、原始证据（**都在工作仓库里 ✗ 可逐条打开** ✓）

| 证据 | 位置 | 关键读数 |
|---|---|---|
| ⭐ **产品侧起点基线** | `capstone/run-before/all.json` | `{total:19, passed:19, decision:'pass'}` ✗ **退出码 0** |
| ⭐ **加检查后（未实现）** | `capstone/run-after/new.json` | `{total:1, passed:**0**, blocking_failed:1, decision:'block'}` ✗ **退出码 1** ✗ ⭐ **红因**：`AttributeError: 'ReportService' object has no attribute 'ar_aging_csv'` |
| ⭐ **实现之后** | `capstone/run-after/fixed.json` | `{total:1, passed:1, decision:'pass'}` ✗ **退出码 0** |
| ⭐ **产品侧完整套件** | `capstone/run-after/all.json` | `{total:**20**, passed:**20**, decision:'pass'}` ✗ **退出码 0** |
| ⭐ **控制侧 before（项目类）** | `capstone/run-control/before-pc.json` | `{total:19, passed:19}` ✗ **`grep -c` 我的名字 ⇒ 0** |
| ⭐ **控制侧 after（项目类）** | `capstone/run-control/after-pc.json` | `{total:**20**, passed:**20**}` ✗ ⭐ **新增 `['ar_aging_export_keeps_columns']` ✗ 无回归** |
| ⭐ **首页登记** | `capstone/04-registered.md` ✗ `/tmp/cap-post4.json` | `{"task_id":"**TASK-892BF97942**","accepted":true,"execution_mode":"verify"}` |
| ⭐ **委托跨进程的原证据** | `capstone/run-control/new.log` | `[PASS] … 106 ms` ✗ **detail 里有 `FlowERP：/home/rchua/GO/flowERP-customer；…；退出码 0；…`** |
| **两个仓库的 diff** | `capstone/links/{flowERP-customer,CodexFDE}.diff` | |

---

## 四、⚠️ 未完成与缺口（**不粉饰** ✓）

```
🚩 **需要你（人）做的**：
   · ⭐ **列规格取舍**：**七列**（`invoice_number` ✗ `partner_code` ✗ `partner_name` ✗
     `due_date` ✗ `outstanding_cents` ✗ `overdue_days` ✗ `bucket`）⇒
     **留哪些 ✗ 汇总（`buckets`/`total_cents`）要不要单独出** ✓
     ⇒ **我按默认值填并标了"待本人"** ✗ **没有代签** ✓
   · ⭐ **具名审核**：**本毕设**没有任何具名接受****（**`TASK-892BF97942` 的 `reviewed_by` 是 `None`** ✓）
   · ⭐ **原使用者的实际复验**：**没有真实反馈者在修复后的版本上重做原操作** ✓
   · 🚩 **是否推送那两个提交**（**对外可见 ✗ 只有你能定** ✓）

⚠️ **我没做的（如实列）**：
   · **`ar_aging` 没有在 API 层暴露**（**本次只做了 `ReportService` 的出口** ⇒
     **HTTP 侧要另立需求** ✓）
   · **`buckets` 与 `total_cents` 没有导出通道**（**按非目标排除** ✓）
   · **工作台首页那条链路只走到"登记 + verify"** ⇒
     ⚠️ **代码执行走的是课程 CLI**（**依据 `workbench_server.py:759`**：
       「**网页API只允许 verify；代码执行须使用明确授权的课程 CLI**」✓）
     ⇒ ⭐ **所以"从首页发起"与"用 CLI 执行"是两步 ✗ 我如实分开写了** ✓
   · ⚠️ **`spec_sha256` 为空**（**三个 Task 都空 ⇒ 是普遍现象 ✗ 原因未查** ✓）
   · ⚠️ **16 条控制仓库的基线固有测试失败**（**与本毕设无关 ✗ 未修** ✓）
   · ⚠️ **L14 的 Escape 焦点缺陷**（**仍是同一未修缺陷 ✗ 按审查反例**关联为新观察** ✓）
```

## 五、⚠️ 一处要如实记的不一致

```
⚠️ **产品仓库 `HEAD~1 = 70660dd`** 的 message：
   「**fix(flowerp): 修复采购原子性 ✗ **空导出**和日期筛选**」
   ⇒ ⭐ **"空导出"就是 L15-A 的内容** ✓
     ⇒ ⚠️ **而 L15-A 的 Task（`TASK-AD82BFE14C`）**仍停在 `review` ✗ 从没被具名接受**** ✓
       ⇒ ⭐⭐ **所以**改动进了产品仓库 ✗ 而课程 Task 没走完审核**** ✓
         ⇒ ⚠️ **我如实记 ✗ 不把它解释成"已通过"** ✓
```

## 六、⭐ 一句话总结

```
⭐ **用工作台（首页「事项与决策」⇒ `TASK-892BF97942`）组织了一次真实交付**：
   **从 L15-B 记录里长出的缺口** ⇒ **在将要实施的基线上核实** ⇒
   ⭐ **两次据实改设计**（**不依赖未合入的候选 ✗ 不用不存在的 `to_csv` 签名**）⇒
   **先加检查（红）⇒ 实现（绿）⇒ 两层验证（产品侧 19⇒20 ✗ 控制侧委托 19⇒20 ✗ 都无回归）** ✓
⇒ ⭐ **代码链接**：**本地提交 `a11cbe2`（产品）✗ `a6dfe4e`（控制）**
   ⇒ 🚩 **GitHub 链接待你确认推送**
```
