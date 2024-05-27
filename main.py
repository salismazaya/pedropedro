from instagrapi import Client
from tempfile import NamedTemporaryFile
from utils import create_instagram_notification, overlay_image_on_video
import requests, atexit, time, os, pickle

from dotenv import load_dotenv

load_dotenv()

cl = Client()
cl.login(os.environ['USERNAME'], os.environ['PASSWORD'])

atexit.register(cl.logout)

UPLOADED = []

if os.path.exists('data.pkl'):
    UPLOADED = pickle.loads(open('data.pkl', 'rb').read())

def save_on_exit():
    data = pickle.dumps(UPLOADED)
    open('data.pkl', 'wb').write(data)


atexit.register(save_on_exit)

while True:
    data = cl.news_inbox_v1(mark_as_seen = True)
    for x in data['new_stories']:
        if x['notif_name'] == 'user_followed':
            username = x['args']['profile_name']
            pp = x['args']['profile_image']

            if username in UPLOADED:
                continue

            pp_file = NamedTemporaryFile(suffix = '.jpg')
            # pp_file.write(requests.get(pp).content)
            open(pp_file.name, 'wb').write(requests.get(pp).content)

            followed_image = NamedTemporaryFile(suffix = '.png')
            output = NamedTemporaryFile(suffix = '.mp4')

            create_instagram_notification(pp_file.name, username, followed_image.name)
            overlay_image_on_video('raw.mp4', followed_image.name, output.name)
            cl.clip_upload(output.name, "@" + username)
            UPLOADED.append(username)
    
    time.sleep(10)