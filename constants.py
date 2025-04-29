"""
Constants for Future MT5 Pro Trading System
"""

# System Information
SYSTEM = {
    'NAME': 'Future MT5 Pro Trading',
    'VERSION': '2.0.0',
    'AUTHOR': 'BLACKBOXAI',
    'DESCRIPTION': 'Professional Fibonacci Trading System',
    'WEBSITE': 'www.blackboxai.com',
    'SUPPORT_EMAIL': 'support@blackboxai.com'
}

# File Paths
PATHS = {
    'CREDENTIALS': 'credentials.json',
    'LOGS': 'logs/',
    'DATA': 'data/',
    'CONFIG': 'config/'
}

# Error Messages
ERRORS = {
    'MT5_NOT_INITIALIZED': 'MetaTrader 5 is not initialized',
    'MT5_NOT_CONNECTED': 'Not connected to MetaTrader 5',
    'MT5_LOGIN_FAILED': 'Login to MetaTrader 5 failed',
    'MT5_NO_ACCOUNT': 'Could not get account information',
    'INVALID_SYMBOL': 'Invalid trading symbol',
    'INVALID_TIMEFRAME': 'Invalid timeframe',
    'INVALID_VOLUME': 'Invalid trading volume',
    'MARKET_CLOSED': 'Market is closed',
    'INSUFFICIENT_MARGIN': 'Insufficient margin for trade',
    'INVALID_STOPS': 'Invalid stop loss or take profit levels',
    'TRADE_DISABLED': 'Trading is disabled',
    'CONFIG_ERROR': 'Configuration error',
    'SYSTEM_ERROR': 'System error occurred'
}

# Success Messages
SUCCESS = {
    'MT5_INITIALIZED': 'MetaTrader 5 initialized successfully',
    'MT5_CONNECTED': 'Connected to MetaTrader 5',
    'LOGIN_SUCCESS': 'Login successful',
    'TRADE_EXECUTED': 'Trade executed successfully',
    'POSITION_CLOSED': 'Position closed successfully',
    'ORDER_PLACED': 'Order placed successfully',
    'ORDER_MODIFIED': 'Order modified successfully',
    'ORDER_CANCELLED': 'Order cancelled successfully'
}

# Warning Messages
WARNINGS = {
    'MARKET_CLOSING': 'Market closing soon',
    'HIGH_SPREAD': 'High spread detected',
    'LOW_MARGIN': 'Low margin level',
    'MAX_POSITIONS': 'Maximum positions reached',
    'RISK_LIMIT': 'Risk limit reached',
    'INVALID_RISK': 'Invalid risk parameters'
}

# Trading Constants
TRADING = {
    'DEFAULT_STOP_LOSS': 50,  # points
    'DEFAULT_TAKE_PROFIT': 100,  # points
    'MAX_SPREAD': 50,  # maximum allowed spread
    'MIN_VOLUME': 0.01,  # minimum trading volume
    'MAX_VOLUME': 100.0,  # maximum trading volume
    'VOLUME_STEP': 0.01,  # volume step
    'MAX_SLIPPAGE': 10,  # maximum allowed slippage
    'MAX_POSITIONS': 5,  # maximum open positions
    'RISK_PERCENT': 2.0,  # risk per trade (%)
    'MIN_RR_RATIO': 1.5,  # minimum risk/reward ratio
    'TRAILING_STOP': 30,  # trailing stop points
    'BREAK_EVEN': 20  # break even points
}

# Timeframes
TIMEFRAMES = {
    'M1': 'One Minute',
    'M5': 'Five Minutes',
    'M15': 'Fifteen Minutes',
    'M30': 'Thirty Minutes',
    'H1': 'One Hour',
    'H4': 'Four Hours',
    'D1': 'One Day'
}

# Technical Analysis
ANALYSIS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MA_FAST': 9,
    'MA_MEDIUM': 21,
    'MA_SLOW': 50,
    'MA_TREND': 200,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_DEVIATION': 2.0,
    'ATR_PERIOD': 14,
    'VOLUME_MA': 20
}

# Fibonacci Levels
FIBONACCI = {
    'PERIOD': 20,
    'MIN_TREND': 2.0,  # minimum trend percentage
    'RETRACEMENT': [0.236, 0.382, 0.5, 0.618, 0.786],
    'EXTENSION': [1.272, 1.618, 2.0, 2.618],
    'REVERSAL_ZONE': 0.1  # percentage zone around levels
}

# Market Hours (Brazil)
MARKET_HOURS = {
    'OPEN': {
        'HOUR': 9,
        'MINUTE': 0
    },
    'CLOSE': {
        'HOUR': 17,
        'MINUTE': 30
    },
    'PRE_MARKET': {
        'HOUR': 8,
        'MINUTE': 45
    },
    'POST_MARKET': {
        'HOUR': 17,
        'MINUTE': 45
    }
}

# UI Constants
UI = {
    'COLORS': {
        'BG_DARK': '#0A0E17',
        'BG_MEDIUM': '#151B28',
        'BG_LIGHT': '#1E2738',
        'ACCENT': '#00B8D4',
        'ACCENT_HOVER': '#00E5FF',
        'SUCCESS': '#00BFA5',
        'WARNING': '#FFB300',
        'DANGER': '#FF3D00',
        'TEXT': '#FFFFFF',
        'TEXT_SECONDARY': '#B0BEC5'
    },
    'FONTS': {
        'FAMILY': 'Helvetica',
        'SIZES': {
            'TITLE': 24,
            'SUBTITLE': 16,
            'NORMAL': 12,
            'SMALL': 10
        }
    },
    'WINDOW': {
        'WIDTH': 1200,
        'HEIGHT': 800,
        'MIN_WIDTH': 800,
        'MIN_HEIGHT': 600
    },
    'PADDING': {
        'SMALL': 5,
        'MEDIUM': 10,
        'LARGE': 20
    }
}

# Logging Configuration
LOGGING = {
    'MAX_LINES': 1000,
    'AUTO_SCROLL': True,
    'TIMESTAMP_FORMAT': '%H:%M:%S.%f',
    'FILE_FORMAT': '%Y%m%d',
    'LEVELS': {
        'DEBUG': 10,
        'INFO': 20,
        'WARNING': 30,
        'ERROR': 40,
        'CRITICAL': 50
    }
}

# Ensure all constants are exported
__all__ = [
    'SYSTEM',
    'PATHS',
    'ERRORS',
    'SUCCESS',
    'WARNINGS',
    'TRADING',
    'TIMEFRAMES',
    'ANALYSIS',
    'FIBONACCI',
    'MARKET_HOURS',
    'UI',
    'LOGGING'
]
