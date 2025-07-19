#!/usr/bin/env python3
"""
命令加载器 - 负责命令的动态加载和管理
"""

import os
import json
from typing import Dict, List, Optional, Any
from ..data.data_manager import DataManager, CacheManager

class CommandLoader:
    """命令加载器 - 实现懒加载和缓存管理"""
    
    def __init__(self, data_manager: DataManager = None):
        self.data_manager = data_manager or DataManager()
        self.cache_manager = CacheManager(max_size=50)  # 缓存最多50个命令
        self.load_stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'total_loads': 0
        }
    
    def load_command(self, command_name: str) -> Optional[Dict[str, Any]]:
        """加载单个命令，优先从缓存获取"""
        self.load_stats['total_loads'] += 1
        
        # 尝试从缓存获取
        cached_command = self.cache_manager.get(command_name)
        if cached_command:
            self.load_stats['cache_hits'] += 1
            return cached_command
        
        # 从数据管理器加载
        self.load_stats['cache_misses'] += 1
        command_data = self.data_manager.load_command(command_name)
        
        if command_data:
            # 添加到缓存
            self.cache_manager.put(command_name, command_data)
            return command_data
        
        return None
    
    def load_commands_batch(self, command_names: List[str]) -> Dict[str, Dict[str, Any]]:
        """批量加载命令"""
        results = {}
        
        for command_name in command_names:
            command_data = self.load_command(command_name)
            if command_data:
                results[command_name] = command_data
        
        return results
    
    def load_category_commands(self, category: str) -> Dict[str, Dict[str, Any]]:
        """加载指定分类的所有命令"""
        command_names = self.data_manager.get_commands_by_category(category)
        return self.load_commands_batch(command_names)
    
    def preload_frequently_used(self, command_list: List[str] = None):
        """预加载常用命令"""
        if command_list is None:
            # 默认预加载的常用命令
            command_list = [
                'ls', 'cd', 'pwd', 'cat', 'grep', 'find', 'ps', 'top', 
                'cp', 'mv', 'rm', 'mkdir', 'chmod', 'chown', 'tar'
            ]
        
        print(f"正在预加载 {len(command_list)} 个常用命令...")
        loaded_count = 0
        
        for command_name in command_list:
            if self.load_command(command_name):
                loaded_count += 1
        
        print(f"预加载完成，成功加载 {loaded_count} 个命令")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        stats = self.load_stats.copy()
        stats['cache_size'] = self.cache_manager.size()
        stats['cache_hit_rate'] = (
            stats['cache_hits'] / stats['total_loads'] * 100 
            if stats['total_loads'] > 0 else 0
        )
        return stats
    
    def clear_cache(self):
        """清空缓存"""
        self.cache_manager.clear()
        self.load_stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'total_loads': 0
        }
    
    def get_available_commands(self) -> List[str]:
        """获取所有可用命令列表"""
        return self.data_manager.get_command_list()
    
    def validate_command(self, command_name: str) -> bool:
        """验证命令是否存在"""
        return self.data_manager.get_command_file_path(command_name) is not None

if __name__ == "__main__":
    # 测试命令加载器
    loader = CommandLoader()
    
    print("测试命令加载器...")
    
    # 测试单个命令加载
    print("\n1. 加载单个命令 (ls):")
    ls_cmd = loader.load_command('ls')
    if ls_cmd:
        print(f"   命令: {ls_cmd['name']}")
        print(f"   描述: {ls_cmd['description']}")
    
    # 测试缓存命中
    print("\n2. 再次加载相同命令 (测试缓存):")
    ls_cmd2 = loader.load_command('ls')
    print(f"   命令加载成功: {ls_cmd2 is not None}")
    
    # 显示缓存统计
    print("\n3. 缓存统计:")
    stats = loader.get_cache_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # 测试批量加载
    print("\n4. 批量加载命令:")
    batch_commands = loader.load_commands_batch(['find', 'grep', 'awk'])
    print(f"   成功加载 {len(batch_commands)} 个命令")
    
    # 测试预加载
    print("\n5. 预加载常用命令:")
    loader.preload_frequently_used(['ps', 'top', 'df', 'free'])
    
    # 最终统计
    print("\n6. 最终缓存统计:")
    final_stats = loader.get_cache_stats()
    for key, value in final_stats.items():
        print(f"   {key}: {value}")