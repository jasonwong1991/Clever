#!/usr/bin/env python3
"""
Linux Command Query Tool (clever) - 重构版本
主程序入口
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.cli import create_parser, CleverCLI


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    cli = CleverCLI()
    
    try:
        if args.lang:
            cli.handle_language_change(args.lang)
        elif args.refresh:
            cli.handle_refresh()
        elif args.stats:
            cli.handle_stats()
        elif args.list:
            cli.handle_list_all()
        elif args.categories:
            cli.handle_list_categories()
        elif args.search:
            cli.handle_search(args.search)
        elif args.category:
            cli.handle_category(args.category)
        elif args.command:
            cli.handle_command_query(args.command)
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        cli_lang = cli.i18n.get_language()
        interrupt_text = "用户中断" if cli_lang == 'zh' else "User interrupted"
        print(f"\n{cli.formatter.colorize(interrupt_text, 'yellow')}")
        sys.exit(1)
    except Exception as e:
        cli.formatter.display_error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()