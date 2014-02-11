from . import BaseTestCase


class TestFlaskage(BaseTestCase):

    def test_something(self):
        response = self.client.get("/")
        assert 'Flaskage' in response.data
