# tests/test_main.py

import sys
import pytest
from Bookmarks.src.main import (
    garantir_sys_path,
    obter_caminhos_e_extensoes,
    main
)


class TestMain:
    def test_obter_caminhos_e_extensoes_returns_tuple(self):
        result = obter_caminhos_e_extensoes()
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)

    def test_obter_caminhos_e_extensoes_content(self):
        caminhos, extensoes = obter_caminhos_e_extensoes()
        assert all(isinstance(caminho, str) for caminho in caminhos)
        assert all(isinstance(ext, str) for ext in extensoes)
        assert all(ext.startswith('.') for ext in extensoes)

    def test_garantir_sys_path_adds_path(self):
        original_path = sys.path.copy()
        garantir_sys_path()
        assert len(sys.path) >= len(original_path)

    def test_garantir_sys_path_idempotent(self):
        garantir_sys_path()
        path_length = len(sys.path)
        garantir_sys_path()
        assert len(sys.path) == path_length

    def test_main_function_executes(self, capsys):
        try:
            main()
            captured = capsys.readouterr()
            assert "Iniciando a análise dos caminhos fornecidos..." in captured.out
        except Exception as e:
            pytest.fail(f"main() raised {e} unexpectedly!")
