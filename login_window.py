import tkinter as tk
from tkinter import ttk, messagebox
import MetaTrader5 as mt5
import sys
import os
import threading

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Default values in case import fails
DEFAULT_CONFIG = {
    'APP_NAME': "Future MT5 Pro Trading",
    'COLORS': {
        'bg_dark': '#0A0E17',
        'bg_medium': '#151B28',
        'bg_light': '#1E2738',
        'accent': '#00B8D4',
        'accent_hover': '#00E5FF',
        'success': '#00BFA5',
        'warning': '#FFB300',
        'danger': '#FF3D00',
        'text': '#FFFFFF',
        'text_secondary': '#B0BEC5'
    }
}

# Try to import configuration
try:
    from config import COLORS, APP_NAME
except ImportError:
    print("Warning: Could not import config, using default values")
    COLORS = DEFAULT_CONFIG['COLORS']
    APP_NAME = DEFAULT_CONFIG['APP_NAME']

class LoginWindow:
    def __init__(self, on_success=None):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} - Login")
        self.on_success = on_success
        
        # Configure window
        self.root.configure(bg=COLORS['bg_dark'])
        self.root.resizable(False, False)
        
        # Set window size and position
        width = 400
        height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Variables
        self.login_var = tk.StringVar()
        self.senha_var = tk.StringVar()
        self.servidor_var = tk.StringVar()
        self.remember_var = tk.BooleanVar(value=False)
        
        # Status variables
        self.is_connecting = False
        self.connection_successful = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with border effect
        main_frame = tk.Frame(
            self.root,
            bg=COLORS['bg_dark'],
            highlightbackground=COLORS['accent'],
            highlightthickness=1
        )
        main_frame.pack(expand=True, fill="both", padx=2, pady=2)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=COLORS['bg_dark'])
        header_frame.pack(fill="x", padx=30, pady=30)
        
        # Logo
        logo_label = tk.Label(
            header_frame,
            text="🔐",
            font=("Helvetica", 48),
            bg=COLORS['bg_dark'],
            fg=COLORS['accent']
        )
        logo_label.pack()
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="MetaTrader 5 Login",
            font=("Helvetica", 18, "bold"),
            bg=COLORS['bg_dark'],
            fg=COLORS['text']
        )
        title_label.pack(pady=(10, 0))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Enter your trading account credentials",
            font=("Helvetica", 10),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary']
        )
        subtitle_label.pack()
        
        # Form container
        form_frame = tk.Frame(main_frame, bg=COLORS['bg_dark'])
        form_frame.pack(fill="x", padx=40, pady=20)
        
        # Style for entry fields
        style = ttk.Style()
        style.configure(
            "Custom.TEntry",
            fieldbackground=COLORS['bg_medium'],
            foreground=COLORS['text']
        )
        
        # Login field
        tk.Label(
            form_frame,
            text="Login",
            font=("Helvetica", 10, "bold"),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary']
        ).pack(anchor="w")
        
        login_entry = ttk.Entry(
            form_frame,
            textvariable=self.login_var,
            style="Custom.TEntry",
            font=("Helvetica", 12),
            width=30
        )
        login_entry.pack(fill="x", pady=(5, 15))
        
        # Password field
        tk.Label(
            form_frame,
            text="Password",
            font=("Helvetica", 10, "bold"),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary']
        ).pack(anchor="w")
        
        senha_entry = ttk.Entry(
            form_frame,
            textvariable=self.senha_var,
            style="Custom.TEntry",
            font=("Helvetica", 12),
            show="●",
            width=30
        )
        senha_entry.pack(fill="x", pady=(5, 15))
        
        # Server field
        tk.Label(
            form_frame,
            text="Server",
            font=("Helvetica", 10, "bold"),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary']
        ).pack(anchor="w")
        
        servidor_entry = ttk.Entry(
            form_frame,
            textvariable=self.servidor_var,
            style="Custom.TEntry",
            font=("Helvetica", 12),
            width=30
        )
        servidor_entry.pack(fill="x", pady=(5, 15))
        
        # Remember me checkbox
        remember_frame = tk.Frame(form_frame, bg=COLORS['bg_dark'])
        remember_frame.pack(fill="x", pady=(0, 20))
        
        remember_check = ttk.Checkbutton(
            remember_frame,
            text="Remember me",
            variable=self.remember_var,
            style="Custom.TCheckbutton"
        )
        remember_check.pack(side="left")
        
        # Login button
        self.login_button = tk.Button(
            form_frame,
            text="LOGIN",
            command=self.fazer_login,
            font=("Helvetica", 12, "bold"),
            bg=COLORS['accent'],
            fg=COLORS['text'],
            activebackground=COLORS['accent_hover'],
            activeforeground=COLORS['text'],
            relief="flat",
            cursor="hand2",
            width=20,
            height=2
        )
        self.login_button.pack(pady=10)
        
        # Status message
        self.status_label = tk.Label(
            form_frame,
            text="",
            font=("Helvetica", 10),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary'],
            wraplength=300
        )
        self.status_label.pack(pady=10)
        
    def fazer_login(self):
        if self.is_connecting:
            return
            
        login = self.login_var.get().strip()
        senha = self.senha_var.get().strip()
        servidor = self.servidor_var.get().strip()
        
        if not all([login, senha, servidor]):
            self.show_status("Please fill in all fields", "warning")
            return
            
        self.is_connecting = True
        self.login_button.config(state="disabled")
        self.show_status("Connecting to MetaTrader 5...", "info")
        
        # Run connection in thread
        threading.Thread(target=self.connect_mt5, args=(login, senha, servidor), daemon=True).start()
        
    def connect_mt5(self, login, senha, servidor):
        try:
            # Initialize MT5
            if not mt5.initialize():
                self.show_status("Failed to initialize MetaTrader 5.\nPlease make sure it's installed.", "error")
                return
                
            # Try login
            if not mt5.login(int(login), senha, servidor):
                self.show_status("Login failed.\nPlease check your credentials.", "error")
                mt5.shutdown()
                return
                
            # Verify connection
            if mt5.account_info() is None:
                self.show_status("Could not connect to trading account.", "error")
                mt5.shutdown()
                return
                
            # Success
            self.connection_successful = True
            self.show_status("Login successful!", "success")
            self.root.after(1000, self.complete_login)
            
        except Exception as e:
            self.show_status(f"Error: {str(e)}", "error")
        finally:
            self.is_connecting = False
            self.login_button.config(state="normal")
            
    def show_status(self, message, status_type="info"):
        colors = {
            "info": COLORS['text_secondary'],
            "success": COLORS['success'],
            "warning": COLORS['warning'],
            "error": COLORS['danger']
        }
        self.root.after(0, lambda: self.status_label.config(
            text=message,
            fg=colors.get(status_type, COLORS['text_secondary'])
        ))
        
    def complete_login(self):
        if self.on_success:
            self.on_success()
        self.root.destroy()
        
    def start(self):
        self.root.mainloop()
        return self.connection_successful

def show_login():
    """Show login window and return True if login successful"""
    login_window = LoginWindow()
    return login_window.start()

if __name__ == "__main__":
    show_login()
