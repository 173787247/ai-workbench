# 结营毕设 · 🎉🎉🎉 **红 ⇒ 绿完成**（**独立 FlowERP 侧 ✗ 20/20 全绿 ✗ 无回归** ✓）

- **日期**：2026-10-16｜**仓库**：`/home/rchua/GO/flowERP-customer`（`HEAD = 70660dd` ✗ 起点干净 ✓）
- **证据**：`capstone/run-before/`（**起点**）✗ `capstone/run-after/`（**新增检查红 ⇒ 修好绿**）

## 一、⭐⭐⭐⭐⭐ 三份报告串起来（**这是本毕设的核心证据** ✓）

| 阶段 | 命令 | 退出码 | 读数 |
|---|---|---|---|
| ⭐ **起点基线** | `eval.harness --suite all` | ✅ **0** | `{total: **19**, passed: **19**, decision: 'pass'}` |
| ⭐ **加检查后（未实现）** | `--suite blocking --case ar_aging_export_keeps_columns` | ⚠️ **1** | `{total:1, passed:**0**, blocking_failed:**1**, decision:'**block**'}` |
| ⭐ **加检查后的整批** | `--suite blocking` | ⚠️ **1** | `{total: **20**, passed: **19**, blocking_failed: **1**}` |
| ⭐ **实现之后** | `--case ar_aging_export_keeps_columns` | ✅ **0** | `{total:1, passed:**1**, decision:'**pass**'}` |
| ⭐ **完整套件** | `--suite all` | ✅ **0** | `{total: **20**, passed: **20**, decision: 'pass'}` |

### ⭐ 红的原因**正是"目标能力缺失"**（**不是缺依赖 ✗ 不是环境错** ✓）

```
⭐ **未实现时**：`AttributeError: 'ReportService' object has no attribute 'ar_aging_csv'` ✓
   ⇒ ⭐ **依据**：**手册 D 区**「**未知用例 ✗ 环境错误不算产品缺口**」✓
     ⇒ ✅ **这条红**说明的是产品缺口**✗ 不是环境没配好** ✓
```

### ⭐⭐ 与起点**逐条对账**（**不能只看总数** ✓）

```
起点：{total: 19, passed: 19, blocking_failed: 0, decision: 'pass'}
现在：{total: 20, passed: 20, blocking_failed: 0, decision: 'pass'}
⭐ **新增**：['ar_aging_export_keeps_columns']
⭐ **减少**：（空）
⭐ **从绿变红的**：（无）
⇒ ✅ **所以既没有回归 ✗ 也不是"总数一样就算过"** ✓
```

## 二、⭐⭐⭐ 改了什么（**`git diff --stat` ✗ 80 insertions** ✓）

```
eval/cases.py      | 58 ++++++++++++++++++++++++++++++
eval/harness.py    |  1 +
flowerp/reports.py | 21 ++++++++++++
3 files changed, 80 insertions(+)
```

### ① `flowerp/reports.py`：**21 行**（**模块常量 + 出口方法** ✓）

```python
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

### ② `eval/cases.py`：**58 行**（**新检查 ✗ 照既有风格** ✓）

它验五件事：
```
① **空结果**：**没有应收发票 ⇒ 只有表头一行 ⇒ 表头正好是那七列** ✓
② **不混汇总**：**表头里不能出现 `as_of` / `buckets` / `total_cents` / `items`** ✓
③ **有数据**：**明细行数等于 `ar_aging()["items"]` 的长度 ✗ 而且 `ar_aging` 仍返回带 `items` 的 `dict`**
   ⇒ ⭐ **这一条同时守住"不改 `ar_aging` 的返回值"** ✓
④ **只读**：**导出前后 `ar_aging()` 的三部分逐字相等** ✓
⑤ **权限**：**无 `finance.read` 的身份 ⇒ `PermissionDenied`**（**不是拿到空文件** ✓）
```

### ③ `eval/harness.py`：**1 行**（**注册** ✓）

```python
("ar_aging_export_keeps_columns", "blocking", cases.ar_aging_export_keeps_columns),
```

## 三、⚠️⚠️ 两个**先核实基线才发现的**事实（**都改了设计** ✓）

```
⚠️ **① 这个仓库的 `to_csv` 是**旧版****：
   `flowerp/reports.py:191~197`：
     `def to_csv(rows: list[dict]) -> str:`
     `    **if not rows: return ""**`（**静默返回空串 ✗ 停在 L15-A 之前**）
   ⇒ ⭐ **它**没有** `fieldnames` 参数**✗ **也**没有**"无规格就拒绝"** ✓
     ⇒ ⭐⭐ **所以我原 Spec 里写的"列规格进 `REPORT_COLUMNS`"做不到** ✓
       ⇒ ✅ **改设计**：**`ar_aging_csv` **自己用 `csv.DictWriter` 显式给 `fieldnames`**** ✓
         ⇒ ⭐ **这样它**不依赖 `to_csv` 的任何版本**** ✓
⚠️ **② L15-B 的四个出口**不在**这个仓库里****：
   `grep -c '_csv(self\|REPORT_COLUMNS' flowerp/reports.py` ⇒ **0** ✓
   ⇒ ⭐ **因为 `TASK-E978708191` 也停在 `review` ✗ 没合入** ✓
     ⇒ ⭐⭐ **所以本次交付**不能依赖另一个未被接受的候选的状态**** ✓
       ⇒ ✅ **正是辅导资料那句的反向**：
         「**不能把当前客户仓库的失败拼到另一份候选上**」
         ⇒ **同理：也不能把另一份候选的**存在**当成前提** ✓
```

## 四、⚠️ 一处要如实记的不一致（**与毕设无关 ✗ 但要说** ✓）

```
⚠️ **`HEAD = 70660dd`** 的 message：「**fix(flowerp): 修复采购原子性 ✗ 空导出和日期筛选**」
   ⇒ **"空导出"⇒ 那是 L15-A 的内容** ✓
   ⇒ ⭐ **而 L15-A 的 Task（`TASK-AD82BFE14C`）**仍停在 `review` ✗ 从没被具名接受**** ✓
     ⇒ ⭐⭐ **所以**改动进了产品仓库 ✗ 而课程 Task 没走完审核**** ✓
       ⇒ ⚠️ **按纪律如实记 ✗ 不解释成"已通过"** ✓
```

## 五、⚠️ 我自己又踩了一次（**记下来 ✗ 因为它和检查绿不绿无关但很典型** ✓）

```
⚠️ **我写的手动演示脚本**：`ERPService(...).ensure_local_defaults()`
   ⇒ `AttributeError: 'ERPService' object has no attribute 'ensure_local_defaults'` ✓
   ⇒ ⭐ **又一次**假设 API**（**本会话第 N 次** ✓）
     ⇒ ⭐⭐ **而**检查本身是对的**：**它用的是 `_service()` 夹具 ✗ 那是既有代码** ✓
       ⇒ ✅ **所以"检查绿"与"我的临时脚本错"可以同时成立** ✓
         ⇒ ⭐ **要分清**：**报告说的是检查 ✗ 而我贴的一段演示说的是另一件事** ✓
```

## 六、⭐ 待办

```
[ ] ⭐ **控制仓库加委托包装**（`eval/cases.py` ✗ 照 `payable_aging_tracks_open_supplier_exposure`
    的 `evaluate_case(...)` 写法 ✓）✗ **并在 `eval/harness.py` 注册** ✓
[ ] ⭐ **跑控制仓库的完整套件** ✗ **确认只多一条 ✗ 无回归** ✓
[ ] ⭐ **交付「完成思路 + 代码链接」**（**毕设的要求** ✓）
[ ] ⚠️ **`spec_sha256` 为空的原因** ✗ **`ar_aging` 是否要在 API 层暴露**（**本次未做 ✗ 属另一需求** ✓）
[ ] 🚩 **待本人**：**列规格取舍**（**七列留哪些 ✗ 汇总要不要**）✗ **具名审核** ✗ **原使用者复验** ✓
```
