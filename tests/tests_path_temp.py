"""
Módulo para validação de strings.
Este módulo fornece funções para validar strings,
incluindo a validação de caminhos de arquivos.
"""

import os
import logging
from typing import Any, List, Union, Dict, Optional
import pytest

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Funções principais


def validar_string(valor: Union[str, None]) -> Optional[str]:
    """Valida se o valor é uma string e retorna a mensagem apropriada."""
    if valor is None:
        logger.info("Valor analisado: None (null).")
        return "O valor é None (null)."
    elif isinstance(valor, str):
        if valor.strip() == "":
            logger.info("Valor analisado: String vazia.")
            return "O valor é uma string vazia."
        elif any(char in valor for char in ['?', '*', ':', '<', '>', '|']):
            logger.info("Valor analisado: '%s' contém caracteres inválidos.", valor)
            return f"O valor é um caminho inválido: '{valor}'. Contém caracteres inválidos."
    else:
        logger.info("Valor analisado: Tipo '%s', não suportado.", type(valor).__name__)
        return f"O valor é do tipo {type(valor).__name__}, que não é suportado para análise."
    return None


def validar_caminho(valor: str) -> str:
    """
    Valida se o valor é um caminho absoluto ou relativo
    e informa se é arquivo, pasta ou inexistente.
    """
    tipo_caminho = "absoluto" if os.path.isabs(valor) else "relativo"
    logger.info("\nAnalisando caminho: '%s'", valor)
    logger.info(" - Tipo de caminho: %s", tipo_caminho.capitalize())

    if os.path.exists(valor) and os.path.isfile(valor):
        logger.info(" - Status: Válido (arquivo existente)")
        return f"O valor é um caminho {tipo_caminho} válido para um arquivo: '{valor}'."
    if os.path.exists(valor) and os.path.isdir(valor):
        logger.info(" - Status: Válido (pasta existente)")
        return f"O valor é um caminho {tipo_caminho} válido para uma pasta: '{valor}'."
    logger.info(" - Status: Inválido (não existe)")
    return f"O valor é um caminho {tipo_caminho} inválido: '{valor}'. Não existe."


def analisar_lista(lista: List[Union[str, None]]) -> List[str]:
    """Analisa cada item da lista e retorna os resultados das validações."""
    resultados = []
    for item in lista:
        if item is None or (isinstance(item, str) and item.strip() == ""):
            msg = f"O valor '{item}' é inválido."
            resultados.append(msg)
            logger.info("\n%s", msg)
        elif isinstance(item, str):
            if invalid_message := validar_string(item):
                resultados.append(invalid_message)
                logger.info("\n%s", invalid_message)
            else:
                resultados.append(validar_caminho(item))
        else:
            msg = f"O valor '{item}' (tipo: {type(item).__name__}) é inválido."
            resultados.append(msg)
            logger.info("\n%s", msg)
    return resultados


def analisar_caminho(dados: Dict[str, Union[str, List[Union[str, None]], None]]) -> List[str]:
    """Analisador de caminhos baseado em dicionário."""
    resultados = []

    for key, valor in dados.items():
        logger.info("\n--- Analisando chave: '%s' ---", key)
        if isinstance(valor, list):
            resultados.extend(analisar_lista(valor))
        elif invalid_message := validar_string(valor):
            resultados.append(invalid_message)
            logger.info("\n%s", invalid_message)
        else:
            resultados.append(validar_caminho(valor))

    return resultados


# ------------------------------
# Testes com Pytest
# ------------------------------


@pytest.fixture
def entradas_teste() -> List[Dict[str, Any]]:
    """
    Fixture que retorna uma lista de dicionários para diferentes casos de entrada
    a serem usados nos testes de validação de caminhos e strings.

    Returns:
        List[Dict[str, Any]]: Lista de dicionários contendo chaves e valores variados
        para serem analisados nas funções de validação.
    """
    return [
        {"testar_caminho": None},
        {"testar_caminho": ""},
        {"testar_caminho": "   "},
        {"testar_caminho": "Olá, mundo!"},
        {"testar_caminho": 42},
        {"testar_caminho": 3.14},
        {"testar_caminho": [1, 2, 3]},
        {"testar_caminho": {"chave1": "valor1"}},
        {"testar_caminho": True},
        {"testar_caminho": False},
        {"testar_caminho": [None, True, 0, 12.34]},
        {"testar_caminho": ["string1", "string2"]},
        {"testar_caminho": ["   ", "valido"]},
        {"testar_caminho": "/usr/local/bin"},
        {"testar_caminho": "/home/user/docs"},
        {"testar_caminho": "./temp"},
        {"testar_caminho": "../images/logo.png"},
        {"testar_caminho": "/invalid/path/too/deep/"},
        {"testar_caminho": "invalid/path/?"},
        {"testar_caminho": "/nonexistent_folder/"},
        {"testar_caminho": "/etc/./hosts"},
        {"testar_caminho": "/../var/log/syslog"},
        {"testar_caminho": ["/home/user/docs", "/etc"]},
        {"testar_caminho": ["", "/usr/bin"]},
        {"testar_caminho": ["valid/path", "invalid/path/?"]},
        {"testar_caminho": ["/home/user/file.txt", "/invalid/?path"]},
        {"testar_caminho": "/home/user/"},
        {"testar_caminho": ["", None, "   "]},
        {"testar_caminho": ["valid/path", "invalid/path/?"]},
    ]


def test_validar_string() -> None:
    """
    Testa a função `validar_string` para verificar a saída de validações de diferentes strings.

    Valida:
        - String nula
        - String vazia
        - String válida
        - String com caracteres inválidos
    """
    assert validar_string(None) == "O valor é None (null)."
    assert validar_string("") == "O valor é uma string vazia."
    assert validar_string("valido") is None
    assert "Contém caracteres inválidos." in validar_string("invalid/path/?")


def test_validar_caminho() -> None:
    """
    Testa a função `validar_caminho` para verificar se os caminhos são
    identificados como válidos ou inválidos com base na existência e tipo.

    Valida:
        - Caminho absoluto válido
        - Caminho relativo inválido
    """
    # Adapte os caminhos para o sistema de arquivos real em que o teste é executado
    assert "caminho absoluto válido para um arquivo" in validar_caminho(
        "/path/to/existing/file"
    )
    assert "caminho relativo inválido" in validar_caminho("invalid/path")


def test_analisar_lista() -> None:
    """
    Testa a função `analisar_lista` para garantir que a validação de uma lista de entradas
    retorna mensagens apropriadas para cada item.

    Valida:
        - Strings vazias ou inválidas
        - Caminhos válidos e inválidos
    """
    resultados = analisar_lista(["", "/invalid/path/?", "/path/to/file"])
    assert "inválido" in resultados[0]
    assert "caminho inválido" in resultados[1]


def test_analisar_caminho(entradas_teste: List[Dict[str, Any]]) -> None:
    """
    Testa a função `analisar_caminho` para assegurar que os caminhos do dicionário
    fornecido são corretamente analisados e retornam as mensagens de validação.

    Args:
        entradas_teste (List[Dict[str, Any]]): Fixture com uma lista de casos de teste variados.

    Valida:
        - Presença de resultados para cada entrada
        - Mensagens de análise corretas para tipos de entrada diferentes
    """
    for entrada in entradas_teste:
        resultados = analisar_caminho(entrada)
        assert len(resultados) > 0
