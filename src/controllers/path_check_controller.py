# pylint: disable=C

import os
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
USERNAME = os.getenv("USERNAME")

router = APIRouter()

# Regex para validar caminhos de arquivos e pastas
PATH_REGEX = r'^(?:/[^/ ]*)+/?$'  # Regex para caminhos absolutos em Unix/Linux


# Modelo de entrada
class RequisicaoVerificacaoCaminho(BaseModel):
    caminho: str

    @field_validator("caminho")
    @classmethod
    def validate_caminho(cls, v):
        if not re.match(PATH_REGEX, v):
            raise ValueError("Caminho inválido. Por favor, forneça um caminho absoluto válido.")
        return v


def verificar_caminho_logica(caminho: str) -> dict:
    caminho_absoluto = Path(f"/home/{USERNAME}").joinpath(caminho).resolve()
    print(f"Verificando caminho: {caminho_absoluto}")

    # Verifica se o caminho existe
    if not caminho_absoluto.exists():
        raise HTTPException(status_code=404, detail="Caminho não encontrado")

    # Retorno da resposta com verificação de tipo e extensão
    return {
        "absoluto": caminho_absoluto.is_absolute(),
        "eh_arquivo": caminho_absoluto.is_file(),
        "extensao": caminho_absoluto.suffix if caminho_absoluto.is_file() else None,
        "nome": caminho_absoluto.name,
        "caminho_final": str(caminho_absoluto)
    }


@router.post("/verificacao-caminho")
async def verificar_caminho(requisicao: RequisicaoVerificacaoCaminho):
    return verificar_caminho_logica(requisicao.caminho)
