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

from flask.ext.failsafe import failsafe
from flask.ext.script import Manager
from flask.ext.script.commands import Clean, Server, Shell, ShowUrls
from flask.ext.migrate import MigrateCommand
from flask.ext.assets import ManageAssets

from config import AVAILABLE_CONFIGS, DEFAULT_CONFIG
from application import create_app, db

# Import all models so that they are visible to Flask-Migrate.  We also
# issue a noqa command to avoid flake8's unused import warning.
import application.models  # noqa

manager = Manager(failsafe(create_app), with_default_commands=False)
manager.add_option('-c', '--config', dest='config',
                   choices=AVAILABLE_CONFIGS.keys(), default=DEFAULT_CONFIG)
manager.add_command('clean', Clean())
manager.add_command('runserver', Server())
manager.add_command(
    'shell', Shell(make_context=lambda: {'app': manager.app, 'db': db}))
manager.add_command('urls', ShowUrls())
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets())


@manager.command
def flake8():
    """Validates all Python source files using Flake8"""
    import flake8.main
    project_root = os.path.dirname(os.path.relpath(__file__)) or '.'
    ignore_paths = ['/.git', '/application/vendor']
    for dirpath, subdirs, filenames in os.walk(project_root):
        if any([dirpath.endswith(d) for d in ignore_paths]):
            subdirs[:] = []
            continue
        for filename in fnmatch.filter(filenames, '*.py'):
            flake8.main.check_file(os.path.join(dirpath, filename))


@manager.command
def test(verbosity=2):
    """Runs all application unit tests"""
    import nose
    nose.run(argv=['nosetests', '--verbosity=%d' % int(verbosity)])

if __name__ == '__main__':
    manager.run()
