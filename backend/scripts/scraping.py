import time
import uuid
import requests
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET
from config import db
from models import RssFlowLibrary

def isXml(rssLink):
    try:
        response = requests.get(rssLink)
        response.raise_for_status()
        fileContent = response.text
        ET.fromstring(fileContent)
        return True
    except (ET.ParseError, requests.RequestException, Exception):
        return False

def scrappRssFlow(xmlFileurl,category):
    atlasRssUrl = f"https://atlasflux.saynete.net/{xmlFileurl}"
    if not isXml(atlasRssUrl):
        return False
    response = requests.get(atlasRssUrl)
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        for flux in root.findall("flux"):
            domains = re.findall(r"^https?:\/\/([^\/]+)",flux.find("adresse").text)
            newRssFlux = RssFlowLibrary(
                rssFlowLibraryId = uuid.uuid4(),
                flowName = flux.find("source").text,
                flowLink = flux.find("adresse").text,
                category = category,
                domains = domains[0],
                logo = f"https://logo.clearbit.com/{domains[0]}"
            )
            db.add(newRssFlux)
            db.commit()
            db.refresh(newRssFlux)
def scrapRssCategory():
    url = "https://atlasflux.saynete.net"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,"html.parser")
        ongleTheme = soup.select_one("#onglet_theme")

        categorys = ongleTheme.find_all(
            lambda tag: tag.has_attr("class") and any(c in ["elem_onss", "elem_onc","elem_ongl"] for c in tag["class"])
        )
        for category in categorys:
            categoryName = category.get_text(strip=True)
            onclick = category.get("onclick", "")
            match = re.search(r"'([^']+\.xml)'", onclick)
            fichier_xml = match.group(1) if match else "N/A"
            scrappRssFlow(fichier_xml,categoryName)

startTime = time.time()
scrapRssCategory()
endTime = time.time()
print(f"Il aura fallu : {endTime - startTime} secondes")

"""
Il faut faire une verification que les liens recuperé contienne bien du xml 
on Teste le lien xml si le contenu recupré retourne True, alors c'est parsable 
"""

