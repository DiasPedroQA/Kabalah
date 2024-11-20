# Bookmarks/src/models/modelo_caminhos.py

"""
Módulo CaminhoBase:
Fornece uma classe para obter informações detalhadas sobre
arquivos ou diretórios e retorna os dados no formato JSON.

Funcionalidades:
- Sanitização de caminhos para evitar traversal de diretórios
- Recuperação de estatísticas do arquivo/diretório
- Listagem de subitens (para diretórios)
- Representação completa do caminho com informações relevantes
- Uso como gerenciador de contexto
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class CaminhoBase:
    """
    Classe para representar um arquivo ou diretório, fornecendo informações detalhadas.
    """

    def __init__(self, caminho_entrada: str) -> None:
        """
        Inicializa a instância com o caminho fornecido.

        :param caminho_entrada: Caminho do arquivo ou diretório.
        """
        self.caminho_atual = Path(self._sanitizar_e_resolver_caminho(caminho_entrada))

    def __enter__(self) -> "CaminhoBase":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def _sanitizar_e_resolver_caminho(self, caminho_entrada: str) -> str:
        """
        Sanitiza e resolve o caminho para evitar traversal de diretórios.

        :param caminho_entrada: Caminho bruto fornecido.
        :return: Caminho absoluto e resolvido.
        :raises ValueError: Se for detectada tentativa de traversal.
        """
        caminho_normalizado = os.path.normpath(caminho_entrada)

        if ".." in caminho_normalizado.split(os.sep):
            raise ValueError(f"Tentativa de traversal detectada no caminho: {caminho_entrada}")

        caminho_resolvido = Path(caminho_normalizado).resolve()
        return str(caminho_resolvido)

    def _estatisticas(self) -> Dict[str, Any]:
        """
        Obtém as estatísticas do caminho, como tamanho e datas.

        :return: Dicionário com as estatísticas.
        """
        try:
            stats = self.caminho_atual.stat()
            return {
                "tamanho_em_kB": round(stats.st_size / 1024, 2),
                "modificado_em": datetime.fromtimestamp(stats.st_mtime).strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),
                "criado_em": datetime.fromtimestamp(stats.st_ctime).strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),
            }
        except FileNotFoundError:
            return {
                "erro": "Caminho não encontrado",
                "status": "falha",
                "detalhes": f"O caminho ({str(self.caminho_atual)}) especificado não existe.",
            }

    def _subitens(self) -> List[str]:
        """
        Lista os subitens do diretório, se aplicável.

        :return: Lista de subitens ou vazia se não for um diretório.
        """
        if self.caminho_atual.is_dir():
            try:
                return [str(item) for item in self.caminho_atual.iterdir()]
            except PermissionError:
                return ["Erro: Permissões insuficientes"]
        return []

    def _dados_caminho(self) -> Dict[str, Any]:
        """
        Coleta informações detalhadas do caminho.

        :return: Dicionário com informações do caminho.
        """
        if not self.caminho_atual.exists():
            return {
                "erro": f"O caminho ({str(self.caminho_atual)}) especificado não existe"
            }

        tipo = "arquivo" if self.caminho_atual.is_file() else "diretório"
        return {
            "tipo": tipo,
            "diretorio_pai": str(self.caminho_atual.parent),
            "nome": self.caminho_atual.name,
            "caminho_absoluto": str(self.caminho_atual),
            "estatisticas": self._estatisticas(),
        }

    def obter_informacoes(self) -> str:
        """
        Retorna informações detalhadas do caminho em formato JSON.

        :return: Informações em formato JSON.
        """
        infos = self._dados_caminho()
        if self.caminho_atual.is_dir():
            infos["subitens"] = self._subitens()
        return json.dumps(infos, indent=4, ensure_ascii=False)


# Exemplo de uso
if __name__ == "__main__":
    try:
        caminho = CaminhoBase(
            caminho_entrada=[
                "/home/pedro-pm-dias/Downloads/Chrome/",
                "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html",
                "/home/pedro-pm-dias/Downloads/Chrome/Teste",
                "/caminho/para/teste"
            ]
        )
        print("ok:", caminho.obter_informacoes())
    except ValueError as e:
        print(f"Erro: {e}")
