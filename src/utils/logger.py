# src/utils/logger.py

"""
Configuração de logging para o módulo.
Este módulo fornece uma função para configurar um logger simples.
O logger usa um `StreamHandler` para exibir as mensagens no terminal,
com formatação padrão que inclui data/hora, nome do logger, nível do log e a mensagem.
"""

import logging
import colorlog


def meu_logger(metodo_chamado):
    """
    Configura um logger combinado com formato colorido e detalhado.

    Este logger exibe as mensagens com cores para cada nível (INFO, WARNING, ERROR, etc.)
    e inclui informações de data, hora, função e mensagem.

    Args:
        metodo_chamado (str): Nome da função ou método que está chamando o logger.

    Returns:
        logging.Logger: O objeto logger configurado.
    """
    # Criando um logger com o nome da função/método que está sendo chamado
    logger = logging.getLogger(metodo_chamado)
    logger.setLevel(logging.DEBUG)  # Usando DEBUG para uma análise mais detalhada

    # Criando o manipulador que exibe os logs no terminal
    manipulador_terminal = logging.StreamHandler()
    manipulador_terminal.setLevel(logging.DEBUG)

    # Definindo o formato colorido dos logs
    formato = colorlog.ColoredFormatter(
        """
        +------------------------------------------------------------+
        | Data & Hora:  %(log_color)s%(asctime)s%(reset)s
        | Função:       %(log_color)s%(funcName)s%(reset)s
        | Mensagem:     %(log_color)s%(levelname)-5s -> %(message)s%(reset)s
        +------------------------------------------------------------+
        """,
        datefmt="%Y-%m-%d %H:%M:%S",  # Definindo o formato de data
        log_colors={  # Definindo as cores para cada nível de log
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
    )

    manipulador_terminal.setFormatter(formato)  # Aplicando a formatação ao manipulador
    logger.addHandler(manipulador_terminal)  # Adicionando o manipulador ao logger

    return logger
