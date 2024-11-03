# pylint: disable=C
# tests/test_path_models.py

from models.path_models import processar_pasta, processar_arquivo


def test_processar_pasta():
    caminho = "/home/pedro-pm-dias/Downloads/folder1"
    expected_result = {"caminho": caminho, "itens": ["file1.txt", "file2.txt", "subfolder"]}

    result = processar_pasta(caminho)
    assert result == expected_result


def test_processar_arquivo():
    caminho = "/home/pedro-pm-dias/Downloads/file1.txt"
    expected_result = {"caminho": caminho, "conteudo": "Conteúdo do arquivo de exemplo"}

    result = processar_arquivo(caminho)
    assert result == expected_result
