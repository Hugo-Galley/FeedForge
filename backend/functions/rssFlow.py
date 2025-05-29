import uuid

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from config import db
from models import CustomRssFlow, RssFlowLibrary
from langdetect import detect
def recupInfoFromRssFlow(url):

    listOfArticle = []
    response = requests.get(url)
    root = ET.fromstring(response.text)
    channel = root.find("channel")
    if channel is not None:
        for item in channel.findall("item"):
            article = {}
            article["title"] = item.find("title").text
            dt = datetime.strptime(item.find("pubDate").text, "%a, %d %b %Y %H:%M:%S %Z")
            article["publicationDate"] = dt.isoformat()
            article["link"] = item.find("link").text
            article["description"] = item.find("description").text
            article["language"] = detect(article["description"])
            article["rssFlowLibraryId"] = db.query(RssFlowLibrary).filter(RssFlowLibrary.flowLink == url).first()
            listOfArticle.append(article)
    return listOfArticle

def recupInfoFromYoutubeRssFlow(channelId):
    listOfVideos = []
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'yt': 'http://www.youtube.com/xml/schemas/2015',
        'media': 'http://search.yahoo.com/mrss/'
    }
    response = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={channelId}")
    root = ET.fromstring(response.text)
    for entry in root.findall("atom:entry",namespaces):
        video = {}
        video["title"] = entry.find("atom:title", namespaces).text
        video["link"] = entry.find("atom:link", namespaces).attrib["href"]
        video["description"] = entry.find("media:group/media:description", namespaces)
        if video["description"] is not None and video["description"].text is not None:
            video["description"] = video["description"].text
        else:
            video["description"] = "No description is available"
        video["publicationDate"] = entry.find("atom:published", namespaces).text
        video["language"] = detect(video["title"])
        video["rssFlowLibraryId"] = db.query(RssFlowLibrary).filter(RssFlowLibrary.flowLink == "https://youtube.com").first()
        listOfVideos.append(video)
    return listOfVideos

def CreatePersonalisateFlow(listOfSelectionnedFlow,userId):
    for flow in listOfSelectionnedFlow:
        match flow["tag"] :
            case "Classic":
                data = recupInfoFromRssFlow(flow["link"])
            case "Youtube" :
                data = recupInfoFromYoutubeRssFlow(flow["link"])
        for item in data:
            newItem = CustomRssFlow(
                customRssFlowId = uuid.uuid4(),
                articleTitle = item["title"],
                articlePublicationDate = item["publicationDate"],
                articleLink = item["link"],
                articleDescription = item["description"],
                articleLanguage = item["language"],
                rssFlowLibraryId = item["rssFlowLibraryId"],
                userId = userId
            )
            db.add(newItem)
            db.commit()
            db.refresh(newItem)




