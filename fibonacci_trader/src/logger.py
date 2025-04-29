"""
Sistema de logging profissional para Future MT5 Pro Trading
Gerencia logs na UI e em arquivos com codificação de cores e formatação
"""

import tkinter as tk
from datetime import datetime
import os
import logging
import json

class TradingLogger:
    def __init__(self):
        self.log_widgets = {}
        self.file_loggers = {}
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)

    def add_log_widget(self, asset_id, text_widget):
        self.log_widgets[asset_id] = text_widget
        self.setup_widget_tags(text_widget)
        self.setup_file_logger(asset_id)

    def setup_widget_tags(self, widget):
        widget.tag_configure('success', foreground='#00BFA5')
        widget.tag_configure('warning', foreground='#FFB300')
        widget.tag_configure('error', foreground='#FF3D00')
        widget.tag_configure('info', foreground='#B0BEC5')
        widget.tag_configure('header', foreground='#00B8D4')

    def setup_file_logger(self, asset_id):
        logger = logging.getLogger(f"trading_{asset_id}")
        logger.setLevel(logging.DEBUG)
        log_file = os.path.join(self.log_dir, f"{asset_id}_{datetime.now().strftime('%Y%m%d')}.log")
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.file_loggers[asset_id] = logger

    def get_message_type(self, message):
        if any(x in message for x in ['✅', 'SUCESSO', '🎯 SINAL']):
            return 'success'
        elif any(x in message for x in ['⚠️', 'AVISO', '⏳']):
            return 'warning'
        elif any(x in message for x in ['❌', 'ERRO']):
            return 'error'
        elif any(x in message for x in ['===', '📊', '📈']):
            return 'header'
        return 'info'

    def logar(self, mensagem, asset_id=None, level='INFO'):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        formatted_message = f"[{timestamp}] {mensagem}\n"
        msg_type = self.get_message_type(mensagem)

        if asset_id and asset_id in self.log_widgets:
            widget = self.log_widgets[asset_id]
            widget.insert('end', formatted_message, msg_type)
            widget.see('end')
            if float(widget.index('end')) > 1000:
                widget.delete('1.0', '500.0')
        elif not asset_id:
            for widget in self.log_widgets.values():
                widget.insert('end', formatted_message, msg_type)
                widget.see('end')
                if float(widget.index('end')) > 1000:
                    widget.delete('1.0', '500.0')

        if asset_id and asset_id in self.file_loggers:
            logger = self.file_loggers[asset_id]
            log_level = getattr(logging, level.upper(), logging.INFO)
            logger.log(log_level, mensagem)

    def clear_logs(self, asset_id=None):
        if asset_id and asset_id in self.log_widgets:
            self.log_widgets[asset_id].delete('1.0', 'end')
        elif not asset_id:
            for widget in self.log_widgets.values():
                widget.delete('1.0', 'end')

    def export_logs(self, asset_id, filepath):
        if asset_id not in self.log_widgets:
            return False
        try:
            widget = self.log_widgets[asset_id]
            logs = widget.get('1.0', 'end').splitlines()
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False

    def cleanup(self):
        for logger in self.file_loggers.values():
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
        self.log_widgets.clear()
        self.file_loggers.clear()

logger = TradingLogger()
