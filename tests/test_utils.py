"""
Unit tests for utility functions
"""

import unittest
from unittest.mock import Mock, patch
import MetaTrader5 as mt5
from datetime import datetime, time
from utils import (
    initialize_mt5, get_account_info, format_currency,
    check_market_hours, calculate_position_size, cleanup_mt5,
    get_symbol_info, format_error_message, log_trade_result
)

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Setup test environment"""
        self.account_mock = Mock(
            login=12345,
            server="TestServer",
            balance=10000.0,
            equity=10500.0,
            margin=1000.0,
            margin_free=9500.0,
            profit=500.0
        )
        
        self.symbol_mock = Mock(
            name="EURUSD",
            description="Euro vs US Dollar",
            currency_base="EUR",
            currency_profit="USD",
            digits=5,
            point=0.00001,
            trade_tick_size=0.00001,
            trade_contract_size=100000.0,
            volume_min=0.01,
            volume_max=100.0,
            volume_step=0.01
        )

    def test_format_currency(self):
        """Test currency formatting"""
        test_cases = [
            (1234.5678, "$1,234.57"),
            (0, "$0.00"),
            (-1234.56, "-$1,234.56"),
            (1000000.00, "$1,000,000.00"),
            (0.01, "$0.01")
        ]
        
        for value, expected in test_cases:
            with self.subTest(value=value):
                self.assertEqual(format_currency(value), expected)

    def test_check_market_hours(self):
        """Test market hours checking"""
        test_times = [
            # During market hours
            (datetime(2024, 1, 1, 10, 30), True),  # 10:30 AM
            (datetime(2024, 1, 1, 14, 0), True),   # 2:00 PM
            # Outside market hours
            (datetime(2024, 1, 1, 8, 30), False),  # 8:30 AM
            (datetime(2024, 1, 1, 18, 0), False),  # 6:00 PM
            (datetime(2024, 1, 1, 0, 0), False),   # Midnight
        ]
        
        for test_time, expected in test_times:
            with self.subTest(time=test_time.strftime("%H:%M")):
                with patch('datetime.datetime') as mock_dt:
                    mock_dt.now.return_value = test_time
                    self.assertEqual(check_market_hours(), expected)

    @patch('MetaTrader5.initialize')
    @patch('MetaTrader5.login')
    @patch('MetaTrader5.account_info')
    def test_initialize_mt5(self, mock_account, mock_login, mock_init):
        """Test MT5 initialization"""
        test_cases = [
            # All successful
            (True, True, self.account_mock, True, "success"),
            # Init fails
            (False, True, self.account_mock, False, "failed"),
            # Login fails
            (True, False, self.account_mock, False, "login"),
            # No account info
            (True, True, None, False, "account")
        ]
        
        for init_result, login_result, account_result, expected_success, expected_message_contains in test_cases:
            with self.subTest(init=init_result, login=login_result, account=bool(account_result)):
                mock_init.return_value = init_result
                mock_login.return_value = login_result
                mock_account.return_value = account_result
                
                success, message = initialize_mt5()
                self.assertEqual(success, expected_success)
                self.assertIn(expected_message_contains.lower(), message.lower())

    @patch('MetaTrader5.account_info')
    def test_get_account_info(self, mock_account):
        """Test account info retrieval"""
        # Test successful retrieval
        mock_account.return_value = self.account_mock
        info = get_account_info()
        
        self.assertIsNotNone(info)
        self.assertEqual(info['login'], 12345)
        self.assertEqual(info['balance'], 10000.0)
        self.assertEqual(info['equity'], 10500.0)
        self.assertEqual(info['profit'], 500.0)
        
        # Test failed retrieval
        mock_account.return_value = None
        info = get_account_info()
        self.assertIsNone(info)

    @patch('MetaTrader5.symbol_info')
    def test_calculate_position_size(self, mock_symbol):
        """Test position size calculation"""
        mock_symbol.return_value = self.symbol_mock
        
        test_cases = [
            # Normal case
            (10000.0, 2.0, 100, 0.2),
            # Minimum lot
            (100.0, 0.1, 10, 0.01),
            # Maximum lot
            (1000000.0, 10.0, 1000, 100.0),
            # Zero risk
            (10000.0, 0.0, 100, 0.01),
            # Invalid stop loss
            (10000.0, 2.0, 0, 0.01)
        ]
        
        for balance, risk_percent, stop_loss_points, expected_min in test_cases:
            with self.subTest(balance=balance, risk=risk_percent, sl=stop_loss_points):
                size = calculate_position_size(balance, risk_percent, stop_loss_points, "EURUSD")
                self.assertGreaterEqual(size, expected_min)
                self.assertLessEqual(size, 100.0)
                self.assertEqual(size % 0.01, 0)  # Check lot step

    @patch('MetaTrader5.symbol_info')
    def test_get_symbol_info(self, mock_symbol):
        """Test symbol info retrieval"""
        # Test successful retrieval
        mock_symbol.return_value = self.symbol_mock
        info = get_symbol_info("EURUSD")
        
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], "EURUSD")
        self.assertEqual(info['digits'], 5)
        self.assertEqual(info['point'], 0.00001)
        
        # Test failed retrieval
        mock_symbol.return_value = None
        info = get_symbol_info("INVALID")
        self.assertIsNone(info)

    def test_format_error_message(self):
        """Test error message formatting"""
        test_cases = [
            (mt5.TRADE_RETCODE_DONE, "success"),
            (mt5.TRADE_RETCODE_REJECT, "reject"),
            (mt5.TRADE_RETCODE_INVALID, "invalid"),
            (9999, "unknown")
        ]
        
        for code, expected in test_cases:
            with self.subTest(code=code):
                message = format_error_message(code)
                self.assertIn(expected.lower(), message.lower())

    def test_log_trade_result(self):
        """Test trade result logging"""
        # Test successful trade
        result = Mock(retcode=mt5.TRADE_RETCODE_DONE)
        success, message = log_trade_result(result)
        self.assertTrue(success)
        self.assertIn("success", message.lower())
        
        # Test failed trade
        result = Mock(retcode=mt5.TRADE_RETCODE_REJECT)
        success, message = log_trade_result(result)
        self.assertFalse(success)
        self.assertIn("reject", message.lower())

    @patch('MetaTrader5.shutdown')
    def test_cleanup_mt5(self, mock_shutdown):
        """Test MT5 cleanup"""
        cleanup_mt5()
        mock_shutdown.assert_called_once()

if __name__ == '__main__':
    unittest.main()
