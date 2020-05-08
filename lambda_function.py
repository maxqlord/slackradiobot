import json
import os
import urllib
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests

refreshToken = os.environ["REFRESH_TOKEN"]
#saoradio: GJBN4UJRM
#saoradiotest: G0136L9H3CJ
allowed_channel = 'GJBN4UJRM'
def send_text_response(event, response_text):
    token = refreshTheToken(refreshToken)
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        SLACK_URL = "https://slack.com/api/chat.postMessage"
        events = json.loads(event["body"])["event"]
        channel_id = events["channel"]
        print(channel_id)
        if events.get("text") is not None:
            print("TEXT: " + events["text"])
            text = events["text"]
            if "open.spotify" in text and channel_id == allowed_channel and "track" in text:
                start_index = text.find("https")
                end_index = len(text)
                link = ""
                if text.find('|') != -1:
                    end_index = text.find('|')
                
                elif text.find(' ') != -1:
                    end_index = text.find(' ', start_index)
                
                link = text[start_index:end_index]
                print("LINK: " + link)
                results = sp.user_playlist_add_tracks(
                    'maxlord17', "spotify:playlist:3riIg7713mvvlffpLXrAGE", [link])
                print(results)
    else:
        print("fail")
    
    

def lambda_handler(event, context):
    print(f"Received event:\n{event}\nWith context:\n{context}")
    if not check_if_from_bot(event):
        send_text_response(event, "Hi")
    
    return "200 OK"

def check_if_from_bot(event):
    body = json.loads(event["body"])
    is_bot = body["event"].get("bot_id") is not None
    if is_bot:
        return True
    return False
    
def refreshTheToken(refreshToken):

    clientIdClientSecret = os.environ["ID_SECRET"]
    data = {'grant_type': 'refresh_token', 'refresh_token': refreshToken}

    headers = {'Authorization': clientIdClientSecret}
    p = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)

    spotifyToken = p.json()
    return spotifyToken['access_token']
