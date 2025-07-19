#!/usr/bin/env python3
"""
命令行参数解析器
"""

import argparse
from ..utils.i18n import I18nManager


def create_parser():
    """创建命令行参数解析器"""
    i18n = I18nManager()
    lang = i18n.get_language()
    
    if lang == 'zh':
        description = "Linux命令查询工具 (重构版本)"
        epilog = """
示例:
  clever ls                    # 查询ls命令
  clever -s file              # 搜索包含'file'的命令
  clever -c 文件管理          # 显示文件管理类命令
  clever -l                   # 列出所有命令
  clever --stats              # 显示系统统计
        """
        help_command = '要查询的命令名'
        help_search = '搜索包含关键词的命令'
        help_category = '按分类查询命令'
        help_list = '列出所有可用命令'
        help_categories = '列出所有命令分类'
        help_stats = '显示系统统计信息'
        help_refresh = '刷新数据缓存'
    else:
        description = "Linux Command Query Tool (Refactored Version)"
        epilog = """
Examples:
  clever ls                    # Query ls command
  clever -s file              # Search commands containing 'file'
  clever -c file_management   # Show file management commands
  clever -l                   # List all commands
  clever --stats              # Show system statistics
        """
        help_command = 'Command name to query'
        help_search = 'Search commands containing keyword'
        help_category = 'Query commands by category'
        help_list = 'List all available commands'
        help_categories = 'List all command categories'
        help_stats = 'Show system statistics'
        help_refresh = 'Refresh data cache'
    
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog
    )
    
    parser.add_argument('command', nargs='?', help=help_command)
    parser.add_argument('-s', '--search', help=help_search)
    parser.add_argument('-c', '--category', help=help_category)
    parser.add_argument('-l', '--list', action='store_true', help=help_list)
    parser.add_argument('--categories', action='store_true', help=help_categories)
    parser.add_argument('--stats', action='store_true', help=help_stats)
    parser.add_argument('--refresh', action='store_true', help=help_refresh)
    parser.add_argument('--lang', choices=['zh', 'en'], help='Set language / 设置语言')
    
    return parser