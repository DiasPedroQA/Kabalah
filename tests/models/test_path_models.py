# tests/test_path_models.py

"""
Tests the functionality of the AnaliseHtml class from the path_models module.
"""

import pytest
from models.path_models import AnaliseHtml


@pytest.fixture
def diretorio_html_temporario(tmp_path):
    """Creates a temporary directory named "pasta_html" and returns it."""
    pasta = tmp_path / "pasta_html"
    pasta.mkdir()
    (pasta / "arquivo1.html").write_text("<html>teste1</html>")
    (pasta / "arquivo2.txt").write_text("texto simples")
    subpasta = pasta / "subpasta"
    subpasta.mkdir()
    (subpasta / "arquivo3.html").write_text("<html>teste2</html>")
    return pasta


def test_analise_html_listar_arquivos_sucesso(diretorio_html=diretorio_html_temporario):
    """Teste de sucesso - Quando arquivos .html são encontrados no diretório."""
    analisador = AnaliseHtml(str(diretorio_html))
    resultado = analisador.listar_arquivos()
    assert resultado["total"] == 2  # Espera-se encontrar 2 arquivos .html
    assert len(resultado["arquivos"]) == 2
    assert all(arquivo.endswith(".html") for arquivo in resultado["arquivos"])


def test_analise_html_extensao_personalizada(tmp_path):
    """Teste para verificar a busca por extensão personalizada (no caso, .txt)."""
    diretorio_temporario = tmp_path / "pasta_txt"
    diretorio_temporario.mkdir()
    (diretorio_temporario / "arquivo1.txt").write_text("texto1")
    (diretorio_temporario / "arquivo2.html").write_text("<html>teste</html>")
    (diretorio_temporario / "arquivo3.txt").write_text("texto2")

    analisador = AnaliseHtml(str(diretorio_temporario), extension=".txt")
    resultado = analisador.listar_arquivos()
    assert resultado["total"] == 2
    assert len(resultado["arquivos"]) == 2
    assert all(arquivo.endswith(".txt") for arquivo in resultado["arquivos"])


def test_analise_html_diretorio_invalido():
    """Teste que garante que uma exceção ValueError é
    levantada quando o diretório é inválido."""
    with pytest.raises(ValueError) as excinfo:
        analisador = AnaliseHtml("/caminho/inexistente")
        analisador.listar_arquivos()
    assert "não é um diretório válido" in str(excinfo.value)


def test_analise_html_sem_arquivos_correspondentes(tmp_path):
    """Teste para garantir que uma exceção FileNotFoundError é
    levantada quando não há arquivos com a extensão especificada."""
    pasta_vazia = tmp_path / "pasta_vazia"
    pasta_vazia.mkdir()
    (pasta_vazia / "arquivo.txt").write_text("texto")

    with pytest.raises(FileNotFoundError) as excinfo:
        analisador = AnaliseHtml(str(pasta_vazia))
        analisador.listar_arquivos()
    assert "Nenhum arquivo com a extensão" in str(excinfo.value)


def test_analise_html_diretorio_vazio(tmp_path):
    """Teste que garante que uma exceção FileNotFoundError é
    levantada quando o diretório está vazio."""
    pasta_vazia = tmp_path / "pasta_vazia"
    pasta_vazia.mkdir()

    with pytest.raises(FileNotFoundError) as excinfo:
        analisador = AnaliseHtml(str(pasta_vazia))
        analisador.listar_arquivos()
    assert "Nenhum arquivo com a extensão" in str(excinfo.value)
