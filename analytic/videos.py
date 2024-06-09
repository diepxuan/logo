import time
import configparser
import random

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlparse, unquote
from unidecode import unidecode
from datetime import datetime, timedelta

import __string as string
import __os as os
import __config as config
import __levenshtein as levenshtein
import __url as url

lstExcept = [
    "DEFAULT",
    "search",
    "images",
]
step_max = 50
step_index = 0


def crawl():
    """product video searching"""
    config = configparser.ConfigParser()
    try:
        config.read(os.path.join(os.dirVids(), "config.ini"))
    except:
        config = configparser.ConfigParser(strict=False)
        config.read(os.path.join(os.dirVids(), "config.ini"))
    for item in [
        "https://www.youtube.com/watch?v=TtcMm2V0P_A",
        "https://www.facebook.com/share/v/Sx1427JawqaCg8cV/",
    ]:
        __view(item)


def __view(url):
    print(url)
    driver = __browserOpen(url)
    body = driver.find_element(By.TAG_NAME, "body")
    match urlparse(url).netloc:
        case "www.youtube.com":
            body.send_keys(Keys.K)
        case "www.facebook.com":
            body.send_keys(Keys.ESCAPE)
    time.sleep(400)
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    __browserClose(driver)


def __browserClose(driver: webdriver.Firefox):
    # driver.close()
    driver.quit()


def __browserOpen(url="") -> webdriver.Firefox:
    mode = os.environ.get("MODE", "developer")
    options = Options()
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("javascript.enabled", mode == "product")
    options.profile = firefox_profile
    options.add_argument("-headless")
    # options.add_argument("--new-window")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    if url:
        driver.get(url)
    return driver
