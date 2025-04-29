import MetaTrader5 as mt5
import numpy as np
import time
import threading
from datetime import datetime


class EstrategiaTrading:
    def __init__(self, ativo, timeframe, lote_base, log_system):
        self.ativo = ativo
        self.timeframe = self.converter_timeframe(timeframe)
        self.lote_base = float(lote_base)
        self.operando = True
        self.log_system = log_system
        self.ticket_atual = None
        self.lock = threading.Lock()
        self.last_analysis_time = None
        self.min_time_between_trades = 30

        # Parâmetros Fibonacci
        self.fib_period = 20  # Período para análise Fibonacci
        self.min_trend_percent = 2.0  # Variação mínima para considerar tendência
        self.fib_levels = [0.382, 0.5, 0.618]  # Níveis de Fibonacci
        self.fib_tp_levels = [1.272, 1.618]  # Níveis para Take Profit

        # Parâmetros de Confirmação
        self.rsi_period = 14
        self.rsi_sobrecomprado = 70
        self.rsi_sobrevendido = 30
        self.use_ma200 = True  # Filtro de MM200

        # Gestão de Risco
        self.risk_percent = 2.0  # Risco por operação
        self.max_positions = 1  # Máximo de operações simultâneas
        self.min_rr_ratio = 2.0  # Risk/Reward mínimo

        self.saldo_inicial = mt5.account_info().balance
        self.last_fib_data = None
        self.current_fib_levels = None

    def converter_timeframe(self, tf):
        mapping = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
        }
        return mapping.get(tf, mt5.TIMEFRAME_M5)

    def calcular_niveis_fibonacci(self, high, low, is_uptrend):
        """Calcula os níveis de Fibonacci"""
        range_price = high - low
        levels = {}
        if is_uptrend:
            for level in self.fib_levels:
                levels[level] = high - (range_price * level)
            for level in self.fib_tp_levels:
                levels[level] = high + (range_price * (level - 1))
        else:
            for level in self.fib_levels:
                levels[level] = low + (range_price * level)
            for level in self.fib_tp_levels:
                levels[level] = low - (range_price * (level - 1))
        return levels

    def identificar_tendencia(self, candles):
        """Identifica a tendência com base na variação percentual"""
        close = candles['close']
        high = candles['high']
        low = candles['low']

        # Calcular variação percentual
        variacao = ((close[-1] - close[0]) / close[0]) * 100

        # Verificar direção dos candles
        uptrend_candles = sum(1 for i in range(1, len(close)) if close[i] > close[i - 1])
        trend_strength = uptrend_candles / (len(close) - 1)

        self.log_system.logar(f"ℹ️ Variação: {variacao:.2f}% | Força da Tendência: {trend_strength:.2f}", self.ativo)

        if variacao > self.min_trend_percent and trend_strength > 0.6:
            return "ALTA", max(high), min(low)
        elif variacao < -self.min_trend_percent and trend_strength < 0.4:
            return "BAIXA", max(high), min(low)
        return "LATERAL", None, None

    def verificar_ma200(self, candles, trend):
        """Verifica filtro de MM200"""
        if not self.use_ma200:
            return True

        close = candles['close']
        ma200 = np.mean(close[-200:])

        if trend == "ALTA":
            return close[-1] > ma200
        elif trend == "BAIXA":
            return close[-1] < ma200
        return False

    def executar(self):
        self.log_system.logar(f"🚀 Iniciando estratégia Fibonacci para {self.ativo}", self.ativo)
        while self.operando:
            try:
                with self.lock:
                    self.analisar_e_operar()
                time.sleep(1)
            except Exception as e:
                self.log_system.logar(f"❌ Erro na estratégia: {str(e)}", self.ativo)
                time.sleep(10)

    def analisar_e_operar(self):
        try:
            # Carregar dados
            barras = mt5.copy_rates_from_pos(self.ativo, self.timeframe, 0, max(200, self.fib_period))
            if barras is None or len(barras) < 200:
                self.log_system.logar(f"❌ Erro: Dados insuficientes para {self.ativo}", self.ativo)
                return

            barras = np.array(barras)

            # Identificar tendência
            self.log_system.logar("\n=== ℹ️ ANÁLISE DE TENDÊNCIA ===", self.ativo)
            trend, high, low = self.identificar_tendencia(barras[-self.fib_period:])

            if trend != "LATERAL":
                # Calcular níveis Fibonacci
                self.current_fib_levels = self.calcular_niveis_fibonacci(high, low, trend == "ALTA")
                self.log_system.logar(f"📈 Tendência: {trend}", self.ativo)
                self.log_system.logar(f"ℹ️ Níveis Fibonacci:", self.ativo)
                for level, price in self.current_fib_levels.items():
                    self.log_system.logar(f"  {level * 100:.1f}%: {price:.5f}", self.ativo)

                # Análise de entrada
                self.log_system.logar("\n=== ℹ️ ANÁLISE DE ENTRADA ===", self.ativo)
                preco_atual = barras['close'][-1]
                rsi = self.calcular_rsi(barras['close'])

                # Verificar MA200
                ma_filter = self.verificar_ma200(barras, trend)
                self.log_system.logar(f"ℹ️ Filtro MM200: {'✅ Passou' if ma_filter else '❌ Não passou'}", self.ativo)

                # Verificar entradas
                for level in self.fib_levels:
                    fib_price = self.current_fib_levels[level]
                    price_diff_percent = abs((preco_atual - fib_price) / fib_price) * 100

                    if price_diff_percent < 0.1:  # Próximo ao nível (0.1%)
                        self.log_system.logar(f"🎯 Preço próximo ao nível {level * 100:.1f}%", self.ativo)

                        if trend == "ALTA" and rsi[-1] < self.rsi_sobrevendido and ma_filter:
                            self.log_system.logar("✅ Condições de COMPRA atendidas:", self.ativo)
                            self.log_system.logar(f"  - RSI: {rsi[-1]:.2f} (< {self.rsi_sobrevendido})", self.ativo)
                            self.processar_entrada("COMPRA", preco_atual, fib_price, self.current_fib_levels)

                        elif trend == "BAIXA" and rsi[-1] > self.rsi_sobrecomprado and ma_filter:
                            self.log_system.logar("✅ Condições de VENDA atendidas:", self.ativo)
                            self.log_system.logar(f"  - RSI: {rsi[-1]:.2f} (> {self.rsi_sobrecomprado})", self.ativo)
                            self.processar_entrada("VENDA", preco_atual, fib_price, self.current_fib_levels)

                if not any(
                        abs((preco_atual - self.current_fib_levels[level]) / self.current_fib_levels[level]) * 100 < 0.1
                        for level in self.fib_levels):
                    self.log_system.logar("⚠️ Aguardando preço atingir nível Fibonacci", self.ativo)
            else:
                self.log_system.logar("⚠️ Sem tendência definida. Aguardando movimento direcional.", self.ativo)

        except Exception as e:
            self.log_system.logar(f"❌ Erro na análise: {str(e)}", self.ativo)

    def processar_entrada(self, tipo, preco_atual, fib_level, fib_levels):
        """Processa uma entrada de trade"""
        if not self.verificar_risco_posicao():
            return

        # Calcular SL e TP baseados nos níveis de Fibonacci
        if tipo == "COMPRA":
            # SL no próximo nível abaixo, TP no próximo nível de extensão
            sl_price = min([p for p in fib_levels.values() if p < fib_level], default=fib_level * 0.99)
            tp_price = min([p for p in fib_levels.values() if p > preco_atual and p / fib_level > 1.272],
                           default=preco_atual * 1.272)
        else:
            # SL no próximo nível acima, TP no próximo nível de extensão
            sl_price = max([p for p in fib_levels.values() if p > fib_level], default=fib_level * 1.01)
            tp_price = max([p for p in fib_levels.values() if p < preco_atual and p / fib_level < 0.728],
                           default=preco_atual * 0.728)

        sl_distance = abs(preco_atual - sl_price)
        tp_distance = abs(preco_atual - tp_price)

        if tp_distance / sl_distance >= self.min_rr_ratio:
            self.log_system.logar(f"\n🎯 EXECUTANDO {tipo}:", self.ativo)
            self.log_system.logar(f"ℹ️ Entrada: {preco_atual:.5f}", self.ativo)
            self.log_system.logar(f"ℹ️ Stop Loss: {sl_price:.5f}", self.ativo)
            self.log_system.logar(f"ℹ️ Take Profit: {tp_price:.5f}", self.ativo)
            self.log_system.logar(f"ℹ️ Risk/Reward: {tp_distance / sl_distance:.2f}", self.ativo)

            order_type = mt5.ORDER_TYPE_BUY if tipo == "COMPRA" else mt5.ORDER_TYPE_SELL
            self.abrir_ordem(order_type, sl_distance, tp_distance)
        else:
            self.log_system.logar(f"⚠️ RR muito baixo: {tp_distance / sl_distance:.2f}", self.ativo)

    def calcular_rsi(self, close, period=14):
        """Calcula o RSI"""
        delta = np.diff(close)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        avg_gain = np.mean(gain[:period])
        avg_loss = np.mean(loss[:period])

        for i in range(period, len(delta)):
            avg_gain = (avg_gain * (period - 1) + gain[i]) / period
            avg_loss = (avg_loss * (period - 1) + loss[i]) / period

        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        return np.array([rsi])

    def verificar_risco_posicao(self):
        """Verifica se pode abrir nova posição"""
        if mt5.positions_total() >= self.max_positions:
            self.log_system.logar("⚠️ Máximo de posições atingido", self.ativo)
            return False

        saldo_atual = mt5.account_info().equity
        drawdown = (self.saldo_inicial - saldo_atual) / self.saldo_inicial * 100

        if drawdown > self.risk_percent:
            self.log_system.logar(f"⚠️ Drawdown máximo atingido: {drawdown:.2f}%", self.ativo)
            return False

        return True

    def abrir_ordem(self, tipo_ordem, sl_distance, tp_distance):
        """Abre uma ordem no mercado"""
        tick = mt5.symbol_info_tick(self.ativo)
        preco = tick.ask if tipo_ordem == mt5.ORDER_TYPE_BUY else tick.bid
        point = mt5.symbol_info(self.ativo).point

        # Calcular volume baseado no risco percentual
        saldo = mt5.account_info().equity
        risco_valor = saldo * (self.risk_percent / 100)
        volume = risco_valor / (sl_distance * point)
        volume = round(max(mt5.symbol_info(self.ativo).volume_min, volume), 2)

        sl = preco - sl_distance * point if tipo_ordem == mt5.ORDER_TYPE_BUY else preco + sl_distance * point
        tp = preco + tp_distance * point if tipo_ordem == mt5.ORDER_TYPE_BUY else preco - tp_distance * point

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.ativo,
            "volume": volume,
            "type": tipo_ordem,
            "price": preco,
            "sl": sl,
            "tp": tp,
            "deviation": 10,
            "magic": 123456,
            "comment": "Fibonacci Strategy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        resultado = mt5.order_send(request)

        if resultado.retcode != mt5.TRADE_RETCODE_DONE:
            self.log_system.logar(f"❌ Erro ao enviar ordem: {resultado.comment}", self.ativo)
        else:
            self.ticket_atual = resultado.order
            self.log_system.logar(f"✅ Ordem executada: {volume} lotes", self.ativo)

    def parar(self):
        """Para a execução da estratégia"""
        with self.lock:
            self.operando = False
            self.log_system.logar(f"🛑 Parando estratégia para {self.ativo}", self.ativo)
</create_file>
