# app/models/path_model.py
# pylint: disable=E0401, R0903, W0105


"""
Módulo para gerenciar caminhos de arquivos e diretórios.
"""


import json
from pathlib import Path
from typing import Dict, List
from json_do_frontend import json_frontend


class ItemSistema:
    """Representa um item genérico no sistema de arquivos."""

    def __init__(self, caminho: Path) -> None:
        if not caminho.exists():
            raise ValueError(f"O caminho {caminho} não existe.")
        self.caminho = caminho
        self.nome = caminho.name
        self.data_criacao = caminho.stat().st_ctime
        self.data_modificacao = caminho.stat().st_mtime

    def para_json(self) -> Dict:
        """Retorna as informações básicas do item como um dicionário."""
        return {
            "caminho": str(self.caminho),
            "nome": self.nome,
            "data_criacao": self.data_criacao,
            "data_modificacao": self.data_modificacao,
        }


class Arquivo(ItemSistema):
    """Representa um arquivo no sistema de arquivos."""

    def __init__(self, caminho: Path) -> None:
        if not caminho.is_file():
            raise ValueError(f"O caminho {caminho} não é um arquivo válido.")
        super().__init__(caminho)
        self.extensao = caminho.suffix
        self.tamanho_formatado = self._formatar_tamanho_arquivo(caminho.stat().st_size)

    @staticmethod
    def _formatar_tamanho_arquivo(tamanho_arquivo: int) -> str:
        """Formata o tamanho do arquivo para uma string legível."""
        for unidade in ["bytes", "KB", "MB", "GB"]:
            if tamanho_arquivo < 1024:
                return f"{tamanho_arquivo:.2f} {unidade}"
            tamanho_arquivo /= 1024
        return f"{tamanho_arquivo:.2f} TB"

    def para_json(self) -> Dict:
        """Adiciona informações específicas de arquivo ao JSON."""
        dados = super().para_json()
        dados.update({
            "extensao": self.extensao,
            "tamanho": self.tamanho_formatado,
        })
        return dados


class Diretorio(ItemSistema):
    """Representa um diretório no sistema de arquivos."""

    def __init__(self, caminho: Path) -> None:
        if not caminho.is_dir():
            raise ValueError(f"O caminho {caminho} não é um diretório válido.")
        super().__init__(caminho)
        self.arquivos: List[Arquivo] = []
        self.subdiretorios: List["Diretorio"] = []
        self._atualizar_conteudo()

    def _atualizar_conteudo(self) -> None:
        """Atualiza o conteúdo do diretório."""
        self.arquivos.clear()
        self.subdiretorios.clear()
        for item in self.caminho.iterdir():
            if item.is_file():
                self.arquivos.append(Arquivo(item))
            elif item.is_dir():
                self.subdiretorios.append(Diretorio(item))

    def para_json(self) -> Dict:
        """Adiciona informações específicas de diretório ao JSON."""
        dados = super().para_json()
        dados.update({
            "sub_arquivos": [arquivo.para_json() for arquivo in self.arquivos],
            "sub_pastas": [subdiretorio.para_json() for subdiretorio in self.subdiretorios],
        })
        return dados


class AnalisadorCaminhos:
    """Classe para analisar caminhos de arquivos e diretórios."""

    def __init__(self, max_tentativas: int = 10) -> None:
        self.max_tentativas = max_tentativas

    def _validar_json(self, json_caminhos: Dict) -> bool:
        """Valida a estrutura do JSON de entrada."""
        return "jsonEntrada" in json_caminhos and isinstance(json_caminhos["jsonEntrada"], list)

    def _ajustar_caminhos(self, lista_caminhos: List[str]) -> List[Path]:
        """Ajusta caminhos relativos e valida a existência."""
        caminhos_ajustados = []
        for caminho_str in lista_caminhos:
            caminho = Path(caminho_str).resolve()
            if caminho.exists():
                caminhos_ajustados.append(caminho)
            elif caminho_str.startswith("../"):
                for _ in range(self.max_tentativas):
                    caminho = Path("../") / caminho
                    if caminho.exists():
                        caminhos_ajustados.append(caminho.resolve())
                        break
        return caminhos_ajustados

    def processar_caminhos(self, json_bruto: str) -> List[Dict]:
        """Processa os caminhos fornecidos, criando objetos Arquivo ou Diretorio."""
        try:
            json_entrada = json.loads(json_bruto)
            if not self._validar_json(json_entrada):
                raise ValueError("Estrutura JSON inválida.")
        except json.JSONDecodeError as e:
            raise ValueError("Entrada JSON inválida.") from e

        lista_caminhos = json_entrada["jsonEntrada"]
        caminhos_ajustados = self._ajustar_caminhos(lista_caminhos)

        resultados_processados = []
        for caminho in caminhos_ajustados:
            if caminho.is_file():
                resultados_processados.append(Arquivo(caminho).para_json())
            elif caminho.is_dir():
                resultados_processados.append(Diretorio(caminho).para_json())
            else:
                resultados_processados.append({"caminho": str(caminho), "erro": "Caminho inválido"})
        return resultados_processados

if __name__ == "__main__":
    # Exemplo de uso
    analisador = AnalisadorCaminhos()
    try:
        resultados = analisador.processar_caminhos(json_frontend)
        for resultado in resultados:
            print(json.dumps(resultado, indent=4, ensure_ascii=False))
    except ValueError as erro:
        print(f"Erro ao processar caminhos: {erro}")
