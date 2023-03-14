import socketio
from dotenv import load_dotenv
import os

load_dotenv()
base_url = os.getenv("BASE_URL")

sio = socketio.Client()

sio.connect(base_url)

sio.emit('join', 33)

sio.emit('input', {"robotSerialNumber": 33, "command": "play", "storyId": 17})

sio.sleep(8)

sio.emit('input', {"robotSerialNumber": 33, "command": "stop"})

