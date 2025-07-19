#!/usr/bin/env python3
"""
命令行界面主类
"""

import sys
from ..core.query_processor import QueryProcessor
from .formatter import OutputFormatter
from ..utils.i18n import I18nManager


class CleverCLI:
    """命令行界面类"""
    
    def __init__(self):
        self.i18n = I18nManager()
        self.processor = QueryProcessor()
        self.formatter = OutputFormatter(self.i18n)
    
    def handle_command_query(self, command_name: str):
        """处理命令查询"""
        command_data = self.processor.query_command(command_name)
        
        if not command_data:
            # 查找相似命令
            similar_commands = self.processor.find_similar_commands(command_name)
            if similar_commands:
                self.formatter.display_similar_commands(command_name, similar_commands)
                
                # 在交互模式下询问用户
                if sys.stdin.isatty():
                    try:
                        lang = self.i18n.get_language()
                        if lang == 'zh':
                            choice = input(f"\n请输入序号(1-{len(similar_commands[:5])})，或直接输入命令名: ").strip()
                        else:
                            choice = input(f"\nEnter number (1-{len(similar_commands[:5])}) or command name directly: ").strip()
                            
                        if choice.isdigit():
                            choice_idx = int(choice) - 1
                            if 0 <= choice_idx < len(similar_commands[:5]):
                                self.handle_command_query(similar_commands[choice_idx]['command'])
                                return
                        elif self.processor.validate_command(choice):
                            self.handle_command_query(choice)
                            return
                    except (KeyboardInterrupt, EOFError):
                        exit_text = "退出" if self.i18n.get_language() == 'zh' else "Exit"
                        print(f"\n{exit_text}")
                        return
                
                # 非交互模式，显示最相似的命令
                lang = self.i18n.get_language()
                suggest_text = "建议您使用:" if lang == 'zh' else "Suggested command:"
                print(f"\n{self.formatter.colorize(suggest_text, 'green')} {similar_commands[0]['command']}")
                self.handle_command_query(similar_commands[0]['command'])
            else:
                lang = self.i18n.get_language()
                if lang == 'zh':
                    self.formatter.display_error(f"命令 '{command_name}' 未找到，也没有找到相似的命令")
                else:
                    self.formatter.display_error(f"Command '{command_name}' not found, and no similar commands found")
            return
        
        self.formatter.display_command_info(command_data)
    
    def handle_search(self, query: str):
        """处理搜索请求"""
        results = self.processor.search_commands(query)
        self.formatter.display_search_results(query, results, self.processor)
    
    def handle_category(self, category: str):
        """处理分类查询，支持模糊搜索"""
        # 首先尝试精确匹配
        category_data = self.processor.get_category_commands(category)
        
        # 如果精确匹配成功，直接显示结果
        if category_data and category_data.get('commands'):
            self.formatter.display_category_commands(category, category_data)
            return
        
        # 精确匹配失败，尝试模糊匹配分类
        similar_categories = self.processor.find_similar_categories(category)
        
        if similar_categories:
            lang = self.i18n.get_language()
            
            # 显示找到的相似分类
            if lang == 'zh':
                print(f"{self.formatter.colorize('未找到精确分类', 'yellow')} '{category}'")
                print(f"{self.formatter.colorize('找到相似分类:', 'green')}")
            else:
                print(f"{self.formatter.colorize('Exact category not found', 'yellow')} '{category}'")
                print(f"{self.formatter.colorize('Similar categories found:', 'green')}")
            
            for i, (cat_name, similarity) in enumerate(similar_categories[:5], 1):
                print(f"  {i}. {self.formatter.colorize(cat_name, 'cyan')} (相似度: {similarity:.2f})")
            
            # 在交互模式下询问用户选择
            if sys.stdin.isatty():
                try:
                    if lang == 'zh':
                        choice = input(f"\n请输入序号(1-{len(similar_categories[:5])})，或直接输入分类名: ").strip()
                    else:
                        choice = input(f"\nEnter number (1-{len(similar_categories[:5])}) or category name directly: ").strip()
                        
                    if choice.isdigit():
                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(similar_categories[:5]):
                            selected_category = similar_categories[choice_idx][0]
                            self.handle_category(selected_category)
                            return
                    else:
                        # 用户直接输入分类名
                        self.handle_category(choice)
                        return
                except (KeyboardInterrupt, EOFError):
                    exit_text = "退出" if lang == 'zh' else "Exit"
                    print(f"\n{exit_text}")
                    return
            
            # 非交互模式，自动选择最相似的分类
            best_match = similar_categories[0][0]
            suggest_text = "自动选择最相似的分类:" if lang == 'zh' else "Auto-selecting most similar category:"
            print(f"\n{self.formatter.colorize(suggest_text, 'green')} {best_match}")
            self.handle_category(best_match)
        else:
            # 完全没有找到相似分类
            lang = self.i18n.get_language()
            if lang == 'zh':
                self.formatter.display_error(f"分类 '{category}' 未找到，也没有找到相似的分类")
                print(f"{self.formatter.colorize('提示:', 'yellow')} 使用 --categories 查看所有可用分类")
            else:
                self.formatter.display_error(f"Category '{category}' not found, and no similar categories found")
                print(f"{self.formatter.colorize('Hint:', 'yellow')} Use --categories to view all available categories")
    
    def handle_list_all(self):
        """处理列出所有命令"""
        categories = self.processor.get_all_categories()
        self.formatter.display_all_commands(categories, self.processor)
    
    def handle_list_categories(self):
        """处理列出所有分类"""
        categories = self.processor.get_all_categories()
        self.formatter.display_categories(categories)
    
    def handle_stats(self):
        """处理统计信息显示"""
        stats = self.processor.get_system_stats()
        self.formatter.display_stats(stats)
    
    def handle_refresh(self):
        """处理数据刷新"""
        lang = self.i18n.get_language()
        if lang == 'zh':
            self.formatter.display_info("正在刷新数据缓存...")
            self.processor.refresh_data()
            self.formatter.display_info("数据缓存刷新完成")
        else:
            self.formatter.display_info("Refreshing data cache...")
            self.processor.refresh_data()
            self.formatter.display_info("Data cache refresh completed")
    
    def handle_language_change(self, new_language: str):
        """处理语言切换"""
        current_lang = self.i18n.get_language()
        
        if current_lang == new_language:
            if new_language == 'zh':
                self.formatter.display_info(f"当前已经是中文界面")
            else:
                self.formatter.display_info(f"Already using English interface")
            return
        
        # 切换语言
        if self.i18n.set_language(new_language):
            # 重新初始化formatter以使用新语言
            self.formatter = OutputFormatter(self.i18n)
            
            if new_language == 'zh':
                self.formatter.display_info("语言已切换为中文")
            else:
                self.formatter.display_info("Language switched to English")
                
            # 刷新数据管理器以加载新语言的数据
            self.processor.data_manager.set_language(new_language)
        else:
            if current_lang == 'zh':
                self.formatter.display_error(f"不支持的语言: {new_language}")
            else:
                self.formatter.display_error(f"Unsupported language: {new_language}")