# pylint: disable=C

import os
import pytest
from fastapi import HTTPException
from pathlib import Path
from src.controllers.path_check_controller import verificar_caminho_logica

# Supondo que você tenha um diretório para testes
USERNAME = "pedro-pm-dias"  # Defina um nome de usuário de teste
os.environ["USERNAME"] = USERNAME

# Criação de um caminho absoluto para testes
test_directory = Path(f"/home/{USERNAME}/Downloads")
# Arquivo existente -> /home/tese_usuario/Downloads/favoritos_08_10_2024.html
test_file_existente = test_directory / "favoritos_08_10_2024.html"
# Arquivo inexistente -> /home/tese_usuario/Downloads/favoritos.html
test_file_inexistente = test_directory / "favoritos.html"


# Configurando o ambiente de teste
@pytest.fixture(scope='module', autouse=True)
def setup_test_environment():
    # Criar um diretório de teste
    test_directory.mkdir(exist_ok=True)
    # Criar um arquivo de teste
    test_file_existente.touch(exist_ok=True)
    yield
    # Limpeza após os testes
    test_file_existente.unlink(missing_ok=True)
    test_directory.rmdir()


def test_verificar_caminho_arquivo_existente():
    resultado = verificar_caminho_logica(test_file_existente)
    assert resultado["absoluto"] is True
    assert resultado["eh_arquivo"] is True
    assert resultado["extensao"] == ".html"
    assert resultado["nome"] == "favoritos_08_10_2024.html"
    assert resultado["caminho_final"] == str(test_file_existente.resolve())


def test_verificar_caminho_diretorio_existente():
    resultado = verificar_caminho_logica(test_directory)
    assert resultado["absoluto"] is True
    assert resultado["eh_arquivo"] is False
    assert resultado["extensao"] is None
    assert resultado["nome"] == "Downloads"  # Nome correto para o diretório
    assert resultado["caminho_final"] == str(test_directory.resolve())


def test_verificar_caminho_inexistente():
    with pytest.raises(HTTPException) as exc_info:
        verificar_caminho_logica(test_file_inexistente)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Caminho não encontrado"


def test_verificar_caminho_vazio():
    with pytest.raises(HTTPException) as exc_info:
        verificar_caminho_logica("")
    assert exc_info.value.status_code == 404  # ou outro código que você deseje definir
    assert exc_info.value.detail == "Caminho não encontrado"


# Novos testes para entradas inválidas e inapropriadas
@pytest.mark.parametrize("caminho_invalido", [
    "invalid_path",                # Caminho sem barra inicial
    "/path/with space/file.txt",   # Caminho com espaço
    "/path/with/invalid/char*?",   # Caracteres inválidos
    "/../etc/passwd",              # Tentativa de acessar um caminho fora do permitido
    "/home/username/../username",  # Caminho que usa retrocesso
    "/home/username/./file.txt",   # Caminho que usa ponto atual
])
def test_verificar_caminho_invalido(caminho_invalido):
    with pytest.raises(HTTPException) as exc_info:
        verificar_caminho_logica(caminho_invalido)
    assert exc_info.value.status_code == 404  # ou outro código que você deseje definir
    assert exc_info.value.detail == "Caminho não encontrado"  # Ou outra mensagem que você tenha definido


# Teste para tipo de entrada inválido
@pytest.mark.parametrize("caminho_invalido", [
    12345,                         # Número
    None,                          # None
    ["path/to/file"],              # Lista
    {"caminho": "path/to/file"},   # Dicionário
    object()                       # Objeto genérico
])
def test_verificar_tipo_entrada_invalido(caminho_invalido):
    with pytest.raises(ValueError) as exc_info:
        verificar_caminho_logica(caminho_invalido)
    assert str(exc_info.value) == "Caminho inválido. Por favor, forneça um caminho absoluto válido."
