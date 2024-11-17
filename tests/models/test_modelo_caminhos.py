# tests/models/test_modelo_caminhos.py

"""
Testes para classes relacionadas ao manuseio de caminhos de arquivos e diretórios.
"""

from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
from models.modelo_caminhos import Caminho, Arquivo, Pasta

CAMINHO_TESTE = "/home/pedro-pm-dias/Downloads/Chrome"
ARQUIVO_TESTE = "/home/pedro-pm-dias/Downloads/"
PASTA_TESTE = "/home/pedro-pm-dias/Downloads/"


class TestModeloCaminhos:
    """
    Testes para classes que manipulam caminhos usando o módulo `pathlib`.
    """

    @pytest.fixture(autouse=True)
    def __init__(self):
        """
        Inicialização da classe de teste.
        """
        self.caminho_teste = None

    def setup(self):
        """
        Configuração antes de cada teste.
        """
        self.caminho_teste = Path(CAMINHO_TESTE)

    def test_inicializacao_caminho_com_string(self):
        """
        Testa se a classe Caminho é inicializada corretamente com uma string.
        """
        caminho = Caminho(CAMINHO_TESTE)
        assert isinstance(caminho.path, Path)

    def test_inicializacao_caminho_com_path(self):
        """
        Testa se a classe Caminho é inicializada corretamente com um objeto Path.
        """
        obj_path = Path(CAMINHO_TESTE)
        caminho = Caminho(obj_path)
        assert caminho.path == obj_path

    @patch('pathlib.Path.exists')
    def test_propriedade_existe_caminho(self, mock_existe):
        """
        Testa se a propriedade `existe` da classe Caminho funciona corretamente.
        """
        mock_existe.return_value = True
        caminho = Caminho(self.caminho_teste)
        assert caminho.existe is True

    def test_propriedade_extensao_arquivo(self):
        """
        Testa se a extensão do arquivo é recuperada corretamente.
        """
        with patch('pathlib.Path.is_file', return_value=True):
            arquivo = Arquivo(ARQUIVO_TESTE)
            assert arquivo.extensao == ".html"

    @patch('pathlib.Path.stat')
    @patch('pathlib.Path.is_file')
    def test_tamanho_formatado_arquivo(self, mock_e_arquivo, mock_stat):
        """
        Testa se o tamanho formatado do arquivo é calculado corretamente.
        """
        mock_e_arquivo.return_value = True
        mock_stat.return_value = MagicMock(st_size=2048)
        arquivo = Arquivo(ARQUIVO_TESTE)
        assert arquivo.tamanho_formatado() == "2.00 kB"

    def test_inicializacao_arquivo_com_caminho_invalido(self):
        """
        Testa se a classe Arquivo gera um erro ao receber um caminho inválido.
        """
        with patch('pathlib.Path.is_file', return_value=False):
            with pytest.raises(
                ValueError, match="O caminho fornecido não é um arquivo válido"
            ):
                Arquivo("/teste/nao_e_arquivo")

    def test_inicializacao_pasta_com_caminho_invalido(self):
        """
        Testa se a classe Pasta gera um erro ao receber um caminho inválido.
        """
        with patch('pathlib.Path.is_dir', return_value=False):
            with pytest.raises(ValueError, match="O caminho fornecido não é uma pasta válida"):
                Pasta("/teste/nao_e_pasta")

    @patch('pathlib.Path.iterdir')
    @patch('pathlib.Path.is_dir')
    def test_listar_arquivos_com_filtro_na_pasta(self, mock_e_pasta, mock_iterdir):
        """
        Testa se a lista de arquivos com filtros retorna os itens corretos.
        """
        mock_e_pasta.return_value = True
        mock_arquivos = [
            MagicMock(is_file=lambda: True, suffix='.html'),
            MagicMock(is_file=lambda: True, suffix='.py'),
            MagicMock(is_file=lambda: True, suffix='.jpg'),
        ]
        mock_iterdir.return_value = mock_arquivos

        pasta = Pasta(PASTA_TESTE)
        arquivos = pasta.listar_arquivos(extensoes=['.html', '.py'])
        assert len(arquivos) == 2

    @patch('pathlib.Path.iterdir')
    @patch('pathlib.Path.is_dir')
    def test_subitens_com_erro_de_permissao(self, mock_e_pasta, mock_iterdir):
        """
        Testa o comportamento ao lidar com erros de permissão em subitens.
        """
        mock_e_pasta.return_value = True
        mock_iterdir.side_effect = PermissionError()

        pasta = Pasta(PASTA_TESTE)
        subitens = pasta.subitens
        assert len(subitens) == 1
        assert "Inacessível" in str(subitens[0].path)

    def test_converter_caminho_para_dict(self):
        """
        Testa se a conversão de um Caminho para dicionário funciona corretamente.
        """
        with patch('pathlib.Path.exists', return_value=True):
            caminho = Caminho(CAMINHO_TESTE)
            resultado = caminho.para_dict()

            assert isinstance(resultado, dict)
            assert "nome" in resultado
            assert "caminho" in resultado
            assert "existe" in resultado
            assert "tipo" in resultado
