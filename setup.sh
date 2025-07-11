#!/bin/bash

# 🤖 Binance Futures Trading Bot - Automated Setup Script
# ======================================================

echo "🚀 Starting Binance Futures Trading Bot Setup..."
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env configuration file..."
    cat > .env << 'EOF'
# ========================================
# 🤖 BINANCE FUTURES TRADING BOT CONFIG
# ========================================

# 🔑 BINANCE API CONFIGURATION
API_KEY=your_binance_api_key_here
API_SECRET=your_binance_secret_key_here

# 📱 TELEGRAM CONFIGURATION
TELEGRAM_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# ⚙️ TRADING CONFIGURATION
DEFAULT_SYMBOL=BTCUSDT
TEST_MODE=true  # Set to false for real trading!

# 🎯 TRADING MODES
# TEST_MODE=true  = Testnet (paper trading)
# TEST_MODE=false = Real trading (LIVE MONEY)
EOF
    echo "✅ Created .env file - PLEASE EDIT IT WITH YOUR CREDENTIALS!"
else
    echo "ℹ️ .env file already exists"
fi

# Create run script
echo "📜 Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
echo "🤖 Starting Binance Futures Trading Bot..."
source venv/bin/activate
python3 main.py
EOF

chmod +x run.sh

echo ""
echo "🎉 Setup completed successfully!"
echo "================================"
echo ""
echo "📋 Next Steps:"
echo "1. Edit the .env file with your API credentials:"
echo "   nano .env"
echo ""
echo "2. Get your Binance API keys:"
echo "   - Go to: https://www.binance.com/en/my/settings/api-management"
echo "   - Create new API key with Futures trading permissions"
echo ""
echo "3. Create Telegram bot:"
echo "   - Message @BotFather on Telegram"
echo "   - Use /newbot command"
echo "   - Get your chat ID from @userinfobot"
echo ""
echo "4. Start the bot:"
echo "   ./run.sh"
echo ""
echo "⚠️  IMPORTANT: Start with TEST_MODE=true for safety!"
echo "🔒 Never share your API keys with anyone!"
echo ""
echo "📖 For detailed instructions, see: trading_bot_analysis.md"