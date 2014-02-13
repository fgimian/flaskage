#!/usr/bin/env python
import os

from flask.ext.script import Manager
from flask.ext.script.commands import ShowUrls, Clean
from flask.ext.migrate import MigrateCommand
from flask.ext.assets import ManageAssets

from config import AVAILABLE_CONFIGS, DEFAULT_CONFIG
from application import create_app

# Import all models so that they are visible to Flask-Migrate.  We also
# issue a noqa command to avoid flake8's unused import warning.
# import application.models.<name>  # noqa

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config',
                   choices=AVAILABLE_CONFIGS.keys(), default=DEFAULT_CONFIG)
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets())


@manager.command
def flake8():
    """Validates all Python source files using Flake8"""
    import flake8.main
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.py'):
                flake8.main.check_file(os.path.join(dirpath, filename))


@manager.command
def test(verbosity=2):
    """Runs all application unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('.')
    result = unittest.TextTestRunner(verbosity=verbosity).run(tests)
    exit(int(not result.wasSuccessful()))

if __name__ == '__main__':
    manager.run()
