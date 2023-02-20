import json

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
        token=f"{api_login_register.json()['data']['token']}",
        code=111111,
        phone=f"{api_login_register.json()['data']['phone']}",
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


@pytest.fixture()
def api_shipping_fee_plan(read_yaml_file):
    path = "https://demo-dknow-api.digikala.com/admin/shipping/shipping-fee-plan/item/0/?_back=http://demo-dknow-api" \
           ".digikala.com/admin/shipping/shipping-fee-plan/"
    payload = dict(
        free_shipping_threshold=read_yaml_file['free_shipping_threshold']
    )
    response = requests.post(path, payload)
    return response


@pytest.fixture()
def api_shipping_fee_shop_and_cart_close_limit(read_yaml_file):
    path = "https://demo-dknow-api.digikala.com/admin/shop/item/49/?_back=http://demo-dknow-api.digikala.com/admin" \
           "/shop/?city%3D%26city_id%3D0%26crud_tab_id%3D%26district_id%3D0%26hash_id%3D%26id%3D%26merchant_id%255B0" \
           "%255D%3D2%26name%3D%25D8%25B3%25D8%25A8%25D9%2584%25D8%25A7%25D9%2586%26nickname%3D%26radius%3D%26status%3D"
    payload = dict(
        shipping_fee_plan_id=read_yaml_file['shipping_fee_plan_id'],
        cart_close_limit=read_yaml_file['cart_close_limit']
    )
    response = requests.post(path, payload)
    return response


@pytest.fixture()
def api_shop(read_yaml_file, api_confirm_phone):
    final_token = api_confirm_phone.json()['data']['token']
    path = '/shop/'f"{read_yaml_file['shop_id']}"'/'
    headers = {
        "Authorization": f"{final_token}"
    }
    response = requests.get(BASE_URL + path, headers=headers)
    return response


@pytest.fixture()
def api_products(read_yaml_file):
    path = '/shop/'f"{read_yaml_file['shop_id']}"'/10/products/'
    response = requests.get(BASE_URL + path)
    return response


@pytest.fixture()
def api_add_cart_amazing(api_shop):
    path = "/cart/add/"
    # shop_product_id = None
    # for k, v in api_shop.json()['data']["body"].items():
    #     for index in v:
    #         print(f"id = {index['data']['products'][0]['id']}")

    # shop_product_id = api_shop.json()['data']['body']['widgets'][0]['data']['products'][0]['id']
    # print(shop_product_id)
    shop_id = api_shop.json()['data']['body']['widgets'][0]['data']['products'][0]['id']
    payload = {
        "shop_product_id": shop_id,
        "source": "web"
    }

    response = requests.post(BASE_URL + path, payload)
    print(response.json())
    return response


@pytest.fixture()
def api_add_cart_simple(api_shop):
    path = "/cart/add/"
    # shop_product_id = api_shop.json()['data']['body']['widgets[2]']['data']['products[0]']['id']
    payload = dict(
        shop_product_id=f"{api_shop.json()['data']['body']['widgets[2]']['data']['products[0]']['id']}",
        source="web"
    )
    response = requests.post(BASE_URL + path, payload)
    return response
