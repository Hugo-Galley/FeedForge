import logging
import time
import uuid
import requests
import re

from bs4 import BeautifulSoup
import xml.etree.ElementTree as Et

from config import db, setup_log
from configFiles.models import RssFlowLibrary
from utility.time import get_time

setup_log()
def is_xml(rss_link):
    try:
        response = requests.get(rss_link)
        response.raise_for_status()
        file_content = response.text
        Et.fromstring(file_content)
        return True
    except (Et.ParseError, requests.RequestException, Exception):
        return False

def scrap_rss_flow(xml_file_url,category):
    atlas_rss_url = f"https://atlasflux.saynete.net/{xml_file_url}"
    if not is_xml(atlas_rss_url):
        return False
    response = requests.get(atlas_rss_url)
    if response.status_code == 200:
        root = Et.fromstring(response.text)
        for flux in root.findall("flux"):
            domains = re.findall(r"^https?:([^/]+)",flux.find("adresse").text)
            test_logo  = requests.get(f"https://logo.clearbit.com/{domains[0]}")
            logging.info(f"On test le logo pour {domains[0]}")
            if test_logo.status_code == 200:
                logo = f"https://logo.clearbit.com/{domains[0]}"
                logging.info(f"Loogo trouvé pour {domains[0]}")
            else:
                logo = None
            new_rss_flux = RssFlowLibrary(
                rssFlowLibraryId = str(uuid.uuid4()),
                flowName = flux.find("source").text,
                flowLink = flux.find("adresse").text,
                category = category,
                domains = domains[0],
                logo = logo
            )
            db.add(new_rss_flux)
            db.commit()
            logging.info(f"On ajoute le flux pour {domains[0]}")
    else:
        return logging.error(f"Code d'erreur non valide {response.status_code}")
def scrap_rss_category():
    url = "https://atlasflux.saynete.net"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,"html.parser")
        onglet_theme = soup.select_one("#onglet_theme")

        categorys = onglet_theme.find_all(
            lambda tag: tag.has_attr("class") and any(c in ["elem_onss", "elem_onc","elem_ongl"] for c in tag["class"])
        )
        for category in categorys:
            category_name = category.get_text(strip=True)
            onclick = category.get("onclick", "")
            match = re.search(r"'([^']+\.xml)'", onclick)
            fichier_xml = match.group(1) if match else "N/A"
            scrap_rss_flow(fichier_xml,category_name)

startTime = time.time()
scrap_rss_category()
endTime = time.time()
get_time(endTime-startTime)

