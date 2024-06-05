import time
import datetime
import configparser

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

import __string as string
import __os as os


domain = "www.diepxuan.com"
lstPage = []
lstExcept = [
    "diepxuan.com/customer/account",
    "diepxuan.com/no-route",
    "diepxuan.com/checkout",
]


class Page:
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

        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(2)

        self.driver.get(self.url)
        time.sleep(1)
        self.pageLoaded()
        lstPage = lstPage + [self.url]
        print(f"{datetime.datetime.now()} Visited: {self.driver.title} - {self.url}")
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
            Page(url).crawl()

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
        except:
            title = ""
        if title:
            return True
        return False
