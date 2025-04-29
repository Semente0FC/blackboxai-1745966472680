"""
Professional logging system for Future MT5 Pro Trading
Handles both UI and file logging with color coding and formatting
"""

import tkinter as tk
from datetime import datetime
import os
import sys
import logging
from typing import Optional, Dict, Any
import json

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import configuration
try:
    from config import config
    from constants import LOGGING, PATHS
except ImportError:
    # Fallback values if import fails
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
    PATHS = {
        'LOGS': 'logs/'
    }

class TradingLogger:
    def __init__(self):
        self.log_widgets: Dict[str, tk.Text] = {}
        self.file_loggers: Dict[str, logging.Logger] = {}
        self.setup_log_directory()
        
    def setup_log_directory(self):
        """Create logs directory if it doesn't exist"""
        os.makedirs(PATHS['LOGS'], exist_ok=True)
        
    def add_log_widget(self, asset_id: str, text_widget: tk.Text):
        """Add a text widget for a specific asset"""
        self.log_widgets[asset_id] = text_widget
        self.setup_widget_tags(text_widget)
        self.setup_file_logger(asset_id)
        
    def setup_widget_tags(self, widget: tk.Text):
        """Setup color tags for the text widget"""
        widget.tag_configure('success', foreground=config.COLORS['SUCCESS'])
        widget.tag_configure('warning', foreground=config.COLORS['WARNING'])
        widget.tag_configure('error', foreground=config.COLORS['DANGER'])
        widget.tag_configure('info', foreground=config.COLORS['TEXT_SECONDARY'])
        widget.tag_configure('header', foreground=config.COLORS['ACCENT'])
        
    def setup_file_logger(self, asset_id: str):
        """Setup file logger for an asset"""
        logger = logging.getLogger(f"trading_{asset_id}")
        logger.setLevel(logging.DEBUG)
        
        # Create file handler
        log_file = os.path.join(
            PATHS['LOGS'],
            f"{asset_id}_{datetime.now().strftime(LOGGING['FILE_FORMAT'])}.log"
        )
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt=LOGGING['TIMESTAMP_FORMAT']
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        self.file_loggers[asset_id] = logger
        
    def get_message_type(self, message: str) -> str:
        """Determine message type and corresponding color tag"""
        if any(x in message for x in ['✅', 'SUCESSO', '🎯 SINAL']):
            return 'success'
        elif any(x in message for x in ['⚠️', 'AVISO', '⏳']):
            return 'warning'
        elif any(x in message for x in ['❌', 'ERRO']):
            return 'error'
        elif any(x in message for x in ['===', '📊', '📈']):
            return 'header'
        return 'info'
        
    def log(self, message: str, asset_id: Optional[str] = None, level: str = 'INFO'):
        """Log a message to UI and file"""
        timestamp = datetime.now().strftime(LOGGING['TIMESTAMP_FORMAT'])
        formatted_message = f"[{timestamp}] {message}\n"
        msg_type = self.get_message_type(message)
        
        # Log to UI
        if asset_id and asset_id in self.log_widgets:
            widget = self.log_widgets[asset_id]
            widget.insert('end', formatted_message, msg_type)
            if LOGGING['AUTO_SCROLL']:
                widget.see('end')
                
            # Limit log size
            if float(widget.index('end')) > LOGGING['MAX_LINES']:
                widget.delete('1.0', f"{LOGGING['MAX_LINES'] // 2}.0")
        elif not asset_id:
            # Log to all widgets
            for widget in self.log_widgets.values():
                widget.insert('end', formatted_message, msg_type)
                if LOGGING['AUTO_SCROLL']:
                    widget.see('end')
                    
                # Limit log size
                if float(widget.index('end')) > LOGGING['MAX_LINES']:
                    widget.delete('1.0', f"{LOGGING['MAX_LINES'] // 2}.0")
                    
        # Log to file
        if asset_id and asset_id in self.file_loggers:
            logger = self.file_loggers[asset_id]
            log_level = LOGGING['LEVELS'].get(level.upper(), LOGGING['LEVELS']['INFO'])
            logger.log(log_level, message)
            
    def clear_logs(self, asset_id: Optional[str] = None):
        """Clear logs for specific asset or all assets"""
        if asset_id and asset_id in self.log_widgets:
            self.log_widgets[asset_id].delete('1.0', 'end')
        elif not asset_id:
            for widget in self.log_widgets.values():
                widget.delete('1.0', 'end')
                
    def export_logs(self, asset_id: str, filepath: str) -> bool:
        """Export logs for an asset to JSON file"""
        if asset_id not in self.log_widgets:
            return False
            
        try:
            widget = self.log_widgets[asset_id]
            logs = widget.get('1.0', 'end').splitlines()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False
            
    def remove_log_widget(self, asset_id: str):
        """Remove a log widget"""
        if asset_id in self.log_widgets:
            del self.log_widgets[asset_id]
        if asset_id in self.file_loggers:
            del self.file_loggers[asset_id]
            
    def cleanup(self):
        """Cleanup logging system"""
        for logger in self.file_loggers.values():
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
        self.log_widgets.clear()
        self.file_loggers.clear()

# Create global logger instance
logger = TradingLogger()

# Export logger instance
__all__ = ['logger']
