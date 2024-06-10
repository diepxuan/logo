import time
import configparser
import random

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
    config.read(os.path.join(os.dirVids(), "config.ini"))
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
    driver = __browserOpen(url)
    __view_open(urlparse(url).netloc)(driver, url)
    # match urlparse(url).netloc:
    #     case "www.youtube.com":

    #     case "www.facebook.com":
    #         body = driver.find_element(By.TAG_NAME, "body")
    #         body.send_keys(Keys.ESCAPE)
    # time.sleep(400)
    # body = driver.find_element(By.TAG_NAME, "body")
    # body.send_keys(Keys.PAGE_DOWN)
    # body.send_keys(Keys.PAGE_DOWN)
    # body.send_keys(Keys.PAGE_DOWN)
    __browserClose(driver)


def __view_www_facebook_com(driver: webdriver.Chrome, url):
    time.sleep(5)
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ESCAPE)
    time.sleep(400)
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.PAGE_UP)
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)


def __view_www_youtube_com(driver: webdriver.Chrome, url):
    wait = WebDriverWait(driver, 2)
    try:
        video_element = wait.until(
            EC.presence_of_element_located((By.ID, "movie_player"))
        )
        video_element.send_keys(Keys.SPACE)
    except NoSuchElementException:
        print("Couldn't find video element to play.")
        return

    duration_element = driver.find_element(
        By.XPATH, "//span[@class='ytp-time-duration']"
    )
    video_duration_text = duration_element.text

    print(f"Estimated video duration: {video_duration_text}")
    if video_duration_text:
        minutes, seconds = video_duration_text.split(":")
        estimated_wait_time = int(minutes) * 60 + int(seconds) + 10
        time.sleep(estimated_wait_time)
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.PAGE_UP)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)


def __browserClose(driver: webdriver.Chrome):
    # driver.close()
    driver.quit()


def __browserOpen(url="") -> webdriver.Chrome:
    mode = os.environ.get("MODE", "developer")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.implicitly_wait(2)
    if url:
        driver.get(url)
    return driver


def __view_open(section):
    try:
        functions = {
            "www.youtube.com": __view_www_youtube_com,
            "www.facebook.com": __view_www_facebook_com,
        }
        function = functions[section]
        return function
    except:
        return __view_do_nothing


def __view_do_nothing(path):
    return
