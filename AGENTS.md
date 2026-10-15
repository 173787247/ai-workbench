# 个人 AI 研发工作台 · 协作规则

> 本文件是**长期约定**（跨会话仍成立），不是本次请求的说明。
> 本次做什么写在请求里；按什么步骤调查写在 Skill 里；何时自动跑检查留给 Hook（L07）。
> 版本 `v1`，制定日期 2026-10-16。改前版本见 `lesson-02-submission/agents-before.md`。

## 目录与职责

| 路径 | 职责 |
|---|---|
| `workbench/` | 实现。`bootstrap.py` 是账本（任务、证据、完整性）；`cli.py` 只做参数解析与转发 |
| `tests/` | 行为检查。`test_l01_workbench_bootstrap.py` 是账本验收；`test_workbench_server.py` 是页面壳 |
| `workbench_web/` | 页面壳静态资源。**L02 不改** |
| `docs/courses/L0N/` | 各讲的需求说明书（Spec）与个人记录 |
| `lesson-0N-submission/` | 个人证据索引。**是原始输出与退出码，不是报告** |
| `.runtime/course/L01-workbench/` | 账本数据。**运行数据不进版本库** |
| `.runtime/workbench/` | 页面壳的运行目录（**与上面那个分开**）|

**当前事实**：
- **解释器**一律用 `/home/rchua/GO/CodexFDE/.venv/bin/python`（3.11.16）。
  系统 `python3`（3.12.3）**不要**用来跑测试。
- **FlowERP 业务代码在独立仓库**，本仓不含 `flowerp/`。
- 课程材料在控制仓库（**只读**）。
- 本仓**是 Git 仓库**，起点提交 `be6024e`。

## 状态与历史（不得改变的边界）

**适用场景**：任何改动状态展示、状态文案或状态字段的请求。

**必须保留的含义**：
- **记录完整性**（`evidence_complete` / `ok_chain`）与**人工验收**（`acceptance`）
  是**两项不同的事实**，必须分别表达。
- `acceptance` 的取值 `pending_human_review` **表示"还没有人作接受决定"**。
  它**不是**界面标签，而是**事实字段**
  （`docs/courses/L01/WORKBENCH_SPEC.md`：要能查清"谁作了接受决定"）。

**允许的动作**：
- ✅ **优化中文措辞**：`"材料完整仍等待人工审核；完整性检查不能代替人的决定"`
  → `"材料完整，仍待人工审核"`（**保留"待"字**）
- ✅ **折叠详情**，只要仍提供完整历史入口
- ✅ 调整字段的**展示格式**（缩进、顺序），只要**取值不变**

**禁止的动作**：
- ❌ **不得由"记录完整"推导"人工验收通过"**。
  把 `acceptance` 改成 `accepted` / 文案改成"已验收通过"，
  **等于让程序替人签字** —— 而全仓没有任何一次真实验收记录。
- ❌ 不得只改**同一语义出现的多处之一**（`bootstrap.py` 的
  `review_status` / `review_note` / `completeness.note`），造成自相矛盾的输出。

**核对依据**（按顺序）：
1. `workbench/bootstrap.py` 的 `status()` —— 状态字段的真实来源
2. `docs/courses/L01/WORKBENCH_SPEC.md` —— 验收项 WB-07 写明了预期
3. `tests/test_l01_workbench_bootstrap.py` —— **看它到底断言了什么**

**缺口状态（2026-10-16 L02 更新）**：

- ⚠️ **原来确有缺口**：只把**文案**改成「已验收通过」而**不动字段取值**时，
  `test_l01_workbench_bootstrap` + `test_workbench_server` **全绿**（**Ran 14 ✗ OK**）。
  这是 L02 的 N1 执行者实测出来的（**变体 B**）✗ **不是推断**。
- ✅ **已补**：`tests/test_l02_status_invariants.py` 三条不变量 ——
  ① `acceptance` 是事实字段，记录齐全时仍须 `pending_human_review`；
  ② 任何一处输出/源码文案**不得出现替人签字的说法**；
  ③ 源码里 `review_status` / `review_note` / `note` 三处**必须一致**。
- **辨别力已验证**：对未改仓库通过；对变体 B 的副本 **FAILED (failures=2)**。
⇒ ⭐ **但"测试全绿"仍然只是必要条件**：它证明不了业务口径对不对
  （**那是 L05 的题目 ✗ 见 L03 的"结构通过 ≠ 业务正确"**）。

## 验证

在**仓库根目录**、用**课程解释器**运行：

```bash
/home/rchua/GO/CodexFDE/.venv/bin/python -X utf8 -m unittest \
  tests.test_l01_workbench_bootstrap tests.test_workbench_server \
  tests.test_l02_status_invariants -v
```

- 保留**完整输出与退出码**；**环境错误、零个用例、或"没有跑"都不能写成"通过"**。
- 改动状态相关代码后，**必须另外证明"危险请求被拦住"**（见上面的已知缺口）。

## 完成条件（Definition of Done）

交回以下四项，缺一项就不算完成：

1. **改了什么**（文件与行号）+ **为什么这样改**（对应哪条边界）
2. **实际验证结果**：命令、退出码、输出摘要（**不写"应该没问题"**）
3. **未解决的问题**：如实列，不粉饰
4. **人工接受、退回或依据不足的决定及理由** ——
   由**具名的人**填；**记录完整不等于验收通过**；
   在拿到具名决定前，状态**保持 `pending_human_review`**。

## 提交与边界（后续 FlowERP 开发适用）

- 可用库存**不得为负**；预占**必须原子化**
- **同一个入库幂等键只能生效一次**
- 订单**只能按状态机迁移**；取消要**释放预占**
- **采购补货必须由具名人员批准后才能入库**

**⇒ 本讲只评审计划，业务账保持原状 —— 不改 FlowERP。**
