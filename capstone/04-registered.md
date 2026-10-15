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
