# src/utils/__init__.py
"""
Fornece uma instância de logger para o pacote utils.

O objeto `meu_logger` é uma instância de logger que
pode ser usada em todo o pacote utils.
Ele está disponível para importação no nível do pacote,
tornando-o mais acessível.
"""

from src.utils.logger import meu_logger

# O objetivo aqui é tornar os métodos mais acessíveis ao importar o pacote.
__all__ = ['meu_logger']
