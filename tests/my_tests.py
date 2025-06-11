import requests


class TestExample:

    def test_short_phrase(self):
        phrase = input("Set a phrase: ")
        expected_len = 15
        assert len(phrase) < expected_len, f"The number of characters is equal to or greater than {expected_len}"

    def test_request_method_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        assert response.status_code == 200, "Wrong response code"

        cookie = response.cookies
        print(cookie)
        assert "HomeWork" in cookie, "There is no cookie 'HomeWork' in the response"

        expected_value = "hw_value"
        actual_value = cookie.get('HomeWork')
        assert actual_value == expected_value, f"Wrong cookie value {actual_value}"
