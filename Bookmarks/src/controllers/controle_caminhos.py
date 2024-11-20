# src/controllers/controle_caminhos.py
# pylint: disable=E0401, E0611, C0413

"""
Controller para processar caminhos de arquivos e diretórios, gerando relatórios em JSON.
"""

import json
from typing import List, Optional, Dict, Union
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.models.modelo_caminhos import CaminhoBase  # noqa: E402


class ControladorDeCaminhos:
    """
    This class likely manages or controls paths in a system.
    """

    def __init__(
        self, lista_caminhos: List[str], filtro_extensoes: Optional[List[str]] = None
    ):
        """
        Inicializa o controlador com os caminhos a serem processados e um filtro opcional.

        :param caminhos: Lista de caminhos de arquivos ou diretórios.
        :param filtro_extensoes: Lista de extensões para filtrar arquivos (ex.: ['.txt', '.json']).
        """
        self.caminhos = lista_caminhos
        self.filtro_extensoes = filtro_extensoes

    def processar_caminhos(self) -> List[Dict[str, Union[str, dict]]]:
        """
        Processa todos os caminhos fornecidos e retorna um relatório detalhado.
        """
        resultados = []
        for caminho in self.caminhos:
            with CaminhoBase(caminho) as caminho_base:
                resultados.append(self._processar_caminho(caminho_base))
        return resultados

    def _processar_caminho(self, caminho: CaminhoBase) -> Dict[str, Union[str, dict]]:
        """
        Processa um único caminho e gera um relatório sobre ele.

        :param caminho: Instância de `CaminhoBase`.
        :return: Dicionário com informações detalhadas.
        """
        dados = json.loads(caminho.obter_informacoes())
        infos = dados.get("infos", {})

        if infos.get("tipo") == "diretório":
            subitens = infos.get("subitens", [])
            if self.filtro_extensoes:
                subitens = [
                    item
                    for item in subitens
                    if any(item.endswith(ext) for ext in self.filtro_extensoes)
                ]
            infos["subitens"] = subitens

        return infos

    def gerar_relatorio_json(self) -> str:
        """
        Gera o relatório dos caminhos processados em formato JSON.

        :return: String JSON contendo o relatório.
        """
        resultados = self.processar_caminhos()
        return json.dumps(resultados, ensure_ascii=False, indent=4)


# Exemplo de uso:
# if __name__ == "__main__":
#     caminhos = [
#         # "/home/pedro-pm-dias/Downloads/Chrome/",
#         # "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html",
#         # "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
#         "/home/pedro-pm-dias/Downloads/Chrome/InvalidPath",  # Caminho inválido
#         "../../Downloads/",  # Caminho relativo para a pasta Downloads/
#         "",  # Caminho vazio
#     ]
#     controlador = ControladorDeCaminhos(caminhos, filtro_extensoes=[".txt", ".json"])
#     # relatorio = controlador.gerar_relatorio_json()
#     # print("\nrelatorio =>", relatorio)
#     processos = controlador.processar_caminhos()
#     print("\nprocessos =>", processos)
