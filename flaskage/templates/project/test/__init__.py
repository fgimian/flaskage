# -*- coding: utf-8 -*-
from app import create_app, db


class BaseTestCase(object):

    def setup(self):
        self.app = create_app('test')
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
