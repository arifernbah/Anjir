#!/usr/bin/env python3
"""
Telegram Handler Module - SUPER BRILLIANT EDITION
Enhanced notifications with genius-level intelligence reporting
"""

import asyncio
import logging
from modules.constants import get_fee_rate
from datetime import datetime
from typing import Dict, Any, List
import telegram
import random

logger = logging.getLogger(__name__)

class TelegramNotifier:
    """SUPER BRILLIANT Telegram Notifier - Genius Level Intelligence Reporting"""
    
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.bot = None
        
        # Enhanced notification features
        self.last_notification_time = {}
        self.notification_cooldown = 30  # seconds
        
        # Genius notification templates
        self.genius_entry_emojis = ["🧠", "⚡", "🎯", "🚀", "💎", "🔥", "⭐", "🌟"]
        self.genius_exit_emojis = ["💰", "🎉", "✨", "🏆", "💎", "🌟", "⭐", "🔥"]
        self.pattern_emojis = {"hammer": "🔨", "doji": "⚖️", "engulfing": "🌊", "shooting_star": "⭐"}

        # Tongkrongan style extra phrases
        self.entry_quotes = [
            "Gaskeun jadi sultan! 👑",
            "Cuan tipis? Tetep traktir bakso lah! 🍜",
            "Kalo rugi, santuy... masih ada THR! 🧧",
            "Udah kaya abang2 indomaret antri top up! 🤣",
            "Profit = kopi + rokok, setuju? ☕️🚬",
            "Let's go to the moon sambil makan cilok! 🌕"
        ]
        self.exit_reactions = [
            "Aduh mantul! Lanjut grind! 💃",
            "Dompet ketawa nih! 😂",
            "Santai, masih bisa purchase skin ML 👾",
            "Yah zonk, tapi at least belajar ya bro 😂",
            "Udud dulu biar chill 🤙",
            "Tarik sis... semongko! 🍉"
        ]
        
    async def send_casual_message(self, message: str, parse_mode: str = 'Markdown'):
        """Send casual message dengan intelligent throttling"""
        try:
            if not self.token or not self.chat_id:
                logger.warning("Telegram credentials not configured")
                return
            
            # Initialize bot if not exists
            if not self.bot:
                self.bot = telegram.Bot(token=self.token)
            
            # Intelligent message throttling
            message_hash = hash(message[:50])  # Hash first 50 chars
            current_time = datetime.now().timestamp()
            
            if message_hash in self.last_notification_time:
                time_diff = current_time - self.last_notification_time[message_hash]
                if time_diff < self.notification_cooldown:
                    return  # Skip duplicate/similar messages
            
            self.last_notification_time[message_hash] = current_time
            
            # Note: Manual escaping is done in message creation, so we don't auto-escape here
            # This prevents double escaping of already escaped characters
            
            # Send message
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode
            )
            
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            # Fallback: try sending without parse_mode
            try:
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode=None
                )
            except Exception as e2:
                logger.error(f"Error sending Telegram message (fallback): {e2}")
    
    def _escape_markdown(self, text: str) -> str:
        """Escape special characters for Markdown parsing"""
        # Characters that need escaping in Markdown
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        
        return text
    
    def get_startup_message(self) -> str:
        """Startup message yang lucu dan ringan"""
        # Gaya temen tongkrongan yang konyol
        return (
            "🤖 *ArifBot hadir cuy!* \(mode *Optimized* dah nyala\)\n\n"
            "🍻 *Yo, geng!* Bot udah bangun dari tidur siang, siap cari cuan sambil ngopi! ☕️\n"
            "🎮 Fitur andalan lagi on semua: pattern detector, risk guard, auto-leverage… pokoknya kayak squad lengkap pas main futsal.\n\n"
            "⚙️ *Status tongkrongan:*\n"
            "• Otak bot: Masih waras ✅\n"
            "• Memori: Ga full, santuy ✅\n"
            "• Target: 30-45% per bulan \(ngayal dikit gapapa\) 🚀\n"
            "• Posisi aktif maksimal: 3 \(biar dompet ga nangis\)\n\n"
            "Gaskeun, siapa takut! Kalo profit traktir seblak ya! 🌶️"
        )
    
    def get_entry_message(self, action: str, symbol: str, confidence: float, reason: str, pro_analysis: Dict, genius_features: Dict = None) -> str:
        """Entry message versi tongkrongan kocak"""

        emoji = random.choice(["🍻", "🔥", "😎", "💸", "🙌", "🥳"])

        if action.lower() == "long":
            action_text = "NAIK BRO ↑"
            direction_emoji = "📈"
        elif action.lower() == "short":
            action_text = "TURUNIN AJA ↓"
            direction_emoji = "📉"
        else:
            action_text = action.upper()
            direction_emoji = "🤔"

        # Confidence commentary
        if confidence >= 90:
            conf_comment = "percaya diri pol!"  # very confident
        elif confidence >= 80:
            conf_comment = "mantap jiwa!"
        elif confidence >= 70:
            conf_comment = "oke juga nih"
        else:
            conf_comment = "hmm, gambling dikit"

        msg = (
            f"{emoji} *Signal Masuk, geng!* {direction_emoji}\n\n"
            f"{action_text} {symbol} – *confidence* {confidence:.0f}% ({conf_comment})\n"
        )

        # Tambah analisis ringkes
        if 'market_regime' in pro_analysis:
            regime = pro_analysis['market_regime'].get('regime', '???').title()
            msg += f"🌍 Market lagi *{regime}*\n"

        # Tambah reason singkat
        simple_reason = reason.split(" | ")[0]
        msg += f"💬 Alasan: _{simple_reason}_\n"

        msg += "\nGaskeun, tapi inget traktir es teh kalo profit! 🍵"

        # Tambah quote random biar rame
        msg += f"\n{random.choice(self.entry_quotes)}"

        return msg
    
    def get_exit_message(self, symbol: str, side: str, profit_pct: float, reason: str, urgency: str, exit_analysis: Dict = None) -> str:
        """Exit message versi tongkrongan kocak"""

        if profit_pct > 0:
            emoji = random.choice(["�", "🥳", "🤟", "�"])
            status = "Profit cuy!"
        else:
            emoji = "�"
            status = "Zonk, ga apa2 next time!"

        msg = (
            f"{emoji} *Trade Kelar*\n\n"
            f"{side} {symbol} ditutup \(P&L {profit_pct:+.2f}%\) → {status}\n"
        )

        simple_reason = reason.split(" | ")[0]
        msg += f"Alasan: _{simple_reason}_\n"

        msg += "\nUdah, yuk jajan dulu buat rayain / pelipur lara! 🍟"

        # Tambah reaksi tongkrongan random
        msg += f"\n{random.choice(self.exit_reactions)}"

        return msg
    
    def get_status_message(self, balance: float, active_positions: int, mode: str, pro_stats: Dict) -> str:
        """Simple status message"""
        
        # Status header
        if active_positions > 0:
            status_emoji = "⚡"
            status_text = "**Trading**"
        else:
            status_emoji = "😴"
            status_text = "**Standby**"
        
        message = f"""{status_emoji} **Bot Status**

💰 Balance: **${balance:.2f}** \\(duit kita\\)
📊 Positions: **{active_positions}** \\(yang lagi jalan\\)
🔧 Mode: **{mode}**
⚙️ Status: {status_text}

📈 Win Rate: **{pro_stats.get('win_rate', 0) * 100:.1f}%** \\(berapa kali menang\\)
🎯 Kelly: **{pro_stats.get('kelly_percentage', 0) * 100:.2f}%** \\(berapa % modal\\)

Ready cuan bro! Atau siap rugi �"""
        
        return message
    
    def get_performance_summary(self, trades_history: List[Dict], current_balance: float, initial_capital: float) -> str:
        """Enhanced performance summary dengan genius metrics"""
        
        if not trades_history:
            return f"""📊 **PERFORMANCE SUMMARY** 📈

💼 **PORTFOLIO STATUS:**
💰 Current Balance: **${current_balance:.2f}**
🏛️ Initial Capital: **${initial_capital:.2f}**
📈 Total Growth: **{((current_balance/initial_capital - 1) * 100):+.2f}%**

🧠 **INTELLIGENCE STATUS:**
⚡ Pattern Recognition: **LEARNING**
📊 Risk Management: **OPTIMIZING** 
🎯 Market Analysis: **CALIBRATING**

Ready untuk first trade! 🚀"""
        
        # Calculate performance metrics
        total_trades = len(trades_history)
        winning_trades = len([t for t in trades_history if t.get('profit_pct', 0) > 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_return = (current_balance / initial_capital - 1) * 100
        
        # Average profit per trade
        profits = [t.get('profit_pct', 0) * 100 for t in trades_history]
        avg_profit = sum(profits) / len(profits) if profits else 0
        
        # Best and worst trades
        best_trade = max(profits) if profits else 0
        worst_trade = min(profits) if profits else 0
        
        # Performance rating
        if win_rate >= 80 and total_return > 20:
            rating = "🏆 **GENIUS LEVEL**"
        elif win_rate >= 70 and total_return > 15:
            rating = "⭐ **EXCELLENT**"
        elif win_rate >= 60 and total_return > 10:
            rating = "✅ **VERY GOOD**"
        elif win_rate >= 50 and total_return > 5:
            rating = "📈 **GOOD**"
        else:
            rating = "🔧 **DEVELOPING**"
        
        message = f"""📊 **GENIUS PERFORMANCE REPORT** 🧠

🏆 **OVERALL RATING:** {rating}

💼 **PORTFOLIO METRICS:**
💰 Current Balance: **${current_balance:.2f}**
📈 Total Return: **{total_return:+.2f}%**
💎 Capital Growth: **${current_balance - initial_capital:+.2f}**

🎯 **TRADING STATISTICS:**
📊 Total Trades: **{total_trades}**
✅ Winning Trades: **{winning_trades}**
🎯 Win Rate: **{win_rate:.1f}%**
💰 Avg Profit/Trade: **{avg_profit:+.2f}%**

🚀 **EXTREMES:**
🌟 Best Trade: **{best_trade:+.2f}%**
🛡️ Worst Trade: **{worst_trade:+.2f}%**

🧠 **INTELLIGENCE ASSESSMENT:**"""
        
        # Add intelligence metrics
        if win_rate >= 75:
            message += f"\n⚡ Pattern Recognition: **MASTER LEVEL**"
        elif win_rate >= 65:
            message += f"\n🎯 Pattern Recognition: **ADVANCED**"
        elif win_rate >= 55:
            message += f"\n📊 Pattern Recognition: **INTERMEDIATE**"
        else:
            message += f"\n🔧 Pattern Recognition: **LEARNING**"
        
        if total_return > 15:
            message += f"\n💎 Risk Management: **OPTIMAL**"
        elif total_return > 8:
            message += f"\n🛡️ Risk Management: **EXCELLENT**"
        elif total_return > 3:
            message += f"\n✅ Risk Management: **GOOD**"
        else:
            message += f"\n⚠️ Risk Management: **CONSERVATIVE**"
        
        # Motivational end
        if total_return > 10:
            message += f"\n\n🚀 **EXCEPTIONAL PERFORMANCE!**\nGenius algorithm delivering results! 💎"
        elif total_return > 5:
            message += f"\n\n⭐ **SOLID PROGRESS!**\nIntelligence system working well! 🧠"
        elif total_return > 0:
            message += f"\n\n✅ **POSITIVE GROWTH!**\nSteady and consistent progress! 📈"
        else:
            message += f"\n\n🔧 **OPTIMIZATION PHASE!**\nLearning and improving continuously! 💪"
        
        return message
    
    def _get_entry_motivation(self, confidence: float) -> str:
        """Get motivational message based on confidence"""
        if confidence >= 90:
            motivations = [
                "🧠 **GENIUS SETUP!** This is what 10-year pro analysis looks like! 🚀",
                "⚡ **PERFECT CONFLUENCE!** All systems firing at maximum! 💎",
                "🎯 **INSTITUTIONAL GRADE!** Professional algorithm at work! 🏆"
            ]
        elif confidence >= 80:
            motivations = [
                "🌟 **HIGH PROBABILITY!** Strong professional analysis! ⚡",
                "💎 **EXCELLENT SETUP!** Confidence backed by data! 🎯",
                "🚀 **SMART ENTRY!** Intelligence system optimized! 🧠"
            ]
        elif confidence >= 70:
            motivations = [
                "✅ **GOOD OPPORTUNITY!** Solid analysis foundation! 📊",
                "🎯 **CALCULATED MOVE!** Professional risk assessment! 💪",
                "📈 **QUALITY SETUP!** Systematic approach working! ⚡"
            ]
        else:
            motivations = [
                "⚠️ **MODERATE SETUP!** Conservative approach activated! 🛡️",
                "🔧 **LEARNING OPPORTUNITY!** Building experience! 📚",
                "💪 **DISCIPLINED ENTRY!** Risk management first! 🏰"
            ]
        
        return random.choice(motivations)
    
    async def send_genius_analysis_update(self, analysis_data: Dict):
        """Send periodic genius analysis updates"""
        try:
            market_condition = analysis_data.get('market_condition', 'unknown')
            key_insights = analysis_data.get('key_insights', [])
            opportunities = analysis_data.get('opportunities', 0)
            
            message = f"""🧠 **GENIUS MARKET ANALYSIS** 📊

🌍 **Market Condition:** **{market_condition.title()}**
🔍 **Opportunities Detected:** **{opportunities}**

🎯 **Key Insights:**"""
            
            for insight in key_insights[:3]:  # Limit to 3 insights
                message += f"\n• {insight}"
            
            if opportunities > 0:
                message += f"\n\n⚡ **High probability setups being monitored!**"
            else:
                message += f"\n\n😴 **Patience mode: Waiting for optimal conditions**"
            
            await self.send_casual_message(message)
            
        except Exception as e:
            logger.error(f"Error sending analysis update: {e}")
    
    async def send_risk_alert(self, alert_type: str, details: Dict):
        """Send risk management alerts"""
        try:
            alert_styles = {
                "high_correlation": "⚠️ **CORRELATION ALERT**",
                "volatility_spike": "📈 **VOLATILITY ALERT**", 
                "drawdown_warning": "🛡️ **DRAWDOWN WARNING**",
                "position_limit": "📊 **POSITION ALERT**"
            }
            
            alert_header = alert_styles.get(alert_type, "⚠️ **RISK ALERT**")
            
            message = f"""{alert_header}

🔍 **Alert Type:** {alert_type.replace('_', ' ').title()}
⏰ **Time:** {datetime.now().strftime('%H:%M:%S')}

📋 **Details:**"""
            
            for key, value in details.items():
                if isinstance(value, float):
                    message += f"\n• {key.title()}: **{value:.2f}**"
                else:
                    message += f"\n• {key.title()}: **{value}**"
            
            message += f"\n\n🧠 **Action:** Risk management protocols activated automatically!"
            
            await self.send_casual_message(message)
            
        except Exception as e:
            logger.error(f"Error sending risk alert: {e}")