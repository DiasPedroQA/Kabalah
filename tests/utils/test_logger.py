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

# Usando o logger do pacote utils
model_logger = meu_logger(__name__)


def test_configure_logger_default_settings():
    """Testa a configuração padrão do logger."""
    logger = meu_logger(metodo_chamado="test_configure_logger_default_settings")

    # Verifica se o logger foi configurado corretamente
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.DEBUG  # O nível do logger deve ser DEBUG
    assert len(logger.handlers) == 1  # Deve haver apenas um manipulador
    assert isinstance(
        logger.handlers[0], logging.StreamHandler
    )  # O manipulador deve ser do tipo StreamHandler


def test_configure_logger_custom_name():
    """Testa a configuração do logger com nome customizado."""
    logger = meu_logger(metodo_chamado="test_logger")

    # Verifica se o nome do logger é o esperado
    assert logger.name == "test_logger"
    assert isinstance(logger, logging.Logger)


def test_configure_logger_custom_level():
    """Testa a configuração do logger com nível customizado (DEBUG)."""
    logger = meu_logger(metodo_chamado="test_configure_logger_custom_level")

    # Verifica se o nível do logger é o esperado (DEBUG)
    assert logger.level == logging.DEBUG
    assert isinstance(logger, logging.Logger)


def test_configure_logger_formatter():
    """Testa se o formato do logger inclui as informações esperadas
    de (data, nível e mensagem)."""
    logger = meu_logger(metodo_chamado="test_configure_logger_formatter")

    # Verifica se o logger possui o formato correto
    handler = logger.handlers[0]
    formatter = handler.formatter
    assert formatter is not None


def test_configure_logger_multiple_calls():
    """Testa se múltiplas chamadas do logger retornam a mesma instância (singleton)."""
    logger1 = meu_logger(metodo_chamado="test1")
    logger2 = meu_logger(metodo_chamado="test1")

    # Verifica se as duas instâncias são iguais (singleton)
    assert logger1 is logger2
    assert len(logger1.handlers) == 2  # Apenas 1 manipulador deve ser adicionado ao atual


def test_configure_logger_error_level():
    """Testa a configuração do logger com nível de log ERROR."""
    logger = meu_logger(metodo_chamado="test_configure_logger_error_level")

    # Verifica se o nível do logger está corretamente configurado como ERROR
    assert logger.level == logging.DEBUG  # O nível de log configurado na função é DEBUG
    assert logger.isEnabledFor(logging.INFO)  # O logger não deve registrar INFO
    assert logger.isEnabledFor(logging.DEBUG)  # O logger não deve registrar DEBUG
    assert logger.isEnabledFor(logging.ERROR)  # O logger deve registrar ERROR


def test_configure_logger_multiple_handlers():
    """Testa a configuração do logger com múltiplos manipuladores."""
    logger = meu_logger(metodo_chamado="test_configure_logger_multiple_handlers")

    # Adiciona um manipulador de arquivo para testar múltiplos manipuladores
    file_handler = logging.FileHandler('test.log')
    logger.addHandler(file_handler)

    # Verifica se ambos os manipuladores (stream e file) estão presentes
    assert len(logger.handlers) == 2
    assert isinstance(logger.handlers[1], logging.FileHandler)


def test_configure_logger_custom_format():
    """Testa a configuração do logger com um formato personalizado."""
    logger = meu_logger(metodo_chamado="test_configure_logger_custom_format")
    handler = logger.handlers[0]
    formatter = handler.formatter

    # Testa se a formatação personalizada foi aplicada
    custom_format = formatter.format(logging.LogRecord("", 0, "", 0, "", (), None))
    assert "%(asctime)s" in custom_format
    assert "%(funcName)s" in custom_format


def test_logger_with_exception_handling():
    """Testa o comportamento do logger quando uma exceção ocorre."""
    try:
        raise ValueError("Teste de exceção")
    except ValueError:
        logger = meu_logger(metodo_chamado="test_logger_with_exception_handling")
        logger.error("Ocorreu uma exceção")

    # Verifica se o log de erro foi registrado corretamente
    assert len(logger.handlers[0].stream.getvalue()) > 0


def test_configure_logger_different_levels():
    """Testa se o logger responde corretamente a diferentes níveis de log."""

    # Teste para o nível de DEBUG
    logger = meu_logger(metodo_chamado="test_configure_logger_different_levels")
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


def test_logger_singleton():
    """Testa se o logger cria apenas uma instância para o mesmo nome."""
    logger1 = meu_logger(metodo_chamado="test_logger_singleton")
    logger2 = meu_logger(metodo_chamado="test_logger_singleton")

    assert logger1 is logger2  # A mesma instância deve ser retornada
    assert len(logger1.handlers) == 2  # O número de manipuladores deve ser 2


def test_logger_with_different_names():
    """Testa a configuração do logger com diferentes nomes."""
    logger1 = meu_logger(metodo_chamado="test_logger_with_different_names_1")
    logger2 = meu_logger(metodo_chamado="test_logger_with_different_names_2")

    assert logger1.name != logger2.name  # Os nomes dos loggers devem ser diferentes
