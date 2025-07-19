#!/usr/bin/env python3
"""
CLI模块初始化
"""

from .parser import create_parser
from .formatter import OutputFormatter
from .interface import CleverCLI

__all__ = ['create_parser', 'OutputFormatter', 'CleverCLI']
