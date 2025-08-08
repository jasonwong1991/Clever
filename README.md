# Popular Command Query Tool (clever)

**English** | [中文](README_CN.md)

A modern popular command query tool with bilingual support (Chinese/English) and a data-code separation architecture design.

Note on alias: The installer creates a short alias clr, which is a shorthand for clever. After installation, you can use either clever or clr interchangeably.

## Features

- 🔍 Query detailed information for specific commands
- 🔎 Search commands by keywords
- 📂 Browse commands by categories
- 🎯 **Smart fuzzy category search (supports Chinese/English)**
- 📝 List all available commands
- 🌏 Bilingual support (Chinese/English)
- 🌍 Intelligent language detection and switching
- ⚡ Lazy loading and smart caching
- 📊 Performance statistics monitoring
- 🔧 Modular architecture design
- 🏷️ Intelligent tag-based search

## Architecture

### Directory Structure
```
project-root/
├── src/                        # Source code directory
│   ├── __init__.py            # Main program entry
│   ├── cli/                   # CLI module
│   │   ├── parser.py          # Command line argument parsing
│   │   ├── formatter.py       # Output formatting
│   │   └── interface.py       # CLI main interface
│   ├── core/                  # Core module
│   │   ├── command_loader.py  # Command loader
│   │   ├── query_processor.py # Query processor
│   │   └── search_engine.py   # Search engine
│   ├── data/                  # Data management module
│   │   └── data_manager.py    # Data manager and cache manager
│   ├── utils/                 # Utilities module
│   │   ├── file_utils.py      # File operation utilities
│   │   ├── search_utils.py    # Search utility functions
│   │   ├── display_utils.py   # Display utility functions
│   │   └── i18n.py           # Internationalization manager
│   └── knowledge_base/        # Knowledge base directory
│       ├── commands_zh/       # Chinese command library
│       │   ├── basic/        # Basic commands
│       │   ├── advanced_tools/ # Advanced tools
│       │   ├── tools/        # System tools
│       │   ├── network/      # Network tools
│       │   ├── system/       # System information
│       │   ├── text/         # Text processing
│       │   ├── compression/  # Compression tools
│       │   ├── dev/          # Development tools
│       │   ├── version/      # Version control
│       │   └── container/    # Containerization
│       ├── commands_en/       # English command library (same structure)
│       ├── categories_zh.json # Chinese category configuration
│       ├── categories_en.json # English category configuration
│       ├── search_mappings_zh.json # Chinese search mappings
│       ├── search_mappings_en.json # English search mappings
│       ├── meta_zh.json      # Chinese metadata configuration
│       ├── meta_en.json      # English metadata configuration
│       └── i18n_config.json  # Internationalization configuration
├── install.sh               # Smart installation script
├── uninstall.sh            # Uninstallation script
├── README.md               # English documentation
├── README_CN.md            # Chinese documentation
└── CLAUDE.md              # Project documentation
```

### Core Components
- **CommandLoader**: Command lazy loading and cache management
- **SearchEngine**: Multi-strategy search engine
- **QueryProcessor**: Query processing and result formatting
- **DataManager**: Data file reading and validation
- **CacheManager**: LRU cache management
- **I18nManager**: Internationalization manager

## Installation

### Using Installation Script (Recommended)

```bash
# Ensure you're in the project root directory
chmod +x install.sh
./install.sh
```

The installation script automatically detects system language and configures the appropriate default language.

### Manual Execution

```bash
# Run directly from project root directory
python3 src/__init__.py [options] [command]
```

## Usage

After installation, you can use the `clever` command anywhere (short alias: `clr`):

```bash
# Query specific commands
clever ls                    # Query ls command details
clever grep                  # Query grep command details
clever docker                # Query docker command details

# Search commands
clever -s file               # Search commands containing "file"
clever -s process            # Search commands containing "process"
clever -s container          # Search container-related commands

# Query by category (with fuzzy search support)
clever -c file_management    # Show file management commands
clever -c "File Management"  # English category name
clever -c process_management # Show process management commands
clever -c containerization  # Show containerization commands

# Fuzzy category search examples
clever -c "file"            # Auto-matches file_management or file_viewing
clever -c "manage"          # Auto-matches file_management or process_management
clever -c "网络"            # Chinese fuzzy search for network tools
clever -c "开发"            # Chinese fuzzy search for development tools

# List all commands
clever -l                    # List all available commands
clever --categories          # Show all categories

# Language switching
clever --lang en             # Switch to English mode
clever --lang zh             # Switch to Chinese mode

# System statistics
clever --stats              # View cache statistics and performance info

# Get help
clever --help               # Show help information
```

### More quick examples

```bash
# Use short alias instead of full command
clr ls
clr -s network
clr -c process_management

# Compare outputs
clever -s docker
clr -s docker

# Category fuzzy search (both work)
clever -c "file"
clr -c "文件"
```

## Currently Supported Commands (65 total)

### Category Statistics
- **File Management**: ls, cd, pwd, mkdir, rmdir, rm, cp, mv, find, touch, ln
- **File Viewing**: cat, less, more, head, tail
- **Permission Management**: chmod, chown
- **Process Management**: ps, top, htop, kill, pkill, killall, pgrep, jobs
- **Network Tools**: ping, wget, curl, ssh, scp, rsync, netstat
- **System Information**: df, du, free, uname, which, whereis, lsof
- **Text Processing**: grep, sed, awk, sort, uniq, wc, tr, cut
- **Compression Tools**: tar, gzip, gunzip, zip, unzip
- **Development Tools**: npm, pip, yarn, node, python, gcc, make
- **Version Control**: git
- **Containerization**: docker, docker-compose, kubectl, podman
- **Advanced Tools**: tmux, screen, xargs

## Mainstream tools and how to install them

Below are quick installation snippets for common tools referenced by this project’s knowledge base. Use the one that matches your OS/package manager.

- Homebrew (macOS/Linux):
  - Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  - Update: brew update
  - Examples: brew install wget curl git tmux htop jq ripgrep fzf
- Debian/Ubuntu (apt):
  - sudo apt update && sudo apt install -y wget curl git tmux htop jq ripgrep fzf python3 python3-pip docker.io docker-compose kubectl
- Fedora/RHEL/CentOS (dnf/yum):
  - sudo dnf install -y wget curl git tmux htop jq ripgrep fzf python3 python3-pip docker docker-compose kubectl || sudo yum install -y wget curl git tmux htop jq ripgrep fzf
- Arch/Manjaro (pacman):
  - sudo pacman -Syu --noconfirm wget curl git tmux htop jq ripgrep fzf python python-pip docker kubectl
- openSUSE (zypper):
  - sudo zypper install -y wget curl git tmux htop jq ripgrep fzf python3 python3-pip docker kubectl
- Windows (Chocolatey):
  - choco install -y git wget curl jq ripgrep fzf python docker-desktop kubernetes-cli
- Windows (Winget):
  - winget install --id Git.Git -e && winget install --id GnuWin32.Wget -e && winget install --id curl.curl -e && winget install --id jqlang.jq -e && winget install --id BurntSushi.ripgrep.MSVC -e && winget install --id fzf.fzf -e && winget install --id Python.Python.3 -e && winget install --id Docker.DockerDesktop -e && winget install --id Kubernetes.kubectl -e

Notes:
- Some tools (e.g., Docker, Docker Desktop) may require additional post-install steps and/or a system restart.
- For Docker on Linux: ensure your user is added to the docker group and the service is enabled.

## Internationalization Features 🌍

- **Bilingual Support**: Complete Chinese/English interface and knowledge base
- **Auto Detection**: Automatic system language detection during installation
- **Smart Configuration**: Automatic language preference setup on first run
- **Dynamic Switching**: Runtime language switching support
- **Complete Localization**: Full translation of command descriptions, categories, and interface text
- **🎯 Smart Category Search**: Fuzzy search supports both English keys and localized Chinese category names
- **Cross-Language Matching**: Search "文件管理" to find "file_management" category automatically

## Uninstallation

```bash
./uninstall.sh
```

Or manually remove:

```bash
sudo rm /usr/local/bin/clever
sudo rm -rf /usr/local/bin/clever_project
```

## System Requirements

- Python 3.x
- Linux/Unix system
- Administrator privileges (only required during installation)

## Performance Features

- **Lazy Loading**: Load command data on demand to reduce memory usage
- **LRU Cache**: Smart caching of recently used commands for faster queries
- **Search Index**: Pre-built search index for fast retrieval
- **Statistics Monitoring**: Real-time monitoring of cache hit rates and performance metrics
- **Multi-Strategy Search**: Support for exact matching, keyword matching, tag matching, etc.

## Sample Output

```bash
$ clever ls
Command: ls
Description: List directory contents
Category: file_management
Usage: ls [options] [directories...]

Options:
  -l: Use long listing format to show detailed information
  -a: Show all files, including hidden files
  -h: Show file sizes in human-readable format
  -R: Recursively list subdirectory contents
  -t: Sort by modification time
  -S: Sort by file size

Examples:
  ls -la
    Show detailed information and hidden files
  ls -lh /home/user
    Show human-readable file sizes
  ls -R /var/log
    Recursively show directory contents

Related Commands:
  cd, pwd, find, tree
```

## Development Information

- **Architecture**: Modular design with code-data separation
- **Version**: v4.0 (Massive command library expansion version)
- **Data Format**: JSON configuration files
- **Caching Strategy**: LRU + lazy loading
- **Internationalization**: Complete Chinese/English bilingual support
- **Extensibility**: Plugin-based extension support
- **Total Commands**: 65 Linux commands
- **Index Terms**: 966 search keywords
- **Tags**: 191 command tags

## Contributing

Issues and Pull Requests are welcome to help improve this project!

## Packaging guides

See PACKAGING.md for Homebrew formula template and Debian/apt packaging notes.

## License

This project is released under an open source license. Please see the LICENSE file for details.
