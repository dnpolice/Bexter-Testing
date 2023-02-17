import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")
headers = {'Content-Type': 'application/json'}
def register():
  url = base_url + 'users'
  body = {
    "name" : "somename",
    "email":"someemail@email.com", 
    "password": "somepassd", 
    "robotSerialNumber":33
  }

  response = requests.post(url, json=body, headers=headers)

  print('signup status: ',response.status_code)
  if response.status_code != 200:
    print(response.content)
  return response

def signin():
  register()
  url = base_url + 'auth/login'
  headers = {'Content-Type': 'application/json'}
  body = {
    "email":"someemail@email.com", 
    "password": "somepassd"
  }
  response = requests.post(url, json=body, headers=headers)

  print('signin status: ', response.status_code)
  if response.status_code != 200:
    print(response.json())
  return response

signin()

