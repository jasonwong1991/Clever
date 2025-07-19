#!/usr/bin/env python3
"""
搜索相关工具函数
"""

import re
from typing import List, Dict, Any
from difflib import SequenceMatcher


def calculate_similarity(str1: str, str2: str) -> float:
    """计算两个字符串的相似度 (0-1)"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def fuzzy_match(query: str, target: str, threshold: float = 0.6) -> bool:
    """模糊匹配，判断query是否与target相似"""
    return calculate_similarity(query, target) >= threshold


def extract_keywords(text: str) -> List[str]:
    """从文本中提取关键词"""
    # 移除标点符号，分割单词
    words = re.findall(r'\b\w+\b', text.lower())
    # 过滤掉长度小于2的单词
    return [word for word in words if len(word) >= 2]


def highlight_match(text: str, query: str, highlight_color: str = '\033[93m') -> str:
    """高亮显示匹配的文本"""
    if not query or not text:
        return text
    
    # 不区分大小写的匹配
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    end_color = '\033[0m'
    
    return pattern.sub(f'{highlight_color}\\g<0>{end_color}', text)


def normalize_text(text: str) -> str:
    """标准化文本（去除多余空格，转小写）"""
    return ' '.join(text.lower().split())


def text_contains_all(text: str, keywords: List[str]) -> bool:
    """检查文本是否包含所有关键词"""
    text_lower = text.lower()
    return all(keyword.lower() in text_lower for keyword in keywords)


def text_contains_any(text: str, keywords: List[str]) -> bool:
    """检查文本是否包含任意关键词"""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)


def rank_by_relevance(results: List[Dict[str, Any]], query: str, key_field: str = 'name') -> List[Dict[str, Any]]:
    """根据相关性对结果进行排序"""
    def relevance_score(item):
        text = item.get(key_field, '')
        
        # 精确匹配得分最高
        if query.lower() == text.lower():
            return 1.0
        
        # 包含查询词得分其次
        if query.lower() in text.lower():
            return 0.8
        
        # 相似度得分
        return calculate_similarity(query, text)
    
    return sorted(results, key=relevance_score, reverse=True)