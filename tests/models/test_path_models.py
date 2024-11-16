# tests/models/test_path_models.py

"""
Testes para a classe AnaliseHtml no módulo path_models.

Este módulo contém os testes unitários para a classe AnaliseHtml, que realiza
operações de análise de arquivos HTML em diretórios.
"""

from pathlib import Path
import pytest
from models.path_models import AnaliseHtml


class TestAnaliseHtml:
    """
    Testes para a classe AnaliseHtml, incluindo a inicialização, listagem de arquivos,
    contagem de arquivos e exibição de arquivos em diferentes condições.
    """

    def test_init_with_custom_extension(self):
        """
        Testa a inicialização da classe AnaliseHtml com um diretório e extensão personalizados.
        Verifica se os valores são atribuídos corretamente.
        """
        analise = AnaliseHtml("/tmp", ".pdf")
        assert str(analise.diretorio) == "/tmp"
        assert analise.extensao == ".pdf"

    def test_listar_arquivos_empty_directory(self, tmp_path):
        """
        Testa a listagem de arquivos em um diretório vazio.
        Espera-se que uma exceção FileNotFoundError seja levantada.
        """
        analise = AnaliseHtml(str(tmp_path))
        with pytest.raises(FileNotFoundError) as excinfo:
            analise.listar_arquivos()
        assert "Nenhum arquivo com a extensão" in str(excinfo.value)

    def test_listar_arquivos_with_multiple_files(self, tmp_path):
        """
        Testa a listagem de arquivos em um diretório com múltiplos arquivos e subdiretórios.
        Verifica se apenas arquivos com a extensão desejada são retornados.
        """
        (tmp_path / "test1.html").touch()
        (tmp_path / "test2.html").touch()
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "test3.html").touch()

        analise = AnaliseHtml(str(tmp_path))
        result = analise.listar_arquivos()

        assert result["total"] == 3
        assert len(result["arquivos"]) == 3
        assert all(".html" in f for f in result["arquivos"])

    def test_invalid_directory(self):
        """
        Testa a verificação de um diretório inválido.
        Espera-se que uma exceção ValueError seja levantada.
        """
        analise = AnaliseHtml("/path/that/does/not/exist")
        with pytest.raises(ValueError) as excinfo:
            analise.listar_arquivos()
        assert "não é um diretório válido" in str(excinfo.value)

    def test_contar_arquivos_with_custom_extension(self, tmp_path):
        """
        Testa a contagem de arquivos com uma extensão personalizada.
        Verifica se a contagem de arquivos está correta.
        """
        (tmp_path / "doc1.pdf").touch()
        (tmp_path / "doc2.pdf").touch()

        analise = AnaliseHtml(str(tmp_path), ".pdf")
        count = analise.contar_arquivos()
        assert count == 2

    def test_exibir_arquivos(self, tmp_path, capsys):
        """
        Testa a exibição de arquivos encontrados no diretório.
        Verifica se a saída padrão contém os arquivos esperados.
        """
        test_file = tmp_path / "test.html"
        test_file.touch()

        analise = AnaliseHtml(str(tmp_path))
        analise.exibir_arquivos()

        captured = capsys.readouterr()
        assert "Arquivos encontrados:" in captured.out
        assert str(test_file) in captured.out

    def test_obter_caminhos_absolutos(self, tmp_path):
        """
        Testa a obtenção de caminhos absolutos de arquivos.
        Verifica se todos os caminhos retornados são absolutos.
        """
        test_file = tmp_path / "test.html"
        test_file.touch()

        analise = AnaliseHtml(str(tmp_path))
        paths = analise.obter_caminhos_absolutos()

        assert len(paths) == 1
        assert str(test_file) in paths
        assert all(Path(p).is_absolute() for p in paths)

    def test_mixed_extensions(self, tmp_path):
        """
        Testa a listagem de arquivos com extensões misturadas.
        Verifica se apenas arquivos com a extensão correta são retornados.
        """
        (tmp_path / "test1.html").touch()
        (tmp_path / "test2.txt").touch()
        (tmp_path / "test3.html").touch()

        analise = AnaliseHtml(str(tmp_path))
        result = analise.listar_arquivos()

        assert result["total"] == 2
        assert all(".html" in f for f in result["arquivos"])

    def test_nested_directories(self, tmp_path):
        """
        Testa a listagem de arquivos em diretórios aninhados.
        Verifica se os arquivos nos subdiretórios são listados corretamente.
        """
        (tmp_path / "dir1" / "dir2" / "dir3").mkdir(parents=True)
        (tmp_path / "dir1" / "test1.html").touch()
        (tmp_path / "dir1" / "dir2" / "test2.html").touch()
        (tmp_path / "dir1" / "dir2" / "dir3" / "test3.html").touch()

        analise = AnaliseHtml(str(tmp_path))
        result = analise.listar_arquivos()

        assert result["total"] == 3
        assert any("dir1/test1.html" in f for f in result["arquivos"])
        assert any("dir2/test2.html" in f for f in result["arquivos"])
        assert any("dir3/test3.html" in f for f in result["arquivos"])
