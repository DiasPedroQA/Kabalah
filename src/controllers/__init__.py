"""
Módulo de inicialização para o pacote de controllers.

Este módulo expõe o roteador `path_check_router` do módulo
`path_check_controller`, permitindo que ele seja facilmente
importado e utilizado na aplicação principal.

Exports:
    path_check_router (APIRouter): O roteador para análise de caminhos.
"""

# src/controllers/__init__.py

from .path_check_controller import router as path_check_router

# Exporta o router para ser facilmente incluído no main
__all__ = ["path_check_router"]
