from tests.conftest import TestBaseConfigDriver
import logging

log = logging.getLogger('log in order')


class TestOrder(TestBaseConfigDriver):

    def test_should_set_address(self, api_set_address):
        assert api_set_address.status_code == 200
        assert api_set_address.json()['data']['address']['id'] != ""
        assert api_set_address.json()['data']['address']['address'] != ""

    def test_should_set_shipping_fee_plan(self, api_shipping_fee_plan):
        assert api_shipping_fee_plan.status_code == 200

    def test_should_set_shipping_fee_shop_and_cart_close_limit(self, api_shipping_fee_shop_and_cart_close_limit):
        assert api_shipping_fee_shop_and_cart_close_limit.status_code == 200

    def test_should_show_shop(self, api_shop):
        assert api_shop.status_code == 200
        assert api_shop.json()['data']['header']['shop']['id'] != ""
        assert api_shop.json()['data']['header']['shop']['status'] == "active"

    def test_should_show_products(self, api_products):
        assert api_products.status_code == 200
        assert api_products.json()['data']['products'] != ""

    def test_should_add_cart_amazing(self, api_add_cart_amazing):
        assert api_add_cart_amazing[0].status_code == 200
        if api_add_cart_amazing[0].json()['status'] == 400:
            assert api_add_cart_amazing[0].json()['message'] == "موجودی محصول تمام شده‌است."
            log.warning('موجودی محصول تمام شده‌است.')
        else:
            for item in api_add_cart_amazing[0].json()['data']['cart_shipment']['cart_items']['items']:
                if item['product']['id'] == api_add_cart_amazing[1]:
                    assert api_add_cart_amazing[0].json()['data']['cart_shipment']['hash_id'] != ""
                    assert item['item_id'] != ""
                    assert True

    def test_should_add_cart_simple(self, api_add_cart_simple):
        assert api_add_cart_simple[0].status_code == 200
        if api_add_cart_simple[0].json()['status'] == 400:
            assert api_add_cart_simple[0].json()['message'] == "موجودی محصول تمام شده‌است."
            log.warning('موجودی محصول تمام شده‌است.')
        else:
            for item in api_add_cart_simple[0].json()['data']['cart_shipment']['cart_items']['items']:
                if item['product']['id'] == api_add_cart_simple[1]:
                    assert api_add_cart_simple[0].json()['data']['cart_shipment']['hash_id'] != ""
                    assert item['item_id'] != ""
                    assert True

    def test_should_shipping(self, api_shipping):
        assert api_shipping.status_code == 200
        assert api_shipping.json()['data']['cart_shipments'][0]['address']['id'] != ""
        assert api_shipping.json()['data']['cart_shipments'][0]['address']['address'] != ""

    def test_should_payment(self, api_payment, api_shipping):
        assert api_payment.status_code == 200
        assert api_payment.json()['data']['total_price']['payable_price'] == \
               api_shipping.json()['data']['cart_shipments'][0]['price']['payable_price']
        assert api_payment.json()['data']['shop']['id'] == \
               api_shipping.json()['data']['cart_shipments'][0]['shop']['id']
