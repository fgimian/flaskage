# -*- coding: utf-8 -*-
"""
    flaskage.tests
    ~~~~~~~~~~~~~~

    The top level test class definition which may be used for defining
    your own application tests.

    :copyright: (c) 2014 Fotis Gimian.
    :license: MIT, see LICENSE for more details.
"""
from flask.ext.testing import TestCase

from application import create_app, db


class BaseTestCase(TestCase):

    def create_app(self):
        return create_app('testing')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
