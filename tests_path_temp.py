"""
Módulo para validação de strings.
Este módulo fornece funções para validar strings,
incluindo a validação de caminhos de arquivos.
"""

import os
import logging
from typing import List, Union, Dict, Optional

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(message)s')


def validar_string(valor: Union[str, None]) -> Optional[str]:
    """Valida se o valor é uma string e retorna a mensagem apropriada."""
    if valor is None:
        logging.info("Valor analisado: None (null).")
        return "O valor é None (null)."
    elif isinstance(valor, str):
        if valor.strip() == "":
            logging.info("Valor analisado: String vazia.")
            return "O valor é uma string vazia."
        elif any(char in valor for char in ['?', '*', ':', '<', '>', '|']):
            logging.info("Valor analisado: '%s' contém caracteres inválidos.", valor)
            return f"O valor é um caminho inválido: '{valor}'. Contém caracteres inválidos."
    else:
        logging.info("Valor analisado: Tipo '%s', não suportado.", type(valor).__name__)
        return f"O valor é do tipo {type(valor).__name__}, que não é suportado para análise."
    return None


def validar_caminho(valor: str) -> str:
    """Valida se o valor é um caminho absoluto ou relativo
    e informa se é arquivo, pasta ou inexistente."""
    tipo_caminho = "absoluto" if os.path.isabs(valor) else "relativo"
    logging.info("\nAnalisando caminho: '%s'", valor)
    logging.info(" - Tipo de caminho: %s", tipo_caminho.capitalize())

    if os.path.exists(valor) and os.path.isfile(valor):
        logging.info(" - Status: Válido (arquivo existente)")
        return f"O valor é um caminho {tipo_caminho} válido para um arquivo: '{valor}'."
    if os.path.exists(valor) and os.path.isdir(valor):
        logging.info(" - Status: Válido (pasta existente)")
        return f"O valor é um caminho {tipo_caminho} válido para uma pasta: '{valor}'."
    logging.info(" - Status: Inválido (não existe)")
    return f"O valor é um caminho {tipo_caminho} inválido: '{valor}'. Não existe."


def analisar_lista(lista: List[Union[str, None]]) -> List[str]:
    """Analisa cada item da lista e retorna os resultados das validações."""
    resultados = []
    for item in lista:
        if item is None or (isinstance(item, str) and item.strip() == ""):
            msg = f"O valor '{item}' é inválido."
            resultados.append(msg)
            logging.info("\n%s", msg)
        elif isinstance(item, str):
            if invalid_message := validar_string(item):
                resultados.append(invalid_message)
                logging.info("\n%s", invalid_message)
            else:
                resultados.append(validar_caminho(item))
        else:
            msg = f"O valor '{item}' (tipo: {type(item).__name__}) é inválido."
            resultados.append(msg)
            logging.info("\n%s", msg)
    return resultados


def analisar_caminho(dados: Dict[str, Union[str, List[Union[str, None]], None]]) -> List[str]:
    """Analisador de caminhos baseado em dicionário."""
    resultados = []

    for key, valor in dados.items():
        logging.info("\n--- Analisando chave: '%s' ---", key)
        if isinstance(valor, list):
            resultados.extend(analisar_lista(valor))
        elif invalid_message := validar_string(valor):
            resultados.append(invalid_message)
            logging.info("\n%s", invalid_message)
        else:
            resultados.append(validar_caminho(valor))

    return resultados


# Exemplo de uso
entradas = [
    {"testar_caminho": [
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html",
        "../../../../Downloads/Chrome/favoritos_17_09_2024.html"]},
    {"testar_caminho": [
        "/home/pedro-pm-dias/Downloads/Chrome/",
        "../../../../Downloads/Chrome/"]}
]

for entrada in entradas:
    resultados = analisar_caminho(entrada)
    for resultado in resultados:
        logging.info("\nResultado da análise: %s\n", resultado)

# {"testar_caminho": None},
# {"testar_caminho": ""},
# {"testar_caminho": "   "},
# {"testar_caminho": "Olá, mundo!"},
# {"testar_caminho": 42},
# {"testar_caminho": 3.14},
# {"testar_caminho": [1, 2, 3]},
# {"testar_caminho": {"chave1": "valor1"}},
# {"testar_caminho": True},
# {"testar_caminho": False},
# {"testar_caminho": [None, True, 0, 12.34]},
# {"testar_caminho": ["string1", "string2"]},
# {"testar_caminho": ["   ", "valido"]},
# {"testar_caminho": "/usr/local/bin"},
# {"testar_caminho": "/home/user/docs"},
# {"testar_caminho": "./temp"},
# {"testar_caminho": "../images/logo.png"},
# {"testar_caminho": "/invalid/path/too/deep/"},
# {"testar_caminho": "invalid/path/?"},
# {"testar_caminho": "/nonexistent_folder/"},
# {"testar_caminho": "/etc/./hosts"},
# {"testar_caminho": "/../var/log/syslog"},
# {"testar_caminho": ["/home/user/docs", "/etc"]},
# {"testar_caminho": "./temp"},
# {"testar_caminho": "../images/logo.png"},
# {"testar_caminho": "/invalid/path/too/deep/"},
# {"testar_caminho": "invalid/path/?"},
# {"testar_caminho": "/nonexistent_folder/"},
# {"testar_caminho": "/etc/./hosts"},
# {"testar_caminho": "/../var/log/syslog"},
# {"testar_caminho": ["/home/user/docs", "/etc"]},
# {"testar_caminho": ["", "/usr/bin"]},
# {"testar_caminho": ["valid/path", "invalid/path/?"]}
