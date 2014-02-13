#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    flaskage.manage
    ~~~~~~~~~~~~~~~

    The main script used to manage all aspects relating to the application
    including configuration, database migration, assets, running the
    development server and so on.

    :copyright: (c) 2014 Fotis Gimian.
    :license: MIT, see LICENSE for more details.
"""
import os
import fnmatch
import sys

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
    project_root = os.path.dirname(os.path.relpath(__file__)) or '.'
    ignore_paths = ['/.git', '/application/vendor', '/migrations/versions']
    for dirpath, subdirs, filenames in os.walk(project_root, topdown=True):
        if any([dirpath.endswith(d) for d in ignore_paths]):
            subdirs[:] = []
            continue
        for filename in fnmatch.filter(filenames, '*.py'):
            flake8.main.check_file(os.path.join(dirpath, filename))


@manager.command
def tests(verbosity=2):
    """Runs all application unit tests"""
    if sys.version_info < (2, 7):
        import unittest2 as unittest
    else:
        import unittest
    project_root = os.path.dirname(os.path.relpath(__file__)) or '.'
    tests = unittest.TestLoader().discover(project_root)
    result = unittest.TextTestRunner(verbosity=verbosity).run(tests)
    exit(int(not result.wasSuccessful()))

if __name__ == '__main__':
    manager.run()
