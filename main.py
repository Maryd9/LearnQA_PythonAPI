import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
cnt_redirects = len(response.history)
print(f"Количество редиректов {cnt_redirects}, конечный url {response.url}")
