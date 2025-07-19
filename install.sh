#!/bin/bash

# Clever Linux Tool (clever) 安装脚本
# 使用方法: 
#   交互式安装: chmod +x install.sh && ./install.sh
#   自动安装:   CLEVER_AUTO_INSTALL=1 ./install.sh

SCRIPT_NAME="clever"
INSTALL_DIR="/usr/local/bin"
SOURCE_DIR="$(pwd)"
MAIN_SCRIPT="$SOURCE_DIR/src/__init__.py"

# 语言检测函数
detect_language() {
    if [[ "$LANG" =~ ^zh ]]; then
        echo "zh"
    elif [[ "$LANG" =~ ^en ]]; then
        echo "en"
    else
        echo "zh"
    fi
}

# 获取语言选择（只在需要时调用）
get_language_choice() {
    local detected_lang=$(detect_language)
    
    if [ "$CLEVER_AUTO_INSTALL" = "1" ]; then
        echo "$detected_lang"
        return
    fi
    
    echo "检测到系统语言: $detected_lang" >&2
    echo "Detected system language: $detected_lang" >&2
    echo >&2
    echo "请选择界面语言 / Please select interface language:" >&2
    echo "1) 中文 (Chinese)" >&2
    echo "2) English" >&2
    echo "3) 使用系统检测语言 (Use detected: $detected_lang)" >&2
    echo >&2
    
    read -t 15 -p "请输入选择 (1-3) / Enter choice (1-3): " choice >&2
    
    case $choice in
        1) echo "zh" ;;
        2) echo "en" ;;
        3) echo "$detected_lang" ;;
        "") echo "$detected_lang" ;;
        *) echo "$detected_lang" ;;
    esac
}

# 主安装函数
install_clever() {
    local selected_lang="$1"
    
    # 设置多语言文本
    if [ "$selected_lang" = "zh" ]; then
        INSTALL_TITLE="=== Clever Linux Tool (clever) 安装脚本 ==="
        ERROR_MAIN_NOT_FOUND="错误: 找不到主程序文件 src/__init__.py"
        ERROR_DIR_NOT_FOUND="错误: 缺少必要的目录结构 (src/ 或 src/knowledge_base/)"
        ERROR_ENSURE_ROOT="请确保在项目根目录中运行此脚本"
        ERROR_PYTHON_NOT_FOUND="错误: 未找到 python3"
        ERROR_INSTALL_PYTHON="请先安装 Python 3"
        MSG_INSTALLING="正在安装 $SCRIPT_NAME 到 $INSTALL_DIR..."
        MSG_SUCCESS="✅ 安装成功！"
        MSG_USAGE="现在您可以在任何地方使用以下命令:"
        MSG_EXAMPLES="示例:"
        MSG_FAILED="❌ 安装失败"
    else
        INSTALL_TITLE="=== Clever Linux Tool (clever) Installation Script ==="
        ERROR_MAIN_NOT_FOUND="Error: Main program file src/__init__.py not found"
        ERROR_DIR_NOT_FOUND="Error: Missing required directory structure (src/ or src/knowledge_base/)"
        ERROR_ENSURE_ROOT="Please ensure running this script in project root directory"
        ERROR_PYTHON_NOT_FOUND="Error: python3 not found"
        ERROR_INSTALL_PYTHON="Please install Python 3 first"
        MSG_INSTALLING="Installing $SCRIPT_NAME to $INSTALL_DIR..."
        MSG_SUCCESS="✅ Installation successful!"
        MSG_USAGE="You can now use the following commands anywhere:"
        MSG_EXAMPLES="Examples:"
        MSG_FAILED="❌ Installation failed"
    fi

    echo "$INSTALL_TITLE"
    echo

    # 检查主程序是否存在
    if [ ! -f "$MAIN_SCRIPT" ]; then
        echo "$ERROR_MAIN_NOT_FOUND"
        echo "$ERROR_ENSURE_ROOT"
        exit 1
    fi

    # 检查必要的目录结构
    if [ ! -d "$SOURCE_DIR/src" ] || [ ! -d "$SOURCE_DIR/src/knowledge_base" ]; then
        echo "$ERROR_DIR_NOT_FOUND"
        echo "$ERROR_ENSURE_ROOT"
        exit 1
    fi

    # 检查Python3是否安装
    if ! command -v python3 &> /dev/null; then
        echo "$ERROR_PYTHON_NOT_FOUND"
        echo "$ERROR_INSTALL_PYTHON"
        exit 1
    fi

    echo "$MSG_INSTALLING"

    # 创建安装目录的项目文件夹
    INSTALL_PROJECT_DIR="$INSTALL_DIR/clever_project"
    mkdir -p "$INSTALL_PROJECT_DIR"

    # 复制整个项目结构
    cp -r "$SOURCE_DIR/src" "$INSTALL_PROJECT_DIR/"

    # 设置初始语言配置
    if [ ! -f "$INSTALL_PROJECT_DIR/src/knowledge_base/i18n_config.json" ]; then
        cat > "$INSTALL_PROJECT_DIR/src/knowledge_base/i18n_config.json" << EOF
{
  "language": "$selected_lang",
  "supported_languages": ["zh", "en"],
  "last_updated": "$(date -Iseconds)"
}
EOF
    fi

    # 创建启动脚本
    cat > "$INSTALL_DIR/$SCRIPT_NAME" << 'EOF'
#!/bin/bash
cd /usr/local/bin/clever_project
python3 src/__init__.py "$@"
EOF

    # 创建缩写命令 clr
    cat > "$INSTALL_DIR/clr" << 'EOF'
#!/bin/bash
cd /usr/local/bin/clever_project
python3 src/__init__.py "$@"
EOF

    # 设置执行权限
    chmod +x "$INSTALL_DIR/$SCRIPT_NAME"
    chmod +x "$INSTALL_DIR/clr"

    # 验证安装
    if [ -f "$INSTALL_DIR/$SCRIPT_NAME" ] && [ -x "$INSTALL_DIR/$SCRIPT_NAME" ] && [ -f "$INSTALL_DIR/clr" ] && [ -x "$INSTALL_DIR/clr" ]; then
        echo "$MSG_SUCCESS"
        echo
        echo "$MSG_USAGE"
        if [ "$selected_lang" = "zh" ]; then
            echo "  clever <命令名>            # 查询具体命令 (简写: clr)"
            echo "  clever -s <关键词>         # 搜索命令 (简写: clr -s)"
            echo "  clever -c <分类>           # 按分类查询 (简写: clr -c)"
            echo "  clever -l                  # 列出所有命令 (简写: clr -l)"
            echo "  clever --help              # 显示帮助 (简写: clr --help)"
            echo
            echo "$MSG_EXAMPLES"
            echo "  clever ls       # 或 clr ls"
            echo "  clever -s 文件  # 或 clr -s 文件"
            echo "  clever -c 文件管理  # 或 clr -c 文件管理"
        else
            echo "  clever <command>           # Query specific command (short: clr)"
            echo "  clever -s <keyword>        # Search commands (short: clr -s)"
            echo "  clever -c <category>       # Query by category (short: clr -c)"
            echo "  clever -l                  # List all commands (short: clr -l)"
            echo "  clever --help              # Show help (short: clr --help)"
            echo
            echo "$MSG_EXAMPLES"
            echo "  clever ls       # or clr ls"
            echo "  clever -s file  # or clr -s file"
            echo "  clever -c file_management  # or clr -c file_management"
        fi
    else
        echo "$MSG_FAILED"
        exit 1
    fi
}

# 主流程
main() {
    # 如果已经是root，直接开始安装
    if [ "$EUID" -eq 0 ]; then
        # 检查是否有语言参数传递
        if [ -n "$CLEVER_INSTALL_LANG" ]; then
            install_clever "$CLEVER_INSTALL_LANG"
        else
            # root用户也需要选择语言
            SELECTED_LANG=$(get_language_choice)
            install_clever "$SELECTED_LANG"
        fi
    else
        # 普通用户，先选择语言，然后sudo
        SELECTED_LANG=$(get_language_choice)
        
        if [ "$SELECTED_LANG" = "zh" ]; then
            echo "需要管理员权限来安装到系统目录"
            echo "正在尝试使用 sudo..."
        else
            echo "Administrator privileges required to install to system directory"
            echo "Trying to use sudo..."
        fi
        
        # 传递语言选择给sudo执行
        exec sudo CLEVER_INSTALL_LANG="$SELECTED_LANG" "$(realpath "$0")" "$@"
    fi
}

# 运行主程序
main "$@"