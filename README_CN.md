# 热门命令查询工具（clever）

[English](README.md) | **中文**

说明：安装脚本会创建一个简写别名 clr（即 clever 的缩写）。安装后，你可以使用 clever 或 clr 互换使用。

一个现代化的热门命令查询工具，支持中英文双语界面，采用数据与代码分离的架构设计。

## 功能特性

- 🔍 查询具体命令的详细信息
- 🔎 按关键词搜索相关命令  
- 📂 按分类浏览命令
- 🎯 **智能分类模糊搜索（支持中英文）**
- 📝 列出所有可用命令
- 🌏 中英文双语支持
- 🌍 智能语言检测和切换
- ⚡ 懒加载和智能缓存
- 📊 性能统计监控
- 🔧 模块化架构设计
- 🏷️ 智能标签搜索

## 项目架构

### 目录结构
```
project-root/
├── src/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── formatter.py
│   │   ├── interface.py
│   │   └── parser.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── command_loader.py
│   │   ├── query_processor.py
│   │   └── search_engine.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_manager.py
│   └── knowledge_base/
│       ├── categories_en.json
│       ├── categories_zh.json
│       ├── commands_en/
│       │   ├── advanced_tools.json
│       │   ├── basic.json
│       │   ├── compression.json
│       │   ├── container.json
│       │   ├── network.json
│       │   ├── system.json
│       │   ├── text.json
│       │   └── tools.json
│       ├── commands_zh/
│       │   ├── advanced_tools.json
│       │   ├── basic.json
│       │   ├── compression.json
│       │   ├── container.json
│       │   ├── dev.json
│       │   ├── network.json
│       │   ├── system.json
│       │   ├── text.json
│       │   ├── tools.json
│       │   └── version.json
│       ├── i18n_config.json
│       ├── meta_en.json
│       ├── meta_zh.json
│       ├── search_mappings_en.json
│       └── search_mappings_zh.json
├── install.sh
├── uninstall.sh
├── .github/
│   └── workflows/
│       └── ci.yml
├── README.md
├── README_CN.md
├── CHANGELOG.md
├── RELEASE_NOTES.md
├── PACKAGING.md
└── SHA256SUMS-v1.0.1.txt
```

### 核心组件
- **CommandLoader**: 命令懒加载和缓存管理
- **SearchEngine**: 多策略搜索引擎 
- **QueryProcessor**: 查询处理和结果格式化
- **DataManager**: 数据文件读取和验证
- **CacheManager**: LRU缓存管理
- **I18nManager**: 国际化管理器

## 安装

### 使用安装脚本 (推荐)

```bash
# 确保在项目根目录中
chmod +x install.sh
./install.sh
```

安装脚本会自动检测系统语言并配置相应的默认语言。

### 手动运行

```bash
# 在项目根目录中直接运行
python3 src/__init__.py [选项] [命令]
```

## 使用方法

提示：支持简写别名 clr，例如 clever ls 与 clr ls 等价。

安装完成后，你可以在任何地方使用 `clever` 命令：

```bash
# 查询具体命令
clever ls                    # 查询 ls 命令详情
clever grep                  # 查询 grep 命令详情
clever docker                # 查询 docker 命令详情

# 搜索命令
clever -s 文件               # 搜索包含"文件"的命令
clever -s process            # 搜索包含"process"的命令
clever -s 容器               # 搜索容器相关命令

# 按分类查询（支持模糊搜索）
clever -c 文件管理           # 显示文件管理类命令
clever -c 进程管理           # 显示进程管理类命令
clever -c 容器化             # 显示容器化相关命令

# 模糊分类搜索示例
clever -c "文件"            # 自动匹配文件管理或文件查看
clever -c "管理"            # 自动匹配文件管理或进程管理
clever -c "file"            # 英文模糊搜索网络工具
clever -c "develop"         # 英文模糊搜索开发工具

# 列出所有命令
clever -l                    # 列出所有可用命令
clever --categories          # 显示所有分类

# 语言切换
clever --lang en             # 切换到英文模式
clever --lang zh             # 切换到中文模式

# 系统统计
clever --stats              # 查看缓存统计和性能信息

# 获取帮助
clever --help               # 显示帮助信息
```

### 更多快速示例

```bash
# 使用简写别名替代完整命令
clr ls
clr -s 网络
clr -c 进程管理

# 对比输出（等价）
clever -s docker
clr -s docker

# 分类模糊搜索（中英文都可）
clever -c "file"
clr -c "文件"
```

## 当前支持的命令 (65个)

### 分类统计
- **文件管理**: ls, cd, pwd, mkdir, rmdir, rm, cp, mv, find, touch, ln
- **文件查看**: cat, less, more, head, tail
- **权限管理**: chmod, chown
- **进程管理**: ps, top, htop, kill, pkill, killall, pgrep, jobs
- **网络工具**: ping, wget, curl, ssh, scp, rsync, netstat
- **系统信息**: df, du, free, uname, which, whereis, lsof
- **文本处理**: grep, sed, awk, sort, uniq, wc, tr, cut
- **压缩工具**: tar, gzip, gunzip, zip, unzip
- **开发工具**: npm, pip, yarn, node, python, gcc, make
- **版本控制**: git
- **容器化**: docker, docker-compose, kubectl, podman
- **高级工具**: tmux, screen, xargs

## 主流工具与安装方式

以下是本项目知识库中涉及的常用工具及其快速安装示例，请根据你的系统选择对应的包管理器：

- Homebrew（macOS/Linux）：
  - 安装 Homebrew：/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  - 更新：brew update
  - 示例：brew install wget curl git tmux htop jq ripgrep fzf
- Debian/Ubuntu（apt）：
  - sudo apt update && sudo apt install -y wget curl git tmux htop jq ripgrep fzf python3 python3-pip docker.io docker-compose kubectl
- Fedora/RHEL/CentOS（dnf/yum）：
  - sudo dnf install -y wget curl git tmux htop jq ripgrep fzf python3 python3-pip docker docker-compose kubectl || sudo yum install -y wget curl git tmux htop jq ripgrep fzf
- Arch/Manjaro（pacman）：
  - sudo pacman -Syu --noconfirm wget curl git tmux htop jq ripgrep fzf python python-pip docker kubectl
- openSUSE（zypper）：
  - sudo zypper install -y wget curl git tmux htop jq ripgrep fzf python3 python3-pip docker kubectl
- Windows（Chocolatey）：
  - choco install -y git wget curl jq ripgrep fzf python docker-desktop kubernetes-cli
- Windows（Winget）：
  - winget install --id Git.Git -e && winget install --id GnuWin32.Wget -e && winget install --id curl.curl -e && winget install --id jqlang.jq -e && winget install --id BurntSushi.ripgrep.MSVC -e && winget install --id fzf.fzf -e && winget install --id Python.Python.3 -e && winget install --id Docker.DockerDesktop -e && winget install --id Kubernetes.kubectl -e

注意：
- 部分工具（如 Docker、Docker Desktop）可能需要额外的安装后步骤和/或重启系统。
- Linux 上使用 Docker 时，请确保将用户加入 docker 组并启用 docker 服务。

## 国际化特性 🌍

- **双语支持**: 完整的中文/英文界面和知识库
- **自动检测**: 安装时自动检测系统语言
- **智能配置**: 首次运行自动设置语言偏好
- **动态切换**: 支持运行时语言切换
- **完整本地化**: 包括命令描述、分类、界面文本的完整翻译
- **🎯 智能分类搜索**: 模糊搜索同时支持英文键名和本地化中文分类名
- **跨语言匹配**: 搜索"文件管理"自动找到"file_management"分类

## 卸载

```bash
./uninstall.sh
```

或手动删除：

```bash
sudo rm /usr/local/bin/clever
sudo rm -rf /usr/local/bin/clever_project
```

## 系统要求

- Python 3.x
- Linux/Unix 系统
- 管理员权限 (仅安装时需要)

## 性能特性

- **懒加载**: 按需加载命令数据，减少内存占用
- **LRU缓存**: 智能缓存最近使用的命令，提高查询速度
- **搜索索引**: 预建搜索索引，支持快速检索
- **统计监控**: 实时监控缓存命中率和性能指标
- **多策略搜索**: 支持精确匹配、关键词匹配、标签匹配等

## 示例输出

```bash
$ clever ls
命令: ls
描述: 显示目录内容
分类: file_management
用法: ls [选项] [目录...]

选项:
  -l: 使用长列表格式显示详细信息
  -a: 显示所有文件，包括隐藏文件
  -h: 以人类可读的格式显示文件大小
  -R: 递归显示子目录内容
  -t: 按修改时间排序
  -S: 按文件大小排序

示例:
  ls -la
    显示详细信息和隐藏文件
  ls -lh /home/user
    显示人类可读的文件大小
  ls -R /var/log
    递归显示目录内容

相关命令:
  cd, pwd, find, tree
```

## 开发信息

- **架构**: 模块化设计，代码与数据分离
- **版本**: v4.0 (大规模命令库扩展版本)
- **数据格式**: JSON配置文件
- **缓存策略**: LRU + 懒加载
- **国际化**: 完整的中英文双语支持
- **扩展性**: 支持插件化扩展
- **命令总数**: 65个Linux命令
- **索引词数**: 966个搜索关键词
- **标签数**: 191个命令标签

## 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目！

## 打包指南

请参阅 PACKAGING.md，包含 Homebrew 配方模板以及 Debian/apt 打包说明。

## 许可证

本项目采用开源许可证，具体信息请查看LICENSE文件。
