# src/custom_logging/__init__.py

"""
Este módulo inicializa a configuração de logging para a aplicação,
facilitando o uso da classe CustomLogger em outros módulos.
"""

from .logger import CustomLogger  # noqa: E402

# Inicialização do logger
logger = CustomLogger(__name__)
# logger.info("...Starting my custom logger...")
