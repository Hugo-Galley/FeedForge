import logging
import time
import uuid
import requests
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET
from config import db, setupLog
from configFiles.models import RssFlowLibrary
from utility.time import getTime

setupLog()
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
            testLogo  = requests.get(f"https://logo.clearbit.com/{domains[0]}")
            logging.info(f"On test le logo pour {domains[0]}")
            if testLogo.status_code == 200:
                testLogo = f"https://logo.clearbit.com/{domains[0]}"
                logging.info(f"Loogo trouvé pour {domains[0]}")
            else:
                testLogo = None
            newRssFlux = RssFlowLibrary(
                rssFlowLibraryId = uuid.uuid4(),
                flowName = flux.find("source").text,
                flowLink = flux.find("adresse").text,
                category = category,
                domains = domains[0],
                logo = testLogo
            )
            db.add(newRssFlux)
            db.commit()
            db.refresh(newRssFlux)
            logging.info(f"On ajoute le flux pour {domains[0]}")
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
getTime(endTime-startTime)

