# src/models/path_models.py

"""
Módulo para análise de diretórios e busca de arquivos com uma extensão específica.

Este módulo contém a classe `AnaliseHtml`, que permite percorrer recursivamente um diretório
e localizar arquivos com uma extensão especificada (por padrão, .html). A classe oferece métodos
para listar os arquivos encontrados, contar a quantidade de arquivos, exibir os caminhos absolutos
dos arquivos e obter informações adicionais sobre eles, como o tamanho.

A classe lança exceções apropriadas caso o diretório não seja válido ou se não houver arquivos
encontrados com a extensão especificada.

Exemplo de uso:
    analise = AnaliseHtml(diretorio="/caminho/do/diretorio")
    resultado = analise.listar_arquivos()
    print(f"{resultado['total']} arquivos encontrados.")
"""

from pathlib import Path
from typing import List, Dict, Union


class AnaliseHtml:
    """
    Classe para análise de diretórios e busca de arquivos com uma extensão específica.
    """

    def __init__(self, diretorio: str, extensao: str = ".html") -> None:
        """
        Inicializa a análise HTML com o diretório e a extensão dos arquivos a serem buscados.

        Args:
            diretorio (str): Caminho do diretório.
            extensao (str): Extensão dos arquivos a serem buscados (padrão: .html).
        """
        self.diretorio = Path(diretorio)
        self.extensao = extensao

    def _listar_arquivos(self) -> List[str]:
        """
        Retorna a lista de arquivos com a extensão especificada no diretório.

        Raises:
            ValueError: Se o diretório não for válido.
            FileNotFoundError: Se não forem encontrados arquivos com a extensão desejada.

        Returns:
            List[str]: Caminhos dos arquivos encontrados.
        """
        if not self.diretorio.is_dir():
            raise ValueError(f"{self.diretorio} não é um diretório válido.")

        arquivos_encontrados = [
            str(arquivo) for arquivo in self.diretorio.rglob(f"*{self.extensao}")
        ]

        if not arquivos_encontrados:
            raise FileNotFoundError(
                f"Nenhum arquivo com a extensão {self.extensao} foi encontrado em {self.diretorio}."
            )

        return arquivos_encontrados

    def listar_arquivos(self) -> Dict[str, Union[int, List[str]]]:
        """
        Retorna o total de arquivos e os caminhos absolutos.

        Returns:
            dict: Contém o total de arquivos e a lista de caminhos.
        """
        arquivos_encontrados = self._listar_arquivos()
        return {"total": len(arquivos_encontrados), "arquivos": arquivos_encontrados}

    def contar_arquivos(self) -> int:
        """
        Retorna o número de arquivos encontrados.

        Returns:
            int: Número de arquivos.
        """
        arquivos = self.listar_arquivos()
        return arquivos["total"]

    def exibir_arquivos(self) -> None:
        """
        Exibe os arquivos encontrados no diretório.
        """
        arquivos = self.listar_arquivos()
        print("Arquivos encontrados:")
        for item in arquivos["arquivos"]:
            print(item)

    def obter_caminhos_absolutos(self) -> List[str]:
        """
        Retorna os caminhos absolutos dos arquivos encontrados.

        Returns:
            List[str]: Caminhos absolutos dos arquivos.
        """
        arquivos = self.listar_arquivos()
        return arquivos["arquivos"]


if __name__ == "__main__":
    # Realiza a análise de arquivos HTML no diretório especificado e exibe os resultados.
    try:
        pasta: str = "/home/pedro-pm-dias/Downloads/"  # Caminho do diretório a ser analisado

        # Instanciando a classe e realizando a análise
        analise = AnaliseHtml(diretorio=pasta)
        resultado = analise.listar_arquivos()

        # Exibe os resultados
        print(f"{resultado['total']} arquivos encontrados com a extensão .html:")
        for arquivo in resultado["arquivos"]:
            print(arquivo)

        # Exibe o tamanho dos arquivos
        for arquivo in resultado["arquivos"]:
            file_size = Path(arquivo).stat().st_size
            print(f"Tamanho de {arquivo}: {file_size / 1024:.2f} KB")

    except (ValueError, FileNotFoundError, PermissionError) as e:
        print(f"Erro: {e}")
