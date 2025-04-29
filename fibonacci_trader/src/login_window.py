import tkinter as tk
from tkinter import ttk, messagebox
import MetaTrader5 as mt5
import threading

class LoginWindow:
    def __init__(self, on_success=None):
        self.root = tk.Tk()
        self.root.title("Login MetaTrader 5")
        self.on_success = on_success
        
        self.root.configure(bg='#1E1E1E')
        self.root.resizable(False, False)
        self.centralizar_janela(400, 500)
        
        self.login_var = tk.StringVar()
        self.senha_var = tk.StringVar()
        self.servidor_var = tk.StringVar()
        self.is_connecting = False
        self.connection_successful = False
        
        self.setup_ui()
        
    def centralizar_janela(self, largura, altura):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#1E1E1E', highlightbackground='#00C853', highlightthickness=1)
        main_frame.pack(expand=True, fill="both", padx=2, pady=2)
        
        header_frame = tk.Frame(main_frame, bg='#1E1E1E')
        header_frame.pack(fill="x", padx=30, pady=30)
        
        logo_label = tk.Label(header_frame, text="🔐", font=("Helvetica", 48), bg='#1E1E1E', fg='#00C853')
        logo_label.pack()
        
        title_label = tk.Label(header_frame, text="Login MetaTrader 5", font=("Helvetica", 18, "bold"), bg='#1E1E1E', fg='white')
        title_label.pack(pady=(10, 0))
        
        subtitle_label = tk.Label(header_frame, text="Insira suas credenciais de negociação", font=("Helvetica", 10), bg='#1E1E1E', fg='#B3B3B3')
        subtitle_label.pack()
        
        form_frame = tk.Frame(main_frame, bg='#1E1E1E')
        form_frame.pack(fill="x", padx=40, pady=20)
        
        tk.Label(form_frame, text="Login:", font=("Helvetica", 10, "bold"), bg='#1E1E1E', fg='#B3B3B3').pack(anchor="w")
        login_entry = ttk.Entry(form_frame, textvariable=self.login_var, width=30)
        login_entry.pack(fill="x", pady=(5, 15))
        
        tk.Label(form_frame, text="Senha:", font=("Helvetica", 10, "bold"), bg='#1E1E1E', fg='#B3B3B3').pack(anchor="w")
        senha_entry = ttk.Entry(form_frame, textvariable=self.senha_var, show="*", width=30)
        senha_entry.pack(fill="x", pady=(5, 15))
        
        tk.Label(form_frame, text="Servidor:", font=("Helvetica", 10, "bold"), bg='#1E1E1E', fg='#B3B3B3').pack(anchor="w")
        servidor_entry = ttk.Entry(form_frame, textvariable=self.servidor_var, width=30)
        servidor_entry.pack(fill="x", pady=(5, 15))
        
        self.login_button = tk.Button(form_frame, text="Conectar", command=self.fazer_login, bg='#00C853', fg='white', font=("Helvetica", 12, "bold"), relief="flat", cursor="hand2", width=20, height=2)
        self.login_button.pack(pady=10)
        
        self.status_label = tk.Label(form_frame, text="", font=("Helvetica", 10), bg='#1E1E1E', fg='#B3B3B3', wraplength=300)
        self.status_label.pack(pady=10)
        
    def fazer_login(self):
        if self.is_connecting:
            return
        
        login = self.login_var.get().strip()
        senha = self.senha_var.get().strip()
        servidor = self.servidor_var.get().strip()
        
        if not all([login, senha, servidor]):
            self.show_status("Por favor, preencha todos os campos", "warning")
            return
        
        self.is_connecting = True
        self.login_button.config(state="disabled")
        self.show_status("Conectando ao MetaTrader 5...", "info")
        
        threading.Thread(target=self.connect_mt5, args=(login, senha, servidor), daemon=True).start()
        
    def connect_mt5(self, login, senha, servidor):
        try:
            if not mt5.initialize():
                self.show_status("Falha ao inicializar o MetaTrader 5.\nVerifique se está instalado.", "error")
                return
            
            if not mt5.login(int(login), senha, servidor):
                self.show_status("Falha no login.\nVerifique suas credenciais.", "error")
                mt5.shutdown()
                return
            
            if mt5.account_info() is None:
                self.show_status("Não foi possível conectar à conta de negociação.", "error")
                mt5.shutdown()
                return
            
            self.connection_successful = True
            self.show_status("Login realizado com sucesso!", "success")
            self.root.after(1000, self.complete_login)
        except Exception as e:
            self.show_status(f"Erro: {str(e)}", "error")
        finally:
            self.is_connecting = False
            self.login_button.config(state="normal")
            
    def show_status(self, message, status_type="info"):
        colors = {
            "info": "#B3B3B3",
            "success": "#00BFA5",
            "warning": "#FFB300",
            "error": "#FF3D00"
        }
        self.status_label.config(text=message, fg=colors.get(status_type, "#B3B3B3"))
        
    def complete_login(self):
        if self.on_success:
            self.on_success()
        self.root.destroy()
        
    def start(self):
        self.root.mainloop()
        return self.connection_successful

def show_login():
    login_window = LoginWindow()
    return login_window.start()
