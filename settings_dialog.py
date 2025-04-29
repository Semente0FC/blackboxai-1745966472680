"""
Settings dialog for Future MT5 Pro Trading System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional

from config import config
from logger import logger

class SettingsDialog:
    def __init__(self, parent: tk.Tk):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configure window
        self.dialog.configure(bg=config.COLORS['bg_dark'])
        self.dialog.resizable(False, False)
        
        # Center dialog
        width = 600
        height = 700
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Store original values
        self.original_values = {
            'trading': dict(config.TRADING),
            'fibonacci': dict(config.FIBONACCI),
            'analysis': dict(config.ANALYSIS),
            'market_hours': dict(config.MARKET_HOURS)
        }
        
        # Variables for settings
        self.variables = self.create_variables()
        
        self.setup_ui()
        
    def create_variables(self) -> Dict[str, Dict[str, tk.Variable]]:
        """Create variables for all settings"""
        variables = {
            'trading': {},
            'fibonacci': {},
            'analysis': {},
            'market_hours': {}
        }
        
        # Trading variables
        for key, value in config.TRADING.items():
            if isinstance(value, bool):
                variables['trading'][key] = tk.BooleanVar(value=value)
            elif isinstance(value, (int, float)):
                variables['trading'][key] = tk.DoubleVar(value=value)
            else:
                variables['trading'][key] = tk.StringVar(value=str(value))
                
        # Fibonacci variables
        for key, value in config.FIBONACCI.items():
            if isinstance(value, (int, float)):
                variables['fibonacci'][key] = tk.DoubleVar(value=value)
            else:
                variables['fibonacci'][key] = tk.StringVar(value=str(value))
                
        # Analysis variables
        for key, value in config.ANALYSIS.items():
            if isinstance(value, (int, float)):
                variables['analysis'][key] = tk.DoubleVar(value=value)
            else:
                variables['analysis'][key] = tk.StringVar(value=str(value))
                
        # Market hours variables
        for key, value in config.MARKET_HOURS.items():
            if isinstance(value, dict):
                variables['market_hours'][key] = {
                    'hour': tk.IntVar(value=value['HOUR']),
                    'minute': tk.IntVar(value=value['MINUTE'])
                }
                
        return variables
        
    def setup_ui(self):
        """Setup the settings dialog UI"""
        # Main container
        main_frame = tk.Frame(
            self.dialog,
            bg=config.COLORS['bg_dark'],
            highlightbackground=config.COLORS['accent'],
            highlightthickness=1
        )
        main_frame.pack(expand=True, fill="both", padx=2, pady=2)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Trading tab
        trading_frame = self.create_trading_tab()
        notebook.add(trading_frame, text="Trading")
        
        # Fibonacci tab
        fibonacci_frame = self.create_fibonacci_tab()
        notebook.add(fibonacci_frame, text="Fibonacci")
        
        # Analysis tab
        analysis_frame = self.create_analysis_tab()
        notebook.add(analysis_frame, text="Analysis")
        
        # Market Hours tab
        market_frame = self.create_market_tab()
        notebook.add(market_frame, text="Market Hours")
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=config.COLORS['bg_dark'])
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Save button
        save_btn = tk.Button(
            button_frame,
            text="Save",
            command=self.save_settings,
            bg=config.COLORS['success'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10, "bold"),
            width=10,
            cursor="hand2"
        )
        save_btn.pack(side="right", padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            bg=config.COLORS['danger'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10, "bold"),
            width=10,
            cursor="hand2"
        )
        cancel_btn.pack(side="right", padx=5)
        
        # Reset button
        reset_btn = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_settings,
            bg=config.COLORS['warning'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10, "bold"),
            width=10,
            cursor="hand2"
        )
        reset_btn.pack(side="left", padx=5)
        
    def create_trading_tab(self) -> tk.Frame:
        """Create trading settings tab"""
        frame = tk.Frame(bg=config.COLORS['bg_medium'])
        
        # Risk Management
        risk_frame = tk.LabelFrame(
            frame,
            text=" Risk Management ",
            bg=config.COLORS['bg_medium'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10, "bold")
        )
        risk_frame.pack(fill="x", padx=10, pady=5)
        
        self.create_setting_row(
            risk_frame, "Risk per Trade (%)",
            self.variables['trading']['risk_percent']
        )
        self.create_setting_row(
            risk_frame, "Max Positions",
            self.variables['trading']['max_positions']
        )
        self.create_setting_row(
            risk_frame, "Min R/R Ratio",
            self.variables['trading']['min_rr_ratio']
        )
        
        # Trade Parameters
        trade_frame = tk.LabelFrame(
            frame,
            text=" Trade Parameters ",
            bg=config.COLORS['bg_medium'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10, "bold")
        )
        trade_frame.pack(fill="x", padx=10, pady=5)
        
        self.create_setting_row(
            trade_frame, "Default Lot Size",
            self.variables['trading']['default_lot']
        )
        self.create_setting_row(
            trade_frame, "Max Spread (points)",
            self.variables['trading']['max_spread']
        )
        
        return frame
        
    def create_fibonacci_tab(self) -> tk.Frame:
        """Create Fibonacci settings tab"""
        frame = tk.Frame(bg=config.COLORS['bg_medium'])
        
        # Analysis Parameters
        analysis_frame = tk.LabelFrame(
            frame,
            text=" Analysis Parameters ",
            bg=config.COLORS['bg_medium'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10, "bold")
        )
        analysis_frame.pack(fill="x", padx=10, pady=5)
        
        self.create_setting_row(
            analysis_frame, "Analysis Period",
            self.variables['fibonacci']['period']
        )
        self.create_setting_row(
            analysis_frame, "Min Trend (%)",
            self.variables['fibonacci']['min_trend']
        )
        
        return frame
        
    def create_analysis_tab(self) -> tk.Frame:
        """Create technical analysis settings tab"""
        frame = tk.Frame(bg=config.COLORS['bg_medium'])
        
        # RSI Settings
        rsi_frame = tk.LabelFrame(
            frame,
            text=" RSI Settings ",
            bg=config.COLORS['bg_medium'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10, "bold")
        )
        rsi_frame.pack(fill="x", padx=10, pady=5)
        
        self.create_setting_row(
            rsi_frame, "RSI Period",
            self.variables['analysis']['rsi_period']
        )
        self.create_setting_row(
            rsi_frame, "Overbought Level",
            self.variables['analysis']['rsi_overbought']
        )
        self.create_setting_row(
            rsi_frame, "Oversold Level",
            self.variables['analysis']['rsi_oversold']
        )
        
        return frame
        
    def create_market_tab(self) -> tk.Frame:
        """Create market hours settings tab"""
        frame = tk.Frame(bg=config.COLORS['bg_medium'])
        
        # Market Hours
        hours_frame = tk.LabelFrame(
            frame,
            text=" Market Hours ",
            bg=config.COLORS['bg_medium'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10, "bold")
        )
        hours_frame.pack(fill="x", padx=10, pady=5)
        
        # Market Open
        open_frame = tk.Frame(hours_frame, bg=config.COLORS['bg_medium'])
        open_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(
            open_frame,
            text="Market Open:",
            bg=config.COLORS['bg_medium'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10)
        ).pack(side="left")
        
        ttk.Spinbox(
            open_frame,
            from_=0,
            to=23,
            width=5,
            textvariable=self.variables['market_hours']['open']['hour']
        ).pack(side="left", padx=5)
        
        ttk.Spinbox(
            open_frame,
            from_=0,
            to=59,
            width=5,
            textvariable=self.variables['market_hours']['open']['minute']
        ).pack(side="left")
        
        # Market Close
        close_frame = tk.Frame(hours_frame, bg=config.COLORS['bg_medium'])
        close_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(
            close_frame,
            text="Market Close:",
            bg=config.COLORS['bg_medium'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10)
        ).pack(side="left")
        
        ttk.Spinbox(
            close_frame,
            from_=0,
            to=23,
            width=5,
            textvariable=self.variables['market_hours']['close']['hour']
        ).pack(side="left", padx=5)
        
        ttk.Spinbox(
            close_frame,
            from_=0,
            to=59,
            width=5,
            textvariable=self.variables['market_hours']['close']['minute']
        ).pack(side="left")
        
        return frame
        
    def create_setting_row(self, parent: tk.Widget, label: str, variable: tk.Variable):
        """Create a row for a setting"""
        frame = tk.Frame(parent, bg=config.COLORS['bg_medium'])
        frame.pack(fill="x", padx=10, pady=2)
        
        tk.Label(
            frame,
            text=label,
            bg=config.COLORS['bg_medium'],
            fg=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], 10)
        ).pack(side="left")
        
        if isinstance(variable, tk.BooleanVar):
            ttk.Checkbutton(
                frame,
                variable=variable
            ).pack(side="right")
        else:
            ttk.Entry(
                frame,
                textvariable=variable,
                width=10
            ).pack(side="right")
            
    def save_settings(self):
        """Save settings to configuration"""
        try:
            # Update trading settings
            new_trading = {}
            for key, var in self.variables['trading'].items():
                new_trading[key] = var.get()
            config.update_section('trading', new_trading)
            
            # Update fibonacci settings
            new_fibonacci = {}
            for key, var in self.variables['fibonacci'].items():
                new_fibonacci[key] = var.get()
            config.update_section('fibonacci', new_fibonacci)
            
            # Update analysis settings
            new_analysis = {}
            for key, var in self.variables['analysis'].items():
                new_analysis[key] = var.get()
            config.update_section('analysis', new_analysis)
            
            # Update market hours
            new_hours = {
                'OPEN': {
                    'HOUR': self.variables['market_hours']['open']['hour'].get(),
                    'MINUTE': self.variables['market_hours']['open']['minute'].get()
                },
                'CLOSE': {
                    'HOUR': self.variables['market_hours']['close']['hour'].get(),
                    'MINUTE': self.variables['market_hours']['close']['minute'].get()
                }
            }
            config.update_section('market_hours', new_hours)
            
            # Save to file
            if config.save_user_config():
                messagebox.showinfo("Success", "Settings saved successfully!")
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to save settings!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving settings: {str(e)}")
            
    def reset_settings(self):
        """Reset settings to original values"""
        if messagebox.askyesno("Reset", "Reset all settings to default values?"):
            config.reset_to_defaults()
            self.dialog.destroy()

def show_settings(parent: tk.Tk):
    """Show settings dialog"""
    dialog = SettingsDialog(parent)
    return dialog
