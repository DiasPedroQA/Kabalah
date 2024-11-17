# tests/views/test_visual_caminho.py

"""
Testes para `visual_caminho` usando pytest.
"""

import json
from unittest.mock import patch
from views.visual_caminho import validar_entradas, filtrar_por_extensao, exibir_resultados


class TestVisualCaminho:
    """
    Classe de testes para funções em `visual_caminho`.
    """

    def test_validar_entradas_caminhos_invalidos(self):
        """
        Testa se entradas inválidas para caminhos retornam mensagens de erro apropriadas.
        """
        resultado = validar_entradas("not_a_list", None)
        assert resultado is not None
        assert "deve ser uma lista" in resultado

    def test_validar_entradas_caminhos_tipos_invalidos(self):
        """
        Testa se tipos inválidos dentro da lista de caminhos geram mensagens de erro.
        """
        resultado = validar_entradas(["/path/1", 2, "/path/3"], None)
        assert resultado is not None
        assert "devem ser do tipo string" in resultado

    def test_validar_entradas_extensoes_invalidas(self):
        """
        Testa se entradas inválidas para extensões retornam mensagens de erro apropriadas.
        """
        resultado = validar_entradas(["/path/1"], "not_a_list")
        assert resultado is not None
        assert "deve ser uma lista" in resultado

    def test_validar_entradas_extensoes_tipos_invalidos(self):
        """
        Testa se tipos inválidos dentro da lista de extensões geram mensagens de erro.
        """
        resultado = validar_entradas(["/path/1"], [".txt", 123])
        assert resultado is not None
        assert "devem ser do tipo string" in resultado

    def test_validar_entradas_validas(self):
        """
        Testa se entradas válidas para caminhos e extensões retornam None.
        """
        resultado = validar_entradas(["/path/1", "/path/2"], [".txt", ".py"])
        assert resultado is None

    def test_filtrar_por_extensao_sem_filtro(self):
        """
        Testa se `filtrar_por_extensao` retorna todos os arquivos quando nenhum filtro é fornecido.
        """
        arquivos = [
            {"nome": "file1.txt", "extensao": ".txt"},
            {"nome": "file2.py", "extensao": ".py"},
        ]
        resultado = filtrar_por_extensao(arquivos, None)
        assert resultado == arquivos

    def test_filtrar_por_extensao_com_filtro(self):
        """
        Testa se `filtrar_por_extensao` retorna apenas os arquivos que correspondem ao filtro.
        """
        arquivos = [
            {"nome": "file1.txt", "extensao": ".txt"},
            {"nome": "file2.py", "extensao": ".py"},
            {"nome": "file3.jpg", "extensao": ".jpg"},
        ]
        resultado = filtrar_por_extensao(arquivos, [".txt", ".py"])
        assert len(resultado) == 2
        assert all(arq["extensao"] in [".txt", ".py"] for arq in resultado)

    @patch('controllers.controle_caminhos.ControladorDeCaminhos')
    @patch('builtins.print')
    def test_exibir_resultados_erro_validacao(self, mock_print, mock_controlador):
        """
        Testa se `exibir_resultados` exibe um erro de validação ao receber entradas inválidas.
        """
        exibir_resultados("caminho_invalido")
        mock_print.assert_called_with(
            "Erro: 'caminhos' deve ser uma lista de strings representando caminhos."
        )
        mock_controlador.assert_not_called()

    @patch('controllers.controle_caminhos.ControladorDeCaminhos')
    @patch('builtins.print')
    def test_exibir_resultados_sucesso(self, mock_print, mock_controlador):
        """
        Testa se `exibir_resultados` funciona corretamente ao processar entradas válidas.
        """
        mock_instance = mock_controlador.return_value
        mock_instance.processar_e_gerar_json.return_value = json.dumps(
            [{"status": "pasta", "conteudo": [{"nome": "file.txt", "extensao": ".txt"}]}]
        )

        exibir_resultados(["/test/path"], [".txt"])
        mock_controlador.assert_called_once()
        assert mock_print.called

    @patch('controllers.controle_caminhos.ControladorDeCaminhos')
    @patch('builtins.print')
    def test_exibir_resultados_erro_processamento(self, mock_print, mock_controlador):
        """
        Testa se `exibir_resultados` lida corretamente com erros durante o processamento.
        """
        mock_instance = mock_controlador.return_value
        mock_instance.processar_e_gerar_json.side_effect = ValueError("Erro teste")

        exibir_resultados(["/test/path"])
        mock_print.assert_called_with("Erro ao processar caminhos: Erro teste")
