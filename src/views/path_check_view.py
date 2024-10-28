# src/views/path_check_view.py

"""
Módulo de verificação de caminhos usando FastAPI.
Este módulo define as rotas e lógica para verificar a validade de caminhos fornecidos.
"""

from pathlib import Path  # Import padrão
from fastapi import APIRouter, HTTPException  # Import de terceiros
from pydantic import BaseModel, Field

router = APIRouter()


class RequisicaoVerificacaoCaminho(BaseModel):
    """
    Modelo Pydantic para validação da entrada de caminho.
    """

    caminho: str = Field(
        ..., regex=r'^(?:/[^/ ]*)+/?$', description="Caminho absoluto Unix válido."
    )


def verificar_caminho_logica(caminho: str) -> dict:
    """
    Função que aplica a lógica de verificação de caminho.

    Args:
        caminho (str): O caminho a ser verificado.

    Returns:
        dict: Informações sobre o caminho, incluindo se é absoluto, se é um arquivo,
            a extensão, o nome e o caminho final.
    """
    caminho_absoluto = Path("/home/pedro-pm-dias").joinpath(caminho).resolve()

    if not caminho_absoluto.exists():
        raise HTTPException(status_code=404, detail="Caminho não encontrado")

    return {
        "absoluto": caminho_absoluto.is_absolute(),
        "eh_arquivo": caminho_absoluto.is_file(),
        "extensao": caminho_absoluto.suffix if caminho_absoluto.is_file() else None,
        "nome": caminho_absoluto.name,
        "caminho_final": str(caminho_absoluto),
    }


@router.post("/verificacao-caminho")
async def verificar_caminho(requisicao: RequisicaoVerificacaoCaminho):
    """
    Endpoint para verificar um caminho.

    Args:
        requisicao (RequisicaoVerificacaoCaminho): Requisição contendo o caminho a ser verificado.

    Returns:
        dict: Resultado da verificação do caminho.
    """
    return verificar_caminho_logica(requisicao.caminho)
