# pylint: disable=C
# src/models/path_models.py

import os
import json
from typing import Dict, List, Union


class PathModel:
    def __init__(self, modelpath: str):
        self.path: str = modelpath

    def is_path_folder(self) -> bool:
        """Verifica se o caminho é uma pasta."""
        return os.path.isdir(self.path)

    def is_path_file(self) -> bool:
        """Verifica se o caminho é um arquivo."""
        return os.path.isfile(self.path)

    def is_path_absolute(self) -> bool:
        """Verifica se o caminho é absoluto."""
        return os.path.isabs(self.path)

    def to_obj_json(self) -> str:
        """Retorna uma string JSON representando o modelo."""
        obj_data: Dict[str, Union[str, bool, List[Dict[str, Union[str, bool]]]]] = {
            "path": self.path,
            "exists": {
                "is_absolute": self.is_path_absolute(),
                "is_folder": self.is_path_folder(),
                "is_file": self.is_path_file(),
            },
        }

        if hasattr(self, "get_extension"):
            obj_data["extension"] = self.get_extension()

        if hasattr(self, "list_contents"):
            obj_data["contents"] = [item.to_obj_json() for item in self.list_contents()]

        return json.dumps(obj_data, ensure_ascii=True, indent=4)


class FilePathModel(PathModel):
    def __init__(self, filepath: str):
        super().__init__(filepath)  # Chamada do construtor da classe base
        self.file_path: str = filepath

    def get_extension(self) -> str:
        """Obtém a extensão do arquivo."""
        if not self.is_path_file():
            print(
                f"WARNING: Tentativa de obter extensão de {self.file_path} que não é um arquivo: {self.path}"
            )
            return "Not Found"
        return os.path.splitext(self.file_path)[1]


class FolderPathModel(PathModel):
    def __init__(self, folderpath: str):
        super().__init__(folderpath)  # Chamada do construtor da classe base
        self.folder_path: str = folderpath

    def list_contents(self, depth: int = 10) -> List[Union[FilePathModel, 'FolderPathModel']]:
        """Lista o conteúdo da pasta com profundidade opcional."""
        if not self.is_path_folder():
            print(
                f"WARNING: Tentativa de listar conteúdo de {self.folder_path} que não é uma pasta: {self.path}"
            )
            return []

        conteudo_identificado = []
        try:
            for item in os.listdir(self.path):
                item_path = os.path.join(self.path, item)
                if os.path.isfile(item_path):
                    conteudo_identificado.append(FilePathModel(item_path))
                elif os.path.isdir(item_path) and depth != 0:
                    folder_model = FolderPathModel(item_path)
                    conteudo_identificado.append(folder_model)
                    conteudo_identificado.extend(folder_model.list_contents(depth - 1))
        except FileNotFoundError:
            print(f"ERROR: Pasta não encontrada: {self.path}")
        except PermissionError:
            print(f"ERROR: Permissão negada ao acessar o conteúdo da pasta: {self.path}")
        except IsADirectoryError:
            print(f"ERROR: Caminho não é uma pasta: {self.path}")
        except OSError as e:
            print(f"ERROR: Erro ao listar conteúdo da pasta {self.path}: {e.strerror}")

        return conteudo_identificado
