"""
Main trading interface for Future MT5 Pro Trading System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import MetaTrader5 as mt5
from datetime import datetime
import threading
import time
from typing import Dict, Any, Optional

# Import local modules
from config import config
from logger import logger
from utils import (
    get_account_info, format_currency, check_market_hours,
    get_symbol_info, calculate_position_size
)
from estrategia import EstrategiaTrading

class TradingApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{config.APP_NAME} v{config.VERSION} - Fibonacci Trading")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configure window
        self.root.configure(bg=config.COLORS['bg_dark'])
        self.setup_window_size()

        # Trading variables
        self.ativo_selecionado = tk.StringVar()
        self.timeframe_selecionado = tk.StringVar(value=config.TRADING['default_timeframe'])
        self.lote_selecionado = tk.StringVar(value=str(config.TRADING['default_lot']))
        
        # State variables
        self.operando = False
        self.estrategia = None
        
        # Setup UI
        self.setup_ui()
        self.start_update_threads()

    def setup_window_size(self):
        """Configure window size and position"""
        width = config.UI['WINDOW']['WIDTH']
        height = config.UI['WINDOW']['HEIGHT']
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(
            config.UI['WINDOW']['MIN_WIDTH'],
            config.UI['WINDOW']['MIN_HEIGHT']
        )

    def setup_ui(self):
        """Setup the main user interface"""
        self.setup_menu()
        
        # Main container with gradient border effect
        main_container = tk.Frame(
            self.root,
            bg=config.COLORS['bg_dark'],
            highlightbackground=config.COLORS['accent'],
            highlightthickness=1
        )
        main_container.pack(expand=True, fill="both", padx=2, pady=2)

        # Header
        self.setup_header(main_container)
        
        # Content area
        content = tk.Frame(main_container, bg=config.COLORS['bg_dark'])
        content.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Split into left and right panels
        left_panel = self.setup_left_panel(content)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_panel = self.setup_right_panel(content)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Status bar
        self.setup_status_bar(main_container)

    def setup_menu(self):
        """Setup the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Clear Logs", command=self.clear_logs)
        view_menu.add_command(label="Export Logs", command=self.export_logs)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def setup_header(self, parent: tk.Widget):
        """Setup the header section"""
        header = tk.Frame(parent, bg=config.COLORS['bg_dark'], height=80)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)

        # Left side - Title
        title_frame = tk.Frame(header, bg=config.COLORS['bg_dark'])
        title_frame.pack(side="left")

        tk.Label(
            title_frame,
            text="FIBONACCI TRADER",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['TITLE'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_dark']
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Professional Trading System",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SUBTITLE']),
            fg=config.COLORS['text_secondary'],
            bg=config.COLORS['bg_dark']
        ).pack(anchor="w")

        # Right side - Account info
        account_frame = tk.Frame(header, bg=config.COLORS['bg_dark'])
        account_frame.pack(side="right")

        # Balance
        balance_frame = tk.Frame(account_frame, bg=config.COLORS['bg_medium'], padx=15, pady=10)
        balance_frame.pack(side="left", padx=5)

        tk.Label(
            balance_frame,
            text="BALANCE",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text_secondary'],
            bg=config.COLORS['bg_medium']
        ).pack()

        self.balance_label = tk.Label(
            balance_frame,
            text="$0.00",
            font=(config.UI['FONTS']['FAMILY'], 16, "bold"),
            fg=config.COLORS['accent'],
            bg=config.COLORS['bg_medium']
        )
        self.balance_label.pack()

        # Equity
        equity_frame = tk.Frame(account_frame, bg=config.COLORS['bg_medium'], padx=15, pady=10)
        equity_frame.pack(side="left", padx=5)

        tk.Label(
            equity_frame,
            text="EQUITY",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text_secondary'],
            bg=config.COLORS['bg_medium']
        ).pack()

        self.equity_label = tk.Label(
            equity_frame,
            text="$0.00",
            font=(config.UI['FONTS']['FAMILY'], 16, "bold"),
            fg=config.COLORS['success'],
            bg=config.COLORS['bg_medium']
        )
        self.equity_label.pack()

    def setup_left_panel(self, parent: tk.Widget):
        """Setup the left panel with trading controls"""
        panel = tk.Frame(parent, bg=config.COLORS['bg_medium'])
        
        # Trading Controls
        controls = tk.LabelFrame(
            panel,
            text=" Trading Controls ",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_medium']
        )
        controls.pack(fill="x", padx=10, pady=10)

        # Grid for controls
        control_grid = tk.Frame(controls, bg=config.COLORS['bg_medium'])
        control_grid.pack(padx=20, pady=20)

        # Asset Selection
        tk.Label(
            control_grid,
            text="Asset",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_medium']
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.combo_ativo = ttk.Combobox(
            control_grid,
            textvariable=self.ativo_selecionado,
            width=15
        )
        self.combo_ativo.grid(row=1, column=0, padx=(0, 10))

        # Timeframe Selection
        tk.Label(
            control_grid,
            text="Timeframe",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_medium']
        ).grid(row=0, column=1, sticky="w", pady=(0, 5))

        self.combo_timeframe = ttk.Combobox(
            control_grid,
            textvariable=self.timeframe_selecionado,
            values=config.TRADING['timeframes'],
            width=10
        )
        self.combo_timeframe.grid(row=1, column=1, padx=10)

        # Lot Size
        tk.Label(
            control_grid,
            text="Lot Size",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_medium']
        ).grid(row=0, column=2, sticky="w", pady=(0, 5))

        self.entry_lote = ttk.Entry(
            control_grid,
            textvariable=self.lote_selecionado,
            width=10
        )
        self.entry_lote.grid(row=1, column=2, padx=10)

        # Control Buttons
        button_frame = tk.Frame(control_grid, bg=config.COLORS['bg_medium'])
        button_frame.grid(row=1, column=3, padx=(10, 0))

        self.btn_iniciar = tk.Button(
            button_frame,
            text="▶ START",
            command=self.iniciar_robo,
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['accent'],
            activebackground=config.COLORS['accent_hover'],
            relief="flat",
            cursor="hand2",
            width=12,
            height=1
        )
        self.btn_iniciar.pack(side="left", padx=2)

        self.btn_parar = tk.Button(
            button_frame,
            text="⏹ STOP",
            command=self.parar_robo,
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['danger'],
            activebackground=config.COLORS['danger'],
            relief="flat",
            cursor="hand2",
            width=12,
            height=1,
            state="disabled"
        )
        self.btn_parar.pack(side="left", padx=2)

        # Log Area
        log_frame = tk.LabelFrame(
            panel,
            text=" Trading Log ",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_medium']
        )
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_log = tk.Text(
            log_frame,
            height=20,
            width=60,
            bg=config.COLORS['bg_dark'],
            fg=config.COLORS['text'],
            font=("Consolas", config.UI['FONTS']['SIZES']['NORMAL']),
            padx=10,
            pady=10
        )
        self.text_log.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(log_frame, command=self.text_log.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        self.text_log.config(yscrollcommand=scrollbar.set)

        # Add log widget to logger
        logger.add_log_widget("main", self.text_log)

        return panel

    def setup_right_panel(self, parent: tk.Widget):
        """Setup the right panel with market analysis"""
        panel = tk.Frame(parent, bg=config.COLORS['bg_medium'])
        
        # Market Analysis
        analysis = tk.LabelFrame(
            panel,
            text=" Market Analysis ",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_medium']
        )
        analysis.pack(fill="both", expand=True, padx=10, pady=10)

        # Fibonacci Levels
        fib_frame = tk.LabelFrame(
            analysis,
            text=" Fibonacci Levels ",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_medium']
        )
        fib_frame.pack(fill="x", padx=10, pady=10)

        self.fib_labels = {}
        for level in config.FIBONACCI['RETRACEMENT']:
            frame = tk.Frame(fib_frame, bg=config.COLORS['bg_medium'])
            frame.pack(fill="x", padx=10, pady=2)
            
            tk.Label(
                frame,
                text=f"{level*100:.1f}%",
                font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL']),
                fg=config.COLORS['text_secondary'],
                bg=config.COLORS['bg_medium'],
                width=8
            ).pack(side="left")
            
            self.fib_labels[level] = tk.Label(
                frame,
                text="0.00000",
                font=("Consolas", config.UI['FONTS']['SIZES']['NORMAL']),
                fg=config.COLORS['text'],
                bg=config.COLORS['bg_medium']
            )
            self.fib_labels[level].pack(side="right")

        # Market Status
        status_frame = tk.LabelFrame(
            analysis,
            text=" Market Status ",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_medium']
        )
        status_frame.pack(fill="x", padx=10, pady=10)

        # Trend
        trend_frame = tk.Frame(status_frame, bg=config.COLORS['bg_medium'])
        trend_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(
            trend_frame,
            text="Trend:",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL']),
            fg=config.COLORS['text_secondary'],
            bg=config.COLORS['bg_medium']
        ).pack(side="left")
        
        self.trend_label = tk.Label(
            trend_frame,
            text="NEUTRAL",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_medium']
        )
        self.trend_label.pack(side="right")

        # RSI
        rsi_frame = tk.Frame(status_frame, bg=config.COLORS['bg_medium'])
        rsi_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(
            rsi_frame,
            text="RSI:",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL']),
            fg=config.COLORS['text_secondary'],
            bg=config.COLORS['bg_medium']
        ).pack(side="left")
        
        self.rsi_label = tk.Label(
            rsi_frame,
            text="50.00",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'], "bold"),
            fg=config.COLORS['text'],
            bg=config.COLORS['bg_medium']
        )
        self.rsi_label.pack(side="right")

        return panel

    def setup_status_bar(self, parent: tk.Widget):
        """Setup the status bar"""
        status_bar = tk.Frame(parent, bg=config.COLORS['bg_medium'], height=25)
        status_bar.pack(fill="x", side="bottom")
        status_bar.pack_propagate(False)

        # Market Status
        self.market_status = tk.Label(
            status_bar,
            text="Market: Closed",
            font=(config.UI['FONTS']['FAMILY'], 9),
            fg=config.COLORS['text_secondary'],
            bg=config.COLORS['bg_medium']
        )
        self.market_status.pack(side="left", padx=10)

        # Connection Status
        self.connection_status = tk.Label(
            status_bar,
            text="MT5: Connected",
            font=(config.UI['FONTS']['FAMILY'], 9),
            fg=config.COLORS['success'],
            bg=config.COLORS['bg_medium']
        )
        self.connection_status.pack(side="right", padx=10)

    def start_update_threads(self):
        """Start update threads"""
        threading.Thread(target=self.update_account_info, daemon=True).start()
        threading.Thread(target=self.update_market_status, daemon=True).start()
        threading.Thread(target=self.carregar_ativos, daemon=True).start()

    def update_account_info(self):
        """Update account information"""
        while True:
            try:
                account_info = get_account_info()
                if account_info:
                    self.balance_label.config(
                        text=format_currency(account_info['balance'])
                    )
                    self.equity_label.config(
                        text=format_currency(account_info['equity'])
                    )
                    
                    # Update connection status
                    self.connection_status.config(
                        text="MT5: Connected",
                        fg=config.COLORS['success']
                    )
                else:
                    self.connection_status.config(
                        text="MT5: Disconnected",
                        fg=config.COLORS['danger']
                    )
            except:
                self.connection_status.config(
                    text="MT5: Error",
                    fg=config.COLORS['danger']
                )
            time.sleep(1)

    def update_market_status(self):
        """Update market status"""
        while True:
            is_open = check_market_hours()
            self.market_status.config(
                text=f"Market: {'Open' if is_open else 'Closed'}",
                fg=config.COLORS['success'] if is_open else config.COLORS['danger']
            )
            time.sleep(1)

    def carregar_ativos(self):
        """Load available assets"""
        try:
            symbols = mt5.symbols_get()
            lista_ativos = [symbol.name for symbol in symbols if symbol.visible]
            self.combo_ativo['values'] = lista_ativos
            if lista_ativos:
                self.combo_ativo.current(0)
            logger.log(f"✅ {len(lista_ativos)} assets loaded")
        except Exception as e:
            logger.log(f"❌ Error loading assets: {str(e)}")

    def iniciar_robo(self):
        """Start the trading robot"""
        ativo = self.ativo_selecionado.get().strip()
        timeframe = self.timeframe_selecionado.get().strip()
        lote = self.lote_selecionado.get().strip()

        if not all([ativo, timeframe, lote]):
            messagebox.showwarning("Warning", "Please fill in all fields!")
            return

        try:
            lote_float = round(float(lote), 2)
            if lote_float <= 0:
                messagebox.showerror("Error", "Lot size must be greater than zero!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid lot size!")
            return

        # Check asset
        symbol_info = get_symbol_info(ativo)
        if not symbol_info:
            messagebox.showerror("Error", f"Asset {ativo} not found!")
            return

        self.operando = True
        self.btn_iniciar.config(state="disabled")
        self.btn_parar.config(state="normal")
        self.combo_ativo.config(state="disabled")
        self.combo_timeframe.config(state="disabled")
        self.entry_lote.config(state="disabled")

        # Create and start strategy
        self.estrategia = EstrategiaTrading(ativo, timeframe, lote_float, logger)
        threading.Thread(target=self.estrategia.executar, daemon=True).start()

    def parar_robo(self):
        """Stop the trading robot"""
        if self.estrategia:
            self.estrategia.parar()
            self.estrategia = None

        self.operando = False
        self.btn_iniciar.config(state="normal")
        self.btn_parar.config(state="disabled")
        self.combo_ativo.config(state="normal")
        self.combo_timeframe.config(state="normal")
        self.entry_lote.config(state="normal")

    def show_settings(self):
        """Show settings dialog"""
        # TODO: Implement settings dialog
        pass

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            f"{config.APP_NAME} v{config.VERSION}\n\n"
            f"Developed by {config.AUTHOR}\n\n"
            "Professional Fibonacci Trading System"
        )

    def clear_logs(self):
        """Clear log area"""
        logger.clear_logs()

    def export_logs(self):
        """Export logs to file"""
        from tkinter import filedialog
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            if logger.export_logs("main", filepath):
                messagebox.showinfo("Success", "Logs exported successfully!")
            else:
                messagebox.showerror("Error", "Failed to export logs!")

    def on_closing(self):
        """Handle window closing"""
        if self.operando:
            if messagebox.askokcancel("Exit", "The robot is running. Do you really want to exit?"):
                self.parar_robo()
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingApp(root)
    root.mainloop()
