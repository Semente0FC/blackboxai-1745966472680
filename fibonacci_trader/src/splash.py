import tkinter as tk
from tkinter import ttk
import threading
import time

class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Carregando...")

        self.root.configure(bg='#1E1E1E')
        self.root.overrideredirect(True)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width = 600
        height = 400
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.attributes('-alpha', 0.0)

        self.main_frame = tk.Frame(
            self.root,
            bg='#1E1E1E',
            highlightbackground='#00C853',
            highlightthickness=2
        )
        self.main_frame.pack(expand=True, fill="both", padx=2, pady=2)

        self.setup_ui()
        self.fade_in()

    def setup_ui(self):
        title_frame = tk.Frame(self.main_frame, bg='#1E1E1E')
        title_frame.pack(pady=(50, 20))

        logo_label = tk.Label(
            title_frame,
            text="🚀",
            font=("Helvetica", 64),
            bg='#1E1E1E',
            fg='#00C853'
        )
        logo_label.pack()

        name_label = tk.Label(
            title_frame,
            text="Future MT5 Pro Trading",
            font=("Helvetica", 24, "bold"),
            bg='#1E1E1E',
            fg='white'
        )
        name_label.pack(pady=(10, 0))

        version_label = tk.Label(
            title_frame,
            text="Versão 2.0.0",
            font=("Helvetica", 12),
            bg='#1E1E1E',
            fg='#B3B3B3'
        )
        version_label.pack()

        author_label = tk.Label(
            title_frame,
            text="por BLACKBOXAI",
            font=("Helvetica", 10),
            bg='#1E1E1E',
            fg='#B3B3B3'
        )
        author_label.pack()

        loading_frame = tk.Frame(self.main_frame, bg='#1E1E1E')
        loading_frame.pack(expand=True, fill="both", padx=50, pady=20)

        self.status_label = tk.Label(
            loading_frame,
            text="Inicializando...",
            font=("Helvetica", 10),
            bg='#1E1E1E',
            fg='#B3B3B3'
        )
        self.status_label.pack(pady=(0, 10))

        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#151B28',
            background='#00C853',
            darkcolor='#00C853',
            lightcolor='#00C853',
            bordercolor='#151B28'
        )

        self.progress = ttk.Progressbar(
            loading_frame,
            style="Custom.Horizontal.TProgressbar",
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=10)

        self.start_loading()

    def fade_in(self):
        alpha = self.root.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.1
            self.root.attributes('-alpha', alpha)
            self.root.after(20, self.fade_in)

    def fade_out(self):
        alpha = self.root.attributes('-alpha')
        if alpha > 0:
            alpha -= 0.1
            self.root.attributes('-alpha', alpha)
            self.root.after(20, self.fade_out)
        else:
            self.root.destroy()

    def update_status(self, message):
        self.status_label.config(text=message)

    def start_loading(self):
        self.loading_steps = [
            ("Inicializando sistema...", 10),
            ("Carregando configurações...", 20),
            ("Conectando ao MetaTrader 5...", 40),
            ("Preparando ambiente de negociação...", 60),
            ("Carregando dados do mercado...", 80),
            ("Iniciando sistema de negociação...", 90),
            ("Pronto para iniciar...", 100)
        ]
        threading.Thread(target=self.loading_simulation, daemon=True).start()

    def loading_simulation(self):
        for message, progress in self.loading_steps:
            time.sleep(0.5)
            self.root.after(0, self.update_status, message)
            self.root.after(0, self.progress.configure, {'value': progress})
        time.sleep(0.5)
        self.root.after(0, self.loading_complete)

    def loading_complete(self):
        self.update_status("Carregamento concluído!")
        time.sleep(1)
        self.fade_out()

    def start(self):
        self.root.mainloop()

def show_splash():
    splash = SplashScreen()
    splash.start()

if __name__ == "__main__":
    show_splash()
