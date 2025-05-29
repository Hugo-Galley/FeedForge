import json
from config import config, db
import requests
from models import YoutubeChannelId

def addYoutubeChannelIdToBdd(nameList):
    for name in nameList:
        response = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={name}&type=channel&key={config.Api.Youtube.Key}")
        data = json.loads(response.text)
        newYoutubeur = YoutubeChannelId(
            name = name,
            channelId = data["items"][0]["id"]["channelId"]
        )
        db.add(newYoutubeur)
        db.commit()
        db.refresh(newYoutubeur)

def getChannelIdForYoutube(name):
    youtubeur = (db.query(YoutubeChannelId)
                 .filter(YoutubeChannelId.name == name)
                 .first()
                 )
    if youtubeur is not  None:
        print(youtubeur.name, youtubeur.channelId)
    else:
       addYoutubeChannelIdToBdd([name])