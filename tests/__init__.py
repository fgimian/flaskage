# -*- coding: utf-8 -*-
"""
    flaskage.tests
    ~~~~~~~~~~~~~~

    The top level test class definition which may be used for defining
    your own application tests.

    :copyright: (c) 2014 Fotis Gimian.
    :license: MIT, see LICENSE for more details.
"""
from application import create_app, db


class BaseTestCase(object):

    def setup(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
