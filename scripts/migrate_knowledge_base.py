#!/usr/bin/env python3
"""
知识库数据迁移工具
将分散的命令JSON文件合并为按分类组织的文件
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class KnowledgeBaseMigrator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.kb_path = self.project_root / "src" / "knowledge_base"
        self.backup_path = self.project_root / "backup_original_files"
        
    def create_backup(self):
        """创建原始文件备份"""
        print("创建原始文件备份...")
        if self.backup_path.exists():
            shutil.rmtree(self.backup_path)
        
        # 备份中英文命令目录
        shutil.copytree(self.kb_path / "commands_zh", self.backup_path / "commands_zh")
        shutil.copytree(self.kb_path / "commands_en", self.backup_path / "commands_en")
        print(f"备份已创建: {self.backup_path}")
    
    def merge_category_files(self, lang="zh"):
        """合并指定语言的分类文件"""
        commands_dir = self.kb_path / f"commands_{lang}"
        merged_files = {}
        
        print(f"合并{lang}语言文件...")
        
        # 遍历所有分类目录
        for category_dir in commands_dir.iterdir():
            if not category_dir.is_dir():
                continue
                
            category_name = category_dir.name
            commands = {}
            
            # 读取该分类下的所有命令文件
            json_files = list(category_dir.glob("*.json"))
            print(f"  处理分类 {category_name}: {len(json_files)} 个文件")
            
            for json_file in json_files:
                with open(json_file, 'r', encoding='utf-8') as f:
                    command_data = json.load(f)
                    command_name = command_data.get('name', json_file.stem)
                    commands[command_name] = command_data
            
            # 创建合并后的文件结构
            merged_data = {
                "category": category_name,
                "category_name": self.get_category_display_name(category_name, lang),
                "description": f"{category_name} commands",
                "commands": commands,
                "metadata": {
                    "total_commands": len(commands),
                    "last_updated": datetime.now().isoformat(),
                    "version": "2.0",
                    "migrated_from": "individual_files"
                }
            }
            
            merged_files[category_name] = merged_data
        
        return merged_files
    
    def get_category_display_name(self, category_name, lang):
        """获取分类的显示名称"""
        # 从categories文件中读取分类显示名称
        categories_file = self.kb_path / f"categories_{lang}.json"
        if categories_file.exists():
            with open(categories_file, 'r', encoding='utf-8') as f:
                categories = json.load(f)
                for cat_key, cat_info in categories.items():
                    if cat_key == category_name or cat_info.get('commands', []):
                        return cat_info.get('name', category_name)
        return category_name
    
    def write_merged_files(self, merged_files, lang):
        """写入合并后的文件"""
        commands_dir = self.kb_path / f"commands_{lang}"
        
        # 清空原有子目录，保留顶级目录
        for item in commands_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
        
        # 写入合并后的文件
        for category_name, data in merged_files.items():
            output_file = commands_dir / f"{category_name}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  创建合并文件: {output_file}")
    
    def validate_migration(self):
        """验证迁移结果"""
        print("验证迁移结果...")
        
        # 统计原始文件数量
        zh_original = len(list((self.backup_path / "commands_zh").rglob("*.json")))
        en_original = len(list((self.backup_path / "commands_en").rglob("*.json")))
        
        # 统计新文件数量
        zh_new = len(list((self.kb_path / "commands_zh").glob("*.json")))
        en_new = len(list((self.kb_path / "commands_en").glob("*.json")))
        
        print(f"迁移前: 中文{zh_original}个文件, 英文{en_original}个文件, 总计{zh_original + en_original}个")
        print(f"迁移后: 中文{zh_new}个文件, 英文{en_new}个文件, 总计{zh_new + en_new}个")
        print(f"文件减少: {((zh_original + en_original) - (zh_new + en_new)) / (zh_original + en_original) * 100:.1f}%")
        
        # 验证命令数量
        self.validate_command_count()
    
    def validate_command_count(self):
        """验证命令数量是否一致"""
        def count_commands_in_merged(lang):
            commands_dir = self.kb_path / f"commands_{lang}"
            total = 0
            for json_file in commands_dir.glob("*.json"):
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total += len(data.get('commands', {}))
            return total
        
        zh_commands = count_commands_in_merged('zh')
        en_commands = count_commands_in_merged('en')
        
        print(f"合并后命令数量: 中文{zh_commands}个, 英文{en_commands}个")
    
    def migrate(self):
        """执行完整迁移"""
        print("开始知识库迁移...")
        
        # 1. 创建备份
        self.create_backup()
        
        # 2. 合并中文文件
        zh_merged = self.merge_category_files('zh')
        self.write_merged_files(zh_merged, 'zh')
        
        # 3. 合并英文文件  
        en_merged = self.merge_category_files('en')
        self.write_merged_files(en_merged, 'en')
        
        # 4. 验证结果
        self.validate_migration()
        
        print("迁移完成!")
        print(f"备份文件位置: {self.backup_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.getcwd()
    
    migrator = KnowledgeBaseMigrator(project_root)
    migrator.migrate()