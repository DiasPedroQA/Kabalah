# app/config.py

"""
Este módulo inicializa a aplicação Flask e registra as rotas.
"""

import os


class Config:
    """Classe base para configurações do Flask"""

    SECRET_KEY = os.environ.get("SECRET_KEY", "defaultsecretkey")
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def get_config(cls, key):
        """Método para obter uma configuração específica"""
        return getattr(cls, key, None)

    @classmethod
    def set_config(cls, key, value):
        """Método para definir uma configuração específica"""
        if key not in cls.__dict__:  # Evita alterar chaves não definidas
            raise ValueError(f"Config key '{key}' is not valid.")
        setattr(cls, key, value)


class DevelopmentConfig(Config):
    """Configurações específicas para desenvolvimento"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Configurações para testes"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class ProductionConfig(Config):
    """Configurações para produção"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
