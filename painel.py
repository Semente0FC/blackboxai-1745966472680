import tkinter as tk
from tkinter import ttk, messagebox
import MetaTrader5 as mt5
from utils import obter_saldo
from estrategia import EstrategiaTrading
from log_system import LogSystem
import threading
import time
from datetime import datetime


class PainelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Future MT5 Pro Trading - Fibonacci")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Theme colors
        self.colors = {
            'bg_dark': '#1E1E1E',
            'bg_medium': '#2D2D2D',
            'bg_light': '#333333',
            'accent': '#00C853',
            'accent_hover': '#00E676',
            'warning': '#FFB300',
            'danger': '#FF3D00',
            'text': '#FFFFFF',
            'text_secondary': '#B3B3B3'
        }

        self.root.configure(bg=self.colors['bg_dark'])
        self.root.resizable(False, False)
        self.centralizar_janela(1000, 700)

        # Trading variables
        self.ativo_selecionado = tk.StringVar()
        self.timeframe_selecionado = tk.StringVar()
        self.lote_selecionado = tk.StringVar(value="0.10")
        self.operando = False
        self.estrategia = None
        self.log_system = LogSystem()

        self.setup_ui()

    def centralizar_janela(self, largura, altura):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors['bg_dark'], pady=20)
        header.pack(fill="x", padx=20)

        # Title
        title = tk.Label(
            header,
            text="FUTURE MT5 PRO - FIBONACCI TRADER",
            font=("Helvetica", 24, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_dark']
        )
        title.pack(side="left")

        # Balance display
        self.saldo_frame = tk.Frame(header, bg=self.colors['bg_light'], padx=15, pady=10)
        self.saldo_frame.pack(side="right")

        tk.Label(
            self.saldo_frame,
            text="SALDO",
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        ).pack()

        self.saldo_label = tk.Label(
            self.saldo_frame,
            text="R$ 0.00",
            font=("Helvetica", 18, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_light']
        )
        self.saldo_label.pack()

        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_medium'], padx=20, pady=20)
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Control panel
        control_panel = tk.Frame(main_container, bg=self.colors['bg_light'], padx=20, pady=20)
        control_panel.pack(fill="x", pady=(0, 20))

        # Asset selection
        asset_frame = tk.Frame(control_panel, bg=self.colors['bg_light'])
        asset_frame.pack(side="left", padx=(0, 20))

        tk.Label(
            asset_frame,
            text="ATIVO",
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        ).pack(anchor="w")

        self.combo_ativo = ttk.Combobox(
            asset_frame,
            textvariable=self.ativo_selecionado,
            width=15
        )
        self.combo_ativo.pack()

        # Timeframe selection
        timeframe_frame = tk.Frame(control_panel, bg=self.colors['bg_light'])
        timeframe_frame.pack(side="left", padx=(0, 20))

        tk.Label(
            timeframe_frame,
            text="TIMEFRAME",
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        ).pack(anchor="w")

        self.combo_timeframe = ttk.Combobox(
            timeframe_frame,
            textvariable=self.timeframe_selecionado,
            values=["M5", "M15", "M30", "H1", "H4", "D1"],
            width=10
        )
        self.combo_timeframe.pack()
        self.combo_timeframe.current(1)  # M15 default

        # Lot size
        lot_frame = tk.Frame(control_panel, bg=self.colors['bg_light'])
        lot_frame.pack(side="left", padx=(0, 20))

        tk.Label(
            lot_frame,
            text="LOTE",
            font=("Helvetica", 10, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        ).pack(anchor="w")

        self.entry_lote = tk.Entry(
            lot_frame,
            textvariable=self.lote_selecionado,
            width=10,
            font=("Helvetica", 11)
        )
        self.entry_lote.pack()

        # Control buttons
        btn_frame = tk.Frame(control_panel, bg=self.colors['bg_light'])
        btn_frame.pack(side="right")

        self.btn_iniciar = tk.Button(
            btn_frame,
            text="▶ INICIAR",
            command=self.iniciar_robo,
            font=("Helvetica", 11, "bold"),
            fg=self.colors['text'],
            bg=self.colors['accent'],
            activebackground=self.colors['accent_hover'],
            padx=20,
            pady=10
        )
        self.btn_iniciar.pack(side="left", padx=5)

        self.btn_parar = tk.Button(
            btn_frame,
            text="⏹ PARAR",
            command=self.parar_robo,
            font=("Helvetica", 11, "bold"),
            fg=self.colors['text'],
            bg=self.colors['danger'],
            activebackground=self.colors['danger'],
            padx=20,
            pady=10,
            state="disabled"
        )
        self.btn_parar.pack(side="left", padx=5)

        # Log area
        log_frame = tk.Frame(main_container, bg=self.colors['bg_light'], padx=20, pady=20)
        log_frame.pack(fill="both", expand=True)

        self.text_log = tk.Text(
            log_frame,
            height=20,
            width=80,
            bg=self.colors['bg_medium'],
            fg=self.colors['text'],
            font=("Consolas", 12),
            padx=10,
            pady=10
        )
        self.text_log.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, command=self.text_log.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_log.config(yscrollcommand=scrollbar.set)

        # Add log widget to log system
        self.log_system.add_log_widget("main", self.text_log)

        # Start update threads
        self.start_update_threads()

    def start_update_threads(self):
        threading.Thread(target=self.atualizar_saldo_loop, daemon=True).start()
        threading.Thread(target=self.carregar_ativos, daemon=True).start()

    def atualizar_saldo_loop(self):
        while True:
            saldo = obter_saldo()
            self.saldo_label.config(text=f"R$ {saldo:.2f}")
            time.sleep(1)

    def carregar_ativos(self):
        try:
            symbols = mt5.symbols_get()
            lista_ativos = [symbol.name for symbol in symbols if symbol.visible]
            self.combo_ativo['values'] = lista_ativos
            if lista_ativos:
                self.combo_ativo.current(0)
            self.log_system.logar(f"✅ {len(lista_ativos)} ativos disponíveis carregados")
        except Exception as e:
            self.log_system.logar(f"❌ Erro ao carregar ativos: {e}")

    def iniciar_robo(self):
        ativo = self.ativo_selecionado.get().strip()
        timeframe = self.timeframe_selecionado.get().strip()
        lote = self.lote_selecionado.get().strip()

        if not all([ativo, timeframe, lote]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            lote_float = round(float(lote), 2)
            if lote_float <= 0:
                messagebox.showerror("Erro", "O lote deve ser maior que zero!")
                return
        except ValueError:
            messagebox.showerror("Erro", "Valor de lote inválido!")
            return

        # Verificar ativo
        info = mt5.symbol_info(ativo)
        if info is None:
            messagebox.showerror("Erro", f"Ativo {ativo} não encontrado!")
            return
        if not info.visible:
            messagebox.showwarning("Aviso", f"Ativo {ativo} não está visível. Abrindo...")
            if not mt5.symbol_select(ativo, True):
                messagebox.showerror("Erro", f"Falha ao abrir {ativo}!")
                return

        self.operando = True
        self.btn_iniciar.config(state="disabled")
        self.btn_parar.config(state="normal")
        self.combo_ativo.config(state="disabled")
        self.combo_timeframe.config(state="disabled")
        self.entry_lote.config(state="disabled")

        # Criar e iniciar estratégia
        self.estrategia = EstrategiaTrading(ativo, timeframe, lote_float, self.log_system)
        threading.Thread(target=self.estrategia.executar, daemon=True).start()

    def parar_robo(self):
        if self.estrategia:
            self.estrategia.parar()
            self.estrategia = None

        self.operando = False
        self.btn_iniciar.config(state="normal")
        self.btn_parar.config(state="disabled")
        self.combo_ativo.config(state="normal")
        self.combo_timeframe.config(state="normal")
        self.entry_lote.config(state="normal")

    def on_closing(self):
        if self.operando:
            if messagebox.askokcancel("Sair", "O robô está em execução. Deseja realmente sair?"):
                self.parar_robo()
                self.root.destroy()
        else:
            self.root.destroy()
