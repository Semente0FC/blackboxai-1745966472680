import tkinter as tk
from tkinter import ttk, messagebox
import MetaTrader5 as mt5


class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login MetaTrader 5")
        self.window.geometry("400x300")
        self.window.configure(bg='#1E1E1E')
        self.window.resizable(False, False)

        # Centralizar janela
        self.centralizar_janela(400, 300)

        # Variáveis
        self.login_var = tk.StringVar()
        self.senha_var = tk.StringVar()
        self.servidor_var = tk.StringVar()

        self.setup_ui()

    def centralizar_janela(self, largura, altura):
        """Centraliza a janela na tela"""
        largura_tela = self.window.winfo_screenwidth()
        altura_tela = self.window.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.window.geometry(f"{largura}x{altura}+{x}+{y}")

    def setup_ui(self):
        """Configura a interface do usuário"""
        # Título
        titulo = tk.Label(
            self.window,
            text="Login MetaTrader 5",
            font=("Helvetica", 16, "bold"),
            fg='white',
            bg='#1E1E1E'
        )
        titulo.pack(pady=20)

        # Frame principal
        main_frame = tk.Frame(self.window, bg='#1E1E1E')
        main_frame.pack(fill='both', expand=True, padx=40)

        # Login
        tk.Label(
            main_frame,
            text="Login:",
            font=("Helvetica", 10),
            fg='white',
            bg='#1E1E1E'
        ).pack(anchor='w')

        entry_login = ttk.Entry(
            main_frame,
            textvariable=self.login_var,
            width=30
        )
        entry_login.pack(fill='x', pady=(0, 10))

        # Senha
        tk.Label(
            main_frame,
            text="Senha:",
            font=("Helvetica", 10),
            fg='white',
            bg='#1E1E1E'
        ).pack(anchor='w')

        entry_senha = ttk.Entry(
            main_frame,
            textvariable=self.senha_var,
            show="*",
            width=30
        )
        entry_senha.pack(fill='x', pady=(0, 10))

        # Servidor
        tk.Label(
            main_frame,
            text="Servidor:",
            font=("Helvetica", 10),
            fg='white',
            bg='#1E1E1E'
        ).pack(anchor='w')

        entry_servidor = ttk.Entry(
            main_frame,
            textvariable=self.servidor_var,
            width=30
        )
        entry_servidor.pack(fill='x', pady=(0, 20))

        # Botão de login
        btn_login = tk.Button(
            main_frame,
            text="Conectar",
            command=self.fazer_login,
            bg='#00C853',
            fg='white',
            font=("Helvetica", 10, "bold"),
            relief='flat',
            cursor='hand2',
            width=20,
            height=2
        )
        btn_login.pack(pady=10)

    def fazer_login(self):
        """Tenta fazer login no MT5"""
        login = self.login_var.get().strip()
        senha = self.senha_var.get().strip()
        servidor = self.servidor_var.get().strip()

        if not all([login, senha, servidor]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            # Inicializar MT5
            if not mt5.initialize():
                messagebox.showerror("Erro", "Falha ao inicializar o MetaTrader 5.\nVerifique se está instalado.")
                return

            # Tentar login
            if not mt5.login(int(login), senha, servidor):
                messagebox.showerror("Erro", "Falha ao fazer login.\nVerifique suas credenciais.")
                mt5.shutdown()
                return

            # Verificar conexão
            if mt5.account_info() is None:
                messagebox.showerror("Erro", "Não foi possível conectar à conta.")
                mt5.shutdown()
                return

            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.window.quit()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar: {str(e)}")
            mt5.shutdown()

    def mostrar(self):
        """Mostra a janela de login"""
        self.window.mainloop()
        return mt5.account_info() is not None


def solicitar_login():
    """Solicita login do usuário"""
    login_window = LoginWindow()
    return login_window.mostrar()
