# src/custom_logging/logger.py

"""
Este módulo fornece funções para criar e configurar loggers.
Esta classe configurará o logger para que os logs apareçam com
uma linha em branco entre eles e sejam separados por vários asteriscos (`*`).
"""

import logging
import os


class CustomLogger:
    """Um logger personalizado para registrar mensagens com diferentes níveis de severidade.

    Esta classe fornece métodos para registrar mensagens em vários níveis de severidade,
    incluindo debug, info, warning, error e critical.
    Ela é projetada para facilitar o logging em aplicações com um formato de saída personalizável.

    Args:
        name (str): O nome do logger.
        log_level (int, opcional): O nível de logging. O padrão é logging.DEBUG.

    Atributos:
        logger (logging.Logger): A instância do logger configurada com
        o nome e nível de log especificados.
    """

    def __init__(self, name: str, log_level=logging.DEBUG):
        """Initialize a custom logger.

        This method sets up a logger with a specified name and logging level.
        It configures both console and file handlers to output log messages
        in a formatted manner, ensuring that logs are recorded both on the
        console and in a file.

        Args:
            name (str): The name of the logger.
            log_level (int, optional): The logging level. Defaults to logging.DEBUG.

        Returns:
            None
        """
        # Criação do logger
        self.logger_name = name
        self.logger = logging.getLogger()  # Logger sem nome para mensagens de log

        # Definindo o nível de log
        self.logger.setLevel(log_level)

        # Configuração do handler para saída no console
        console_handler = logging.StreamHandler()

        # Configuração do formato do log (sem nome da classe)
        formatter = logging.Formatter(
            fmt=(
                "_" * 80 + "\n\n" + "🕒 Data e Hora  => {  %(asctime)s  }\n"
                "🌟 Nível        => [  %(levelname)s  ]\n"
                "🔍 Mensagem     => (  %(message)s  )\n" + "_" * 80 + "\n"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",  # Formato personalizado para a data e hora
        )
        console_handler.setFormatter(formatter)

        # Evitar múltiplos handlers no logger
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

        # Criação do handler para salvar os logs em um arquivo
        log_file_path = os.path.join("src/custom_logging", f"{self.logger_name}.log")
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)  # Usar o mesmo formato do console

        # Adicionar o handler de arquivo ao logger
        self.logger.addHandler(file_handler)

    def debug(self, message: str):
        """Registra uma mensagem de depuração (debug)."""
        self.logger.debug(message)

    def info(self, message: str):
        """Registra uma mensagem informativa."""
        self.logger.info(message)

    def warning(self, message: str):
        """Registra uma mensagem de aviso."""
        self.logger.warning(message)

    def error(self, message: str):
        """Registra uma mensagem de erro."""
        self.logger.error(message)

    def critical(self, message: str):
        """Registra uma mensagem crítica."""
        self.logger.critical(message)


# if __name__ == "__main__":
#     logger = CustomLogger("Meu_Logger_Customizado")

#     logger.debug("Esta é uma mensagem de debug")
#     logger.info("Esta é uma mensagem informativa")
#     logger.warning("Esta é uma mensagem de aviso")
#     logger.error("Esta é uma mensagem de erro")
#     logger.critical("Esta é uma mensagem crítica")
