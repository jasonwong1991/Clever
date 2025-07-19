#!/usr/bin/env python3
"""
查询处理器 - 统一的查询处理接口
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from ..data.data_manager import DataManager
from ..core.command_loader import CommandLoader
from ..core.search_engine import SearchEngine

class QueryProcessor:
    """查询处理器 - 统一处理各种查询请求"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.command_loader = CommandLoader(self.data_manager)
        self.search_engine = SearchEngine(self.data_manager, self.command_loader)
    
    def query_command(self, command_name: str) -> Optional[Dict[str, Any]]:
        """查询单个命令的详细信息"""
        return self.command_loader.load_command(command_name)
    
    def search_commands(self, query: str, search_type: str = 'enhanced') -> Dict[str, Any]:
        """搜索命令"""
        if search_type == 'enhanced':
            return self.search_engine.enhanced_search(query)
        elif search_type == 'name':
            return {'name_matches': self.search_engine.search_by_name(query)}
        elif search_type == 'keyword':
            return self.search_engine.search_by_keyword(query)
        else:
            return self.search_engine.enhanced_search(query)
    
    def get_category_commands(self, category: str) -> Dict[str, Any]:
        """获取分类下的所有命令"""
        command_names = self.data_manager.get_commands_by_category(category)
        commands = {}
        
        for command_name in command_names:
            command_data = self.command_loader.load_command(command_name)
            if command_data:
                commands[command_name] = command_data
        
        return {
            'category': category,
            'commands': commands,
            'total_count': len(commands)
        }
    
    def get_all_categories(self) -> Dict[str, Any]:
        """获取所有分类信息"""
        return self.data_manager.get_all_categories()
    
    def get_command_list(self) -> List[str]:
        """获取所有可用命令列表"""
        return self.data_manager.get_command_list()
    
    def get_search_suggestions(self, partial_query: str) -> List[str]:
        """获取搜索建议"""
        return self.search_engine.get_search_suggestions(partial_query)
    
    def find_similar_categories(self, category: str, threshold: float = 0.4) -> List[Tuple[str, float]]:
        """查找相似分类，支持中英文搜索"""
        all_categories = self.data_manager.get_all_categories()
        
        # 计算相似度
        from difflib import SequenceMatcher
        similarities = []
        
        for cat_key, cat_data in all_categories.items():
            # 计算与键名的相似度
            key_similarity = SequenceMatcher(None, category.lower(), cat_key.lower()).ratio()
            
            # 计算与本地化名称的相似度（如果存在）
            name_similarity = 0.0
            if 'name' in cat_data:
                name_similarity = SequenceMatcher(None, category.lower(), cat_data['name'].lower()).ratio()
            
            # 计算与描述的相似度
            desc_similarity = 0.0
            if 'description' in cat_data:
                desc_similarity = SequenceMatcher(None, category.lower(), cat_data['description'].lower()).ratio()
            
            # 取最高的相似度
            max_similarity = max(key_similarity, name_similarity, desc_similarity)
            
            # 如果相似度足够高，添加到结果中
            if max_similarity >= threshold:
                similarities.append((cat_key, max_similarity))
        
        # 按相似度降序排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities
    
    def find_similar_commands(self, command: str, threshold: float = 0.6) -> List[Dict[str, Any]]:
        """查找相似命令"""
        similar_results = self.search_engine.find_similar_commands(command, threshold)
        
        results = []
        for cmd_name, similarity in similar_results:
            command_data = self.command_loader.load_command(cmd_name)
            if command_data:
                results.append({
                    'command': cmd_name,
                    'similarity': similarity,
                    'description': command_data.get('description', ''),
                    'category': command_data.get('category', '')
                })
        
        return results
    
    def validate_command(self, command_name: str) -> bool:
        """验证命令是否存在"""
        return self.command_loader.validate_command(command_name)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计信息"""
        return {
            'data_manager': self.data_manager.get_meta_info(),
            'command_loader': self.command_loader.get_cache_stats(),
            'search_engine': self.search_engine.get_index_stats(),
            'total_commands': len(self.get_command_list())
        }
    
    def refresh_data(self):
        """刷新数据"""
        self.data_manager.refresh_cache()
        self.command_loader.clear_cache()
        self.search_engine.rebuild_index()
    
    def export_command_data(self, command_name: str, format_type: str = 'json') -> str:
        """导出命令数据"""
        command_data = self.query_command(command_name)
        if not command_data:
            return ""
        
        if format_type == 'json':
            return json.dumps(command_data, indent=2, ensure_ascii=False)
        elif format_type == 'text':
            return self._format_command_text(command_data)
        else:
            return str(command_data)
    
    def _format_command_text(self, command_data: Dict[str, Any]) -> str:
        """格式化命令数据为文本"""
        text = f"命令: {command_data['name']}\n"
        text += f"描述: {command_data['description']}\n"
        text += f"分类: {command_data['category']}\n"
        text += f"用法: {command_data['usage']}\n"
        
        if 'options' in command_data:
            text += "\n选项:\n"
            for option in command_data['options']:
                text += f"  {option.get('flag', '')}: {option.get('description', '')}\n"
        
        if 'examples' in command_data:
            text += "\n示例:\n"
            for example in command_data['examples']:
                text += f"  {example.get('command', '')}\n"
                text += f"    {example.get('description', '')}\n"
        
        return text

if __name__ == "__main__":
    # 测试查询处理器
    processor = QueryProcessor()
    
    print("测试查询处理器...")
    
    # 测试命令查询
    print("\n1. 查询命令 'ls':")
    ls_data = processor.query_command('ls')
    if ls_data:
        print(f"   命令: {ls_data['name']}")
        print(f"   描述: {ls_data['description']}")
        print(f"   分类: {ls_data['category']}")
    
    # 测试搜索
    print("\n2. 搜索 'file':")
    search_results = processor.search_commands('file')
    for category, commands in search_results.items():
        if commands:
            print(f"   {category}: {commands[:3]}...")  # 只显示前3个
    
    # 测试分类查询
    print("\n3. 查询分类 '文件管理':")
    category_data = processor.get_category_commands('文件管理')
    print(f"   分类: {category_data['category']}")
    print(f"   命令数量: {category_data['total_count']}")
    
    # 测试相似命令
    print("\n4. 查找相似命令 'lis':")
    similar = processor.find_similar_commands('lis')
    for cmd_info in similar[:3]:  # 显示前3个
        print(f"   {cmd_info['command']} (相似度: {cmd_info['similarity']:.2f})")
    
    # 测试系统统计
    print("\n5. 系统统计:")
    stats = processor.get_system_stats()
    print(f"   总命令数: {stats['total_commands']}")
    print(f"   缓存命中率: {stats['command_loader']['cache_hit_rate']:.2f}%")
    
    # 测试导出
    print("\n6. 导出命令数据 (ls):")
    exported = processor.export_command_data('ls', 'text')
    print(exported[:200] + "..." if len(exported) > 200 else exported)