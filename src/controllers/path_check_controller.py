# pylint: disable=C

from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
from typing import Optional

router = APIRouter()


# Modelo de entrada
class RequisicaoVerificacaoCaminho(BaseModel):
    caminho: str


# Modelo de resposta
class RespostaVerificacaoCaminho(BaseModel):
    absoluto: bool
    eh_arquivo: bool
    nome: str
    extensao: Optional[str]
    caminho_final: str


@router.post("/verificacao-caminho", response_model=RespostaVerificacaoCaminho)
async def verificar_caminho(requisicao: RequisicaoVerificacaoCaminho):
    caminho_original = Path(requisicao.caminho).resolve()  # Resolve o caminho
    tentativas = 0
    caminho_final = caminho_original

    # Verifica se é absoluto
    while not caminho_final.is_absolute() and tentativas < 5:
        tentativas += 1
        caminho_final = Path("..") / caminho_final  # Adiciona ../

    # Se não for absoluto, usa o original
    if not caminho_final.is_absolute():
        caminho_final = caminho_original  # Mantém o original

    # Verifica se é um arquivo
    eh_arquivo = caminho_final.is_file()
    extensao = caminho_final.suffix if eh_arquivo else None

    # Retornando os dados
    return RespostaVerificacaoCaminho(
        absoluto=caminho_final.is_absolute(),
        eh_arquivo=eh_arquivo,
        extensao=extensao,
        nome=caminho_final.name,
        caminho_final=str(caminho_final)  # Convertendo para string
    )
