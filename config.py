import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
AVAILABLE_CONFIGS = {
    'production': 'config.ProductionConfig',
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig'
}
DEFAULT_CONFIG = 'development'


class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    SECRET_KEY = 'prodkey'
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'devkey'
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(PROJECT_ROOT, 'data.db'))
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'testkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'
