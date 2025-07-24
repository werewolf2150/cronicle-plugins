class CronicleEvent:
    """
    📅 Represents a Cronicle event object retrieved via the API.
    🇫🇷 Représente un événement Cronicle, tel qu’obtenu depuis l’API.
    
    This class wraps the raw event dictionary and exposes convenience properties.
    """

    def __init__(self, api, event):
        """
        Initialize the event wrapper.
        🇫🇷 Initialise l’objet événement à partir des données brutes fournies par l’API.
        
        :param api: CronicleAPI instance used to trigger execution
        :param event: Dictionary with event data
        """
        self.api = api              # 🌐 Référence à l’API utilisée / API reference
        self.event = event          # 📦 Données brutes de l’événement / Raw event data

    @property
    def id(self):
        """
        Unique event ID
        🇫🇷 Identifiant unique de l’événement
        :return: str
        """
        return self.event["id"]

    @property
    def title(self):
        """
        Event title / 🇫🇷 Titre de l’événement
        :return: str
        """
        return self.event["title"]

    @property
    def enabled(self):
        """
        Indicates if the event is currently enabled
        🇫🇷 Retourne vrai si l’événement est activé
        :return: bool
        """
        return self.event["enabled"] != 0

    @property
    def web_hook(self):
        """
        Webhook URL associated with the event (if any)
        🇫🇷 Adresse webhook associée à l’événement (si définie)
        :return: str or None
        """
        return self.event.get("web_hook")

    @property
    def multiplex(self):
        """
        Multiplex mode (concurrency settings)
        🇫🇷 Mode multiplex de l’événement (concurrence)
        :return: bool or int
        """
        return self.event["multiplex"]

    def run(self):
        """
        Execute the event via the API
        🇫🇷 Exécute l’événement en passant par l’API Cronicle
        :return: API response (dict)
        """
        return self.api.run_event(self)