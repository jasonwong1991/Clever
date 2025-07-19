#!/usr/bin/env python3
"""
数据管理模块 - 负责加载和管理命令数据
"""

import os
import glob
from typing import Dict, List, Optional, Any
from pathlib import Path
from ..utils.file_utils import load_json_file, list_json_files
from ..utils.i18n import I18nManager

class DataManager:
    """数据管理器 - 负责JSON数据的加载、缓存和管理"""
    
    def __init__(self, data_dir: str = None):
        if data_dir:
            self.data_dir = data_dir
        else:
            # 获取src目录下的knowledge_base目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            src_dir = os.path.dirname(current_dir)
            self.data_dir = os.path.join(src_dir, 'knowledge_base')
        
        # 初始化国际化管理器
        self.i18n = I18nManager(self.data_dir)
        
        self.commands_cache = {}
        self.categories = {}
        self.search_mappings = {}
        self.meta = {}
        self._load_meta_data()
    
    def _load_meta_data(self):
        """加载元数据"""
        current_lang = self.i18n.get_language()
        self.meta = load_json_file(os.path.join(self.data_dir, f'meta_{current_lang}.json')) or {}
        self.categories = load_json_file(os.path.join(self.data_dir, f'categories_{current_lang}.json')) or {}
        self.search_mappings = load_json_file(os.path.join(self.data_dir, f'search_mappings_{current_lang}.json')) or {}
    
    def load_command(self, command_name: str) -> Optional[Dict[str, Any]]:
        """懒加载单个命令数据"""
        if command_name in self.commands_cache:
            return self.commands_cache[command_name]
        
        # 获取当前语言的命令目录
        current_lang = self.i18n.get_language()
        commands_dir = os.path.join(self.data_dir, f'commands_{current_lang}')
        
        # 在各个子目录中搜索命令文件
        subdirs = ['basic', 'advanced', 'tools', 'network', 'system', 'text', 'dev', 'version', 'container', 'compression', 'advanced_tools']
        for subdir in subdirs:
            command_file = os.path.join(commands_dir, subdir, f'{command_name}.json')
            if os.path.exists(command_file):
                command_data = load_json_file(command_file)
                if command_data:
                    self.commands_cache[command_name] = command_data
                    return command_data
        
        return None
    
    def load_all_commands(self) -> Dict[str, Dict[str, Any]]:
        """加载所有命令数据"""
        if len(self.commands_cache) > 0:
            return self.commands_cache
        
        # 获取当前语言的命令目录
        current_lang = self.i18n.get_language()
        commands_dir = os.path.join(self.data_dir, f'commands_{current_lang}')
        
        # 遍历所有子目录
        subdirs = ['basic', 'advanced', 'tools', 'network', 'system', 'text', 'dev', 'version', 'container', 'compression', 'advanced_tools']
        for subdir in subdirs:
            subdir_path = os.path.join(commands_dir, subdir)
            if not os.path.exists(subdir_path):
                continue
            
            # 加载该子目录下的所有JSON文件
            json_files = list_json_files(subdir_path)
            for json_file in json_files:
                command_name = os.path.splitext(os.path.basename(json_file))[0]
                command_data = load_json_file(json_file)
                if command_data:
                    self.commands_cache[command_name] = command_data
        
        return self.commands_cache
    
    def get_commands_by_category(self, category: str) -> List[str]:
        """根据分类获取命令列表"""
        if category in self.categories:
            return self.categories[category].get('commands', [])
        return []
    
    def get_all_categories(self) -> Dict[str, Dict[str, Any]]:
        """获取所有分类"""
        return self.categories
    
    def get_search_mappings(self) -> Dict[str, List[str]]:
        """获取搜索映射"""
        return self.search_mappings
    
    def get_command_list(self) -> List[str]:
        """获取所有可用命令列表"""
        self.load_all_commands()
        return list(self.commands_cache.keys())
    
    def validate_command_data(self, command_data: Dict[str, Any]) -> bool:
        """验证命令数据格式"""
        required_fields = ['name', 'description', 'category', 'usage']
        
        for field in required_fields:
            if field not in command_data:
                return False
        
        return True
    
    def get_meta_info(self) -> Dict[str, Any]:
        """获取元数据信息"""
        return self.meta
    
    def refresh_cache(self):
        """刷新缓存"""
        self.commands_cache.clear()
        self._load_meta_data()
    
    def get_command_file_path(self, command_name: str) -> Optional[str]:
        """获取命令文件路径"""
        current_lang = self.i18n.get_language()
        commands_dir = os.path.join(self.data_dir, f'commands_{current_lang}')
        
        subdirs = ['basic', 'advanced', 'tools', 'network', 'system', 'text', 'dev', 'version', 'container']
        for subdir in subdirs:
            command_file = os.path.join(commands_dir, subdir, f'{command_name}.json')
            if os.path.exists(command_file):
                return command_file
        return None
    
    def get_i18n_manager(self) -> I18nManager:
        """获取国际化管理器"""
        return self.i18n
    
    def set_language(self, language: str) -> bool:
        """设置语言并重新加载数据"""
        if self.i18n.set_language(language):
            # 清空缓存并重新加载元数据
            self.commands_cache.clear()
            self._load_meta_data()
            return True
        return False

class CacheManager:
    """缓存管理器 - 实现LRU缓存策略"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.cache = {}
        self.access_order = []
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存项"""
        if key in self.cache:
            # 更新访问顺序
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key: str, value: Any):
        """添加缓存项"""
        if key in self.cache:
            # 更新现有项
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            # 移除最久未使用的项
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
        
        self.cache[key] = value
        self.access_order.append(key)
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.access_order.clear()
    
    def size(self) -> int:
        """获取缓存大小"""
        return len(self.cache)

if __name__ == "__main__":
    # 测试数据管理器
    dm = DataManager()
    
    print("元数据信息:")
    print(json.dumps(dm.get_meta_info(), indent=2, ensure_ascii=False))
    
    print("\n加载命令: ls")
    ls_cmd = dm.load_command('ls')
    if ls_cmd:
        print(f"命令: {ls_cmd['name']}")
        print(f"描述: {ls_cmd['description']}")
    
    print(f"\n可用命令数量: {len(dm.get_command_list())}")