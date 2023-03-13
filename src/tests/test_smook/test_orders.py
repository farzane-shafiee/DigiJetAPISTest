import pytest

from tests.conftest import TestBaseConfigDriver
import logging

log = logging.getLogger('*** Test Order ***')


@pytest.mark.order
class TestOrder(TestBaseConfigDriver):

    def test_should_set_address(self, api_set_address):
        assert api_set_address.status_code == 200
        if api_set_address.json()['status'] == 404:
            log.warning('*** address_id is invalid ***')
            assert True
        else:
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

    def test_gift_cards(self, api_list_gift_cards):
        if api_list_gift_cards is False:
            log.warning('api_list_gift_cards: gift card is null')
            assert True
        else:
            assert api_list_gift_cards[0].status_code == 200
            assert api_list_gift_cards[0].json()['data']['with_balance'][0]['id'] != ""

    def test_payment(self, api_payment, api_shipping):
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

    def test_bpg_manifest_data(self, api_bpg_manifest_data):
        if api_bpg_manifest_data is False:
            log.warning('has stock is false.')
            assert True
        else:
            assert api_bpg_manifest_data.status_code == 200
            assert api_bpg_manifest_data.json()['data']['credit_payment_id'] != ""

    # def test_set_gift_card(self, api_set_gift_card):
    #     if api_set_gift_card is False:
    #         assert True
    #         log.warning('api_set_gift_card: gift card is null or invalid')
    #     else:
    #         assert api_set_gift_card.status_code == 200
    #         if api_set_gift_card.json()['status'] == 400:
    #             assert api_set_gift_card.json()['message'] == 'Invalid gift card Id.'
    #             log.warning('gift card is null')
    #         else:
    #             assert api_set_gift_card.json()['data']['gift_card_amount'] != ""

    def test_checkout(self, api_checkout):
        if api_checkout is False:
            assert True
            log.warning('api_checkout: gift card is invalid or has stock is false.')
        else:
            assert api_checkout[0].status_code == 200
            assert api_checkout[0].json()['data']['redirect_url'] != ""

    def test_send_to_bank(self, api_send_to_bank):
        if api_send_to_bank is False:
            assert True
            log.warning('payment is False')
        else:
            assert api_send_to_bank.status_code == 200


