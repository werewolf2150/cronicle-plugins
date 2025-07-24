import threading

class Lock:
    """
    🔒 Thread-safe lock wrapper
    🇫🇷 Wrapper de verrou pour synchroniser l’accès concurrent à une ressource
    """
    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        """🔐 Acquire lock / 🇫🇷 Acquisition du verrou"""
        self.lock.acquire()
        return self.lock

    def __exit__(self, exception_type, exception_value, traceback):
        """🔓 Release lock / 🇫🇷 Libération du verrou"""
        self.lock.release()

class DataEvent:
    """
    📡 Thread-safe event with attached data payload
    🇫🇷 Événement synchronisé entre threads, avec transmission de données
    """
    def __init__(self):
        self.data = None
        self.lock = Lock()
        self.event = threading.Event()

    def set(self, data):
        """
        Sets the data and triggers the event
        🇫🇷 Définit les données et déclenche l’événement
        """
        with self.lock:
            self.data = data
        self.event.set()

    def clear(self):
        """
        Resets the event and clears its data
        🇫🇷 Réinitialise l’événement et supprime les données
        """
        self.event.clear()
        with self.lock:
            self.data = None

    def wait(self):
        """
        Blocks until the event is set, then returns data
        🇫🇷 Attend que l’événement soit déclenché, puis retourne les données
        """
        self.event.wait()
        with self.lock:
            return self.data

class Flag:
    """
    🏁 Simple boolean flag
    🇫🇷 Drapeau booléen utilisé pour signaler un état
    """
    def __init__(self):
        self.value = False

    def set(self):
        """Set flag to True / 🇫🇷 Active le drapeau"""
        self.value = True

    def __nonzero__(self):
        """Check flag state / 🇫🇷 Teste si le drapeau est actif"""
        return self.value

def wait_for_callback(func):
    """
    ⏳ Waits until a callback is called, then returns its value
    🇫🇷 Attend qu’un callback soit invoqué, puis retourne la donnée transmise
    """
    event = DataEvent()

    def callback(data):
        event.set(data)

    func(callback)
    return event.wait()