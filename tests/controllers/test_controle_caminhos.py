# pylint: disable=C, E

import unittest
import json
from unittest.mock import patch, Mock
from src.controllers.controle_caminhos import ControladorDeCaminhos
# from src.models.modelo_caminhos import Caminho, Arquivo, Pasta


class TestControladorDeCaminhos(unittest.TestCase):

    def setUp(self):
        """Configura o cenário inicial para os testes."""
        self.paths = ["/test/path1", "/test/path2"]
        self.controller = ControladorDeCaminhos(self.paths)

    @patch('src.models.modelo_caminhos.Caminho')
    def test_init_creates_caminhos_list(self, mock_caminho):
        """Testa se a lista de caminhos é criada corretamente na inicialização."""
        controller = ControladorDeCaminhos(self.paths)
        self.assertEqual(len(controller.caminhos), 2)
        mock_caminho.assert_called()

    @patch('src.models.modelo_caminhos.Caminho')
    def test_init_with_extension_filter(self):
        """Testa se o filtro de extensões é configurado corretamente."""
        extensions = [".txt", ".py"]
        controller = ControladorDeCaminhos(self.paths, extensions)
        self.assertEqual(controller.filtro_extensoes, extensions)

    @patch('src.models.modelo_caminhos.Arquivo')
    @patch('src.models.modelo_caminhos.Caminho')
    def test_processar_arquivo_valido(self, mock_caminho, mock_arquivo):
        """Testa o processamento de um arquivo válido."""
        mock_caminho.existe = True
        mock_caminho.tipo = "arquivo"
        mock_caminho.path = "/test/file.txt"
        mock_arquivo.return_value.para_dict.return_value = {"name": "file.txt"}

        result = self.controller.processar_arquivo(mock_caminho)

        self.assertEqual(result["status"], "arquivo")
        self.assertIn("conteudo", result)

    @patch('src.models.modelo_caminhos.Pasta')
    @patch('src.models.modelo_caminhos.Caminho')
    def test_processar_pasta_valida(self, mock_caminho, mock_pasta):
        """Testa o processamento de uma pasta válida."""
        mock_caminho.existe = True
        mock_caminho.tipo = "pasta"
        mock_caminho.path = "/test/folder"
        mock_pasta.return_value.listar_arquivos.return_value = []
        mock_pasta.return_value.subitens = []

        result = self.controller.processar_pasta(mock_caminho)

        self.assertEqual(result["status"], "pasta")
        self.assertIn("conteudo", result)
        self.assertIn("subitens", result)

    @patch('src.models.modelo_caminhos.Caminho')
    def test_processar_caminho_invalido(self, mock_caminho):
        """Testa o processamento de um caminho inválido."""
        mock_caminho.existe = False
        mock_caminho.path = "/invalid/path"

        result = self.controller.processar_caminho(mock_caminho)

        self.assertEqual(result["status"], "inválido")
        self.assertIn("mensagem", result)

    @patch('src.models.modelo_caminhos.Caminho')
    def test_buscar_recursivamente_pasta_vazia(self):
        """Testa a busca recursiva em uma pasta vazia."""
        mock_caminho = Mock()
        mock_caminho.tipo = "pasta"
        mock_caminho.subitens = []

        result = self.controller.buscar_recursivamente(mock_caminho)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    @patch('src.models.modelo_caminhos.Caminho')
    def test_buscar_recursivamente_arquivo(self, mock_caminho):
        """Testa a busca recursiva de um arquivo."""
        mock_caminho.tipo = "arquivo"

        result = self.controller.buscar_recursivamente(mock_caminho)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_gerar_relatorio_json_formato(self):
        """Testa a geração do relatório JSON e seu formato."""
        with patch.object(self.controller, 'processar_e_gerar_json') as mock_process:
            mock_process.return_value = [{"status": "arquivo", "path": "/test/file.txt"}]
            result = self.controller.gerar_relatorio_json()

            self.assertIsInstance(result, str)
            parsed_result = json.loads(result)
            self.assertIsInstance(parsed_result, list)


if __name__ == '__main__':
    unittest.main()
