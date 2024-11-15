# pylint: disable=C
# tests/test_path_models.py

import json
import pytest
from src.models.path_models import AnalisadorDeCaminhos


@pytest.fixture
def arquivo_temporario(tmp_path):
    caminho_arquivo = tmp_path / "arquivo_teste.txt"
    caminho_arquivo.write_text("conteúdo de teste")
    return caminho_arquivo


@pytest.fixture
def pasta_temporaria(tmp_path):
    pasta = tmp_path / "pasta_teste"
    pasta.mkdir()
    (pasta / "arquivo1.txt").write_text("arquivo na pasta")
    (pasta / "arquivo2.txt").write_text("outro arquivo na pasta")
    (pasta / "subpasta").mkdir()
    return pasta


def test_analisar_arquivo(arquivo_temporario):
    analisador = AnalisadorDeCaminhos(str(arquivo_temporario))
    resultado = json.loads(analisador.analisar())
    assert len(resultado) == 1
    assert resultado[0]["resultado"] == "sucesso"
    assert resultado[0]["dados"]["tipo"] == "arquivo"
    assert resultado[0]["dados"]["nome"] == "arquivo_teste.txt"
    assert resultado[0]["dados"]["extensao"] == ".txt"


def test_analisar_pasta(pasta_temporaria):
    analisador = AnalisadorDeCaminhos(str(pasta_temporaria))
    resultado = json.loads(analisador.analisar())
    assert len(resultado) == 1
    assert resultado[0]["resultado"] == "sucesso"
    assert resultado[0]["dados"]["tipo"] == "pasta"
    assert resultado[0]["dados"]["total_arquivos"] == 2
    assert resultado[0]["dados"]["total_pastas"] == 1


def test_caminho_invalido():
    analisador = AnalisadorDeCaminhos("/caminho/invalido")
    resultado = json.loads(analisador.analisar())
    assert len(resultado) == 1
    assert resultado[0]["resultado"] == "erro"
    assert "Caminho não existe" in resultado[0]["mensagem"]
