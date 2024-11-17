# src/models/modelo_caminhos.py

"""
O código define classes para representar caminhos, arquivos e pastas, com métodos
para obter informações e interagir com eles.
"""

from pathlib import Path
from typing import List, Optional, Union


class Caminho:
    """
    A classe `Caminho` fornece métodos para manipular caminhos de arquivos,
    incluindo verificar a existência, obter o nome, determinar o tipo
    (diretório ou arquivo) e converter informações do caminho para um dicionário.
    """

    def __init__(self, caminho: Union[str, Path]):
        """
        Inicializa o objeto com um atributo de caminho, aceitando uma string
        ou um objeto `Path`.

        :param caminho: Caminho em formato de string ou objeto `Path`.
        """
        self.path = Path(caminho)

    @property
    def existe(self) -> bool:
        """
        Verifica se o caminho especificado existe.

        :return: Verdadeiro se o caminho existe, caso contrário, Falso.
        """
        return self.path.exists()

    @property
    def nome(self) -> str:
        """
        Retorna o nome do caminho.

        :return: Nome do caminho.
        """
        return self.path.name

    @property
    def tipo(self) -> str:
        """
        Determina se o caminho é um diretório, um arquivo ou inválido.

        :return: "pasta" se for um diretório, "arquivo" se for um arquivo,
                 ou "inválido" caso contrário.
        """
        if self.is_diretorio():
            return "pasta"
        if self.is_arquivo():
            return "arquivo"
        return "inválido"

    def is_diretorio(self) -> bool:
        """
        Verifica se o caminho é um diretório.

        :return: Verdadeiro se for um diretório, caso contrário, Falso.
        """
        return self.path.is_dir()

    def is_arquivo(self) -> bool:
        """
        Verifica se o caminho é um arquivo.

        :return: Verdadeiro se for um arquivo, caso contrário, Falso.
        """
        return self.path.is_file()

    def para_dict(self) -> dict:
        """
        Converte informações do caminho para um dicionário.

        :return: Dicionário com informações do caminho.
        """
        return {
            "nome": self.nome,
            "caminho": str(self.path),
            "existe": self.existe,
            "tipo": self.tipo,
        }


class Arquivo(Caminho):
    """
    Representa um arquivo no sistema de arquivos, estendendo a classe `Caminho`.
    """

    def __init__(self, caminho: Union[str, Path]):
        """
        Inicializa um objeto para representar um arquivo. Levanta um erro
        se o caminho não for um arquivo.

        :param caminho: Caminho do arquivo.
        :raises ValueError: Se o caminho não for um arquivo.
        """
        super().__init__(caminho)
        if not self.is_arquivo():
            raise ValueError(f"O caminho {self.path} não é um arquivo.")

    @property
    def extensao(self) -> str:
        """
        Retorna a extensão do arquivo.

        :return: Extensão do arquivo.
        """
        return self.path.suffix

    @property
    def tamanho(self) -> int:
        """
        Retorna o tamanho do arquivo em bytes.

        :return: Tamanho do arquivo em bytes.
        """
        return self.path.stat().st_size

    def tamanho_formatado(self) -> str:
        """
        Retorna o tamanho do arquivo formatado em kB.

        :return: Tamanho formatado como string.
        """
        return f"{self.tamanho / 1024:.2f} kB"

    def para_dict(self) -> dict:
        """
        Adiciona informações adicionais (extensão e tamanho) ao dicionário
        de informações do arquivo.

        :return: Dicionário com informações do arquivo.
        """
        dados = super().para_dict()
        dados.update(
            {
                "extensao": self.extensao,
                "tamanho": self.tamanho_formatado(),
            }
        )
        return dados


class Pasta(Caminho):
    """
    Representa uma pasta no sistema de arquivos, estendendo a classe `Caminho`.
    """

    def __init__(self, caminho: Union[str, Path]):
        """
        Inicializa um objeto para representar uma pasta. Levanta um erro
        se o caminho não for um diretório.

        :param caminho: Caminho do diretório.
        :raises ValueError: Se o caminho não for um diretório.
        """
        super().__init__(caminho)
        if not self.is_diretorio():
            raise ValueError(f"O caminho {self.path} não é uma pasta.")

    @property
    def subitens(self) -> List[Caminho]:
        """
        Lista os subitens (arquivos e diretórios) dentro da pasta.

        :return: Lista de objetos `Caminho` representando os subitens.
        """
        itens = []
        try:
            for item in self.path.iterdir():
                if item.is_file():
                    itens.append(Arquivo(item))
                elif item.is_dir():
                    itens.append(Pasta(item))
        except PermissionError:
            itens.append(Caminho(f"Inacessível: {self.path}"))
        return itens

    def listar_arquivos(self, extensoes: Optional[List[str]] = None) -> List[Arquivo]:
        """
        Lista arquivos na pasta, filtrando por extensões se especificadas.

        :param extensoes: Lista de extensões para filtrar os arquivos.
        :return: Lista de objetos `Arquivo`.
        """
        arquivos = []
        try:
            arquivos = [Arquivo(f) for f in self.path.iterdir() if f.is_file()]
            if extensoes:
                arquivos = [arq for arq in arquivos if arq.extensao in extensoes]
        except PermissionError:
            pass
        return arquivos

    def para_dict(self) -> dict:
        """
        Adiciona informações dos subitens ao dicionário da pasta.

        :return: Dicionário com informações da pasta.
        """
        dados = super().para_dict()
        dados.update({"subitens": [item.para_dict() for item in self.subitens]})
        return dados
