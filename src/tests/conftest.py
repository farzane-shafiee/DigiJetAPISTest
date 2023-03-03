import logging
import pytest
import yaml
import requests
import os

log = logging.getLogger('*** fixture ***')
BASE_URL = "https://demo-dknow-api.digikala.com"


# def pytest_logger_config(logger_config):
#     logger_config.add_loggers(['log', 'warning'], stdout_level='info')
#     logger_config.set_log_option_default('log,warning')
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_logger_logdirlink(config):
#     return os.path.join(os.path.dirname(__file__), 'mylogs')


class TestBaseConfigDriver:
    base_url = ""

    def setup_method(self):
        self.base_url = BASE_URL

    def teardown_method(self):
        pass


@pytest.fixture(scope="session")
def read_yaml_file():
    with open('resource.yml') as file:
        yaml_file = yaml.safe_load(file)
        # log.info('*** Read Yaml file. ***')
        return yaml_file


@pytest.fixture(scope="session")
def api_login_register(read_yaml_file):
    path = "/user/login-register/"
    payload = dict(
        phone=read_yaml_file['phone_number']
    )
    response = requests.post(BASE_URL + path, payload)
    # log.info('*** API phone is run. ***')
    return response


@pytest.fixture(scope="session")
def api_confirm_phone(api_login_register):
    path = '/user/confirm-phone/'
    payload = dict(
        token=f"{api_login_register.json()['data']['token']}",
        code=111111,
        phone=f"{api_login_register.json()['data']['phone']}",
    )
    response = requests.post(BASE_URL + path, payload)
    final_token = response.json()['data']['token']
    # log.info('*** API OTP is run. ***')
    return response, final_token


@pytest.fixture()
def api_set_address(read_yaml_file, api_confirm_phone):
    path = '/address/'f"{read_yaml_file['address_id']}"'/set-default/'
    headers = {
        "Authorization": f"{api_confirm_phone[1]}"
    }
    response = requests.post(BASE_URL + path, headers=headers)
    # log.info('*** API set address is run. ***')
    return response


@pytest.fixture()
def api_shipping_fee_plan(read_yaml_file):
    path = "https://demo-dknow-api.digikala.com/admin/shipping/shipping-fee-plan/item/0/?_back=http://demo-dknow-api" \
           ".digikala.com/admin/shipping/shipping-fee-plan/"
    payload = dict(
        free_shipping_threshold=read_yaml_file['free_shipping_threshold']
    )
    response = requests.post(path, payload)
    # log.info('*** API create shipping fee plan is run. ***')
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
    # log.info('*** API set shipping fee plan is run. ****')
    return response


@pytest.fixture(scope="session")
def api_shop(read_yaml_file, api_confirm_phone):
    shop_id = read_yaml_file['shop_id']
    path = '/shop/'f"{shop_id}"'/'
    headers = {
        "Authorization": f"{api_confirm_phone[1]}",
        "client": f"{read_yaml_file['client']}"
    }
    response = requests.get(BASE_URL + path, headers=headers)
    # log.info('*** API shop is run. ***')
    return response


@pytest.fixture()
def api_products(read_yaml_file):
    path = '/shop/'f"{read_yaml_file['shop_id']}"'/10/products/'
    response = requests.get(BASE_URL + path)
    # log.info('*** API products is run. ***')
    return response


@pytest.fixture()
def api_add_cart_amazing(api_shop, api_confirm_phone):
    path = "/cart/add/"
    headers = {
        "Authorization": f"{api_confirm_phone[1]}"
    }
    for item in api_shop.json()['data']['body']['widgets']:
        if item['data']['title'] in "تخفیف‌دارها":
            shop_product_id = item['data']['products'][0]['id']
            payload = dict(
                shop_product_id=shop_product_id,
                source="web"
            )
            response = requests.post(BASE_URL + path, payload, headers=headers)
            # log.info('*** API add cart amazing product is run. ***')
            return response, shop_product_id
        else:
            continue
    return False


@pytest.fixture(scope="session")
def api_add_cart_simple(api_shop, api_confirm_phone):
    path = "/cart/add/"
    headers = {
        "Authorization": f"{api_confirm_phone[1]}"
    }
    for item in api_shop.json()['data']['body']['widgets']:
        if item['data']['title'] in ["قفسه‌ها", "قبلا این‌ها را خریده‌اید", "تخفیف‌دارها"]:
            continue
        else:
            shop_product_id = item['data']['products'][0]['id']
            payload = dict(
                shop_product_id=shop_product_id,
                source="web"
            )
            response = requests.post(BASE_URL + path, payload, headers=headers)
            # log.info('*** API add cart simple product is run. ***')
            if response.json()['status'] == 200:
                cart_shipment_id = response.json()['data']['cart_shipment']['hash_id']
                print(cart_shipment_id)
                return response, shop_product_id, cart_shipment_id
            elif response.json()['status'] == 400:
                return False
    return False


@pytest.fixture(scope="session")
def api_shipping(api_confirm_phone, api_add_cart_simple):
    if api_add_cart_simple is not False:
        path = f"/shipping/{api_add_cart_simple[2]}/"
        headers = {
            "Authorization": f"{api_confirm_phone[1]}"
        }
        response = requests.get(BASE_URL + path, headers=headers)
        # log.info('*** API shipping is run. ***')
        return response
    elif api_add_cart_simple is False:
        return False


@pytest.fixture()
def api_payment(api_confirm_phone, api_add_cart_simple):
    if api_add_cart_simple is not False:
        # final_token = api_confirm_phone.json()['data']['token']
        path = f"/payment/{api_add_cart_simple[2]}/"
        headers = {
            "Authorization": f"{api_confirm_phone[1]}"
        }
        response = requests.get(BASE_URL + path, headers=headers)
        # log.info('*** API payment is run. ***')
        return response
    elif api_add_cart_simple is False:
        return False
