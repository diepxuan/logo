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
    config.read(os.path.join(os.dirVids(), "config.ini"))
    # try:
    #     config.read(os.path.join(os.dirVids(), "config.ini"))
    # except:
    #     config = configparser.ConfigParser(strict=False)
    #     config.read(os.path.join(os.dirVids(), "config.ini"))
    for item in [
        "https://www.youtube.com/watch?v=TtcMm2V0P_A",
        "https://www.facebook.com/share/v/Sx1427JawqaCg8cV/",
    ]:
        __view(item)


def __view(url):
    driver = __browserOpen(url)
    print(url)
    print(driver.title)
    # match urlparse(url).netloc:
    #     case "www.youtube.com":
    #         # wait = WebDriverWait(driver, 10)
    #         play_button = driver.find_element(By.XPATH, '//button[@class="ytp-button"]')
    #         print(play_button)
    #         play_button.click()
    #         driver.save_screenshot(os.path.join(os.dirVids(), "screenshot.png"))
    #         duration_element = wait.until(
    #             EC.presence_of_element_located(
    #                 # (By.XPATH, "//span[@class='ytp-time-duration']")
    #                 (By.XPATH, '//button[@class="ytp-button"]')
    #             )
    #         )
    #         body = driver.find_element(By.TAG_NAME, "body")
    #         body.send_keys(Keys.k)
    #         video_duration_text = duration_element.text

    #         print(f"Estimated video duration: {video_duration_text}")
    #         driver.save_screenshot("screenshot.png")
    #         if video_duration_text:
    #             minutes, seconds = video_duration_text.split(":")
    #             estimated_wait_time = int(minutes) * 60 + int(seconds) + 10

    #         user_interaction_detected = False  # Flag to track user interaction

    #         def check_user_interaction():
    #             global user_interaction_detected
    #             user_interaction_detected = driver.find_element(
    #                 By.TAG_NAME, "body"
    #             ).is_enabled()  # Check if body element is disabled (indicates user interaction)

    #         while not user_interaction_detected:
    #             driver.implicitly_wait(5)  # Check for interaction every 5 seconds
    #             check_user_interaction()

    #         print(
    #             f"Waiting for {estimated_wait_time} seconds (approximate, with buffer)"
    #         )
    #         time.sleep(estimated_wait_time)

    #     case "www.facebook.com":
    #         body = driver.find_element(By.TAG_NAME, "body")
    #         body.send_keys(Keys.ESCAPE)
    # # time.sleep(400)
    # body.send_keys(Keys.PAGE_DOWN)
    # body.send_keys(Keys.PAGE_DOWN)
    # body.send_keys(Keys.PAGE_DOWN)
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
    options.page_load_strategy = "none"
    # options.add_argument("start-maximized")
    # options.add_argument("enable-automation")
    options.add_argument("-headless")
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-browser-side-navigation")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--disable-infobars")
    # options.add_argument("--new-window")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(2)
    if url:
        driver.get(url)
    return driver
