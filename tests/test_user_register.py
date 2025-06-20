import requests, pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


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

    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'

        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f"Users with email '{email}' already exists")

    def test_create_user_with_invalid_email(self):
        email = 'vinkotovexample.com'

        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "Invalid email format")

    @pytest.mark.parametrize("data, missing_param", param)
    def test_create_user_with_invalid_data(self, data, missing_param):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f"The following required params are missed: {missing_param}")

    def test_create_user_with_short_username(self):
        data = {
            'password': '123',
            'username': 'l',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotovexample.com'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'username' field is too short")

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

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'username' field is too long")
