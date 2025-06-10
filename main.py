import requests

# 1 Без параметра method выводится сообщение Wrong method provided
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

# 2 Отправляя HEAD-запрос с параметром method = 'HEAD' в ответе приходит пустота
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "HEAD"})
print(response.text)

# 3 Делая запрос с правильным значением method выводится текст {"success":"!"}
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":"GET"})
print(response.text)

# 4 Перебор всех вариантов
# Сервер отвечает ок в случае, если передается DELETE-запрос с параметром method = 'GET'
# Сервер отвечает Wrong method provided в случае, если передается OPTIONS-запрос с параметром method = 'OPTIONS'
# или передается PATCH-запрос с параметром method = 'PATCH'
url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
requests_methods = ["get", "post", "delete", "put", "patch", "options"]
methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
for requests_method in requests_methods:
    request = getattr(requests, requests_method)
    for data_method in methods:
        data = {"method": f"{data_method}"}
        if requests_method == 'get':
            response = request(url, params=data)
            print(f"Тип http-запроса: {requests_method}, параметр method: {data_method}, ответ: {response.text}")
        else:
            response = request(url, data=data)
            print(f"Тип http-запроса: {requests_method}, параметр method: {data_method}, ответ: {response.text}")