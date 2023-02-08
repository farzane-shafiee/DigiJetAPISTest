import pytest
from selenium import webdriver
import requests

PHONE_NUMBER = "09193619468"


class TestBaseConfigDriver:

    base_url = ""

    def setup_method(self):
        self.base_url = "https://demo-dknow-api.digikala.com"

    def teardown_method(self):
        pass


@pytest.fixture()
def api_login_register():
    path = "https://demo-dknow-api.digikala.com/user/login-register/"
    payload = dict(
        phone=PHONE_NUMBER
    )
    response = requests.post(path, payload)
    return response


@pytest.fixture()
def api_confirm(api_login_register):
    path = 'https://demo-dknow-api.digikala.com/user/confirm-phone/'
    payload = dict(
        user_id=f"{api_login_register.json()['data']['user_id']}",
        token=f"{api_login_register.json()['data']['token']}",
        code=111111
    )
    response = requests.post(path, payload)
    return response





