# 结营毕设 · 🎉 **从首页登记成功**（**补上 L16 那条缺口** ✓）

- **日期**：2026-10-16｜**入口**：**工作台首页 `http://127.0.0.1:8001/`** ✓
- ⭐ **生成的 Task**：**`TASK-892BF97942`** ✗ `accepted: true` ✗ `execution_mode: "verify"`
- **证据**：`/tmp/cap-verif.json` ✗ `/tmp/cap-post4.json`

## 一、⭐⭐⭐⭐⭐ 首页那三步（**我一步步试出来的 ✗ 每步都有明确的报错指路** ✓）

```
① ⭐ **先直接 POST** ⇒ **HTTP 400**：`{"error":"invalid_body","message":"请求体为空或过大"}` ✓
   ⇒ ⭐ **根因**：**`workbench_server.py:599` 的请求体上限**：
     `maximum = … else **8192**` ⇒ ⭐ **`/api/v1/delivery/requests` 落到最后一个 `else`** ✓
     ⚠️ **而网页表单写的是 `maxlength="40000"`** ⇒ ⭐ **两者不一致 ✗ 记下这个现值缺口** ✓
② ⭐ **把 Spec 压到 6835 字节再 POST** ⇒ **HTTP 400**：
   `{"error":"ValueError","message":"**现场需求不能超过 1000 个字符**"}` ✓
   ⇒ ⭐⭐⭐⭐⭐ **这句是关键**：**首页的 `request` 字段放的是**现场需求描述**（≤1000 字符）✗
     **不是整份 Spec** ✓
     ⇒ ⭐ **而 Spec 是**工作台自己生成的**** ⇒ **正是合同那条**：
       「**`delivery_evidence_and_review_controls` ⇒ **需求自动生成任务级 Spec 并推进至审核****」✓
③ ⭐ **改成 486 字符的需求描述再 POST** ⇒ **HTTP 409**：
   `{"error":"**course_verification_not_ready**",
     "message":"**检查对象或范围已变化。请重新核对条件后再提交。**"}` ✓
   ⇒ ⭐ **响应里带着 `verification`** ✗ 其中 `issues[0].action` 直接指路：
     「**点击"重新核对条件"✗ 确认最新源码目录和检查项。**」✓
   ⇒ ⭐⭐ **而 `app.js` 里有那条端点**：`api('/api/course/verification?lesson=' + …)` ✓
④ ⭐ **两步走**：
   · ⭐ `GET /api/course/verification?lesson=16` ⇒ **退出码 0** ✗
     `ready = **true**` ✗ `verification_key = **f9e0ac871b93…73a39**` ✓
   · ⭐ `POST /api/v1/delivery/requests` **带上那个 key** ⇒ ✅ **成功** ✓
```

## 二、⭐⭐⭐⭐⭐ 登记的结果

```json
{
  "task_id": "TASK-892BF97942",
  "accepted": true,
  "execution_mode": "verify",
  "status_url": "/api/v1/tasks/TASK-892BF97942",
  "view_url": "/api/v1/delivery/views/TASK-892BF97942"
}
```
⇒ ⭐ **它生成了一个**课程任务**** ✗ **而 `execution_mode` 是 `verify`** ✓
   ⇒ ⭐⭐ **依据**：**`workbench_server.py:758~759`**：
     `if body.get("execution_mode", "verify") != "verify":
        raise ValueError("**网页API只允许 verify；代码执行须使用明确授权的课程 CLI**")` ✓
     ⇒ ⭐⭐⭐ **所以**首页登记**与**代码执行**是两步 ✗ 要分别说明** ✓
       ⇒ **正是 `AGENTS.md` 那句**「**后端能力与首页已贯通的交互应**分别说明****」✓

## 三、⭐⭐ 核对条件里的读数（**原文** ✓）

```
`lesson`      = 16 ｜ `title` = "在新环境接手 ✗ 并完成现场新需求"
`ready`       = **true**
`target`      = {`workbench_root`: "/home/rchua/GO/CodexFDE",
                 `project_id`: **null** ✗ `product_root`: **null** ✗ `root_path`: **null**}
`projects`    = **[]**（**空**）
`checks`      = [{`name`: "**delivery_evidence_and_review_controls**",
                  `label`: "**任务 ✗ 报告与具名人审可追溯**", `target`: "**工作台**"}]
⇒ ⭐ **`projects` 是空的 ✗ 而 `ready` 仍是 `true`** ✓
  ⇒ ⭐⭐ **因为本讲的固定检查 target 是**「工作台」**✗ 不涉及 ERP 项目** ✓
    ⇒ ⭐ **`app.js:803` 那句印证了**：
      `automatic.textContent = !checksProduct ? '**本讲固定检查不涉及 ERP 项目**' : …` ✓
```

## 四、⭐⭐⭐ 所以"首页链路"这条现在**真的补上了**

```
⚠️ **L16 发布证据索引里原本写**：
   「🚩 **首页那条链路未核对**（**我只用了命令行**）」✓
⇒ ⭐⭐⭐⭐⭐ **现在**：
   · **首页在跑**（**已核实 ✗ PID 512271** ✓）
   · ⭐ **"事项与决策"就是入口**（**导航里有它** ✓）
   · ⭐⭐ **而且我真的从那里登记了一个需求 ✗ 拿到了 `TASK-892BF97942`** ✓
⇒ ✅ **所以正确表述**：
   **首页可用（已核实）** ✗ **首页能登记需求并生成任务（已实测）** ✗
   **而 L16 那次交付**仍是命令行做的**（**那条记录不改写** ✓）
```

## 五、⚠️ 我顺手发现的两个现值不一致（**记下 ✗ 不改 ✗ 不在写集** ✓）

```
⚠️ **① 网页表单 `maxlength="40000"` vs 服务端请求体上限 8192**
   ⇒ **网页允许贴得比 API 收得下的多**
⚠️ **② 首页的 `request` 字段限长 1000 字符 ✗ 而表单没写这个限制**
   ⇒ **用户要提交两次才知道真正约束是什么**
⇒ ⭐ **两条都是真的 ✗ 都有实测证据**（**400 的两种 message** ✓）
  ⇒ ⚠️ **但它们**不在本次写集**（**`flowerp/reports.py` ✗ `eval/`** ✓）
    ⇒ ⭐ **按纪律：不顺手修 ✗ 记在这里给下一位接手者** ✓
```

## 六、⭐ 待办

```
[ ] ⭐ **看 `TASK-892BF97942` 生成了什么**（`GET /api/v1/tasks/TASK-892BF97942` ✓）
    ⇒ **它有没有自动生成任务级 Spec**（**合同那条要求** ✓）
[ ] ⭐ **写独立 FlowERP 的业务检查**（`ar_aging_export_keeps_columns` ✓）
[ ] ⭐ **跑它 ⇒ 应先红**（**`ar_aging_csv` 不存在** ✓）
[ ] ⭐ **实现 `ar_aging_csv`** ✗ **再跑 ⇒ 应绿** ✓
[ ] ⭐ **控制仓库 `eval/cases.py` 加委托包装** ✓
[ ] ⭐ **交付「完成思路 + 代码链接」** ✓
[ ] 🚩 **待本人**：**列规格取舍** ✗ **具名审核** ✗ **原使用者复验** ✓
```

---

# 🔍 澄清：生成的 Spec 是**讲次合同的机器投影**（**不是我的原话** ✓）

- **日期**：2026-10-16｜**证据**：`/tmp/cap-task.json` ✗
  `…/.runtime/workbench/course/L16/9b2e8dbcfcb04c53bdab76785b40c912/FDE_SPEC.md` ✓

## 一、⭐⭐⭐⭐⭐ 它生成了什么（**2563 字节 ✗ 49 行** ✓）

```
`# REQ-COURSE-L16｜L16 在新环境接手 ✗ 并完成现场新需求`

`## 来源`
   · 课程主线合同：L16 ｜ 前置课次：L15
   · 业务对象：`REQUIREMENT:LIVE-DRAW` ｜ 起始基线：`course/l16-start`

`## 目标`
   · **合同那句**：「**现场抽取一个此前未实现的 FlowERP 小需求 ✗ 使用工作台完成**
     **Spec ✗ 受控执行 ✗ Eval ✗ 人审和发布证据**」
   · **工作台增量**：冷启动 ✗ 发布证据索引与迁移答辩
   · **ERP 产品增量**：现场交付此前未实现的小需求
   · **课程建设主线 / 本讲阶段 / Codex 当讲角色 / FDE 循环 / 因果交接**（**全是合同字段**）

`## 非目标`
   · 不提前实现后续课次的 ERP 产品增量
   · 不修改本讲允许写集之外的文件
   · 不删除失败证据 ✗ 降低 Eval 等级或绕过具名人工审核

`## 约束`
   · 允许写集：`flowerp/` ✗ `workbench/` ✗ `eval/` ✗ `web/` ✗ `tests/`
   · ⭐ **项目与路径归属**：「**CodexFDE 是控制仓库 ✗ FlowERP 是独立客户项目。…
     **`flowerp/` ✗ `web/` 的业务源码归属独立 FlowERP；`workbench/` ✗ `agent/` 归属工作台。
     `eval/` ✗ `tests/` 须按具体文件和来源记录区分工程检查与客户业务检查。**」✓
   · 本讲复用 Eval：`delivery_evidence_and_review_controls`

`## 验收用例`（**合同的三条** ✓）
   1. 需求在答辩现场抽取且仓库基线中尚未实现
   2. 正常 ✗ 失败和失败后不变状态均有新证据
   3. 发布索引能追溯需求 ✗ Diff ✗ Eval ✗ 人审与剩余风险

`## 完成定义`（**合同的四条** ✓）
   · ERP 产品增量与工作台增量均有可复现证据 ✗ 且能够说明二者因果
   · 正常路径 ✗ 失败路径和失败后不变状态均已验证
   · 学生保存首次判断 ✗ 失败 ✗ 修订和复验结果；参考仓库终态不计作学生成果
   · 若 `course-status --require-baselines` 未通过 ✗ 不得声称完成了渐进式课程复现
```

## 二、⭐⭐⭐⭐⭐ 所以"需求自动生成任务级 Spec"在本讲的实现里是什么

```
⚠️ **它生成的是**讲次合同的参数化投影**✗ **不是把我那 486 字变成六段** ✓
   · **`spec`** = **合同的机器投影**（**每讲一份模板 ✗ L16 的就是上面这份**）
   · ⭐ **`request`** = **我提交的现场需求原文**（**在 `Task.request` 键里 ✗ 9291 字节的 JSON** ✓）
⇒ ⭐ **所以那条 Eval 的 label 说得很准**：
   「**`delivery_evidence_and_review_controls` ⇒ **任务 ✗ 报告与具名人审可追溯****」✓
   ⇒ ⭐⭐ **而真正的六段 Spec 是**我自己写的**（`capstone/03-spec.md` ✗ 167 行** ✓）
     ⇒ ⭐⭐⭐ **而那条新 Eval（`ar_aging_export_keeps_columns`）**不在合同里**⇒
       **所以要**另走课程 CLI**✗ 不能只靠首页的 verify** ✓
       ⇒ ✅ **正是 `workbench_server.py:759` 那句**：
         「**网页API只允许 verify；代码执行须使用明确使用的课程 CLI**」✓
```

## 三、⭐⭐ 顺带核实的四件事

```
① ⭐ **`spec_path` 是**显示截断****：Task 里是 `…9b2e8dbcfcb04c53bdab76785b`✗
   真实目录是 `…9b2e8dbcfcb04c53bdab76785b**40c912**`（**多 6 字符** ✓）
② ⭐ **8001 的 `--runtime-dir` = `/home/rchua/GO/CodexFDE/.runtime/**workbench**`**（**不是
   `.runtime/l04-learning`** ✓）⇒ ⭐ **两个 runtime 分开 ✗ 各自一个 `workbench.db`** ✓
   ⇒ **正是 `AGENTS.md`**：「**两套数据目录不得混用**」✓
③ ⚠️ **`spec_sha256 = **None**`** ⇒ **它在这个 Task 上也是空的** ✗
   与 L16 那个 `TASK-FE48B898DB` **一样** ⇒ ⭐ **所以这是个**普遍现象**✗ 不是偶发** ✓
   ⇒ 🚩 **原因仍未调查** ⇒ **列入待办** ✓
④ ⚠️ **`spec_text` 长度 = 0** ⇒ **Spec 在文件里 ✗ 不在字段里** ✓
```

## 四、⭐ 待办

```
[ ] ⭐ **写独立 FlowERP 的业务检查**（`ar_aging_export_keeps_columns` ✗ **应先红** ✓）
[ ] ⭐ **实现 `ar_aging_csv`** ⇒ **应绿**
[ ] ⭐ **控制仓库 `eval/cases.py` 加 `evaluate_case(...)` 委托包装** ✓
[ ] ⭐ **交付「完成思路 + 代码链接」** ✓
[ ] ⚠️ **`spec_sha256` 为空的原因**（**两个 Task 都空 ⇒ 普遍现象**）
[ ] 🚩 **待本人**：**列规格取舍** ✗ **具名审核** ✗ **原使用者复验** ✓
```
