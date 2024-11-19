# tests/controllers/test_controle_caminhos.py

"""
Casos de teste para a classe `ControladorDeCaminhos`.
Os testes cobrem inicialização, processamento de arquivos e pastas,
busca recursiva e geração de relatório JSON.
"""

import json
from unittest.mock import patch
import pytest
from controllers.controle_caminhos import ControladorDeCaminhos


class TestControladorDeCaminhos:
    """
    Classe de testes unitários para o `ControladorDeCaminhos`.
    """

    @pytest.fixture
    def setup_controller(self):
        """
        Configura o ambiente de teste com caminhos de exemplo e uma instância do controlador.
        """
        paths = ["/teste/caminho1", "/teste/caminho2"]
        controller = ControladorDeCaminhos(paths)
        return controller, paths

    @patch('models.modelo_caminhos.Caminho')
    def test_inicializa_cria_lista_de_caminhos(self, mock_caminho, setup_controller):
        """
        Testa se o `ControladorDeCaminhos` inicializa com uma lista de caminhos.
        """
        _, paths = setup_controller
        controlador = ControladorDeCaminhos(paths)
        assert len(controlador.caminhos) == 2
        mock_caminho.assert_called()

    @patch('models.modelo_caminhos.Caminho')
    def test_inicializa_com_filtro_de_extensoes(self):
        """
        Testa a inicialização com uma lista especificada de extensões de arquivo.
        """
        extensoes = [".txt", ".py"]
        controlador = ControladorDeCaminhos(["/teste/caminho"], extensoes)
        assert controlador.filtro_extensoes == extensoes

    @patch('models.modelo_caminhos.Arquivo')
    @patch('models.modelo_caminhos.Caminho')
    def test_processa_arquivo_valido(self, mock_caminho, mock_arquivo, setup_controller):
        """
        Testa o processamento de um arquivo válido e retorna seu conteúdo como dicionário.
        """
        controlador, _ = setup_controller
        mock_caminho.existe = True
        mock_caminho.tipo = "arquivo"
        mock_caminho.path = "/teste/arquivo.txt"
        mock_arquivo.return_value.para_dict.return_value = {"nome": "arquivo.txt"}

        resultado = controlador.processar_arquivo(mock_caminho)

        assert resultado["status"] == "arquivo"
        assert "conteudo" in resultado

    @patch('models.modelo_caminhos.Pasta')
    @patch('models.modelo_caminhos.Caminho')
    def test_processa_pasta_valida(self, mock_caminho, mock_pasta, setup_controller):
        """
        Testa o processamento de uma pasta válida e retorna seu conteúdo como dicionário.
        """
        controlador, _ = setup_controller
        mock_caminho.existe = True
        mock_caminho.tipo = "pasta"
        mock_caminho.path = "/teste/pasta"
        mock_pasta.return_value.listar_arquivos.return_value = []
        mock_pasta.return_value.subitens = []

        resultado = controlador.processar_pasta(mock_caminho)

        assert resultado["status"] == "pasta"
        assert "conteudo" in resultado
        assert "subitens" in resultado

    @patch('models.modelo_caminhos.Caminho')
    def test_processa_caminho_invalido(self, mock_caminho, setup_controller):
        """
        Testa o processamento de um caminho inválido.
        """
        controlador, _ = setup_controller
        mock_caminho.existe = False
        mock_caminho.path = "/invalido/caminho"

        resultado = controlador.processar_caminho(mock_caminho)

        assert resultado["status"] == "inválido"
        assert "mensagem" in resultado

    @patch('models.modelo_caminhos.Caminho')
    def testbusca_recursiva_pasta_vazia(self, mock_caminho, setup_controller):
        """
        Testa a funcionalidade de busca recursiva para uma pasta vazia.
        """
        controlador, _ = setup_controller
        mock_caminho.tipo = "pasta"
        mock_caminho.subitens = []

        resultado = controlador.buscar_recursivamente(mock_caminho)

        assert isinstance(resultado, list)
        assert len(resultado) == 1

    @patch('models.modelo_caminhos.Caminho')
    def testbusca_recursiva_arquivo(self, mock_caminho, setup_controller):
        """
        Testa a busca recursiva para um arquivo.
        """
        controlador, _ = setup_controller
        mock_caminho.tipo = "arquivo"

        resultado = controlador.buscar_recursivamente(mock_caminho)

        assert isinstance(resultado, list)
        assert len(resultado) == 1

    def test_gera_relatorio_json_formato(self, setup_controller):
        """
        Testa a geração de um relatório JSON e seu formato.
        """
        controlador, _ = setup_controller
        with patch.object(controlador, 'processar_e_gerar_json') as mock_process:
            mock_process.return_value = [{"status": "arquivo", "path": "/teste/arquivo.txt"}]
            resultado = controlador.gerar_relatorio_json()

            assert isinstance(resultado, str)
            resultado_processado = json.loads(resultado)
            assert isinstance(resultado_processado, list)
