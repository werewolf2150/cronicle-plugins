# 📦 Cronicle Plugin – Speedtest

![Cronicle Plugin](https://img.shields.io/badge/Cronicle-Speedtest-blue?logo=python&logoColor=white&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7%2B-green?logo=python&logoColor=white&style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge)

> 🇫🇷 Plugin Python pour Cronicle permettant de mesurer la performance réseau via `speedtest-cli` ou `Ookla speedtest`.  
> 🇬🇧 Python plugin for Cronicle to measure network speed using `speedtest-cli` or `Ookla speedtest`.

## 📦 Présentation du plugin / Plugin Overview
🇫🇷 Ce plugin permet à Cronicle de mesurer les performances réseau en utilisant speedtest-cli ou l’outil officiel speedtest d’Ookla. Il s’appuie sur Python ≥ 3.7 et fournit des métriques structurées dans les logs, exploitables pour la surveillance ou l’optimisation.

🇬🇧 This plugin allows Cronicle to measure network performance using either speedtest-cli or the official Ookla speedtest tool. It runs on Python ≥ 3.7 and outputs structured metrics to logs, suitable for monitoring or optimization.

## 🚀 Fonctionnalités / Features
- 🇫🇷 Compatible Python 3 (recommandé ≥ 3.7)
🇬🇧 Compatible with Python 3 (recommended ≥ 3.7)
- 🇫🇷 Tests de performance upload et download via CLI speedtest
🇬🇧 Upload and download performance tests via speedtest CLI
- 🇫🇷 Logs structurés avec métriques (JSON en Gbps)
🇬🇧 Structured logs with metrics (JSON format in Gbps)
- 🇫🇷 Webhooks internes pour suivi d'événement Cronicle
🇬🇧 Internal webhooks for Cronicle job tracking
- 🇫🇷 Code modulaire et entièrement documenté
🇬🇧 Modular code, fully documented

## 🧱 Structure du projet / File Structure
- ✅ 🇫🇷 Compatible Python 3 (recommandé ≥ 3.7)
✅ 🇬🇧 Python 3 compatible (recommended ≥ 3.7)
- 📡 🇫🇷 Prise en charge des tests de débit upload et download
📡 🇬🇧 Supports upload and download speed testing
- 📊 🇫🇷 Logs structurés en JSON avec métriques de performance (Gbps)
📊 🇬🇧 Structured JSON logs with performance metrics (Gbps)
- 🔧 🇫🇷 Code modulaire, documenté et facile à maintenir
🔧 🇬🇧 Modular, well-documented and maintainable code
- 🧪 🇫🇷 Utilise des webhooks internes pour suivre les événements dans Cronicle
🧪 🇬🇧 Uses internal webhooks to track Cronicle job


## 🧱 Structure du projet / File Structure

cronicle-plugins/
├── cronicle/
│   ├── speedtest.py           # 🇫🇷 Script principal / 🇬🇧 Main plugin script
│   ├── api.py                 # 🇫🇷 Appels API Cronicle / 🇬🇧 Cronicle API calls
│   ├── plugin.py              # 🇫🇷 Base des plugins / 🇬🇧 Plugin base class
│   ├── job.py                 # 🇫🇷 Suivi du job / 🇬🇧 Job tracking
│   ├── event.py               # 🇫🇷 Données d'événement / 🇬🇧 Event object
│   ├── error.py               # 🇫🇷 Gestion des erreurs / 🇬🇧 Error handling
│   ├── hookmanager.py         # 🇫🇷 Webhook local / 🇬🇧 Local webhook server
│   ├── utils.py               # 🇫🇷 Verrouillage & utilitaires / 🇬🇧 Locking & helpers
│   ├── __init__.py            # 🇫🇷 Interface du module / 🇬🇧 Module interface
│   └── install_speedtest.sh   # 🇫🇷 Script d’installation / 🇬🇧 Installation script
├── schedule/
│   ├── speedtest.cronicle.json         # 🇫🇷 Tâche de test réseau / 🇬🇧 Network test task
│   └── install-speedtest.cronicle.json # 🇫🇷 Tâche d’installation / 🇬🇧 Install plugin task
└── README.md


## ⚙️ Prérequis / Requirements
- 🇫🇷 Python ≥ 3.7 avec les modules standards : `json`, `http.client`, `urllib.parse`  
- 🇬🇧 Python ≥ 3.7 with standard modules: `json`, `http.client`, `urllib.parse`

- 🇫🇷 Le binaire `speedtest` (CLI Ookla) doit être installé — le script l’installe automatiquement si absent  
- 🇬🇧 The `speedtest` binary (Ookla CLI) must be installed — script will auto-install it if missing

- 🇫🇷 Cronicle v3 ou supérieur recommandé  
- 🇬🇧 Cronicle v3 or newer recommended

## 🧪 Intégration dans Cronicle / Integration in Cronicle
- 🇫🇷 Les fichiers du dossier `schedule/` peuvent être importés via l’interface Cronicle → Events → Import Event JSON  
- 🇬🇧 You can import `schedule/` JSON files via Cronicle → Events → Import Event JSON

Cela crée automatiquement les tâches / Automatically creates the tasks:
- ✅ `Installer le plugin Speedtest` / `Install Speedtest plugin` — exécute le script `install_speedtest.sh`
- ✅ `Speedtest Cronicle Plugin` — lance un test de débit (upload / download)

> 🧾 Les tâches incluent une documentation bilingue (FR/ENG) pour faciliter l’intégration dans tout environnement  
> 🧾 Tasks include bilingual (FR/ENG) documentation to simplify integration across environments

## 🧭 Installation
```bash
cd cronicle/
chmod +x install_speedtest.sh
./install_speedtest.sh

🇫🇷 Ce script :
- 📁 Copie tous les fichiers nécessaires dans /opt/cronicle/plugins/speedtest/
- 🐍 Vérifie la présence de Python ≥ 3.7
- 📡 Installe automatiquement le CLI Speedtest (Ookla) si absent
🇬🇧 This script:
- 📁 Copies all necessary files to /opt/cronicle/plugins/speedtest/
- 🐍 Checks that Python ≥ 3.7 is available
- 📡 Automatically installs Ookla Speedtest CLI if missing


🔬 Exemple d’événement Cronicle / Sample Cronicle Event
🔧 Commande / Command :
python3 /opt/cronicle/plugins/speedtest.py

📦 Paramètres JSON / JSON Parameters :
{
  "params": {
    "speedtest": "/usr/bin/speedtest",
    "download": true,
    "upload": true
  }
}

📊 Exemple de sortie / Sample output :
{
  "perf": {
    "upload": 0.88,
    "download": 1.45
  }
}
{
  "complete": 1
}

🇫🇷 Les vitesses sont exprimées en Gbps (gigabits par seconde)
🇬🇧 Speeds are expressed in Gbps (gigabits per second)

🙌 Remerciements / Acknowledgements
🇫🇷 Plugin modernisé pour Python 3 et entièrement documenté par werewolf2150 🧠⚡
🇬🇧 Plugin updated for Python 3 and fully documented by werewolf2150 🧠⚡
🇫🇷 Prêt pour une utilisation en production ou une contribution communautaire
🇬🇧 Ready for production use or open community contribution