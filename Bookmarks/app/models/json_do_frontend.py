# app/models/json_do_frontend.py

"""
Este módulo fornece uma função para formatar
uma lista de caminhos em um formato JSON adequado.
"""

import json
import re
from typing import Dict, List


def validar_regex_caminho(caminho: str) -> bool:
    """
    Verifica se o caminho atende ao padrão definido pela regex.
    """
    padrao_caminho = re.compile(
        r"""
        ^(
            (/[\w\s.-]+)+/?$          # Caminhos absolutos Unix/Linux/MacOS
            |
            [a-zA-Z]:\\([\w\s.-]+\\?)+$  # Caminhos absolutos Windows
            |
            ([\w\s.-]+(/|\\)?)+$         # Caminhos relativos
            |
            \\\\[\w\s.-]+(\\[\w\s.-]+)+$ # Caminhos UNC (rede)
        )$
        """,
        re.VERBOSE,
    )
    return bool(padrao_caminho.match(caminho))


def validar_caminho(caminho: str) -> bool:
    """
    Verifica condições adicionais para validar o caminho:
    - Não deve conter caracteres inválidos.
    - Deve ser maior que 1 caractere.
    """
    caracteres_invalidos = r'[<>:"|?*\x00-\x1f]'
    if re.search(caracteres_invalidos, caminho):
        return False
    if not caminho.strip() or len(caminho.strip()) < 2:
        return False
    return True


def filtrar_caminhos_validos(caminhos: List[str]) -> List[str]:
    """
    Filtra a lista de caminhos, aplicando as validações.
    """
    caminhos_validados = []
    for c in caminhos:
        caminho_strip = c.strip()
        if isinstance(c, str) and caminho_strip:
            if validar_regex_caminho(caminho_strip) and validar_caminho(caminho_strip):
                caminhos_validados.append(caminho_strip)
    return caminhos_validados


def formatar_caminhos_para_json(caminhos: List[str]) -> str:
    """
    Formata uma lista de caminhos válidos em um JSON adequado.
    """
    caminhos_validados = filtrar_caminhos_validos(caminhos)
    dict_caminhos: Dict[str, List[str]] = {"jsonEntrada": caminhos_validados}
    return json.dumps(dict_caminhos, indent=4, ensure_ascii=False)


# Exemplo de caminhos fornecidos pelo frontend
caminhos_frontend: List[str] = [
    "  /home/pedro-pm-dias/Documentos/Photos.zip",
    "/home/pedro-pm-dias/Documentos/Photos.txt  ",
    "  /home/pedro-pm-dias/Documentos/K19  ",
    "/home/pedro-pm-dias/Documentos/nao_existe",
    "  ../Documentos/",
    "../Downloads/",
    "../Documents/",
    "C:\\Users\\Pedro\\Documents\\file.txt",
    "C:/Users/Pedro/Documents/file.txt",
    "\\\\NetworkDrive\\Shared\\file.txt",
    "\\\\Server\\Share\\folder\\",
    "/var/log/syslog/",
    "C:\\Windows\\System32\\cmd.exe",
    "./relative/path/to/file",
    "invalid_path_@!",
    "",
    "C:\\Users\\Invalid|Char",
    "/invalid/path<>",
    "C:\\Another\\..\\Invalid\\Path",
    "relative\\path\\..\\invalid",
]

# Formatação de caminhos em JSON
json_frontend: str = formatar_caminhos_para_json(caminhos_frontend)
print(json_frontend)
