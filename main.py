"""
Main entry point for Future MT5 Pro Trading System
"""

import tkinter as tk
from tkinter import messagebox
import MetaTrader5 as mt5
import sys
import traceback
import os
from typing import Tuple

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import local modules
try:
    from config import config
    from logger import logger
    from splash import show_splash
    from login_window import show_login
    from trading_app import TradingApp
    from utils import initialize_mt5, get_account_info, format_currency
except ImportError as e:
    print(f"\n❌ Error importing modules: {str(e)}")
    print("Please ensure all required files are in the same directory.")
    sys.exit(1)

def handle_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions"""
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    messagebox.showerror(
        "Error",
        f"An unexpected error occurred:\n\n{str(exc_value)}\n\nPlease check the logs for details."
    )
    logger.log(f"Uncaught exception:\n{error_msg}", level='ERROR')
    sys.exit(1)

def setup_mt5() -> Tuple[bool, str]:
    """Initialize MT5 and verify connection"""
    success, message = initialize_mt5()
    if not success:
        return False, message
        
    # Show login window if needed
    if not show_login():
        return False, "Login failed or cancelled"
        
    # Get account info
    account_info = get_account_info()
    if not account_info:
        return False, "Could not get account information"
        
    # Log success
    logger.log("✅ Successfully connected to MetaTrader 5")
    logger.log(f"📊 Account: {account_info['login']}")
    logger.log(f"🏢 Server: {account_info['server']}")
    logger.log(f"💰 Balance: {format_currency(account_info['balance'])}")
    logger.log(f"📈 Equity: {format_currency(account_info['equity'])}")
    
    return True, "Connected successfully"

def main():
    """Main application entry point"""
    # Set exception handler
    sys.excepthook = handle_exception
    
    print(f"\n=== {config.APP_NAME} v{config.VERSION} ===")
    print(f"Developed by {config.AUTHOR}")
    print("\nInitializing system...")
    
    try:
        # Show splash screen
        show_splash()
        
        # Setup MT5
        success, message = setup_mt5()
        if not success:
            print(f"\n❌ {message}")
            sys.exit(1)
        
        # Create and run main application
        print("\n🚀 Launching trading interface...")
        root = tk.Tk()
        app = TradingApp(root)
        root.mainloop()
        
    except Exception as e:
        error_msg = f"Failed to start the application:\n\n{str(e)}"
        messagebox.showerror("Startup Error", error_msg)
        logger.log(error_msg, level='ERROR')
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        # Cleanup
        print("\n👋 Shutting down...")
        mt5.shutdown()
        logger.cleanup()
        print("✅ Connection closed")

if __name__ == "__main__":
    main()
