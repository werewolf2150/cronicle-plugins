#!/bin/bash
# -*- UTF-8 -*-
#
# 🛠 install_speedtest.sh — Cronicle Speedtest Plugin Installer
#
# 🇫🇷 Installe le plugin Speedtest pour Cronicle (compatible Alpine, Python 3.7+)
# 🇬🇧 Installs Speedtest plugin into Cronicle (Alpine-compatible, Python 3.7+ required)

set -e  # 🚨 Stop execution on any error

### 🔧 Configuration variables / Variables de configuration
PLUGIN_NAME="speedtest"
PLUGIN_ROOT="/opt/cronicle/plugins/${PLUGIN_NAME}"
PYTHON_BIN="$(which python3)"
BASE_URL="https://raw.githubusercontent.com/werewolf2150/cronicle-plugins/master"

PLUGIN_FILE="speedtest.py"
MODULE_FILES=(
  "cronicle/__init__.py"
  "cronicle/plugin.py"
  "cronicle/error.py"
  "cronicle/api.py"
  "cronicle/hookmanager.py"
  "cronicle/job.py"
  "cronicle/event.py"
  "cronicle/utils.py"
)
SCHEDULE_FILES=(
  "schedule/install-speedtest.cronicle.json"
  "schedule/uninstall-speedtest.cronicle.json"
  "schedule/run-speedtest.cronicle.json"
)

### 🧾 Intro / Introduction
echo ""
echo "🛠 Installation du plugin Speedtest pour Cronicle / Installing Speedtest plugin for Cronicle"
echo "📂 Dossier cible : $PLUGIN_ROOT"
echo ""

### 📁 Create plugin folder / Création du dossier du plugin
if [ ! -d "$PLUGIN_ROOT" ]; then
  echo "📁 Création du dossier / Creating plugin folder..."
  mkdir -p "$PLUGIN_ROOT"
  echo "✅ Dossier créé / Folder created"
else
  echo "📁 Dossier existant — mise à jour / Folder exists — updating files"
fi

### 📥 Download main plugin script / Téléchargement du script principal
echo "📥 Téléchargement du fichier principal / Downloading main script..."
curl -s -L -A "Mozilla/5.0" -o "${PLUGIN_ROOT}/${PLUGIN_FILE}" "${BASE_URL}/${PLUGIN_FILE}" || {
  echo "❌ Échec téléchargement fichier principal / Failed to download plugin script"
  exit 1
}
chmod +x "${PLUGIN_ROOT}/${PLUGIN_FILE}"
echo "✅ Script téléchargé / Script downloaded and made executable"

### 📥 Download Python module files / Téléchargement des modules Python
for file in "${MODULE_FILES[@]}"; do
  DEST="${PLUGIN_ROOT}/${file}"
  URL="${BASE_URL}/${file}"
  mkdir -p "$(dirname "$DEST")"
  curl -s -L -A "Mozilla/5.0" -o "$DEST" "$URL" || {
    echo "❌ Échec téléchargement : ${file} / Failed to download: ${file}"
    exit 1
  }
  echo "✅ Téléchargé : ${file} / Downloaded"
done

### 📥 Download schedule files / Téléchargement des fichiers de tâches Cronicle
echo ""
echo "📅 Téléchargement des fichiers de tâche Cronicle / Downloading Cronicle schedule files"
for file in "${SCHEDULE_FILES[@]}"; do
  DEST="${PLUGIN_ROOT}/${file}"
  URL="${BASE_URL}/${file}"
  mkdir -p "$(dirname "$DEST")"
  curl -s -L -A "Mozilla/5.0" -o "$DEST" "$URL" || {
    echo "❌ Échec téléchargement : ${file} / Failed to download: ${file}"
    exit 1
  }
  echo "✅ Téléchargé : ${file} / Downloaded"
done

### 🩺 Python version check / Vérification version Python
echo ""
echo "🐍 Vérification de la version Python / Checking Python version..."
PY_MAJOR=$("$PYTHON_BIN" -c 'import sys; print(sys.version_info.major)')
PY_MINOR=$("$PYTHON_BIN" -c 'import sys; print(sys.version_info.minor)')

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 7 ]; }; then
  echo "❌ Python ${PY_MAJOR}.${PY_MINOR} trop ancien / Too old — Python ≥ 3.7 requis"
  exit 1
fi
echo "✅ Version Python ${PY_MAJOR}.${PY_MINOR} OK"

### 📦 Python modules check / Vérification des modules requis
echo "🔎 Vérification des modules Python / Checking Python modules..."
if ! "$PYTHON_BIN" -c 'import json, http.client, urllib.parse' >/dev/null 2>&1; then
  echo "❌ Modules manquants : json, http.client, urllib.parse / Missing modules"
  exit 1
fi
echo "✅ Modules requis présents / Required modules present"

### 📡 Speedtest CLI check & install / Vérification & installation du binaire Speedtest
echo "📡 Vérification du binaire Speedtest / Checking Speedtest CLI..."
if ! command -v speedtest >/dev/null 2>&1; then
  echo "⚠️ Speedtest CLI absent — téléchargement manuel / Not found — downloading manually"
  curl -s -L -A "Mozilla/5.0" -o /usr/local/bin/speedtest https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64 || {
    echo "❌ Échec du téléchargement du binaire / Binary download failed"
    exit 1
  }
  chmod +x /usr/local/bin/speedtest
  echo "✅ Binaire Speedtest installé / Speedtest CLI installed"
else
  echo "✅ Speedtest CLI déjà présent / Already installed"
fi

### 🧹 Fix outdated Python imports / Correction des imports obsolètes
echo ""
echo "🩺 Correction des imports Python / Fixing outdated Python imports..."
sed -i 's/from urlparse import/from urllib.parse import/' "${PLUGIN_ROOT}/cronicle/api.py"
sed -i 's/from httplib import/from http.client import/' "${PLUGIN_ROOT}/cronicle/api.py"
sed -i 's/from urlparse import/from urllib.parse import/' "${PLUGIN_ROOT}/cronicle/hookmanager.py"
sed -i 's/from httplib import/from http.client import/' "${PLUGIN_ROOT}/cronicle/hookmanager.py"
sed -i 's/from BaseHTTPServer import/from http.server import/' "${PLUGIN_ROOT}/cronicle/hookmanager.py"

### ✅ Final confirmation / Confirmation finale
echo ""
echo "🎉 Plugin Speedtest installé avec succès / Speedtest plugin successfully installed"
echo "📂 Dossier : $PLUGIN_ROOT"
echo "⚙️ Commande Cronicle : $PYTHON_BIN $PLUGIN_ROOT/$PLUGIN_FILE"
echo "📅 Fichiers de tâches dans : $PLUGIN_ROOT/schedule/"
echo ""