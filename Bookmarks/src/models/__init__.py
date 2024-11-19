# Bookmarks/src/models/__init__.py
# pylint: disable=E0401

"""
Pacote `models`.

Este módulo inicializa o pacote `models`, facilitando a importação das classes e funções principais
para o gerenciamento de caminhos, como a classe `CaminhoBase` do módulo `modelo_caminhos`.

A classe `CaminhoBase` oferece funcionalidades para trabalhar com arquivos e diretórios, permitindo
a obtenção de informações detalhadas sobre caminhos no sistema de arquivos.

Exemplo de uso:
    from src.models import CaminhoBase
    caminho = CaminhoBase("/caminho/para/diretorio")
    print(caminho.obter_informacoes())

Este arquivo marca o diretório `models` como um pacote Python e expõe a classe `CaminhoBase`.
"""

from .modelo_caminhos import CaminhoBase

__all__ = ["CaminhoBase"]
