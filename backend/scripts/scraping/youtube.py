import requests

from config import CONFIG, db
from configFiles.models import YoutubeChannelId

def add_yt_channel_id_to_bdd(name_list):
    for name in name_list:
        try:
            response = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={name}&type=channel&key={CONFIG.API.Youtube.Key}")
            response.raise_for_status()
            data = response.json()
            if data.get("items") and len(data["items"]) > 0:
                is_exist = db.query(YoutubeChannelId).filter(YoutubeChannelId.channelId == data["items"][0]["id"]["channelId"]).first()
                if is_exist is None:
                    new_youtubeur = YoutubeChannelId(
                        name = name,
                        channelId = data["items"][0]["id"]["channelId"]
                    )
                    db.add(new_youtubeur)
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
            print(f"Erreur de commit {e}")
            db.rollback()

