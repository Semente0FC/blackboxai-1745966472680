"""
Funções utilitárias para o sistema de negociação Future MT5 Pro
"""

import MetaTrader5 as mt5
from datetime import datetime
import json
import os

def obter_saldo():
    """Retorna o saldo atual da conta"""
    try:
        account_info = mt5.account_info()
        if account_info is not None:
            return account_info.balance
        return 0.0
    except:
        return 0.0

def verificar_conexao_mt5():
    """Verifica se o MT5 está conectado e retorna status e mensagem"""
    try:
        if not mt5.initialize():
            return False, "MetaTrader 5 não está instalado ou não pode ser inicializado"
        if not mt5.login():
            mt5.shutdown()
            return False, "Faça login no MetaTrader 5 primeiro"
        account_info = mt5.account_info()
        if account_info is None:
            mt5.shutdown()
            return False, "Não foi possível obter informações da conta"
        return True, "Conectado ao MetaTrader 5"
    except Exception as e:
        return False, f"Erro ao conectar ao MetaTrader 5: {str(e)}"

def formatar_moeda(valor, simbolo="R$"):
    """Formata um valor para exibição em moeda"""
    try:
        return f"{simbolo} {valor:,.2f}"
    except:
        return f"{simbolo} 0.00"

def verificar_horario_mercado():
    """Verifica se o mercado está aberto (9:00 - 17:30)"""
    current_time = datetime.now().time()
    return (current_time.hour >= 9 and
            (current_time.hour < 17 or
             (current_time.hour == 17 and current_time.minute <= 30)))

def obter_info_conta():
    """Retorna informações detalhadas da conta"""
    try:
        account_info = mt5.account_info()
        if account_info is not None:
            return {
                'login': account_info.login,
                'servidor': account_info.server,
                'saldo': account_info.balance,
                'equity': account_info.equity,
                'margem': account_info.margin,
                'margem_livre': account_info.margin_free,
                'lucro': account_info.profit
            }
        return None
    except:
        return None

def salvar_credenciais(login, servidor, lembrar=False):
    """Salva credenciais se lembrar for True"""
    if not lembrar:
        return
    try:
        credenciais = {'login': login, 'servidor': servidor}
        with open('credenciais.json', 'w') as f:
            json.dump(credenciais, f)
    except:
        pass

def carregar_credenciais():
    """Carrega credenciais salvas"""
    try:
        if not os.path.exists('credenciais.json'):
            return None
        with open('credenciais.json', 'r') as f:
            return json.load(f)
    except:
        return None

def limpar_credenciais():
    """Remove credenciais salvas"""
    try:
        if os.path.exists('credenciais.json'):
            os.remove('credenciais.json')
    except:
        pass

def obter_info_ativo(simbolo):
    """Retorna informações detalhadas do ativo"""
    try:
        info = mt5.symbol_info(simbolo)
        if info is None:
            return None
        return {
            'nome': info.name,
            'descricao': info.description,
            'moeda_base': info.currency_base,
            'moeda_lucro': info.currency_profit,
            'digitos': info.digits,
            'ponto': info.point,
            'tamanho_contrato': info.trade_contract_size,
            'volume_min': info.volume_min,
            'volume_max': info.volume_max,
            'passo_volume': info.volume_step
        }
    except:
        return None

def calcular_tamanho_posicao(saldo, risco_percentual, stop_loss_pontos, simbolo):
    """Calcula o tamanho da posição baseado no risco"""
    try:
        info = mt5.symbol_info(simbolo)
        if info is None:
            return 0.0
        risco_valor = saldo * (risco_percentual / 100)
        valor_ponto = info.trade_tick_value * (stop_loss_pontos / info.point)
        if valor_ponto == 0:
            return 0.0
        tamanho = risco_valor / valor_ponto
        tamanho = round(tamanho / info.volume_step) * info.volume_step
        tamanho = max(info.volume_min, min(tamanho, info.volume_max))
        return tamanho
    except:
        return 0.0

def formatar_mensagem_erro(codigo_erro):
    """Formata código de erro do MT5 para mensagem legível"""
    mensagens = {
        mt5.RES_S_OK: "Sucesso",
        mt5.RES_E_FAIL: "Erro geral",
        mt5.RES_E_INVALID_PARAMS: "Parâmetros inválidos",
        mt5.RES_E_NO_MEMORY: "Memória insuficiente",
        mt5.RES_E_NOT_FOUND: "Não encontrado",
        mt5.RES_E_INVALID_VERSION: "Versão inválida",
        mt5.RES_E_AUTH_FAILED: "Falha na autenticação",
        mt5.RES_E_UNSUPPORTED: "Método não suportado",
        mt5.RES_E_AUTO_TRADING_DISABLED: "AutoTrading desabilitado",
        mt5.RES_E_INTERNAL_FAIL: "Erro interno",
        mt5.RES_E_MARKET_CLOSED: "Mercado fechado",
        mt5.RES_E_TRADE_DISABLED: "Negociação desabilitada",
        mt5.RES_E_INVALID_PRICE: "Preço inválido",
        mt5.RES_E_INVALID_STOPS: "Stops inválidos",
        mt5.RES_E_INVALID_VOLUME: "Volume inválido",
        mt5.RES_E_TICK_PROCESSING: "Erro no processamento do tick"
    }
    return mensagens.get(codigo_erro, f"Erro desconhecido ({codigo_erro})")

def registrar_resultado_trade(resultado):
    """Registra resultado da execução de trade"""
    if resultado.retcode != mt5.TRADE_RETCODE_DONE:
        return False, formatar_mensagem_erro(resultado.retcode)
    return True, "Trade executado com sucesso"

def limpar_conexao_mt5():
    """Encerra conexão com MT5 com segurança"""
    try:
        mt5.shutdown()
    except:
        pass
