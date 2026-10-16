# 结营毕设 · 完成思路 + 代码链接

> 🚩 **本文件是毕设的交付物** ✓
> ⭐ **完成思路按 L16 的**四件亲手工作**组织** ✗ **每步写**实际结果**✗ 缺项如实标** ✓
> ⚠️ **使用说明在代码仓库的 README 里**：
> · `flowERP-customer/README.md` 的 `## 应收账龄导出`（**功能 ✗ 用法 ✗ 边界 ✗ 怎么检查**）
> · `CodexFDE/README.md` 的 `### ERP 业务检查是委托执行的`（**怎么跑业务检查 ✗ 一个易错的过滤规则**）

**日期**：2026-10-16｜**执行者**：🚩 **待本人署名**（**会话里的 actor 是 `course-learner` ✗ 占位**）

---

## 一、四件亲手工作的实际结果

### ⭐① 把已有交付交给别人 —— **⚠️ 这一件我基本没做**

| 应产出 | 我的实际状态 |
|---|---|
| **写好的接手说明** | ⚠️ **没有单独成文** ⇒ **要素散在 `lesson-{14,15,16}-submission/` 与 `START-HERE.md`** |
| **同伴首次操作与修订记录** | 🚩 **没有同伴** ⇒ **0 条** |

```
⚠️ **为什么没做**：**这一件要求一个**接手者**✗ 而我是单人会话 ✗ 没有同伴** ✓
   ⇒ ⭐ **我没有编造"同伴记录了 X"** ✗ **如实标未做** ✓
⭐ **而我确实查清了一份接手者会卡住的材料**：
   **同一个 `flowerp/` 名字下有**两套不同的组织方式**** ✓
   · **`course/l16-start` 系候选**：**没有 `api.py`/`server.py`/`__main__.py`** ⇒ **HTTP 层在
     `workbench/api_v2.py`** ⇒ **业务 ✗ HTTP ✗ 页面分属三个目录** ✓
   · **独立 FlowERP**：**`flowerp/api.py` 存在** ⇒ **HTTP 放在业务包里** ✓
   ⇒ ⭐⭐ **两者长得像 ✗ 但层次划分不同 ⇒ 拿错一份 ✗ "需求尚未实现"这个判断就站不住** ✓
     ⇒ **证据**：`lesson-16-submission/02-material.md`（**两种候选各缺一半的对照表**）✓
   ⇒ ✅ **这就是"接手说明该写的第一句"✗ 只是我写成了调查记录 ✗ 没写成交接文档** ✓
```

### ⭐② 把新请求变成可判断的要求 —— ✅ **这一件做完整了**

| 应产出 | 我的实际结果 |
|---|---|
| ⭐ **本人确认的 Spec** | ✅ **`capstone/03-spec.md`（167 行 ✗ 六段 ✗ 围栏自检通过）** ✗ **`workbench.cli spec` 退出码 0** ⇒ 🚩 **"本人确认"待本人** |
| ⭐ **新增检查** | ✅ **`ar_aging_export_keeps_columns`**（**阻断级 ✗ 确认不在合同 `eval_cases` 里**）|
| ⭐ **真实起始失败** | ✅ **退出码 1** ✗ `AttributeError: 'ReportService' object has no attribute 'ar_aging_csv'` ⇒ ⭐ **红的原因是**目标能力缺失**✗ 不是缺依赖 ✗ 不是环境错** ✓ |

```
⭐ **需求是怎么来的**：**不是为毕设另找的** ⇒ **我在 L15-B 的记录里就写下了这个缺口** ✓
   **（`ar_aging` 返回 `dict` ✗ 结构不同 ⇒ 没有 CSV 出口）** ✓
⭐ **先在**将要实施的那份基线**上核实缺口**（**辅导资料 §3 的纪律** ✓）：
   `ar_aging` 在整个 `reports.py` 里只出现 **1** 次（**就是它自己**）✗
   而同类的四个报表都有 `_csv` 出口 ⇒ ⭐ **它是**唯一没有出口的**** ✓
⭐ **检查先行**：**只加检查 ⇒ 跑 ⇒ 必红 ⇒ 再实现 ⇒ 再跑 ⇒ 应绿** ✓
   ✗ ⭐ **起始失败的原因经得起手册那句**「**未知用例 ✗ 环境错误不算产品缺口**」✓
⚠️ **一处撞出来的约束**（**如实记**）：**首页的"现场需求"字段上限 1000 字符** ✗
   **请求体上限 8192 字节** ⇒ ⭐ **而网页表单写的是 `maxlength="40000"`** ⇒ **两者不一致** ✓
```

### ⭐③ 组织 Codex 实现并纠偏 —— ✅ **这一件做完整了 ✗ 而且纠偏是真的**

| 应产出 | 我的实际结果 |
|---|---|
| ⭐ **工作台正式任务** | ✅ **`TASK-892BF97942`**（**从首页「事项与决策」登记 ✗ `accepted: true` ✗ `execution_mode: verify`**）|
| ⭐ **源码 Diff** | ✅ **产品侧 `96954fc`（3 文件 ✗ +80）** ✗ **控制侧 `1b07d16`（2 文件 ✗ +7 −1）** ✗ **`out_of_scope_files: []`** |
| ⭐ **失败原因与修订结果** | ⭐ **两次据实改设计**（**见下**）✗ **一次真实的红 ⇒ 绿** |

#### ⭐⭐ 两次据实改设计（**这是这一件里最值钱的部分**）

```
⚠️ **第一次**：**我以为可以复用 L15-B 的 `REPORT_COLUMNS`** ✓
   ⇒ ⭐ **实测**：`grep -c '_csv(self\|REPORT_COLUMNS' flowerp/reports.py` ⇒ **0** ✓
     ⇒ ⭐⭐ **因为 L15-B 的 `TASK-E978708191` 也停在 `review` ✗ 没合入产品仓库** ✓
       ⇒ ✅ **改设计**：**`ar_aging_csv` **自己声明 `AR_AGING_COLUMNS`**** ✗
         **不依赖另一个未被接受的候选的状态** ✓
         ⇒ ⭐ **依据（反向同理）**：**辅导资料**「**不能把当前客户仓库的失败拼到
           另一份候选上**」⇒ **也不能把另一份候选的**存在**当成前提** ✓
⚠️ **第二次**：**我以为可以直接调 `self.to_csv(rows, fieldnames=…)`** ✓
   ⇒ ⭐ **实测**：**那个仓库的 `to_csv` 还是旧版**：
     `def to_csv(rows: list[dict]) -> str:` ✗ `if not rows: return ""`
     ⇒ ⭐⭐ **它**没有** `fieldnames` 参数 ✗ 也**没有**"无规格就拒绝"**（**停在 L15-A 之前** ✓）
       ⇒ ✅ **改设计**：**`ar_aging_csv` **自己用 `csv.DictWriter` 显式给 `fieldnames`**** ✗
         **这样它不依赖 `to_csv` 的任何版本** ✓
```

#### ⭐ 红 ⇒ 绿（**五份报告串起来 ✗ 都在 `capstone/`** ✓）

| 阶段 | 命令 | **退出码** | **读数** |
|---|---|---|---|
| **起点基线** | `--suite all` | ✅ **0** | `{total:19, passed:19, decision:'pass'}` |
| **加检查后（未实现）** | `--case ar_aging_export_keeps_columns` | ⚠️ **1** | `{total:1, passed:0, blocking_failed:1, decision:'block'}` |
| **加检查后的整批** | `--suite blocking` | ⚠️ **1** | `{total:20, passed:19, blocking_failed:1}` |
| **实现之后** | `--case ar_aging_export_keeps_columns` | ✅ **0** | `{total:1, passed:1, decision:'pass'}` |
| **完整套件** | `--suite all` | ✅ **0** | `{total:20, passed:20, decision:'pass'}` |

⇒ ⭐ **与起点**逐条对账**（**不是只看总数**）**：
   **新增 `['ar_aging_export_keeps_columns']`** ✗ **减少（空）** ✗ **从绿变红的（无）** ✓

### ⭐④ 将可接受的结果交出去 —— ⚠️ **技术部分做了 ✗ 人的部分没有**

| 应产出 | 我的实际结果 |
|---|---|
| ⭐ **同候选复验** | ✅ **`--suite blocking` 21/21（退出码 0）** ✗ **真 HTTP 三层**（**正常「椅」2 行 ✗「USB」1 行；空结果 `ZZZNOMATCH` 0 行；只读前后一致**）✗ **恢复实验退出码 0**（**正常 ✗ 失败 ✗ 失败后不变状态**）✗ **独立演示七步闭合** |
| 🚩 **具名决定** | 🚩 **没有** ⇒ **`TASK-FE48B898DB` 与 `TASK-892BF97942` 的 `reviewed_by` 都是 `None`** ✗ **候选导出被 `course_release.py:191` 正确拦住** |
| ⭐ **导出** | ✅ **`task-show` 导出 55043 字节 / 26 个键** ✗ **本文件 + 证据索引**（**`lesson-16-submission/10-release-index.md`：七条链判为"已证明 6 ✗ 证据不足 6 ✗ 与证据矛盾 2"**）|
| 🚩 **反馈和答辩稿** | ⚠️ **答辩稿有**（**`L16-结业记录.md` §7 五分钟五段 ✗ 每段有证据链接**）✗ 🚩 **实际答辩未发生** ✗ **原使用者复验没有**（**`feedback` 读数 0 ✗ 而同目录回查也只证明"可追溯"**）|

```
⚠️ **一处我特意没有混淆的**：**上面的复验是**我自己**跑的** ✓
   ⇒ ⭐ **而四件工作里写的"**同伴亲自查询****"⇒ **那一步是**同伴**做的 ✗ 我没有同伴** ✓
     ⇒ ⭐⭐ **所以这一件的技术层完成 ✗ 人的层未完成** ✗ **如实分开** ✓
```

---

## 二、代码链接

### ⚠️ 先说一件要你定的事

```
⚠️ **两个仓库都有 GitHub 远端**：
   · **FlowERP**：`origin https://github.com/**congde/flowERP.git**`
   · **控制仓库**：`origin https://github.com/**congde/CodexFDE.git**`
⇒ ⭐ **我只做了**本地提交 ✗ **没有推送** ✓
  ⇒ ⭐⭐ **因为推送是**对外可见的改动**** ⇒ 🚩 **要你明确说推哪个仓库哪个提交** ✓
    ⇒ ⚠️ **而按规则我不把一次授权推断成"推广到类似的东西"** ✓
```

### 链接一：完整代码（**本地 ✗ 现在就能用** ✓）

| 仓库 | 提交 | 内容 |
|---|---|---|
| ⭐ **独立 FlowERP** | **`96954fca83043838c6b2a1bb441d55b7ac320b68`** | **`feat(flowerp): 应收账龄可导出明细`** ✗ **3 文件 ✗ +80 行** ✗ **含 README 使用说明** |
| ⭐ **控制仓库** | **`1b07d16e576e6a0badaca733ec841fc4443a1e17`** | **`eval: 委托应收账龄导出检查到独立 FlowERP`** ✗ **2 文件 ✗ +7 −1** ✗ **含 README 委托说明** |

```bash
# 产品侧：新增的出口、列规格与检查
cd /home/rchua/GO/flowERP-customer
git show 96954fc --stat
git diff HEAD~1 HEAD -- flowerp/reports.py eval/

# 控制侧：委托包装与注册
cd /home/rchua/GO/CodexFDE
git show 1b07d16
git diff HEAD~1 HEAD -- eval/
```

**两个仓库都在**本地 ✗ 路径如上**✗ 两个提交都是**完整可检出**的** ✓
⇒ 🚩 **GitHub 链接在推送后才是上面那两个 URL + `/commit/<sha>`✗ 现在打开是旧内容** ✓

### 链接二：使用说明（**在代码仓库的 README 里 ✗ 按你的要求** ✓）

| 位置 | 内容 |
|---|---|
| ⭐ **`flowERP-customer/README.md` → `## 应收账龄导出`** | **它是干什么的 ✗ 怎么调（两行 Python ✗ 实测可跑）✗ 守住的四件事（只导明细 ✗ 空结果仍可用 ✗ 只读 ✗ 权限不伪装）✗ 怎么检查** |
| ⭐ **`CodexFDE/README.md` → `### ERP 业务检查是委托执行的`** | **业务检查为什么要点名 ✗ 三条命令 ✗ 一个易错点（`PROJECT_CASES` 不进批次所以总数不变）✗ 写一条业务检查要动哪两处** |

### 能运行 ✗ 能检查 ✗ 能继续使用（**三条都验过** ✓）

```
✅ **能运行**：**Python 运行时零第三方依赖**（**两个 `pyproject.toml` 的 `dependencies = []`** ✓）
   ✗ **README 里那段 Python 用法**照抄**跑通** ⇒ 输出
     `'invoice_number,partner_code,partner_name,due_date,outstanding_cents,overdue_days,bucket\r\n'` ✓
   ✗ **服务能起**：`workbench.cli serve --port 18160` ⇒ **健康检查 `ready`** ✗
     **schema version 17** ✗ **`foreign_key_errors []`** ✓
   ✗ **工作台首页在跑**：`http://127.0.0.1:8001/` ⇒ **HTTP 200** ✗ **PID 512271** ✓
✅ **能检查**：**README 里那条命令**照抄**跑通** ⇒ **`[PASS] ar_aging_export_keeps_columns 55 ms`**
   ✗ **退出码 0** ✓ ✗ **完整套件 20/20** ✓
✅ **能继续使用**：**检查分两层 ✗ 产品侧写断言 ✗ 控制侧加委托包装** ✗ **README 写清了要动哪两处** ✓
   ✗ ⭐ **而"工作台首页 → 事项与决策 → 交付"那条链路**我实测走通过**（**`TASK-892BF97942`**）✓

⭐ **以上三条在一个**全新克隆**里逐条走过一遍**（**不是"在我这台机器上能跑"** ✓）：

```
$ git clone <flowERP> /tmp/cap-fresh-XXXX/flowERP
✓ 克隆里没有 .venv、没有 .runtime（源码自带，运行材料不入库）
$ python3 -m venv .venv && ./.venv/bin/python -m pip install -e .
✓ 退出码 0；flowerp 导入自 /tmp/cap-fresh-XXXX/flowERP/flowerp/__init__.py
   ⇒ dependencies = [] ⇒ 零第三方运行时依赖确实成立

$ ./.venv/bin/python -X utf8 -m eval.harness --suite blocking --case ar_aging_export_keeps_columns
✓ [PASS] … 52 ms ⇒ 退出码 0

$ ./.venv/bin/python -c "… ReportService(store).ar_aging_csv(SYSTEM_PRINCIPAL)"
✓ 'invoice_number,partner_code,partner_name,due_date,outstanding_cents,overdue_days,bucket\r\n'

$ ./.venv/bin/python -X utf8 -m flowerp serve --help
✓ usage: __main__.py … {serve} ／ FlowERP 客户系统
```
```

---

## 三、证据索引（**可逐条打开** ✓）

| 证据 | 位置 |
|---|---|
| ⭐ **产品侧起点 ✗ 红 ✗ 绿 ✗ 完整套件** | `capstone/run-before/all.json` ✗ `capstone/run-after/{new,fixed,all}.json` |
| ⭐ **控制侧委托的 before / after** | `capstone/run-control/{before-pc,after-pc}.json` ✗ `new.log`（**detail 里有客户仓库路径与子进程退出码**）|
| ⭐ **首页登记** | `capstone/04-registered.md` |
| ⭐ **四件工作与缺口** | `capstone/{01-requirements,02-project,05-baseline-facts,06-implemented,07-delegation}.md` |
| ⭐ **L16 的发布证据索引** | `lesson-16-submission/10-release-index.md` |
| ⭐ **L16 结业记录（七步 ✗ 含答辩表）** | `…/.runtime/l04-learning/l16-evidence/L16-结业记录.md` |
| ⭐ **两个仓库的 diff** | `capstone/links/{flowERP-customer,CodexFDE}.diff` |

---

## 四、⚠️ 未完成（**不粉饰** ✓）

```
🚩 **要你做的**：
   · 四件工作的**①**：**找一个接手者 ✗ 让他只按说明操作 ✗ 记下首次结果与修订** ✓
   · 四件工作的**④**：**具名决定 ✗ 原使用者（周宁）在修复后的版本上重做原操作 ✗ 实际答辩** ✓
   · **列规格取舍**：**七列留哪些 ✗ 汇总（`buckets`/`total_cents`）要不要单独出** ✓
   · **是否推送那两个提交**（**对外可见 ✗ 只有你能定** ✓）
⚠️ **我没做的**：
   · **`ar_aging` 没有在 HTTP API 层暴露**（**本次只做了 `ReportService` 的出口** ⇒ **HTTP 侧另立需求**）
   · **`buckets`/`total_cents` 没有导出通道**（**按非目标排除**）
   · **`spec_sha256` 为 `None`**（**三个 Task 都空 ⇒ 普遍现象 ✗ 原因未查**）
   · **16 条控制仓库的基线固有测试失败**（**与本毕设无关 ✗ 未修**）
   · ⚠️ **一处要如实记的不一致**：**产品仓库 `HEAD~1 = 70660dd`** 的 message 里有"空导出"⇒
     **那是 L15-A 的内容** ✗ **而 L15-A 的 Task 从未被具名接受** ⇒
     **改动进了产品仓库 ✗ 课程 Task 没走完审核** ✓
```

## 五、一句话

```
⭐ **用工作台首页（「事项与决策」⇒ `TASK-892BF97942`）组织了一次真实交付**：
   **从 L15-B 记录里长出的缺口** ⇒ **在将要实施的基线上核实** ⇒
   ⭐ **两次据实改设计**（**不依赖未合入的候选 ✗ 不用不存在的签名**）⇒
   **先加检查（红）⇒ 实现（绿）⇒ 两层验证（产品侧 19⇒20 ✗ 控制侧委托 19⇒20 ✗ 都无回归）** ✓
   ⇒ ⭐ **使用说明在两个仓库的 README 里** ✗ **代码是本地的两个提交** ✗
     🚩 **GitHub 链接待你确认推送**
```
