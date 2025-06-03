from config import config, db
import requests
from models import YoutubeChannelId

def addYoutubeChannelIdToBdd(nameList):
    for name in nameList:
        try:
            response = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={name}&type=channel&key={config.API.Youtube.Key}")
            response.raise_for_status()
            data = response.json()
            if data.get("items") and len(data["items"]) > 0:
                isExist = db.query(YoutubeChannelId).filter(YoutubeChannelId.channelId == data["items"][0]["id"]["channelId"]).first()
                if isExist is None:
                    newYoutubeur = YoutubeChannelId(
                        name = name,
                        channelId = data["items"][0]["id"]["channelId"]
                    )
                    db.add(newYoutubeur)
            else:
                print(f"Aucun channel ID trouvé pour {name}")
        except requests.RequestException as e:
            print(f"Erreur lors de la requete pour {name}, {e}")
        except KeyError as e :
            print(f"Données manquante dans {name}, {e}")
        except Exception as e:
            print(f"Erreur innatendu pour {name}, {e}")
        try:
            db.commit()
        except Exception as e:
            print("Erreur de commit {e}")
            db.rollback()

def getChannelIdForYoutube(name):
    youtubeur = (db.query(YoutubeChannelId)
                 .filter(YoutubeChannelId.name == name)
                 .first()
                 )
    if youtubeur is not  None:
        print(youtubeur.name, youtubeur.channelId)
    else:
       addYoutubeChannelIdToBdd([name])
