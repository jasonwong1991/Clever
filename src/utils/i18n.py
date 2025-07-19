#!/usr/bin/env python3
"""
国际化支持模块 - 语言检测、配置和翻译管理
"""

import os
import locale
import json
from typing import Dict, Optional, Any
from pathlib import Path

class I18nManager:
    """国际化管理器"""
    
    def __init__(self, knowledge_base_dir: str = None):
        if knowledge_base_dir:
            self.kb_dir = knowledge_base_dir
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.kb_dir = os.path.join(os.path.dirname(current_dir), 'knowledge_base')
        
        self.config_file = os.path.join(self.kb_dir, 'i18n_config.json')
        self.supported_languages = ['zh', 'en']
        self.default_language = 'zh'
        self.current_language = None
        self._load_config()
    
    def _load_config(self):
        """加载国际化配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_language = config.get('language', self.default_language)
            except:
                self.current_language = self.default_language
        else:
            # 首次运行，检测系统语言
            self.current_language = self._detect_system_language()
            self._save_config()
    
    def _detect_system_language(self) -> str:
        """检测系统语言"""
        try:
            # 获取系统locale
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                # 提取语言代码
                lang_code = system_locale.split('_')[0].lower()
                if lang_code in self.supported_languages:
                    return lang_code
                elif lang_code in ['zh', 'cn']:
                    return 'zh'
                elif lang_code in ['en', 'us', 'gb']:
                    return 'en'
        except:
            pass
        
        # 检查环境变量
        for env_var in ['LANG', 'LANGUAGE', 'LC_ALL']:
            env_value = os.environ.get(env_var, '')
            if 'zh' in env_value.lower() or 'cn' in env_value.lower():
                return 'zh'
            elif 'en' in env_value.lower():
                return 'en'
        
        return self.default_language
    
    def _save_config(self):
        """保存国际化配置"""
        config = {
            'language': self.current_language,
            'supported_languages': self.supported_languages,
            'last_updated': self._get_timestamp()
        }
        
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save i18n config: {e}")
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_language(self) -> str:
        """获取当前语言"""
        return self.current_language
    
    def set_language(self, language: str) -> bool:
        """设置语言"""
        if language in self.supported_languages:
            self.current_language = language
            self._save_config()
            return True
        return False
    
    def get_knowledge_base_path(self) -> str:
        """获取当前语言的知识库路径"""
        return os.path.join(self.kb_dir, f'commands_{self.current_language}')
    
    def get_meta_file_path(self, filename: str) -> str:
        """获取元数据文件路径"""
        lang_filename = f"{filename.replace('.json', '')}_{self.current_language}.json"
        return os.path.join(self.kb_dir, lang_filename)
    
    def is_first_run(self) -> bool:
        """检查是否首次运行"""
        return not os.path.exists(self.config_file)
    
    def get_ui_text(self, key: str) -> str:
        """获取界面文本（简单实现）"""
        ui_texts = {
            'zh': {
                'command': '命令',
                'description': '描述',
                'category': '分类',
                'usage': '用法',
                'options': '选项',
                'examples': '示例',
                'related_commands': '相关命令',
                'search_results': '搜索结果',
                'available_commands': '所有可用命令',
                'no_results': '未找到匹配的命令',
                'error_command_not_found': '错误: 命令未找到',
                'tip_use_help': '提示: 使用 --help 查看帮助信息'
            },
            'en': {
                'command': 'Command',
                'description': 'Description', 
                'category': 'Category',
                'usage': 'Usage',
                'options': 'Options',
                'examples': 'Examples',
                'related_commands': 'Related Commands',
                'search_results': 'Search Results',
                'available_commands': 'Available Commands',
                'no_results': 'No matching commands found',
                'error_command_not_found': 'Error: Command not found',
                'tip_use_help': 'Tip: Use --help for help information'
            }
        }
        
        return ui_texts.get(self.current_language, ui_texts['zh']).get(key, key)

if __name__ == "__main__":
    # 测试国际化管理器
    i18n = I18nManager()
    
    print(f"Current language: {i18n.get_language()}")
    print(f"Is first run: {i18n.is_first_run()}")
    print(f"Knowledge base path: {i18n.get_knowledge_base_path()}")
    print(f"UI text 'command': {i18n.get_ui_text('command')}")
    
    # 测试语言切换
    print(f"\nSwitching to English...")
    i18n.set_language('en')
    print(f"Current language: {i18n.get_language()}")
    print(f"UI text 'command': {i18n.get_ui_text('command')}")