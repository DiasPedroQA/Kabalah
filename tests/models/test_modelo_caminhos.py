# tests/models/test_modelo_caminhos.py

"""
Testes para classes relacionadas ao manuseio de caminhos de arquivos e diretórios.
"""

import json
from unittest.mock import MagicMock, patch
from pathlib import Path
from pytest import raises, fixture
from models.modelo_caminhos import CaminhoBase


class TestCaminhoBase:
    """
    Testes para a classe CaminhoBase que manipula informações de arquivos e diretórios.
    """

    @fixture(autouse=True)
    def __init__(self):
        self.caminho_base = None
        self.caminho_teste = "/home/user/test/file.txt"

    def test_sanitizar_caminho_com_traversal(self):
        """
        The function `test_sanitizar_caminho_com_traversal` tests the sanitization of a path to
        prevent directory traversal vulnerabilities.
        """
        with raises(ValueError, match="Caminho inválido: tentativa de traversal detectada"):
            CaminhoBase("../../../etc/passwd")

    @patch('pathlib.Path.resolve')
    def test_sanitizar_caminho_relativo(self, mock_resolve):
        """
        The function `test_sanitizar_caminho_relativo` tests the creation of a relative path using
        a mocked resolve function.

        :param mock_resolve: The `mock_resolve` parameter seems to be a mock object that is being
        used to simulate the behavior of a function or method called `resolve`. In this test case,
        it is being set up to return a `Path` object representing the path "/home/user/test". This
        mock object is likely used
        """
        mock_resolve.return_value = Path("/home/user/test")
        caminho = CaminhoBase("./test")
        assert isinstance(caminho.caminho_atual, Path)

    def test_context_manager(self):
        with CaminhoBase(self.caminho_teste) as cb:
            assert isinstance(cb, CaminhoBase)

    @patch('pathlib.Path.stat')
    @patch('pathlib.Path.exists')
    def test_estatisticas_formatacao_datas(self, mock_exists, mock_stat):
        mock_exists.return_value = True
        mock_stat.return_value = MagicMock(
            st_size=1024,
            st_mtime=1632223200,
            st_ctime=1632223200
        )

        caminho = CaminhoBase(self.caminho_teste)
        stats = caminho.estatisticas()

        assert "21/09/2021" in stats["modificado_em"]
        assert "21/09/2021" in stats["criado_em"]

    @patch('pathlib.Path.exists')
    def test_estatisticas_arquivo_inexistente(self, mock_exists):
        mock_exists.return_value = False
        caminho = CaminhoBase(self.caminho_teste)
        stats = caminho.estatisticas()
        assert stats["status"] == "falha"
        assert "erro" in stats

    @patch('pathlib.Path.iterdir')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.exists')
    def test_subitens_diretorio_vazio(self, mock_exists, mock_is_dir, mock_iterdir):
        """
        The function tests for subitems in an empty directory.

        :param mock_exists: The `mock_exists`, `mock_is_dir`, and `mock_iterdir` parameters are
        likely mock objects that are being used to simulate the behavior of certain functions or
        methods during testing. In this specific test case, they are being used to mock the
        behavior of the `os.path.exists`, `os
        :param mock_is_dir: The `mock_is_dir` parameter is a mock object that is used to simulate
        the behavior of the `os.path.isdir` function in Python. By setting its return value to
        `True`, the test is simulating the scenario where the path being checked is a directory.
        This allows the test to verify
        :param mock_iterdir: The `mock_iterdir` parameter is a mock object that is used to simulate
        the behavior of the `os.listdir` function in Python. In this specific test case, it is
        being used to simulate the scenario where the directory is empty, as it is returning an
        empty list `[]`. This allows
        """
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        mock_iterdir.return_value = []

        caminho = CaminhoBase(self.caminho_teste)
        resultado = caminho.obter_subitens()
        assert resultado["subitens"] == []

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.is_dir')
    def test_dados_caminho_tipo_desconhecido(self, mock_is_dir, mock_is_file, mock_exists):
        mock_exists.return_value = True
        mock_is_file.return_value = False
        mock_is_dir.return_value = False

        caminho = CaminhoBase(self.caminho_teste)
        resultado = caminho.dados_caminho()
        assert resultado["tipo"] == "desconhecido"

    @patch('pathlib.Path.exists')
    def test_obter_informacoes_caminho_inexistente(self, mock_exists):
        mock_exists.return_value = False
        caminho = CaminhoBase(self.caminho_teste)
        resultado = json.loads(caminho.obter_informacoes())
        assert resultado["infos"]["status"] == "falha"
        assert "erro" in resultado["infos"]

    @patch('pathlib.Path.iterdir')
    @patch('pathlib.Path.is_dir')
    @patch('pathlib.Path.exists')
    def test_obter_informacoes_com_subitens(self, mock_exists, mock_is_dir, mock_iterdir):
        mock_exists.return_value = True
        mock_is_dir.return_value = True
        mock_iterdir.return_value = [Path("/test/sub1"), Path("/test/sub2")]

        caminho = CaminhoBase(self.caminho_teste)
        resultado = json.loads(caminho.obter_informacoes())
        assert "subitens" in resultado["infos"]
        assert len(resultado["infos"]["subitens"]) == 2
