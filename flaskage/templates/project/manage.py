#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import fnmatch

from flask.ext.failsafe import failsafe
from flask.ext.script import Manager
from flask.ext.script.commands import Clean, Server, Shell, ShowUrls
from flask.ext.migrate import MigrateCommand
from flask.ext.assets import ManageAssets

from app import create_app, db, models
from config import AVAILABLE_CONFIGS, DEFAULT_CONFIG
from tests import fixtures

manager = Manager(failsafe(create_app), with_default_commands=False)


def _make_context():
    return dict(app=manager.app, db=db, models=models, fixtures=fixtures)

manager.add_option('-c', '--config', dest='config',
                   choices=AVAILABLE_CONFIGS.keys(), default=DEFAULT_CONFIG)
manager.add_command('clean', Clean())
manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('urls', ShowUrls())
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets())


@manager.command
def flake8():
    """Validates all Python source files using Flake8"""
    import flake8.main
    project_root = os.path.dirname(os.path.relpath(__file__)) or '.'
    ignore_paths = ['/.git', '/app/vendor']
    for dirpath, subdirs, filenames in os.walk(project_root):
        if any([dirpath.endswith(d) for d in ignore_paths]):
            subdirs[:] = []
            continue
        for filename in fnmatch.filter(filenames, '*.py'):
            flake8.main.check_file(os.path.join(dirpath, filename))


@manager.command
def behave():
    """Runs all behaviour driven development tests"""
    import behave.__main__
    behave.__main__.main(args=sys.argv[2:])


@manager.command
def test():
    """Runs all application unit tests"""
    # To ensure proper coverage results, we need to execute nosetests
    # via subprocess.  The reason is that coverage won't report statistics
    # if used modules have already been imported (which is necessary for
    # Flask-Script to work properly).
    #
    # e.g.
    #
    # import coverage
    # cov = coverage.coverage()
    # cov.start()
    # from module import function  # import must be after cov.start()
    # assert function(...) == ...
    # cov.stop()
    # cov.report()
    #
    # I've contacted the author of Coverage.py to see if there's a workaround.
    import subprocess
    exit(subprocess.call('nosetests'))

if __name__ == '__main__':
    manager.run()
