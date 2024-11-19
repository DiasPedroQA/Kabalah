# tests/controllers/test_controle_caminhos.py
# pylint: disable=C0413

"""
Módulo de testes para a classe ControladorDeCaminhos.

Este módulo contém uma série de testes automatizados para a classe 
ControladorDeCaminhos, responsável por processar caminhos de arquivos e diretórios.
Os testes abrangem funcionalidades como:

- Processamento de listas vazias de caminhos.
- Filtragem de caminhos por extensões de arquivos, incluindo suporte para múltiplos filtros.
- Geração de relatórios em formato JSON.
- Tratamento de erros, como arquivos inexistentes.
- Sensibilidade a maiúsculas e minúsculas na filtragem de extensões.
- Processamento de caminhos relativos e múltiplos diretórios.

Os testes visam garantir o correto funcionamento do controlador sob diferentes cenários.
"""


import os
import sys
import json
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.controllers.controle_caminhos import ControladorDeCaminhos


class TestControladorDeCaminhos:
    """
    Conjunto de testes para a classe ControladorDeCaminhos, que gerencia e processa
    listas de caminhos de arquivos e diretórios, com foco na filtragem de extensões
    e geração de relatórios em formato JSON.
    """

    def test_processar_caminhos_vazios(self):
        """
        Testa o processamento de uma lista vazia de caminhos.
        O controlador deve retornar uma lista vazia quando nenhum caminho é fornecido.
        """
        controlador = ControladorDeCaminhos([])
        resultado = controlador.processar_caminhos()
        assert isinstance(resultado, list)
        assert len(resultado) == 0

    def test_filtro_extensoes_sem_correspondencia(self):
        """
        Testa o filtro de extensões quando não há correspondência.
        O controlador deve retornar uma lista vazia de subitens filtrados.
        """
        controlador = ControladorDeCaminhos(["/tmp"], [".xyz"])
        resultado = controlador.processar_caminhos()
        assert resultado[0].get("subitens_filtrados", []) == []

    def test_multiplos_filtros_extensao(self):
        """
        Testa o filtro de múltiplas extensões.
        O controlador deve garantir que os subitens filtrados tenham uma das extensões fornecidas.
        """
        controlador = ControladorDeCaminhos(["/tmp"], [".txt", ".json", ".html"])
        resultado = controlador.processar_caminhos()
        for item in resultado[0].get("subitens_filtrados", []):
            assert any(item.endswith(ext) for ext in [".txt", ".json", ".html"])

    def test_processar_arquivo_inexistente(self):
        """
        Testa o comportamento ao tentar processar um arquivo inexistente.
        O controlador deve lançar um erro FileNotFoundError.
        """
        with pytest.raises(FileNotFoundError):
            controlador = ControladorDeCaminhos(["/caminho/inexistente/arquivo.txt"])
            controlador.processar_caminhos()

    def test_relatorio_json_formatacao(self):
        """
        Testa a formatação do relatório gerado em JSON.
        O controlador deve retornar um string formatada corretamente,
        que pode ser analisada como uma lista.
        """
        controlador = ControladorDeCaminhos(["/tmp"])
        relatorio = controlador.gerar_relatorio_json()
        assert isinstance(relatorio, str)
        parsed = json.loads(relatorio)
        assert isinstance(parsed, list)

    def test_filtro_extensoes_case_sensitive(self):
        """
        Testa o filtro de extensões com diferenciação de maiúsculas e minúsculas.
        O controlador deve tratar a diferenciação de maiúsculas e minúsculas nas extensões.
        """
        controlador = ControladorDeCaminhos(["/tmp"], [".TXT", ".JSON"])
        resultado = controlador.processar_caminhos()
        subitens = resultado[0].get("subitens_filtrados", [])
        for item in subitens:
            assert not item.endswith(".txt")
            assert not item.endswith(".json")

    def test_caminhos_relativos(self):
        """
        Testa o processamento de caminhos relativos.
        O controlador deve identificar corretamente um diretório relativo e seus subitens.
        """
        controlador = ControladorDeCaminhos(["./"])
        resultado = controlador.processar_caminhos()
        assert resultado[0]["tipo"] == "diretório"
        assert "subitens" in resultado[0]

    def test_processamento_multiplos_diretorios(self):
        """
        Testa o processamento de múltiplos diretórios.
        O controlador deve ser capaz de processar mais de um diretório de uma vez.
        """
        controlador = ControladorDeCaminhos(["/tmp", "/var"])
        resultado = controlador.processar_caminhos()
        assert len(resultado) == 2
        assert all(item.get("tipo") == "diretório" for item in resultado)
