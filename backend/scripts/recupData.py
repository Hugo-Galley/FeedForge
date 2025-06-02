import json
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

podcasts_francais_2024 = [
    "Génération Do It Yourself",
    "HugoDécrypte – Les actus du jour",
    "Mediarama",
    "Le Précepteur",
    "Un podcast de goûts",
    "Affaires sensibles",
    "Legend",
    "Hondelatte Raconte",
    "Les Pieds sur terre",
    "Small Talk",
    "Step Back",
    "Programme B",
    "Criminels",
    "Somnifère",
    "La riposte",
    "La chronique de Guillaume Meurice",
    "La chronique de Pierre-Emmanuel Barré",
    "Timeline, 5.000 ans d’Histoire",
    "Au fil de l'histoire",
    "Transfert",
    "L’Heure du Monde",
    "FloodCast",
    "Star Freestyle",
    "CHRONIQUES CRIMINELLES",
    "Les Grosses Têtes",
    "L'After Foot",
    "Ça commence aujourd'hui",
    "C dans l'air",
    "Nota Bene",
    "Soft Power",
    "Choses à Savoir",
    "Le Masque et la Plume",
    "Du Poil sous les bras",
    "Mourir Moins Con",
    "Maintenant Vous Savez – Culture",
    "Tatousenti",
    "Le Point culture",
    "3 minutes à méditer",
    "Cold cases",
    "En 6 dates clés",
    "LE CODE Radio avec Mehdi Maïzi",
    "Fifty States — un Podcast Quotidien",
    "Les nouvelles aventures de Cornebidouille",
    "Faites entrer l'accusé",
    "Book Club",
    "Allons-y voir!",
    "Polissons",
    "Jean-Chat voit dans le noir",
    "Edith Piaf par Balasko",
    "La Chute de Lapinville",
    "Les actus du jour avec Hugo Travers",
    "Mediarama de François Defossez",
    "Le Précepteur avec Charles Robin",
    "Un podcast de goûts avec Louis Dumoulin",
    "La chronique de Guillaume Meurice",
    "La chronique de Pierre-Emmanuel Barré",
    "Timeline, 5.000 ans d’Histoire",
    "Small Talk",
    "Step Back",
    "Programme B",
    "Criminels",
    "Somnifère",
    "La riposte",
    "Affaires sensibles",
    "Legend",
    "Hondelatte Raconte",
    "Les Pieds sur terre",
    "Transfert",
    "L’Heure du Monde",
    "FloodCast",
    "Star Freestyle",
    "CHRONIQUES CRIMINELLES",
    "Les Grosses Têtes",
    "L'After Foot",
    "Ça commence aujourd'hui",
    "C dans l'air",
    "Nota Bene",
    "Soft Power",
    "Choses à Savoir",
    "Le Masque et la Plume",
    "Du Poil sous les bras",
    "Mourir Moins Con",
    "Maintenant Vous Savez – Culture",
    "Tatousenti",
    "Le Point culture",
    "3 minutes à méditer",
    "Cold cases",
    "En 6 dates clés",
    "LE CODE Radio avec Mehdi Maïzi",
    "Fifty States — un Podcast Quotidien",
    "Les nouvelles aventures de Cornebidouille",
    "Faites entrer l'accusé",
    "Book Club",
    "Allons-y voir!",
    "Polissons",
    "Jean-Chat voit dans le noir",
    "Edith Piaf par Balasko",
    "La Chute de Lapinville",
    "Les actus du jour avec Hugo Travers",
    "Mediarama de François Defossez",
    "Le Précepteur avec Charles Robin",
    "Un podcast de goûts avec Louis Dumoulin"
]

addYoutubeChannelIdToBdd(podcasts_francais_2024)