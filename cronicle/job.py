import sys
import time
from .error import CronicleError  # ⚠️ Gestion des erreurs Cronicle / Custom error class
from .utils import Lock, wait_for_callback  # 🔒 Synchro thread-safe + callback utilities

class CronicleJob:
    """
    🎯 Represents an active Cronicle job instance.
    🇫🇷 Représente un job Cronicle en cours, avec son état, ses données et son suivi.
    """

    def __init__(self, api, event, hook_start_data):
        """
        Initialize job with start hook data
        🇫🇷 Initialise le job avec les données du hook de démarrage
        """
        self.api = api
        self.event = event
        self.hook_start_data = hook_start_data
        self.hook_complete_data = None

        self.lock = Lock()  # 🔐 Protège les accès concurrents
        self.callbacks = []  # 📋 Liste des fonctions à appeler en fin de job

        self.update_status()  # 📦 Récupère les données de l’état initial

    def on_job_complete(self, data):
        """
        📬 Called when job completes. Triggers all callbacks.
        🇫🇷 Appelée à la fin du job. Déclenche tous les callbacks enregistrés.
        """
        if data["id"] != self.id:
            raise CronicleError(100, "Received a complete notification for the wrong job.")
        self.update_status(3)
        with self.lock:
            self.hook_complete_data = data
            callbacks = self.callbacks
            self.callbacks = None
        for callback in callbacks:
            callback(self)

    def update_status(self, retries=0):
        """
        🔁 Attempts to fetch job status from API.
        🇫🇷 Essaie de récupérer le statut du job via l’API avec nombre d’essais configurables.
        """
        while True:
            try:
                job = self.api.call_api("get_job_status", { "id": self.id })["job"]
                break
            except Exception as e:
                if retries == 0:
                    raise
                retries -= 1
                time.sleep(2)  # 💤 Attente entre les tentatives

        with self.lock:
            self.job = job  # 🗂️ Données du job mises à jour

    def on_complete(self, callback):
        """
        🔔 Register a callback to be invoked when job completes.
        🇫🇷 Enregistre une fonction à appeler une fois le job terminé.
        """
        if self.is_complete:
            callback(self)
        with self.lock:
            self.callbacks.append(callback)

    def wait_for_complete(self):
        """
        🕓 Blocks until the job has completed.
        🇫🇷 Attend que le job soit terminé de manière synchrone.
        """
        wait_for_callback(self.on_complete)

    def safe_get(self, property, default=None):
        """
        🔎 Safely retrieves a property from job dictionary
        🇫🇷 Récupère une propriété du job avec valeur par défaut
        """
        with self.lock:
            if property in self.job:
                return self.job[property]
        return default

    @property
    def id(self):
        """🔑 Job ID / 🇫🇷 Identifiant du job"""
        return self.hook_start_data["id"]

    @property
    def is_complete(self):
        """✔️ Whether job is complete / 🇫🇷 Si le job est terminé"""
        return self.safe_get("complete", 0) == 1

    @property
    def is_failed(self):
        """❌ Whether job failed / 🇫🇷 Si le job a échoué"""
        return self.safe_get("code", 0) != 0

    @property
    def progress(self):
        """📊 Job progress (0.0–1.0) / 🇫🇷 Progression du job"""
        if self.is_complete:
            return 1.0
        return self.safe_get("progress", 0.0)

    @property
    def elapsed(self):
        """⏱️ Elapsed time / 🇫🇷 Durée écoulée"""
        return self.safe_get("elapsed")

    @property
    def code(self):
        """🔢 Return code / 🇫🇷 Code de retour"""
        return self.safe_get("code")

    @property
    def description(self):
        """📝 Description / 🇫🇷 Message de fin du job"""
        return self.safe_get("description")

    @property
    def details_url(self):
        """🔗 Job details URL / 🇫🇷 URL des détails du job"""
        return self.hook_start_data["job_details_url"]

class CronicleQueuedJob:
    """
    ⏳ Represents a job queued for execution.
    🇫🇷 Représente un job mis en file d’attente, en attente de démarrage.
    """

    def __init__(self, api, event):
        self.api = api
        self.event = event
        self.lock = Lock()
        self.job = None
        self.callbacks = []
        self.started = False  # ⏯️ Flag de démarrage

    def on_job_start(self, job):
        """
        ▶️ Called when job starts successfully
        🇫🇷 Appelée quand le job démarre effectivement
        """
        with self.lock:
            self.job = job
            self.started = True
            callbacks = self.callbacks
            self.callbacks = None
        for callback in callbacks:
            callback(job)

    def on_job_launch_failure(self):
        """
        ❌ Called if job fails to launch
        🇫🇷 Appelée si le job n’a pas pu démarrer
        """
        with self.lock:
            self.started = True
            callbacks = self.callbacks
            self.callbacks = None
        for callback in callbacks:
            callback(None)

    def on_job_started(self, callback):
        """
        🧷 Registers a callback triggered when job starts
        🇫🇷 Enregistre une fonction à appeler lorsque le job démarre
        """
        with self.lock:
            if self.started:
                callback(self.job)
                return
            self.callbacks.append(callback)

    def wait_for_job(self):
        """
        ⏳ Waits until job has started, raises if failed
        🇫🇷 Attend que le job démarre, ou lève une erreur en cas d’échec
        """
        job = wait_for_callback(self.on_job_started)

        if job is None:
            raise CronicleError(101, "Event %s failed to start." % self.event.title)
        return job