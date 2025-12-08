import time
import json
import re
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _try_click(driver, element):
    try:
        element.click()
        return True
    except ElementNotInteractableException:
        try:
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception:
            return False
    except Exception:
        return False


def _accept_cookies(driver, timeout=5) -> bool:
    wait = WebDriverWait(driver, timeout)
    selectors = [
        "//button[contains(., 'Accepter')]",
        "//button[contains(., 'Tout accepter')]",
        "//button[contains(., 'Accept all')]",
        "//button[contains(., 'I Agree')]",
    ]
    for sel in selectors:
        try:
            el = wait.until(EC.presence_of_element_located((By.XPATH, sel)))
            try:
                clickable = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, sel)))
                if _try_click(driver, clickable):
                    time.sleep(0.5)
                    return True
            except TimeoutException:
                if _try_click(driver, el):
                    time.sleep(0.5)
                    return True
        except TimeoutException:
            continue
        except NoSuchElementException:
            continue
    return False


def get_channel_id(name: str):
    try:
        driver = webdriver.Safari()
        url = f"https://www.youtube.com/@{name}/about"
        driver.get(url)
        time.sleep(1)

        if not _accept_cookies(driver):
            logging.warning(f"Could not accept cookies for {name}")
            return None

        time.sleep(1)

        json_information_about_youtubeur_xpath = "//script[contains(text(), 'ytInitialData')]/text()"
        json_element = driver.find_element(By.XPATH, json_information_about_youtubeur_xpath)
        script_content = json_element.get_attribute("textContent")

        match = re.search(r'var\s+ytInitialData\s*=\s*(\{.*\});?', script_content, re.DOTALL)

        if not match:
            logging.error(f"ytInitialData not found in script for {name}")
            return None

        try:
            data = json.loads(match.group(1))
            return data["onResponseReceivedEndpoints"][0]["showEngagementPanelEndpoint"]["engagementPanel"]["engagementPanelSectionListRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["aboutChannelRenderer"]["metadata"]["aboutChannelViewModel"]["channelId"]
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing failed for {name}: {e}")
            return None

    except Exception as e:
        logging.exception(f"Error retrieving channel ID for {name}: {e}")
        return None
    finally:
        if driver:
            driver.quit()
