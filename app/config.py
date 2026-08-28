import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///mechanic_shop.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


class ProductionConfig:
    database_url = os.getenv("DATABASE_URL", "sqlite:///mechanic_shop.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
