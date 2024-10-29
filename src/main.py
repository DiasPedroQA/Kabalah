# pylint: disable=C, E

# src/main.py

from flask import Flask, request
from src.controllers.path_check_controller import check_path
from src.views.path_check_view import render_path_check
from logging.logger import setup_logging, get_logger


app = Flask(__name__)
logger = get_logger(__name__)


@app.route('/check_path', methods=['GET'])
def check_path_route():
    path = request.args.get('path', '')
    model = check_path(path)
    return render_path_check(model)


if __name__ == "__main__":
    setup_logging()  # Mova esta chamada para aqui
    logger.info("Iniciando a aplicação.")
    app.run(debug=True)
