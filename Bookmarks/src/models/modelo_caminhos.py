# Bookmarks/src/models/modelo_caminhos.py

"""
Este módulo contém classes para análise e manipulação de caminhos no sistema de arquivos.

Classes:
    - Arquivo: Representa um arquivo e fornece informações estruturadas sobre ele.
    - Pasta: Representa uma pasta e fornece informações estruturadas, incluindo subitens.
    - PathFinder: Processa e analisa caminhos fornecidos, identificando arquivos e pastas,
      e fornecendo estatísticas detalhadas como tamanho, data de criação e última modificação.

Funcionalidades:
    - Análise de caminhos válidos e inválidos.
    - Correção de caminhos relativos usando regex.
    - Geração de informações detalhadas em formato JSON.

Exemplo de uso:
    ```
    caminhos = ["../Downloads/arquivo.txt", "/caminho/invalido"]
    path_finder = PathFinder(caminhos)
    resultado = path_finder.analisar_caminhos_com_regex()
    print(resultado)
    ```
"""

import re
from typing import List, Union
import json
from pathlib import Path
from datetime import datetime


class Arquivo:
    """
    Representa um arquivo no sistema de arquivos, fornecendo informações
    estruturais e estatísticas relacionadas a ele.

    Atributos:
        _caminho (Path): Caminho completo para o arquivo.
        _estrutura (dict): Informações sobre a estrutura do arquivo, incluindo:
            - "nome_arquivo": Nome do arquivo.
            - "pastaMae": Caminho do diretório pai do arquivo.
        _estatisticas (dict): Estatísticas do arquivo, incluindo tamanho, data de criação
                             e última modificação.
    """

    def __init__(self, caminho: Path, estatisticas: dict):
        """
        Inicializa um objeto `Arquivo` com o caminho e as estatísticas fornecidos.

        Args:
            caminho (Path): O caminho completo para o arquivo.
            estatisticas (dict): Dicionário contendo informações estatísticas do arquivo,
                                 como tamanho, data de criação e última modificação.
        """
        self._caminho = caminho
        self._estrutura = {
            "nome_arquivo": self._caminho.name,
            "pastaMae": str(self._caminho.parent),
        }
        self._estatisticas = estatisticas

    def to_dict(self) -> dict:
        """
        Converte as informações do objeto `Arquivo` para um dicionário.

        Returns:
            dict: Um dicionário contendo:
                - "natureza": Tipo do objeto ("ARQUIVO").
                - "infos": Sub-dicionário com:
                    - "estrutura": Informações estruturais do arquivo (nome, pasta mãe).
                    - "estatisticas": Informações estatísticas do arquivo (tamanho,
                                      data de criação, última modificação).
        """
        return {
            "natureza": "ARQUIVO",
            "infos": {
                "estrutura": self._estrutura,
                "estatisticas": self._estatisticas,
            },
        }


class Pasta:
    """
    Representa uma pasta no sistema de arquivos, fornecendo informações
    estruturais, estatísticas e uma lista dos subitens contidos nela.

    Atributos:
        _caminho (Path): Caminho completo para a pasta.
        _estrutura (dict): Informações sobre a estrutura da pasta, incluindo:
            - "nome_pasta": Nome da pasta.
            - "pastaMae": Caminho do diretório pai da pasta.
        _estatisticas (dict): Estatísticas da pasta, como tamanho, data de criação
                              e última modificação.
        _subitens (list): Lista dos nomes dos arquivos e pastas contidos na pasta.
    """

    def __init__(self, caminho: Path, estatisticas: dict):
        """
        Inicializa um objeto `Pasta` com o caminho e as estatísticas fornecidos.

        Args:
            caminho (Path): O caminho completo para a pasta.
            estatisticas (dict): Dicionário contendo informações estatísticas da pasta,
                                 como tamanho, data de criação e última modificação.
        """
        self._caminho = caminho
        self._estrutura = {
            "nome_pasta": self._caminho.name,
            "pastaMae": str(self._caminho.parent),
        }
        self._estatisticas = estatisticas
        self._subitens = [item.name for item in self._caminho.iterdir()]

    def to_dict(self) -> dict:
        """
        Converte as informações do objeto `Pasta` para um dicionário.

        Returns:
            dict: Um dicionário contendo:
                - "natureza": Tipo do objeto ("PASTA").
                - "infos": Sub-dicionário com:
                    - "estrutura": Informações estruturais da pasta (nome, pasta mãe).
                    - "estatisticas": Informações estatísticas da pasta (tamanho,
                                      data de criação, última modificação).
                    - "subitens": Lista dos nomes dos itens contidos na pasta.
        """
        return {
            "natureza": "PASTA",
            "infos": {
                "estrutura": self._estrutura,
                "estatisticas": self._estatisticas,
                "subitens": self._subitens,
            },
        }


class PathFinder:
    """
    Classe para analisar e obter informações sobre caminhos no sistema de arquivos.

    Essa classe processa arquivos e pastas, fornecendo informações detalhadas como
    estrutura, estatísticas e subitens, além de permitir a análise de caminhos com
    suporte a regex para caminhos relativos.
    """

    def __init__(self, entrada_dados: Union[str, List[str]]):
        """
        Inicializa a classe com os caminhos de entrada fornecidos.

        Args:
            entrada_dados (Union[str, List[str]]): Caminhos a serem analisados. Pode ser uma string
                                                  (caminho único) ou uma lista de strings.
        """
        self._caminhos_entrada = (
            [entrada_dados] if isinstance(entrada_dados, str) else entrada_dados
        )

    def formatar_tamanho(self, tamanho_bytes: int) -> dict:
        """
        Formata o tamanho de um arquivo ou pasta em kilobytes.

        Args:
            tamanho_bytes (int): Tamanho em bytes.

        Returns:
            dict: Dicionário contendo o tamanho em kilobytes.
        """
        return {"tamanho_em_kB": round(tamanho_bytes / 1024, 2)}

    def formatar_data_brasileiro(self, timestamp: float) -> str:
        """
        Converte um timestamp para o formato de data e hora brasileiro.

        Args:
            timestamp (float): Timestamp em segundos desde a época Unix.

        Returns:
            str: Data e hora no formato "dd/mm/aaaa hh:mm:ss".
        """
        return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")

    def analisar_caminhos(self) -> str:
        """
        Analisa os caminhos fornecidos e retorna suas informações em formato JSON.

        Returns:
            str: JSON contendo os resultados da análise dos caminhos.
        """
        resultado_analise = [
            {"caminhoEntrada": caminho, "statusAnalise": self._analisar_status(caminho)}
            for caminho in self._caminhos_entrada
        ]
        return json.dumps(resultado_analise, indent=4, ensure_ascii=False)

    def analisar_caminhos_com_regex(self) -> str:
        """
        Analisa caminhos que possivelmente começam com '../', corrigindo automaticamente
        até encontrar um caminho válido ou atingir o limite de tentativas.

        Returns:
            str: JSON contendo os resultados da análise dos caminhos corrigidos.
        """
        regex = re.compile(r"^\.\./")
        resultado_analise = []

        for caminho in self._caminhos_entrada:
            caminho_obj = Path(caminho)
            tentativas = 0
            while regex.match(caminho) and tentativas < 10:
                if not caminho_obj.exists():
                    tentativas += 1
                    caminho = "../" + caminho
                    caminho_obj = Path(caminho)
                else:
                    break
            resultado_analise.append(
                {
                    "caminhoEntrada": caminho,
                    "statusAnalise": self._analisar_status(caminho),
                }
            )

        return json.dumps(resultado_analise, indent=4, ensure_ascii=False)

    def _analisar_status(self, caminho: str) -> dict:
        """
        Analisa o status de um caminho, determinando se é um arquivo, pasta ou inválido.

        Args:
            caminho (str): Caminho a ser analisado.

        Returns:
            dict: Dicionário contendo informações detalhadas sobre o status do caminho.
        """
        caminho_obj = Path(caminho)
        if not caminho_obj.exists():
            return {"tipo": "erro", "mensagem": "Caminho não encontrado"}

        estatisticas = self._obter_estatisticas(caminho_obj)
        if caminho_obj.is_file():
            return Arquivo(caminho_obj, estatisticas).to_dict()
        elif caminho_obj.is_dir():
            return Pasta(caminho_obj, estatisticas).to_dict()

        return {"tipo": "erro", "mensagem": "Status desconhecido"}

    def _obter_estatisticas(self, caminho_obj: Path) -> dict:
        """
        Obtém as estatísticas de um arquivo ou pasta, como tamanho, data de criação
        e última modificação.

        Args:
            caminho_obj (Path): Objeto `Path` representando o caminho a ser analisado.

        Returns:
            dict: Dicionário contendo as estatísticas formatadas do caminho.
        """
        estatisticas = caminho_obj.stat()
        return {
            "tamanho": self.formatar_tamanho(estatisticas.st_size),
            "dataCriacao": self.formatar_data_brasileiro(estatisticas.st_ctime),
            "ultimaModificacao": self.formatar_data_brasileiro(estatisticas.st_mtime),
        }
