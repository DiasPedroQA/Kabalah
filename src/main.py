# pylint: disable=C

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import path_check_controller

# Configuração de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define o lifespan event handler
@asynccontextmanager
async def lifespan():
    logger.info("A aplicação FastAPI foi iniciada.")
    yield
    logger.info("A aplicação FastAPI está sendo encerrada.")

# Nome original 'app' do aplicativo FastAPI
app = FastAPI(
    title="Meu Projeto API",
    description="Esta API permite realizar verificações de caminhos de arquivos e outros exemplos.",  # noqa: E501
    version="1.0.0",
    lifespan=lifespan
)

# Configuração de CORS
origins = [
    "http://localhost:3000",   # Permitir acesso de um front-end local
    "https://meu-site.com",    # Adicione aqui o domínio do seu front-end
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclua rotas
app.include_router(path_check_controller.router)
