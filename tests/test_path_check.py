# pylint: disable=C

import os
import pytest
from fastapi import HTTPException
from pathlib import Path
from src.controllers.path_check_controller import verificar_caminho_logica

# Supondo que você tenha um diretório para testes
USERNAME = "teste_usuario"  # Defina um nome de usuário de teste
os.environ["USERNAME"] = USERNAME

# Criação de um caminho absoluto para testes
test_directory = Path(f"/home/{USERNAME}/test_directory")
test_file = test_directory / "test_file.txt"


# Configurando o ambiente de teste
@pytest.fixture(scope='module', autouse=True)
def setup_test_environment():
    # Criar um diretório de teste
    test_directory.mkdir(exist_ok=True)
    # Criar um arquivo de teste
    test_file.touch(exist_ok=True)
    yield
    # Limpeza após os testes
    test_file.unlink(missing_ok=True)
    test_directory.rmdir()


def test_verificar_caminho_arquivo_existente():
    resultado = verificar_caminho_logica("test_directory/test_file.txt")
    assert resultado["absoluto"] is True
    assert resultado["eh_arquivo"] is True
    assert resultado["extensao"] == ".txt"
    assert resultado["nome"] == "test_file.txt"
    assert resultado["caminho_final"] == str(test_file.resolve())


def test_verificar_caminho_diretorio_existente():
    resultado = verificar_caminho_logica("test_directory/")
    assert resultado["absoluto"] is True
    assert resultado["eh_arquivo"] is False
    assert resultado["extensao"] is None
    assert resultado["nome"] == "test_directory"
    assert resultado["caminho_final"] == str(test_directory.resolve())


def test_verificar_caminho_inexistente():
    with pytest.raises(HTTPException) as exc_info:
        verificar_caminho_logica("test_directory/arquivo_inexistente.txt")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Caminho não encontrado"


def test_verificar_caminho_vazio():
    with pytest.raises(HTTPException) as exc_info:
        verificar_caminho_logica("")
    assert exc_info.value.status_code == 404  # ou outro código que você deseje definir
    assert exc_info.value.detail == "Caminho não encontrado"
