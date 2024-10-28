# src/main.py

"""
Módulo principal da aplicação FastAPI.
Este módulo configura e executa a API que verifica caminhos
de arquivos e pastas.
"""

import logging
from contextlib import asynccontextmanager  # Import padrão
from fastapi import FastAPI  # Import de terceiros
from fastapi.middleware.cors import CORSMiddleware  # Import de terceiros
from src.controllers.path_check_controller import router  # Importando router diretamente
from src.controllers.path_check_controller import (
    analisar_caminho,
)  # Importando a função analisar_caminho

# Configuração de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan():
    """
    Gerenciador de contexto para o ciclo de vida da aplicação FastAPI.
    Registra informações quando a aplicação é iniciada e encerrada.
    """
    logger.info("A aplicação FastAPI foi iniciada.")
    yield
    logger.info("A aplicação FastAPI está sendo encerrada.")


async def main():
    """
    Função principal que testa a lógica de verificação de caminhos.
    Utiliza entradas de exemplo para demonstrar a funcionalidade.
    """
    # Exemplo de uso com diferentes entradas
    entradas = [
        {"testar_caminho": "/path/to/file.txt"},
        {"testar_caminho": ["/invalid/?path", "/valid/path/to/dir"]},
    ]

    for entrada in entradas:
        resultados = await analisar_caminho(entrada)  # Certifique-se de que essa função existe
        if isinstance(resultados, list):
            for resultado in resultados:
                print("\nResultado da análise:", resultado)
        else:
            print("\nResultado da análise:", resultados)


if __name__ == "__main__":
    main()

# Nome original 'app' do aplicativo FastAPI
app = FastAPI(
    title="Meu Projeto API",
    description="Esta API verifica caminhos de arquivos e pastas.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuração de CORS
origins = [
    "http://localhost:8000",  # Permitir acesso de um front-end local
    "https://meu-site.com",  # Adicione aqui o domínio do seu front-end
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclua rotas
app.include_router(router)
