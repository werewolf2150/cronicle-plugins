import inspect  # 🧪 Permet d'accéder à la pile d'exécution / Access call stack info

class CronicleError(Exception):
    """
    🔧 Custom error class for Cronicle plugin system
    💬 Classe d'erreur personnalisée utilisée pour capturer des exceptions dans les plugins Cronicle.
    """

    def __init__(self, *args):
        """
        Initialize the error instance.
        🇫🇷 Initialise une erreur avec soit une exception native, soit un code + message.
        - If one argument is passed: assume it's an Exception
        - If two arguments: (error_code, description)
        """
        if len(args) == 1:
            self.init_with_exception(args[0])
        elif len(args) == 2:
            self.init_with_code(args[0], args[1])
        else:
            self.init_with_code(1, "CronicleError called with too many arguments.")

    def init_with_exception(self, e):
        """
        Build error from native exception
        🇫🇷 Convertit une exception standard Python en CronicleError enrichie (avec fichier + ligne)
        """
        trace = inspect.trace()[-1]  # 📍 Dernière trace appelée / Most recent stack frame
        self.code = -1  # ⛔ Code générique pour erreur inconnue / Generic error code
        self.description = "%s: %s (%s:%s)." % (type(e).__name__, str(e), trace[1], trace[2])

    def init_with_code(self, code, description):
        """
        Assigns a numeric error code and custom description
        🇫🇷 Définit manuellement un code d’erreur et sa description
        """
        self.code = code
        self.description = description

    def __str__(self):
        """
        Returns formatted error string
        🇫🇷 Renvoie une chaîne lisible contenant le code et le message
        """
        return "%d: %s" % (self.code, self.description)