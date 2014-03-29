# -*- coding: utf-8 -*-
"""
    flaskage.tests.test_flaskage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the Flaskage template application.

    :copyright: (c) 2014 Fotis Gimian.
    :license: MIT, see LICENSE for more details.
"""
from .. import BaseTestCase


class TestFlaskage(BaseTestCase):

    def test_index(self):
        response = self.client.get('/')
        assert b'Flaskage' in response.data

    def test_index_pyjade(self):
        response = self.client.get('/pyjade')
        assert b'Flaskage' in response.data
