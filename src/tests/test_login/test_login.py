from tests.conftest import TestBaseConfigDriver, PHONE_NUMBER


class TestLogIn(TestBaseConfigDriver):

    def test_api_login_register_valid(self, api_login_register):
        assert api_login_register.status_code == 200
        assert api_login_register.json()['data']['user_id'] != ""
        assert api_login_register.json()['data']['token'] != ""

    def test_api_confirm_phone(self, api_confirm):
        assert api_confirm.status_code == 200
        user_info = api_confirm.json()['data']['in_track']['user_info']['phone']
        assert PHONE_NUMBER[1::] == user_info[3::]

    def test_api_far(self, api_confirm):
        final_token = api_confirm.json()['data']['token']