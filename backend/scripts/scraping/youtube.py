from config import config, db
import requests
from configFiles.models import YoutubeChannelId

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

podcast_channels = [
    # Top 1–60 selon le classement YouTube US (semaine du 5–11 mai 2025)
    "The Joe Rogan Experience",
    "Kill Tony",
    "Rotten Mango",
    "48 Hours",
    "The MeidasTouch Podcast",
    "H3 Podcast",
    "Club Shay Shay",
    "This Past Weekend w/ Theo Von",
    "Smosh Reads Reddit Stories",
    "Dr Insanity",
    "Shawn Ryan Show",
    "The Pat McAfee Show",
    "Timcast IRL",
    "The Diary Of A CEO",
    "CreepCast",
    "Karen Read",
    "Murder, Mystery & Makeup",
    "The Tucker Carlson Show",
    "The Megyn Kelly Show",
    "Gil’s Arena",
    "Reality Check with Ross Coulthart",
    "Lex Fridman Podcast",
    "It Is What It Is",
    "Bad Friends Podcast",
    "60 Minutes",
    "PBD Podcast",
    "A Closer Look – Late Night with Seth Meyers",
    "Nightcap",
    "Just Trish",
    "The Lets Read Podcast",
    "IHIP News",
    "Law&Crime Sidebar with Jesse Weber",
    "Unsubscribe Podcast",
    "The Bulwark Podcast with Tim Miller",
    "The Philip DeFranco Show",
    "The Yak",
    "Smosh Mouth",
    "NBC Nightly News with Lester Holt",
    "Crime Stories with Nancy Grace",
    "Breaking Points",
    "Timcast News Stories",
    "Cancelled with Tana Mongeau & Brooke Schofield",
    "True Crime with Kendall Rae",
    "Dark History",
    "Julian Dorey Podcast",
    "Authorized Account",
    "StarTalk Podcast",
    "Distractible",
    "Serialously with Annie Elise",
    "TigerBelly",
    "The Joe Budden Podcast",
    "Democracy Now!",
    "Matt and Shane’s Secret Podcast",
    "Triggernometry",
    "On Purpose Podcast",
    "rSlash",
    "The 85 South Comedy Show",
    "You Should Know Podcast",
    "Power Hour",
    # Top 61–100 (complément au-delà de 60)
    "Emergency Intercom",
    "Ear Biscuits",
    "Hello Internet",
    "This is Gavin Newsom",
    "Funky Friday",
    # et compléments courants pour atteindre 100
    "Impaulsive",
    "Chuckle Sandwich",
    "Zach Sang Show",
    "TigerBelly",          # déjà listé — doublon évité
    "Jenna & Julien Podcast",
    "Psychobabble",
    "The Morning Toast",
    "Dear Hank & John",
    "Not Too Deep",
    "Adventures in Roommating",
    "The True Geordie Podcast",
    "Podcast Français Facile",
    "Français avec Pierre",
    "Français Authentique",
    "Learn French With Alexa",
    "FrenchPod101",
    "Oh La La, I Speak French!",
    "Parlez‑vous French?",
    "Comme Une Française",
    "InnerFrench",
    "HugoDécrypte",
    "Zack en Roue Libre",
    "La Boîte à curiosités",
    "Radio K7",
    "Mind Gap",
    "The Rest Is History",
    "No Such Thing as a Fish",
    "Conan O’Brien Needs A Friend",
    "Rotten Mango",        # déjà listé — doublon évité
    "Mind Pump"
]


addYoutubeChannelIdToBdd(podcast_channels)

