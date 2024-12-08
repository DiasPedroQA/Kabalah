# pylint: disable=C, E
# tests/test_app.py

# import pytest
# from app.main import create_app
# from app.config import DevelopmentConfig


# @pytest.fixture
# def flask_app():
#     """Fixture para criar a aplicação Flask para os testes"""
#     app = create_app(DevelopmentConfig)
#     yield app


# def test_development_config(app):
#     """Testa as configurações de desenvolvimento"""
#     app.config.from_object(DevelopmentConfig)
#     assert app.config["DEBUG"]
#     assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///dev.db"


# def test_testing_config(app):
#     """Testa as configurações de teste"""
#     app.config.from_object(TestingConfig)
#     assert app.config["TESTING"]
#     assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///test.db"


# def test_production_config(app):
#     """Testa as configurações de produção"""
#     app.config.from_object(DevelopmentConfig)
#     assert not app
