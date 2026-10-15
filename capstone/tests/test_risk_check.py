"""毕设验收用例 AC-1 ~ AC-8 的可复跑测试。

运行：`python -X utf8 -m unittest discover -s capstone/tests`
"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from capstone.risk_check import (                                    # noqa: E402
    HUMAN_REVIEW, PASS, TRIGGERED, UNKNOWN, Finding, SnapshotError,
    check_2n_stop, check_halt_line, check_hard_stop, check_missing_positions,
    check_time_stop, load_snapshot, render_markdown, run_checks,
)
from capstone.__main__ import main                                   # noqa: E402


def run_cli(argv):
    """跑 CLI 但**吞掉它的打印** ✗ 只留退出码。"""
    with contextlib.redirect_stdout(io.StringIO()):
        return main(argv)

SAMPLE = ROOT / "capstone" / "samples" / "snapshot-2026-10-15.json"


def _snap() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


def _pos(**over):
    base = {"code": "X", "weight_pct": 0.05, "industry_l1": "A", "industry_l2": "A1",
            "close": 10.0, "open_price": 12.0, "atr14": 1.0, "held_days": 5,
            "unrealized_pnl_pct": -0.1, "loss_pct_of_total": 0.005}
    base.update(over)
    return base


class CapstoneTests(unittest.TestCase):

    # ---------- AC-1：单只 2N 止损 ----------
    def test_ac1_2n_stop_triggers_with_shortfall_and_rule_ref(self):
        f = check_2n_stop(_pos(close=9.0, open_price=12.0, atr14=1.0))   # 止损位 10.0
        self.assertEqual(f.status, TRIGGERED)
        self.assertEqual(f.rule_ref, "§2")
        self.assertAlmostEqual(f.shortfall, 1.0)
        # **可重算**：输入齐全
        for k in ("close", "open_price", "atr14", "multiple", "stop"):
            self.assertIn(k, f.inputs)

    def test_ac1_boundary_equal_is_not_triggered(self):
        """规则是 `<` 止损位才触发 ✗ 等于不触发 ✓（边界）"""
        f = check_2n_stop(_pos(close=10.0, open_price=12.0, atr14=1.0))
        self.assertEqual(f.status, PASS)

    # ---------- AC-2：合计风险可加总 ----------
    def test_ac2_aggregate_risk_is_sum_of_parts(self):
        rep = run_checks(_snap())
        agg = rep["aggregate_risk"]
        self.assertEqual(agg["triggered_stop_count"], len(agg["parts"]))
        self.assertAlmostEqual(agg["total_loss_pct_if_all_stopped"],
                               round(sum(p["loss_pct"] for p in agg["parts"]), 6))

    # ---------- AC-3：漏项检测（改进的核心判据）----------
    def test_ac3_missing_position_is_named(self):
        f = check_missing_positions(_snap(), ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG"])
        self.assertEqual(f.status, TRIGGERED)
        self.assertIn("GGG", f.detail)
        self.assertEqual(f.inputs["missing"], ["GGG"])

    def test_ac3_extra_position_is_unknown_not_pass(self):
        """快照多了清单里没有的 → **unknown**（可能清单过期）✗ 不是 pass。"""
        f = check_missing_positions(_snap(), ["AAA"])
        self.assertEqual(f.status, UNKNOWN)

    def test_ac3_consistent_returns_pass(self):
        f = check_missing_positions(_snap(),
                                    [p["code"] for p in _snap()["positions"]])
        self.assertEqual(f.status, PASS)

    # ---------- AC-4：空与异常输入 ----------
    def test_ac4_missing_atr_is_unknown_not_pass(self):
        f = check_2n_stop(_pos(atr14=None))
        self.assertEqual(f.status, UNKNOWN)
        self.assertIn("atr14", f.detail)

    def test_ac4_empty_positions_produces_no_fake_pass(self):
        snap = {"as_of": "x", "total_assets_pct_base": 1.0, "positions": []}
        rep = run_checks(snap)
        self.assertEqual(rep["counts"][TRIGGERED], 0)
        # C7/C8 缺输入 → unknown ✗ 不能因为没有持仓就报通过
        self.assertGreaterEqual(rep["counts"][UNKNOWN], 2)

    def test_ac4_bad_snapshot_is_controlled_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text('{"as_of":"x"}', encoding="utf-8")
            with self.assertRaises(SnapshotError):
                load_snapshot(bad)
            rc = run_cli([str(bad)])
            self.assertEqual(rc, 2, "受控失败 ✗ 不是崩溃")

    def test_ac4_duplicate_code_is_rejected(self):
        """同一只出现两次会让占比算错 ✗ 必须拒绝。"""
        snap = _snap()
        snap["positions"].append(dict(snap["positions"][0]))
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "dup.json"
            p.write_text(json.dumps(snap), encoding="utf-8")
            with self.assertRaises(SnapshotError):
                load_snapshot(p)

    # ---------- AC-5：跌停例外 ----------
    def test_ac5_triggered_but_untradeable_is_deferred(self):
        """规则 §2 唯一例外：跌停/停牌卖不出 ⇒ **记录并顺延**。

        既不能写成「已执行」✗ 也不能写成「未触发」✓
        """
        snap = _snap()
        for p in snap["positions"]:
            if p["code"] == "DDD":
                p["close"] = 40.0            # < 46.2 → 触发
                p["untradeable_today"] = True
        rep = run_checks(snap)
        self.assertTrue(rep["deferred_actions"], "必须留下顺延记录")
        ddd = [f for f in rep["findings"] if f["code"] == "C1" and f["subject"] == "DDD"][0]
        self.assertEqual(ddd["status"], TRIGGERED, "仍是触发 ✗ 不是未触发")
        self.assertIn("顺延", ddd["detail"], "必须写明不可执行并顺延")

    def test_ac5_tradeable_trigger_has_no_deferral(self):
        rep = run_checks(_snap())
        ddd = [f for f in rep["findings"] if f["code"] == "C1" and f["subject"] == "DDD"][0]
        self.assertEqual(ddd["status"], PASS)
        self.assertEqual(rep["deferred_actions"], [])

    # ---------- AC-6：只读性 ----------
    def test_ac6_run_does_not_modify_input(self):
        import hashlib
        before = hashlib.sha256(SAMPLE.read_bytes()).hexdigest()
        snap = _snap()
        frozen = json.dumps(snap, sort_keys=True)
        run_checks(snap)
        render_markdown(run_checks(snap))
        self.assertEqual(json.dumps(snap, sort_keys=True), frozen, "入参不得被修改")
        self.assertEqual(hashlib.sha256(SAMPLE.read_bytes()).hexdigest(), before,
                         "快照文件不得被改动")

    # ---------- AC-7：可重算 ----------
    def test_ac7_every_finding_carries_recomputable_inputs(self):
        rep = run_checks(_snap())
        for f in rep["findings"]:
            with self.subTest(code=f["code"], subject=f["subject"]):
                self.assertIsInstance(f["inputs"], dict)
                self.assertTrue(f["rule_ref"], "每项必须带规则出处")
                self.assertIn(f["status"], (PASS, TRIGGERED, UNKNOWN))

    def test_ac7_2n_stop_is_recomputable_from_inputs(self):
        f = check_2n_stop(_pos(close=9.0, open_price=12.0, atr14=1.0))
        i = f.inputs
        recomputed = i["open_price"] - i["multiple"] * i["atr14"]
        self.assertAlmostEqual(i["stop"], recomputed)
        self.assertAlmostEqual(f.shortfall, recomputed - i["close"])

    # ---------- AC-8：两次一致 + 不覆盖 ----------
    def test_ac8_two_runs_are_identical(self):
        a, b = run_checks(_snap()), run_checks(_snap())
        for rep in (a, b):
            rep.pop("as_of", None)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_ac8_reports_are_never_overwritten(self):
        import shutil
        tmp = tempfile.mkdtemp(prefix="cap8-")
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        for _ in range(3):
            self.assertEqual(run_cli([str(SAMPLE), "--out", tmp]), 1)
        files = sorted(Path(tmp).glob("risk-*.json"))
        self.assertEqual(len(files), 3, f"三次的报告都要留下，实得 {[f.name for f in files]}")

    # ---------- 附带：人工接受 & 覆盖边界 ----------
    def test_acceptance_always_pending_human_review(self):
        rep = run_checks(_snap())
        self.assertEqual(rep["acceptance"], HUMAN_REVIEW)
        self.assertFalse(rep["accepted"])

    def test_coverage_boundary_is_declared(self):
        rep = run_checks(_snap())
        self.assertTrue(rep["coverage"]["not_checked"], "必须列出未覆盖的规则项")
        self.assertTrue(rep["coverage"]["why"])

    def test_exit_code_reflects_triggered(self):
        self.assertEqual(run_cli([str(SAMPLE)]), 1)
        tmp = tempfile.mkdtemp()
        clean = Path(tmp) / "clean.json"
        snap = _snap()
        for p in snap["positions"]:
            p.update(close=p["open_price"], atr14=1.0, loss_pct_of_total=0.0,
                     held_days=1, unrealized_pnl_pct=0.01, weight_pct=0.01)
        snap["cash_weight_pct"] = 0.5
        snap["drawdown_pct"] = 0.0
        clean.write_text(json.dumps(snap), encoding="utf-8")
        self.assertEqual(run_cli([str(clean)]), 0, "全通过应返回 0")

    def test_halt_line_three_levels(self):
        for dd, expect in ((0.01, PASS), (0.03, TRIGGERED), (0.09, TRIGGERED), (0.16, TRIGGERED)):
            with self.subTest(drawdown=dd):
                f = check_halt_line({"drawdown_pct": dd})
                self.assertEqual(f.status, expect)
                self.assertEqual(f.rule_ref, "§5")

    def test_hard_stop_and_time_stop_boundaries(self):
        self.assertEqual(check_hard_stop({"code": "X", "loss_pct_of_total": 0.02}).status,
                         TRIGGERED, "≥ 2% 即触发")
        self.assertEqual(check_hard_stop({"code": "X", "loss_pct_of_total": 0.019}).status, PASS)
        self.assertEqual(check_time_stop({"code": "X", "held_days": 60,
                                          "unrealized_pnl_pct": 0.0}).status, TRIGGERED)
        self.assertEqual(check_time_stop({"code": "X", "held_days": 60,
                                          "unrealized_pnl_pct": 0.01}).status, PASS,
                         "盈利则不触发")


if __name__ == "__main__":
    unittest.main()
