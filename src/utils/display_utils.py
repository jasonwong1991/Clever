#!/usr/bin/env python3
"""
显示相关工具函数
"""

import shutil
from typing import Dict, Any, List


def get_terminal_width() -> int:
    """获取终端宽度"""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80


def format_table(headers: List[str], rows: List[List[str]], min_width: int = 10) -> str:
    """格式化表格输出"""
    if not headers or not rows:
        return ""
    
    # 计算每列的最大宽度
    col_widths = []
    for i, header in enumerate(headers):
        max_width = len(header)
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])))
        col_widths.append(max(max_width, min_width))
    
    # 构建分隔线
    separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"
    
    # 构建表格
    lines = [separator]
    
    # 添加表头
    header_line = "|"
    for i, header in enumerate(headers):
        header_line += f" {header:<{col_widths[i]}} |"
    lines.append(header_line)
    lines.append(separator)
    
    # 添加数据行
    for row in rows:
        row_line = "|"
        for i in range(len(headers)):
            cell = str(row[i]) if i < len(row) else ""
            row_line += f" {cell:<{col_widths[i]}} |"
        lines.append(row_line)
    
    lines.append(separator)
    return "\n".join(lines)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """截断文本到指定长度"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_list(items: List[str], columns: int = 3, min_width: int = 20) -> str:
    """格式化列表为多列显示"""
    if not items:
        return ""
    
    terminal_width = get_terminal_width()
    col_width = max(min_width, (terminal_width - (columns - 1) * 2) // columns)
    
    lines = []
    for i in range(0, len(items), columns):
        row_items = items[i:i + columns]
        line = ""
        for j, item in enumerate(row_items):
            truncated_item = truncate_text(item, col_width)
            if j < len(row_items) - 1:
                line += f"{truncated_item:<{col_width}}  "
            else:
                line += truncated_item
        lines.append(line)
    
    return "\n".join(lines)


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def format_duration(seconds: float) -> str:
    """格式化时间间隔"""
    if seconds < 1:
        return f"{seconds * 1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m{secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h{minutes}m"