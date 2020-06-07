# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

from PIL import Image

headers = {
    'x-api-key': 'dff71cbd-4ced-419e-8979-341a053c67ad'
}

url = f'https://api.thecatapi.com/v1/images/search'

response = requests.get(url, headers=headers)

json_data = response.json()[0]
img_name = ''.join(json_data['url'].split('/')[-1:])

with open(f'res.json', 'w', encoding="utf-8") as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)

img = Image.open(requests.get(json_data['url'], stream=True, headers=headers).raw)
img.show()

