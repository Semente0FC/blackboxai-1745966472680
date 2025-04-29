"""
UI Styles for Future MT5 Pro Trading System
"""

from tkinter import ttk
from typing import Dict, Any

from config import config

class Styles:
    @staticmethod
    def setup_styles():
        """Setup all custom styles for the application"""
        style = ttk.Style()
        
        # Configure common elements
        style.configure(
            "App.TFrame",
            background=config.COLORS['bg_dark']
        )
        
        style.configure(
            "App.TLabel",
            background=config.COLORS['bg_dark'],
            foreground=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'])
        )
        
        # Entry fields
        style.configure(
            "App.TEntry",
            fieldbackground=config.COLORS['bg_medium'],
            foreground=config.COLORS['text'],
            insertcolor=config.COLORS['text'],
            borderwidth=0,
            relief="flat"
        )
        
        # Combobox
        style.configure(
            "App.TCombobox",
            fieldbackground=config.COLORS['bg_medium'],
            background=config.COLORS['bg_medium'],
            foreground=config.COLORS['text'],
            arrowcolor=config.COLORS['accent'],
            borderwidth=0,
            relief="flat"
        )
        
        style.map(
            "App.TCombobox",
            fieldbackground=[
                ('readonly', config.COLORS['bg_medium']),
                ('disabled', config.COLORS['bg_dark'])
            ],
            selectbackground=[
                ('readonly', config.COLORS['accent'])
            ],
            selectforeground=[
                ('readonly', config.COLORS['text'])
            ]
        )
        
        # Button styles
        style.configure(
            "App.TButton",
            background=config.COLORS['accent'],
            foreground=config.COLORS['text'],
            borderwidth=0,
            relief="flat",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'], "bold")
        )
        
        style.map(
            "App.TButton",
            background=[
                ('active', config.COLORS['accent_hover']),
                ('disabled', config.COLORS['bg_medium'])
            ],
            foreground=[
                ('disabled', config.COLORS['text_secondary'])
            ]
        )
        
        # Success button
        style.configure(
            "Success.TButton",
            background=config.COLORS['success'],
            foreground=config.COLORS['text'],
            borderwidth=0,
            relief="flat",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'], "bold")
        )
        
        style.map(
            "Success.TButton",
            background=[
                ('active', config.COLORS['success']),
                ('disabled', config.COLORS['bg_medium'])
            ]
        )
        
        # Warning button
        style.configure(
            "Warning.TButton",
            background=config.COLORS['warning'],
            foreground=config.COLORS['text'],
            borderwidth=0,
            relief="flat",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'], "bold")
        )
        
        style.map(
            "Warning.TButton",
            background=[
                ('active', config.COLORS['warning']),
                ('disabled', config.COLORS['bg_medium'])
            ]
        )
        
        # Danger button
        style.configure(
            "Danger.TButton",
            background=config.COLORS['danger'],
            foreground=config.COLORS['text'],
            borderwidth=0,
            relief="flat",
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'], "bold")
        )
        
        style.map(
            "Danger.TButton",
            background=[
                ('active', config.COLORS['danger']),
                ('disabled', config.COLORS['bg_medium'])
            ]
        )
        
        # Checkbutton
        style.configure(
            "App.TCheckbutton",
            background=config.COLORS['bg_medium'],
            foreground=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'])
        )
        
        # Radiobutton
        style.configure(
            "App.TRadiobutton",
            background=config.COLORS['bg_medium'],
            foreground=config.COLORS['text'],
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'])
        )
        
        # Notebook
        style.configure(
            "App.TNotebook",
            background=config.COLORS['bg_dark'],
            borderwidth=0
        )
        
        style.configure(
            "App.TNotebook.Tab",
            background=config.COLORS['bg_medium'],
            foreground=config.COLORS['text'],
            padding=[10, 5],
            font=(config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'])
        )
        
        style.map(
            "App.TNotebook.Tab",
            background=[
                ('selected', config.COLORS['accent']),
                ('active', config.COLORS['accent_hover'])
            ],
            foreground=[
                ('selected', config.COLORS['text']),
                ('active', config.COLORS['text'])
            ]
        )
        
        # Progressbar
        style.configure(
            "App.Horizontal.TProgressbar",
            troughcolor=config.COLORS['bg_medium'],
            background=config.COLORS['accent'],
            borderwidth=0,
            relief="flat"
        )
        
        # Scrollbar
        style.configure(
            "App.Vertical.TScrollbar",
            background=config.COLORS['bg_medium'],
            troughcolor=config.COLORS['bg_dark'],
            borderwidth=0,
            relief="flat",
            arrowcolor=config.COLORS['text_secondary']
        )
        
        style.map(
            "App.Vertical.TScrollbar",
            background=[
                ('active', config.COLORS['accent']),
                ('disabled', config.COLORS['bg_medium'])
            ]
        )
        
        # Spinbox
        style.configure(
            "App.TSpinbox",
            fieldbackground=config.COLORS['bg_medium'],
            foreground=config.COLORS['text'],
            insertcolor=config.COLORS['text'],
            borderwidth=0,
            relief="flat",
            arrowcolor=config.COLORS['accent']
        )

    @staticmethod
    def get_button_style(style_type: str = "normal") -> Dict[str, Any]:
        """Get button style configuration"""
        styles = {
            "normal": {
                "bg": config.COLORS['accent'],
                "fg": config.COLORS['text'],
                "activebackground": config.COLORS['accent_hover'],
                "activeforeground": config.COLORS['text'],
                "relief": "flat",
                "borderwidth": 0,
                "cursor": "hand2",
                "font": (config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'], "bold")
            },
            "success": {
                "bg": config.COLORS['success'],
                "fg": config.COLORS['text'],
                "activebackground": config.COLORS['success'],
                "activeforeground": config.COLORS['text'],
                "relief": "flat",
                "borderwidth": 0,
                "cursor": "hand2",
                "font": (config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'], "bold")
            },
            "warning": {
                "bg": config.COLORS['warning'],
                "fg": config.COLORS['text'],
                "activebackground": config.COLORS['warning'],
                "activeforeground": config.COLORS['text'],
                "relief": "flat",
                "borderwidth": 0,
                "cursor": "hand2",
                "font": (config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'], "bold")
            },
            "danger": {
                "bg": config.COLORS['danger'],
                "fg": config.COLORS['text'],
                "activebackground": config.COLORS['danger'],
                "activeforeground": config.COLORS['text'],
                "relief": "flat",
                "borderwidth": 0,
                "cursor": "hand2",
                "font": (config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'], "bold")
            }
        }
        return styles.get(style_type, styles["normal"])

    @staticmethod
    def get_label_style(style_type: str = "normal") -> Dict[str, Any]:
        """Get label style configuration"""
        styles = {
            "normal": {
                "bg": config.COLORS['bg_dark'],
                "fg": config.COLORS['text'],
                "font": (config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['NORMAL'])
            },
            "title": {
                "bg": config.COLORS['bg_dark'],
                "fg": config.COLORS['text'],
                "font": (config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['TITLE'], "bold")
            },
            "subtitle": {
                "bg": config.COLORS['bg_dark'],
                "fg": config.COLORS['text_secondary'],
                "font": (config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SUBTITLE'])
            },
            "small": {
                "bg": config.COLORS['bg_dark'],
                "fg": config.COLORS['text_secondary'],
                "font": (config.UI['FONTS']['FAMILY'], config.UI['FONTS']['SIZES']['SMALL'])
            }
        }
        return styles.get(style_type, styles["normal"])

    @staticmethod
    def get_frame_style(style_type: str = "normal") -> Dict[str, Any]:
        """Get frame style configuration"""
        styles = {
            "normal": {
                "bg": config.COLORS['bg_dark'],
                "highlightthickness": 0
            },
            "border": {
                "bg": config.COLORS['bg_dark'],
                "highlightbackground": config.COLORS['accent'],
                "highlightthickness": 1
            },
            "raised": {
                "bg": config.COLORS['bg_dark'],
                "relief": "raised",
                "borderwidth": 1
            }
        }
        return styles.get(style_type, styles["normal"])

# Initialize styles
def init_styles():
    """Initialize all application styles"""
    Styles.setup_styles()

# Export styles
__all__ = ['Styles', 'init_styles']
