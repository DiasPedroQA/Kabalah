# src/main.py

"""
Exemplo de uso das classes `FilePathModel` e `FolderPathModel`.

O `FilePathModel` representa um caminho de arquivo,
enquanto `FolderPathModel` representa um caminho de pasta.
Este exemplo demonstra como usar cada método importante em ambas as classes.
"""

from models.path_model import FilePathModel, FolderPathModel


def show_path_info(model, type_name):
    """Função auxiliar para imprimir informações sobre um caminho."""
    print(f"\n### Informações do objeto {type_name} ###\n")
    print("Caminho:", model.path)
    print("É um caminho absoluto?", model.is_path_absolute())
    print("É um arquivo?", model.is_path_file())
    print("É uma pasta?", model.is_path_folder())


def main(caminho_arquivo: str, caminho_pasta: str):
    """
    Função principal que demonstra o uso das classes `FilePathModel` e `FolderPathModel`.
    """

    # Exemplo 1: Utilizando FilePathModel para representar e manipular um caminho de arquivo
    file_model = FilePathModel(caminho_arquivo)

    show_path_info(file_model, "Arquivo")
    print("Extensão do arquivo:", file_model.get_extension())
    # print("Representação JSON do objeto de arquivo:", file_model.to_obj_json())

    # Exemplo 2: Utilizando FolderPathModel para representar e manipular um caminho de pasta
    folder_model = FolderPathModel(caminho_pasta)

    show_path_info(folder_model, "Pasta")

    print("\nConteúdo da pasta:", caminho_pasta)
    conteudo_pasta = folder_model.list_contents(depth=1)

    for item in conteudo_pasta:
        print(
            f"- {item.path} (Tipo: {'Arquivo' if isinstance(item, FilePathModel) else 'Pasta'})"
        )
        print(f"    - Item inteiro: {item.to_obj_json()}\n\n")

    # print("\nRepresentação JSON do objeto de pasta:", folder_model.to_obj_json())


if __name__ == "__main__":
    file_path: str = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html"
    folder_path: str = "/home/pedro-pm-dias/Downloads/"

    main(caminho_arquivo=file_path, caminho_pasta=folder_path)
