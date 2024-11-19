# tests/views/test_visual_caminho.py
# pylint: disable=C0413, E0401, E0611

"""
Módulo de testes para funções de visualização de caminhos.

Este módulo contém uma série de testes automatizados para funções presentes no módulo 
`visual_caminho`. Os testes garantem o correto funcionamento de funcionalidades como:
- Validação das entradas para caminhos e extensões.
- Filtragem de arquivos por extensão.
- Exibição de resultados com tratamento de erros de permissões ou caminhos inexistentes.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.views.visual_caminho import (
    exibir_resultados,
    filtrar_por_extensao,
    validar_entradas,
)


class TestVisualCaminho:
    """
    Classe de testes para funções de visualização de caminhos.

    Contém testes para as funções de validação, filtragem e exibição de resultados de caminhos.
    """

    def test_validar_entradas_caminhos_invalidos(self):
        """
        Testa a validação das entradas para caminhos inválidos.

        Verifica se a função `validar_entradas` retorna o erro
        adequado quando os caminhos fornecidos
        não são do tipo lista de strings.
        """
        caminhos = [123, "path/to/file", True]
        extensoes = [".txt", ".py"]
        resultado = validar_entradas(caminhos, extensoes)
        assert resultado == "'caminhos' deve ser uma lista de strings."

    def test_validar_entradas_extensoes_invalidas(self):
        """
        Testa a validação das entradas para extensões inválidas.

        Verifica se a função `validar_entradas` retorna o erro
        adequado quando as extensões fornecidas
        não são do tipo lista de strings.
        """
        caminhos = ["path/to/file"]
        extensoes = [".txt", 123, True]
        resultado = validar_entradas(caminhos, extensoes)
        assert resultado == "'extensoes' deve ser uma lista de strings."

    def test_validar_entradas_validas(self):
        """
        Testa a validação de entradas válidas para caminhos e extensões.

        Verifica se a função `validar_entradas` não retorna erros
        quando as entradas estão corretamente
        formatadas.
        """
        caminhos = ["path/to/file1", "path/to/file2"]
        extensoes = [".txt", ".py"]
        resultado = validar_entradas(caminhos, extensoes)
        assert resultado is None

    def test_filtrar_por_extensao_com_filtro(self):
        """
        Testa a filtragem de arquivos por extensões quando existe um filtro.

        Verifica se a função `filtrar_por_extensao` retorna
        corretamente apenas os arquivos que possuem
        as extensões fornecidas no filtro.
        """
        arquivos = [
            {"nome": "arquivo1.txt", "extensao": ".txt"},
            {"nome": "arquivo2.py", "extensao": ".py"},
            {"nome": "arquivo3.jpg", "extensao": ".jpg"},
        ]
        extensoes = [".txt", ".py"]
        resultado = filtrar_por_extensao(arquivos, extensoes)
        assert len(resultado) == 2
        assert all(arquivo["extensao"] in extensoes for arquivo in resultado)

    def test_filtrar_por_extensao_sem_filtro(self):
        """
        Testa a filtragem de arquivos quando não há filtro de extensões.

        Verifica se a função `filtrar_por_extensao` retorna
        todos os arquivos quando o filtro é `None`.
        """
        arquivos = [
            {"nome": "arquivo1.txt", "extensao": ".txt"},
            {"nome": "arquivo2.py", "extensao": ".py"},
        ]
        resultado = filtrar_por_extensao(arquivos, None)
        assert len(resultado) == 2
        assert resultado == arquivos

    def test_exibir_resultados_erro_permissao(self, capsys):
        """
        Testa a exibição de resultados quando ocorre erro de permissão.

        Verifica se a função `exibir_resultados` captura o erro
        quando um caminho sem permissão é processado.
        """
        caminhos = ["/path/sem/permissao"]
        exibir_resultados(caminhos)
        captured = capsys.readouterr()
        assert "Erro ao processar caminhos" in captured.out

    def test_exibir_resultados_caminho_inexistente(self, capsys):
        """
        Testa a exibição de resultados quando o caminho não existe.

        Verifica se a função `exibir_resultados` captura o erro
        quando um caminho inexistente é processado.
        """
        caminhos = ["/caminho/que/nao/existe"]
        exibir_resultados(caminhos)
        captured = capsys.readouterr()
        assert "Erro ao processar caminhos" in captured.out

    def test_exibir_resultados_json_invalido(self, capsys, mocker):
        """
        Testa a exibição de resultados quando o formato do JSON gerado é inválido.

        Verifica se a função `exibir_resultados` captura o erro
        quando o controlador retorna um JSON inválido.
        """
        caminhos = ["path/valido"]
        mock_controlador = mocker.patch(
            "src.controllers.controle_caminhos.ControladorDeCaminhos"
        )
        mock_controlador.return_value.processar_caminhos.return_value = "json invalido"
        exibir_resultados(caminhos)
        captured = capsys.readouterr()
        assert "Erro ao processar caminhos" in captured.out
