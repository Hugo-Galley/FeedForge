import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from langdetect import detect
def recupInfoFromRssFlow(url):
    article = {}
    listOfArticle = []
    response = requests.get(url)
    root = ET.fromstring(response.text)
    channel = root.find("channel")
    if channel is not None:
        for item in channel.findall("item"):
            article["title"] = item.find("title").text
            dt = datetime.strptime(item.find("pubDate").text, "%a, %d %b %Y %H:%M:%S %z")
            article["publicationDate"] = dt.isoformat()
            article["link"] = item.find("link").text
            article["description"] = item.find("description").text
            article["language"] = detect(article["description"])
            listOfArticle.append(article)
    return listOfArticle

