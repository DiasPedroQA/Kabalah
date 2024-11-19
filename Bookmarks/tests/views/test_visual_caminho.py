# tests/views/test_visual_caminho.py

from Bookmarks.src.views.visual_caminho import exibir_resultados, filtrar_por_extensao, validar_entradas


class TestVisualCaminho:
    def test_validar_entradas_caminhos_invalidos(self):
        caminhos = [123, "path/to/file", True]
        extensoes = [".txt", ".py"]
        resultado = validar_entradas(caminhos, extensoes)
        assert resultado == "'caminhos' deve ser uma lista de strings."

    def test_validar_entradas_extensoes_invalidas(self):
        caminhos = ["path/to/file"]
        extensoes = [".txt", 123, True]
        resultado = validar_entradas(caminhos, extensoes)
        assert resultado == "'extensoes' deve ser uma lista de strings."

    def test_validar_entradas_validas(self):
        caminhos = ["path/to/file1", "path/to/file2"]
        extensoes = [".txt", ".py"]
        resultado = validar_entradas(caminhos, extensoes)
        assert resultado is None

    def test_filtrar_por_extensao_com_filtro(self):
        arquivos = [
            {"nome": "arquivo1.txt", "extensao": ".txt"},
            {"nome": "arquivo2.py", "extensao": ".py"},
            {"nome": "arquivo3.jpg", "extensao": ".jpg"}
        ]
        extensoes = [".txt", ".py"]
        resultado = filtrar_por_extensao(arquivos, extensoes)
        assert len(resultado) == 2
        assert all(arquivo["extensao"] in extensoes for arquivo in resultado)

    def test_filtrar_por_extensao_sem_filtro(self):
        arquivos = [
            {"nome": "arquivo1.txt", "extensao": ".txt"},
            {"nome": "arquivo2.py", "extensao": ".py"}
        ]
        resultado = filtrar_por_extensao(arquivos, None)
        assert len(resultado) == 2
        assert resultado == arquivos

    def test_exibir_resultados_erro_permissao(self, capsys):
        caminhos = ["/path/sem/permissao"]
        exibir_resultados(caminhos)
        captured = capsys.readouterr()
        assert "Erro ao processar caminhos" in captured.out

    def test_exibir_resultados_caminho_inexistente(self, capsys):
        caminhos = ["/caminho/que/nao/existe"]
        exibir_resultados(caminhos)
        captured = capsys.readouterr()
        assert "Erro ao processar caminhos" in captured.out

    def test_exibir_resultados_json_invalido(self, capsys, mocker):
        caminhos = ["path/valido"]
        mock_controlador = mocker.patch('src.controllers.controle_caminhos.ControladorDeCaminhos')
        mock_controlador.return_value.processar_caminhos.return_value = "json invalido"
        exibir_resultados(caminhos)
        captured = capsys.readouterr()
        assert "Erro ao processar caminhos" in captured.out
