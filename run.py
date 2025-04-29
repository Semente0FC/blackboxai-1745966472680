#!/usr/bin/env python3
"""
Future MT5 Pro Trading System
Launch script for the trading application
"""

import os
import sys
import traceback
from typing import Optional, Tuple

def check_python_version() -> Tuple[bool, Optional[str]]:
    """Check if Python version meets requirements"""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        return False, f"Python {required_version[0]}.{required_version[1]} or higher is required"
    return True, None

def check_dependencies() -> Tuple[bool, Optional[str]]:
    """Check if all required packages are installed"""
    required_packages = {
        'MetaTrader5': 'MetaTrader5',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'Pillow': 'PIL'
    }
    
    missing = []
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)
            
    if missing:
        return False, f"Missing required packages: {', '.join(missing)}"
    return True, None

def setup_environment() -> Tuple[bool, Optional[str]]:
    """Setup the environment for the application"""
    try:
        # Add current directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
            
        # Create required directories
        dirs = ['logs', 'data', 'config']
        for dir_name in dirs:
            os.makedirs(os.path.join(current_dir, dir_name), exist_ok=True)
            
        return True, None
    except Exception as e:
        return False, f"Failed to setup environment: {str(e)}"

def main():
    """Main entry point"""
    print("\nFuture MT5 Pro Trading System")
    print("Initializing...\n")
    
    # Check Python version
    success, message = check_python_version()
    if not success:
        print(f"❌ Error: {message}")
        sys.exit(1)
    print("✅ Python version check passed")
    
    # Check dependencies
    success, message = check_dependencies()
    if not success:
        print(f"❌ Error: {message}")
        print("\nPlease install required packages:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    print("✅ Dependencies check passed")
    
    # Setup environment
    success, message = setup_environment()
    if not success:
        print(f"❌ Error: {message}")
        sys.exit(1)
    print("✅ Environment setup complete")
    
    try:
        # Import and run application
        from main import main as run_app
        print("\n🚀 Launching application...\n")
        run_app()
        
    except ImportError as e:
        print(f"\n❌ Error importing application: {str(e)}")
        print("Please ensure all files are in the correct location.")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error running application:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error:")
        traceback.print_exc()
        sys.exit(1)
