import requests
import xml.etree.ElementTree as ET

url = "https://www.lemonde.fr/rss/une.xml"
response = requests.get(url)
root = ET.fromstring(response.text)
channel = root.find("channel")
if channel is not None:
    for item in channel.findall("item"):
        title = item.find("title").text
        publicationDate = item.find("pubDate")
        link = item.find("link").text
        print(f"On a trouvé l'article {title} publié le {publicationDate} a suivre sur se lien {link}")