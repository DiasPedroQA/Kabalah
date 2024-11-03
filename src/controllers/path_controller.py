# pylint: disable=C
# src/controllers/path_controller.py

from flask import Flask, jsonify, request  # Importar request corretamente
import os
from src.models.path_models import processar_pasta, processar_arquivo  # Corrigindo importação
from src.views.path_view import transformar_dados  # Corrigindo importação

app = Flask(__name__)


@app.route('/processar', methods=['POST'])
def processar_caminhos():
    # Supondo que os caminhos sejam recebidos no corpo da requisição como JSON
    caminhos = request.json.get('caminhos', [])  # Correção aqui
    resultados = []

    for caminho in caminhos:
        if os.path.isdir(caminho):
            dados = processar_pasta(caminho)
            resultado = transformar_dados(dados, "pasta")
            resultados.append(resultado)
        elif os.path.isfile(caminho):
            dados = processar_arquivo(caminho)
            resultado = transformar_dados(dados, "arquivo")
            resultados.append(resultado)
        else:
            resultados.append({"erro": f"Caminho inválido ou inexistente: {caminho}"})

    return jsonify(resultados)  # Retorna todos os resultados como JSON


def inicializar_controller():
    app.run(debug=True)


# Para rodar a aplicação diretamente
if __name__ == "__main__":
    inicializar_controller()


# class GerenciadorCaminhos:
#     """
#     Classe para gerenciar a filtragem de arquivos HTML e manipulação de caminhos.

#     Esta classe permite inicializar um caminho como arquivo ou pasta, identificar o tipo de caminho,
#     e filtrar arquivos com extensão .html. Os arquivos HTML filtrados são armazenados para uso
#     posterior.

#     Atributos:
#         caminho (Path): Caminho do arquivo ou pasta a ser gerenciado.
#         logger (CustomLogger): Logger personalizado para registrar mensagens do GerenciadorCaminhos.
#         model (Union[FilePathModel, FolderPathModel]): Modelo de caminho inicializado.
#         arquivos_html (List[FilePathModel]): Lista de arquivos HTML filtrados.
#     """

#     def __init__(self, caminho: str):
#         """
#         Inicializa o GerenciadorCaminhos com o caminho especificado.

#         Args:
#             caminho (str): O caminho do arquivo ou pasta a ser gerenciado.
#         """
#         self.caminho = pathlib.Path(caminho)
#         self.logger = CustomLogger(__name__)
#         self.model = self._inicializar_modelo()
#         self.arquivos_html: List[FilePathModel] = []

#     def _inicializar_modelo(self) -> Union[FilePathModel, FolderPathModel]:
#         """
#         Inicializa o modelo de arquivo ou pasta com base no caminho especificado.

#         Returns:
#             Union[FilePathModel, FolderPathModel]: Instância do modelo de caminho.

#         Raises:
#             ValueError: Se o caminho não for um arquivo nem uma pasta.
#         """
#         if self.caminho.is_dir():
#             self.logger.info(f"Inicializado como pasta: {self.caminho}")
#             return FolderPathModel(str(self.caminho))
#         if self.caminho.is_file():
#             self.logger.info(f"Inicializado como arquivo: {self.caminho}")
#             return FilePathModel(str(self.caminho))

#         error_message = "Caminho inválido: não é um arquivo nem uma pasta."
#         self.logger.error(error_message)
#         raise ValueError(error_message)

#     def tipo_caminho(self) -> str:
#         """
#         Retorna o tipo do caminho inicializado (arquivo ou pasta).

#         Returns:
#             str: "Pasta" se for uma pasta, "Arquivo" se for um arquivo,
#             ou "Inválido" se não for nenhum.
#         """
#         if isinstance(self.model, FolderPathModel):
#             return "Pasta"
#         elif isinstance(self.model, FilePathModel):
#             return "Arquivo"
#         return "Inválido"

#     def filtrar_arquivos_html(self) -> List[FilePathModel]:
#         """
#         Filtra e retorna uma lista de arquivos `.html` no caminho especificado.

#         Returns:
#             List[FilePathModel]: Lista de objetos `FilePathModel` representando arquivos `.html`.
#         """
#         if isinstance(self.model, FolderPathModel):
#             self.arquivos_html = [
#                 item
#                 for item in self.model.list_contents()
#                 if isinstance(item, FilePathModel) and item.get_file_extension() == '.html'
#             ]
#             self.logger.info(
#                 f"{len(self.arquivos_html)} arquivos .html encontrados na pasta: {self.caminho}"
#             )
#             return self.arquivos_html
#         if (
#             isinstance(self.model, FilePathModel)
#             and self.model.get_file_extension() == '.html'
#         ):
#             self.logger.info(f"Arquivo .html único encontrado: {self.caminho}")
#             self.arquivos_html = [self.model]
#             return self.arquivos_html

#         self.logger.warning("Nenhum arquivo .html encontrado.")
#         return []

#     def listar_arquivos_html(self) -> List[FilePathModel]:
#         """
#         Retorna a lista de arquivos HTML filtrados.

#         Returns:
#             List[FilePathModel]: Lista de objetos `FilePathModel`
#             representando arquivos `.html` filtrados.
#         """
#         return self.arquivos_html


# class HTMLParser:
#     """
#     Classe para parseamento de arquivos HTML e geração de PDFs
#     com listas de links organizadas por título.

#     Esta classe permite carregar e processar arquivos HTML para
#     extrair listas de links agrupadas
#     por títulos. Também fornece um método para gerar um arquivo
#     PDF formatado com as listas extraídas.

#     Atributos:
#         file_path (Path): Caminho do arquivo HTML a ser processado.
#         logger (CustomLogger): Logger personalizado para registrar mensagens do HTMLParser.
#     """

#     def __init__(self, file_path: str):
#         """
#         Inicializa o parser com o caminho do arquivo HTML.

#         Args:
#             file_path (str): Caminho do arquivo HTML.
#         """
#         self.file_path = pathlib.Path(file_path)
#         self.logger = CustomLogger(__name__)

#     def process_html_file(self) -> Dict[str, Any]:
#         """
#         Processa o arquivo HTML e extrai listas de links agrupadas por título.

#         Returns:
#             Dict[str, Any]: Dicionário com listas de links agrupadas por títulos numerados.
#         """
#         soup = self._load_html()
#         return self._extract_lists(soup)

#     def _load_html(self) -> BeautifulSoup:
#         """
#         Carrega o conteúdo HTML do arquivo especificado e retorna um objeto BeautifulSoup.

#         Returns:
#             BeautifulSoup: Objeto BeautifulSoup do conteúdo HTML.
#         """
#         with self.file_path.open('r', encoding='utf-8') as file:
#             content = file.read()
#         return BeautifulSoup(content, 'html.parser')

#     def _extract_lists(self, soup: BeautifulSoup) -> Dict[str, Any]:
#         """
#         Extrai listas de links e títulos do conteúdo HTML, incluindo listas aninhadas.

#         Args:
#             soup (BeautifulSoup): Objeto BeautifulSoup do conteúdo HTML.

#         Returns:
#             Dict[str, Any]: Dicionário com listas agrupadas por títulos numerados.
#         """
#         lists = {}
#         list_count = 1

#         def process_sublist(parent) -> List[Dict[str, Any]]:
#             items = []
#             for child in parent.find_all(['h3', 'a'], recursive=False):
#                 if child.name == 'h3':
#                     sub_title = f"{child.text.strip()} {list_count}"
#                     lists[sub_title] = {
#                         "title_attributes": {
#                             "text_content": child.text.strip(),
#                             "add_date": child.get('add_date', ''),
#                             "last_modified": child.get('last_modified', ''),
#                         },
#                         "items": process_sublist(child),
#                     }
#                 elif child.name == 'a':
#                     items.append(
#                         {
#                             "text_content": child.text.strip(),
#                             "add_date": child.get('add_date', ''),
#                             "href": child.get('href', ''),
#                         }
#                     )
#             return items

#         for tag in soup.find_all(['h3', 'a']):
#             if tag.name == 'h3':
#                 current_title = f"{tag.text.strip()} {list_count}"
#                 lists[current_title] = {
#                     "title_attributes": {
#                         "text_content": tag.text.strip(),
#                         "add_date": tag.get('add_date', ''),
#                         "last_modified": tag.get('last_modified', ''),
#                     },
#                     "items": process_sublist(tag),
#                 }
#                 list_count += 1

#         return lists

#     def create_pdf(self, json_data: Dict[str, Any]) -> None:
#         """
#         Gera um PDF formatado com as listas do JSON e o salva na mesma pasta do arquivo HTML.

#         Args:
#             json_data (Dict[str, Any]): JSON com listas de links agrupadas por títulos.
#         """
#         pdf_file_path = self.file_path.with_suffix('.pdf')
#         doc = SimpleDocTemplate(str(pdf_file_path), pagesize=A4)
#         story = []

#         title_style = ParagraphStyle(
#             "TitleStyle", fontSize=16, leading=20, spaceAfter=12, textColor=colors.darkblue
#         )
#         item_style = ParagraphStyle("ItemStyle", fontSize=10, leading=12, spaceAfter=8)

#         for title, data in json_data.items():
#             story.append(Paragraph(f"<b>{title}</b>", title_style))
#             title_attr = data.get("title_attributes", {})
#             story.extend(
#                 (
#                     Paragraph(
#                         f"Data de criação: {title_attr.get('add_date', '')}",
#                         item_style,
#                     ),
#                     Paragraph(
#                         f"Última modificação: {title_attr.get('last_modified', '')}",
#                         item_style,
#                     ),
#                     Spacer(1, 12),
#                 )
#             )
#             items = [
#                 ListItem(
#                     Paragraph(
#                         f"{item.get('text_content')} - {item.get('href')} "
#                         f"(Adicionado em: {item.get('add_date')})",
#                         item_style,
#                     )
#                 )
#                 for item in data.get("items", [])
#             ]
#             story.extend((ListFlowable(items, bulletType='bullet'), Spacer(1, 20)))
#         doc.build(story)
#         self.logger.info(f"PDF criado com sucesso: {pdf_file_path}")
