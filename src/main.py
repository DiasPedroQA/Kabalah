# src/main.py

"""
Módulo principal para executar o Gerenciador de Caminhos.

Este script inicializa e utiliza a classe GerenciadorCaminhos para verificar e
exibir informações sobre um caminho especificado pelo usuário. A aplicação é capaz de:
    - Identificar o tipo do caminho (arquivo ou pasta).
    - Listar todos os arquivos presentes em um diretório.
    - Filtrar e exibir arquivos com extensão `.html`.

Caso nenhum caminho seja fornecido como argumento ao rodar o script, ele utiliza um
caminho padrão.

Exemplo de uso:
    python src/main.py /caminho/para/diretorio_ou_arquivo

Dependências:
    - controllers.GerenciadorCaminhos: Classe que gerencia operações sobre o caminho.
    - sys, typing.List

Exceções:
    - IOError: Levantada em caso de problemas de I/O com o sistema de arquivos.
    - OSError: Levantada em caso de erro do sistema ao acessar o caminho.
    - ValueError: Levantada para indicar um caminho inválido.
"""

import sys
from controllers import GerenciadorCaminhos


def main(caminho: str) -> None:
    """Função principal para executar o gerenciamento de caminhos.

    Argumentos:
        caminho (str): O caminho a ser gerenciado.
    """
    try:
        gerenciador = GerenciadorCaminhos(caminho)
        exibir_informacoes(gerenciador)
    except (IOError, OSError) as e:
        print(f"Erro de sistema ao acessar o caminho: {e}")
    except ValueError as ve:
        print(f"Erro: {ve}")


def exibir_informacoes(gerenciador: GerenciadorCaminhos) -> None:
    """Exibe informações sobre o caminho gerenciado.

    Argumentos:
        gerenciador (GerenciadorCaminhos): A instância do gerenciador de caminhos.
    """
    # Exibir tipo do caminho
    tipo = gerenciador.tipo_caminho()
    print(f"O caminho fornecido é um(a): {tipo}\n")

    if arquivos := gerenciador.listar_todos_os_arquivos():
        print("Arquivos encontrados:")
        for arquivo in arquivos:
            print(f"- {arquivo}")
    else:
        print("Nenhum arquivo encontrado na pasta.\n")

    if arquivos_html := gerenciador.filtrar_arquivos_html():
        print("\nArquivos .html encontrados:")
        for arquivo_html in arquivos_html:
            print(f"- {arquivo_html.file_path}")
    else:
        print("Nenhum arquivo .html encontrado.\n")


if __name__ == "__main__":
    # Verifica se um caminho foi passado como argumento ou usa um padrão
    caminho_usuario = sys.argv[1] if len(sys.argv) > 1 else "/home/pedro-pm-dias/Downloads/"
    main(caminho=caminho_usuario)

# file_path: str = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html"
# folder_path: str = "/home/pedro-pm-dias/Downloads/"
#
# def processar(caminho: str) -> None:
#     gerenciador_caminhos = GerenciadorCaminhos(caminho)
#     arquivos_html = gerenciador_caminhos.filtrar_arquivos_html()

#     for arquivo in arquivos_html:
#         dados = GerenciadorRaspagem.raspar_dados_html(arquivo)
#         nome_pdf = f"{os.path.splitext(os.path.basename(arquivo.file_path))[0]}.pdf"
#         GerenciadorEscritaPDF.criar_pdf(dados, nome_pdf)
#         print(f"Arquivo PDF criado: {nome_pdf}")
