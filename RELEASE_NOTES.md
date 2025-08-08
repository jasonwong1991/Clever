# Clever v1.0.0 – Initial public release

This is the first public release of Clever, a modern bilingual (中文/English) command query tool with a code–data separation architecture.

Highlights
- Query detailed information for common commands
- Search by keywords and tags; browse by categories
- Smart fuzzy category search (supports Chinese/English)
- Lazy loading + LRU cache + performance statistics
- Pre-built search index for fast retrieval
- Full i18n with intelligent language detection and switching

What’s included
- 65 popular commands covered across categories (file, text, process, network, system, compression, dev tools, containers, VCS)
- Modular structure: CLI, core engine, data manager, utilities, bilingual knowledge base

Getting started
- Install via script:
  - chmod +x install.sh && ./install.sh
- Or run directly:
  - python3 src/__init__.py --help

Commit summary
- 6d60dd7 feat: 完成第一版~
- 27e6343 feat: 完成第一阶段的开发，涉及大多数主流命令

Notes
- If upgrading from a pre-release/local copy, please re-install using the script to ensure proper language detection and symlink setup.
