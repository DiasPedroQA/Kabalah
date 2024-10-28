"""
Configura o módulo de logging com uma configuração básica.

O nível de logging é definido como `logging.INFO`
e o formato da mensagem de log é definido como `%(message)s`.

Uma instância de logger é criada com o nome do
módulo atual (`__name__`), que pode ser usada para
registrar mensagens ao longo do módulo.
"""

# src/logging/logger.py

import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
