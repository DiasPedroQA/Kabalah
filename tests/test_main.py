# pylint: disable=C, E

import unittest
# from unittest.mock import patch, MagicMock
from unittest.mock import patch
from src.main import obter_caminhos_e_extensoes, main


class TestMain(unittest.TestCase):
    def test_obter_caminhos_e_extensoes_retorna_tupla(self):
        resultado = obter_caminhos_e_extensoes()
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], list)
        self.assertIsInstance(resultado[1], list)

    def test_obter_caminhos_e_extensoes_conteudo(self):
        caminhos, extensoes = obter_caminhos_e_extensoes()
        self.assertIn("/home/pedro-pm-dias/Downloads/", caminhos)
        self.assertIn("/home/pedro-pm-dias/Downloads/InvalidPath", caminhos)
        self.assertEqual(extensoes, [".html", ".txt"])

    @patch('sys.path')
    @patch('os.path.abspath')
    @patch('os.path.dirname')
    def test_main_adiciona_path_se_necessario(self, mock_dirname, mock_abspath, mock_syspath):
        mock_dirname.return_value = "/fake/path"
        mock_abspath.return_value = "/fake/absolute/path"
        mock_syspath.__contains__.return_value = False

        with patch('builtins.print') as mock_print, patch('src.main.exibir_resultados'):
            main()
            mock_syspath.append.assert_called_once()
            mock_print.assert_called_with("Iniciando a análise dos caminhos fornecidos...\n")

    @patch('sys.path')
    @patch('src.main.exibir_resultados')
    def test_main_nao_adiciona_path_se_ja_existe(self, mock_syspath):
        mock_syspath.__contains__.return_value = True

        with patch('builtins.print'):
            main()
            mock_syspath.append.assert_not_called()

    @patch('src.main.exibir_resultados')
    def test_main_chama_exibir_resultados_com_parametros_corretos(self, mock_exibir):
        with patch('builtins.print'):
            main()
            caminhos, extensoes = obter_caminhos_e_extensoes()
            mock_exibir.assert_called_once_with(caminhos, extensoes)


if __name__ == '__main__':
    unittest.main()
