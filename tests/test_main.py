# pylint: disable=C
# tests/test_main.py


from src.main import processar_caminhos


# Função de teste principal
def test_processar_caminhos():
    # Caminhos que você deve garantir que existam no seu sistema
    folder_path = "/home/pedro-pm-dias/Downloads/folder1"  # Substitua por um caminho válido
    file_path = "/home/pedro-pm-dias/Downloads/file1.txt"  # Substitua por um caminho válido
    invalid_path = "/invalid/path"  # Caminho inválido

    # Testando caminhos válidos
    caminhos = [folder_path, file_path, invalid_path]

    # Chamar a função
    resultados = processar_caminhos(caminhos)

    # Verificações
    assert len(resultados) == 3  # Deve ter um resultado para cada caminho

    # Verificar o resultado para a pasta
    assert resultados[0]["tipo"] == "diretório"
    assert resultados[0]["conteudo"]["caminho"] == folder_path

    # Verificar o resultado para o arquivo
    assert resultados[1]["tipo"] == "arquivo"
    assert resultados[1]["conteudo"]["caminho"] == file_path

    # Verificar o resultado para caminho inválido
    assert "erro" in resultados[2]
    assert resultados[2]["erro"] == f"Caminho inválido ou inexistente: {invalid_path}"
