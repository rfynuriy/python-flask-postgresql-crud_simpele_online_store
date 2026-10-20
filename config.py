from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    db_secret_key = os.getenv("SECRET_KEY")

    JWT_SECRET_KEY = db_secret_key
    SECRET_KEY = db_secret_key
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class DevelopmentConfig(Config):
    DEBUG = True
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

class TestingConfig(Config):
    TESTING = True
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = "simpleonlinestore_test"

    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

class ProductionConfig(Config):
    pass
