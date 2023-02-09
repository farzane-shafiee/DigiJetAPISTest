import pytest
import yaml
import requests


BASE_URL = "https://demo-dknow-api.digikala.com"

class TestBaseConfigDriver:

    base_url = ""

    def setup_method(self):
        self.base_url = BASE_URL

    def teardown_method(self):
        pass


@pytest.fixture()
def read_yaml_file():
    with open('resource.yml') as file:
        yaml_file = yaml.safe_load(file)
        return yaml_file


@pytest.fixture()
def api_login_register(read_yaml_file):
    path = "https://demo-dknow-api.digikala.com/user/login-register/"
    payload = dict(
        phone=read_yaml_file['phone_number']
    )
    response = requests.post(path, payload)

    return response


@pytest.fixture()
def api_confirm_phone(api_login_register):
    path = 'https://demo-dknow-api.digikala.com/user/confirm-phone/'
    payload = dict(
        user_id=f"{api_login_register.json()['data']['user_id']}",
        token=f"{api_login_register.json()['data']['token']}",
        code=111111
    )
    response = requests.post(path, payload)
    return response


@pytest.fixture()
def api_set_address(api_confirm_phone, read_yaml_file):
    final_token = api_confirm_phone.json()['data']['token']
    path = '/address/'f"{read_yaml_file['address_id']}"'/set-default/'
    headers = {
        "Authorization": f"{final_token}"
    }
    response = requests.post(BASE_URL + path, headers=headers)
    return response


