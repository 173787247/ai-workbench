# 结营毕设 · ⭐ 独立 FlowERP 的基线事实（**先查清 ✗ 再动手** ✓）

- **日期**：2026-10-16｜**仓库**：`/home/rchua/GO/flowERP-customer` ✓

## 一、⭐⭐ 仓库状态

```
⭐ **它是 git 仓库** ✗ `HEAD = **70660dd**` ✗ **工作区干净**（`git status --short` 空 ✓）
   `70660dd **fix(flowerp): 修复采购原子性 ✗ 空导出和日期筛选**`
   `46eeb6f docs: 完善启动 ✗ 演示账号与 ERP 架构说明`
```

### ⚠️ 一处要如实记的不一致

```
⚠️ **`70660dd` 的 message 里有"**空导出**"⇒ **那正是 L15-A 的内容** ✓
   ⇒ ⭐ **而 L15-A 的 Task（`TASK-AD82BFE14C`）**仍停在 `status = "review"`
     ✗ `reviewed_by = None`**✗ 从没被具名接受** ✓
     ⇒ ⭐⭐ **所以**改动进了产品仓库 ✗ 而课程 Task 没走完审核**** ✓
       ⇒ ⚠️ **按纪律如实记 ✗ 不解释成"已通过"** ✓
         ⇒ ⭐ **它对毕设的影响**：**我在 `lesson-15-submission/` 里说 L15-A 停在 `review`**
           ✗ **而产品仓库已经有那个字符串** ⇒ ⭐ **两件事都对 ✗ 只是**层级不同**** ✓
```

## 二、⭐⭐⭐ 业务检查的写法（**照它写 ✗ 不发明** ✓）

```
⭐ **`eval/cases.py`（497 行）**：**每个检查是一个 `def <name>() -> str`**
   `:27 def _service() -> tuple[tempfile.TemporaryDirectory, ERPService]:`（**公共夹具** ✓）
   `:33 stock_never_negative` ✗ `:46 receiving_is_idempotent` ✗ `:55 inventory_export_is_stable`
   ✗ `:78 cancellation_releases_reservation` ✗ `:89 illegal_transition_is_blocked`
   ✗ `:98 purchase_requires_approval` ✗ `:111 purchase_request_preserves_reason`
   ✗ `:136 order_total_matches_lines` ✗ `:144 ecommerce_channel_order_is_idempotent_and_guarded` ✓
⭐ **`eval/harness.py`（108 行）**：`EVALS = [` @ `:24` ✗ `def run_suite(...)` @ `:47`
   ✗ `def main()` @ `:89` ✓
⭐ **`payable_aging_tracks_open_supplier_exposure`** 在 `eval/harness.py` ✗ `eval/cases.py` ✓
```

## 三、⚠️⚠️ 一个必须改设计的事实

```
⚠️ **`grep -c '_csv(self\|REPORT_COLUMNS' flowerp/reports.py` ⇒ **0**** ✓
   ⇒ ⭐ **L15-B 的四个出口**不在**这个仓库里** ✓
     ⇒ ⭐ **因为 `TASK-E978708191`（L15-B）也停在 `review` ✗ 没合入** ✓
       ⇒ ⭐⭐⭐ **所以我原 Spec 里写的"列规格进 `REPORT_COLUMNS`"**做不到**** ✓
         ⇒ ✅ **要改设计**：**`ar_aging_csv` **自己声明列规格**✗ 不依赖未合入的改动** ✓
           ⇒ ⭐ **而这也**更符合边界****：
             **本次交付不能依赖另一个**未被接受的**候选的状态** ✓
             ⇒ ⭐⭐ **这正是辅导资料那句**：「**不能把当前客户仓库的失败拼到另一份候选上**」
               —— **反向同理：也不能把另一个候选的**存在**当成前提** ✓
```

## 四、⭐ 所以本次交付的设计（**修正后** ✓）

```
⭐ **独立 FlowERP（`/home/rchua/GO/flowERP-customer`）**：
   · **`flowerp/reports.py`**：**加 `ar_aging_csv(self, principal, as_of=None) -> str`**
     ⇒ ⭐ **它自己声明明细的列规格**（**模块级常量 `AR_AGING_COLUMNS` ✗ 或方法内常量** ✓）
   · **`eval/cases.py`**：**加 `ar_aging_export_keeps_columns() -> str`**（**照既有风格** ✓）
   · **`eval/harness.py`**：**把它注册进 `EVALS`** ✓
⭐ **控制仓库（`/home/rchua/GO/CodexFDE`）**：
   · **`eval/cases.py`**：**加委托包装**（**照 `payable_aging_tracks_open_supplier_exposure`
     的写法**：`from workbench.external_project import evaluate_case;
      return evaluate_case('ar_aging_export_keeps_columns')` ✓）
   · **`eval/harness.py`**：**注册它** ✓
```

## 五、⭐ 待办

```
[ ] ⭐ **先跑一遍独立 FlowERP 的完整套件**（**记起点基线** ✓）
[ ] ⭐ **写 `ar_aging_export_keeps_columns`** ⇒ **跑它 ⇒ 应红**（**`ar_aging_csv` 不存在** ✓）
[ ] ⭐ **实现 `ar_aging_csv`** ⇒ **再跑 ⇒ 应绿** ✓
[ ] ⭐ **控制仓库加委托包装** ⇒ **跑完整套件** ✓
[ ] ⭐ **交付「完成思路 + 代码链接」** ✓
[ ] 🚩 **待本人**：**列规格取舍** ✗ **具名审核** ✗ **原使用者复验** ✓
```
