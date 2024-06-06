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
import __config as config


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
        self.path = self.url.split("/")[-1].split(".")[0]

    def links(self) -> list:
        global lstPage
        links = []

        self.browserOpen()

        self.driver.get(self.url)
        # time.sleep(1)
        if self.productChecker():
            _config = config.get(self.path)
            _config["DEFAULT"]["url"] = self.url
            _config["DEFAULT"]["lastOpen"] = datetime.datetime.now()
            config.set(_config)
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
        self.browserClose()
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

    def browserOpen(self):
        mode = os.environ.get("MODE", "developer")
        options = Options()
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference("javascript.enabled", mode == "product")
        options.profile = firefox_profile
        options.add_argument("-headless")

        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(2)

    def browserClose(self):
        self.driver.quit()

    def productChecker(self) -> bool:
        try:
            xpath = "//div[@class='product-info-main']//h1[@class='page-title']"
            title = self.driver.find_element(By.XPATH, xpath).text
        except:
            title = ""
        if title:
            return True
        return False
