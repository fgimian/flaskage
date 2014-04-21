# -*- coding: utf-8 -*-
from .. import BaseTestCase


class Test{{{ name }}}(BaseTestCase):

    def test_index(self):
        response = self.client.get('/')
        assert b'Welcome to your new blueprint! :)' in response.data
