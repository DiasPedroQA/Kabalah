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
        | Data & Hora:  %(log_color)s%(asctime)s%(reset)s            |
        | Função:       %(log_color)s%(funcName)s%(reset)s            |
        | Mensagem:     %(log_color)s%(levelname)-5s -> %(message)s%(reset)s |
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


# def calcular_soma_quadrados_com_logs(logger):
#     """
#     Função que realiza o cálculo da soma dos quadrados de números
#     até um limite aleatório e gera logs para reportar o progresso.

#     Este exemplo simula o processo de somar os quadrados de números inteiros
#     e registra informações no log em diferentes estágios (INFO, DEBUG, WARNING, ERROR).

#     Args:
#         logger (logging.Logger): O logger configurado para registrar as mensagens.
#     """
#     import random
#     import time

#     # Definindo um número aleatório para o limite superior do cálculo
#     limite = random.randint(50, 100)
#     logger.info(f"Iniciando o cálculo da soma dos quadrados até o número {limite}.")

#     resultado_soma = 0
#     for i in range(1, limite + 1):
#         resultado_soma += i**2  # Soma dos quadrados de i
#         time.sleep(random.uniform(0.05, 0.1))  # Simulando algum atraso no cálculo

#         # Registrando a progressão do cálculo
#         if i == limite // 2:  # Alerta no meio do processo
#             logger.warning(
#                 f"Alerta: Chegando perto do meio! Soma parcial dos quadrados: {resultado_soma}."
#             )

#         # Se a soma atingir um número elevado, simula um erro
#         if resultado_soma > 5000 and random.choice([True, False]):
#             logger.error(
#                 f"Erro: Soma excessiva de quadrados atingida "
#                 f"({resultado_soma}). Abortando cálculo."
#             )
#             break

#         # Log para cada número sendo somado (DEBUG)
#         logger.debug(f"Adicionando o quadrado de {i}: {i**2}. Soma atual: {resultado_soma}.")

#     # Finalizando o cálculo
#     logger.info(f"Processo finalizado. Soma total dos quadrados: {resultado_soma}.")


# # Exemplo de uso para comparar os formatos de log
# if __name__ == "__main__":
#     # Criando o logger combinado
#     logger_combinado = meu_logger(metodo_chamado="método de cálculo")

#     # Chamando a função de cálculo com logs
#     print("\nExibindo log com formato combinado:")
#     calcular_soma_quadrados_com_logs(logger_combinado)
