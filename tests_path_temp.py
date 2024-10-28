# %%
import os
import logging

# %%
# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(message)s')


# %%
def validar_string(valor):
    """Valida se o valor é uma string e retorna a mensagem apropriada."""
    if valor is None:
        return "O valor é None (null)."
    elif isinstance(valor, str):
        if valor.strip() == "":
            return "O valor é uma string vazia."
        elif any(char in valor for char in ['?', '*', ':', '<', '>', '|']):
            return f"O valor é um caminho inválido: '{valor}'. Contém caracteres inválidos."
        else:
            return None
    return f"O valor é do tipo {type(valor).__name__}, que não é suportado para análise."


# %%
def validar_caminho(valor):
    """Valida se o valor é um caminho absoluto ou relativo e retorna a mensagem apropriada."""
    if os.path.isabs(valor):
        return f"O valor é um caminho absoluto {'válido' if os.path.exists(valor) else 'inválido'}: '{valor}'{'' if os.path.exists(valor) else '. Não existe'}."
    return f"O valor é um caminho relativo {'válido' if os.path.exists(valor) else 'inválido'}: '{valor}'{'' if os.path.exists(valor) else '. Não existe'}."


# %%
def analisar_lista(lista):
    """Analisa cada item da lista e retorna os resultados das validações."""
    resultados = []
    for item in lista:
        item_tipo = type(item).__name__
        if item is None or (isinstance(item, str) and item.strip() == ""):
            resultados.append(f"O valor '{item}' é inválido.")
        elif isinstance(item, str):
            if invalid_message := validar_string(item):
                resultados.append(invalid_message)
            else:
                resultados.append(validar_caminho(item))
        else:
            resultados.append(f"O valor '{item}' (tipo: {item_tipo}) é inválido.")
    return resultados


# %%
def analisar_caminho(dados):
    """Analisador de caminhos baseado em dicionário."""
    resultados = []

    for key, valor in dados.items():
        print(f"Analisando chave: {key}, valor: {valor}")
        if isinstance(valor, list):
            resultados.extend(analisar_lista(valor))
        elif invalid_message := validar_string(valor):
            resultados.append(invalid_message)
        else:
            resultados.append(validar_caminho(valor))

    return resultados


# %%
# Exemplo de uso
entradas = [
    {"testar_caminho": None},
    {"testar_caminho": ""},
    {"testar_caminho": "   "},
    {"testar_caminho": "Olá, mundo!"},
    {"testar_caminho": 42},
    {"testar_caminho": 3.14},
    {"testar_caminho": [1, 2, 3]},
    {"testar_caminho": {"chave1": "valor1"}},
    {"testar_caminho": True},
    {"testar_caminho": False},
    {"testar_caminho": [None, True, 0, 12.34]},
    {"testar_caminho": ["string1", "string2"]},
    {"testar_caminho": ["   ", "valido"]},
    {"testar_caminho": "/usr/local/bin"},
    {"testar_caminho": "home/user/docs"},
    {"testar_caminho": "./temp"},
    {"testar_caminho": "../images/logo.png"},
    {"testar_caminho": "/invalid/path/too/deep/"},
    {"testar_caminho": "invalid/path/?"},
    {"testar_caminho": "/nonexistent_folder/"},
    {"testar_caminho": "/etc/./hosts"},
    {"testar_caminho": "/../var/log/syslog"},
    {"testar_caminho": ["home/user/docs", "/etc"]},
    {"testar_caminho": ["", "/usr/bin"]},
    {"testar_caminho": ["valid/path", "invalid/path/?"]}
]

# %%
for entrada in entradas:
    resultados = analisar_caminho(entrada)
    for resultado in resultados:
        logging.info(resultado)
# %%
