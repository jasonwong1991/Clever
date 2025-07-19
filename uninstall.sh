#!/bin/bash

# Clever Linux Tool (clever) 卸载脚本
# 使用方法: chmod +x uninstall.sh && ./uninstall.sh

SCRIPT_NAME="clever"
INSTALL_DIR="/usr/local/bin"
SCRIPT_PATH="$INSTALL_DIR/$SCRIPT_NAME"
INSTALL_PROJECT_DIR="$INSTALL_DIR/clever_project"

echo "=== Clever Linux Tool (clever) 卸载脚本 ==="
echo

# 检查是否有sudo权限
if [ "$EUID" -ne 0 ]; then
    echo "需要管理员权限来从系统目录卸载"
    echo "正在尝试使用 sudo..."
    
    # 重新以sudo运行
    sudo "$0" "$@"
    exit $?
fi

# 检查脚本是否存在
if [ ! -f "$SCRIPT_PATH" ] && [ ! -d "$INSTALL_PROJECT_DIR" ] && [ ! -f "$INSTALL_DIR/clr" ]; then
    echo "⚠️  $SCRIPT_NAME 未安装或已被删除"
    exit 0
fi

echo "正在卸载 $SCRIPT_NAME..."

# 删除启动脚本
if [ -f "$SCRIPT_PATH" ]; then
    rm "$SCRIPT_PATH"
    echo "已删除启动脚本: $SCRIPT_PATH"
fi

# 删除缩写命令
if [ -f "$INSTALL_DIR/clr" ]; then
    rm "$INSTALL_DIR/clr"
    echo "已删除缩写命令: $INSTALL_DIR/clr"
fi

# 删除项目目录
if [ -d "$INSTALL_PROJECT_DIR" ]; then
    rm -rf "$INSTALL_PROJECT_DIR"
    echo "已删除项目目录: $INSTALL_PROJECT_DIR"
fi

# 验证卸载
if [ ! -f "$SCRIPT_PATH" ] && [ ! -d "$INSTALL_PROJECT_DIR" ] && [ ! -f "$INSTALL_DIR/clr" ]; then
    echo "✅ 卸载成功！"
    echo "$SCRIPT_NAME 已从系统中完全移除"
else
    echo "❌ 卸载失败"
    exit 1
fi