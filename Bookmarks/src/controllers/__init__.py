# src/controllers/__init__.py
# pylint: disable=E0401

"""
Este módulo inicializa o pacote 'controllers' e
disponibiliza a classe ControladorDeCaminhos.

O objetivo deste pacote é centralizar o gerenciamento
dos caminhos de arquivos e diretórios, processando-os
para gerar relatórios detalhados sobre seus conteúdos,
especialmente para uso em sistemas de manipulação de arquivos.

A classe `ControladorDeCaminhos` permite:
- Processar uma lista de caminhos fornecidos.
- Filtrar subitens de diretórios com base em extensões de arquivo.
- Gerar relatórios detalhados sobre os caminhos processados em formato JSON.
"""

from .controle_caminhos import ControladorDeCaminhos

__all__ = ["ControladorDeCaminhos"]
