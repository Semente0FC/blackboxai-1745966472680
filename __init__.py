"""
Future MT5 Pro Trading System
Professional Fibonacci-based trading system for MetaTrader 5
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Version information
__version__ = '2.0.0'
__author__ = 'BLACKBOXAI'
__email__ = 'support@blackboxai.com'

# Import configuration and constants
from config import config
from constants import (
    SYSTEM, TRADING, FIBONACCI, ANALYSIS,
    MARKET_HOURS, UI, LOGGING
)

# Import core components
from logger import logger
from utils import (
    initialize_mt5, get_account_info, format_currency,
    check_market_hours, get_symbol_info,
    calculate_position_size, cleanup_mt5
)

# Import UI components
from styles import init_styles, Styles
from splash import show_splash
from login_window import show_login
from trading_app import TradingApp
from settings_dialog import show_settings

# Initialize styles
init_styles()

# Export public interface
__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__email__',
    
    # Core components
    'config',
    'logger',
    
    # Constants
    'SYSTEM',
    'TRADING',
    'FIBONACCI',
    'ANALYSIS',
    'MARKET_HOURS',
    'UI',
    'LOGGING',
    
    # Utility functions
    'initialize_mt5',
    'get_account_info',
    'format_currency',
    'check_market_hours',
    'get_symbol_info',
    'calculate_position_size',
    'cleanup_mt5',
    
    # UI components
    'Styles',
    'init_styles',
    'show_splash',
    'show_login',
    'TradingApp',
    'show_settings'
]

def main():
    """Main entry point"""
    from main import main as run_main
    run_main()

if __name__ == "__main__":
    main()
