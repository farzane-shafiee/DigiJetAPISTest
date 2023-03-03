import pytest

from tests.conftest import TestBaseConfigDriver
from tests.test_smook.test_orders import TestOrder
import logging

log = logging.getLogger('*** TestVoucher ***')


@pytest.mark.run
class TestVoucher(TestBaseConfigDriver):
    parent = TestOrder()

    def test_add_product(
            self,
            api_set_address,
            api_shipping_fee_plan,
            api_shipping_fee_shop_and_cart_close_limit,
            api_shop,
            api_products,
            api_add_cart_simple,
            api_shipping,
    ):
        self.parent.test_should_set_address(api_set_address)
        self.parent.test_should_set_shipping_fee_plan(api_shipping_fee_plan)
        self.parent.test_should_set_shipping_fee_shop_and_cart_close_limit(api_shipping_fee_shop_and_cart_close_limit)
        self.parent.test_should_show_shop(api_shop)
        self.parent.test_should_show_products(api_products)
        self.parent.test_should_add_cart_simple(api_add_cart_simple)
        self.parent.test_should_shipping(api_shipping)
    # def test_should_set_voucher(self, api_set_voucher):
    #     assert api_set_voucher.status_code == 200

    # def test_payment(self, api_shipping, api_payment):
    #     self.test_should_payment(api_shipping, api_payment)
