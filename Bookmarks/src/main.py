# src/main.py

"""
Provides the main entry point for the Bookmarks application.

This module sets up the necessary paths, retrieves the file paths and extensions to
filter, and calls the `exibir_resultados` function from the `visual_caminho` module
to display the analysis results.
"""

import sys
import os
from src.views.visual_caminho import exibir_resultados


def obter_caminhos_e_extensoes() -> tuple:
    """
    Retorna os caminhos e as extensões de filtro como uma tupla.

    Neste exemplo, os caminhos são definidos estaticamente. Pode-se adaptar
    para receber entradas via linha de comando ou arquivo de configuração.
    """
    caminhos = [
        "/home/pedro-pm-dias/Downloads/",
        "/home/pedro-pm-dias/Downloads/Chrome/",
    ]
    filtro_extensoes = [".html", ".txt"]  # Exemplo de filtro de extensões
    return caminhos, filtro_extensoes


def garantir_sys_path():
    """Garante que o diretório raiz esteja no sys.path para acesso a módulos."""
    if os.path.abspath(os.path.dirname(__file__)) not in sys.path:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def main():
    """
    Função principal para execução do programa. Realiza a validação de entradas,
    coleta os dados necessários e chama as funções da camada de visualização para
    exibir os resultados da análise.
    """
    # Garantir que o diretório raiz esteja no sys.path
    garantir_sys_path()

    # Obter caminhos e extensões para o filtro
    caminhos, filtro_extensoes = obter_caminhos_e_extensoes()

    # Exibir mensagem inicial
    print("Iniciando a análise dos caminhos fornecidos...\n")

    # Exibir os resultados usando a função definida em 'views'
    exibir_resultados(caminhos, filtro_extensoes)


if __name__ == "__main__":
    main()
