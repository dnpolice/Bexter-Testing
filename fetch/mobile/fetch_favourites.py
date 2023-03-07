import requests
import os
import user_auth
from dotenv import load_dotenv

load_dotenv()

login_response = user_auth.signin()
print(login_response)
base_url = os.getenv("BASE_URL")
url = base_url + 'stories/favourites'
headers = {'Content-Type': 'application/json'}
print(login_response.cookies)
response = requests.get(url, headers = headers, cookies=login_response.cookies)
data = response.json()
print('data', data)

if response.status_code == 200:
    for i, story in enumerate(data):
        print("Title:",  story["title"])
        print("Author", story["author"])
        print("Description", story["description"])
        print("Key Learning Outcomes", story["keyLearningOutcomes"])
        print("Cover Photo:", story["coverPhoto"])
        print("")
else:
    print(data)