# src/models/path_models.py

from pathlib import Path
import json


class EstruturaResposta:
    """
    Classe responsável por gerar a estrutura padronizada de respostas para a análise de caminhos.
    """

    @staticmethod
    def gerar_resposta(caminho, sucesso, dados=None, mensagem=None):
        """
        Gera uma resposta padronizada no formato de dicionário.

        Parâmetros:
        caminho (str): Caminho do arquivo ou pasta.
        sucesso (bool): Indica se a operação foi bem-sucedida ou não.
        dados (dict, opcional): Dados adicionais a serem incluídos na resposta (caso haja).
        mensagem (str, opcional): Mensagem de erro ou sucesso.

        Retorna:
        dict: Estrutura padronizada de resposta.
        """
        return {
            "caminho": str(caminho),
            "resultado": "sucesso" if sucesso else "erro",
            "dados": dados,
            "mensagem": mensagem,
        }


class CaminhoBase:
    """
    Classe base abstrata para representar um caminho e fornecer métodos comuns.

    Métodos:
    __init__(caminho): Inicializa a classe com o caminho fornecido e verifica se o caminho existe.
    analisar(): Método abstrato que deve ser implementado nas subclasses.
    """

    def __init__(self, caminho):
        """
        Inicializa a classe com o caminho fornecido.

        Parâmetros:
        caminho (str): Caminho para um arquivo ou pasta.

        Levanta:
        ValueError: Se o caminho não existe.
        """
        self._caminho = Path(caminho)
        if not self._caminho.exists():
            raise ValueError(f"O caminho {caminho} não existe")

    def analisar(self):
        """
        Método abstrato para análise do caminho. Deve ser implementado pelas subclasses.

        Levanta:
        NotImplementedError: Quando não implementado nas subclasses.
        """
        raise NotImplementedError("Método deve ser implementado nas subclasses.")

    def validar_caminho(self):
        """
        Valida se o caminho fornecido existe.

        Levanta:
        ValueError: Se o caminho não existe.
        """
        if not self._caminho.exists():
            raise ValueError(f"O caminho {self._caminho} não existe")


class AnalisadorDeArquivos(CaminhoBase):
    """
    Classe para análise de arquivos específicos. Herda de `CaminhoBase`.

    Métodos:
    analisar(): Realiza a análise de um arquivo,
    coletando informações como tamanho, nome e extensão.
    """

    def analisar(self):
        """
        Analisa o arquivo, coletando informações como nome, tamanho e extensão.

        Retorna:
        dict: Estrutura padronizada com os dados do arquivo, ou uma mensagem de erro.
        """
        try:
            dados = {
                "tipo": "arquivo",
                "tamanho": self._caminho.stat().st_size,
                "nome": self._caminho.name,
                "extensao": self._caminho.suffix,
            }
            return EstruturaResposta.gerar_resposta(self._caminho, sucesso=True, dados=dados)
        except (OSError, IOError) as e:
            return EstruturaResposta.gerar_resposta(
                self._caminho, sucesso=False, mensagem=f"Erro ao acessar arquivo: {e}"
            )


class AnalisadorDePastas(CaminhoBase):
    """
    Classe para análise de pastas. Herda de `CaminhoBase`.

    Métodos:
    analisar(): Realiza a análise de uma pasta, contando arquivos e subpastas.
    """

    def analisar(self):
        """
        Analisa a pasta, contando o número de arquivos e subpastas.

        Retorna:
        dict: Estrutura padronizada com a quantidade de arquivos e pastas, ou uma mensagem de erro.
        """
        try:
            total_arquivos = sum(bool(item.is_file()) for item in self._caminho.iterdir())
            total_pastas = sum(bool(item.is_dir()) for item in self._caminho.iterdir())
            dados = {
                "tipo": "pasta",
                "total_arquivos": total_arquivos,
                "total_pastas": total_pastas,
            }
            return EstruturaResposta.gerar_resposta(self._caminho, sucesso=True, dados=dados)
        except OSError as e:
            return EstruturaResposta.gerar_resposta(
                self._caminho, sucesso=False, mensagem=f"Erro ao acessar pasta: {e}"
            )


class AnalisadorDeCaminhos:
    """
    Classe principal para analisar caminhos de arquivos ou pastas e gerar respostas padronizadas.

    Pode receber uma lista de strings ou uma única string
    representando os caminhos a serem analisados.

    Métodos:
    __init__(caminhos): Inicializa a classe com os caminhos fornecidos.
    analisar(): Analisa todos os caminhos fornecidos, identificando se são arquivos ou pastas.
    procurar_arquivos(pasta=None, extensao=None): Procura arquivos em uma pasta,
    opcionalmente filtrando por extensão.
    """

    def __init__(self, paths):
        """
        Inicializa a classe com os caminhos fornecidos.

        Parâmetros:
        paths (list or str): Lista de caminhos ou um único caminho a ser analisado.
        """
        self.caminhos = paths if isinstance(paths, list) else [paths]

    def analisar(self):
        """
        Analisa cada caminho na lista, verificando se é um arquivo ou uma pasta,
        e retorna um JSON com os resultados.

        Retorna:
        str: Resultado da análise de todos os caminhos fornecidos no formato JSON.
        """
        resultados = []
        for caminho in self.caminhos:
            path = Path(caminho)
            try:
                if path.is_file():
                    analisador_arquivo = AnalisadorDeArquivos(path)
                    resultados.append(analisador_arquivo.analisar())
                elif path.is_dir():
                    analisador_pasta = AnalisadorDePastas(path)
                    resultados.append(analisador_pasta.analisar())
                else:
                    raise ValueError(f"Caminho {caminho} não é um arquivo nem uma pasta")
            except ValueError as e:
                resultados.append(
                    EstruturaResposta.gerar_resposta(caminho, sucesso=False, mensagem=str(e))
                )
        return json.dumps(resultados, indent=4, ensure_ascii=False)

    def procurar_arquivos(self, pasta=None, extensao=None):
        """
        Procura arquivos dentro de uma pasta. Pode filtrar por extensão.

        Parâmetros:
        pasta (str, opcional): Caminho da pasta onde procurar os arquivos.
        Se não fornecido, utiliza o primeiro caminho fornecido na inicialização.
        extensao (str, opcional): Extensão dos arquivos a serem buscados
        (exemplo: ".txt"). Se não fornecido, busca todos os arquivos.

        Retorna:
        str: Resultado da busca por arquivos no formato JSON.
        """
        pasta = pasta or self.caminhos[0]
        path = Path(pasta)

        if not path.is_dir():
            return json.dumps(
                EstruturaResposta.gerar_resposta(
                    pasta, sucesso=False, mensagem="A pasta especificada não existe"
                ),
                indent=4,
                ensure_ascii=False,
            )

        arquivos = [
            {
                "nome": arquivo.name,
                "tamanho": arquivo.stat().st_size,
                "extensao": arquivo.suffix,
                "modificado_em": arquivo.stat().st_mtime,
            }
            for arquivo in path.iterdir()
            if arquivo.is_file() and (extensao is None or arquivo.suffix == extensao)
        ]

        return json.dumps(arquivos, indent=4, ensure_ascii=False)


# Exemplo de uso com docstrings:

# Caminhos a serem analisados
caminhos = [
    "/home/pedro-pm-dias/Downloads/Chrome/",
    "/home/pedro-pm-dias/Downloads/"
]

# Instancia o AnalisadorDeCaminhos com os caminhos fornecidos
analisador = AnalisadorDeCaminhos(caminhos)

# Analisando os caminhos
resultado_analise = analisador.analisar()
print("Resultado da Análise dos Caminhos:")
print(resultado_analise)

# Procurando por arquivos com extensão .html
resultado_busca_html = analisador.procurar_arquivos(extensao=".html")
print("Resultado da Busca por Arquivos .html:")
print(resultado_busca_html)
