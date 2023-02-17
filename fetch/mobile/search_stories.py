import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")
url = base_url + 'stories/search'
headers = {'Content-type': 'application/json', 'charset': 'utf-8'}
keyLearningOutcomes = ["Dog", "Cat"]
data = json.dumps({"keyLearningOutcomes": keyLearningOutcomes})

response = requests.post(url, headers=headers, data=data)
data = response.json()

for i, story in enumerate(data):
    print("Title:",  story["title"])
    print("Author:", story["author"])
    print("Description:", story["description"])
    print("Key Learning Outcomes:", story["keyLearningOutcomes"])
    print("Cover Photo:", story["coverPhoto"])
    print("")