# Bookmarks/tests/models/test_modelo_caminhos.py
# pylint: disable=C0413, E0401, E0611

"""
Módulo de testes para a classe CaminhoBase, que verifica funcionalidades
relacionadas ao gerenciamento de caminhos de arquivos e diretórios.
"""

import json
import os
import sys
import tempfile
from pathlib import Path
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.models.modelo_caminhos import CaminhoBase  # noqa: E402


class TestCaminhoBase:
    """
    Testes para a classe CaminhoBase, que manipula informações de arquivos
    e diretórios, verificando suas propriedades, estatísticas e comportamento
    em condições válidas e inválidas.
    """

    @pytest.fixture
    def caminho_diretorio(self):
        """Retorna um caminho de diretório real."""
        return "/home/pedro-pm-dias/Downloads/Chrome/"

    @pytest.fixture
    def caminho_arquivo(self):
        """Retorna um caminho de arquivo real."""
        return "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html"

    @pytest.fixture
    def caminho_invalido(self):
        """Retorna um caminho inválido."""
        return "/home/pedro-pm-dias/Downloads/Chrome/InvalidPath"

    @pytest.fixture
    def caminho_com_espacos(self):
        """Retorna um caminho com espaços."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path_with_spaces = Path(temp_dir, "folder with spaces")
            path_with_spaces.mkdir()
            yield str(path_with_spaces)

    def test_inicializacao_caminho_base(self):
        """Testa a inicialização de um objeto CaminhoBase
        e a atribuição correta do caminho."""
        caminho = CaminhoBase("/home/pedro-pm-dias/Downloads/Chrome/")
        assert caminho.caminho_atual == Path("/home/pedro-pm-dias/Downloads/Chrome/")

    def test_informacoes_diretorio_chrome(self, caminho_diretorio):
        """Testa o retorno correto de informações sobre um diretório,
        como tipo, tamanho e subitens."""
        caminho = CaminhoBase(caminho_diretorio)
        resultado = json.loads(caminho.obter_informacoes())

        # Testando tipos e estatísticas
        assert resultado["infos"]["tipo"] == "diretório"
        assert isinstance(resultado["infos"]["estatisticas"]["tamanho_em_kB"], (int, float))
        assert isinstance(resultado["infos"]["estatisticas"]["modificado_em"], str)
        assert isinstance(resultado["infos"]["estatisticas"]["criado_em"], str)

        # Testando subitens
        assert isinstance(resultado["infos"]["subitens"], list)
        assert all(isinstance(item, str) for item in resultado["infos"]["subitens"])

    def test_informacoes_arquivo_favoritos(self, caminho_arquivo):
        """Testa o retorno correto de informações sobre um arquivo,
        incluindo tipo e estatísticas."""
        caminho = CaminhoBase(caminho_arquivo)
        resultado = json.loads(caminho.obter_informacoes())

        # Testando tipo e caminho absoluto
        assert resultado["infos"]["tipo"] == "arquivo"
        assert resultado["infos"]["caminho_absoluto"] == caminho_arquivo

        # Testando estatísticas
        assert isinstance(resultado["infos"]["estatisticas"]["tamanho_em_kB"], (int, float))
        assert isinstance(resultado["infos"]["estatisticas"]["modificado_em"], str)
        assert isinstance(resultado["infos"]["estatisticas"]["criado_em"], str)

    def test_caminho_invalido(self, caminho_invalido):
        """Testa o comportamento quando um caminho inválido é fornecido,
        verificando a presença de um erro apropriado."""
        caminho = CaminhoBase(caminho_invalido)
        resultado = json.loads(caminho.obter_informacoes())

        # Verificando o erro
        assert "erro" in resultado["infos"]
        assert "não existe" in resultado["infos"]["erro"].lower()

    def test_dados_completos(self):
        """Testa o retorno completo de dados para vários caminhos,
        verificando a presença de chaves essenciais e a validade dos subitens."""
        caminhos = [
            "/home/pedro-pm-dias/Downloads/Chrome/",
            "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html",
            "/home/pedro-pm-dias/Downloads/Chrome/Teste",
        ]

        for caminho_str in caminhos:
            caminho = CaminhoBase(caminho_str)
            resultado = json.loads(caminho.obter_informacoes())

            # Testa a presença de chaves essenciais
            assert "infos" in resultado
            assert "tipo" in resultado["infos"]
            assert "diretorio_pai" in resultado["infos"]
            assert "nome" in resultado["infos"]
            assert "caminho_absoluto" in resultado["infos"]
            assert "estatisticas" in resultado["infos"]
            assert "subitens" in resultado["infos"]

            # Verifica que todos os subitens são caminhos válidos, se for diretório
            if resultado["infos"]["tipo"] == "diretório":
                assert all(Path(item).exists() for item in resultado["infos"]["subitens"])

    def test_symlink_diretorio(self):
        """Testa o comportamento de um symlink,
        verificando se o caminho absoluto do link
        resolve para o caminho correto."""
        with tempfile.TemporaryDirectory() as temp_dir:
            original = Path(temp_dir, "original")
            original.touch()
            link = Path(temp_dir, "link")
            os.symlink(original, link)
            caminho = CaminhoBase(str(link))
            resultado = json.loads(caminho.obter_informacoes())

            # Testando symlink
            assert "infos" in resultado
            assert resultado["infos"]["tipo"] == "arquivo"
            assert Path(resultado["infos"]["caminho_absoluto"]).resolve() == original.resolve()

    def test_caminho_com_tentativa_de_traversal(self):
        """Testa o comportamento com uma tentativa de traversal."""
        caminho = CaminhoBase("/home/user/../../../etc/passwd")
        resultado = json.loads(caminho.obter_informacoes())
        assert "erro" in resultado["infos"]
        assert "traversal" in resultado["infos"]["erro"].lower()

    def test_diretorio_vazio(self):
        """Testa o comportamento de um diretório vazio."""
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = CaminhoBase(temp_dir)
            resultado = json.loads(caminho.obter_informacoes())
            assert resultado["infos"]["tipo"] == "diretório"
            assert resultado["infos"]["subitens"] == []

    def test_arquivo_zero_bytes(self):
        """Testa um arquivo de zero bytes."""
        with tempfile.NamedTemporaryFile() as temp_file:
            caminho = CaminhoBase(temp_file.name)
            resultado = json.loads(caminho.obter_informacoes())
            assert resultado["infos"]["tipo"] == "arquivo"
            assert resultado["infos"]["estatisticas"]["tamanho_em_kB"] == 0.0

    def test_caminho_com_espacos(self, caminho_com_espacos):
        """Testa o comportamento com um caminho contendo espaços."""
        caminho = CaminhoBase(caminho_com_espacos)
        resultado = json.loads(caminho.obter_informacoes())
        assert resultado["infos"]["tipo"] == "diretório"
        assert "folder with spaces" in resultado["infos"]["nome"]

    def test_uso_do_context_manager(self):
        """Testa o uso de um context manager com CaminhoBase."""
        with tempfile.NamedTemporaryFile() as temp_file:
            with CaminhoBase(temp_file.name) as caminho:
                resultado = json.loads(caminho.obter_informacoes())
                assert resultado["infos"]["tipo"] == "arquivo"
                assert Path(resultado["infos"]["caminho_absoluto"]).exists()

    def test_arquivo_com_multiplas_extensoes(self):
        """Testa um arquivo com múltiplas extensões."""
        with tempfile.NamedTemporaryFile(suffix=".tar.gz") as temp_file:
            caminho = CaminhoBase(temp_file.name)
            resultado = json.loads(caminho.obter_informacoes())
            assert ".tar.gz" in resultado["infos"]["nome"]

    def test_diretorio_com_permissoes_restritas(self):
        """Testa um diretório com permissões restritas."""
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chmod(temp_dir, 0o000)
            try:
                caminho = CaminhoBase(temp_dir)
                resultado = json.loads(caminho.obter_informacoes())
                assert resultado["infos"]["tipo"] == "diretório"
                assert "subitens" in resultado["infos"]
            finally:
                os.chmod(temp_dir, 0o755)

    def test_caminho_muito_longo(self):
        """Testa um caminho muito longo."""
        long_path = "/a" * 255
        caminho = CaminhoBase(long_path)
        resultado = json.loads(caminho.obter_informacoes())
        assert "erro" in resultado["infos"]
        assert resultado["infos"]["status"] == "falha"
