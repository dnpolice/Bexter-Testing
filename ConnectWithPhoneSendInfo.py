import socketio
from dotenv import load_dotenv
import os


load_dotenv()
base_url = os.getenv("BASE_URL")


# standard Python
sio = socketio.Client()

@sio.on('play')
def on_message(data):
    print(data)
    id = data["storyId"]
    # asyncio.wait_for(asyncio.run(main(id)))
    run = True

sio.connect(base_url)

sio.emit('join', 33)

sio.emit('input', {"robotSerialNumber": 33, "command": "stop", "storyId": 1})
