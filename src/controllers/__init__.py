# src/controllers/__init__.py

"""
Este módulo fornece classes para gerenciar e processar caminhos de arquivos e pastas.

As classes disponíveis incluem:
- GerenciadorCaminhos: Gerencia a identificação e filtragem de arquivos em um caminho.
"""

from .path_controller import GerenciadorCaminhos


__all__ = ["GerenciadorCaminhos"]
