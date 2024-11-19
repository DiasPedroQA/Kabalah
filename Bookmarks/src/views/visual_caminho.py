# src/views/visual_caminho.py
# pylint: disable=E0401

"""
Valida os parâmetros de entrada para a função `exibir_resultados`.

Args:
    caminhos (List[str]): Uma lista de caminhos de arquivos para analisar.
    extensoes (Optional[List[str]]): Uma lista opcional de extensões
    de arquivos para filtrar os resultados.

Returns:
    str ou None: Uma mensagem de erro se as entradas forem inválidas,
    ou `None` se as entradas forem válidas.
"""

import json
from typing import List, Optional
from src.controllers.controle_caminhos import ControladorDeCaminhos


def validar_entradas(caminhos: List[str], extensoes: Optional[List[str]]):
    """
    Valida os parâmetros de entrada para a função `exibir_resultados`.

    Args:
        caminhos (List[str]): Uma lista de caminhos de arquivos para analisar.
        extensoes (Optional[List[str]]): Uma lista opcional de extensões
        de arquivos para filtrar os resultados.

    Retorna:
        str ou None: Uma mensagem de erro caso as entradas sejam inválidas,
        ou `None` caso as entradas sejam válidas.
    """
    if not all(isinstance(caminho, str) for caminho in caminhos):
        return "'caminhos' deve ser uma lista de strings."

    if extensoes and not all(isinstance(extensao, str) for extensao in extensoes):
        return "'extensoes' deve ser uma lista de strings."

    return None


def filtrar_por_extensao(
    arquivos: List[dict], extensoes: Optional[List[str]]
) -> List[dict]:
    """
    Filtra a lista de dicionários de informações de arquivos pelas extensões fornecidas.

    Args:
        arquivos (List[dict]): Uma lista de dicionários com informações sobre arquivos.
        extensoes (Optional[List[str]]): Uma lista opcional de extensões de arquivos
        para filtrar os resultados.

    Retorna:
        List[dict]: A lista filtrada de dicionários de informações de arquivos.
    """
    return (
        [arquivo for arquivo in arquivos if arquivo["extensao"] in extensoes]
        if extensoes
        else arquivos
    )


def exibir_resultados(caminhos: List[str], extensoes: Optional[List[str]] = None):
    """
    Exibe os resultados da análise dos caminhos fornecidos, com filtro opcional por extensões.

    Args:
        caminhos (List[str]): Uma lista de caminhos de arquivos para analisar.
        extensoes (Optional[List[str]]): Uma lista opcional de extensões de arquivos
        para filtrar os resultados.
    """
    # Valida entradas
    erro = validar_entradas(caminhos, extensoes)
    if erro:
        print(f"Erro: {erro}")
        return

    try:
        # Processa os caminhos
        controlador = ControladorDeCaminhos(caminhos, extensoes)
        resultados_json = json.loads(controlador.processar_caminhos())

        # Filtra por extensão, se necessário
        for resultado in resultados_json:
            if resultado.get("status") == "pasta" and "conteudo" in resultado:
                resultado["conteudo"] = filtrar_por_extensao(
                    resultado["conteudo"], extensoes
                )

        # Exibe os resultados
        print(json.dumps(resultados_json, ensure_ascii=False, indent=4))

    except (ValueError, TypeError, FileNotFoundError, PermissionError) as e:
        print(f"Erro ao processar caminhos: {e}")
