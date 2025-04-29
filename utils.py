"""
Utility functions for Future MT5 Pro Trading System
"""

import MetaTrader5 as mt5
from datetime import datetime
import json
import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Try to import configuration
try:
    from config import MARKET_HOURS
except ImportError:
    MARKET_HOURS = {
        'open': {'hour': 9, 'minute': 0},
        'close': {'hour': 17, 'minute': 30}
    }

def initialize_mt5():
    """Initialize MT5 and return status and message"""
    try:
        if not mt5.initialize():
            return False, "MetaTrader 5 initialization failed"
        return True, "MetaTrader 5 initialized successfully"
    except Exception as e:
        return False, f"Error initializing MetaTrader 5: {str(e)}"

def verify_mt5_connection():
    """Verify MT5 connection and return status and message"""
    try:
        # Check if MT5 is initialized
        if not mt5.initialize():
            return False, "MetaTrader 5 is not initialized"
        
        # Check if logged in
        if not mt5.login():
            mt5.shutdown()
            return False, "Not logged in to MetaTrader 5"
        
        # Check account info
        account_info = mt5.account_info()
        if account_info is None:
            mt5.shutdown()
            return False, "Could not get account information"
        
        return True, "Connected to MetaTrader 5"
        
    except Exception as e:
        return False, f"Error checking MT5 connection: {str(e)}"

def get_account_info():
    """Get detailed account information"""
    try:
        account_info = mt5.account_info()
        if account_info is None:
            return None
            
        return {
            'login': account_info.login,
            'server': account_info.server,
            'currency': account_info.currency,
            'balance': account_info.balance,
            'equity': account_info.equity,
            'margin': account_info.margin,
            'margin_free': account_info.margin_free,
            'margin_level': account_info.margin_level,
            'profit': account_info.profit
        }
    except:
        return None

def format_currency(value, decimals=2, currency_symbol="$"):
    """Format currency value"""
    try:
        return f"{currency_symbol}{value:,.{decimals}f}"
    except:
        return f"{currency_symbol}0.00"

def check_market_hours():
    """Check if market is open"""
    current_time = datetime.now().time()
    
    # Market open time
    market_open = datetime.now().replace(
        hour=MARKET_HOURS['open']['hour'],
        minute=MARKET_HOURS['open']['minute'],
        second=0,
        microsecond=0
    ).time()
    
    # Market close time
    market_close = datetime.now().replace(
        hour=MARKET_HOURS['close']['hour'],
        minute=MARKET_HOURS['close']['minute'],
        second=0,
        microsecond=0
    ).time()
    
    return market_open <= current_time <= market_close

def save_credentials(login, server, remember=False):
    """Save login credentials if remember me is checked"""
    if not remember:
        return
        
    try:
        credentials = {
            'login': login,
            'server': server
        }
        
        with open('credentials.json', 'w') as f:
            json.dump(credentials, f)
    except:
        pass

def load_credentials():
    """Load saved credentials"""
    try:
        if not os.path.exists('credentials.json'):
            return None
            
        with open('credentials.json', 'r') as f:
            return json.load(f)
    except:
        return None

def clear_credentials():
    """Clear saved credentials"""
    try:
        if os.path.exists('credentials.json'):
            os.remove('credentials.json')
    except:
        pass

def get_symbol_info(symbol):
    """Get detailed symbol information"""
    try:
        info = mt5.symbol_info(symbol)
        if info is None:
            return None
            
        return {
            'name': info.name,
            'description': info.description,
            'currency_base': info.currency_base,
            'currency_profit': info.currency_profit,
            'digits': info.digits,
            'point': info.point,
            'tick_size': info.trade_tick_size,
            'contract_size': info.trade_contract_size,
            'volume_min': info.volume_min,
            'volume_max': info.volume_max,
            'volume_step': info.volume_step
        }
    except:
        return None

def calculate_position_size(account_balance, risk_percent, stop_loss_points, symbol):
    """Calculate position size based on risk parameters"""
    try:
        # Get symbol information
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return 0.0
            
        # Calculate risk amount
        risk_amount = account_balance * (risk_percent / 100)
        
        # Calculate position size
        point_value = symbol_info.trade_tick_value * (stop_loss_points / symbol_info.point)
        if point_value == 0:
            return 0.0
            
        position_size = risk_amount / point_value
        
        # Round to valid lot size
        position_size = round(position_size / symbol_info.volume_step) * symbol_info.volume_step
        
        # Ensure within limits
        position_size = max(symbol_info.volume_min, min(position_size, symbol_info.volume_max))
        
        return position_size
    except:
        return 0.0

def format_error_message(error_code):
    """Format MT5 error code into readable message"""
    error_messages = {
        mt5.RES_S_OK: "Success",
        mt5.RES_E_FAIL: "General error",
        mt5.RES_E_INVALID_PARAMS: "Invalid parameters",
        mt5.RES_E_NO_MEMORY: "No memory",
        mt5.RES_E_NOT_FOUND: "Not found",
        mt5.RES_E_INVALID_VERSION: "Invalid version",
        mt5.RES_E_AUTH_FAILED: "Authorization failed",
        mt5.RES_E_UNSUPPORTED: "Unsupported method",
        mt5.RES_E_AUTO_TRADING_DISABLED: "AutoTrading disabled",
        mt5.RES_E_INTERNAL_FAIL: "Internal error",
        mt5.RES_E_MARKET_CLOSED: "Market closed",
        mt5.RES_E_TRADE_DISABLED: "Trade disabled",
        mt5.RES_E_INVALID_PRICE: "Invalid price",
        mt5.RES_E_INVALID_STOPS: "Invalid stops",
        mt5.RES_E_INVALID_VOLUME: "Invalid volume",
        mt5.RES_E_TICK_PROCESSING: "Tick processing error"
    }
    
    return error_messages.get(error_code, f"Unknown error ({error_code})")

def log_trade_result(result):
    """Log trade execution result"""
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return False, format_error_message(result.retcode)
    
    return True, "Trade executed successfully"

def cleanup_mt5():
    """Safely cleanup MT5 connection"""
    try:
        mt5.shutdown()
    except:
        pass
