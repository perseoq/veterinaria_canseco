import os

class Config(object):
    SECRET_KEY = os.urandom(16)

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('CONEXION_DB')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('CONEXION_DB')
    SQLALCHEMY_TRACK_MODIFICATIONS = True