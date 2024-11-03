# pylint: disable=C
# tests/test_main.py

from main import processar_caminhos


# Função de teste para uma pasta válida
def test_processar_pasta():
    folder_path = "/home/pedro-pm-dias/Downloads/Chrome"  # Substitua por um caminho válido
    caminhos = [folder_path]

    # Chamar a função
    resultados = processar_caminhos(caminhos)
    print("\nTeste com folder_path", caminhos)

    # Verificações
    assert len(resultados) == 1  # Deve ter um resultado para a pasta
    # assert resultados[0]["tipo"] == "pasta"
    assert resultados[0]["conteudo"]["caminho"] == folder_path


# Função de teste para um arquivo válido
def test_processar_arquivo():
    file_path = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_17_09_2024.html"  # Substitua por um caminho válido
    caminhos = [file_path]

    # Chamar a função
    resultados = processar_caminhos(caminhos)
    print("\nTeste com file_path", caminhos)

    # Verificações
    assert len(resultados) == 1  # Deve ter um resultado para o arquivo
    # assert resultados[0]["tipo"] == "arquivo"
    assert resultados[0]["conteudo"]["caminho"] == file_path


# Função de teste para um caminho inválido
def test_processar_caminho_invalido():
    invalid_path = "/invalid/path"  # Caminho inválido
    caminhos = [invalid_path]

    # Chamar a função
    resultados = processar_caminhos(caminhos)

    # Verificações
    assert len(resultados) == 1  # Deve ter um resultado para o caminho inválido
    assert "erro" in resultados[0]
    assert resultados[0]["erro"] == f"Caminho inválido ou inexistente: {invalid_path}"
