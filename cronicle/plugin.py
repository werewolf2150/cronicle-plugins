import sys
import json
import inspect
import subprocess
from .error import CronicleError  # ⚠️ Classe d’erreur personnalisée Cronicle / Custom exception class

class ProcessLogParser:
    """
    📄 Base class for log parsers used during process execution
    🇫🇷 Classe de base pour parser les logs d’un processus (ligne par ligne)
    """

    def parse_line(self, line):
        """
        Called for each line from stdout
        🇫🇷 Méthode appelée pour chaque ligne lue depuis stdout
        """
        pass

    def process_complete(self, code):
        """
        Called after process ends. Raises if exit code is non-zero.
        🇫🇷 Appelée quand le processus se termine — lève une erreur si code de sortie non nul.
        """
        if code != 0:
            raise CronicleError(code, "Process exited with exit code %d." % code)

class TextParser(ProcessLogParser):
    """
    📝 Simple parser that accumulates all lines from stdout
    🇫🇷 Accumule toutes les lignes retournées par le processus
    """

    def __init__(self):
        self.lines = []

    def parse_line(self, line):
        """Adds line to internal list / 🇫🇷 Ajoute la ligne à la liste"""
        self.lines.append(line)

    def process_complete(self, code):
        """
        Returns list of lines if success, else raises
        🇫🇷 Retourne les lignes si succès, lève une erreur sinon
        """
        if code != 0:
            return ProcessLogParser.process_complete(self, code)
        return self.lines

class JsonParser(TextParser):
    """
    🧬 Extends TextParser to return parsed JSON
    🇫🇷 Transforme la sortie texte du processus en JSON Python
    """

    def process_complete(self, code):
        """
        Parses joined text as JSON, raises if malformed
        🇫🇷 Concatène les lignes et tente de parser en JSON
        """
        text = "\n".join(TextParser.process_complete(self, code))
        try:
            return json.loads(text)
        except:
            raise CronicleError(2, "Process returned invalid json.")

class CroniclePlugin:
    """
    🔌 Base class for building a plugin compatible with Cronicle
    🇫🇷 Classe de base pour créer un plugin Python exécutable par Cronicle
    """

    def __init__(self, start=True, stdin=sys.stdin, stdout=sys.stdout):
        """
        Initializes plugin I/O streams and optionally starts execution
        🇫🇷 Initialise les flux d'entrée/sortie et lance le plugin si demandé
        """
        self.stdin = stdin
        self.stdout = stdout
        self.perf = {}  # 🧪 Dictionnaire de mesures de performance
        self.last_progress = 0.0  # 📉 Suivi de la progression

        if start:
            self.start()

    def execute(self, params):
        """
        Main logic of the plugin (to be overridden)
        🇫🇷 Logique principale du plugin — à surcharger dans les sous-classes
        """
        pass

    def start(self):
        """
        Entry point for plugin execution from Cronicle
        🇫🇷 Point d’entrée du plugin appelé par Cronicle (parse, exécute, retourne)
        """
        result = { "complete": 1 }

        try:
            try:
                self.arguments = json.load(self.stdin)
            except:
                raise CronicleError(1, "Invalid input arguments")

            self.execute(self.arguments["params"])

            if len(self.perf) > 0:
                self.log_json({ "perf": self.perf })

        except Exception as e:
            if not isinstance(e, CronicleError):
                e = CronicleError(e)
            result["code"] = e.code
            result["description"] = e.description

        self.log(json.dumps(result))

    def exec_process(self, args, parser, cwd=None):
        """
        🧨 Launches a subprocess and parses its stdout using given parser
        🇫🇷 Lance un sous-processus et parse sa sortie avec un parser personnalisé
        """
        process = subprocess.Popen(
            args,
            cwd=cwd,
            bufsize=0,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        line = process.stdout.readline()
        while line:
            parser.parse_line(line.strip())
            line = process.stdout.readline()

        code = process.wait()
        return parser.process_complete(code)

    def log(self, line):
        """📤 Writes a raw log line to stdout / 🇫🇷 Envoie une ligne dans les logs Cronicle"""
        self.stdout.write("%s\n" % line)
        self.stdout.flush()

    def log_json(self, data):
        """📤 Sends structured JSON log / 🇫🇷 Envoie un log structuré en JSON"""
        self.log(json.dumps(data))

    def set_progress(self, progress):
        """📉 Reports progress as float 0–1 / 🇫🇷 Envoie une progression au moteur Cronicle"""
        if progress != self.last_progress:
            self.log_json({ "progress": progress })

    def set_perf(self, name, time):
        """⏱️ Logs performance metric / 🇫🇷 Stocke une métrique de performance"""
        self.perf[name] = time

    def log_table(self, title, headers, rows, caption=None):
        """
        📊 Outputs a table for display in Cronicle UI
        🇫🇷 Affiche un tableau structuré dans l’interface de Cronicle
        """
        stats = {
            "table": {
                "title": title,
                "header": headers,
                "rows": rows,
            },
        }

        if caption:
            stats["table"]["caption"] = caption

        self.log_json(stats)