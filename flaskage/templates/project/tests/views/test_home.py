# -*- coding: utf-8 -*-
from .. import BaseTestCase


class TestHome(BaseTestCase):

    def test_index(self):
        response = self.client.get('/')
        assert b'Flaskage' in response.data

    def test_index_pyjade(self):
        response = self.client.get('/pyjade')
        assert b'Flaskage' in response.data
