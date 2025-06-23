import pytest
import allure
from lib.base_case import BaseCase
from allure_commons.types import Severity
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    param = [
        ({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
         "password"),
        ({'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
         "username"),
        ({'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
         "firstName"),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'vinkotov@example.com'},
         "lastName"),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa'}, "email")
    ]

    @allure.testcase("https://testit.ru/projects/8236454/tests/123458",
                     "Successful user creation")
    @allure.tag("smoke", "regression", "create")
    @allure.severity(Severity.CRITICAL)
    @allure.description("The test tries to create user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.testcase("https://testit.ru/projects/8236454/tests/123459",
                     "Create a user with an existing email")
    @allure.tag("create")
    @allure.severity(Severity.NORMAL)
    @allure.description("The test tries to create user with an existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f"Users with email '{email}' already exists")

    @allure.testcase("https://testit.ru/projects/8236454/tests/123460",
                     "Creating a user with an email in the wrong format")
    @allure.tag("create")
    @allure.severity(Severity.NORMAL)
    @allure.description("The test tries to create user with an email in the wrong format")
    def test_create_user_with_invalid_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "Invalid email format")

    @allure.testcase("https://testit.ru/projects/8236454/tests/123461",
                     "Create user with invalid data")
    @allure.tag("smoke", "regression", "create")
    @allure.severity(Severity.CRITICAL)
    @allure.description("The test tries to create user with invalid data")
    @pytest.mark.parametrize("data, missing_param", param)
    def test_create_user_with_invalid_data(self, data, missing_param):
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f"The following required params are missed: {missing_param}")

    @allure.testcase("https://testit.ru/projects/8236454/tests/123462",
                     "Create a user with a short name")
    @allure.tag("create")
    @allure.severity(Severity.NORMAL)
    @allure.description("The test tries to create user with short username")
    def test_create_user_with_short_username(self):
        data = {
            'password': '123',
            'username': 'l',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotovexample.com'
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'username' field is too short")

    @allure.testcase("https://testit.ru/projects/8236454/tests/123463",
                     "Create a user with a long name")
    @allure.tag("create")
    @allure.severity(Severity.NORMAL)
    @allure.description("The test tries to create user with long username")
    def test_create_user_with_long_username(self):
        data = {
            'password': '123',
            'username': 'йцу кен гшщ зхъ фва про лдж эяч сми тьб юёъ ЙЦУ КЕН ГШЩ ЗХЪ ФВА ПРО ЛДЖ ЭЯЧ СМИ ТЬБ ЮЁЪ !“№ ;%:'
                        ' ?*()_+/, § $&= @#«» <>~®-;²³ йцу кен гшщ зхъ фва про лдж эяч сми тьб юёъ ЙЦУ КЕН ГШЩ ЗХЪ ФВА '
                        'ПРО ЛДЖ ЭЯЧ СМИ ТЬБ ЮЁЪ !“№ ;%: ?*()_+/, § $&= @#«» <>~®-;²³.',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotovexample.com'
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'username' field is too long")
