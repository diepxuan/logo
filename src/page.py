import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

import __string as string
import __os as os


domain = "www.diepxuan.com"
lstPage = []
lstExcept = [
    "diepxuan.com/customer/account",
    "diepxuan.com/customer/account",
    "diepxuan.com/no-route",
]


class Page:
    def __init__(self, driver: webdriver.Firefox, url):
        self.driver = driver
        self.url = url

    def links(self):
        global lstPage
        links = []
        time.sleep(1)
        self.driver.get(self.url)
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
        return list(set(links))

    def crawl(self):
        for url in [url for url in self.links() if url not in lstPage]:
            Page(self.driver, url).crawl()

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
            print(path)
            path = os.dirImg(path)

    def productChecker(self):
        try:
            xpath = "//div[@class='product-info-main']//h1[@class='page-title']"
            title = self.driver.find_element(By.XPATH, xpath).text
        except:
            title = ""
        if title:
            return True
        return False
