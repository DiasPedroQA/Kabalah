# src/main.py
# pylint: disable=C

import sys
import os
from views.visual_caminho import exibir_resultados


def obter_caminhos_e_extensoes() -> tuple:
    """Retorna os caminhos e as extensões de filtro como uma tupla."""
    caminhos = [
        "/home/pedro-pm-dias/Downloads/",
        # "/home/pedro-pm-dias/Downloads/Chrome/",
        # "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
        "/home/pedro-pm-dias/Downloads/InvalidPath",
    ]
    filtro_extensoes = [".html", ".txt"]
    return caminhos, filtro_extensoes


def main():
    # Garantir que o diretório raiz esteja no sys.path
    if os.path.abspath(os.path.dirname(__file__)) not in sys.path:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # Obter caminhos e extensões
    caminhos, filtro_extensoes = obter_caminhos_e_extensoes()

    # Exibir mensagem inicial
    print("Iniciando a análise dos caminhos fornecidos...\n")

    # Exibir os resultados usando a função definida em 'views'
    exibir_resultados(caminhos, filtro_extensoes)


if __name__ == "__main__":
    main()
