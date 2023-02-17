import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")
url = base_url + "stories/robot/3"
headers = {"x-auth-token": "33"}
response = requests.get(url, headers=headers)
print(response.status_code)
data = response.json()

if (response.status_code == 400 or response.status_code == 500):
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

    cover_photo_path = os.path.dirname(__file__) + "/coverphoto/coverphoto.png"
    voice_recording_path = os.path.dirname(__file__) + "/voicerecording/voicerecording.wav"
    story_photo_dir = os.path.dirname(__file__) + "/storyphotos/"

    cover_photo_data = bytes(coverPhoto["Body"]["data"])
    with open(cover_photo_path, 'wb') as img:
        img.write(cover_photo_data)

    voice_recording_data = bytes(voiceRecording["Body"]["data"])
    with open(voice_recording_path, 'wb') as img:
        img.write(voice_recording_data)

    for i in range(len(storyPhotos)):
        storyPhoto = storyPhotos[i]
        story_photo_data = bytes(storyPhoto["Body"]["data"])
        fileNum = str(i+1) if i+1 >= 10 else "0" + str(i+1)
        story_photo_path = story_photo_dir + fileNum + ".png"
        with open(story_photo_path, 'wb') as img:
            img.write(story_photo_data)

    storyPhotoTimes = tuple([time for time in data["storyPhotoTimes"]])
    transcriptOfKeywords = tuple([keyword for keyword in data["transcriptOfKeywords"]])
    transcriptOfKeywordTimes = tuple(time for time in data["transcriptOfKeywordTimes"])

    story_json = {
        "storyPhotoTimes": json.dumps(storyPhotoTimes),
        "transcriptOfKeywords": json.dumps(transcriptOfKeywords),
        "transcriptOfKeywordTimes": json.dumps(transcriptOfKeywordTimes)
    }
    json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "story_json.json")
    with open(json_file_path, "w") as outfile:
        json.dump(story_json, outfile)
    