# pylint: disable=C
# tests/models/test_modelo_caminhos.py

import json
import os
import tempfile
from pathlib import Path
from src.models.modelo_caminhos import CaminhoBase


class TestCaminhoBaseEdgeCases:
    def test_caminho_com_caracteres_especiais(self):
        caminho = CaminhoBase("test/path/with/@#$%^&*()")
        resultado = json.loads(caminho.obter_informacoes())
        assert "infos" in resultado
        assert "erro" in resultado["infos"]

    def test_caminho_muito_longo(self):
        caminho_longo = "/".join(["a" * 10 for _ in range(50)])
        caminho = CaminhoBase(caminho_longo)
        resultado = json.loads(caminho.obter_informacoes())
        assert "infos" in resultado

    def test_caminho_vazio(self):
        caminho = CaminhoBase("")
        resultado = json.loads(caminho.obter_informacoes())
        assert "infos" in resultado
        assert "erro" in resultado["infos"]

    def test_caminho_com_espacos(self):
        caminho = CaminhoBase("  test/path with spaces  ")
        resultado = json.loads(caminho.obter_informacoes())
        assert "infos" in resultado

    def test_multiplos_traversal_attempts(self):
        caminho = CaminhoBase("../../../etc/passwd")
        resultado = json.loads(caminho.obter_informacoes())
        assert "infos" in resultado
        assert "erro" in resultado["infos"]

    def test_uso_context_manager(self):
        with CaminhoBase(".") as caminho:
            resultado = json.loads(caminho.obter_informacoes())
            assert "infos" in resultado
            assert resultado["infos"]["tipo"] == "diretório"

    def test_diretorio_com_arquivos_ocultos(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            Path(temp_dir, ".hidden_file").touch()
            caminho = CaminhoBase(temp_dir)
            resultado = json.loads(caminho.obter_informacoes())
            assert "subitens" in resultado["infos"]
            assert any(".hidden_file" in item for item in resultado["infos"]["subitens"])

    def test_arquivo_zero_bytes(self):
        with tempfile.NamedTemporaryFile() as temp_file:
            caminho = CaminhoBase(temp_file.name)
            resultado = json.loads(caminho.obter_informacoes())
            assert resultado["infos"]["estatisticas"]["tamanho_em_kB"] == 0.0

    def test_diretorio_vazio(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = CaminhoBase(temp_dir)
            resultado = json.loads(caminho.obter_informacoes())
            assert "subitens" in resultado["infos"]
            assert len(resultado["infos"]["subitens"]) == 0

    def test_caminho_com_symlink(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            original = Path(temp_dir, "original")
            original.touch()
            link = Path(temp_dir, "link")
            os.symlink(original, link)
            caminho = CaminhoBase(str(link))
            resultado = json.loads(caminho.obter_informacoes())
            assert "infos" in resultado
            assert resultado["infos"]["tipo"] == "arquivo"
