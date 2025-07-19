#!/usr/bin/env python3
"""
输出格式化器 - 负责美化终端输出
"""

import sys
from typing import Dict, Any
from ..utils.i18n import I18nManager


class OutputFormatter:
    """输出格式化器"""
    
    def __init__(self, i18n_manager: I18nManager = None):
        self.i18n = i18n_manager or I18nManager()
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
    
    def colorize(self, text: str, color: str) -> str:
        """为文本添加颜色"""
        return f"{self.colors.get(color, '')}{text}{self.colors['end']}"
    
    def display_command_info(self, command_data: Dict[str, Any]):
        """显示命令的详细信息"""
        command_name = command_data.get('command', command_data.get('name', 'Unknown'))
        print(f"{self.colorize(self.i18n.get_ui_text('command') + ':', 'bold')} {self.colorize(command_name, 'cyan')}")
        print(f"{self.colorize(self.i18n.get_ui_text('description') + ':', 'bold')} {command_data['description']}")
        print(f"{self.colorize(self.i18n.get_ui_text('category') + ':', 'bold')} {self.colorize(command_data['category'], 'magenta')}")
        
        # 显示语法/用法
        syntax = command_data.get('syntax', command_data.get('usage', ''))
        if syntax:
            print(f"{self.colorize(self.i18n.get_ui_text('usage') + ':', 'bold')} {syntax}")
        
        # 显示选项
        if 'options' in command_data and command_data['options']:
            print(f"\n{self.colorize(self.i18n.get_ui_text('options') + ':', 'bold')}")
            for option in command_data['options']:
                option_text = option.get('option', '')
                desc = option.get('description', '')
                print(f"  {self.colorize(option_text, 'green')}: {desc}")
        
        # 显示示例
        if 'examples' in command_data and command_data['examples']:
            print(f"\n{self.colorize(self.i18n.get_ui_text('examples') + ':', 'bold')}")
            for example in command_data['examples']:
                cmd = example.get('command', '')
                desc = example.get('description', '')
                print(f"  {self.colorize(cmd, 'yellow')}")
                if desc:
                    print(f"    {desc}")
        
        # 显示相关命令
        if 'related_commands' in command_data and command_data['related_commands']:
            print(f"\n{self.colorize(self.i18n.get_ui_text('related_commands') + ':', 'bold')}")
            related = ', '.join([self.colorize(cmd, 'cyan') for cmd in command_data['related_commands']])
            print(f"  {related}")
    
    def display_search_results(self, query: str, results: Dict[str, Any], processor):
        """显示搜索结果"""
        total_results = sum(len(cmds) for cmds in results.values())
        
        if total_results == 0:
            print(f"{self.colorize(self.i18n.get_ui_text('no_results'), 'red')}")
            return
        
        lang = self.i18n.get_language()
        if lang == 'zh':
            print(f"{self.colorize('搜索结果', 'bold')} (查询: '{query}', 共找到 {total_results} 个命令):")
        else:
            print(f"{self.colorize('Search Results', 'bold')} (Query: '{query}', Found {total_results} commands):")
        print("=" * 60)
        
        # 显示各类结果
        result_types = {}
        if lang == 'zh':
            result_types = {
                'exact_matches': ('🎯 精确匹配', 'green'),
                'name_matches': ('📝 名称匹配', 'cyan'),
                'keyword_matches': ('🔍 关键词匹配', 'yellow'),
                'tag_matches': ('🏷️ 标签匹配', 'magenta'),
                'similar_commands': ('🤔 相似命令', 'blue')
            }
        else:
            result_types = {
                'exact_matches': ('🎯 Exact Matches', 'green'),
                'name_matches': ('📝 Name Matches', 'cyan'),
                'keyword_matches': ('🔍 Keyword Matches', 'yellow'),
                'tag_matches': ('🏷️ Tag Matches', 'magenta'),
                'similar_commands': ('🤔 Similar Commands', 'blue')
            }
        
        for result_type, (title, color) in result_types.items():
            if result_type in results and results[result_type]:
                print(f"\n{self.colorize(title, color)}:")
                for cmd in results[result_type]:
                    cmd_data = processor.query_command(cmd)
                    if cmd_data:
                        print(f"  {self.colorize(cmd, 'cyan'):<12} - {cmd_data['description']}")
        
        print("\n" + "=" * 60)
        tip_text = self.i18n.get_ui_text('tip_use_help')
        if lang == 'zh':
            print(f"{self.colorize('提示:', 'bold')} 使用 'clever 命令名' 查看具体命令的详细用法")
        else:
            print(f"{self.colorize('Tip:', 'bold')} Use 'clever command_name' to view detailed usage")
    
    def display_category_commands(self, category: str, category_data: Dict[str, Any]):
        """显示分类中的所有命令"""
        if not category_data['commands']:
            lang = self.i18n.get_language()
            if lang == 'zh':
                print(f"{self.colorize('分类', 'red')} '{category}' {self.colorize('未找到', 'red')}")
            else:
                print(f"{self.colorize('Category', 'red')} '{category}' {self.colorize('not found', 'red')}")
            return
        
        lang = self.i18n.get_language()
        if lang == 'zh':
            print(f"{self.colorize(category, 'bold')} 类命令 (共 {category_data['total_count']} 个):")
        else:
            print(f"{self.colorize(category, 'bold')} Commands ({category_data['total_count']} total):")
        print("-" * 50)
        
        for cmd_name, cmd_data in category_data['commands'].items():
            print(f"  {self.colorize(cmd_name, 'cyan'):<12} - {cmd_data['description']}")
    
    def display_all_commands(self, categories: Dict[str, Any], processor):
        """显示所有命令"""
        print(f"{self.colorize(self.i18n.get_ui_text('available_commands') + ':', 'bold')}")
        print("=" * 60)
        
        for category, category_info in categories.items():
            print(f"\n{self.colorize(category, 'magenta')}:")
            if isinstance(category_info, dict) and 'commands' in category_info:
                for cmd_name in category_info['commands']:
                    cmd_data = processor.query_command(cmd_name)
                    if cmd_data:
                        print(f"  {self.colorize(cmd_name, 'cyan'):<12} - {cmd_data['description']}")
    
    def display_categories(self, categories: Dict[str, Any]):
        """显示所有分类"""
        lang = self.i18n.get_language()
        if lang == 'zh':
            print(f"{self.colorize('可用的命令分类:', 'bold')}")
        else:
            print(f"{self.colorize('Available Command Categories:', 'bold')}")
        print("-" * 30)
        
        for category, category_info in categories.items():
            if isinstance(category_info, dict):
                desc = category_info.get('description', '')
                count = len(category_info.get('commands', []))
                if lang == 'zh':
                    print(f"  {self.colorize(category, 'magenta'):<15} - {desc} ({count}个命令)")
                else:
                    print(f"  {self.colorize(category, 'magenta'):<15} - {desc} ({count} commands)")
    
    def display_stats(self, stats: Dict[str, Any]):
        """显示系统统计信息"""
        lang = self.i18n.get_language()
        if lang == 'zh':
            print(f"{self.colorize('系统统计信息:', 'bold')}")
            print("-" * 40)
            print(f"数据版本: {stats['data_manager']['version']}")
            print(f"总命令数: {stats['total_commands']}")
            print(f"缓存命中率: {stats['command_loader']['cache_hit_rate']:.1f}%")
            print(f"缓存大小: {stats['command_loader']['cache_size']}")
            print(f"索引词数: {stats['search_engine']['total_words']}")
            print(f"索引标签数: {stats['search_engine']['total_tags']}")
            print(f"最后更新: {stats['data_manager']['last_updated']}")
        else:
            print(f"{self.colorize('System Statistics:', 'bold')}")
            print("-" * 40)
            print(f"Data version: {stats['data_manager']['version']}")
            print(f"Total commands: {stats['total_commands']}")
            print(f"Cache hit rate: {stats['command_loader']['cache_hit_rate']:.1f}%")
            print(f"Cache size: {stats['command_loader']['cache_size']}")
            print(f"Index words: {stats['search_engine']['total_words']}")
            print(f"Index tags: {stats['search_engine']['total_tags']}")
            print(f"Last updated: {stats['data_manager']['last_updated']}")
    
    def display_similar_commands(self, command_name: str, similar_commands: list):
        """显示相似命令建议"""
        lang = self.i18n.get_language()
        if lang == 'zh':
            print(f"{self.colorize('命令', 'red')} '{command_name}' {self.colorize('未找到', 'red')}")
            print(f"\n{self.colorize('您是否要查询以下相似命令:', 'yellow')}")
        else:
            print(f"{self.colorize('Command', 'red')} '{command_name}' {self.colorize('not found', 'red')}")
            print(f"\n{self.colorize('Did you mean one of these similar commands:', 'yellow')}")
        
        for i, cmd_info in enumerate(similar_commands[:5], 1):
            print(f"  {i}. {self.colorize(cmd_info['command'], 'cyan')} - {cmd_info['description']}")
    
    def display_error(self, message: str):
        """显示错误信息"""
        lang = self.i18n.get_language()
        error_text = "错误:" if lang == 'zh' else "Error:"
        print(f"{self.colorize(error_text, 'red')} {message}")
    
    def display_info(self, message: str):
        """显示提示信息"""
        lang = self.i18n.get_language()
        info_text = "信息:" if lang == 'zh' else "Info:"
        print(f"{self.colorize(info_text, 'green')} {message}")
    
    def display_warning(self, message: str):
        """显示警告信息"""
        lang = self.i18n.get_language()
        warning_text = "警告:" if lang == 'zh' else "Warning:"
        print(f"{self.colorize(warning_text, 'yellow')} {message}")