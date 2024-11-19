# src/views/visual_caminho.py
# pylint: disable=C

import json
from typing import List, Optional
from controllers.controle_caminhos import ControladorDeCaminhos


def validar_entradas(caminhos: List[str], extensoes: Optional[List[str]]):
    if not isinstance(caminhos, list):
        return "'caminhos' deve ser uma lista de strings representando caminhos."  # noqa

    if any(not isinstance(caminho, str) for caminho in caminhos):
        return "Todos os itens em 'caminhos' devem ser do tipo string."

    if extensoes and not isinstance(extensoes, list):
        return "'extensoes' deve ser uma lista de strings representando extensões."  # noqa

    if extensoes and any(not isinstance(extensao, str) for extensao in extensoes):  # noqa
        return "Todos os itens em 'extensoes' devem ser do tipo string."

    return None  # Caso não haja erro


def filtrar_por_extensao(
    arquivos: List[dict], extensoes: Optional[List[str]]
) -> List[dict]:  # noqa
    """Filtra os arquivos por extensão, se as extensões forem fornecidas."""
    if not extensoes:
        return arquivos  # Retorna todos os arquivos se não houver filtro

    # Filtra os arquivos que possuem a extensão dentro da lista fornecida
    return [arquivo for arquivo in arquivos if arquivo['extensao'] in extensoes]  # noqa


def exibir_resultados(caminhos: List[str], extensoes: Optional[List[str]] = None):  # noqa
    # Validação das entradas
    erro_validacao = validar_entradas(caminhos, extensoes)
    if erro_validacao:
        print(f"Erro: {erro_validacao}")
        return

    try:
        # Criação do controlador e processamento dos dados
        controlador = ControladorDeCaminhos(caminhos, extensoes)
        resultados = controlador.processar_e_gerar_json()

        # Parse do JSON para manipulação dos resultados
        resultados_json = json.loads(resultados)  # noqa

        # Filtra os arquivos, se as extensões forem fornecidas
        for resultado in resultados_json:
            if resultado.get("status") == "pasta" and "conteudo" in resultado:
                resultado["conteudo"] = filtrar_por_extensao(
                    resultado["conteudo"], extensoes
                )  # noqa

        # Exibe os resultados de forma legível
        print("Resultados da análise:")
        print(json.dumps(resultados_json, ensure_ascii=False, indent=4))  # noqa

    except (ValueError, TypeError, FileNotFoundError, PermissionError) as e:
        print(f"Erro ao processar caminhos: {e}")
