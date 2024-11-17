# pylint: disable=C, E

import unittest
import os
import json
from src.main import app, DIRETORIO_ARQUIVOS  # Import the Flask app


class TestRotaProcessarArquivo(unittest.TestCase):
    def setUp(self):
        """
        Configura o ambiente de teste:
            - Inicializa o cliente de teste do Flask.
            - Garante que o diretório de arquivos existe.
        """
        self.client = app.test_client()
        self.client.testing = True
        os.makedirs(DIRETORIO_ARQUIVOS, exist_ok=True)

    def tearDown(self):
        """
        Limpa o ambiente de teste:
            - Remove os arquivos de teste criados.
        """
        for arquivo in os.listdir(DIRETORIO_ARQUIVOS):
            caminho = os.path.join(DIRETORIO_ARQUIVOS, arquivo)
            os.remove(caminho)

    def criar_arquivo_teste(self, nome_arquivo, conteudo=""):
        """
        Cria um arquivo de teste no diretório de arquivos.

        Args:
            nome_arquivo (str): Nome do arquivo a ser criado.
            conteudo (str): Conteúdo a ser escrito no arquivo.
        """
        with open(
                os.path.join(
                    DIRETORIO_ARQUIVOS,
                    nome_arquivo
                ),
                "w",
                encoding="utf-8") as arquivo:
            arquivo.write(conteudo)

    def test_parametro_ausente(self):
        """
        Testa a rota sem fornecer o parâmetro 'arquivo'.
        """
        resposta = self.client.get('/processar')
        self.assertEqual(resposta.status_code, 400)
        dados = json.loads(resposta.data)
        self.assertEqual(dados["erro"], "O parâmetro 'arquivo' é obrigatório.")

    def test_arquivo_nao_encontrado(self):
        """
        Testa a rota com um arquivo inexistente.
        """
        resposta = self.client.get(
            '/processar?arquivo=arquivo_inexistente.txt'
        )
        self.assertEqual(resposta.status_code, 404)
        dados = json.loads(resposta.data)
        self.assertEqual(
            dados["erro"],
            "Arquivo 'arquivo_inexistente.txt' não encontrado."
        )

    def test_arquivo_encontrado(self):
        """
        Testa a rota com um arquivo existente.
        """
        nome_arquivo = "teste.txt"
        self.criar_arquivo_teste(nome_arquivo, "Conteúdo de teste")

        resposta = self.client.get(f'/processar?arquivo={nome_arquivo}')
        self.assertEqual(resposta.status_code, 200)
        dados = json.loads(resposta.data)
        self.assertEqual(
            dados["mensagem"],
            f"Conteúdo do arquivo '{nome_arquivo}' foi processado com sucesso!"
        )


if __name__ == "__main__":
    unittest.main()
