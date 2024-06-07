import time
import datetime
import configparser

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlparse
from unidecode import unidecode

import __string as string
import __os as os
import __levenshtein as levenshtein


def crawl():
    for item in [
        item for item in os.listdir(os.dirImg()) if os.path.isdir(os.dirImg(item))
    ]:
        __search_init(item)


def __search_init(path):
    # path = os.dirImg(path)
    title = path.replace("-", " ")
    print(f"Searching {title}")
    mode = os.environ.get("MODE", "developer")
    options = Options()
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("javascript.enabled", mode == "product")
    options.profile = firefox_profile
    options.add_argument("-headless")
    # options.add_argument("--new-window")

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(2)

    # try:
    __search_query(driver, title)
    # except NoSuchElementException as e:
    # print(e)

    driver.quit()


def __search_query(driver: webdriver.Firefox, title):
    driver.get("https://www.google.com/")
    time.sleep(1)

    wait = WebDriverWait(driver, 10)

    search_xpath = "//textarea[@name='q']"
    search_field = wait.until(EC.presence_of_element_located((By.XPATH, search_xpath)))
    search_field.send_keys(title)
    search_field.send_keys(Keys.ENTER)

    result_xpath = "//div[@id='search']/div/div/div"
    search_results = wait.until(EC.presence_of_element_located((By.ID, "search")))
    body = driver.find_element(By.TAG_NAME, "body")
    for i in range(5):
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    search_results = driver.find_elements(By.XPATH, result_xpath)
    for search_result in [
        search_result for search_result in search_results if search_result.text.strip()
    ]:
        try:
            search_element = search_result.find_element(By.TAG_NAME, "a")
            search_url = search_element.get_attribute("href")
            search_title = search_result.find_element(By.TAG_NAME, "h3").text
            search_text = search_result.find_element(By.TAG_NAME, "cite").text
            search_match = levenshtein.percentage(
                unidecode(search_title).lower(), title
            )
            search_match_txt = "{:.1f}%".format(search_match)
            print(f" * {search_match_txt} {search_title}")
            print(f"   - {search_text}")
            print(f"   - {search_url}")
            if search_match < 70:
                continue
            search_element.click()
            time.sleep(3)
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            break
        except NoSuchElementException:
            continue
        except StaleElementReferenceException:
            continue


domain = "www.diepxuan.com"
lstPage = []
lstExcept = [
    "diepxuan.com/customer/account",
    "diepxuan.com/customer/account",
    "diepxuan.com/no-route",
]


class Search:
    def __init__(self, url):
        self.url = url

    def links(self):
        global lstPage
        links = []

        mode = os.environ.get("MODE", "developer")
        options = Options()
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference("javascript.enabled", mode == "product")
        options.profile = firefox_profile
        options.add_argument("-headless")
        # options.add_argument("--new-window")

        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(2)

        self.driver.get(self.url)
        time.sleep(1)
        self.pageLoaded()
        lstPage = lstPage + [self.url]
        print(f"{datetime.datetime.now()} Searching: {self.driver.title} - {self.url}")
        for link in self.driver.find_elements(By.TAG_NAME, "a"):
            try:
                url = link.get_attribute("href")
            except:
                url = ""
            url = self.urlChecker(url=url)
            if url:
                links = links + [url]
        self.driver.quit()
        return list(set(links))

    def crawl(self):
        for url in [url for url in self.links() if url not in lstPage]:
            Search(url).crawl()

    def urlChecker(self, url=""):
        if url:
            if len(url.strip()) == 0:
                url = self.url
        if not url:
            return ""
        url = url.split("#")[0].rstrip("/")
        if not urlparse(url).netloc == domain:
            return ""
        if url in lstPage:
            return ""
        if any(item for item in lstExcept if item in url):
            return ""
        return url

    def pageLoaded(self):
        if self.productChecker():
            path = self.url.split("/")[-1].split(".")[0]
            path = os.dirImg(path)

            configPath = os.path.join(path, "config.ini")
            config = configparser.ConfigParser()
            config.read(configPath)
            config["DEFAULT"]["url"] = self.url
            with open(configPath, "w") as configfile:
                config.write(configfile)

    def productChecker(self):
        try:
            xpath = "//div[@class='product-info-main']//h1[@class='page-title']"
            title = self.driver.find_element(By.XPATH, xpath).text
            print(title)
        except:
            title = ""
        if title:
            return True
        return False
