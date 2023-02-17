import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")
url = base_url + 'stories/all'
headers = {'Content-type': 'application/json'}

response = requests.get(url, headers=headers)
data = response.json()

for i, story in enumerate(data):
    print("Title:",  story["title"])
    print("Author:", story["author"])
    print("Description:", story["description"])
    print("Key Learning Outcomes:", story["keyLearningOutcomes"])
    print("Cover Photo:", story["coverPhoto"])
    print("")