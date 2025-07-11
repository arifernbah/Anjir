#!/bin/bash

# 🔄 Safe Requirements Update Script
# ==================================

echo "🔄 Starting Safe Requirements Update..."
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if bot is currently running
check_bot_running() {
    if pgrep -f "main.py" > /dev/null; then
        echo -e "${RED}⚠️  Bot is currently running!${NC}"
        echo "Please stop the bot first: pkill -f main.py"
        exit 1
    fi
}

# Backup current environment
backup_environment() {
    echo -e "${BLUE}📋 Creating backup...${NC}"
    
    # Backup requirements
    cp requirements.txt requirements_backup_$(date +%Y%m%d_%H%M%S).txt
    
    # Backup current package list
    pip freeze > installed_packages_backup_$(date +%Y%m%d_%H%M%S).txt
    
    echo -e "${GREEN}✅ Backup created successfully${NC}"
}

# Test bot functionality
test_bot() {
    echo -e "${BLUE}🧪 Testing bot functionality...${NC}"
    
    # Create test script
    cat > test_imports.py << 'EOF'
#!/usr/bin/env python3
import sys

def test_imports():
    try:
        # Test critical imports
        print("Testing python-binance...")
        from binance.client import Client
        
        print("Testing python-telegram-bot...")
        from telegram import Bot
        
        print("Testing data analysis libraries...")
        import numpy as np
        import pandas as pd
        
        print("Testing other utilities...")
        import requests
        import psutil
        import asyncio
        from dotenv import load_dotenv
        
        print("✅ All critical imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
EOF

    # Run test
    python3 test_imports.py
    test_result=$?
    
    # Cleanup test file
    rm test_imports.py
    
    return $test_result
}

# Update packages step by step
update_packages() {
    echo -e "${BLUE}📦 Updating packages step by step...${NC}"
    
    # Activate virtual environment if exists
    if [ -d "venv" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
    fi
    
    # Critical updates first
    echo -e "${YELLOW}1. Updating python-binance (CRITICAL)...${NC}"
    pip install --upgrade "python-binance>=1.0.46"
    if ! test_bot; then
        echo -e "${RED}❌ python-binance update failed tests!${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}2. Updating python-telegram-bot (CRITICAL)...${NC}"
    pip install --upgrade "python-telegram-bot>=21.9,<22.0"
    if ! test_bot; then
        echo -e "${RED}❌ python-telegram-bot update failed tests!${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}3. Updating psutil...${NC}"
    pip install --upgrade "psutil>=6.1.1"
    
    echo -e "${YELLOW}4. Updating numpy...${NC}"
    pip install --upgrade "numpy>=1.26.4"
    
    echo -e "${YELLOW}5. Updating pandas...${NC}"
    pip install --upgrade "pandas>=2.2.3"
    
    # Test again after all updates
    if test_bot; then
        echo -e "${GREEN}✅ All updates successful!${NC}"
        return 0
    else
        echo -e "${RED}❌ Final test failed!${NC}"
        return 1
    fi
}

# Rollback function
rollback() {
    echo -e "${YELLOW}🔙 Rolling back to previous versions...${NC}"
    
    # Find latest backup
    latest_backup=$(ls requirements_backup_*.txt 2>/dev/null | tail -1)
    
    if [ -n "$latest_backup" ]; then
        echo "Rolling back to: $latest_backup"
        pip install -r "$latest_backup" --force-reinstall
        
        if test_bot; then
            echo -e "${GREEN}✅ Rollback successful!${NC}"
        else
            echo -e "${RED}❌ Rollback failed! Manual intervention required.${NC}"
        fi
    else
        echo -e "${RED}❌ No backup found for rollback!${NC}"
    fi
}

# Main execution
main() {
    echo "🔍 Checking current status..."
    
    # Check if bot is running
    check_bot_running
    
    # Create backup
    backup_environment
    
    # Show current versions
    echo -e "${BLUE}📋 Current package versions:${NC}"
    pip list | grep -E "(binance|telegram|numpy|pandas|requests|psutil|asyncio)"
    
    # Ask for confirmation
    echo ""
    read -p "Continue with update? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Perform updates
        if update_packages; then
            echo ""
            echo -e "${GREEN}🎉 Update completed successfully!${NC}"
            echo -e "${BLUE}📋 New package versions:${NC}"
            pip list | grep -E "(binance|telegram|numpy|pandas|requests|psutil|asyncio)"
            
            # Update requirements.txt file
            pip freeze | grep -E "(python-binance|python-telegram-bot|numpy|pandas|requests|python-dotenv|psutil|asyncio-throttle)" > requirements_new.txt
            echo -e "${GREEN}📝 Generated requirements_new.txt${NC}"
            
        else
            echo ""
            echo -e "${RED}❌ Update failed!${NC}"
            read -p "Rollback to previous versions? (Y/n): " -n 1 -r
            echo
            
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                rollback
            fi
        fi
    else
        echo "Update cancelled."
    fi
}

# Run main function
main

echo ""
echo "📝 Next steps:"
echo "1. Test the bot: python3 main.py"
echo "2. Monitor for any errors"
echo "3. If issues occur, use rollback: ./update_requirements.sh rollback"