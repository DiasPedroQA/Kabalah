# pylint: disable=C

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.controllers import exemplo_controller, path_check_controller

# Configuração de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Meu Projeto API",
    description="Esta API permite realizar verificações de caminhos de arquivos e outros exemplos.",  # noqa: E501
    version="1.0.0"
)

# Configuração de CORS
origins = [
    "http://localhost:3000",  # Permitir acesso de um front-end local
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
app.include_router(exemplo_controller.router)
app.include_router(path_check_controller.router)


# Logging de Inicialização
@app.on_event("startup")
async def startup_event():
    logger.info("A aplicação FastAPI foi iniciada.")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("A aplicação FastAPI está sendo encerrada.")
