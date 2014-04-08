# -*- coding: utf-8 -*-
import os

AVAILABLE_CONFIGS = {
    'production': 'config.ProductionConfig',
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig'
}
DEFAULT_CONFIG = 'development'


class Config(object):
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DEBUG = False
    ASSETS_LOAD_PATH = [os.path.join(PROJECT_ROOT, 'application', 'assets')]


class ProductionConfig(Config):
    SECRET_KEY = 'prodkey'
    ASESTS_AUTO_BUILD = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@host/dbname'


class DevelopmentConfig(Config):
    SECRET_KEY = 'devkey'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(Config.PROJECT_ROOT, 'data.db'))
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    SECRET_KEY = 'testkey'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
