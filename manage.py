#!/usr/bin/env python
import os

from flask.ext.script import Manager
from flask.ext.script.commands import ShowUrls, Clean
from flask.ext.migrate import MigrateCommand

from config import AVAILABLE_CONFIGS, DEFAULT_CONFIG
from webapp import create_app

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', default=DEFAULT_CONFIG,
                   choices=AVAILABLE_CONFIGS.keys())
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())
manager.add_command('db', MigrateCommand)


@manager.command
def flake8():
    """Validates all Python source files using PEP8 and Pyflakes."""
    import flake8.main
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            if (
                filename.endswith('.py') and
                not dirpath.endswith('/migrations/versions') and
                not dirpath.endswith('/migrations')
            ):
                flake8.main.check_file(
                    os.path.join(dirpath, filename))


if __name__ == '__main__':
    manager.run()
