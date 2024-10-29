# src/logging/logger.py

"""
Este módulo fornece funções para criar e configurar loggers.
"""

import logging
import os


def setup_logging(log_file='app.log', log_level=logging.INFO):
    """Configura o logging para a aplicação."""

    # Cria o diretório para o log se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configura o formato do log
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join('logs', log_file)),
            logging.StreamHandler(),  # Para exibir no console
        ],
    )


# Função para obter um logger
def get_logger(name):
    """Retorna um logger com o nome especificado."""
    return logging.getLogger(name)
