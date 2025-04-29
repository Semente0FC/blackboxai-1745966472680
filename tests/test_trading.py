"""
Unit tests for trading functionality
"""

import unittest
import numpy as np
from unittest.mock import Mock, patch
import MetaTrader5 as mt5

from estrategia import EstrategiaTrading

class TestEstrategiaTrading(unittest.TestCase):
    def setUp(self):
        """Setup test environment"""
        self.logger_mock = Mock()
        self.strategy = EstrategiaTrading(
            ativo="EURUSD",
            timeframe="M15",
            lote_base=0.1,
            log_system=self.logger_mock
        )
        
    def test_fibonacci_levels(self):
        """Test Fibonacci level calculations"""
        high = 1.2000
        low = 1.1000
        
        # Test uptrend levels
        levels = self.strategy.calcular_niveis_fibonacci(high, low, True)
        self.assertAlmostEqual(levels[0.382], 1.1618, places=4)
        self.assertAlmostEqual(levels[0.5], 1.1500, places=4)
        self.assertAlmostEqual(levels[0.618], 1.1382, places=4)
        
        # Test downtrend levels
        levels = self.strategy.calcular_niveis_fibonacci(high, low, False)
        self.assertAlmostEqual(levels[0.382], 1.1382, places=4)
        self.assertAlmostEqual(levels[0.5], 1.1500, places=4)
        self.assertAlmostEqual(levels[0.618], 1.1618, places=4)
        
    def test_trend_identification(self):
        """Test trend identification"""
        # Create mock data
        data = {
            'close': np.array([1.1000, 1.1100, 1.1200, 1.1300, 1.1400]),
            'high': np.array([1.1010, 1.1110, 1.1210, 1.1310, 1.1410]),
            'low': np.array([1.0990, 1.1090, 1.1190, 1.1290, 1.1390])
        }
        
        # Test uptrend
        trend, high, low = self.strategy.identificar_tendencia(data)
        self.assertEqual(trend, "ALTA")
        self.assertAlmostEqual(high, 1.1410, places=4)
        self.assertAlmostEqual(low, 1.0990, places=4)
        
        # Test downtrend
        data['close'] = np.array([1.1400, 1.1300, 1.1200, 1.1100, 1.1000])
        data['high'] = np.array([1.1410, 1.1310, 1.1210, 1.1110, 1.1010])
        data['low'] = np.array([1.1390, 1.1290, 1.1190, 1.1090, 1.0990])
        
        trend, high, low = self.strategy.identificar_tendencia(data)
        self.assertEqual(trend, "BAIXA")
        
    def test_rsi_calculation(self):
        """Test RSI calculation"""
        close_prices = np.array([
            44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42,
            45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28
        ])
        
        rsi = self.strategy.calcular_rsi(close_prices)
        self.assertGreaterEqual(rsi[-1], 0)
        self.assertLessEqual(rsi[-1], 100)
        
    @patch('MetaTrader5.positions_total')
    def test_risk_position(self, mock_positions):
        """Test risk position verification"""
        # Test max positions limit
        mock_positions.return_value = 5
        self.assertFalse(self.strategy.verificar_risco_posicao())
        
        # Test within limits
        mock_positions.return_value = 1
        self.assertTrue(self.strategy.verificar_risco_posicao())
        
    @patch('MetaTrader5.symbol_info_tick')
    @patch('MetaTrader5.symbol_info')
    @patch('MetaTrader5.order_send')
    def test_order_execution(self, mock_order, mock_info, mock_tick):
        """Test order execution"""
        # Setup mocks
        mock_tick.return_value = Mock(ask=1.2000, bid=1.1990)
        mock_info.return_value = Mock(point=0.0001)
        mock_order.return_value = Mock(retcode=mt5.TRADE_RETCODE_DONE)
        
        # Test buy order
        self.strategy.abrir_ordem(mt5.ORDER_TYPE_BUY, 0.001, 0.002)
        mock_order.assert_called_once()
        
        # Verify order parameters
        args = mock_order.call_args[0][0]
        self.assertEqual(args['action'], mt5.TRADE_ACTION_DEAL)
        self.assertEqual(args['type'], mt5.ORDER_TYPE_BUY)
        self.assertGreater(args['volume'], 0)

if __name__ == '__main__':
    unittest.main()
