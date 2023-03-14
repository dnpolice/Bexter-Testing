import requests
import os
from dotenv import load_dotenv
load_dotenv()

base_url = os.getenv("BASE_URL")
url = base_url + "stories/delete"
body = {
    "storyId": "13"
}
headers = {'Content-type': 'application/json'}
response = requests.post(url, json=body, headers=headers)

print(print(response.status_code))
print(response.json())