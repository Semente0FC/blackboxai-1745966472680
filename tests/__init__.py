"""
Test suite for Future MT5 Pro Trading System
"""

import unittest
import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

def load_tests(loader, standard_tests, pattern):
    """Load all test cases from the tests directory"""
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern='test_*.py')
    standard_tests.addTests(package_tests)
    return standard_tests

def run_tests():
    """Run all tests with coverage report"""
    try:
        import coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Run tests
        unittest.main(module=None, exit=False)
        
        # Generate coverage report
        cov.stop()
        cov.save()
        
        print("\nCoverage Report:")
        cov.report()
        
        # Generate HTML report
        cov.html_report(directory='htmlcov')
        print("\nDetailed HTML coverage report generated in htmlcov/index.html")
        
    except ImportError:
        print("\nCoverage package not found. Running tests without coverage report...")
        unittest.main(module=None)

# Test categories
TEST_CATEGORIES = {
    'trading': [
        'test_trading.py',
        'Trading strategy tests',
        ['Fibonacci analysis', 'Trade execution', 'Risk management']
    ],
    'utils': [
        'test_utils.py',
        'Utility function tests',
        ['MT5 connection', 'Data formatting', 'Calculations']
    ]
}

def run_category(category):
    """Run tests for a specific category"""
    if category not in TEST_CATEGORIES:
        print(f"Error: Category '{category}' not found")
        print("\nAvailable categories:")
        for cat, details in TEST_CATEGORIES.items():
            print(f"- {cat}: {details[1]}")
            print(f"  Tests: {', '.join(details[2])}")
        return
        
    test_file = TEST_CATEGORIES[category][0]
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.dirname(__file__), pattern=test_file)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

def list_categories():
    """List available test categories"""
    print("\nAvailable Test Categories:")
    print("=" * 50)
    for category, details in TEST_CATEGORIES.items():
        print(f"\n{category.upper()}")
        print("-" * len(category))
        print(f"Description: {details[1]}")
        print("Test areas:")
        for area in details[2]:
            print(f"- {area}")
    print("\nTo run tests for a specific category:")
    print("python -m unittest tests.<category>")
    print("\nTo run all tests:")
    print("python -m unittest discover")

# Test configuration
TEST_CONFIG = {
    'timeout': 30,  # seconds
    'verbosity': 2,
    'failfast': False,
    'buffer': True,
    'warnings': 'default'
}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--list':
            list_categories()
        else:
            run_category(sys.argv[1])
    else:
        run_tests()
