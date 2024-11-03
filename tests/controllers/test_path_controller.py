# pylint: disable=C
# tests/controllers/test_path_controller.py

import pytest
from flask import json
from controllers.path_controller import app


# Mock para processar_pasta e processar_arquivo
def mock_processar_pasta(caminho):
    return {"caminho": caminho, "itens": ["file1.txt", "file2.txt"]}


def mock_processar_arquivo(caminho):
    return {"caminho": caminho, "conteudo": "Conteúdo do arquivo de exemplo"}


# Substituir as funções de processamento reais pelos mocks
app.config['TESTING'] = True


@pytest.fixture
def test_client():
    with app.test_client() as client:
        yield client


def test_processar_pasta(client, monkeypatch):
    # Substituindo a função processar_pasta pelo mock
    monkeypatch.setattr(
        "src.controllers.path_controller.processar_pasta", mock_processar_pasta
    )

    # Dados de entrada
    response = client.post('/processar', json={"caminhos": ["/fake/path/to/folder"]})

    # Verificações
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["tipo"] == "diretório"
    assert data[0]["conteudo"]["caminho"] == "/fake/path/to/folder"


def test_processar_arquivo(client, monkeypatch):
    # Substituindo a função processar_arquivo pelo mock
    monkeypatch.setattr(
        "src.controllers.path_controller.processar_arquivo", mock_processar_arquivo
    )

    # Dados de entrada
    response = client.post('/processar', json={"caminhos": ["/fake/path/to/file.txt"]})

    # Verificações
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["tipo"] == "arquivo"
    assert data[0]["conteudo"]["caminho"] == "/fake/path/to/file.txt"


def test_processar_caminho_invalido(client):
    # Dados de entrada para um caminho inválido
    response = client.post('/processar', json={"caminhos": ["/invalid/path"]})

    # Verificações
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert "erro" in data[0]
    assert data[0]["erro"] == "Caminho inválido ou inexistente: /invalid/path"
