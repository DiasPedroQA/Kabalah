"""
Fornece funções para validar e analisar caminhos de arquivos e listas de caminhos.

A função `validar_string` verifica se um valor fornecido é uma string válida
e retorna uma mensagem de erro apropriada se não for.

A função `validar_caminho` verifica se um caminho fornecido é válido
e retorna uma mensagem indicando se o caminho é absoluto ou relativo,
e se aponta para um arquivo, diretório ou não existe.

A função `analisar_lista` aceita uma lista de strings ou valores `None`
e retorna uma lista de mensagens de validação para cada item na lista.

A função `analisar_caminho` aceita um dicionário de valores,
onde os valores podem ser strings ou listas de strings ou valores `None`,
e retorna uma lista de mensagens de validação para cada valor no dicionário.
"""

# src/controllers/path_check_controller.py

from typing import Union, List, Dict, Optional
import os
import logging
from fastapi import APIRouter

# Configuração do logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Criação do router
router = APIRouter()


def validar_string(valor: Union[str, None]) -> Optional[str]:
    """Valida se o valor é uma string e retorna a mensagem apropriada."""
    if valor is None:
        logger.info("Valor analisado: None (null).")
        return "O valor é None (null)."
    elif isinstance(valor, str):
        if valor.strip() == "":
            logger.info("Valor analisado: String vazia.")
            return "O valor é uma string vazia."
        elif any(char in valor for char in ['?', '*', ':', '<', '>', '|']):
            logger.info("Valor analisado: '%s' contém caracteres inválidos.", valor)
            return f"O valor é um caminho inválido: '{valor}'. Contém caracteres inválidos."
    else:
        logger.info("Valor analisado: Tipo '%s', não suportado.", type(valor).__name__)
        return f"O valor é do tipo {type(valor).__name__}, que não é suportado para análise."
    return None


def validar_caminho(valor: str) -> str:
    """Valida se o valor é um caminho absoluto ou relativo e informa se é arquivo ou pasta."""
    tipo_caminho = "absoluto" if os.path.isabs(valor) else "relativo"
    nome_final = os.path.basename(valor)

    logger.info("\nAnalisando caminho: '%s'", valor)
    logger.info(" - Tipo de caminho: %s", tipo_caminho.capitalize())

    if os.path.exists(valor) and os.path.isfile(valor):
        return (
            f"O valor é um caminho {tipo_caminho} válido para um arquivo: "
            f"'{valor}'. Nome do arquivo: '{nome_final}'."
        )
    if os.path.exists(valor) and os.path.isdir(valor):
        return f"O valor é um caminho {tipo_caminho} válido para uma pasta: '{nome_final}'."

    return f"O valor é um caminho {tipo_caminho} inválido: '{valor}'. Não existe."


@router.post("/analisar_caminho/")
async def analisar_caminho(
    dados: Dict[str, Union[str, List[Union[str, None]], None]]
) -> List[str]:
    """
    Endpoint para analisar caminhos de arquivos e pastas.
    Recebe um dicionário com caminhos e retorna uma lista de mensagens de validação.
    """
    resultados = []
    for valor in dados.values():
        if isinstance(valor, list):
            for item in valor:
                if invalid_message := validar_string(item):
                    resultados.append(invalid_message)
                else:
                    resultados.append(validar_caminho(item))
        elif invalid_message := validar_string(valor):
            resultados.append(invalid_message)
        else:
            resultados.append(validar_caminho(valor))
    return resultados
