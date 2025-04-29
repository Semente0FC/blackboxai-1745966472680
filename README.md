# Future MT5 Pro Trading System

Professional Fibonacci-based trading system for MetaTrader 5.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Version](https://img.shields.io/badge/version-2.0.0-green.svg)

## 🚀 Features

- Professional dark theme interface
- Advanced Fibonacci analysis
- Real-time market monitoring
- Risk management system
- Detailed trading logs
- Customizable settings

## 📋 Requirements

- Python 3.8 or higher
- MetaTrader 5
- Required Python packages:
  ```
  MetaTrader5>=5.0.0
  numpy>=1.19.0
  pandas>=1.1.0
  matplotlib>=3.3.0
  Pillow>=8.0.0
  ```

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/blackboxai/future-mt5-pro.git
   cd future-mt5-pro
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

## 🎮 Usage

1. Start MetaTrader 5 and log in to your account

2. Run the application:
   ```bash
   python run.py
   ```

3. Configure trading parameters:
   - Select trading asset
   - Choose timeframe
   - Set lot size
   - Adjust risk parameters

4. Click START to begin trading

## 💹 Trading Strategy

The system uses a professional Fibonacci-based strategy:

### Trend Detection
- Minimum 2% price movement
- Volume confirmation
- MA200 filter (optional)

### Entry Conditions
- Fibonacci retracement levels (38.2%, 50%, 61.8%)
- RSI confirmation
- Volume analysis

### Exit Strategy
- Fibonacci extension targets (127.2%, 161.8%)
- Trailing stop system
- Risk/Reward optimization

## ⚙️ Configuration

Edit `config/user_config.json` to customize:

### Trading Parameters
```json
{
    "trading": {
        "default_lot": 0.1,
        "risk_percent": 2.0,
        "max_positions": 1,
        "min_rr_ratio": 2.0
    }
}
```

### Fibonacci Settings
```json
{
    "fibonacci": {
        "period": 20,
        "min_trend_percent": 2.0,
        "retracement_levels": [0.382, 0.5, 0.618],
        "extension_levels": [1.272, 1.618]
    }
}
```

### Market Hours
```json
{
    "market_hours": {
        "open": {
            "hour": 9,
            "minute": 0
        },
        "close": {
            "hour": 17,
            "minute": 30
        }
    }
}
```

## 🔒 Security

- Secure MT5 connection handling
- Encrypted credential storage
- Safe trade execution
- Error handling and validation

## 📊 Risk Management

- Position sizing based on account equity
- Maximum drawdown protection
- Risk per trade limits
- Multiple position management

## 🎯 Features

### Professional Interface
- Modern dark theme
- Real-time updates
- Status indicators
- Detailed logging

### Trading Tools
- Asset selection
- Timeframe control
- Lot size management
- Market analysis panel

### Analysis Features
- Fibonacci levels display
- Trend detection
- Technical indicators
- Volume analysis

## 🤝 Support

For support, please contact:
- Email: support@blackboxai.com
- Website: www.blackboxai.com

## 📝 License

Copyright © 2024 BLACKBOXAI

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

Trading involves substantial risk. This software is for educational purposes only. Always test thoroughly before live trading.

## 🔄 Updates

Check for updates regularly to ensure optimal performance and security.

## 🌟 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 Changelog

### Version 2.0.0
- Complete rewrite with professional UI
- Advanced Fibonacci analysis
- Improved risk management
- Real-time market monitoring

### Version 1.0.0
- Initial release
- Basic trading functionality
- Simple interface

## 🏆 Acknowledgments

- MetaTrader 5 Team
- Python Trading Community
- All contributors

---
Made with ❤️ by BLACKBOXAI
