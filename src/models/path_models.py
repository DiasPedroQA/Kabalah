"""
Imports the os module, which provides a way to interact with the operating system.
"""
import os
from typing import List, Dict, Union


class AnaliseHtml:
    """
    Classe para análise de diretórios e busca de arquivos com extensão específica.

    Esta classe percorre recursivamente um diretório fornecido e retorna todos os arquivos
    que correspondem à extensão especificada, como .html.
    """

    def __init__(self, diretorio: str, extension: str = ".html") -> None:
        """
        Inicializa a classe AnaliseHtml com um diretório e uma extensão de arquivo.

        Args:
            diretorio (str): Caminho do diretório a ser analisado.
            extension (str): Extensão dos arquivos a serem buscados (padrão: .html).
        """
        self.pasta: str = diretorio
        self.extension: str = extension

    def listar_arquivos(self) -> Dict[str, Union[int, List[str]]]:
        """
        Lista recursivamente todos os arquivos com a extensão desejada no diretório.

        Retorna um dicionário contendo o total de arquivos encontrados e a lista de caminhos
        absolutos desses arquivos.

        Returns:
            dict: Contém o total de arquivos encontrados e a lista de caminhos absolutos.
                Exemplo de retorno:
                {
                    "total": 3,
                    "arquivos": [
                        "/home/pedro/Downloads/arquivo1.html",
                        "/home/pedro/Downloads/subpasta/arquivo2.html"
                    ]
                }
        """
        arquivos_encontrados: List[str] = []

        # Verifica se o caminho fornecido é um diretório válido
        if not os.path.isdir(self.pasta):
            raise ValueError(f"O caminho {self.pasta} não é um diretório válido.")

        # Percorre recursivamente o diretório
        for root, _, files in os.walk(self.pasta):
            arquivos_encontrados.extend(
                os.path.join(root, file) for file in files if file.endswith(self.extension)
            )

        # Se nenhum arquivo for encontrado, lança uma exceção
        if not arquivos_encontrados:
            raise FileNotFoundError(
                f"Nenhum arquivo com a extensão {self.extension},"
                f" foi encontrado em {self.pasta}."
            )

        return {"total": len(arquivos_encontrados), "arquivos": arquivos_encontrados}


if __name__ == "__main__":
    # Bloco principal do programa.
    # Realiza a análise de arquivos HTML no diretório especificado e exibe o resultado
    # com o total de arquivos encontrados e seus caminhos absolutos.
    try:
        # Caminho do diretório para análise
        pasta: str = "/home/pedro-pm-dias/Downloads/"

        # Instanciando a classe e realizando a análise
        analise = AnaliseHtml(diretorio=pasta)
        resultado: Dict[str, Union[int, List[str]]] = analise.listar_arquivos()

        # Exibe os resultados
        print(f"{resultado['total']} arquivos encontrados com a extensão .html:")
        arquivos: List[str] = resultado['arquivos']
        for arquivo in arquivos:
            print(arquivo)

        # Informações adicionais, como o tamanho do arquivo ou data de modificação,
        # poderiam ser incluídas
        # Exemplo de uso:
        for arquivo in arquivos:
            file_size = os.path.getsize(arquivo)
            print(f"Tamanho de {arquivo}: {file_size / 1024:.2f} KB")

    except ValueError as e:
        print(f"Erro de diretório: {e}")
    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except PermissionError as e:
        print(f"Erro de permissão: {e}")
