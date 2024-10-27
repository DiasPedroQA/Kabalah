# pylint: disable=C

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
USERNAME = os.getenv("USERNAME")

router = APIRouter()


# Modelo de entrada
class RequisicaoVerificacaoCaminho(BaseModel):
    caminho: str


@router.post("/verificacao-caminho")
async def verificar_caminho(requisicao: RequisicaoVerificacaoCaminho):
    caminho_absoluto = Path(
        f"/home/{USERNAME}"
    ).joinpath(
        requisicao.caminho
    ).resolve()

    # Verifica se o caminho existe
    if not caminho_absoluto.exists():
        raise HTTPException(status_code=404, detail="Caminho não encontrado")

    # Retorno da resposta com verificação de tipo e extensão
    return {
        "absoluto": caminho_absoluto.is_absolute(),
        "eh_arquivo": caminho_absoluto.is_file(),
        "extensao": caminho_absoluto.suffix if caminho_absoluto.is_file() else None,  # noqa: E501
        "nome": caminho_absoluto.name,
        "caminho_final": str(caminho_absoluto)
    }
