import requests
from tests.conftest import TestBaseConfigDriver


class TestOrder(TestBaseConfigDriver):

    def test_should_set_address(self, api_set_address):
        assert api_set_address.status_code == 200
        assert api_set_address.json()['data']['address']['id'] != ""
        assert api_set_address.json()['data']['address']['address'] != ""
