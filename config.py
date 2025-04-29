"""
Configuration file for Future MT5 Pro Trading System
Imports constants and allows for user customization
"""

import os
import sys
import json
from typing import Dict, Any

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import constants
from constants import (
    SYSTEM, TRADING, FIBONACCI, ANALYSIS,
    MARKET_HOURS, UI, LOGGING
)

class Config:
    def __init__(self):
        # System Information
        self.APP_NAME = SYSTEM['NAME']
        self.VERSION = SYSTEM['VERSION']
        self.AUTHOR = SYSTEM['AUTHOR']
        
        # Load user configuration if exists
        self.user_config = self.load_user_config()
        
        # Initialize configuration
        self.init_config()
        
    def load_user_config(self) -> Dict[str, Any]:
        """Load user configuration from file"""
        config_path = os.path.join(current_dir, 'user_config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                print("Warning: Could not load user configuration")
        return {}
        
    def init_config(self):
        """Initialize configuration with user overrides"""
        # Trading Parameters
        self.TRADING = self.override_config('trading', TRADING)
        
        # Fibonacci Settings
        self.FIBONACCI = self.override_config('fibonacci', FIBONACCI)
        
        # Technical Analysis
        self.ANALYSIS = self.override_config('analysis', ANALYSIS)
        
        # Market Hours
        self.MARKET_HOURS = self.override_config('market_hours', MARKET_HOURS)
        
        # UI Settings
        self.UI = self.override_config('ui', UI)
        
        # Logging
        self.LOGGING = self.override_config('logging', LOGGING)
        
        # Colors (commonly used, so separate for easy access)
        self.COLORS = self.UI['COLORS']
        
    def override_config(self, section: str, defaults: Dict) -> Dict:
        """Override default configuration with user settings"""
        if section in self.user_config:
            return {**defaults, **self.user_config[section]}
        return defaults
        
    def save_user_config(self):
        """Save current configuration as user config"""
        config = {
            'trading': self.TRADING,
            'fibonacci': self.FIBONACCI,
            'analysis': self.ANALYSIS,
            'market_hours': self.MARKET_HOURS,
            'ui': self.UI,
            'logging': self.LOGGING
        }
        
        config_path = os.path.join(current_dir, 'user_config.json')
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except:
            return False
            
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        self.user_config = {}
        self.init_config()
        
    def update_section(self, section: str, values: Dict):
        """Update a configuration section"""
        if hasattr(self, section.upper()):
            current = getattr(self, section.upper())
            if isinstance(current, dict):
                setattr(self, section.upper(), {**current, **values})
                
    def get_section(self, section: str) -> Dict:
        """Get a configuration section"""
        return getattr(self, section.upper(), {})

# Create global configuration instance
config = Config()

# Export commonly used values
APP_NAME = config.APP_NAME
VERSION = config.VERSION
AUTHOR = config.AUTHOR
COLORS = config.COLORS

# Export configuration instance
__all__ = ['config', 'APP_NAME', 'VERSION', 'AUTHOR', 'COLORS']
