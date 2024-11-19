# src/__init__.py

"""
Pacote principal do sistema de análise de caminhos.

Este pacote serve como ponto de inicialização para o módulo `src`, facilitando o acesso
aos módulos essenciais como `controllers`, `models` e `views`.

A estrutura deste pacote permite uma organização clara e uma fácil manutenção do código.
"""

# O pacote `src` inicializa e expõe os módulos principais.
from .controllers import ControladorDeCaminhos
from .models import CaminhoBase
from .views import exibir_resultados

__all__ = ["ControladorDeCaminhos", "CaminhoBase", "exibir_resultados"]
