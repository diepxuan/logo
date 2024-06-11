import time
import configparser
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlparse
from datetime import datetime, timedelta

import __string as string
import __os as os
import __config as config
import __url as Url


domain = "www.diepxuan.com"
lstPage = []
lstExcept = [
    "diepxuan.com/catalog/product_compare",
    "diepxuan.com/stores/store/redirect",
    "diepxuan.com/customer/account",
    "diepxuan.com/no-route",
    "diepxuan.com/checkout",
]
step_max = 50
step_index = 0
driver: webdriver.Chrome = None
url = f"https://www.diepxuan.com"
path = url.split("/")[-1].split(".")[0]


def __crawl():
    global lstPage, step_index
    print(f"{datetime.now()} Visited: {driver.title} - {driver.current_url}")

    link = driver.current_url.split("#")[0].rstrip("/")
    path = link.split("/")[-1].split(".")[0]
    if __productChecker():
        _config = config.get(path)
        _config["DEFAULT"]["url"] = f"{driver.current_url}"
        _config["DEFAULT"]["lastOpen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if config.valid(_config):
            config.set(_config)
        step_index += 1
        lstPage = lstPage + [link]

    if step_index > step_max:
        return

    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.TAG_NAME, "main"))
    )
    nav_link = driver.find_elements(By.CSS_SELECTOR, "nav.navigation a")
    prod_link = driver.find_elements(By.CSS_SELECTOR, "main.page-main a")
    links = [_link for _link in prod_link] + [_link for _link in nav_link]
    links = [_link for _link in list(set(links))]
    random.shuffle(links)

    while len(links) > 0:
        link = random.choice(links)
        href = __url(link.get_attribute("href"))
        try:
            if href:
                link.click()
                time.sleep(2)
                return __crawl()
        except:
            pass
        links.remove(link)


def crawl():
    __browserOpen()
    driver.get(url)
    __crawl()
    __browserClose()


def __url(link):
    if __urlChecker(link):
        return link
    return None


def __urlChecker(link):
    if not link:
        return False
    link = link.split("#")[0].rstrip("/")
    if not Url.valid(link):
        return False
    if link in lstPage:
        return False
    if any(item for item in lstExcept if item in link or link in item):
        return False
    path = link.split("/")[-1].split(".")[0]
    if not config.isOld(path):
        if config.valid(config.get(path)):
            return False
    return True


def __browserOpen():
    global driver
    mode = os.environ.get("MODE", "developer")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.implicitly_wait(2)
    return driver


def __browserClose():
    driver.quit()


def __productChecker() -> bool:
    try:
        xpath = "//div[@class='product-info-main']//h1[@class='page-title']"
        title = driver.find_element(By.XPATH, xpath).text
    except:
        title = ""
    if title:
        return True
    return False
