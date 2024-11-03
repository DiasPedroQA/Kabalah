# pylint: disable=C
# src/main.py

import os
from controllers.path_controller import inicializar_controller
from models.path_models import processar_pasta, processar_arquivo
from src.views.path_view import transformar_dados


def processar_caminhos(caminhos):
    resultados = []

    for caminho in caminhos:
        if os.path.isdir(caminho):
            dados = processar_pasta(caminho)
            resultado = transformar_dados(dados, "pasta")
            resultados.append(resultado)
        elif os.path.isfile(caminho):
            dados = processar_arquivo(caminho)
            resultado = transformar_dados(dados, "arquivo")
            resultados.append(resultado)
        else:
            resultados.append({"erro": f"Caminho inválido ou inexistente: {caminho}"})

    # Aqui você pode querer fazer algo com os resultados
    return resultados


def principal():
    # Caminhos fictícios para as pastas e arquivos
    folder_path1 = "/home/pedro-pm-dias/Downloads/folder1"
    folder_path2 = "/home/pedro-pm-dias/Downloads/folder2"
    file_path1 = "/home/pedro-pm-dias/Downloads/file1.txt"
    file_path2 = "/home/pedro-pm-dias/Downloads/file2.txt"

    # Processamento dos caminhos pelo controller
    caminhos = [folder_path1, folder_path2, file_path1, file_path2]
    resultados = processar_caminhos(caminhos)
    print(resultados)

    # Inicialização da API
    inicializar_controller()


if __name__ == "__main__":
    principal()
