# pylint: disable=C

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# Teste para rota POST /verificacao-caminho com caminho absoluto de arquivo
def test_verificacao_caminho_arquivo_absoluto():
    requisicao = {
        "caminho": "/home/pedro-pm-dias/Downloads/favoritos_08_10_2024.html"
    }

    response = client.post("/verificacao-caminho", json=requisicao)

    assert response.status_code == 200
    # Confirmando que o caminho final é absoluto
    assert response.json() == {
        "absoluto": True,
        "eh_arquivo": True,
        "extensao": ".html",
        "nome": "favoritos_08_10_2024.html",
        "caminho_final": "/home/pedro-pm-dias/Downloads/favoritos_08_10_2024.html"  # noqa: E501
    }


# Teste para rota POST /verificacao-caminho com caminho relativo de arquivo
def test_verificacao_caminho_arquivo_relativo():
    requisicao = {
        "caminho": "../../../../Downloads/favoritos_08_10_2024.html"
    }
    # Usando um caminho relativo

    response = client.post("/verificacao-caminho", json=requisicao)

    assert response.status_code == 200
    # Confirmando o caminho final absoluto
    assert response.json() == {
        "absoluto": True,
        "eh_arquivo": True,
        "extensao": ".html",
        "nome": "favoritos_08_10_2024.html",
        "caminho_final": "/home/pedro-pm-dias/Downloads/favoritos_08_10_2024.html"  # noqa: E501
    }


# Teste para rota POST /verificacao-caminho com caminho absoluto de pasta
def test_verificacao_caminho_diretorio_absoluto():
    requisicao = {
        "caminho": "/home/pedro-pm-dias/Downloads/"
    }

    response = client.post("/verificacao-caminho", json=requisicao)

    assert response.status_code == 200
    # Confirmando que o caminho final é absoluto
    assert response.json() == {
        "absoluto": True,
        "eh_arquivo": False,
        "extensao": None,
        "nome": "Downloads",
        "caminho_final": "/home/pedro-pm-dias/Downloads"
    }


# Teste para rota POST /verificacao-caminho com caminho relativo de pasta
def test_verificacao_caminho_diretorio_relativo():
    requisicao = {
        "caminho": "../../../../Downloads/"  # Caminho relativo
    }

    response = client.post("/verificacao-caminho", json=requisicao)

    try:
        response.status_code == 200
    except AssertionError as ae:
        print('\n\naeaeaeae ->', ae)
    # Confirmando que o caminho final é absoluto
    assert response.json() == {
        "absoluto": True,
        "eh_arquivo": False,
        "extensao": None,
        "nome": "Downloads",
        "caminho_final": "/home/pedro-pm-dias/Downloads"
    }
