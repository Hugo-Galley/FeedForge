import uuid
import requests
import xml.etree.ElementTree as ET
from config import db
from models import CustomRssFlow, RssFlowLibrary
from langdetect import detect
from dateutil import parser

def findFilter(listOfFiler,flowId):
    for filter in listOfFiler:
        if filter["FlowId"] == flowId:
            return filter

def parse_iso_date(date_str):
    try:
        dt = parser.isoparse(date_str)
    except Exception:
        dt = parser.parse(date_str)
    return dt.isoformat()

def recupInfoFromRssFlow(url):

    listOfArticle = []
    response = requests.get(url)
    root = ET.fromstring(response.text)
    channel = root.find("channel")
    rssFlowLibraryId = db.query(RssFlowLibrary).filter(RssFlowLibrary.flowLink == url).first().rssFlowLibraryId
    if channel is not None:
        for item in channel.findall("item"):
            article = {}
            article["title"] = item.find("title").text
            article["publicationDate"] = parse_iso_date(item.find("pubDate").text)
            article["link"] = item.find("link").text
            article["description"] = item.find("description").text
            article["language"] = detect(article["description"])
            article["rssFlowLibraryId"] = rssFlowLibraryId
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
    rssFlowLibrairyId = db.query(RssFlowLibrary).filter(RssFlowLibrary.flowLink.contains("https://youtube.com")).first()
    for entry in root.findall("atom:entry",namespaces):
        video = {}
        video["title"] = entry.find("atom:title", namespaces).text
        video["link"] = entry.find("atom:link", namespaces).attrib["href"]
        video["description"] = entry.find("media:group/media:description", namespaces)
        if video["description"] is not None and video["description"].text is not None:
            video["description"] = video["description"].text
        else:
            video["description"] = "No description is available"
        video["publicationDate"] = parse_iso_date(entry.find("atom:published", namespaces).text)
        video["language"] = detect(video["title"])
        video["rssFlowLibraryId"] = rssFlowLibrairyId
        listOfVideos.append(video)
    return listOfVideos

def CreatePersonalisateFlow(listOfSelectionnedFlow,userId,lisOfFilter):
    for flow in listOfSelectionnedFlow:
        filter = findFilter(lisOfFilter, flow["FlowId"])
        match flow["tag"] :
            case "Classic":
                data = recupInfoFromRssFlow(flow["link"])
                sortData = filterRssFlow(filter,data)
            case "Youtube" :
                data = recupInfoFromYoutubeRssFlow(flow["link"])
                sortData = filterRssFlow(filter,data)
        for item in sortData:
            existingItem = db.query(CustomRssFlow).filter(
                CustomRssFlow.articleLink == item["link"],
                CustomRssFlow.userId == userId
            ).first()
            if existingItem is None:
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

def filterRssFlow(filter,listOfSelectionnedarticle):
    finalListOfArticle = []
    for article in listOfSelectionnedarticle:
        shouldInclude = False
        if filter["keywords"] != "Nothing":
            listOfKeyword = filter["keywords"].split(";")
            for keyword in listOfKeyword:
                if keyword.lower() in article["title"].lower() or keyword.lower() in article["description"].lower():
                    shouldInclude = True
                    break
        else:
            shouldInclude = True
        if shouldInclude:
            if filter["language"] != "Nothing":
                if article["language"] == filter["language"]:
                    finalListOfArticle.append(article)
            else :
                finalListOfArticle.append(article)

    return finalListOfArticle

