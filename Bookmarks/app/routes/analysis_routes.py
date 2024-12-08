# pylint: disable=C
# app/routes/analysis_routes.py

"""
Este módulo define as rotas relacionadas
à análise de texto e caminhos de arquivos.
"""

from flask import Blueprint, render_template, request
from app.services.text_analysis import analyze_text
from app.services.file_manager import analyze_paths

# Definindo o Blueprint. O nome do blueprint é "analysis".
bp = Blueprint("analysis", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
def home():
    """
    Renderiza a página inicial.
    """
    return render_template("index.html")


@bp.route("/analyze_text", methods=["POST"])
def analyze_text_route():
    """
    Recebe texto enviado pelo cliente e retorna o resultado da análise.
    """
    text = request.form.get("text")
    if not text:
        return "Nenhum texto fornecido.", 400
    result = analyze_text(text)
    return render_template("result.html", result=result)


@bp.route("/analyze_paths", methods=["POST"])
def analyze_paths_route():
    """
    Recebe caminhos enviados pelo cliente e retorna o resultado da análise.
    """
    paths = request.form.getlist("paths")
    if not paths:
        return "Nenhum caminho fornecido.", 400
    result = analyze_paths(paths)
    return render_template("result.html", result=result)
