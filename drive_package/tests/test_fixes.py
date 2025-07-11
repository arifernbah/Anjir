import asyncio
from unittest import mock
import pytest

# Import modules from project
from core.bot_runner import BinanceFuturesProBot
from modules.telegram_handler import TelegramNotifier


@pytest.mark.asyncio
async def test_min_notional_handling():
    """execute_trade_pro should skip trades < $5 notional and return False"""

    bot = BinanceFuturesProBot()

    # --- Mock Binance client ---
    class DummyClient:
        async def futures_account_balance(self):
            return [{"asset": "USDT", "balance": "100"}]

        async def futures_symbol_ticker(self, symbol):
            return {"price": "0.5"}  # Very cheap, so notional likely < $5

        async def futures_exchange_info(self):
            return {
                "symbols": [
                    {
                        "symbol": "DOGEUSDT",
                        "filters": [
                            {"filterType": "LOT_SIZE", "minQty": "1", "stepSize": "1"}
                        ],
                    }
                ]
            }

        async def futures_change_leverage(self, **kwargs):
            return {"leverage": kwargs.get("leverage", 2)}

        async def futures_create_order(self, **kwargs):
            # Should never be called because notional < 5
            raise AssertionError("Order should not be placed when notional < 5")

    bot.client = DummyClient()

    klines_stub = [[0, 0.5, 0.5, 0.5, 0.5, 100]] * 30  # Dummy klines

    entry_analysis = {
        "action": "long",
        "confidence": 80,
        "reason": "test",
        "pro_analysis": {},
        "position_sizing": {"risk_percentage": 0.02, "leverage": 2},
    }

    success = await bot.execute_trade_pro("DOGEUSDT", entry_analysis, klines_stub)
    assert success is False, "Trade should be skipped due to < $5 notional"


def test_numpy_import():
    """Importing modules should not raise NameError for numpy"""
    import importlib
    market_analysis = importlib.import_module("modules.market_analysis")
    assert hasattr(market_analysis, "np"), "numpy should be imported as np"


def test_fun_message_style():
    """New Telegram messages contain disclaimers and casual phrases"""
    notifier = TelegramNotifier("dummy", "dummy")
    msg = notifier.get_startup_message()
    assert "Disclaimer" in msg, "Startup message should include disclaimer"
    entry_msg = notifier.get_entry_message("long", "DOGEUSDT", 75, "testing", {}, {})
    assert "traktir" in entry_msg.lower() or "disclaimer" in entry_msg.lower()
    exit_msg = notifier.get_exit_message("DOGEUSDT", "LONG", 0.01, "hit tp", "LOW")
    assert "bot cuma" in exit_msg.lower()