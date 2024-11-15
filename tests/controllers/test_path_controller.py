# pylint: disable=C, W0621
# tests/controllers/test_path_controller.py

# import pytest
# from flask import json
# from controllers.path_controller import app

# # Configuração do Flask para testes
# app.config['TESTING'] = True


# @pytest.fixture
# def test_client():
#     with app.test_client() as client:
#         yield client


# def test_processar_pasta(test_client):
#     # Dados de entrada
#     response = test_client.post(
#         '/processar',
#         json={
#             "caminhos": ["/home/Downloads/Chrome/Teste/Histórico.html"]
#         }
#     )

#     # Verificações
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert len(data) == 1
#     # assert data[0]["tipo"] == "pasta"
#     assert data[0]["conteudo"]["caminho"] == "/home/Downloads/Chrome/Teste/Histórico.html"


# def test_processar_arquivo(test_client):
#     # Dados de entrada
#     response = test_client.post(
#         '/processar', json={"caminhos": ["/home/Downloads/Chrome/Teste/Histórico.html"]}
#     )

#     # Verificações
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert len(data) == 1
#     assert data[0]["tipo"] == "arquivo"
#     assert (
#         data[0]["conteudo"]["caminho"] == "/home/Downloads/Chrome/Teste/Histórico.html"
#     )


# def test_processar_caminho_invalido(test_client):
#     # Dados de entrada para um caminho inválido
#     response = test_client.post('/processar', json={"caminhos": ["/invalid/path"]})

#     # Verificações
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert len(data) == 1
#     assert "erro" in data[0]
#     assert data[0]["erro"] == "Caminho inválido ou inexistente: /invalid/path"
