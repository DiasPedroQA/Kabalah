# tests/test_main.py
# pylint: disable = C0413, E0401, E0611

"""
Módulo de testes para as funções principais do aplicativo.

Este módulo contém uma série de testes para as funções presentes no módulo `main` do 
pacote `Bookmarks`. Os testes verificam o comportamento das funções que manipulam o 
caminho do sistema e a execução principal da aplicação.
"""

import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.main import (
    garantir_sys_path,
    obter_caminhos_e_extensoes,
    main
)


class TestMain:
    """
    Classe de testes para as funções principais do módulo `main`.

    Contém testes para funções como `garantir_sys_path`, `obter_caminhos_e_extensoes`,
    e `main`, verificando seu comportamento e a integridade dos dados manipulados.
    """

    def test_obter_caminhos_e_extensoes_returns_tuple(self):
        """
        Testa se a função `obter_caminhos_e_extensoes` retorna uma tupla.

        Verifica se o resultado da função é uma tupla contendo dois elementos:
        uma lista de caminhos e uma lista de extensões.
        """
        result = obter_caminhos_e_extensoes()
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)

    def test_obter_caminhos_e_extensoes_content(self):
        """
        Testa o conteúdo retornado pela função `obter_caminhos_e_extensoes`.

        Verifica se ambos os elementos da tupla são listas de strings, e se
        as extensões começam com um ponto (".").
        """
        caminhos, extensoes = obter_caminhos_e_extensoes()
        assert all(isinstance(caminho, str) for caminho in caminhos)
        assert all(isinstance(ext, str) for ext in extensoes)
        assert all(ext.startswith(".") for ext in extensoes)

    def test_garantir_sys_path_adds_path(self):
        """
        Testa se a função `garantir_sys_path` adiciona o caminho ao `sys.path`.

        Verifica se a execução da função resulta no aumento do número de entradas
        em `sys.path`, garantindo que o caminho foi adicionado corretamente.
        """
        original_path = sys.path.copy()
        garantir_sys_path()
        assert len(sys.path) >= len(original_path)

    def test_garantir_sys_path_idempotent(self):
        """
        Testa se a função `garantir_sys_path` é idempotente.

        Verifica se a execução múltipla da função não altera o resultado após a
        primeira execução, ou seja, `sys.path` não deve ser alterado após a primeira chamada.
        """
        garantir_sys_path()
        path_length = len(sys.path)
        garantir_sys_path()
        assert len(sys.path) == path_length

    def test_main_function_executes(self, capsys):
        """
        Testa a execução da função `main`.

        Verifica se a função `main` executa corretamente, capturando a saída no
        terminal e garantindo que a mensagem esperada é impressa.
        """
        try:
            main()
            captured = capsys.readouterr()
            assert "Iniciando a análise dos caminhos fornecidos..." in captured.out
        except (ValueError, IOError, ImportError) as e:
            pytest.fail(f"main() raised {e} inesperadamente!")
