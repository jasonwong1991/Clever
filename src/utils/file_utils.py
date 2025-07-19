#!/usr/bin/env python3
"""
文件操作工具函数
"""

import os
import json
from typing import Dict, Any, Optional


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """安全地加载JSON文件"""
    try:
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"加载文件 {file_path} 失败: {e}")
        return None


def list_json_files(directory: str) -> list:
    """列出目录中的所有JSON文件"""
    if not os.path.exists(directory):
        return []
    
    json_files = []
    try:
        for file_name in os.listdir(directory):
            if file_name.endswith('.json'):
                json_files.append(os.path.join(directory, file_name))
    except OSError:
        pass
    
    return json_files