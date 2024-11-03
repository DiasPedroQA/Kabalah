# pylint: disable=C
# src/models/path_models.py


def processar_pasta(caminho):
    # Retorna dados fictícios de uma pasta
    return {"caminho": caminho, "itens": ["file1.txt", "file2.txt", "subfolder"]}


def processar_arquivo(caminho):
    # Retorna dados fictícios de um arquivo
    return {"caminho": caminho, "conteudo": "Conteúdo do arquivo de exemplo"}


# class PathModel:
#     """Classe base para representar um caminho no sistema de arquivos."""

#     def __init__(self, modelpath: str):
#         """
#         Inicializa o modelo de caminho com o caminho especificado.

#         Argumento(s):
#             modelpath (str): O caminho a ser representado.
#         """
#         self.path: Path = Path(modelpath)  # Usando Path do pathlib
#         self.logger = CustomLogger(__name__)  # Instância do logger

#     def is_path_folder(self) -> bool:
#         """Verifica se o caminho é uma pasta."""
#         return self.path.is_dir()

#     def is_path_file(self) -> bool:
#         """Verifica se o caminho é um arquivo."""
#         return self.path.is_file()

#     def is_path_absolute(self) -> bool:
#         """Verifica se o caminho é absoluto."""
#         return self.path.is_absolute()

#     def to_obj_json(self) -> str:
#         """Retorna um JSON representando o modelo."""
#         obj_data = {
#             str(self.path): {
#                 "is_absolute": self.is_path_absolute(),
#                 "is_folder": self.is_path_folder(),
#                 "is_file": self.is_path_file(),
#             },
#         }

#         if hasattr(self, "get_file_extension"):
#             obj_data["file_extension"] = self.get_file_extension()

#         if hasattr(self, "list_contents"):
#             obj_data["contents"] = [item.to_obj_json() for item in self.list_contents()]

#         return json.dumps(obj_data, ensure_ascii=False, indent=4)


# class FilePathModel(PathModel):
#     """Representa um caminho de arquivo, herdando de PathModel."""

#     def __init__(self, filepath: str):
#         """Inicializa o modelo de caminho de arquivo com o caminho especificado."""
#         super().__init__(filepath)
#         self.file_path = filepath
#         self.file_size: int = self.get_file_size()  # Tamanho do arquivo em bytes
#         self.file_extension: str = self.get_file_extension()  # Extensão do arquivo

#     def get_file_extension(self) -> str:
#         """Obtém a extensão do arquivo."""
#         if not self.is_path_file():
#             self.logger.warning(
#                 f"Tentativa de obter extensão de {self.path} que não é um arquivo."
#             )
#             return "Not Found"
#         return self.path.suffix  # Usando suffix do pathlib

#     def get_file_size(self) -> int:
#         """Obtém o tamanho do arquivo."""
#         if not self.is_path_file():
#             self.logger.warning(
#                 f"Tentativa de obter tamanho de {self.path} que não é um arquivo."
#             )
#             return 0
#         return self.path.stat().st_size  # Usando stat() do pathlib


# class FolderPathModel(PathModel):
#     """Representa um caminho de pasta, herdando de PathModel."""

#     def __init__(self, folderpath: str):
#         """Inicializa o modelo de caminho de pasta com o caminho especificado."""
#         super().__init__(folderpath)
#         self.num_contents: int = self.count_contents()  # Número de itens na pasta
#         self.contents: List[Union[FilePathModel, 'FolderPathModel']] = []  # Lista de conteúdos

#     def count_contents(self) -> int:
#         """Conta o número de itens na pasta."""
#         if not self.is_path_folder():
#             self.logger.warning(
#                 f"Tentativa de contar itens de {self.path} que não é uma pasta."
#             )
#             return 0
#         return len(list(self.path.iterdir()))  # Usando iterdir() do pathlib

#     def list_contents(self, depth: int = 10) -> List[Union[FilePathModel, 'FolderPathModel']]:
#         """Lista o conteúdo da pasta com profundidade opcional."""
#         if not self.is_path_folder():
#             self.logger.warning(
#                 f"Tentativa de listar conteúdo de {self.path} que não é uma pasta."
#             )
#             return []

#         conteudo_identificado = []
#         try:
#             for item in self.path.iterdir():  # Usando iterdir() do pathlib
#                 if item.is_file():
#                     conteudo_identificado.append(
#                         FilePathModel(str(item))
#                     )  # Converter para string
#                 elif item.is_dir() and depth != 0:
#                     folder_model = FolderPathModel(str(item))  # Converter para string
#                     conteudo_identificado.append(folder_model)
#                     conteudo_identificado.extend(folder_model.list_contents(depth - 1))
#         except FileNotFoundError:
#             self.logger.error(f"Arquivo ou pasta não encontrado: {self.path}")
#         except PermissionError:
#             self.logger.error(f"Erro de permissão ao acessar {self.path}")
#         except OSError as e:
#             self.logger.error(f"Erro ao listar conteúdo de {self.path}: {e.strerror}")

#         self.contents = conteudo_identificado  # Armazena o conteúdo na instância
#         return conteudo_identificado
