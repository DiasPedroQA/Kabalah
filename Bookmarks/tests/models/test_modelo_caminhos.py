# pylint: disable=C, W
# Bookmarks/tests/models/test_modelo_caminhos.py

# Testes

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.modelo_caminhos import PathFinder

caminhos_teste = {
    "caminho_arquivo_valido": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html",
    "caminho_arquivo_invalido": "/home/pedro-pm-dias/Downloads/Invalido.txt/",
    "caminho_pasta_valida": "/home/pedro-pm-dias/Downloads/Chrome/",
    "caminho_pasta_invalida": "/home/pedro-pm-dias/Downloads/Invalid/",
}


# Teste 1: Caminho de arquivo válido
def test_caminho_arquivo_valido():
    localizador = PathFinder(caminhos_teste["caminho_arquivo_valido"])
    arquivo_valido = localizador.analisar_caminhos_com_regex()
    arquivo_json = json.loads(arquivo_valido, indent=4, ensure_ascii=False)
    assert arquivo_json.get("statusAnalise", {}).get("natureza") == "ARQUIVO"
    assert arquivo_json.get("statusAnalise", {}).get("infos", {}).get(
        "estrutura", {}).get("nome_pasta") == "favoritos_17_09_2024"
    assert arquivo_json.get("statusAnalise", {}).get("infos", {}).get(
        "estrutura", {}).get("pastaMae") == "/home/pedro-pm-dias/Downloads/Chrome"
    assert arquivo_json.get("statusAnalise", {}).get("infos", {}).get(
        "estatisticas", {}).get("tamanho", {}).get("tamanho_em_kB") == 4.0
    assert arquivo_json.get("statusAnalise", {}).get("infos", {}).get(
        "estatisticas", {}).get("dataCriacao") == "29/09/2024 05:30:32"
    assert arquivo_json.get("statusAnalise", {}).get("infos", {}).get(
        "estatisticas", {}).get("ultimaModificacao") == "17/09/2024 03:43:43"
    assert arquivo_json.get("statusAnalise", {}).get("infos", {}).get(
        "subitens", {}) == {}
    assert arquivo_json.get("statusAnalise", {}).get("tipo") == "sucesso"
    assert arquivo_json.get("statusAnalise", {}).get("mensagem") == "Arquivo analisado com sucesso"
    assert arquivo_json.get("statusAnalise", {}).get(
        "caminhoEntrada"
    ) == "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html"


# caminhosTeste = PathFinder(caminhos)
# json_resultado = caminhosTeste.analisar_caminhos_com_regex()
# print(json_resultado)


'''
[
    {
        "caminhoEntrada": "../../../../Downloads/Chrome/",
        "statusAnalise": {
            "natureza": "PASTA",
            "infos": {
                "estrutura": {
                    "nome_pasta": "Chrome",
                    "pastaMae": "../../../../Downloads"
                },
                "estatisticas": {
                    "tamanho": {
                        "tamanho_em_kB": 4.0
                    },
                    "dataCriacao": "29/09/2024 05:34:07",
                    "ultimaModificacao": "29/09/2024 05:34:07"
                },
                "subitens": [
                    "favoritos_17_09_2024.html",
                    "Teste"
                ]
            }
        }
    },
    {
        "caminhoEntrada": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html",
        "statusAnalise": {
            "natureza": "ARQUIVO",
            "infos": {
                "estrutura": {
                    "nome_arquivo": "favoritos_17_09_2024.html",
                    "pastaMae": "/home/pedro-pm-dias/Downloads/Chrome"
                },
                "estatisticas": {
                    "tamanho": {
                        "tamanho_em_kB": 952.78
                    },
                    "dataCriacao": "29/09/2024 05:30:32",
                    "ultimaModificacao": "17/09/2024 03:43:43"
                }
            }
        }
    },
    {
        "caminhoEntrada": "../../../../../../../../../../../Downloads/Chrome/Teste/histórico.html",
        "statusAnalise": {
            "tipo": "erro",
            "mensagem": "Caminho não encontrado"
        }
    },
    {
        "caminhoEntrada": "/home/pedro-pm-dias/Downloads/Invalid/",
        "statusAnalise": {
            "tipo": "erro",
            "mensagem": "Caminho não encontrado"
        }
    },
    {
        "caminhoEntrada": "../../../../Downloads/Chrome/Teste/Histórico.html",
        "statusAnalise": {
            "natureza": "ARQUIVO",
            "infos": {
                "estrutura": {
                    "nome_arquivo": "Histórico.html",
                    "pastaMae": "../../../../Downloads/Chrome/Teste"
                },
                "estatisticas": {
                    "tamanho": {
                        "tamanho_em_kB": 1.29
                    },
                    "dataCriacao": "29/09/2024 05:34:07",
                    "ultimaModificacao": "28/09/2024 20:07:55"
                }
            }
        }
    }
]
'''
