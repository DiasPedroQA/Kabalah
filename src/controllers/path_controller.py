# pylint: disable=C
# src/controllers/path_controller.py

# from flask import Flask, jsonify, request
# from services.path_service import processar_caminhos

# app = Flask(__name__)


# @app.route('/processar', methods=['POST'])
# def processar():
#     dados = request.get_json()
#     caminhos = dados.get("caminhos", [])

#     # Chama o serviço de processamento de caminhos
#     resultados = processar_caminhos(caminhos)
#     return jsonify(resultados)


# def inicializar_controller():
#     app.run(debug=True)


# if __name__ == "__main__":
#     inicializar_controller()


# class GerenciadorCaminhos:
#     def __init__(self, caminho: str):
#         self.caminho = pathlib.Path(caminho)
#         self.logger = CustomLogger(__name__)
#         self.model = self._inicializar_modelo()
#         self.arquivos_html: List[FilePathModel] = []

#     def _inicializar_modelo(self) -> Union[FilePathModel, FolderPathModel]:
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
#         Retorna o tipo do caminho inicializado (arquivo ou pasta).

#         Returns:
#             str: "Pasta" se for uma pasta, "Arquivo" se for um arquivo,
#             ou "Inválido" se não for nenhum.
#         if isinstance(self.model, FolderPathModel):
#             return "Pasta"
#         elif isinstance(self.model, FilePathModel):
#             return "Arquivo"
#         return "Inválido"

#     def filtrar_arquivos_html(self) -> List[FilePathModel]:
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
#         return self.arquivos_html


# class HTMLParser:
#     def __init__(self, file_path: str):
#         self.file_path = pathlib.Path(file_path)
#         self.logger = CustomLogger(__name__)

#     def process_html_file(self) -> Dict[str, Any]:
#         soup = self._load_html()
#         return self._extract_lists(soup)

#     def _load_html(self) -> BeautifulSoup:
#         with self.file_path.open('r', encoding='utf-8') as file:
#             content = file.read()
#         return BeautifulSoup(content, 'html.parser')

#     def _extract_lists(self, soup: BeautifulSoup) -> Dict[str, Any]:
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
