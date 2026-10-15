# 结营毕设 · ⭐⭐⭐⭐⭐ 真实小问题定义（**从仓库现状找 ✗ 不编** ✓）

- **日期**：2026-10-16｜**入口**：**工作台首页 `http://127.0.0.1:8001/` 的「事项与决策」** ✓
- **问题来源**：⭐ **我在 L15-B 的记录里就记下过它**（**不是现在才编的** ✓）

## 一、⭐⭐⭐ 首页链路（**先读懂它要什么** ✓）

```
⭐ **导航四项**：
   · ⭐ 「**◇ 事项与决策 <small>新需求</small>**」（`id="new-decision"` ✗ `data-view="decision"` ✓）
   · 「**◇ 交付记录 <span id="review-count" class="count">0</span>**」（**待审计数** ✓）
   · 「**▤ 课程与练习**」✗ 「**↗ 打开 FlowERP <small>客户项目</small>**」（**`http://127.0.0.1:8000`** ✓）
⭐ ⭐⭐⭐⭐⭐ **登记需求的表单**：
   `<textarea id="code-requirement-spec" rows="8" maxlength="40000"
     placeholder="**粘贴包含来源 ✗ 目标 ✗ 非目标 ✗ 约束 ✗ 验收用例 ✗ 完成定义的具体需求**">` ✓
   ⇒ ⭐ **它要**六段 Spec**** ✗ **正是 `workbench/spec.py:10` 那六段** ✓
⭐ **API 面**（**从 `app.js` 取** ✓）：`/api/v1/delivery/requests` ✗ `/api/v1/delivery/views`
   ✗ `/api/v1/tasks/` ✗ `/api/course/current` ✗ `/api/cockpit/upgrade` ✓
   ⇒ ⚠️ **`GET /api/v1/delivery/requests` ⇒ **404**** ⇒ ⭐ **它是 `POST`-only** ✓
     ⇒ **实现在 `workbench/workbench_server.py:757`**（**控制仓库侧 ✗ 不在候选** ✓）
```

## 二、⭐⭐⭐⭐⭐ 毕设的问题：**`ar_aging` 是唯一没有 CSV 出口的报表**

### 事实（**在**对的候选**上核实** ✓）

```
⭐ **候选**：`…/course-worktrees/**TASK-E978708191**`（**L15-B ✗ 它有那四个出口** ✓）
   ✅ `sales_summary_csv`(:123) ｜ `inventory_valuation_csv`(:141) ｜
      `inventory_aging_csv`(:156) ｜ `reorder_suggestions_csv`(:189) ✓
   ✗ `REPORT_COLUMNS` **四个键**：`sales_summary` ✗ `inventory_valuation` ✗
      `inventory_aging` ✗ `reorder_suggestions` ✓
   ✗ ⭐ **`ar_aging` 在整个 `reports.py` 里只出现 **1** 次**（**就是 `def ar_aging` 自己**）
     ⇒ ⭐⭐⭐⭐⭐ **所以它是**唯一没有 CSV 出口的报表**** ✓
⚠️ **而 `TASK-FE48B898DB`（L16 的候选）里那些出口**一个也没有****
   （**它从 `course/l16-start` 建的 ✗ 不含 L15-B** ✓）
   ⇒ ⭐ **这又一次说明**看代码必须先确认候选**✓ 我上一轮就差点跨候选下结论** ✓
```

### `ar_aging` 的真实形状（**实测 ✗ 不是读注释** ✓）

```
⭐ `def ar_aging(self, principal: Principal, as_of: str | None = None) -> **dict**:` ✓
   ⇒ **返回 `dict`✗ 键 `['as_of','buckets','items','total_cents']`** ✓
     · ⭐ **`items` = 明细行**（**每行 `id` ✗ `invoice_number` ✗ `partner_code` ✗ `partner_name`
       ✗ `due_date` ✗ `outstanding_cents` ✗ `overdue_days` ✗ **`bucket`**** ✓）
     · ⭐ **`buckets` = 五个账龄桶的汇总**（`current` ✗ `1_30` ✗ `31_60` ✗ `61_90` ✗ `over_90` ✓）
     · **`as_of` ✗ `total_cents`** ✓
⚠️ **现在把它丢给 `to_csv` 会怎样**（**实测** ✓）：
   `to_csv([ar_aging(...)])` ⇒ **`'as_of,buckets,total_cents,items\r\n2026-10…'`**
   ⇒ ⚠️⚠️ **它把 **`dict` 的键**当列**✗ **`buckets` 与 `items` 是**嵌套结构****⇒
     **在 CSV 里会变成 Python `repr`**（**`{'current': 0, …}` 和 `[{...}, …]`** ✓）
     ⇒ ⭐⭐⭐ **所以这不是"缺一个导出"✗ 而是"**如果把整个 dict 当行导出 ✗ 会输出一堆 repr"** ✓
```

## 三、⭐⭐⭐⭐ 所以本次交付要做什么

```
⭐ **给 `ReportService` 加 `ar_aging_csv(principal, as_of=None)`**：
   · ⭐ **导出的是**明细行**（`items`）✗ 列规格取自**明细行自己的字段**** ✓
   · ⭐ **边界**：**`buckets` 与 `total_cents` 是**汇总**✗ 不进这个 CSV** ✓
     ⇒ **如果需要汇总导出 ✗ 那是另一个需求**（**写进非目标** ✓）
   · ⭐ **空结果**：**没有应收发票时 ⇒ **仍写出明细的列名**✗ 行数为 0** ✓
     ⇒ ⭐⭐ **这正是 L15-A 那条经验的**下一次迁移****：
       「**合法空结果必须保留已确认的字段规格**」✓
       ⇒ ⭐ **而 `not_when` 里写着**：「**销售导出不能直接沿用库存或供应商的列名 ✗
         **要重新确认自己的规格****」⇒ ⭐ **本次正是"重新确认"** ✓
         ⇒ ⭐⭐⭐ **`ar_aging` 的规格与那四个**都不同****（**它是财务侧的应收账龄** ✓）
```

### ⭐ 列规格（**从 `items` 的构造取 ✗ 不照搬别的报表** ✓）

```
⭐ **`items` 的列**（**从 SQL 的 `AS` 别名读** ✓）：
   `id, invoice_number, partner_id, partner_code, partner_name, due_date,
    outstanding_cents, overdue_days` ✗ **加上循环里追加的 `bucket`** ✓
   ⇒ ⚠️ **而 `partner_id` 与 `partner_code`/`partner_name` 重复** ⇒ **要决定留哪些** ✓
     ⇒ ⭐ **本次取**：`invoice_number, partner_code, partner_name, due_date,
        outstanding_cents, overdue_days, bucket` ✓
       ⇒ **理由**：**导给财务看的是单号 ✗ 客户 ✗ 到期日 ✗ 未结金额 ✗ 逾期天数 ✗ 账龄桶** ✓
         ⇒ ⚠️ **`id` 与 `partner_id` 是内部主键 ✗ 不进面向财务的导出** ✓
           ⇒ ⭐ **这个取舍要写进 Spec 的"约束"✗ 并由人确认** ✓
```

## 四、⭐ 为什么它适合当毕设

```
✅ **真实**：**不是编的 ✗ 我在 L15-B 的记录里已经把它列为剩余缺口** ✓
✅ **范围受控**：**一个方法 + 一个列规格 + 一条新增检查** ✓
✅ **能先红后绿**：**`ar_aging_csv` 现在**不存在**** ⇒ **检查必红** ✓
✅ **能迁移经验**：**L15-A 的"空结果保留规格"✗ L15-B 的"报表各自声明规格"**
   ⇒ ⭐ **本次是第三次迁移 ✗ 而且**边界不同**（**明细 vs 汇总** ✓）
✅ **能走首页**：**它是 FlowERP 侧的需求 ✗ 可以从工作台的"事项与决策"发起** ✓
✅ **能复验**：**空结果 ✗ 有数据 ✗ 只读 ✗ 权限** 四条都能验 ✓
```

## 五、⭐ 待办

```
[ ] ⭐ **从首页登记它**（**用 `code-requirement-spec` 那栏粘贴六段 Spec** ✓）
    ⇒ ⚠️ **要先写六段 Spec ✗ 而且它必须**逐字**包含新增 Eval 名** ✓
[ ] ⭐ **记下首页返回的请求 ID 与生成的任务** ✓
[ ] ⭐ **后续按课程那条链走**（**Spec ⇒ 检查先红 ⇒ 实现 ⇒ Eval ⇒ 人审 ⇒ 证据** ✓）
[ ] ⭐ **交付「完成思路 + 代码链接」** ✓
[ ] 🚩 **待本人**：**列规格的取舍**（**留哪些列 ✗ 汇总要不要**）✗ **人审** ✓
```
