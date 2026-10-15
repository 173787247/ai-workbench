# 结营毕设 · 应收账龄导出 · 六段需求（**本人确认版**）

> 🚩 **"本人确认版"四字与确认人**：**待本人**（**我不代签** ✓）
> ⭐ **本次新增的 Eval 名称**：**`ar_aging_export_keeps_columns`**
>   ⇒ ✅ **已确认未被占用**（`grep -rc` 在 `eval/` ✗ `workbench/` ✗ `tests/` 里全为 0）
>   ⇒ ✅ **不在合同 L16 的 `eval_cases` 里**（**合同只有 `delivery_evidence_and_review_controls`** ✓）
> ⚠️ **列规格的取舍**：🚩 **待本人**（**见"约束"第②条**——我按默认值填并标注** ✓）

## 来源

**原问题**（**不是现在编的 ✗ 我在 L15-B 的记录里就记过它** ✓）：
```
⭐ **L15-B（`TASK-E978708191`）给 `ReportService` 加了四个 CSV 出口**：
   `sales_summary_csv` ✗ `inventory_valuation_csv` ✗ `inventory_aging_csv` ✗
   `reorder_suggestions_csv` ✗ **列规格集中在 `REPORT_COLUMNS` 里** ✓
⚠️ **而 `ar_aging` 没有**：**它在整个 `reports.py` 里只出现一次（`def ar_aging` 自己）** ✓
   ⇒ ⭐ **所以它是**唯一没有 CSV 出口的报表**** ✓
⚠️ **而它的形状与那四个都不同**：**它返回 `dict`（`{as_of, buckets, total_cents, items}`）✗
   不是行列表** ✓
   ⇒ ⭐⭐ **现在把它丢给 `to_csv` 会是**：
     `to_csv([ar_aging(...)])` ⇒ **`'as_of,buckets,total_cents,items\r\n2026-10…'`** ✓
     ⇒ ⚠️⚠️ **它把 `dict` 的键当列 ✗ 而 `buckets` 与 `items` 是**嵌套结构**⇒
       在 CSV 里会变成 Python `repr`**（**`{'current': 0, …}` 与 `[{...}, …]`** ✓）
       ⇒ ⭐⭐⭐ **所以这不是"缺一个导出"✗ 而是"**照现状导出去就是一堆 repr"** ✓
```

**需求方**：⭐ **工作台「事项与决策」登记的本次事项**（**FlowERP 侧需求** ✓）
⇒ 🚩 **真实提出者**：**待本人**（**我不编造原话** ✓）

**规格来源与边界**（**辅助资料** ✓）：
```
⭐ **需求**：**财务要能拿到**应收账龄明细**去核销与催收** ✓
⭐ **边界**：**它要的是**逐张发票**的明细 ✗ 不是五个桶的汇总** ✓
   ⇒ ⭐ **依据**：**`ar_aging` 的 `items` 已经是明细行 ✗ 而 `buckets`/`total_cents` 是派生汇总** ✓
⭐ **命名与风格的现成对照**：⭐ **工作台里已有一条**对称的**业务 Eval**：
   ⭐ **`payable_aging_tracks_open_supplier_exposure`**（**应付账龄 ✗ 跟踪未结供应商敞口** ✓）
   ⇒ **它通过 `workbench.external_project.evaluate_case(...)` **委托**给独立 FlowERP 执行** ✓
     ⇒ ⭐ **所以本次的检查也走同一条委托路径** ✓
```

**基线事实**：
```
⭐ **控制仓库侧**：**合同 L16 的 `write_scope` = `flowerp/` ✗ `workbench/` ✗ `eval/` ✗
   `web/` ✗ `tests/`** ✓ ⇒ **本次要动 `eval/`** ✓
⭐ **独立 FlowERP 侧**：`FLOWERP_PROJECT_ROOT = /home/rchua/GO/flowERP-customer` ✗
   **`flowerp/reports.py` 是产品实现所在** ✗ **`eval/` 是业务检查所在** ✓
⚠️ **`AGENTS.md` 的边界**：「**本仓库不保留或导入 FlowERP 的 `flowerp` 包。
   **ERP 业务 Eval 在独立仓库中执行 ✗ 课程显式用例通过**进程边界委托****」✓
   ⇒ ⭐ **所以本次是**跨两个仓库**的交付** ✓
```

## 目标

```
⭐ **给 `ReportService` 加 `ar_aging_csv(principal, as_of=None) -> str`**：
   · ⭐ **导出的是**明细行**（`ar_aging(...)["items"]`）✗ 不是整个 `dict`** ✓
   · ⭐ **列规格由 `ar_aging` 自己声明**（**进 `REPORT_COLUMNS` ✗ 与那四个并列** ✓）
   · ⭐ **空结果**（**没有应收发票时**）⇒ **仍写出明细的列名 ✗ 行数为 0** ✓
✗ ⭐ **新增一条业务检查 `ar_aging_export_keeps_columns`**：
   · **独立 FlowERP 的 `eval/` 里写真正的断言**
   · **控制仓库的 `eval/cases.py` 里加一个 `evaluate_case(...)` 委托包装** ✓
✗ **工作台侧**：**从首页「事项与决策」登记本次事项 ✗ 让需求自动生成任务级 Spec** ✓
```

### ⭐ 列规格（**从 `items` 的构造取 ✗ 不照搬别的报表** ✓）

```
⭐ **`items` 的实际字段**（**从 SQL 的 `AS` 别名 + 循环里追加的键读出来** ✓）：
   `id, invoice_number, partner_id, partner_code, partner_name, due_date,
    outstanding_cents, overdue_days, bucket` ✓
⇒ ⭐ **本次导出取这七个**：
   `invoice_number, partner_code, partner_name, due_date,
    outstanding_cents, overdue_days, bucket`
   ⇒ **理由**：**导给财务看的是**单号 ✗ 客户编码与名称 ✗ 到期日 ✗ 未结金额 ✗
     逾期天数 ✗ 账龄桶**** ✓
   ⇒ ⚠️ **`id` 与 `partner_id` 是**内部主键**⇒ 不进面向财务的导出** ✓
     ⇒ 🚩 **这一条取舍**待本人**确认** ✓
```

## 非目标

```
❌ **不改 `ar_aging` 的返回值**（**它仍是 `dict`✗ 五个桶与总额照旧** ✓）
❌ ⭐ **不导出 `buckets` 与 `total_cents`**（**它们是派生汇总 ✗ 不是行明细** ✓）
   ⇒ ⭐ **若需要汇总导出 ✗ 那是**另一个需求**** ✓
❌ **不改 `to_csv` 的既有语义**（**"无规格的空结果明确拒绝"保留** ✓）
❌ **不改那四个已有出口**（**`sales_summary_csv` ✗ `inventory_valuation_csv` ✗
   `inventory_aging_csv` ✗ `reorder_suggestions_csv`** ✓）
❌ **不改 `ar_aging` 的 SQL ✗ 排序 ✗ 过滤条件 ✗ 账龄分桶规则** ✓
❌ **不改权限模型**（**仍要 `finance.read`** ✓）
❌ ⚠️ **不顺手修任何别的缺陷**（**含 L14 的 Escape 焦点 ✗ 16 条基线固有测试失败** ✓）
❌ **不做 Excel / PDF / 多表导出** ✓
```

## 约束

```
① ⭐ **明细与汇总分开**：**CSV 是**明细**✗ `buckets`/`total_cents` 不进它** ✓
② 🚩 **列的选择**：**七列**（**见"目标"**）⇒ **留哪些列 ✗ 汇总要不要单独出**待本人** ✓
③ ⭐ **规格来自报表自己**：**`ar_aging` 的列进 `REPORT_COLUMNS` ✗ 不照搬库存或销售的** ✓
   ⇒ ⭐ **依据**：**L15-A 那条经验的 `not_when` 原文**：
     「**销售导出不能直接沿用库存或供应商的列名 ✗ **要重新确认自己的规格****」✓
④ ⭐ **空结果保留列名**：**没有应收发票 ⇒ **仍写出七列表头**✗ 行数为 0** ✓
⑤ ⭐ **只读**：**导出前后同一发票的 `outstanding_cents` ✗ 账本 ✗ 分桶都不变** ✓
⑥ ⭐ **权限不变**：**仍要 `finance.read` ✗ 无权限要**明确拒绝**✗ 不能包成空文件** ✓
⑦ ⭐ **检查先红后绿**：**`ar_aging_csv` 现在**不存在**⇒ 新增检查必红** ✓
⑧ ⭐ **业务检查在独立仓库执行 ✗ 控制仓库只加委托包装** ✓
   ⇒ **依据**：**`AGENTS.md`**「**ERP 业务 Eval 在独立仓库中执行 ✗
     课程显式用例通过**进程边界委托****」✓
⑨ ⭐ **从首页发起**：**需求经「事项与决策」登记 ✗ 生成任务级 Spec** ✓
   ⚠️ **而首页只能 `verify`**（**`workbench_server.py:759`**：
     「**网页API只允许 verify；代码执行须使用明确授权的课程 CLI**」✓）
   ⇒ ⭐ **所以"从首页登记"与"用 CLI 执行"是**两步**✗ 要分别说明** ✓
⑩ ⭐ **六段顺序固定**（**`workbench/spec.py:10`** ✓）
```

## 验收用例

```
⭐ **本次新增的 Eval 名称**：**`ar_aging_export_keeps_columns`**（**阻断级** ✓）
   ⇒ ✅ **未被占用** ✗ ✅ **不在合同 `eval_cases` 里** ✓
   ⇒ ⭐ **它与既有的 `payable_aging_tracks_open_supplier_exposure` **对称但不重复****：
     · **那条**验**应付侧敞口**（**`ap_aging` 类**）
     · **这条**验**应收侧导出的列规格**
```

### 它要验的五件事

```
① ⭐ **明细导出可用**：**有应收发票时 ⇒ `ar_aging_csv()` 返回带七列表头的 CSV ✗ 行数 = 明细行数** ✓
② ⭐ **空结果保留列名**：**没有应收发票 ⇒ **表头仍是那七列**✗ 0 行** ✓
   ⇒ ⭐ **而且**不抛错**（**规格由报表自己给 ✗ 不是靠调用方传** ✓）
③ ⭐ **不混入汇总**：**CSV 里**没有** `buckets` / `total_cents` / `items` 这类键名** ✓
   ⇒ ⭐ **这一条正是**防止"把 `dict` 的键当列"**那个现状** ✓
④ ⭐ **只读**：**导出前后 `ar_aging()` 的 `buckets` ✗ `total_cents` ✗ `items` **逐字相同**** ✓
⑤ ⭐ **权限**：**无 `finance.read` 的身份 ⇒ **明确拒绝**（**不是空文件**）** ✓
```

**同时保留的既有检查**（**一条都不能少** ✓）：
```
⭐ **合同 L16 的一条**：`delivery_evidence_and_review_controls` ✓
⭐ **其余全部**（**含 `payable_aging_tracks_open_supplier_exposure` ✗ `inventory_export_is_stable`
   ✗ `raw_feedback_cannot_become_blocking` 等** ✓）
   ⇒ ⭐ **要跑一次完整套件记下来 ✗ 作为起点基线** ✓
```

## 完成定义

```
✅ **① 新增检查在改动前是红的**（**原始报告 ✗ 且红的原因是"目标能力缺失"** ✓）
✅ **② 既有检查在改动前后都通过**（**逐条可比 ✗ 不能把基线固有失败算进来** ✓）
✅ **③ `ar_aging_csv` 有数据时给出七列表头 ✗ 行数对** ✓
✅ **④ 空结果仍写出七列表头 ✗ 行数 0 ✗ 不抛错** ✓
✅ **⑤ CSV 里没有汇总键名** ✓
✅ **⑥ 导出只读**（**桶 ✗ 总额 ✗ 明细逐字不变** ✓）
✅ **⑦ 权限拒绝是明确拒绝 ✗ 不是空文件** ✓
✅ **⑧ 改动只在写集内**（**独立仓库的 `flowerp/reports.py` ✗ `eval/`；控制仓库的 `eval/`** ✓）
✅ **⑨ 业务检查在独立仓库跑 ✗ 控制仓库只加委托包装** ✓
✅ **⑩ 从首页登记的记录可回查**（**请求 ID ✗ 生成的任务 ✗ 请求原文** ✓）
✅ **⑪ 交付「完成思路 + 代码链接」**（**毕设的要求** ✓）
🚩 **⑫ 列规格取舍与具名审核** ⇒ **待本人** ✓
🚩 **⑬ 原使用者的实际复验** ⇒ **待本人** ✓
```

---

**签署**：🚩 **待本人确认**（**我不代签 ✗ 不编造反馈** ✓）
