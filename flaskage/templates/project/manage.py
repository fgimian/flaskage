#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import getmembers, isclass

from flask.ext.failsafe import failsafe
from flask.ext.script import Manager
from flask.ext.script.commands import Clean, Server, Shell, ShowUrls
from flask.ext.migrate import MigrateCommand
from flask.ext.assets import ManageAssets
from factory.alchemy import SQLAlchemyModelFactory

from app import create_app, db, models
from config.application import AVAILABLE_CONFIGS, DEFAULT_CONFIG
from test import factories

manager = Manager(failsafe(create_app), with_default_commands=False)


def _make_context():
    context = dict(app=manager.app, db=db)
    # Add models to the context
    context.update(getmembers(
        models, lambda m: isclass(m) and issubclass(m, db.Model)
    ))
    # Add factories to the context
    context.update(getmembers(
        factories,
        lambda m: isclass(m) and issubclass(m, SQLAlchemyModelFactory)
    ))
    return context

manager.add_option('-c', '--config', dest='config',
                   choices=list(AVAILABLE_CONFIGS), default=DEFAULT_CONFIG)
manager.add_command('clean', Clean())
manager.add_command('server', Server(host='0.0.0.0'))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('urls', ShowUrls())
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets())

if __name__ == '__main__':
    manager.run()
