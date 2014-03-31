# -*- coding: utf-8 -*-
"""
    flaskage.features.environment
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The main environment setup for BDD testing.

    :copyright: (c) 2014 Fotis Gimian.
    :license: MIT, see LICENSE for more details.
"""
from application import create_app, db


def before_feature(context, feature):
    context.app = create_app('testing')
    context.client = context.app.test_client()
    context.ctx = context.app.test_request_context()
    context.ctx.push()
    db.create_all()


def after_feature(context, feature):
    db.session.remove()
    db.drop_all()
    context.ctx.pop()
