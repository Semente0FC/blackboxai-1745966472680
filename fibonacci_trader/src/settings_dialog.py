"""
Diálogo de configurações para o sistema de negociação Future MT5 Pro
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config import config
from logger import logger

class SettingsDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configurações")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg=config.COLORS['bg_dark'])
        self.dialog.resizable(False, False)
        self.center_window(600, 700, parent)

        self.original_values = {
            'trading': dict(config.TRADING),
            'fibonacci': dict(config.FIBONACCI),
            'analysis': dict(config.ANALYSIS),
            'market_hours': dict(config.MARKET_HOURS)
        }

        self.variables = self.create_variables()
        self.setup_ui()

    def center_window(self, width, height, parent):
        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

    def create_variables(self):
        variables = {
            'trading': {},
            'fibonacci': {},
            'analysis': {},
            'market_hours': {}
        }
        for key, value in config.TRADING.items():
            variables['trading'][key] = tk.DoubleVar(value=value) if isinstance(value, (int, float)) else tk.StringVar(value=str(value))
        for key, value in config.FIBONACCI.items():
            variables['fibonacci'][key] = tk.DoubleVar(value=value) if isinstance(value, (int, float)) else tk.StringVar(value=str(value))
        for key, value in config.ANALYSIS.items():
            variables['analysis'][key] = tk.DoubleVar(value=value) if isinstance(value, (int, float)) else tk.StringVar(value=str(value))
        for key, value in config.MARKET_HOURS.items():
            if isinstance(value, dict):
                variables['market_hours'][key] = {
                    'hour': tk.IntVar(value=value['HOUR']),
                    'minute': tk.IntVar(value=value['MINUTE'])
                }
        return variables

    def setup_ui(self):
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        notebook.add(self.create_trading_tab(), text="Negociação")
        notebook.add(self.create_fibonacci_tab(), text="Fibonacci")
        notebook.add(self.create_analysis_tab(), text="Análise Técnica")
        notebook.add(self.create_market_tab(), text="Horário do Mercado")

        button_frame = tk.Frame(self.dialog, bg=config.COLORS['bg_dark'])
        button_frame.pack(fill="x", padx=10, pady=10)

        save_btn = tk.Button(button_frame, text="Salvar", command=self.save_settings, bg=config.COLORS['success'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10, "bold"), width=10, cursor="hand2")
        save_btn.pack(side="right", padx=5)

        cancel_btn = tk.Button(button_frame, text="Cancelar", command=self.dialog.destroy, bg=config.COLORS['danger'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10, "bold"), width=10, cursor="hand2")
        cancel_btn.pack(side="right", padx=5)

        reset_btn = tk.Button(button_frame, text="Resetar", command=self.reset_settings, bg=config.COLORS['warning'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10, "bold"), width=10, cursor="hand2")
        reset_btn.pack(side="left", padx=5)

    def create_trading_tab(self):
        frame = tk.Frame(bg=config.COLORS['bg_medium'])
        risk_frame = tk.LabelFrame(frame, text="Gestão de Risco", bg=config.COLORS['bg_medium'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10, "bold"))
        risk_frame.pack(fill="x", padx=10, pady=5)

        self.create_setting_row(risk_frame, "Risco por Operação (%)", self.variables['trading']['risk_percent'])
        self.create_setting_row(risk_frame, "Máximo de Posições", self.variables['trading']['max_positions'])
        self.create_setting_row(risk_frame, "Relação Risco/Recompensa Mínima", self.variables['trading']['min_rr_ratio'])

        trade_frame = tk.LabelFrame(frame, text="Parâmetros de Negociação", bg=config.COLORS['bg_medium'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10, "bold"))
        trade_frame.pack(fill="x", padx=10, pady=5)

        self.create_setting_row(trade_frame, "Lote Padrão", self.variables['trading']['default_lot'])
        self.create_setting_row(trade_frame, "Spread Máximo (pontos)", self.variables['trading'].get('max_spread', tk.DoubleVar(value=50)))

        return frame

    def create_fibonacci_tab(self):
        frame = tk.Frame(bg=config.COLORS['bg_medium'])
        analysis_frame = tk.LabelFrame(frame, text="Parâmetros de Análise", bg=config.COLORS['bg_medium'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10, "bold"))
        analysis_frame.pack(fill="x", padx=10, pady=5)

        self.create_setting_row(analysis_frame, "Período de Análise", self.variables['fibonacci']['period'])
        self.create_setting_row(analysis_frame, "Mínimo de Tendência (%)", self.variables['fibonacci']['min_trend'])

        return frame

    def create_analysis_tab(self):
        frame = tk.Frame(bg=config.COLORS['bg_medium'])
        rsi_frame = tk.LabelFrame(frame, text="Configurações RSI", bg=config.COLORS['bg_medium'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10, "bold"))
        rsi_frame.pack(fill="x", padx=10, pady=5)

        self.create_setting_row(rsi_frame, "Período RSI", self.variables['analysis']['rsi_period'])
        self.create_setting_row(rsi_frame, "Nível Sobrecomprado", self.variables['analysis']['rsi_overbought'])
        self.create_setting_row(rsi_frame, "Nível Sobrevendido", self.variables['analysis']['rsi_oversold'])

        return frame

    def create_market_tab(self):
        frame = tk.Frame(bg=config.COLORS['bg_medium'])
        hours_frame = tk.LabelFrame(frame, text="Horário do Mercado", bg=config.COLORS['bg_medium'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10, "bold"))
        hours_frame.pack(fill="x", padx=10, pady=5)

        open_frame = tk.Frame(hours_frame, bg=config.COLORS['bg_medium'])
        open_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(open_frame, text="Abertura do Mercado:", bg=config.COLORS['bg_medium'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10)).pack(side="left")

        ttk.Spinbox(open_frame, from_=0, to=23, width=5, textvariable=self.variables['market_hours']['open']['hour']).pack(side="left", padx=5)
        ttk.Spinbox(open_frame, from_=0, to=59, width=5, textvariable=self.variables['market_hours']['open']['minute']).pack(side="left")

        close_frame = tk.Frame(hours_frame, bg=config.COLORS['bg_medium'])
        close_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(close_frame, text="Fechamento do Mercado:", bg=config.COLORS['bg_medium'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10)).pack(side="left")

        ttk.Spinbox(close_frame, from_=0, to=23, width=5, textvariable=self.variables['market_hours']['close']['hour']).pack(side="left", padx=5)
        ttk.Spinbox(close_frame, from_=0, to=59, width=5, textvariable=self.variables['market_hours']['close']['minute']).pack(side="left")

        return frame

    def create_setting_row(self, parent, label, variable):
        frame = tk.Frame(parent, bg=config.COLORS['bg_medium'])
        frame.pack(fill="x", padx=10, pady=2)

        tk.Label(frame, text=label, bg=config.COLORS['bg_medium'], fg=config.COLORS['text'], font=(config.UI['FONTS']['FAMILY'], 10)).pack(side="left")

        if isinstance(variable, tk.BooleanVar):
            ttk.Checkbutton(frame, variable=variable).pack(side="right")
        else:
            ttk.Entry(frame, textvariable=variable, width=10).pack(side="right")

    def save_settings(self):
        try:
            new_trading = {key: var.get() for key, var in self.variables['trading'].items()}
            config.update_section('trading', new_trading)

            new_fibonacci = {key: var.get() for key, var in self.variables['fibonacci'].items()}
            config.update_section('fibonacci', new_fibonacci)

            new_analysis = {key: var.get() for key, var in self.variables['analysis'].items()}
            config.update_section('analysis', new_analysis)

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

            if config.save_user_config():
                messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
                self.dialog.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao salvar configurações!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")

    def reset_settings(self):
        if messagebox.askyesno("Resetar", "Deseja resetar todas as configurações para os valores padrão?"):
            config.reset_to_defaults()
            self.dialog.destroy()

def show_settings(parent):
    dialog = SettingsDialog(parent)
    return dialog
</create_file>
