import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Default values in case import fails
DEFAULT_CONFIG = {
    'APP_NAME': "Future MT5 Pro Trading",
    'VERSION': "2.0.0",
    'AUTHOR': "BLACKBOXAI",
    'COLORS': {
        'bg_dark': '#0A0E17',
        'bg_medium': '#151B28',
        'bg_light': '#1E2738',
        'accent': '#00B8D4',
        'accent_hover': '#00E5FF',
        'text': '#FFFFFF',
        'text_secondary': '#B0BEC5'
    }
}

# Try to import configuration
try:
    from config import COLORS, APP_NAME, VERSION, AUTHOR
except ImportError:
    print("Warning: Could not import config, using default values")
    COLORS = DEFAULT_CONFIG['COLORS']
    APP_NAME = DEFAULT_CONFIG['APP_NAME']
    VERSION = DEFAULT_CONFIG['VERSION']
    AUTHOR = DEFAULT_CONFIG['AUTHOR']

class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loading...")
        
        # Configure window
        self.root.configure(bg=COLORS['bg_dark'])
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size and position
        width = 600
        height = 400
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Add shadow effect
        self.root.attributes('-alpha', 0.0)  # Start fully transparent
        
        # Create main frame with padding
        self.main_frame = tk.Frame(
            self.root,
            bg=COLORS['bg_dark'],
            highlightbackground=COLORS['accent'],
            highlightthickness=2
        )
        self.main_frame.pack(expand=True, fill="both", padx=2, pady=2)
        
        self.setup_ui()
        self.fade_in()
        
    def setup_ui(self):
        # Logo and Title Section
        title_frame = tk.Frame(self.main_frame, bg=COLORS['bg_dark'])
        title_frame.pack(pady=(50, 20))
        
        # App Logo (rocket emoji as placeholder)
        logo_label = tk.Label(
            title_frame,
            text="🚀",
            font=("Helvetica", 64),
            bg=COLORS['bg_dark'],
            fg=COLORS['accent']
        )
        logo_label.pack()
        
        # App Name
        name_label = tk.Label(
            title_frame,
            text=APP_NAME,
            font=("Helvetica", 24, "bold"),
            bg=COLORS['bg_dark'],
            fg=COLORS['text']
        )
        name_label.pack(pady=(10, 0))
        
        # Version
        version_label = tk.Label(
            title_frame,
            text=f"Version {VERSION}",
            font=("Helvetica", 12),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary']
        )
        version_label.pack()
        
        # Author
        author_label = tk.Label(
            title_frame,
            text=f"by {AUTHOR}",
            font=("Helvetica", 10),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary']
        )
        author_label.pack()
        
        # Loading Section
        loading_frame = tk.Frame(self.main_frame, bg=COLORS['bg_dark'])
        loading_frame.pack(expand=True, fill="both", padx=50, pady=20)
        
        # Status message
        self.status_label = tk.Label(
            loading_frame,
            text="Initializing...",
            font=("Helvetica", 10),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary']
        )
        self.status_label.pack(pady=(0, 10))
        
        # Progress bar style
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=COLORS['bg_medium'],
            background=COLORS['accent'],
            darkcolor=COLORS['accent'],
            lightcolor=COLORS['accent'],
            bordercolor=COLORS['bg_medium']
        )
        
        # Progress bar
        self.progress = ttk.Progressbar(
            loading_frame,
            style="Custom.Horizontal.TProgressbar",
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        
        # Start loading simulation
        self.start_loading()
        
    def fade_in(self):
        """Smooth fade-in effect"""
        alpha = self.root.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.1
            self.root.attributes('-alpha', alpha)
            self.root.after(20, self.fade_in)
            
    def fade_out(self):
        """Smooth fade-out effect"""
        alpha = self.root.attributes('-alpha')
        if alpha > 0:
            alpha -= 0.1
            self.root.attributes('-alpha', alpha)
            self.root.after(20, self.fade_out)
        else:
            self.root.destroy()
            
    def update_status(self, message):
        """Update status message"""
        self.status_label.config(text=message)
        
    def start_loading(self):
        """Start loading simulation"""
        self.loading_steps = [
            ("Initializing system...", 10),
            ("Loading configurations...", 20),
            ("Connecting to MetaTrader 5...", 40),
            ("Preparing trading environment...", 60),
            ("Loading market data...", 80),
            ("Starting trading system...", 90),
            ("Ready to launch...", 100)
        ]
        threading.Thread(target=self.loading_simulation, daemon=True).start()
        
    def loading_simulation(self):
        """Simulate loading process"""
        for message, progress in self.loading_steps:
            time.sleep(0.5)  # Simulate work being done
            self.root.after(0, self.update_status, message)
            self.root.after(0, self.progress.configure, {'value': progress})
            
        # Complete loading
        time.sleep(0.5)
        self.root.after(0, self.loading_complete)
        
    def loading_complete(self):
        """Handle completion of loading"""
        self.update_status("Launch complete!")
        time.sleep(1)
        self.fade_out()
        
    def start(self):
        """Start the splash screen"""
        self.root.mainloop()

def show_splash():
    """Show splash screen and return when complete"""
    splash = SplashScreen()
    splash.start()

if __name__ == "__main__":
    show_splash()
