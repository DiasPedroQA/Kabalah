# pylint: disable=C, E

import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.models.modelo_caminhos import Caminho, Arquivo, Pasta


class TestModeloCaminhos(unittest.TestCase):
    def setUp(self):
        self.test_path = Path("/test/path")

    def test_caminho_init_with_string(self):
        caminho = Caminho("/test/path")
        self.assertIsInstance(caminho.path, Path)

    def test_caminho_init_with_path(self):
        path_obj = Path("/test/path")
        caminho = Caminho(path_obj)
        self.assertEqual(caminho.path, path_obj)

    @patch('pathlib.Path.exists')
    def test_caminho_existe_property(self, mock_exists):
        mock_exists.return_value = True
        caminho = Caminho(self.test_path)
        self.assertTrue(caminho.existe)

    def test_arquivo_extensao_property(self):
        with patch('pathlib.Path.is_file') as mock_is_file:
            mock_is_file.return_value = True
            arquivo = Arquivo("/test/file.txt")
            self.assertEqual(arquivo.extensao, ".txt")

    @patch('pathlib.Path.stat')
    @patch('pathlib.Path.is_file')
    def test_arquivo_tamanho_formatado(self, mock_is_file, mock_stat):
        mock_is_file.return_value = True
        mock_stat.return_value = MagicMock(st_size=2048)
        arquivo = Arquivo("/test/file.txt")
        self.assertEqual(arquivo.tamanho_formatado(), "2.00 kB")

    def test_arquivo_init_invalid_path(self):
        with patch('pathlib.Path.is_file') as mock_is_file:
            mock_is_file.return_value = False
            with self.assertRaises(ValueError):
                Arquivo("/test/not_a_file")

    def test_pasta_init_invalid_path(self):
        with patch('pathlib.Path.is_dir') as mock_is_dir:
            mock_is_dir.return_value = False
            with self.assertRaises(ValueError):
                Pasta("/test/not_a_directory")

    @patch('pathlib.Path.iterdir')
    @patch('pathlib.Path.is_dir')
    def test_pasta_listar_arquivos_com_filtro(self, mock_is_dir, mock_iterdir):
        mock_is_dir.return_value = True
        mock_files = [
            MagicMock(is_file=lambda: True, suffix='.txt'),
            MagicMock(is_file=lambda: True, suffix='.py'),
            MagicMock(is_file=lambda: True, suffix='.jpg'),
        ]
        mock_iterdir.return_value = mock_files

        pasta = Pasta("/test/folder")
        arquivos = pasta.listar_arquivos(extensoes=['.txt', '.py'])
        self.assertEqual(len(arquivos), 2)

    @patch('pathlib.Path.iterdir')
    @patch('pathlib.Path.is_dir')
    def test_pasta_subitens_com_permission_error(self, mock_is_dir, mock_iterdir):
        mock_is_dir.return_value = True
        mock_iterdir.side_effect = PermissionError()

        pasta = Pasta("/test/folder")
        subitens = pasta.subitens
        self.assertEqual(len(subitens), 1)
        self.assertIn("Inacessível", str(subitens[0].path))

    def test_caminho_para_dict_formato(self):
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            caminho = Caminho("/test/path")
            resultado = caminho.para_dict()

            self.assertIsInstance(resultado, dict)
            self.assertIn("nome", resultado)
            self.assertIn("caminho", resultado)
            self.assertIn("existe", resultado)
            self.assertIn("tipo", resultado)


if __name__ == '__main__':
    unittest.main()
