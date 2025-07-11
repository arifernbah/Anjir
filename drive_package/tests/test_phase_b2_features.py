import pytest
from modules.performance_monitor import PerformanceMonitor
from modules.smart_trading import SmartEntry, SmartExit
from modules.config_manager import SmartConfig

# ---------------- Heat-limit dynamic tests ----------------

def test_heat_limit_increase_after_win_streak():
    pm = PerformanceMonitor()
    start_limit = pm.get_current_heat_limit_pct()
    # 3 consecutive wins
    for _ in range(3):
        pm.add_trade({'profit_pct': 0.01})
    assert pm.get_current_heat_limit_pct() == min(start_limit + 2, 20)


def test_heat_limit_decrease_after_lose_streak():
    pm = PerformanceMonitor()
    pm.current_heat_limit_pct = 12  # start higher
    # 2 consecutive losses
    for _ in range(2):
        pm.add_trade({'profit_pct': -0.02})
    assert pm.get_current_heat_limit_pct() == max(12 - 2, 6)

# ---------------- Pattern bonus tests ----------------

def test_pattern_confidence_bonus():
    cfg = SmartConfig()
    se = SmartEntry(cfg)
    pattern = "bullish_dominant"
    # feed 30 trades, 20 wins (66%)
    for i in range(30):
        se.pattern_stats.setdefault(pattern, {'trades': 0, 'wins': 0})
        se.pattern_stats[pattern]['trades'] += 1
        if i < 20:
            se.pattern_stats[pattern]['wins'] += 1
    bonus = se._get_pattern_confidence_bonus(pattern)
    assert bonus == 5
    # underperforming pattern
    bad_pattern = "bearish_dominant"
    for i in range(40):
        se.pattern_stats.setdefault(bad_pattern, {'trades': 0, 'wins': 0})
        se.pattern_stats[bad_pattern]['trades'] += 1
        if i < 16:  # 40% win rate
            se.pattern_stats[bad_pattern]['wins'] += 1
    penalty = se._get_pattern_confidence_bonus(bad_pattern)
    assert penalty == -5

# ---------------- Adaptive SL/TP tests ----------------

def test_dynamic_sl_tp_ranges():
    cfg = SmartConfig()
    se = SmartExit(cfg)
    sl,tp = se._get_dynamic_sl_tp(0.8, 'trending_strong')
    assert tp > 0 and abs(sl) > 0
    assert tp > 0.008  # trending strong +25%
    sl2,tp2 = se._get_dynamic_sl_tp(3.5, 'volatile')
    assert abs(sl2) > abs(sl)  # wider stop in volatile