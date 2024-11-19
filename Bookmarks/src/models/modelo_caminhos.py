# src/models/modelo_caminhos.py

"""
Represents a base class for obtaining detailed information
about a file or directory, returning the data in JSON format.

The `CaminhoBase` class provides methods to:
- Sanitize the path to prevent directory traversal
- Retrieve file/directory statistics, including size in kB
    and formatted creation/modification dates
- List the sub-items within a directory
- Retrieve the absolute path of the file/directory

The class can be used as a context manager,
allowing it to be used in a `with` statement.
"""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class CaminhoBase:
    """
    Classe para representar e obter informações detalhadas sobre um arquivo ou diretório,
    retornando os dados em formato JSON.
    """

    def __init__(self, caminho: str) -> None:
        """
        Inicializa a classe com o caminho especificado.
        :param caminho: Caminho do arquivo ou diretório.
        """
        self.caminho_atual = Path(self._sanitizar_e_resolver_caminho(caminho))

    def __enter__(self) -> "CaminhoBase":
        """
        Permite usar a classe como gerenciador de contexto.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Método de limpeza ao sair do contexto. Não realiza nenhuma ação específica aqui.
        """
        return None

    def _sanitizar_e_resolver_caminho(self, caminho: str) -> Optional[str]:
        """
        Sanitiza o caminho, previne traversal de diretórios e retorna o caminho absoluto.
        """
        sanitized_path = os.path.normpath(caminho)

        # Prevenir traversal de diretórios
        if ".." in sanitized_path.split(os.sep):
            return str(f"Caminho inválido: ({caminho}) tentativa de traversal detectada.")

        # Retorna o caminho absoluto
        caminho = Path(sanitized_path)
        return str(caminho.resolve() if not caminho.is_absolute() else caminho.absolute())

    def _estatisticas(self) -> Dict:
        """
        Obtém as estatísticas do arquivo ou diretório, incluindo o tamanho em kB
        e as datas formatadas no padrão brasileiro.
        """
        try:
            stats = self.caminho_atual.stat()
            tamanho_kb = stats.st_size / 1024
            return {
                "tamanho_em_kB": round(tamanho_kb, 2),
                "modificado_em": datetime.fromtimestamp(stats.st_mtime).strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),
                "criado_em": datetime.fromtimestamp(stats.st_ctime).strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),
            }
        except FileNotFoundError:
            return {
                "status": "falha",
                "erro": f"Caminho ({self.caminho_atual}) não encontrado",
            }

    def _subitens(self) -> Dict[str, List[str]]:
        """
        Retorna os subitens dentro de um diretório, se for um diretório.
        """
        if not self.caminho_atual.exists() or not self.caminho_atual.is_dir():
            return {"subitens": []}
        return {"subitens": [str(item) for item in self.caminho_atual.iterdir()]}

    def _dados_caminho(self) -> Dict:
        """
        Obtém diversas informações sobre o caminho, incluindo nome, extensão, etc.
        """
        if not self.caminho_atual.exists():
            return {
                "status": "falha",
                "erro": "O caminho especificado não existe",
            }

        return {
            "tipo": (
                "arquivo"
                if self.caminho_atual.is_file()
                else "diretório" if self.caminho_atual.is_dir() else "desconhecido"
            ),
            "diretorio_pai": str(self.caminho_atual.parent),
            "nome": str(self.caminho_atual.stem + self.caminho_atual.suffix),
            "caminho_absoluto": self._sanitizar_e_resolver_caminho(str(self.caminho_atual)),
            "estatisticas": self._estatisticas(),
        }

    def obter_informacoes(self) -> str:
        """
        Converte as informações para um formato JSON.
        """
        infos = self._dados_caminho()
        subitens = self._subitens()
        if subitens["subitens"]:
            infos.update(subitens)
        return json.dumps({"infos": infos}, indent=4, ensure_ascii=False)


# Exemplo de uso:
if __name__ == "__main__":
    caminho_diretorio = CaminhoBase('/home/pedro-pm-dias/Downloads/Chrome/')
    print("\nInformações (em JSON) do diretório =>", caminho_diretorio.obter_informacoes())

    caminho_arquivo = CaminhoBase(
        '/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html'
    )
    print("\nInformações (em JSON) do arquivo =>", caminho_arquivo.obter_informacoes())

    caminho_teste1 = CaminhoBase('/home/pedro-pm-dias/Downloads/Chrome/Teste/')
    print("\nInformações (em JSON) do teste1 =>", caminho_teste1.obter_informacoes())

    caminho_teste2 = CaminhoBase('/home/pedro-pm-dias/Downloads/Chrome/InvalidPath')
    print("\nInformações (em JSON) do teste2 =>", caminho_teste2.obter_informacoes())

    caminho_teste3 = CaminhoBase('../../Downloads/')
    print("\nInformações (em JSON) do teste3 =>", caminho_teste3.obter_informacoes())

    caminho_teste4 = CaminhoBase("")
    resultado = json.loads(caminho_teste4.obter_informacoes())
    print("\nInformações (em JSON) do teste4 =>", resultado)
    assert "infos" in resultado

    with tempfile.TemporaryDirectory() as temp_dir:
        caminho = CaminhoBase(temp_dir)
        resultado = json.loads(caminho.obter_informacoes())
        # assert "subitens" in resultado["infos"]
        # assert len(resultado["infos"]["subitens"]) == 0
