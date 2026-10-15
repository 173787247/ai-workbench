# 结营毕设 · ⭐⭐⭐⭐ 控制仓库侧的**委托包装**（**跨进程边界 ✗ 19 ⇒ 20 ✗ 无回归** ✓）

- **日期**：2026-10-16｜**仓库**：`/home/rchua/GO/CodexFDE`（**控制仓库** ✓）
- **证据**：`capstone/run-control/{before-pc,after-pc,batch}.{json,log}`

## 一、⭐⭐⭐ 改了哪三处

```
⭐ **`eval/cases.py`**：**加包装函数**（**照既有 `payable_aging_tracks_open_supplier_exposure` 的写法** ✓）
   ```python
   def ar_aging_export_keeps_columns():
       from workbench.external_project import evaluate_case
       return evaluate_case('ar_aging_export_keeps_columns')
   ```
⭐ **`eval/harness.py:13`**：**`PROJECT_CASES` 里加 `'ar_aging_export_keeps_columns'`** ✓
⭐ **`eval/harness.py`**：**`EVALS` 里加一行**：
   `("ar_aging_export_keeps_columns", "blocking", cases.ar_aging_export_keeps_columns),` ✓
```

## 二、⭐⭐⭐⭐⭐ 委托真的跨了进程边界（**那行 detail 就是原始证据** ✓）

```
⭐ `[PASS] ar_aging_export_keeps_columns 106 ms`
   detail：
   「**FlowERP：`/home/rchua/GO/flowERP-customer`；
     **`ar_aging_export_keeps_columns`**；
     **退出码 0**；
     应收账龄导出走明细七列 ✗ 空结果留列名 ✗ 不混汇总 ✗ 只读 ✗ 且权限拒绝不伪装成空文件**」
⇒ ⭐⭐⭐⭐⭐ **它写明了**四件事**：
   **哪个 FlowERP 根** ✗ **哪个用例** ✗ ⭐ **那个子进程的退出码** ✗ **子进程返回的结论** ✓
   ⇒ ⭐ **依据**：**`workbench/external_project.py:87~95`** 的子脚本：
     `assert Path(flowerp.__file__).resolve().is_relative_to(root),
      '**ERP import escaped candidate**'`
     ✗ `print(json.dumps({'evidence': getattr(module, sys.argv[2])()}, ensure_ascii=False))` ✓
     ⇒ ⭐⭐ **所以它是**真的另起一个进程**跑独立 FlowERP 的检查 ✗
       **并把它的 `evidence` 回传** ✓
```

## 三、⚠️⚠️ 一个**必须先读懂**的机制（**否则会得出错误的"没生效"** ✓）

```
⚠️ **`eval/harness.py:73`**：
   `if not case_names:`
   `    selected = [item for item in selected if item[0] **not in PROJECT_CASES**]` ✓
⇒ ⭐⭐⭐⭐⭐ **所以 `PROJECT_CASES` 里的检查**默认不进整批**** ✓
   ⇒ ⭐ **它们只有**显式 `--case <name>` 才会跑**** ✓
     ⇒ ⭐⭐ **原因**：**它们是**委托给独立 FlowERP** 的 ✗ 没有项目时跑不了** ✓
```

### ⚠️ 而我**第一版对照就这样被骗了一次**

```
⚠️ **我先跑了 `--suite all` 的 before / after** ⇒ **两边都是** `{total: 14, passed: 14}`** ✓
   ⇒ ⭐ **新增：`[]`** ⇒ **看起来"我的改动没生效"** ✓
     ⇒ ⭐⭐ **而真相是**：**整批**设计上**不跑项目类 ✗ 所以我的新检查压根不在那 14 条里** ✓
       ⇒ ⭐⭐⭐ **修法**：**显式把那 20 条项目类列出来跑** ✓
         ⇒ ✅ **这才是正确的对照** ✓
           ⇒ ⭐ **教训**：**"总数没变" 不等于 "没生效" ✗ 要先读懂过滤规则** ✓
```

## 四、⭐⭐⭐⭐⭐ 数清三类与正确对照

```
⭐ **数清**：`EVALS 总数 = **34**` ✗ `PROJECT_CASES = **20**` ✗
   `非项目类（整批跑）= **14**` ✗ `EVALS 里的项目类 = **20**` ✓
   ⇒ ⭐ **14 + 20 = 34** ✓
```

| 对照 | before | after | 结论 |
|---|---|---|---|
| ⭐ **整批（非项目类 14 条）** | `{total:14, passed:14, decision:'pass'}` | **同** | ⭐ **设计上**不含项目类 ✗ 所以两边一样是**正确的**** ✓ |
| ⭐⭐ **项目类（显式 19 条 ⇒ 20 条）** | `{total: **19**, passed: **19**, decision:'pass'}`<br>**`grep -c ar_aging_export_keeps_columns` ⇒ **0**** | `{total: **20**, passed: **20**, decision:'pass'}` | ⭐ **新增 `['ar_aging_export_keeps_columns']`** ✗ **减少（无）** ✗ **从绿变红（无）** ✓ |

⇒ ⭐ **我是用 `git stash` 拿的真 before**（**不是凭印象** ✓）：
   `git stash push -m … -- eval/cases.py eval/harness.py` ⇒ **跑** ⇒ `git stash pop` ✓
   ⇒ ⭐⭐ **而 `grep -c` 在 before 的日志里是 **0**** ⇒ **证明那条检查当时确实不在** ✓
     ⇒ ✅ **这比"我记得原来是多少"强** ✓

## 五、⚠️ 一处**要说清**的**红 ⇒ 绿发生在哪一侧**

```
⚠️ **控制仓库侧**没有**出现红 ⇒ 绿** ✓
   ⇒ ⭐ **因为**红 ⇒ 绿发生在**独立 FlowERP**那侧**（**见 `capstone/06-implemented.md`** ✓）
     · **FlowERP 侧**：**起点 19/19 ⇒ 加检查 1 红 ⇒ 实现后 20/20** ✓
     · ⭐ **控制仓库侧**：**委托包装**只证明**边界是通的** ✗ **且没有回归** ✓
   ⇒ ⭐⭐ **所以正确表述**：
     **验证是两段**：**产品侧的红 ⇒ 绿** ✗ **控制侧的委托可用与无回归** ✓
     ⇒ ⭐ **不能把控制侧的 20/20 说成"产品侧也被验了两次"** ✓
```

## 六、⭐ 待办

```
[ ] ⭐ **交付「完成思路 + 代码链接」**（**毕设的要求 ✗ 也是最后一项** ✓）
[ ] ⚠️ **`spec_sha256` 为空的原因**（**三个 Task 都空**）
[ ] ⚠️ **`ar_aging` 是否要在 API 层暴露**（**本次只做了 `ReportService` 出口 ✗ 属另一需求** ✓）
[ ] 🚩 **待本人**：**列规格取舍** ✗ **具名审核** ✗ **原使用者复验** ✓
```
