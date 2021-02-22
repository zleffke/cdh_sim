#!/usr/bin/env python
"""
    Remote Relay Daemon.
"""

try:
    import setuptools
except ImportError:
    print("=========================================================")
    print(" CDH SIM requires setuptools for installing              ")
    print(" You can install setuptools using pip:                   ")
    print("    $ pip install setuptools                             ")
    print("=========================================================")
    exit(1)


from setuptools import setup
import vcc

setup(
    name         = 'CDH SIM', # This is the name of your PyPI-package.
    version      = __version__,
    url          = __url__,
    author       = __author__,
    author_email = __email__,
    #scripts=['relay_daemon']  # executable name  
    entry_points ={
        "console_scripts": ["cdh_sim = cdh_sim.main:main"]
    }
)
