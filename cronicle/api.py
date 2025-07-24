import json
from urllib.parse import urlparse, urljoin  # 🧭 Analyse et combinaison d'URLs / Parse and join URLs
from http.client import HTTPConnection, HTTPException  # 🌐 Requêtes HTTP en Python 3 / HTTP requests
from .error import CronicleError  # ⚠️ Gestion des erreurs personnalisées / Custom error handling
from .hookmanager import HookManager  # 🔌 Gestion des hooks d’événements / Event hook manager
from .event import CronicleEvent  # 📅 Modèle d’événement Cronicle / Cronicle event structure

class CronicleAPI:
    def __init__(self, host, key):
        self.key = key  # 🔐 Clé API d’authentification / API authentication key
        self.hook_manager = None

        # 🔗 Génère l’URL complète vers l’API / Build full API URL
        self.url = urljoin(host, "/api/")
        parts = urlparse(self.url)

        # ❌ Vérifie que l’URL utilise bien HTTP / Make sure the scheme is HTTP
        if parts[0] != "http":
            raise CronicleError(100, "Unsupported scheme for API: %s." % host)

        self.host = parts[1]  # 🖥️ Nom d’hôte extrait de l’URL / Extracted hostname

    def run_event(self, event):
        # 🔄 Initialise HookManager si besoin / Initialize hook manager if missing
        if self.hook_manager is None:
            self.hook_manager = HookManager(self)
        return self.hook_manager.run_event(event)  # ▶️ Lance l’événement / Run the event

    def call_api(self, name, params):
        # 🧱 Construit l’URL de l’API REST / Build full endpoint URL
        url = urljoin(self.url, "app/%s/v1" % name)

        # 🛡️ Ajoute la clé API à la requête / Add API key to request params
        params["api_key"] = self.key
        headers = {
            "Content-Type": "application/json",  # 📦 Envoie des données JSON / Send JSON payload
        }

        try:
            # 🌐 Création de la requête HTTP POST / Create HTTP POST request
            connection = HTTPConnection(self.host)
            connection.request("POST", url, json.dumps(params), headers)
            response = connection.getresponse()
        except HTTPException as e:
            # 🧨 En cas d’échec de connexion / If connection fails
            raise CronicleError(100, "API call failed: %s." % str(e))

        # 📉 Vérifie que le code de retour est entre 200 et 299 / Ensure status code is 2xx
        if response.status < 200 or response.status >= 300:
            raise CronicleError(100, "API call failed: %d %s." % (response.status, response.reason))

        try:
            # 📬 Parse la réponse JSON / Decode JSON response
            result = json.loads(response.read())
        except:
            raise CronicleError(100, "API call returned unparsable data.")

        # 🚦 Vérifie le code de retour Cronicle / Check API-level return code
        if result["code"] != 0:
            raise CronicleError(100, "API call failed with result: '(%s) %s'." % (result["code"], result["description"]))

        return result  # 🎉 Retourne la réponse finale / Return final API response

    def get_event(self, id=None, title=None):
        # 📋 Prépare les paramètres de recherche d’événement / Build event query params
        params = {}
        if id is not None and len(id) > 0:
            params["id"] = id
        elif title is not None and len(title) > 0:
            params["title"] = title
        else:
            # ❌ Ni ID ni titre fourni / Neither ID nor title given
            raise CronicleError(100, "Attempt to retrieve an event with no id or title.")

        # 📡 Appelle l’API et instancie l’objet événement / Call API and instantiate event
        event = self.call_api("get_event", params)["event"]
        return CronicleEvent(self, event)