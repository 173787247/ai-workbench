"""每日持仓风控检查 —— 结营毕设的交付物。

设计要点（全部来自 `docs/AI-TRADING-RULES.md` 与毕设 Spec）：

1. **只读**：不修改任何交易数据；只产出报告。
2. **三种结论**：每条检查对每只持仓给出
   `pass`（未触发）/ `triggered`（已触发）/ `unknown`（无法判断）。
   **`unknown` 是一等公民 ✗ 不允许静默跳过** ✓
3. **可重算**：每项结论都带**算它的输入与算式**，第三方能独立复算。
4. **带出处**：每项带规则文件的**章节号**。
5. **不替人决定**：报告末尾永远是 `pending_human_review` ✓
6. **失败即失败**：缺输入是 `unknown` ✗ 不是 `pass` ✓

规则出处（`docs/AI-TRADING-RULES.md`）：
    §1  单票 20% / 二级行业 20% 且 ≤2 只 / 一级行业 35% / 最低现金 5%
    §2  2N 止损 / 硬止损（单笔 ≥ 总资产 2%）/ 时间止损（≥60 交易日且未盈利）
    §5  停手线：黄 2% / 橙 8% / 红 15%
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

#: 检查结论 —— **`unknown` 必须存在**，否则「缺数据」会被悄悄算成通过。
PASS = "pass"
TRIGGERED = "triggered"
UNKNOWN = "unknown"

#: 报告结尾永远是这个 —— 程序不能替人签字（`AGENTS.md` §一）。
HUMAN_REVIEW = "pending_human_review"

#: 规则里的阈值（**全部是倍数或百分比 ✗ 不含任何绝对金额**）。
LIMITS = {
    "single_position_pct": 0.20,      # §1 单票上限
    "industry2_pct": 0.20,            # §1 二级行业上限
    "industry2_max_count": 2,         # §1 二级行业最多 2 只
    "industry1_pct": 0.35,            # §1 一级行业上限
    "min_cash_pct": 0.05,             # §1 最低现金
    "atr_stop_multiple": 2.0,         # §2 2N 止损
    "hard_stop_pct": 0.02,            # §2 硬止损（占总资产）
    "time_stop_days": 60,             # §2 时间止损
    "halt_yellow_pct": 0.02,          # §5 黄
    "halt_orange_pct": 0.08,          # §5 橙
    "halt_red_pct": 0.15,             # §5 红
}


class SnapshotError(ValueError):
    """快照本身不可用（缺字段 / 类型错 / 过期）。"""


@dataclass
class Finding:
    """一条检查结论。"""

    code: str                 # C1..C8
    rule_ref: str             # 规则出处，如 "§2"
    subject: str              # 检查对象：占位代码或 "组合"
    status: str               # pass / triggered / unknown
    detail: str               # 人读的说明
    inputs: dict = field(default_factory=dict)   # **算它的输入 ✗ 让第三方能重算**
    shortfall: float | None = None               # 触发时差多少（None = 不适用）

    def as_dict(self) -> dict:
        return {
            "code": self.code, "rule_ref": self.rule_ref, "subject": self.subject,
            "status": self.status, "detail": self.detail,
            "inputs": self.inputs, "shortfall": self.shortfall,
        }


# --------------------------------------------------------------------------- #
# 快照校验
# --------------------------------------------------------------------------- #

def _require(obj: dict, key: str, where: str):
    if key not in obj or obj[key] is None:
        raise SnapshotError(f"{where} 缺字段 {key!r} ✗ 无法判断 ✗ 不写成通过")
    return obj[key]


def load_snapshot(path) -> dict:
    """读快照并做**结构校验**（不判断业务正确性）。"""
    text = Path(path).read_text(encoding="utf-8")
    try:
        snap = json.loads(text)
    except json.JSONDecodeError as error:
        raise SnapshotError(f"快照不是合法 JSON：{error}") from error
    _require(snap, "as_of", "快照")
    _require(snap, "total_assets_pct_base", "快照")
    positions = _require(snap, "positions", "快照")
    if not isinstance(positions, list):
        raise SnapshotError("positions 必须是列表")
    seen = set()
    for i, pos in enumerate(positions):
        where = f"positions[{i}]"
        code = _require(pos, "code", where)
        if code in seen:
            raise SnapshotError(f"{where} 代码重复：{code}（同一只出现两次会让占比算错）")
        seen.add(code)
        _require(pos, "weight_pct", where)
        _require(pos, "industry_l1", where)
        _require(pos, "industry_l2", where)
    return snap


def check_missing_positions(snapshot: dict, expected_codes) -> Finding:
    """**AC-3 的核心**：对照一份「应有的持仓清单」✗ 找出快照里**漏掉**的。

    这是「检查改善效果」的主判据 —— 手工核对最容易漏的就是这一步。
    """
    got = {p["code"] for p in snapshot.get("positions", [])}
    want = set(expected_codes or [])
    missing = sorted(want - got)
    extra = sorted(got - want)
    if missing:
        return Finding(
            "C0", "毕设 AC-3", "组合", TRIGGERED,
            f"快照漏掉 {len(missing)} 只：{', '.join(missing)}",
            {"expected": sorted(want), "got": sorted(got),
             "missing": missing, "extra": extra},
            shortfall=float(len(missing)),
        )
    if extra:
        return Finding(
            "C0", "毕设 AC-3", "组合", UNKNOWN,
            f"快照多了 {len(extra)} 只：{', '.join(extra)}（可能是清单过期 ✗ 需人确认）",
            {"expected": sorted(want), "got": sorted(got), "missing": missing},
        )
    return Finding("C0", "毕设 AC-3", "组合", PASS,
                   f"快照与应有清单一致（{len(got)} 只）",
                   {"expected": sorted(want), "got": sorted(got)})


# --------------------------------------------------------------------------- #
# C1 ~ C3：逐只的止损
# --------------------------------------------------------------------------- #

def check_2n_stop(pos: dict, *, limit: float = LIMITS["atr_stop_multiple"]) -> Finding:
    """C1 2N 止损：收盘价 < 开仓价 − 2×ATR(14)  →  §2。"""
    code = pos["code"]
    need = ("close", "open_price", "atr14")
    missing = [k for k in need if pos.get(k) is None]
    if missing:
        return Finding("C1", "§2", code, UNKNOWN,
                       f"缺 {', '.join(missing)} ✗ 无法算 2N 止损",
                       {k: pos.get(k) for k in need})
    stop = pos["open_price"] - limit * pos["atr14"]
    inputs = {"close": pos["close"], "open_price": pos["open_price"],
              "atr14": pos["atr14"], "multiple": limit, "stop": stop}
    if pos["close"] < stop:
        return Finding("C1", "§2", code, TRIGGERED,
                       f"收盘价 {pos['close']} < 2N 止损位 {stop:.4f}",
                       inputs, shortfall=round(stop - pos["close"], 6))
    return Finding("C1", "§2", code, PASS,
                   f"收盘价 {pos['close']} ≥ 2N 止损位 {stop:.4f}", inputs)


def check_hard_stop(pos: dict, *, limit: float = LIMITS["hard_stop_pct"]) -> Finding:
    """C2 硬止损：单笔亏损 ≥ 总资产 × 2%  →  §2。"""
    code = pos["code"]
    need = ("loss_pct_of_total",)
    missing = [k for k in need if pos.get(k) is None]
    if missing:
        return Finding("C2", "§2", code, UNKNOWN,
                       "缺 loss_pct_of_total ✗ 无法算硬止损", {k: pos.get(k) for k in need})
    loss = pos["loss_pct_of_total"]
    inputs = {"loss_pct_of_total": loss, "limit": limit}
    if loss >= limit:
        return Finding("C2", "§2", code, TRIGGERED,
                       f"单笔亏损占总资产 {loss:.2%} ≥ {limit:.0%}", inputs,
                       shortfall=round(loss - limit, 6))
    return Finding("C2", "§2", code, PASS,
                   f"单笔亏损占总资产 {loss:.2%} < {limit:.0%}", inputs)


def check_time_stop(pos: dict, *, limit: int = LIMITS["time_stop_days"]) -> Finding:
    """C3 时间止损：持有 ≥ 60 个交易日**且未盈利**  →  §2。"""
    code = pos["code"]
    need = ("held_days", "unrealized_pnl_pct")
    missing = [k for k in need if pos.get(k) is None]
    if missing:
        return Finding("C3", "§2", code, UNKNOWN,
                       f"缺 {', '.join(missing)} ✗ 无法算时间止损",
                       {k: pos.get(k) for k in need})
    days, pnl = pos["held_days"], pos["unrealized_pnl_pct"]
    inputs = {"held_days": days, "unrealized_pnl_pct": pnl, "limit": limit}
    if days >= limit and pnl <= 0:
        return Finding("C3", "§2", code, TRIGGERED,
                       f"持有 {days} 个交易日 ≥ {limit} 且未盈利（{pnl:.2%}）", inputs,
                       shortfall=float(days - limit))
    return Finding("C3", "§2", code, PASS,
                   f"持有 {days} 日 ✗ 未盈利 {pnl:.2%} → 不触发", inputs)


# --------------------------------------------------------------------------- #
# C4 ~ C6：集中度（组合层面）
# --------------------------------------------------------------------------- #

def check_single_position(snapshot: dict, *, limit: float = LIMITS["single_position_pct"]):
    """C4 单票上限：单只市值 ≤ 总资产 × 20%  →  §1。"""
    out = []
    for pos in snapshot["positions"]:
        w = pos["weight_pct"]
        inputs = {"weight_pct": w, "limit": limit}
        if w > limit:
            out.append(Finding("C4", "§1", pos["code"], TRIGGERED,
                               f"单票占比 {w:.2%} > {limit:.0%}", inputs,
                               shortfall=round(w - limit, 6)))
        else:
            out.append(Finding("C4", "§1", pos["code"], PASS,
                               f"单票占比 {w:.2%} ≤ {limit:.0%}", inputs))
    return out


def _group_weights(snapshot: dict, key: str) -> dict:
    """按行业字段汇总权重与只数（**可被第三方重算**）。"""
    agg: dict[str, dict] = {}
    for pos in snapshot["positions"]:
        name = pos.get(key)
        if name is None:
            continue
        slot = agg.setdefault(name, {"weight": 0.0, "codes": []})
        slot["weight"] += pos["weight_pct"]
        slot["codes"].append(pos["code"])
    return agg


def check_industry2(snapshot: dict, *,
                    pct_limit: float = LIMITS["industry2_pct"],
                    count_limit: int = LIMITS["industry2_max_count"]):
    """C5 二级行业：≤ 总资产 × 20% **且** ≤ 2 只  →  §1。"""
    out = []
    for name, slot in sorted(_group_weights(snapshot, "industry_l2").items()):
        w, n = slot["weight"], len(slot["codes"])
        inputs = {"industry_l2": name, "weight_pct": round(w, 6), "count": n,
                  "pct_limit": pct_limit, "count_limit": count_limit,
                  "codes": slot["codes"]}
        if w > pct_limit:
            out.append(Finding("C5", "§1", f"行业:{name}", TRIGGERED,
                               f"二级行业占比 {w:.2%} > {pct_limit:.0%}（{n} 只）", inputs,
                               shortfall=round(w - pct_limit, 6)))
        elif n > count_limit:
            out.append(Finding("C5", "§1", f"行业:{name}", TRIGGERED,
                               f"二级行业 {n} 只 > {count_limit} 只", inputs,
                               shortfall=float(n - count_limit)))
        else:
            out.append(Finding("C5", "§1", f"行业:{name}", PASS,
                               f"二级行业 {w:.2%} ≤ {pct_limit:.0%} 且 {n} ≤ {count_limit} 只",
                               inputs))
    return out


def check_industry1(snapshot: dict, *, limit: float = LIMITS["industry1_pct"]):
    """C6 一级行业：≤ 总资产 × 35%  →  §1。"""
    out = []
    for name, slot in sorted(_group_weights(snapshot, "industry_l1").items()):
        w = slot["weight"]
        inputs = {"industry_l1": name, "weight_pct": round(w, 6), "limit": limit,
                  "codes": slot["codes"]}
        if w > limit:
            out.append(Finding("C6", "§1", f"一级行业:{name}", TRIGGERED,
                               f"一级行业占比 {w:.2%} > {limit:.0%}", inputs,
                               shortfall=round(w - limit, 6)))
        else:
            out.append(Finding("C6", "§1", f"一级行业:{name}", PASS,
                               f"一级行业 {w:.2%} ≤ {limit:.0%}", inputs))
    return out


def check_min_cash(snapshot: dict, *, limit: float = LIMITS["min_cash_pct"]) -> Finding:
    """C7 最低现金：可用资金 ≥ 总资产 × 5%  →  §1。"""
    cash = snapshot.get("cash_weight_pct")
    if cash is None:
        return Finding("C7", "§1", "组合", UNKNOWN,
                       "缺 cash_weight_pct ✗ 无法算最低现金", {"cash_weight_pct": None})
    inputs = {"cash_weight_pct": cash, "limit": limit}
    if cash < limit:
        return Finding("C7", "§1", "组合", TRIGGERED,
                       f"可用资金占比 {cash:.2%} < {limit:.0%}", inputs,
                       shortfall=round(limit - cash, 6))
    return Finding("C7", "§1", "组合", PASS,
                   f"可用资金占比 {cash:.2%} ≥ {limit:.0%}", inputs)


def check_halt_line(snapshot: dict) -> Finding:
    """C8 停手线：累计回撤 黄 2% / 橙 8% / **红 15% → 清仓 + 停手**  →  §5。"""
    dd = snapshot.get("drawdown_pct")
    if dd is None:
        return Finding("C8", "§5", "组合", UNKNOWN,
                       "缺 drawdown_pct ✗ 无法判断停手线", {"drawdown_pct": None})
    inputs = {"drawdown_pct": dd, "yellow": LIMITS["halt_yellow_pct"],
              "orange": LIMITS["halt_orange_pct"], "red": LIMITS["halt_red_pct"]}
    if dd >= LIMITS["halt_red_pct"]:
        return Finding("C8", "§5", "组合", TRIGGERED,
                       f"累计回撤 {dd:.2%} ≥ 红 15% → **全部清仓 + 停止交易 ✗ 等用户重新授权**",
                       inputs, shortfall=round(dd - LIMITS["halt_red_pct"], 6))
    if dd >= LIMITS["halt_orange_pct"]:
        return Finding("C8", "§5", "组合", TRIGGERED,
                       f"累计回撤 {dd:.2%} ≥ 橙 8% → 停止开新仓 ✗ 已有仓位按 §2 走", inputs,
                       shortfall=round(dd - LIMITS["halt_orange_pct"], 6))
    if dd >= LIMITS["halt_yellow_pct"]:
        return Finding("C8", "§5", "组合", TRIGGERED,
                       f"累计回撤 {dd:.2%} ≥ 黄 2% → 当日只卖不买", inputs,
                       shortfall=round(dd - LIMITS["halt_yellow_pct"], 6))
    return Finding("C8", "§5", "组合", PASS,
                   f"累计回撤 {dd:.2%} < 黄 2% ✗ 未触停手线", inputs)


# --------------------------------------------------------------------------- #
# 跌停 / 停牌例外（**规则明文唯一的例外**）
# --------------------------------------------------------------------------- #

def apply_untradeable(findings, snapshot: dict):
    """C1/C2 触发但当日**跌停或停牌** ⇒ 改为「触发 ✗ 今日不可执行 ✗ 顺延」。

    规则 §2 原文：「触发后不解释、不等反弹、不改规则 —— 这是止损的全部意义。
    **例外只有一条：停牌 / 跌停卖不出 ⇒ 记录并顺延到能卖的第一时间。**」

    ⚠️ **不能写成「已执行」✗ 也不能写成「未触发」** ✓ ——
    这是「失败不能被写成成功」在业务侧的对应物。
    """
    untradeable = {p["code"] for p in snapshot["positions"] if p.get("untradeable_today")}
    if not untradeable:
        return findings, []
    out, deferred = [], []
    for f in findings:
        if f.status == TRIGGERED and f.code in ("C1", "C2") and f.subject in untradeable:
            new = Finding(
                f.code, f.rule_ref, f.subject, TRIGGERED,
                f"{f.detail} ✗ **但当日跌停/停牌卖不出 ⇒ 记录并顺延到能卖的第一时间**",
                dict(f.inputs, untradeable_today=True), f.shortfall)
            out.append(new)
            deferred.append({"code": f.code, "subject": f.subject,
                             "reason": "跌停/停牌卖不出", "rule_ref": "§2 例外"})
        else:
            out.append(f)
    return out, deferred


# --------------------------------------------------------------------------- #
# 报告
# --------------------------------------------------------------------------- #

def run_checks(snapshot: dict, *, expected_codes=None) -> dict:
    """跑全部检查 ✗ 返回报告字典。**只读 ✗ 不修改任何输入。**"""
    findings: list[Finding] = []
    if expected_codes is not None:
        findings.append(check_missing_positions(snapshot, expected_codes))
    for pos in snapshot["positions"]:
        findings.append(check_2n_stop(pos))
        findings.append(check_hard_stop(pos))
        findings.append(check_time_stop(pos))
    findings.extend(check_single_position(snapshot))
    findings.extend(check_industry2(snapshot))
    findings.extend(check_industry1(snapshot))
    findings.append(check_min_cash(snapshot))
    findings.append(check_halt_line(snapshot))

    findings, deferred = apply_untradeable(findings, snapshot)

    by_status = {PASS: [], TRIGGERED: [], UNKNOWN: []}
    for f in findings:
        by_status[f.status].append(f)

    # **合计风险**：全部触发止损时的亏损合计占总资产比例（AC-2 ✗ 可逐项加总复算）
    trig = [f for f in by_status[TRIGGERED] if f.code in ("C1", "C2")]
    parts = []
    for f in trig:
        sub = next((p for p in snapshot["positions"] if p["code"] == f.subject), None)
        if sub is not None and sub.get("loss_if_stopped_pct") is not None:
            parts.append({"code": f.subject, "loss_pct": sub["loss_if_stopped_pct"]})
    total = round(sum(p["loss_pct"] for p in parts), 6) if parts else 0.0

    return {
        "as_of": snapshot["as_of"],
        "coverage": {
            "checked": ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"],
            "not_checked": ["移动止损（§2，需历史最高价）",
                            "熔断（§2，系统已有 kris）",
                            "单日买入上限 10%（§1，当日买入数据不在快照里）",
                            "单一策略 30%（§1，策略归属不在快照里）"],
            "why": "只覆盖**机械可判**的项；其余需要快照里没有的输入 ✗ 如实列出而不假装覆盖。",
        },
        "counts": {k: len(v) for k, v in by_status.items()},
        "findings": [f.as_dict() for f in findings],
        "aggregate_risk": {
            "triggered_stop_count": len(parts),
            "total_loss_pct_if_all_stopped": total,
            "parts": parts,
            "note": "可逐项加总复算；百分比 ✗ 不含绝对金额。",
        },
        "deferred_actions": deferred,
        "acceptance": HUMAN_REVIEW,
        "accepted": False,
        "disclaimer": "本报告只做算术核对 ✗ 不构成买卖建议 ✗ 处置决定由人作出。",
    }


def render_markdown(report: dict) -> str:
    """人可读版（与 JSON 同源 ✗ 不另算一遍）。"""
    lines = [f"# 每日持仓风控检查 · {report['as_of']}", ""]
    c = report["counts"]
    lines += [f"**结论**：通过 {c['pass']} ✗ 触发 {c['triggered']} ✗ 无法判断 {c['unknown']}", ""]
    if report["deferred_actions"]:
        lines += ["## ⚠️ 触发但今日不可执行（顺延）", ""]
        for d in report["deferred_actions"]:
            lines.append(f"- `{d['code']}` {d['subject']}：{d['reason']}（{d['rule_ref']}）")
        lines.append("")
    for title, key in (("触发", "triggered"), ("无法判断", "unknown"), ("通过", "pass")):
        rows = [f for f in report["findings"] if f["status"] == key]
        if not rows:
            continue
        lines += [f"## {title}（{len(rows)}）", ""]
        for f in rows:
            lines.append(f"- **{f['code']}** `{f['subject']}`（{f['rule_ref']}）：{f['detail']}")
        lines.append("")
    lines += ["## 覆盖边界", "", report["coverage"]["why"], ""]
    for item in report["coverage"]["not_checked"]:
        lines.append(f"- 未覆盖：{item}")
    lines += ["", "## 合计风险", "",
              f"触发止损的 {report['aggregate_risk']['triggered_stop_count']} 只 ✗ "
              f"全部触及时的合计亏损占总资产 **{report['aggregate_risk']['total_loss_pct_if_all_stopped']:.2%}**", ""]
    lines += [f"---", "",
              f"**接受状态：`{report['acceptance']}`** —— {report['disclaimer']}"]
    return "\n".join(lines) + "\n"
