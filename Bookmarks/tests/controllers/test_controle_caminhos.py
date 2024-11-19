# tests/controllers/test_controle_caminhos.py

import json
import pytest
from Bookmarks.src.controllers.controle_caminhos import ControladorDeCaminhos


class TestControladorDeCaminhos:
    def test_processar_caminhos_vazios(self):
        controlador = ControladorDeCaminhos([])
        resultado = controlador.processar_caminhos()
        assert isinstance(resultado, list)
        assert len(resultado) == 0

    def test_filtro_extensoes_sem_correspondencia(self):
        controlador = ControladorDeCaminhos(["/tmp"], [".xyz"])
        resultado = controlador.processar_caminhos()
        assert resultado[0].get("subitens_filtrados", []) == []

    def test_multiplos_filtros_extensao(self):
        controlador = ControladorDeCaminhos(["/tmp"], [".txt", ".json", ".html"])
        resultado = controlador.processar_caminhos()
        for item in resultado[0].get("subitens_filtrados", []):
            assert any(item.endswith(ext) for ext in [".txt", ".json", ".html"])

    def test_processar_arquivo_inexistente(self):
        with pytest.raises(FileNotFoundError):
            controlador = ControladorDeCaminhos(["/caminho/inexistente/arquivo.txt"])
            controlador.processar_caminhos()

    def test_relatorio_json_formatacao(self):
        controlador = ControladorDeCaminhos(["/tmp"])
        relatorio = controlador.gerar_relatorio_json()
        assert isinstance(relatorio, str)
        parsed = json.loads(relatorio)
        assert isinstance(parsed, list)

    def test_filtro_extensoes_case_sensitive(self):
        controlador = ControladorDeCaminhos(["/tmp"], [".TXT", ".JSON"])
        resultado = controlador.processar_caminhos()
        subitens = resultado[0].get("subitens_filtrados", [])
        for item in subitens:
            assert not item.endswith(".txt")
            assert not item.endswith(".json")

    def test_caminhos_relativos(self):
        controlador = ControladorDeCaminhos(["./"])
        resultado = controlador.processar_caminhos()
        assert resultado[0]["tipo"] == "diretório"
        assert "subitens" in resultado[0]

    def test_processamento_multiplos_diretorios(self):
        controlador = ControladorDeCaminhos(["/tmp", "/var"])
        resultado = controlador.processar_caminhos()
        assert len(resultado) == 2
        assert all(item.get("tipo") == "diretório" for item in resultado)
