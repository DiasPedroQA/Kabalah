# pylint: disable=C
# tests/views/test_path_view.py

# from src.views.path_view import transformar_dados


# def test_transformar_dados_pasta():
#     dados = {
#         "caminho": "/home/pedro-pm-dias/Downloads/folder1",
#         "itens": ["file1.txt", "file2.txt"],
#     }
#     tipo = "pasta"

#     expected_result = {
#         "tipo": "pasta",
#         "conteudo": dados,
#         "mensagem": "Processamento completo para a pasta: /home/pedro-pm-dias/Downloads/folder1",
#     }

#     result = transformar_dados(dados, tipo)
#     assert result == expected_result


# def test_transformar_dados_arquivo():
#     dados = {
#         "caminho": "/home/pedro-pm-dias/Downloads/file1.txt",
#         "conteudo": "Conteúdo do arquivo de exemplo",
#     }
#     tipo = "arquivo"

#     expected_result = {
#         "tipo": "arquivo", "conteudo": dados,
# "mensagem": "Conteúdo do arquivo /home/pedro-pm-dias/Downloads/file1.txt processado com sucesso",
#     }

#     result = transformar_dados(dados, tipo)
#     assert result == expected_result


# def test_transformar_dados_tipo_desconhecido():
#     dados = {"caminho": "/home/pedro-pm-dias/Downloads/unknown"}
#     tipo = "desconhecido"

#     expected_result = {"erro": "Tipo desconhecido"}

#     result = transformar_dados(dados, tipo)
#     assert result == expected_result
