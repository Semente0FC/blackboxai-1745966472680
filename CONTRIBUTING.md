# Contributing to Future MT5 Pro Trading System

First off, thank you for considering contributing to Future MT5 Pro! It's people like you that make this project such a great tool.

## 📋 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps to reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible
* Include your environment details (OS, Python version, etc.)

### Suggesting Enhancements

If you have a suggestion for the project, we'd love to hear it! Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* A clear and descriptive title
* A detailed description of the proposed feature
* Explain why this enhancement would be useful
* List any potential drawbacks or challenges
* If possible, outline the implementation approach

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing style
6. Issue that pull request!

## 🔧 Development Setup

1. Clone your fork of the repo
   ```bash
   git clone https://github.com/YOUR_USERNAME/future-mt5-pro.git
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. Create a branch
   ```bash
   git checkout -b name-of-your-feature
   ```

## 📝 Style Guide

### Python Style Guide

* Follow PEP 8
* Use type hints
* Write docstrings for all public methods
* Keep lines under 100 characters
* Use meaningful variable names

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Documentation Style

* Use Markdown for documentation
* Include code examples where appropriate
* Keep explanations clear and concise
* Update the README.md if needed

## 🧪 Testing

* Write unit tests for new features
* Ensure all tests pass before submitting
* Include integration tests where appropriate
* Test edge cases thoroughly

### Running Tests
```bash
python -m pytest
```

## 📚 Documentation

* Update documentation for any changed functionality
* Include docstrings for all public methods
* Update the README.md if needed
* Add comments for complex code sections

## 🔄 Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the CHANGELOG.md with a note describing your changes
3. The PR will be merged once you have the sign-off of at least one maintainer

## 📌 Project Structure

```
future-mt5-pro/
├── config/              # Configuration files
├── docs/               # Documentation
├── src/                # Source code
│   ├── ui/            # User interface components
│   ├── trading/       # Trading logic
│   └── utils/         # Utility functions
├── tests/             # Test files
├── LICENSE            # License file
└── README.md          # Project documentation
```

## 🎯 Development Goals

1. Maintain high code quality
2. Improve test coverage
3. Enhance documentation
4. Add new features carefully
5. Keep the codebase maintainable

## 🤔 Questions?

Feel free to contact us if you have any questions:
* Email: support@blackboxai.com
* GitHub Issues: Create an issue in the repository

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---
Thank you for contributing to Future MT5 Pro! 🚀
