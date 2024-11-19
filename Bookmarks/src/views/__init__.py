# src/views/__init__.py

"""
Pacote `views` responsável pela interação com o usuário e exibição dos resultados processados.

Este módulo importa e torna acessíveis as funções essenciais
de visualização de caminhos, como `exibir_resultados`,
permitindo que outras partes do sistema interajam com
os dados e os mostrem de maneira adequada.

Exemplos de uso:
    - Exibir relatórios de análise de caminhos.
    - Filtrar e validar entradas de dados para processamento de arquivos.

Módulos importados:
    - `visual_caminho`: Contém funções relacionadas ao processamento
    e exibição de caminhos de arquivos.
"""

from .visual_caminho import exibir_resultados

__all__ = ["exibir_resultados"]
