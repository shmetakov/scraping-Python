# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

# username = 'shmetakov'
username = input('Имя пользователя: ')

params = {
    'type': 'owner'
}

url = f'https://api.github.com/users/{username}/repos'

response = requests.get(url, params=params)

json_data = json.loads(response.text)

with open(f'{username}.json', 'w', encoding="utf-8") as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)

print(f'Список public репозиториев для {username}:')

for item in json_data:
    print(f'    {item["name"]:35} ({item["description"]})')
