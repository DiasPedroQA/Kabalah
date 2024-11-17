# src/controllers/controle_caminhos.py
# pylint: disable=C, E

import json
from typing import List, Optional
from models.modelo_caminhos import Caminho, Arquivo, Pasta


class ControladorDeCaminhos:
    def __init__(
        self,
        paths: List[str],
        filtro_extensoes: Optional[List[str]] = None
    ):
        self.caminhos = [Caminho(path) for path in paths]
        self.filtro_extensoes = filtro_extensoes

    def processar_e_gerar_json(self) -> List[dict]:
        """Processa todos os caminhos fornecidos e retorna um relatório."""
        resultados = []
        for caminho in self.caminhos:
            encontrados = self._buscar_recursivamente(caminho)  # Busca recursiva  # noqa
            for item in encontrados:
                resultados.append(self._processar_caminho(item))  # Processa cada item encontrado  # noqa
        return resultados

    def _processar_caminho(self, caminho: Caminho) -> dict:
        """Processa um único caminho e retorna o resultado adequado."""
        if not caminho.existe:
            return {
                "status": "inválido",
                "mensagem": f"O caminho {caminho.path} não existe."
            }
        if caminho.tipo == "pasta":
            return self._processar_pasta(caminho)
        if caminho.tipo == "arquivo":
            return self._processar_arquivo(caminho)
        return {}

    def _processar_pasta(self, caminho: Caminho) -> dict:
        """Processa um caminho que é uma pasta."""
        try:
            pasta = Pasta(caminho.path)
            arquivos = pasta.listar_arquivos(self.filtro_extensoes)
            subitens = pasta.subitens  # Buscando subitens (subpastas e arquivos)  # noqa
            return {
                "status": "pasta",
                "mensagem": f"O caminho {caminho.path} é uma pasta.",
                "conteudo": [arquivo.para_dict() for arquivo in arquivos],
                "subitens": [item.para_dict() for item in subitens]  # Incluindo subpastas  # noqa
            }
        except ValueError as e:
            return {
                "status": "erro",
                "mensagem": f"Erro ao processar pasta {caminho.path}: {str(e)}"
            }

    def _processar_arquivo(self, caminho: Caminho) -> dict:
        """Processa um caminho que é um arquivo."""
        try:
            arquivo = Arquivo(caminho.path)
            return {
                "status": "arquivo",
                "mensagem": f"O caminho {caminho.path} é um arquivo.",
                "conteudo": arquivo.para_dict()
            }
        except ValueError as e:
            return {
                "status": "erro",
                "mensagem": f"Erro ao processar o arquivo {caminho.path}: {str(e)}"  # noqa
            }

    def _buscar_recursivamente(self, caminho: Caminho) -> List[Caminho]:
        """Busca recursivamente por arquivos e pastas dentro de uma pasta."""
        encontrados = []
        if caminho.tipo == "pasta":
            try:
                pasta = Pasta(caminho.path)
                encontrados.append(pasta)  # Adiciona a própria pasta
                for subitem in pasta.subitens:
                    encontrados.extend(self._buscar_recursivamente(subitem))  # Chamada recursiva  # noqa
            except ValueError:
                pass  # Ignora pastas que não podem ser acessadas
        elif caminho.tipo == "arquivo":
            encontrados.append(Arquivo(caminho.path))  # Adiciona o arquivo encontrado  # noqa
        return encontrados

    def gerar_relatorio_json(self) -> str:
        """Processa todos os caminhos e gera o relatório em formato JSON."""
        resultados = self.processar_e_gerar_json()  # Usa o método de processamento de caminhos  # noqa
        return json.dumps(resultados, ensure_ascii=False, indent=4)
