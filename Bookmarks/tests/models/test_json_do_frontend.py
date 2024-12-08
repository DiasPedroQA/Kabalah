# tests/models/test_json_do_frontend.py
# pylint: disable=C0301

"""
Este módulo contém testes para o módulo json_do_frontend.py.
"""

from app.models.json_do_frontend import (
    filtrar_caminhos_validos,
    formatar_caminhos_para_json,
    validar_regex_caminho,
    validar_caminho,
)


def test_validar_regex_caminho_linux_absolute():
    """
    Testa se a função validar_regex_caminho reconhece caminhos absolutos no Linux.
    """
    assert validar_regex_caminho("/usr/local/bin/python") is True

def test_validar_regex_caminho_windows_absolute():
    """
    Testa se a função validar_regex_caminho reconhece caminhos absolutos no Windows.
    """
    assert validar_regex_caminho("C:\\Program Files\\App\\file.exe") is True

def test_validar_regex_caminho_windows_relative():
    """
    Testa se a função validar_regex_caminho reconhece caminhos relativos no Windows.
    """
    assert validar_regex_caminho("..\\Documents\\file.txt") is True

def test_validar_regex_caminho_unc():
    """
    Testa se a função validar_regex_caminho reconhece caminhos UNC.
    """
    assert validar_regex_caminho("\\\\Server\\Share\\folder\\file.txt") is True

def test_validar_regex_caminho_invalid_format():
    """
    Testa se a função validar_regex_caminho rejeita caminhos inválidos.
    """
    assert validar_regex_caminho("invalid/path?<>*") is False

def test_validar_caminho_too_short():
    """
    Testa se a função validar_caminho rejeita caminhos muito curtos.
    """
    assert validar_caminho("a") is False

def test_validar_caminho_invalid_characters():
    """
    Testa se a função validar_caminho rejeita caminhos com caracteres inválidos.
    """
    assert validar_caminho("invalid_path<>") is False

def test_validar_caminho_valid_case():
    """
    Testa se a função validar_caminho aceita caminhos válidos.
    """
    assert validar_caminho("/valid/path") is True

def test_validar_caminho_with_spaces():
    """
    Testa se a função validar_caminho aceita caminhos com espaços.
    """
    assert validar_caminho("  /valid/path  ") is True

def test_filtrar_caminhos_validos_empty_list():
    """
    Testa se a função filtrar_caminhos_validos retorna
    uma lista vazia quando não há caminhos válidos.
    """
    assert filtrar_caminhos_validos([]) is []

def test_filtrar_caminhos_validos_mixed_cases():
    """
    Testa se a função filtrar_caminhos_validos filtra
    corretamente caminhos válidos e inválidos.
    """
    caminhos_teste = [
        "  /home/user/Documents/Photos.zip",
        "C:\\Users\\Valid\\file.txt",
        "invalid_path<>",
        " ",
        "../relative/path",
    ]
    assert filtrar_caminhos_validos(caminhos_teste) == [
        "/home/user/Documents/Photos.zip",
        "C:\\Users\\Valid\\file.txt",
        "../relative/path",
    ]

def test_filtrar_caminhos_validos_no_valid_paths():
    """
    Testa se a função filtrar_caminhos_validos retorna
    uma lista vazia quando não há caminhos válidos.
    """
    caminhos_teste = ["invalid_path<>", "<>"]
    assert filtrar_caminhos_validos(caminhos_teste) is []

def test_formatar_caminhos_para_json_empty():
    """
    Testa se a função formatar_caminhos_para_json retorna
    um JSON vazio quando não há caminhos válidos.
    """
    assert formatar_caminhos_para_json([]) == '{"jsonEntrada": []}'

def test_formatar_caminhos_para_json_no_valid_paths():
    """
    Testa se a função formatar_caminhos_para_json retorna
    um JSON vazio quando não há caminhos válidos.
    """
    caminhos_teste = ["invalid_path<>", "another_invalid_path"]
    assert formatar_caminhos_para_json(caminhos_teste) == '{"jsonEntrada": []}'

def test_formatar_caminhos_para_json_with_valid_and_invalid_paths():
    """
    Testa se a função formatar_caminhos_para_json formata
    corretamente uma lista de caminhos válidos e inválidos.
    """
    caminhos = ["  /valid/path  ", "invalid_path<>", "C:\\Valid\\Path\\file.txt"]
    expected_json = '{"jsonEntrada": ["/valid/path", "C:\\Valid\\Path\\file.txt"]}'
    assert formatar_caminhos_para_json(caminhos) == expected_json

def test_formatar_caminhos_para_json_large_list():
    """
    Testa se a função formatar_caminhos_para_json formata
    corretamente uma lista grande de caminhos.
    """
    caminhos = [f"/valid/path/{i}" for i in range(100)] + ["invalid<>", "another_invalid"]
    expected_json = '{"jsonEntrada": [' + ", ".join(f'"/valid/path/{i}"' for i in range(100)) + ']}'
    assert formatar_caminhos_para_json(caminhos) == expected_json

def test_each_caminho_in_lista():
    """
    Testa se a função formatar_caminhos_para_json formata
    corretamente cada caminho da lista.
    """
    caminhos_frontend = [
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

    resultados_esperados = [
        True, True, True, True, True, True, True, True, True, True,
        True, True, True, True, False, False, False, False, False, True
    ]

    for caminho, esperado in zip(caminhos_frontend, resultados_esperados):
        assert validar_regex_caminho(caminho) == esperado
