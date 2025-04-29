"""
Setup script for Future MT5 Pro Trading System
"""

import os
from setuptools import setup, find_packages

# Read version from __init__.py
with open(os.path.join('__init__.py'), 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'").strip('"')
            break

# Read README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='future-mt5-pro',
    version=version,
    author='BLACKBOXAI',
    author_email='support@blackboxai.com',
    description='Professional Fibonacci-based trading system for MetaTrader 5',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blackboxai/future-mt5-pro',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'MetaTrader5>=5.0.0',
        'numpy>=1.19.0',
        'pandas>=1.1.0',
        'matplotlib>=3.3.0',
        'Pillow>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'future-mt5=run:main',
        ],
    },
    include_package_data=True,
    package_data={
        'future_mt5_pro': [
            'config/*.json',
            'data/*',
            'logs/*',
        ],
    },
    data_files=[
        ('config', ['config/default_config.json']),
    ],
    project_urls={
        'Bug Reports': 'https://github.com/blackboxai/future-mt5-pro/issues',
        'Source': 'https://github.com/blackboxai/future-mt5-pro',
        'Documentation': 'https://future-mt5-pro.readthedocs.io/',
    },
)
