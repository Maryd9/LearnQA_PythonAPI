from tabnanny import process_tokens

import requests, time

token = ''
seconds = 0

# Создание задачи
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
if response.status_code == 200:
    data = response.json()
    token = data.get('token')
    seconds = data.get('seconds')
    print(response.text)
else:
    print(f"Ошибка запроса {response.status_code}")

# Запрос до готовности
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": f"{token}"})
if response.status_code == 200:
    data = response.json()
    status = data.get('status')
    print(response.text)
    assert status == "Job is NOT ready", f"Получен другой status {status}"
else:
    print(f"Ошибка запроса {response.status_code}")

# Ожидание
time.sleep(seconds)

# Запрос после завершения задачи
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": f"{token}"})
if response.status_code == 200:
    data = response.json()
    status = data.get('status')
    result = data.get('result')
    print(response.text)
    assert status == "Job is ready", f"Получен status: {status}"
    assert 'result' in data, "Поле result отсутствует в JSON"
else:
    print(f"Ошибка запроса {response.status_code}")
