import uuid
import requests
import xml.etree.ElementTree as Et

from langdetect import detect
from dateutil import parser

from config import db
from configFiles.models import CustomRssFlow, RssFlowLibrary


def find_filter(list_of_filter,flow_id):
    for filters in list_of_filter:
        if filters["FlowId"] == flow_id:
            return filters
    return None

def parse_iso_date(date_str):
    try:
        dt = parser.isoparse(date_str)
    except ValueError:
        dt = parser.parse(date_str)
    return dt.isoformat()

def recup_info_rss_flow(url):

    article_list = []
    response = requests.get(url)
    root = Et.fromstring(response.text)
    channel = root.find("channel")
    rss_flow_library_id = db.query(RssFlowLibrary).filter(RssFlowLibrary.flowLink == url).first().rssFlowLibraryId
    if channel is not None:
        for item in channel.findall("item"):
            article = {
                "title": item.find("title").text,
                "publicationDate": parse_iso_date(item.find("pubDate").text),
                "link": item.find("link").text,
                "description": item.find("description").text,
                "language": detect(item.find("description").text),
                "rssFlowLibraryId": rss_flow_library_id,
            }
            article_list.append(article)
    return article_list

def recup_info_youtube_rss_flow(channel_id):
    videos_list = []
    namespaces = {
        'atom': 'https://www.w3.org/2005/Atom',
        'yt': 'https://www.youtube.com/xml/schemas/2015',
        'media': 'https://search.yahoo.com/mrss/'
    }
    response = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
    root = Et.fromstring(response.text)
    rss_flow_library_id = db.query(RssFlowLibrary).filter(RssFlowLibrary.flowLink.contains("https://youtube.com")).first()
    for entry in root.findall("atom:entry",namespaces):
        video = {
            "title": entry.find("atom:title", namespaces).text,
            "link": entry.find("atom:link", namespaces).attrib["href"],
            "publicationDate": parse_iso_date(entry.find("atom:published", namespaces).text),
            "language": detect(entry.find("atom:title", namespaces).text),
            "rssFlowLibraryId": rss_flow_library_id,
            "description": (
                entry.find("media:group/media:description", namespaces).text
                if entry.find("media:group/media:description", namespaces) is not None and
                   entry.find("media:group/media:description", namespaces).text is not None
                else "No description is available"
            ),
        }
        videos_list.append(video)
    return videos_list

def create_personal_flow(list_selectionned_flow,user_id,filters_list):
    for flow in list_selectionned_flow:
        filter_find = find_filter(filters_list, flow["FlowId"])
        sort_data = ""
        match flow["tag"] :
            case "Classic":
                data = recup_info_rss_flow(flow["link"])
                sort_data = filter_rss_flow(filter_find,data)
            case "Youtube" :
                data = recup_info_youtube_rss_flow(flow["link"])
                sort_data = filter_rss_flow(filter_find,data)
        for item in sort_data:
            existing_item = db.query(CustomRssFlow).filter(
                CustomRssFlow.articleLink == item.get("link"),
                CustomRssFlow.userId == user_id
            ).first()
            if existing_item is None:
                new_item = CustomRssFlow(
                    customRssFlowId = str(uuid.uuid4()),
                    articleTitle = item.get("title"),
                    articlePublicationDate = item.get("publicationDate"),
                    articleLink = item.get("link"),
                    articleDescription = item.get("description"),
                    articleLanguage = item.get("language"),
                    rssFlowLibraryId = item.get("rssFlowLibraryId"),
                    userId = user_id
                )
                db.add(new_item)

        db.commit()

def filter_rss_flow(filters,selectionned_article_list):
    final_articles_list = []
    for article in selectionned_article_list:
        if filters.get("keywords") != "Nothing":
            keywords_list = filters.get("keywords").split(";")
            for keyword in keywords_list:
                if keyword.lower() in article.get("title").lower() or keyword.lower() in article.get("description").lower():
                    break
        else:
            if filters.get("language") != "Nothing":
                if article.get("language") == filters.get("language"):
                    final_articles_list.append(article)
            else :
                final_articles_list.append(article)

    return final_articles_list

