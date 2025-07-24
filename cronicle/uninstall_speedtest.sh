#!/bin/bash
# -*- UTF-8 -*-
#
# 🧹 uninstall_speedtest.sh — Cronicle Speedtest Plugin Remover
#
# 🇫🇷 Supprime proprement le plugin Speedtest de Cronicle
# 🇬🇧 Cleanly removes the Speedtest plugin from Cronicle

set -e  # 🚨 Stop execution on any error

### 🔧 Configuration
PLUGIN_NAME="speedtest"
PLUGIN_DIR="/opt/cronicle/plugins/${PLUGIN_NAME}"

echo ""
echo "🧹 Désinstallation du plugin Speedtest / Uninstalling Speedtest plugin"
echo "📂 Cible : ${PLUGIN_DIR}"
echo ""

### 🧾 Vérification présence dossier / Check if plugin folder exists
if [ ! -d "$PLUGIN_DIR" ]; then
  echo "⚠️ Le plugin n'existe pas / Plugin not found — nothing to remove"
  exit 0
fi

### 🧹 Suppression du dossier plugin / Remove plugin folder
rm -rf "$PLUGIN_DIR"
echo "✅ Plugin supprimé / Plugin folder deleted"

### 🧼 Suppression du binaire Speedtest (optionnel) / Optional removal of CLI
if command -v speedtest >/dev/null 2>&1; then
  if [ -f /usr/local/bin/speedtest ]; then
    echo "🗑️ Suppression du binaire Speedtest / Removing Speedtest binary..."
    rm -f /usr/local/bin/speedtest
    echo "✅ Binaire supprimé / Binary removed"
  else
    echo "ℹ️ Binaire Speedtest géré par le système — non supprimé / System-managed binary — not removed"
  fi
else
  echo "✅ Aucun binaire Speedtest détecté / No CLI detected — skipping"
fi

### 📅 Suppression éventuelle des tâches Cronicle / Optionally remove Cronicle tasks
# ✏️ Tu peux supprimer manuellement les tâches via l’interface Cronicle
# ou ajouter ici une requête HTTP à l’API si tu automatises à fond

### ✅ Résumé final
echo ""
echo "🎉 Plugin Speedtest désinstallé avec succès / Speedtest plugin successfully removed"
echo ""