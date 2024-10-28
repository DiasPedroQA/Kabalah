"""
Fornece funções para validar e analisar caminhos de arquivos e listas de caminhos.

A função `validar_string` verifica se um valor fornecido é uma string válida
e retorna uma mensagem de erro apropriada se não for.

A função `validar_caminho` verifica se um caminho fornecido é válido
e retorna uma mensagem indicando se o caminho é absoluto ou relativo,
e se aponta para um arquivo, diretório ou não existe.

A função `analisar_lista` aceita uma lista de strings ou valores `None`
e retorna uma lista de mensagens de validação para cada item na lista.

A função `analisar_caminho` aceita um dicionário de valores,
onde os valores podem ser strings ou listas de strings ou valores `None`,
e retorna uma lista de mensagens de validação para cada valor no dicionário.
"""

# test_path_check_controller.py

import os
import pytest
from fastapi.testclient import TestClient
from src.controllers.path_check_controller import router, validar_caminho, validar_string

client = TestClient(router)


@pytest.fixture
def create_temp_file(tmp_path):
    """Cria um arquivo temporário para testes."""
    file = tmp_path / "test_file.txt"
    file.write_text("Conteúdo do arquivo.")
    return str(file)


@pytest.fixture
def create_temp_directory(tmp_path):
    """Cria um diretório temporário para testes."""
    directory = tmp_path / "test_directory"
    directory.mkdir()
    return str(directory)


def test_validar_string():
    """
    Validates the provided input string and returns
    an appropriate error message if the input is invalid.

    Args:
        input_str (str): The input string to be validated.

    Returns:
        str or None: If the input is valid, returns `None`.
            If the input is invalid, returns an error message.
    """
    assert validar_string(None) == "O valor é None (null)."
    assert validar_string("") == "O valor é uma string vazia."
    assert validar_string("valid_string") is None
    assert (
        validar_string("invalid?|*path")
        == "O valor é um caminho inválido: 'invalid?|*path'. Contém caracteres inválidos."
    )
    assert validar_string(123) == "O valor é do tipo int, que não é suportado para análise."


def test_validar_caminho(create_temp_file, create_temp_directory):
    """
    Tests the `validar_caminho` function by checking various valid and invalid
    file and directory paths.

    The test cases cover:
    - Absolute path to a valid file
    - Absolute path to a valid directory
    - Invalid relative path
    - Valid relative path to an existing file

    The test also creates temporary files and directories as needed, and cleans up
    after the test is complete.
    """
    # Teste caminho absoluto para arquivo
    assert validar_caminho(create_temp_file) == (
        f"O valor é um caminho absoluto válido para um arquivo: '{create_temp_file}'. "
        f"Nome do arquivo: 'test_file.txt'."
    )

    # Teste caminho absoluto para diretório
    assert validar_caminho(create_temp_directory) == (
        f"O valor é um caminho absoluto válido para uma pasta: '{create_temp_directory}'."
    )

    # Teste caminho inválido
    assert validar_caminho("caminho/para/um/arquivo/inexistente.txt") == (
        "O valor é um caminho relativo inválido: 'caminho/para/um/arquivo/inexistente.txt'.",
        " Não existe.",
    )

    # Teste caminho relativo para um arquivo existente
    os.makedirs('test_relative_dir', exist_ok=True)  # Cria um diretório para teste
    with open('test_relative_dir/test_file.txt', 'w', encoding='utf-8') as f:
        f.write('Conteúdo do arquivo.')

    assert validar_caminho('test_relative_dir/test_file.txt') == (
        "O valor é um caminho relativo válido para um arquivo: 'test_file.txt'."
    )

    # Limpeza após o teste
    os.remove('test_relative_dir/test_file.txt')
    os.rmdir('test_relative_dir')


def test_analisar_caminho(create_temp_file, create_temp_directory):
    """
    Tests the `analisar_caminho` endpoint by sending various valid
    and invalid file and directory paths as JSON data.

    The test cases cover:
    - Absolute path to a valid file
    - Absolute path to a valid directory
    - Invalid relative path
    - `None` value
    - Empty string
    - Invalid path with special characters

    The test also creates temporary files and directories as needed,
    and checks the expected response from the endpoint.
    """
    # Teste com dicionário de entradas válidas e inválidas
    response = client.post(
        "/analisar_caminho/",
        json={
            "caminho1": create_temp_file,
            "caminho2": create_temp_directory,
            "caminho3": "caminho/para/um/arquivo/inexistente.txt",
            "caminho4": None,
            "caminho5": ["valid_string", "", "invalid?|*path"],
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        f"O valor é um caminho absoluto válido para um arquivo: '{create_temp_file}'."
        f"Nome do arquivo: 'test_file.txt'.",
        f"O valor é um caminho absoluto válido para uma pasta: '{create_temp_directory}'.",
        "O valor é um caminho relativo inválido: 'caminho/para/um/arquivo/inexistente.txt'.",
        " Não existe.",
        "O valor é None (null).",
        "O valor é uma string vazia.",
        "O valor é um caminho inválido: 'invalid?|*path'. Contém caracteres inválidos.",
    ]
