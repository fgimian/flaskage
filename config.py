# -*- coding: utf-8 -*-
"""
    flaskage.config
    ~~~~~~~~~~~~~~~

    Configuration for the various environments where the application may run.

    In addition to adjusting this configuration, you'll need to generate some
    secure secret keys.  To do this, simply run the following in a python
    shell and use the result as your secret key (output provided below for
    demonstrational purposes only).

    >>> import os
    >>> os.urandom(24)
    '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

    :copyright: (c) 2014 Fotis Gimian.
    :license: MIT, see LICENSE for more details.
"""
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
