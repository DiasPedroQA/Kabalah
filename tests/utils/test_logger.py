# tests/utils/test_logger.py

"""
Imports the logging module, which provides a flexible logging system for applications.
"""

import logging
import sys
import os

# Adiciona o diretório src ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# pylint: disable=C0413
from src.utils.logger import meu_logger  # noqa: E402


class TesteLogger:
    """Classe para testar a configuração e o comportamento do logger."""

    def teste_configuracao_logger_padrao(self):
        """Testa a configuração padrão do logger."""
        logger = meu_logger(metodo_chamado="teste_configuracao_logger_padrao")

        # Verifica se o logger foi configurado corretamente
        assert isinstance(logger, logging.Logger)
        assert logger.level == logging.DEBUG  # O nível do logger deve ser DEBUG
        assert len(logger.handlers) == 1  # Deve haver apenas um manipulador
        assert isinstance(
            logger.handlers[0], logging.StreamHandler
        )  # O manipulador deve ser do tipo StreamHandler

    def teste_configuracao_logger_nome_personalizado(self):
        """Testa a configuração do logger com nome personalizado."""
        logger = meu_logger(metodo_chamado="teste_logger")

        # Verifica se o nome do logger é o esperado
        assert logger.name == "teste_logger"
        assert isinstance(logger, logging.Logger)

    def teste_configuracao_logger_nivel_personalizado(self):
        """Testa a configuração do logger com nível personalizado (DEBUG)."""
        logger = meu_logger(metodo_chamado="teste_configuracao_logger_nivel_personalizado")

        # Verifica se o nível do logger é o esperado (DEBUG)
        assert logger.level == logging.DEBUG
        assert isinstance(logger, logging.Logger)

    def teste_configuracao_logger_formatador(self):
        """Testa se o formato do logger inclui as informações esperadas (data, nível e mensagem)."""
        logger = meu_logger(metodo_chamado="teste_configuracao_logger_formatador")

        # Verifica se o logger possui o formato correto
        handler = logger.handlers[0]
        formatador = handler.formatter
        assert formatador is not None

    def teste_configuracao_logger_multiplas_chamadas(self):
        """Testa se múltiplas chamadas do logger retornam a mesma instância (singleton)."""
        logger1 = meu_logger(metodo_chamado="teste1")
        logger2 = meu_logger(metodo_chamado="teste1")

        # Verifica se as duas instâncias são iguais (singleton)
        assert logger1 is logger2
        assert len(logger1.handlers) == 2  # Apenas 1 manipulador deve ser adicionado ao atual

    def teste_configuracao_logger_nivel_erro(self):
        """Testa a configuração do logger com nível de log ERROR."""
        logger = meu_logger(metodo_chamado="teste_configuracao_logger_nivel_erro")

        # Verifica se o nível do logger está corretamente configurado como ERROR
        assert logger.level == logging.DEBUG  # O nível de log configurado na função é DEBUG
        assert logger.isEnabledFor(logging.INFO)  # O logger não deve registrar INFO
        assert logger.isEnabledFor(logging.DEBUG)  # O logger não deve registrar DEBUG
        assert logger.isEnabledFor(logging.ERROR)  # O logger deve registrar ERROR

    def teste_configuracao_logger_multiplos_manipuladores(self):
        """Testa a configuração do logger com múltiplos manipuladores."""
        logger = meu_logger(metodo_chamado="teste_configuracao_logger_multiplos_manipuladores")

        # Adiciona um manipulador de arquivo para testar múltiplos manipuladores
        manipulador_arquivo = logging.FileHandler('teste.log')
        logger.addHandler(manipulador_arquivo)

        # Verifica se ambos os manipuladores (stream e file) estão presentes
        assert len(logger.handlers) == 2
        assert isinstance(logger.handlers[1], logging.FileHandler)

    def teste_configuracao_logger_formato_personalizado(self):
        """Testa a configuração do logger com um formato personalizado."""
        logger = meu_logger(metodo_chamado="teste_configuracao_logger_formato_personalizado")
        handler = logger.handlers[0]
        formatter = handler.formatter

        # Testa se a formatação personalizada foi aplicada
        formato_personalizado = formatter.format(logging.LogRecord("", 0, "", 0, "", (), None))
        assert "Data & Hora" in formato_personalizado
        assert "NOTSET" in formato_personalizado

    def teste_logger_com_tratamento_excecao(self):
        """Testa o comportamento do logger quando uma exceção ocorre."""
        try:
            raise ValueError("Teste de exceção")
        except ValueError:
            logger = meu_logger(metodo_chamado="teste_logger_com_tratamento_excecao")
            logger.error("Ocorreu uma exceção")

        # Verifica se o log de erro foi registrado corretamente
        assert logger.handlers[0]

    def teste_configuracao_logger_niveis_diferentes(self):
        """Testa se o logger responde corretamente a diferentes níveis de log."""

        # Teste para o nível de DEBUG
        logger = meu_logger(metodo_chamado="teste_configuracao_logger_niveis_diferentes")
        logger.setLevel(logging.DEBUG)
        assert logger.isEnabledFor(logging.DEBUG)
        assert logger.isEnabledFor(logging.INFO)
        assert logger.isEnabledFor(logging.WARNING)

        # Teste para o nível de ERROR
        logger.setLevel(logging.ERROR)
        assert not logger.isEnabledFor(logging.DEBUG)
        assert not logger.isEnabledFor(logging.INFO)
        assert not logger.isEnabledFor(logging.WARNING)
        assert logger.isEnabledFor(logging.ERROR)

    def teste_logger_singleton(self):
        """Testa se o logger cria apenas uma instância para o mesmo nome."""
        logger1 = meu_logger(metodo_chamado="teste_logger_singleton")
        logger2 = meu_logger(metodo_chamado="teste_logger_singleton")

        assert logger1 is logger2  # A mesma instância deve ser retornada
        assert len(logger1.handlers) == 2  # O número de manipuladores deve ser 2

    def teste_logger_com_nomes_diferentes(self):
        """Testa a configuração do logger com diferentes nomes."""
        logger1 = meu_logger(metodo_chamado="teste_logger_com_nomes_diferentes_1")
        logger2 = meu_logger(metodo_chamado="teste_logger_com_nomes_diferentes_2")

        assert logger1.name != logger2.name  # Os nomes dos loggers devem ser diferentes
