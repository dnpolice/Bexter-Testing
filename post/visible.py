import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")
url = base_url + 'stories/visible'

headers = { 'Content-Type': 'application/json' }
body = {
    'storyId': 1
}

response = requests.post(url, json=body, headers=headers)

print(response.status_code)
print(response.json())