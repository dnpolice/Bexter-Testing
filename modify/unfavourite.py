import requests
import sys
sys.path.append('../')
import os
from dotenv import load_dotenv
import user_auth

load_dotenv()

login_response = user_auth.signin()
base_url = os.getenv("BASE_URL")
url = base_url + 'stories/unfavourite'
headers = {'Content-Type': 'application/json'}
body = {
    'storyId': '6'
}

response = requests.post(url, json=body, headers=headers, cookies=login_response.cookies)
print('_____________________')
print(response.status_code)
print(response.json())