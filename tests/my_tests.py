import requests
from datetime import datetime, timezone


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

    def test_request_method_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        assert response.status_code == 200, "Wrong response code"

        headers = response.headers
        print(headers)

        now_datetime = datetime.now(timezone.utc)
        formatted_datetime = now_datetime.strftime('%a, %d %b %Y %H:%M:%S GMT')

        expected_headers = {"Date": formatted_datetime,
                            "Content-Type": "application/json",
                            "Content-Length": "15",
                            "Connection": "keep-alive",
                            "Keep-Alive": "timeout=10",
                            "Server": "Apache",
                            "x-secret-homework-header": "Some secret value",
                            "Cache-Control": "max-age=0",
                            "Expires": formatted_datetime}
        missed_headers = [header for header in expected_headers if header not in headers]
        assert not missed_headers, f"There is no header {', '.join(missed_headers)} in the response"

        for header, expected_value in expected_headers.items():
            assert headers[header] == expected_value, f"The header {header} has unexpected value {headers[header]}"
