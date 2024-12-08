# app/models/__init__.py

"""
Este módulo implementa o modelo PathModel para gerenciar e analisar.
"""


from .json_do_frontend import json_frontend
from .path_model import AnalisadorCaminhos


__all__ = ["json_frontend", "AnalisadorCaminhos"]
