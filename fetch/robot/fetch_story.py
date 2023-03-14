import os
import json
from dotenv import load_dotenv
import time
import asyncio
import aiohttp
from pydub import AudioSegment
import socketio
import shutil

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

    #Fetch Data
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            status_code = response.status;
            data = await response.json()

    print("Status Code: ", status_code)

    if (status_code == 400 or status_code == 500):
        print(data["msg"])
    else:
        base_folder = os.path.dirname(fileName)

        # Delete existing files
        if os.path.exists(base_folder + "/coverphoto"):
            shutil.rmtree(base_folder + "/coverphoto")
        if os.path.exists(base_folder + "/storyphotos"):
            shutil.rmtree(base_folder + "/storyphotos")
        if os.path.exists(base_folder + "/voicerecording"):
            shutil.rmtree(base_folder + "/voicerecording")

        # Create new files
        os.mkdir(base_folder + "/coverphoto")
        os.mkdir(base_folder + "/storyphotos")
        os.mkdir(base_folder + "/voicerecording")

        # Data extraction  
        coverPhoto = data.get("coverPhoto")
        voiceRecording = data.get("voiceRecording")
        storyPhotos = data.get("storyPhotos")
        storyPhotoTimes = data.get("storyPhotoTimes")
        transcriptOfKeywords = data.get("transcriptOfKeywords")
        transcriptOfKeywordTimes = data.get("transcriptOfKeywordTimes")

        # Define storage paths
        cover_photo_path = base_folder + "/coverphoto/coverphoto.png"
        compressed_voice_path = base_folder + "/voicerecording/compressed_voicerecording.mp3"
        decompressed_voice_path = base_folder + '/voicerecording/voicerecording.wav'
        story_photo_dir = base_folder + "/storyphotos/"

        # Download files
        async with aiohttp.ClientSession() as session:
            tasks = [
                download_file(session, coverPhoto, cover_photo_path),
                download_voice_recording(session, voiceRecording, compressed_voice_path),
                *[download_file(session, storyPhoto, story_photo_dir + f"{i+1:02d}.png") for i, storyPhoto in enumerate(storyPhotos)]
            ]
            await asyncio.gather(*tasks)

        end_time = time.perf_counter()
        print(f"The code fetched in {end_time - start_time:0.4f} seconds")

        # Convert to .wav file
        sound = AudioSegment.from_mp3(compressed_voice_path)
        sound.export(decompressed_voice_path, format="wav")

        # Convert to tuples for json storage
        storyPhotoTimes = tuple([time for time in data["storyPhotoTimes"]])
        transcriptOfKeywords = tuple([keyword for keyword in data["transcriptOfKeywords"]])
        transcriptOfKeywordTimes = tuple(time for time in data["transcriptOfKeywordTimes"])

        # Store data in JSON
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
    id = data["storyId"]
    asyncio.run(main(id))
    
sio.connect(base_url)

sio.emit('join', 33)

sio.wait()