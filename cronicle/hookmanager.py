import re
import sys
import json
import time
import threading
from uuid import uuid4
from urllib.parse import urlparse              # 🧭 Analyse d'URL / Parse URLs
from http.client import HTTPConnection         # 🌐 Connexion HTTP / HTTP connection
from http.server import HTTPServer, BaseHTTPRequestHandler  # 📨 Serveur HTTP local
from .utils import Lock, DataEvent             # 🔒 Synchro et event local
from .error import CronicleError               # ⚠️ Gestion des erreurs
from .job import CronicleQueuedJob, CronicleJob  # 🎯 Jobs Cronicle (queued + live)

class HookRequestHandler(BaseHTTPRequestHandler):
    """
    📩 HTTP handler for incoming POST hook calls from Cronicle
    🇫🇷 Gère les requêtes HTTP POST envoyées par Cronicle vers le plugin
    """
    def log_request(self, code='-', size='-'):
        pass  # ❌ Désactive les logs HTTP par défaut

    def do_POST(self):
        """
        🚪 Point d’entrée pour les requêtes POST
        🇫🇷 Parse les données reçues et les transmet au HookManager
        """
        try:
            try:
                data = json.loads(self.rfile.readline())
            except:
                self.send_response(400)  # 📛 JSON invalide
                return

            self.send_response(200)  # ✅ OK
            self.server.manager.handle_request(self.path, data)
        except Exception as e:
            if not isinstance(e, CronicleError):
                e = CronicleError(e)
            sys.stderr.write("%s\n" % str(e))

class HookServer(HTTPServer):
    """
    🖥️ Local HTTP server to receive webhook events
    🇫🇷 Lance un petit serveur HTTP pour écouter les événements Cronicle
    """
    def __init__(self, manager, address):
        super().__init__((address, 0), HookRequestHandler)
        self.manager = manager

        self.thread = threading.Thread(target=self)
        self.thread.daemon = True
        self.thread.start()

    def __call__(self):
        """
        🔄 Démarre le serveur dans son thread
        🇫🇷 Lance le serveur HTTP en continu
        """
        self.serve_forever()

class Hook:
    """
    🧩 Manages lifecycle of a single job via webhook callbacks
    🇫🇷 Gère les callbacks d’un job spécifique via les hooks HTTP
    """
    def __init__(self, api, event, queued_job):
        self.api = api
        self.event = event
        self.queued_job = queued_job
        self.job = None  # ➕ Créé au moment du lancement

    def on_hook_data(self, data):
        """
        ✉️ Traite les données reçues via webhook
        🇫🇷 Interprète l'action transmise par Cronicle (start, complete, fail)
        """
        next_hook = self.event.web_hook
        if next_hook is not None:
            try:
                host = urlparse(next_hook)[1]
                connection = HTTPConnection(host)
                connection.request("POST", next_hook, json.dumps(data))
            except:
                pass  # 🌐 Envoi du webhook secondaire ignoré en cas d’échec

        if data["action"] == "job_launch_failure":
            self.on_job_launch_failure()
            return False
        elif data["action"] == "job_start":
            self.on_job_start(data)
            return True
        elif data["action"] == "job_complete":
            self.on_job_complete(data)
            return False
        else:
            raise CronicleError(100, "Saw unknown job action: %s." % data["action"])

    def on_job_start(self, data):
        """
        ✅ Reçoit le signal de démarrage du job
        🇫🇷 Initialise l’objet CronicleJob et notifie le queued_job
        """
        if self.job is not None:
            raise CronicleError(100, "Saw job_start for a job that already started.")
        self.job = CronicleJob(self.api, self.event, data)
        self.queued_job.on_job_start(self.job)

    def on_job_launch_failure(self):
        """
        ❌ Échec de lancement du job
        🇫🇷 Notifie le queued_job de l’échec
        """
        if self.job is not None:
            raise CronicleError(100, "Saw job_launch_failure for a job that already started.")
        self.queued_job.on_job_failure()

    def on_job_complete(self, data):
        """
        ✔️ Terminaison du job
        🇫🇷 Transmet les données de fin à l’objet CronicleJob
        """
        if self.job is None:
            raise CronicleError(100, "Saw job_complete for a job that never started.")
        self.job.on_job_complete(data)

class HookManager:
    """
    🔧 Core class to manage all webhook jobs and events
    🇫🇷 Gère le serveur HTTP, les hooks actifs, et le déclenchement des jobs
    """
    def __init__(self, api):
        self.api = api
        self.address = "127.0.0.1"
        self.server = HookServer(self, self.address)
        self.hooks = {}  # 🗂️ Dictionnaire des hooks actifs
        self.lock = Lock()  # 🔒 Pour accès concurrent aux hooks

    def create_hook_id(self):
        """
        🆔 Génère un ID unique pour le webhook
        🇫🇷 Empêche les collisions dans le dictionnaire des hooks
        """
        id = str(uuid4())
        if id not in self.hooks:
            return id
        return self.create_hook_id()

    def handle_request(self, path, data):
        """
        📥 Appelé par HookServer lors de la réception d’un webhook
        🇫🇷 Cherche le hook correspondant et lui transmet les données
        """
        id = path[1:]  # 🔎 Supprime le slash initial de l’URL
        with self.lock:
            if id not in self.hooks:
                raise CronicleError(100, "Saw a request for an unknown web hook.")
            hook = self.hooks[id]

        if not hook.on_hook_data(data):
            with self.lock:
                del self.hooks[id]  # 🧹 Nettoyage du hook terminé

    def run_event(self, event):
        """
        ▶️ Déclenche l’exécution d’un événement Cronicle
        🇫🇷 Crée un hook, le lie à l’event, envoie l’appel API
        """
        if event.multiplex:
            raise CronicleError(100, "API does not support running multiplexed events.")

        queued_job = CronicleQueuedJob(self.api, event)

        with self.lock:
            hook_id = self.create_hook_id()
            self.hooks[hook_id] = Hook(self.api, event, queued_job)

        new_hook_url = "http://%s:%s/%s" % (self.address, self.server.server_port, hook_id)

        self.api.call_api("run_event", { "id": event.id, "web_hook": new_hook_url })

        return queued_job