import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")
url = base_url + 'stories/mobile/2'
response = requests.get(url)

data = response.json()

if (response.status_code == 400):
    print(data["msg"])
else:
    print("Title:",  data["title"])
    print("Author:", data["author"])
    print("Description:", data["description"])
    print("Key Learning Outcomes:", data["keyLearningOutcomes"])
    print("Cover Photo:", data["coverPhoto"])