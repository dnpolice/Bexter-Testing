import requests
import os
import json
from dotenv import load_dotenv
import time
import asyncio
import aiohttp
from pydub import AudioSegment
import socketio

load_dotenv()

sio = socketio.Client()
base_url = os.getenv("BASE_URL")
fileName = __file__

async def download_file(session, url, path):
    async with session.get(url) as response:
        content = await response.read()
        with open(path, 'wb') as f:
            f.write(content)

async def download_voice_recording(session, url, path):
    async with session.get(url) as response:
        with open(path, 'wb') as f:
            async for chunk in response.content.iter_chunked(1024):
                if chunk:
                    f.write(chunk)

async def main(id):
    start_time = time.perf_counter()
    url = base_url + "stories/robots/" + str(id)
    headers = {"x-auth-token": "33"}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            status_code = response.status;
            data = await response.json()

    print(status_code)
    if (status_code == 400 or status_code == 500):
        print(data["msg"])
    else:
        coverPhoto = data["coverPhoto"]
        voiceRecording = data["voiceRecording"]
        storyPhotos = data["storyPhotos"]
        storyPhotoTimes = data["storyPhotoTimes"]
        transcriptOfKeywords = data["transcriptOfKeywords"]
        transcriptOfKeywordTimes = data["transcriptOfKeywordTimes"]

        print(storyPhotoTimes)
        print(transcriptOfKeywords)
        print(transcriptOfKeywordTimes)

        cover_photo_path = os.path.dirname(fileName) + "/coverphoto/coverphoto.png"
        compressed_voice_path = os.path.dirname(fileName) + "/voicerecording/compressed_voicerecording.mp3"
        decompressed_voice_path = os.path.dirname(fileName) + '/voicerecording/voicerecording.wav'
        story_photo_dir = os.path.dirname(fileName) + "/storyphotos/"

        async with aiohttp.ClientSession() as session:
            tasks = [
                download_file(session, coverPhoto, cover_photo_path),
                download_voice_recording(session, voiceRecording, compressed_voice_path),
                *[download_file(session, storyPhoto, story_photo_dir + f"{i+1:02d}.png") for i, storyPhoto in enumerate(storyPhotos)]
            ]
            await asyncio.gather(*tasks)

        end_time = time.perf_counter()
        print(f"The code fetched in {end_time - start_time:0.4f} seconds")

        sound = AudioSegment.from_mp3(compressed_voice_path)
        sound.export(decompressed_voice_path, format="wav")

        storyPhotoTimes = tuple([time for time in data["storyPhotoTimes"]])
        transcriptOfKeywords = tuple([keyword for keyword in data["transcriptOfKeywords"]])
        transcriptOfKeywordTimes = tuple(time for time in data["transcriptOfKeywordTimes"])

        story_json = {
            "storyPhotoTimes": json.dumps(storyPhotoTimes),
            "transcriptOfKeywords": json.dumps(transcriptOfKeywords),
            "transcriptOfKeywordTimes": json.dumps(transcriptOfKeywordTimes)
        }
        json_file_path = os.path.join(os.path.dirname(os.path.abspath(fileName)), "story_json.json")
        with open(json_file_path, "w") as outfile:
            json.dump(story_json, outfile)

        end_time = time.perf_counter()
        print(f"The code ran in {end_time - start_time:0.4f} seconds")


@sio.on('play')
def on_message(data):
    print("message");
    id = data["storyId"]
    asyncio.run(main(id))
    
sio.connect(base_url)

sio.emit('join', 33)

sio.wait()

# asyncio.run(main(18))