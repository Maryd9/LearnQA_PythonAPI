import requests


class TestExample:
    def test_request_method_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        assert response.status_code == 200, "Wrong response code"

        headers = response.headers
        print(headers)

        expected_headers = ["Date", "Content-Type", "Content-Length", "Connection", "Keep-Alive", "Server",
                            "x-secret-homework-header", "Cache-Control", "Expires"]
        for header in headers:
            assert header in expected_headers, f"There is no header {header} in the response"
