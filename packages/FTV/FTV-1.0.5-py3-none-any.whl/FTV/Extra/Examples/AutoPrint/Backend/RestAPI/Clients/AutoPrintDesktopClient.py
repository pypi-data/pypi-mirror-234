import json

import requests


url = "http://127.0.0.1:80/Users/register"
data = {"name": "Kfir", "password": "1234"}

response = requests.post(url, data)
response_data = json.loads(response.text)

key = list(response_data.keys())[0]

if key == "ok":
    data["id"] = response_data[key]
    print(data)
elif key == "error":
    print(response_data[key])



url = "http://127.0.0.1:80/Users/Database"
response = requests.get(url)
print(response.text)
