import requests

from tests.conftest import TestBaseConfigDriver, PHONE_NUMBER


class TestLogIn(TestBaseConfigDriver):

    def _handel_register_phone_number_invalid(self, phone):
        path = "https://demo-dknow-api.digikala.com/user/login-register/"
        payload = dict(
            phone=phone
        )
        response = requests.post(path, payload)
        return response

    def test_api_login_register_valid(self, api_login_register):
        assert api_login_register.status_code == 200
        assert api_login_register.json()['data']['user_id'] != ""
        assert api_login_register.json()['data']['token'] != ""

    def test_should_fail_phone_number_have_less_characters(self, read_yaml_file):
        invalid_rsp = self._handel_register_phone_number_invalid(
            phone=read_yaml_file['less_characters_phone_number']
        )
        assert invalid_rsp.status_code == 200
        assert invalid_rsp.json()['status'] == 400
        assert invalid_rsp.json()['message'] == "شماره تلفن نامعتبر است."

    def test_should_fail_phone_number_have_more_characters(self, read_yaml_file):
        invalid_rsp = self._handel_register_phone_number_invalid(
            phone=read_yaml_file['more_characters_phone_number']
        )
        assert invalid_rsp.status_code == 200
        assert invalid_rsp.json()['status'] == 400
        assert invalid_rsp.json()['message'] == "شماره تلفن نامعتبر است."

    def test_should_fail_phone_number_have_null_characters(self, read_yaml_file):
        invalid_rsp = self._handel_register_phone_number_invalid(
            phone=read_yaml_file['null_phone_number']
        )
        assert invalid_rsp.status_code == 200
        assert invalid_rsp.json()['status'] == 400
        assert invalid_rsp.json()['message'] == "شماره تلفن را وارد کنید."

    def test_should_fail_phone_number_have_string_characters(self, read_yaml_file):
        invalid_rsp = self._handel_register_phone_number_invalid(
            phone=read_yaml_file['string_phone_number']
        )
        assert invalid_rsp.status_code == 200
        assert invalid_rsp.json()['status'] == 400
        assert invalid_rsp.json()['message'] == "شماره تلفن نامعتبر است."

    def test_api_confirm_phone(self, api_confirm_phone):
        assert api_confirm_phone.status_code == 200
        expected_phone = None
        for key, value in api_confirm_phone.json()['data']['in_track'].items():
            expected_phone = value['phone']
        assert PHONE_NUMBER[1::] == expected_phone[3::]

    def test_api_far(self, api_confirm_phone):
        final_token = api_confirm_phone.json()['data']['token']