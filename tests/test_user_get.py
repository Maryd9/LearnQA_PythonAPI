import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from allure_commons.types import Severity


class TestUserGet(BaseCase):

    @allure.testcase("https://testit.ru/projects/8236454/tests/123455", "Get user details without authorization")
    @allure.tag("smoke", "regression", "get")
    @allure.severity(Severity.CRITICAL)
    @allure.description("The test tries to get user details without authorization")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.testcase("https://testit.ru/projects/8236454/tests/123456", "Get user details")
    @allure.tag("smoke", "regression", "get")
    @allure.severity(Severity.CRITICAL)
    @allure.description("The test tries to get user details")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.testcase("https://testit.ru/projects/8236454/tests/123457",
                     "Get user details under different authorization")
    @allure.tag("regression", "get")
    @allure.severity(Severity.CRITICAL)
    @allure.description("The test tries to get user details by logging in under another")
    def test_get_user_details_auth_as_another_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method + 1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")
