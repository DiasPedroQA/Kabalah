# tests/test_main.py

"""
Testes para o módulo `main`.
"""

from unittest.mock import patch
from main import obter_caminhos_e_extensoes, main


class TestMain:
    """
    Testes para as funções no módulo `main`.
    """

    def test_obter_caminhos_e_extensoes_retorna_tupla(self):
        """
        Testa se a função `obter_caminhos_e_extensoes` retorna uma tupla com listas.
        """
        resultado = obter_caminhos_e_extensoes()
        assert isinstance(resultado, tuple)
        assert len(resultado) == 2
        assert isinstance(resultado[0], list)
        assert isinstance(resultado[1], list)

    def test_obter_caminhos_e_extensoes_conteudo(self):
        """
        Testa o conteúdo retornado pela função `obter_caminhos_e_extensoes`.
        """
        caminhos, extensoes = obter_caminhos_e_extensoes()
        assert "/home/pedro-pm-dias/Downloads/" in caminhos
        assert "/home/pedro-pm-dias/Downloads/InvalidPath" in caminhos
        assert extensoes == [".html", ".txt"]

    @patch('sys.path')
    @patch('os.path.abspath')
    @patch('os.path.dirname')
    def test_main_adiciona_path_se_necessario(self, mock_dirname, mock_abspath, mock_syspath):
        """
        Testa se `main` adiciona o caminho ao `sys.path` quando necessário.
        """
        mock_dirname.return_value = "/fake/path"
        mock_abspath.return_value = "/fake/absolute/path"
        mock_syspath.__contains__.return_value = False

        with patch('builtins.print') as mock_print, patch('main.exibir_resultados'):
            main()
            mock_syspath.append.assert_called_once()
            mock_print.assert_called_with("Iniciando a análise dos caminhos fornecidos...\n")

    @patch('sys.path')
    def test_main_nao_adiciona_path_se_ja_existe(self, mock_syspath):
        """
        Testa se `main` não adiciona o caminho ao `sys.path` se já existir.
        """
        mock_syspath.__contains__.return_value = True

        with patch('builtins.print'):
            main()
            mock_syspath.append.assert_not_called()

    @patch('main.exibir_resultados')
    def test_main_chama_exibir_resultados_com_parametros_corretos(self, mock_exibir):
        """
        Testa se `main` chama `exibir_resultados` com os parâmetros esperados.
        """
        with patch('builtins.print'):
            main()
            caminhos, extensoes = obter_caminhos_e_extensoes()
            mock_exibir.assert_called_once_with(caminhos, extensoes)
