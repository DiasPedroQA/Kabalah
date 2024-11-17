# src/models/modelo_caminhos.py
# pylint: disable=C

from pathlib import Path
from typing import List, Optional, Union


class Caminho:
    def __init__(self, caminho: Union[str, Path]):
        self.path = Path(caminho)

    @property
    def existe(self) -> bool:
        return self.path.exists()

    @property
    def nome(self) -> str:
        return self.path.name

    @property
    def tipo(self) -> str:
        if self.is_directory():
            return "pasta"
        if self.is_file():
            return "arquivo"
        return "inválido"

    def is_directory(self) -> bool:
        return self.path.is_dir()

    def is_file(self) -> bool:
        return self.path.is_file()

    def para_dict(self) -> dict:
        return {
            "nome": self.nome,
            "caminho": str(self.path),
            "existe": self.existe,
            "tipo": self.tipo,
        }


class Arquivo(Caminho):
    def __init__(self, caminho: Union[str, Path]):
        super().__init__(caminho)
        if not self.is_file():
            raise ValueError(f"O caminho {self.path} não é um arquivo.")

    @property
    def extensao(self) -> str:
        return self.path.suffix

    @property
    def tamanho(self) -> int:
        return self.path.stat().st_size

    def tamanho_formatado(self) -> str:
        """Retorna o tamanho do arquivo formatado em kB."""
        return f"{self.tamanho / 1024:.2f} kB"

    def para_dict(self) -> dict:
        dados = super().para_dict()
        dados.update(
            {
                "extensao": self.extensao,
                "tamanho": self.tamanho_formatado(),
            }
        )
        return dados


class Pasta(Caminho):
    def __init__(self, caminho: Union[str, Path]):
        super().__init__(caminho)
        if not self.is_directory():
            raise ValueError(f"O caminho {self.path} não é uma pasta.")

    @property
    def subitens(self) -> List[Caminho]:
        itens = []
        try:
            for item in self.path.iterdir():
                if item.is_file():
                    itens.append(Arquivo(item))
                elif item.is_dir():
                    itens.append(Pasta(item))
        except PermissionError:
            # Pode adicionar um log para erros de permissão ou retornar um erro de acesso  # noqa
            itens.append(Caminho(f"Inacessível: {self.path}"))
        return itens

    def listar_arquivos(self, extensoes: Optional[List[str]] = None) -> List[Arquivo]:  # noqa
        arquivos = []
        try:
            arquivos = [Arquivo(f) for f in self.path.iterdir() if f.is_file()]
            if extensoes:
                arquivos = [arq for arq in arquivos if arq.extensao in extensoes]
        except PermissionError:
            # Pode retornar uma mensagem ou registrar o erro
            pass
        return arquivos

    def para_dict(self) -> dict:
        dados = super().para_dict()
        dados.update({"subitens": [item.para_dict() for item in self.subitens]})
        return dados
