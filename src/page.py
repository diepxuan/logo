import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

domain = "www.diepxuan.com"
lstPage = []
lstExcept = [
    "diepxuan.com/customer/account",
    "diepxuan.com/customer/account",
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
        if not any(item not in url for item in lstExcept):
            return ""
        return url
