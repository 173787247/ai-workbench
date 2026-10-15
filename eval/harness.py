"""L04 最小 Eval：只做**阻断级**检查，不替代业务验收。

`minimum_eval` 回答的问题只有一个：**这次受控执行是否留下了可核对的证据？**
它**不判断**库存导出是否正确 —— 业务验收归人。
"""
from __future__ import annotations

import json
from pathlib import Path


def minimum_eval(runtime, *, expect_task: str, result_changed=(),
                 expect_evidence: str | None = None,
                 expect_evidence_id: int | None = None,
                 expect_digest: str | None = None) -> tuple[bool, str]:
    """返回 (是否通过, 说明)。**通过不等于被接受** —— acceptance 恒为 pending_human_review。"""
    import hashlib as _hashlib
    import sqlite3

    runtime = Path(runtime)
    directory = runtime / "evidence"

    # ── 第四轮复验 ②⑧：**以 L01 账本为权威副本 ✗ 不用 mtime 猜** ──
    # 原实现有两处会被伪造证据骗过：
    #   (1) `key=st_mtime_ns` 选证据 → 攻击者用 `os.utime` 把 mtime 推到未来即可抢占；
    #   (2) `if digest_file.is_file():` → 指纹文件被删就**跳过校验**（自毁式校验）。
    # 现在：优先按账本里**最新的一条** evidence_id 定位证据 ✗ 并校验它与账本摘要一致。
    db = runtime / "workbench.db"
    if not db.is_file():
        return False, (f"最小 Eval 未通过：找不到 L01 账本（{db}）✗ "
                       "无法确认哪一份证据是权威的")
    try:
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            row = conn.execute(
                "SELECT evidence_id, output_sha256, returncode, phase"
                " FROM evidence WHERE task_id=? ORDER BY evidence_id DESC LIMIT 1",
                (expect_task,)).fetchone()
        finally:
            conn.close()
    except sqlite3.Error as error:
        return False, f"最小 Eval 未通过：账本不可读（{error}）"

    if row is None:
        return False, f"最小 Eval 未通过：账本里没有任务 {expect_task} 的运行记录"
    evidence_id, ledger_digest, ledger_rc, ledger_phase = row

    # 第五轮复验 R-2：**精确绑定「本次」** ✗
    # 只按「该任务最新一行」找 ✗ 一次干净的追加失败就会让它去校验**上一轮**的证据 ✓
    if expect_evidence_id is not None and evidence_id != expect_evidence_id:
        return False, (f"最小 Eval 未通过：账本最新记录的 evidence_id={evidence_id} "
                       f"不是本次的 {expect_evidence_id}（本次未成功入账）")
    if expect_digest is not None and ledger_digest != expect_digest:
        return False, (f"最小 Eval 未通过：账本里的摘要 {str(ledger_digest)[:16]}… "
                       f"与本次证据的摘要 {expect_digest[:16]}… 不符（本次未成功入账）")

    # 账本存的是**证据内容的哈希** ✗ 不是路径 ✓
    # 所以要在磁盘上找**哈希与账本一致的那一份** —— 找不到就是不通过 ✓
    #
    # ⚠️ **第五轮复验 R-3 更正**：原注释写「删掉 / 改写 / **伪造新证据** 都过不了」✗
    # **「伪造」那半是错的。** 复验者实测：被执行命令自己写一份
    # `<task>-20990101…-execution.json` + 配套 `.sha256` ✗ 再往 `evidence` 表插一行 ✗
    # **就能让 Eval 通过** ✓ 而且 `course-submit` 的候选就在 `<runtime>/candidates/<task>-<stamp>`
    # ✗ **命令从 cwd 向上两级就能找到 `workbench.db` ✗ 不需要任何带外信息** ✓
    #
    # **准确的说法**：
    #   ✓ 删掉既有证据 → 不通过（账本里那一条找不到对应文件）
    #   ✓ 改写既有证据 → 不通过（摘要对不上）
    #   ✗ **伪造新证据（并自行入账）→ 挡不住** —— 命令与账本**同一权限域** ✓
    #     **要根治需要隔离执行 / 签名 / nonce** ✗ **这是方案层面的取舍 ✗ 应由人决定** ✓
    #   ✓ 但 R-2 修好后，「真实追加失败」会立刻判失败 ✗ 伪造不再**静默**生效 ✓
    if not directory.is_dir():
        return False, f"最小 Eval 未通过：证据目录不存在（{directory}）"
    evidence, actual = None, None
    for cand in sorted(directory.glob(f"{expect_task}-*-execution.json")):
        try:
            digest = _hashlib.sha256(cand.read_bytes()).hexdigest()
        except OSError:
            continue
        if digest == ledger_digest:
            evidence, actual = cand, digest
            break
    if evidence is None:
        return False, (f"最小 Eval 未通过：磁盘上找不到与账本摘要一致的证据 ✗ "
                       f"（账本 evidence_id={evidence_id} ✗ 摘要 {ledger_digest[:16]}…）"
                       "—— 证据被删或被改，都不能让它变成通过")

    # **指纹文件缺失 = 不通过** ✗ 不是跳过 ✓
    digest_file = evidence.with_suffix(".sha256")
    # **指纹文件缺失 = 不通过** ✗ 不是跳过 ✓
    digest_file = evidence.with_suffix(".sha256")
    if not digest_file.is_file():
        return False, (f"最小 Eval 未通过：证据指纹文件缺失（{digest_file.name}）✗ "
                       "删掉指纹不能让它变成通过")
    try:
        if digest_file.read_text(encoding="utf-8").strip() != actual:
            return False, f"最小 Eval 未通过：证据指纹不符，{evidence.name} 已被改写"
    except OSError as error:
        return False, f"最小 Eval 未通过：指纹文件不可读（{error}）"

    try:
        payload = json.loads(evidence.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return False, f"最小 Eval 未通过：执行证据不可读（{error}）"

    # **以账本记录的退出码为准** ✗ 磁盘上的 JSON 只是副本 ✓
    if ledger_rc is not None and payload.get("returncode") != ledger_rc:
        return False, (f"最小 Eval 未通过：证据里的退出码 {payload.get('returncode')} "
                       f"与账本记录的 {ledger_rc} 不符")

    if payload.get("task_id") != expect_task:
        return False, f"最小 Eval 未通过：证据里的任务编号不是 {expect_task}"
    if payload.get("stopped"):
        return False, f"最小 Eval 未通过：执行已停止（{payload.get('stop_reason')}）"
    if payload.get("returncode") != 0:
        return False, f"最小 Eval 未通过：退出码为 {payload.get('returncode')}"
    if payload.get("out_of_scope"):
        return False, f"最小 Eval 未通过：存在越界改动 {payload['out_of_scope']}"
    if not payload.get("changed_files"):
        return False, "最小 Eval 未通过：本次执行没有产生可核对的改动"
    if payload.get("acceptance") != "pending_human_review":
        return False, "最小 Eval 未通过：验收状态被自动改写，违反『程序不能替人签字』"
    return True, (f"最小 Eval 通过：任务 {expect_task} 退出码 0、改动 {len(payload['changed_files'])} 个、"
                  f"全部在写集内（账本 evidence_id={evidence_id} ✗ {evidence.name} ✗ "
                  f"与账本摘要一致）；**业务验收与接受仍待具名的人**")


def blocking_suite(runtime, *, expect_task: str) -> dict:
    """阻断级检查的汇总视图。"""
    ok, message = minimum_eval(runtime, expect_task=expect_task)
    return {"suite": "blocking", "ok": ok, "message": message,
            "acceptance": "pending_human_review"}
