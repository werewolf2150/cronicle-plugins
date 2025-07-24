# -*- coding: utf-8 -*-
"""
cronicle package initializer 🧩

Ce module expose les composants principaux du framework Cronicle en Python.
It makes the plugin architecture usable by importing key classes for error handling, API access and plugin logic.
"""

# 🛑 Gestion des erreurs personnalisées / Custom error management
from .error import CronicleError

# 🌐 Interface avec l'API Cronicle / Cronicle API interface
from .api import CronicleAPI

# 🔌 Classe de base pour créer des plugins / Base class to build plugins
from .plugin import CroniclePlugin