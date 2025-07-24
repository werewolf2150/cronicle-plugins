#! /usr/bin/env python

import re
from cronicle import CronicleError, CroniclePlugin  # 🔧 Base plugin class + error system
from cronicle.plugin import JsonParser  # 🧬 Parser to decode subprocess JSON output

BITS_PER_GB = 8 * 1024 * 1024 * 1024  # 🧮 1 gigabyte = 8 × 1024³ bits

class SpeedTestPlugin(CroniclePlugin):
    """
    🚀 Cronicle plugin to run speedtest-cli and report network performance
    🇫🇷 Plugin Cronicle pour exécuter speedtest-cli et remonter les performances réseau
    """

    def execute(self, params):
        """
        📡 Executes the speed test and captures results
        🇫🇷 Lance le test de débit et capture les résultats JSON
        """

        args = [params["speedtest"], "--json"]  # 🔍 Exemple : '/usr/bin/speedtest --json'

        # 🛑 Désactive les tests selon les paramètres transmis
        if not params.get("upload", True):
            args.append("--no-upload")
        if not params.get("download", True):
            args.append("--no-download")

        # 🚦 Lance le processus et parse la sortie JSON
        json_result = self.exec_process(args, JsonParser())

        # 📈 Calcule le débit en Gbps (plus lisible pour les logs)
        if params.get("upload", True):
            self.set_perf("upload", BITS_PER_GB / json_result["upload"])  # vitesse en Gbps

        if params.get("download", True):
            self.set_perf("download", BITS_PER_GB / json_result["download"])  # vitesse en Gbps

if __name__ == "__main__":
    SpeedTestPlugin()