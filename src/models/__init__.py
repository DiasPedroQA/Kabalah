# src/models/__init__.py

"""
Este módulo define três classes para representar diferentes tipos de
caminhos no sistema de arquivos:

- `PathModel`: Classe base para representar qualquer tipo de caminho.
- `FilePathModel`: Subclasse de `PathModel` que representa um arquivo.
- `FolderPathModel`: Subclasse de `PathModel` que representa uma pasta.

Essas classes oferecem uma maneira consistente de trabalhar com caminhos
do sistema de arquivos na sua aplicação.
"""

from .path_models import PathModel, FilePathModel, FolderPathModel

__all__ = ["PathModel", "FilePathModel", "FolderPathModel"]
