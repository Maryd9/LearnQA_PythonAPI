import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from allure_commons.types import Severity


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):

    @allure.testcase("https://testit.ru/projects/8236454/tests/123447", "Delete user with id 2")
    @allure.tag("delete")
    @allure.severity(Severity.NORMAL)
    @allure.description("This test tries to delete user with id 2")
    def test_delete_user_with_id_2(self):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_code_status(response1, 200)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        # DELETE
        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(
            response2,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "Wrong error message"
        )

    @allure.testcase("https://testit.ru/projects/8236454/tests/123448", "Successful user deletion")
    @allure.tag("smoke", "regression", "delete")
    @allure.severity(Severity.CRITICAL)
    @allure.description("This test successfully deletes user")
    def test_delete_user_successfully(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        Assertions.assert_code_status(response2, 200)

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_content(response3, '{"success":"!"}')

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response4, 404)
        Assertions.assert_content(response4, 'User not found')

    @allure.testcase("https://testit.ru/projects/8236454/tests/123449", "Deleting a user with different authorization")
    @allure.tag("regression", "delete")
    @allure.severity(Severity.CRITICAL)
    @allure.description("This test tries to delete a user by logging in under another")
    def test_delete_user_with_another_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        Assertions.assert_code_status(response2, 200)

        # DELETE
        response3 = MyRequests.delete(f"/user/{int(user_id) - 1}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "This user can only delete their own account.",
            "Wrong error message"
        )
