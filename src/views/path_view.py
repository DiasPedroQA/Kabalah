# src/custom_logging/logger.py

"""
Este módulo fornece a classe CustomLogger para criação e configuração de loggers
personalizados. Os logs são formatados com linhas de separação e detalhes em
diferentes níveis de severidade.
"""

import logging
import os


class CustomLogger:
    """
    Um logger personalizado para registrar mensagens com diferentes níveis de severidade.

    Esta classe facilita o logging em aplicações, com um formato de saída
    personalizado e suporte para múltiplos níveis de severidade.

    Argumento(s):
        nome (str): O nome do logger.
        nivel_log (int, opcional): O nível de logging. Padrão é logging.DEBUG.

    Atributos:
        logger (logging.Logger): A instância do logger configurada com o
        nome e nível de log especificados.
    """

    def __init__(self, nome: str, nivel_log=logging.DEBUG):
        """
        Inicializa o logger customizado.

        Este método configura um logger com o nome e o nível especificados.
        Configura tanto a saída para o console quanto para um arquivo de log.

        Argumento(s):
            nome (str): O nome do logger.
            nivel_log (int, opcional): O nível de logging. Padrão é logging.DEBUG = 10.

        Retorna:
            None
        """
        # Criação do logger
        self.nome_logger = nome
        self.logger = logging.getLogger(nome)

        # Definindo o nível de log
        self.logger.setLevel(nivel_log)

        # Configuração do handler para saída no console
        console_handler = logging.StreamHandler()

        # Configuração do formato do log
        formato_log = logging.Formatter(
            fmt=(
                "_" * 95 + "\n\n" + "🕒 Data e Hora  => {  %(asctime)s  }\n"
                "🌟 Nível        => [  %(levelname)s  ]\n"
                "🔍 Mensagem     => (  %(message)s  )\n" + "_" * 95 + "\n"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",  # Formato personalizado para a data e hora
        )
        console_handler.setFormatter(formato_log)

        # Evitar múltiplos handlers no logger
        if not self.logger.hasHandlers():
            self.logger.addHandler(console_handler)

        # Criação do handler para salvar os logs em um arquivo
        nome_logger = self.nome_logger.replace(".", "_")
        caminho_arquivo_log = os.path.join("src/custom_logging", f"{nome_logger}.log")
        arquivo_handler = logging.FileHandler(caminho_arquivo_log)
        arquivo_handler.setFormatter(formato_log)  # Usar o mesmo formato do console

        # Adicionar o handler de arquivo ao logger
        self.logger.addHandler(arquivo_handler)

    def debug(self, mensagem: str):
        """Registra uma mensagem de depuração (debug)."""
        self.logger.debug(mensagem)

    def info(self, mensagem: str):
        """Registra uma mensagem informativa."""
        self.logger.info(mensagem)

    def warning(self, mensagem: str):
        """Registra uma mensagem de aviso."""
        self.logger.warning(mensagem)

    def error(self, mensagem: str):
        """Registra uma mensagem de erro."""
        self.logger.error(mensagem)

    def critical(self, mensagem: str):
        """Registra uma mensagem crítica."""
        self.logger.critical(mensagem)


# if __name__ == "__main__":
#     this_file_name = os.path.basename(__file__).replace(".py", "")
#     logger = CustomLogger(this_file_name)

#     logger.debug("Esta é uma mensagem de debug")
#     logger.info("Esta é uma mensagem informativa")
#     logger.warning("Esta é uma mensagem de aviso")
#     logger.error("Esta é uma mensagem de erro")
#     logger.critical("Esta é uma mensagem crítica")


# src/views/path_check_view.py

"""
Este módulo contém funções para exibir informações relacionadas a arquivos e pastas,
especialmente no contexto de arquivos HTML e criação de PDFs.

Funções:
    exibir_arquivos_html: Exibe a lista de arquivos HTML encontrados.
    exibir_tipo_caminho: Exibe o tipo de caminho (arquivo ou pasta).
"""

from typing import List

from models import FilePathModel


def exibir_arquivos_html(arquivos_html: List[FilePathModel]) -> None:
    """
    Exibe a lista de arquivos HTML encontrados.

    Args:
        arquivos_html (List[FilePathModel]):
        Lista de objetos `FilePathModel` representando arquivos `.html`.
    """
    if not arquivos_html:
        print("Nenhum arquivo HTML encontrado.")
    else:
        print("Arquivos HTML encontrados:")
        for arquivo in arquivos_html:
            print(
                f"- {arquivo.caminho}"
            )  # Supondo que `caminho` é um atributo de FilePathModel


def exibir_tipo_caminho(tipo: str) -> None:
    """
    Exibe o tipo de caminho.

    Args:
        tipo (str): O tipo do caminho (arquivo ou pasta).
    """
    print(f"O tipo de caminho é: {tipo}")
