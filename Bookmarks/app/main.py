# main.py

# pylint: disable=C

from flask import Flask
from app.config import (
    DevelopmentConfig,
)  # Configuração de ambiente para desenvolvimento
from app.routes.analysis_routes import bp as analysis_bp


def create_app(config_class=DevelopmentConfig):
    """Fábrica para criar a instância do aplicativo Flask."""
    flask_app = Flask(__name__)

    # Carregar configurações da classe fornecida
    flask_app.config.from_object(config_class)

    # Registrar blueprints
    flask_app.register_blueprint(analysis_bp, url_prefix="/analysis")

    return flask_app


# Código para rodar a aplicação quando executada diretamente
if __name__ == "__main__":
    app = (
        create_app()
    )  # Criar a aplicação com a configuração padrão (DevelopmentConfig)
    app.run(debug=True)  # Habilitar o modo debug
