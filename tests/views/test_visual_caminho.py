# pylint: disable=C, E

import unittest
import json
from unittest.mock import patch
from src.views.visual_caminho import validar_entradas, filtrar_por_extensao, exibir_resultados


class TestVisualCaminho(unittest.TestCase):
    def test_validar_entradas_caminhos_invalidos(self):
        resultado = validar_entradas("not_a_list", None)
        self.assertIsNotNone(resultado)
        self.assertIn("deve ser uma lista", resultado)

    def test_validar_entradas_caminhos_tipos_invalidos(self):
        resultado = validar_entradas(["/path/1", 2, "/path/3"], None)
        self.assertIsNotNone(resultado)
        self.assertIn("devem ser do tipo string", resultado)

    def test_validar_entradas_extensoes_invalidas(self):
        resultado = validar_entradas(["/path/1"], "not_a_list")
        self.assertIsNotNone(resultado)
        self.assertIn("deve ser uma lista", resultado)

    def test_validar_entradas_extensoes_tipos_invalidos(self):
        resultado = validar_entradas(["/path/1"], [".txt", 123])
        self.assertIsNotNone(resultado)
        self.assertIn("devem ser do tipo string", resultado)

    def test_validar_entradas_validas(self):
        resultado = validar_entradas(["/path/1", "/path/2"], [".txt", ".py"])
        self.assertIsNone(resultado)

    def test_filtrar_por_extensao_sem_filtro(self):
        arquivos = [
            {"nome": "file1.txt", "extensao": ".txt"},
            {"nome": "file2.py", "extensao": ".py"},
        ]
        resultado = filtrar_por_extensao(arquivos, None)
        self.assertEqual(resultado, arquivos)

    def test_filtrar_por_extensao_com_filtro(self):
        arquivos = [
            {"nome": "file1.txt", "extensao": ".txt"},
            {"nome": "file2.py", "extensao": ".py"},
            {"nome": "file3.jpg", "extensao": ".jpg"},
        ]
        resultado = filtrar_por_extensao(arquivos, [".txt", ".py"])
        self.assertEqual(len(resultado), 2)
        self.assertTrue(all(arq["extensao"] in [".txt", ".py"] for arq in resultado))

    @patch('controllers.controle_caminhos.ControladorDeCaminhos')
    @patch('builtins.print')
    def test_exibir_resultados_erro_validacao(self, mock_print, mock_controlador):
        exibir_resultados("caminho_invalido")
        mock_print.assert_called_with(
            "Erro: 'caminhos' deve ser uma lista de strings representando caminhos."
        )
        mock_controlador.assert_not_called()

    @patch('controllers.controle_caminhos.ControladorDeCaminhos')
    @patch('builtins.print')
    def test_exibir_resultados_sucesso(self, mock_print, mock_controlador):
        mock_instance = mock_controlador.return_value
        mock_instance.processar_e_gerar_json.return_value = json.dumps(
            [{"status": "pasta", "conteudo": [{"nome": "file.txt", "extensao": ".txt"}]}]
        )

        exibir_resultados(["/test/path"], [".txt"])
        mock_controlador.assert_called_once()
        self.assertTrue(mock_print.called)

    @patch('controllers.controle_caminhos.ControladorDeCaminhos')
    @patch('builtins.print')
    def test_exibir_resultados_erro_processamento(self, mock_print, mock_controlador):
        mock_instance = mock_controlador.return_value
        mock_instance.processar_e_gerar_json.side_effect = ValueError("Erro teste")

        exibir_resultados(["/test/path"])
        mock_print.assert_called_with("Erro ao processar caminhos: Erro teste")


if __name__ == '__main__':
    unittest.main()
