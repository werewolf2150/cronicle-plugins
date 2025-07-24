# 📦 Cronicle Plugin – Speedtest

> 🇫🇷 Plugin Python pour Cronicle permettant de mesurer la performance réseau via `speedtest-cli` ou `Ookla speedtest`.  
> 🇬🇧 Python plugin for Cronicle to measure network speed using `speedtest-cli` or `Ookla speedtest`.

---

## 🚀 Fonctionnalités / Features

- ✅ Compatible Python 3 (recommandé ≥ 3.7)
- 📡 Support des tests upload et download
- 📊 Logs structurés avec métriques de performance (JSON)
- 🔧 Code entièrement documenté et maintenable
- 🧪 Utilisation interne des webhooks pour suivre les jobs

---

## 🧱 Structure du projet / File Structure

cronicle-speedtest/
├── cronicle/
│   ├── speedtest.py           # Script principal du plugin
│   ├── api.py                 # Appel API vers Cronicle
│   ├── plugin.py              # Classe de base des plugins
│   ├── job.py                 # Suivi du job
│   ├── event.py               # Objet événement
│   ├── error.py               # Classe d'erreur
│   ├── hookmanager.py         # Serveur Webhook local
│   ├── utils.py               # Gestion Lock/Event
│   ├── __init__.py            # Interface du module
│   └── install_speedtest.sh   # Script d'installation
└── README.md


---

## ⚙️ Prérequis / Requirements

- Python ≥ 3.7 avec les modules standards : `json`, `http.client`, `urllib.parse`
- `speedtest` CLI installé (Ookla ou speedtest-cli)
- Cronicle v3 ou supérieur

---

## 🧭 Installation

```bash
cd cronicle/
chmod +x install_speedtest.sh
./install_speedtest.sh


Ce script copie tous les fichiers nécessaires dans :
/opt/cronicle/plugins/speedtest/


Et vérifie la présence de Python 3 et de la commande speedtest.

🔬 Exemple d’événement Cronicle
🔧 Commande :
python3 /opt/cronicle/plugins/speedtest/speedtest.py


📦 Paramètres JSON :
{
  "params": {
    "speedtest": "/usr/bin/speedtest",
    "download": true,
    "upload": true
  }
}



📊 Exemple de sortie dans les logs
{
  "perf": {
    "upload": 0.88,
    "download": 1.45
  }
}
{
  "complete": 1
}


Les vitesses sont exprimées en Gbps (gigabits par seconde).

🙌 Remerciements / Acknowledgements
Plugin modernisé pour Python 3 et entièrement documenté par Jean-Denis 🧠⚡
Cette version du plugin est prête pour une utilisation en production ou une contribution communautaire.