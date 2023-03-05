import pytest

from tests.conftest import TestBaseConfigDriver
import logging

log = logging.getLogger('*** Test Order ***')


@pytest.mark.order
class TestOrder(TestBaseConfigDriver):

    def test_should_set_address(self, api_set_address):
        assert api_set_address.status_code == 200
        assert api_set_address.json()['data']['address']['id'] != ""
        assert api_set_address.json()['data']['address']['address'] != ""
        log.info('*** API set address is run. ***')

    def test_should_set_shipping_fee_plan(self, api_shipping_fee_plan):
        assert api_shipping_fee_plan.status_code == 200
        log.info('*** API create shipping fee plan is run. ***')

    def test_should_set_shipping_fee_shop_and_cart_close_limit(self, api_shipping_fee_shop_and_cart_close_limit):
        assert api_shipping_fee_shop_and_cart_close_limit.status_code == 200
        log.info('*** API set shipping fee plan is run. ****')

    def test_should_show_shop(self, api_shop):
        assert api_shop.status_code == 200
        assert api_shop.json()['data']['header']['shop']['id'] != ""
        assert api_shop.json()['data']['header']['shop']['status'] == "active"
        log.info('*** API shop is run. ***')

    def test_should_show_products(self, api_products):
        assert api_products.status_code == 200
        assert api_products.json()['data']['products'] != ""
        log.info('*** API products is run. ***')

    def test_should_add_cart_amazing(self, api_add_cart_amazing):
        if api_add_cart_amazing is False:
            log.warning('*** Add cart: products not added ***')
            assert True
        else:
            assert api_add_cart_amazing[0].status_code == 200
            log.info('*** API add cart amazing product is run. ***')
            if api_add_cart_amazing[0].json()['status'] == 400:
                assert api_add_cart_amazing[0].json()['message'] == "موجودی محصول تمام شده‌است."
                log.warning('*** has stock is false. ***')
            else:
                for item in api_add_cart_amazing[0].json()['data']['cart_shipment']['cart_items']['items']:
                    if item['product']['id'] == api_add_cart_amazing[1]:
                        assert api_add_cart_amazing[0].json()['data']['cart_shipment']['hash_id'] != ""
                        assert item['item_id'] != ""

    def test_should_add_cart_simple(self, api_add_cart_simple):
        if api_add_cart_simple is False:
            log.warning('*** Add cart: products not added ***')
            assert True
        else:
            assert api_add_cart_simple[0].status_code == 200
            log.info('*** API add cart simple product is run. ***')
            if api_add_cart_simple[0].json()['status'] == 400:
                assert api_add_cart_simple[0].json()['message'] == "موجودی محصول تمام شده‌است."
                log.warning('*** has stock is false. ***')
            else:
                for item in api_add_cart_simple[0].json()['data']['cart_shipment']['cart_items']['items']:
                    if item['product']['id'] == api_add_cart_simple[1]:
                        assert api_add_cart_simple[0].json()['data']['cart_shipment']['hash_id'] != ""
                        assert item['item_id'] != ""

    def test_should_shipping(self, api_shipping):
        if api_shipping is False:
            log.warning('*** Shipping: products not added. ***')
            assert True
        else:
            assert api_shipping.status_code == 200
            assert api_shipping.json()['data']['cart_shipments'][0]['address']['id'] != ""
            assert api_shipping.json()['data']['cart_shipments'][0]['address']['address'] != ""
            log.info('*** API shipping is run. ***')

    def test_get_balance(self, api_get_balance):
        assert api_get_balance.status_code == 200

    def test_gift_cards(self, api_gift_cards):
        assert api_gift_cards.status_code == 200

    def test_should_payment(self, api_payment, api_shipping):
        if api_payment is False:
            log.warning('*** Payment: products not added. ***')
            assert True
        else:
            assert api_payment.status_code == 200
            assert api_payment.json()['data']['total_price']['payable_price'] == \
                   api_shipping.json()['data']['cart_shipments'][0]['price']['payable_price']
            assert api_payment.json()['data']['shop']['id'] == \
                   api_shipping.json()['data']['cart_shipments'][0]['shop']['id']
            log.info('*** API payment is run. ***')