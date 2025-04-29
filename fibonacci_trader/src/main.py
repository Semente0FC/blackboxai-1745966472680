import tkinter as tk
from tkinter import messagebox
import MetaTrader5 as mt5
import sys
import traceback
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from config import config
    from logger import logger
    from splash import show_splash
    from login_window import show_login
    from trading_app import TradingApp
    from utils import initialize_mt5, get_account_info, format_currency
except ImportError as e:
    print(f"Erro ao importar módulos: {str(e)}")
    sys.exit(1)

def handle_exception(exc_type, exc_value, exc_traceback):
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    messagebox.showerror(
        "Erro",
        f"Ocorreu um erro inesperado:\n\n{str(exc_value)}\n\nVerifique os logs para mais detalhes."
    )
    logger.log(f"Exceção não tratada:\n{error_msg}", level='ERROR')
    sys.exit(1)

def setup_mt5():
    success, message = initialize_mt5()
    if not success:
        return False, message
    if not show_login():
        return False, "Login falhou ou foi cancelado"
    account_info = get_account_info()
    if not account_info:
        return False, "Não foi possível obter informações da conta"
    logger.log("✅ Conectado com sucesso ao MetaTrader 5")
    logger.log(f"📊 Conta: {account_info['login']}")
    logger.log(f"🏢 Servidor: {account_info['server']}")
    logger.log(f"💰 Saldo: {format_currency(account_info['balance'])}")
    logger.log(f"📈 Equity: {format_currency(account_info['equity'])}")
    return True, "Conectado com sucesso"

def main():
    sys.excepthook = handle_exception
    print(f"\n=== {config.APP_NAME} v{config.VERSION} ===")
    print(f"Desenvolvido por {config.AUTHOR}")
    print("\nInicializando sistema...")
    try:
        show_splash()
        success, message = setup_mt5()
        if not success:
            print(f"\n❌ {message}")
            sys.exit(1)
        print("\n🚀 Iniciando interface de negociação...")
        root = tk.Tk()
        app = TradingApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro de inicialização", f"Falha ao iniciar o aplicativo:\n\n{str(e)}")
        logger.log(f"Erro de inicialização: {str(e)}", level='ERROR')
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("\n👋 Encerrando...")
        mt5.shutdown()
        logger.cleanup()
        print("✅ Conexão encerrada")

if __name__ == "__main__":
    main()
