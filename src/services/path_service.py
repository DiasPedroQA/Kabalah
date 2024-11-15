# src/services/path_service.py

# """
# Este módulo contém funções para processar e gerenciar caminhos de arquivos e pastas.

# As principais funcionalidades incluem:
# - Processar caminhos fornecidos e identificar se são arquivos ou pastas.
# - Filtrar arquivos HTML em pastas específicas.
# """

# from src.models.path_models import PathManager


# def processar_caminhos(caminhos):
#     """
#     Processa uma lista de caminhos, identificando o tipo de cada caminho (arquivo ou pasta).

#     Para as pastas, filtra os arquivos HTML presentes e retorna os resultados organizados.
#     Para os arquivos, retorna o caminho como está.

#     Args:
#         caminhos (list): Lista de caminhos (arquivos ou pastas) a serem processados.

#     Returns:
#         list: Lista de resultados, incluindo erros ou caminhos processados.
#     """
#     resultados = []

#     # Processa cada caminho usando o GerenciadorCaminhos
#     for caminho in caminhos:
#         try:
#             # Usando a lógica da classe GerenciadorCaminhos para identificar o tipo
#             gerenciador = GerenciadorCaminhos(caminho)
#             tipo = gerenciador.tipo_caminho()
#             if tipo == "Pasta":
#                 # Filtra arquivos .html em uma pasta
#                 arquivos_html = gerenciador.filtrar_arquivos_html()
#                 resultados.append(
#                     {"tipo": tipo, "conteudo": [arq.caminho for arq in arquivos_html]}
#                 )
#             else:
#                 resultados.append({"tipo": tipo, "conteudo": caminho})
#         except ValueError as e:
#             resultados.append({"erro": str(e)})

#     return resultados
