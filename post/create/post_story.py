import requests
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

cover_photo_path = os.path.dirname(__file__)+ '/coverphoto/coverphoto.png'
voice_recording_path = os.path.dirname(__file__) + '/voicerecording/voicerecording.wav'
story_photo_path = os.path.dirname(__file__) + '/storyphotos'

# Compress voice recording
sound = AudioSegment.from_wav(voice_recording_path)
compressed_voice_path = os.path.dirname(__file__) + '/voicerecording/compressed_voicerecording.mp3'
sound.export(compressed_voice_path, format="mp3")

fields = []

# Add Story Photos
for file_name in sorted(os.listdir(story_photo_path)):
    if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
        fields.append(('storyPhotos', (file_name, open(os.path.join(story_photo_path, file_name), 'rb'), 'image/png')))

# Add Story Photo Times
storyPhotoTimes = ["9", "33", "54", "78", "101", "124", "150", "172", "195", "216"]
for t in storyPhotoTimes:
    fields.append(('storyPhotoTimes', t))

# Add Key Transcript Of Keywords
transcriptOfKeywords = ['like', 'red', 'what', 'red', 'red', 'like', 'like', 'blue', 'blue', 'blue', 'like', 'yellow', 'yellow', 'like', 'pink', 'pink', 'pink', 'like', 'purple', 'purple', 'purple', 'like', 'green', 'green', 'green', 'like', 'green', 'green', 'like', 'black', 'black', 'black', 'like', 'white', 'white', 'white', 'see', 'see', 'pink', 'yellow', 'green', 'purple', 'like']
transcriptOfKeywordTimes = ['4', '13', '17', '21', '24', '29', '35', '42', '46', '50', '59', '67', '71', '83', '91', '95', '100', '105', '112', '118', '123', '128', '140', '145', '149', '154', '162', '170', '176', '185', '189', '193', '198', '205', '211', '215', '226', '235', '241', '247', '253', '260', '268']
for i in range(len(transcriptOfKeywords)):
    w = transcriptOfKeywords[i]
    t = transcriptOfKeywordTimes[i]
    fields.append(('transcriptOfKeywords', w))
    fields.append(('transcriptOfKeywordTimes', t))

# Add Key Learning Outcomes
keyLearningOutcomes = ['Colours','See','Like','What']
for w in keyLearningOutcomes:
    fields.append(('keyLearningOutcomes', w))

single_data_fields = [
    ('title', 'I Like My Car'),
    ('author', 'Michael Robertson'),
    ('description', 'Funny animals match their equally funny cars as they all make their way to a car party!'),
    ('isVisible', "true"),
    ('coverPhoto', (os.path.basename(cover_photo_path), open(cover_photo_path, 'rb'), 'image/png')),
    ('voiceRecording', (os.path.basename(compressed_voice_path), open(compressed_voice_path, 'rb'), 'audio/mpeg'))
]

fields += single_data_fields

mp_encoder = MultipartEncoder(fields=fields, encoding='utf-8')

# Send requests
base_url = os.getenv("BASE_URL")
url = base_url + 'stories/create'
headers = {'Content-type': mp_encoder.content_type}
response = requests.post(url, headers=headers, data=mp_encoder)

print(response.status_code)
print(response.json())
