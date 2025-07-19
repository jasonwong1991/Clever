#!/usr/bin/env python3
"""
搜索引擎模块 - 实现智能搜索和索引
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
import difflib
from ..data.data_manager import DataManager
from ..core.command_loader import CommandLoader
from ..utils.search_utils import calculate_similarity, extract_keywords, text_contains_any

class SearchEngine:
    """搜索引擎 - 实现多种搜索策略"""
    
    def __init__(self, data_manager: DataManager = None, command_loader: CommandLoader = None):
        self.data_manager = data_manager or DataManager()
        self.command_loader = command_loader or CommandLoader(self.data_manager)
        self.search_index = {}
        self.keyword_index = {}
        self.tag_index = {}
        self._build_indexes()
    
    def _build_indexes(self):
        """构建搜索索引"""
        # print("正在构建搜索索引...")
        
        # 获取所有命令
        all_commands = self.data_manager.get_command_list()
        
        # 构建关键词索引
        for command_name in all_commands:
            command_data = self.data_manager.load_command(command_name)
            if not command_data:
                continue
            
            # 索引命令名
            self._add_to_index(command_name, command_name, 'name')
            
            # 索引描述
            self._add_to_index(command_data.get('description', ''), command_name, 'description')
            
            # 索引分类
            self._add_to_index(command_data.get('category', ''), command_name, 'category')
            
            # 索引选项
            for option in command_data.get('options', []):
                self._add_to_index(option.get('description', ''), command_name, 'option')
            
            # 索引示例
            for example in command_data.get('examples', []):
                self._add_to_index(example.get('description', ''), command_name, 'example')
            
            # 索引标签
            for tag in command_data.get('tags', []):
                self._add_to_tag_index(tag, command_name)
        
        # 构建文本搜索映射索引
        search_mappings = self.data_manager.get_search_mappings()
        for keyword, commands in search_mappings.items():
            for command in commands:
                if command in all_commands:
                    self._add_to_index(keyword, command, 'mapping')
        
        # print(f"搜索索引构建完成，索引了 {len(all_commands)} 个命令")
    
    def _add_to_index(self, text: str, command_name: str, source: str):
        """添加文本到搜索索引"""
        if not text:
            return
        
        # 分词并添加到索引
        words = self._tokenize(text)
        for word in words:
            if word not in self.search_index:
                self.search_index[word] = defaultdict(list)
            
            if command_name not in self.search_index[word][source]:
                self.search_index[word][source].append(command_name)
    
    def _add_to_tag_index(self, tag: str, command_name: str):
        """添加标签到标签索引"""
        if tag not in self.tag_index:
            self.tag_index[tag] = []
        
        if command_name not in self.tag_index[tag]:
            self.tag_index[tag].append(command_name)
    
    def _tokenize(self, text: str) -> List[str]:
        """文本分词"""
        # 简单的分词实现
        words = re.findall(r'\w+', text.lower())
        return [word for word in words if len(word) > 1]
    
    def search_by_name(self, query: str) -> List[str]:
        """按命令名搜索"""
        results = []
        query_lower = query.lower()
        
        all_commands = self.data_manager.get_command_list()
        
        # 精确匹配
        if query_lower in all_commands:
            results.append(query_lower)
        
        # 前缀匹配
        for command in all_commands:
            if command.startswith(query_lower) and command not in results:
                results.append(command)
        
        # 包含匹配
        for command in all_commands:
            if query_lower in command and command not in results:
                results.append(command)
        
        return results
    
    def search_by_keyword(self, query: str) -> Dict[str, List[str]]:
        """按关键词搜索"""
        results = {
            'exact': [],
            'partial': [],
            'related': []
        }
        
        query_lower = query.lower()
        words = self._tokenize(query)
        
        # 搜索索引
        for word in words:
            if word in self.search_index:
                for source, commands in self.search_index[word].items():
                    if source == 'name':
                        results['exact'].extend(commands)
                    elif source in ['description', 'category']:
                        results['partial'].extend(commands)
                    else:
                        results['related'].extend(commands)
        
        # 去重并保持顺序
        for key in results:
            results[key] = list(dict.fromkeys(results[key]))
        
        return results
    
    def search_by_tags(self, tags: List[str]) -> List[str]:
        """按标签搜索"""
        if not tags:
            return []
        
        results = set()
        
        for tag in tags:
            if tag in self.tag_index:
                if not results:
                    results.update(self.tag_index[tag])
                else:
                    # 取交集
                    results = results.intersection(set(self.tag_index[tag]))
        
        return list(results)
    
    def find_similar_commands(self, command: str, threshold: float = 0.6) -> List[Tuple[str, float]]:
        """查找相似命令"""
        all_commands = self.data_manager.get_command_list()
        similarities = []
        
        for cmd in all_commands:
            similarity = difflib.SequenceMatcher(None, command.lower(), cmd.lower()).ratio()
            if similarity >= threshold:
                similarities.append((cmd, similarity))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:10]  # 返回前10个最相似的命令
    
    def enhanced_search(self, query: str) -> Dict[str, List[str]]:
        """增强搜索 - 综合多种搜索策略"""
        results = {
            'exact_matches': [],
            'name_matches': [],
            'keyword_matches': [],
            'tag_matches': [],
            'similar_commands': []
        }
        
        # 1. 精确命令名匹配
        name_results = self.search_by_name(query)
        if name_results:
            results['exact_matches'] = [name_results[0]]  # 只取第一个精确匹配
            results['name_matches'] = name_results[1:]  # 其他名称匹配
        
        # 2. 关键词搜索
        keyword_results = self.search_by_keyword(query)
        results['keyword_matches'] = keyword_results['exact'] + keyword_results['partial']
        
        # 3. 标签搜索
        query_tags = self._tokenize(query)
        tag_results = self.search_by_tags(query_tags)
        results['tag_matches'] = tag_results
        
        # 4. 相似命令搜索
        similar_results = self.find_similar_commands(query)
        results['similar_commands'] = [cmd for cmd, _ in similar_results]
        
        # 去重处理
        all_found = set()
        for category in ['exact_matches', 'name_matches', 'keyword_matches', 'tag_matches']:
            filtered = []
            for cmd in results[category]:
                if cmd not in all_found:
                    filtered.append(cmd)
                    all_found.add(cmd)
            results[category] = filtered
        
        # 相似命令去重
        results['similar_commands'] = [
            cmd for cmd in results['similar_commands'] 
            if cmd not in all_found
        ]
        
        return results
    
    def get_search_suggestions(self, partial_query: str) -> List[str]:
        """获取搜索建议"""
        suggestions = []
        
        # 命令名建议
        all_commands = self.data_manager.get_command_list()
        for command in all_commands:
            if command.startswith(partial_query.lower()):
                suggestions.append(command)
        
        # 标签建议
        for tag in self.tag_index.keys():
            if tag.startswith(partial_query.lower()):
                suggestions.append(f"#{tag}")
        
        return suggestions[:10]  # 返回前10个建议
    
    def rebuild_index(self):
        """重建搜索索引"""
        self.search_index.clear()
        self.keyword_index.clear()
        self.tag_index.clear()
        self._build_indexes()
    
    def get_index_stats(self) -> Dict[str, Any]:
        """获取索引统计信息"""
        return {
            'total_words': len(self.search_index),
            'total_tags': len(self.tag_index),
            'total_commands': len(self.data_manager.get_command_list()),
            'index_size_bytes': len(str(self.search_index).encode('utf-8'))
        }

if __name__ == "__main__":
    # 测试搜索引擎
    search_engine = SearchEngine()
    
    print("测试搜索引擎...")
    
    # 测试搜索
    print("\n1. 搜索 'file':")
    results = search_engine.enhanced_search('file')
    for category, commands in results.items():
        if commands:
            print(f"   {category}: {commands}")
    
    print("\n2. 搜索 'ls':")
    results = search_engine.enhanced_search('ls')
    for category, commands in results.items():
        if commands:
            print(f"   {category}: {commands}")
    
    print("\n3. 搜索建议 'fi':")
    suggestions = search_engine.get_search_suggestions('fi')
    print(f"   建议: {suggestions}")
    
    print("\n4. 索引统计:")
    stats = search_engine.get_index_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")