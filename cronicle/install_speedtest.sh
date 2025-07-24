#!/bin/bash
# -*- UTF-8 -*-
#
# 🛠 install_speedtest.sh — Cronicle Speedtest Plugin Installer
#
# 🇫🇷 Installe le plugin Python Speedtest dans Cronicle, avec vérification de compatibilité
# 🇬🇧 Installs the Python Speedtest plugin into Cronicle, with compatibility checks

set -e  # 🚨 Stop execution on any error

### 🔧 Configuration variables

PLUGIN_NAME="speedtest"
PLUGIN_ROOT="/opt/cronicle/plugins/${PLUGIN_NAME}"
PYTHON_BIN="$(which python3)"
SPEEDTEST_BIN="$(which speedtest || true)"
LOCAL_SRC_DIR="$(dirname "$0")"

### 🧾 Introduction
echo ""
echo "🛠 Installing Cronicle Speedtest Plugin"
echo "📂 Source directory: $LOCAL_SRC_DIR"
echo "📦 Target directory: $PLUGIN_ROOT"
echo ""

### 📁 Create target plugin directory
if [ ! -d "$PLUGIN_ROOT" ]; then
    echo "📁 Creating plugin folder..."
    mkdir -p "$PLUGIN_ROOT"
    echo "✅ Folder created at $PLUGIN_ROOT"
else
    echo "📁 Folder already exists — updating files"
fi

### 📥 Copy plugin files from local source
echo "📥 Copying plugin files..."
cp -r "$LOCAL_SRC_DIR/"*.py "$PLUGIN_ROOT/"
cp -r "$LOCAL_SRC_DIR/cronicle" "$PLUGIN_ROOT/"
chmod +x "$PLUGIN_ROOT/speedtest.py"
echo "✅ Files copied successfully"

### 🐍 Check Python 3 environment
if ! "$PYTHON_BIN" -c 'import json, http.client, urllib.parse' >/dev/null 2>&1; then
    echo "❌ Python 3 environment missing required modules"
    echo "💡 Try installing Python 3.10+ and retry"
    exit 1
fi
echo "🐍 Python 3 environment OK"

### 📡 Check speedtest binary presence
if [ -z "$SPEEDTEST_BIN" ]; then
    echo "⚠️ speedtest binary not found"
    echo "💡 Install Ookla CLI: https://www.speedtest.net/apps/cli"
    exit 1
fi
echo "📡 speedtest binary found at $SPEEDTEST_BIN"

### ✅ Final confirmation
echo ""
echo "✅ Plugin installed at: $PLUGIN_ROOT"
echo "🔁 To test manually:"
echo "$PYTHON_BIN $PLUGIN_ROOT/speedtest.py"
echo ""